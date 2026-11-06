"""Control del consumo y aplicación de los límites comunes de ejecución."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from .configuracion import ConfiguracionExperimento
from .errores import CapaComunError
from .traza import EscritorTraza


@dataclass(frozen=True, slots=True)
class AutorizacionModelo:
    autorizada: bool
    max_output_tokens: int
    motivo: str | None


class ControlLimites:
    """Mantiene contadores únicos y emite avisos comparables en la traza."""

    def __init__(
        self,
        configuracion: ConfiguracionExperimento,
        traza: EscritorTraza,
    ) -> None:
        """Inicializa los contadores de consumo y los registros de avisos."""
        self.configuracion = configuracion
        self.traza = traza
        self._inicio = time.perf_counter()
        self.model_calls = 0
        self.model_calls_por_rol = {
            "planner": 0,
            "analyst_initial": 0,
            "reviewer": 0,
            "analyst_correction": 0,
        }
        self.tool_calls = 0
        self.tool_calls_por_rol = {
            rol: {herramienta: 0 for herramienta in ("inspect_dataset", "execute_python", "read_output", "validate_outputs")}
            for rol in self.model_calls_por_rol
        }
        self.tool_successes = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_tokens = 0
        self.cached_input_tokens = 0
        self.reasoning_output_tokens = 0
        self.retries = 0
        self.error_ids: set[str] = set()
        self.python_time_seconds = 0.0
        self.cost_usd = Decimal("0")
        self._avisados: set[str] = set()
        self._alcanzados: set[str] = set()

    def elapsed_seconds(self) -> float:
        """Devuelve los segundos transcurridos desde el inicio del control."""
        return max(time.perf_counter() - self._inicio, 0.0)

    def autorizar_modelo(
        self,
        rol: str,
        fase: str,
        input_tokens_estimados: int,
        output_tokens_solicitados: int | None = None,
    ) -> AutorizacionModelo:
        """Comprueba si puede iniciarse una petición y ajusta su máximo de salida."""
        if rol not in self.model_calls_por_rol:
            raise CapaComunError(f"Rol no reconocido para límites: {rol}")
        if not isinstance(input_tokens_estimados, int) or isinstance(input_tokens_estimados, bool) or input_tokens_estimados < 0:
            raise CapaComunError("input_tokens_estimados debe ser un entero no negativo")
        if output_tokens_solicitados is not None and (
            not isinstance(output_tokens_solicitados, int)
            or isinstance(output_tokens_solicitados, bool)
            or output_tokens_solicitados < 1
        ):
            raise CapaComunError("output_tokens_solicitados debe ser un entero positivo")

        limites = self.configuracion.datos["limits"]
        if self.elapsed_seconds() >= limites["time_seconds"]["run"]:
            self._emitir_limite("run_time", limites["time_seconds"]["run"], self.elapsed_seconds(), "seconds", "run", fase, rol, True)
            return AutorizacionModelo(False, 0, "run_time")
        if self.model_calls >= limites["model_requests"]["run"]:
            self._emitir_limite("model_calls", limites["model_requests"]["run"], self.model_calls, "calls", "run", fase, rol, True)
            return AutorizacionModelo(False, 0, "model_calls")
        limite_rol = limites["model_requests"]["roles"][rol]
        if self.model_calls_por_rol[rol] >= limite_rol:
            self._emitir_limite(f"model_calls_{rol}", limite_rol, self.model_calls_por_rol[rol], "calls", "role", fase, rol, True)
            return AutorizacionModelo(False, 0, f"model_calls_{rol}")
        if input_tokens_estimados > limites["tokens"]["request_input_estimate_max"]:
            self._emitir_limite("request_input_tokens", limites["tokens"]["request_input_estimate_max"], input_tokens_estimados, "tokens", "request", fase, rol, True)
            return AutorizacionModelo(False, 0, "request_input_tokens")

        limites_tokens = limites["tokens"]
        entrada_proyectada = self.input_tokens + input_tokens_estimados
        if entrada_proyectada > limites_tokens["run_input_max"]:
            self._emitir_limite(
                "input_tokens",
                limites_tokens["run_input_max"],
                entrada_proyectada,
                "tokens",
                "run",
                fase,
                rol,
                True,
            )
            return AutorizacionModelo(False, 0, "input_tokens")

        restante = limites_tokens["run_output_max"] - self.output_tokens
        reserva = limites_tokens["minimum_run_output_remaining_for_new_request"]
        if restante < reserva:
            self._emitir_limite("output_tokens", limites_tokens["run_output_max"], self.output_tokens, "tokens", "run", fase, rol, True)
            return AutorizacionModelo(False, 0, "output_tokens")

        restante_total = limites_tokens["run_total_max"] - self.total_tokens - input_tokens_estimados
        if restante_total <= 0:
            self._emitir_limite(
                "total_tokens",
                limites_tokens["run_total_max"],
                self.total_tokens + input_tokens_estimados,
                "tokens",
                "run",
                fase,
                rol,
                True,
            )
            return AutorizacionModelo(False, 0, "total_tokens")

        solicitado = (
            output_tokens_solicitados
            if output_tokens_solicitados is not None
            else limites_tokens["request_output_max"]
        )
        max_output = min(
            solicitado,
            limites_tokens["request_output_max"],
            restante,
            restante_total,
        )
        max_output = self._ajustar_por_coste(input_tokens_estimados, max_output)
        if max_output < 1:
            self._emitir_limite("cost", float(self.configuracion.datos["pricing"]["budgets"]["maximum_per_run"]), float(self.cost_usd), "USD", "run", fase, rol, True)
            return AutorizacionModelo(False, 0, "cost")
        return AutorizacionModelo(True, max_output, None)

    def registrar_modelo_iniciado(self, rol: str, fase: str) -> None:
        """Incrementa el contador de peticiones al modelo y comprueba si corresponde emitir un aviso."""
        self.model_calls += 1
        self.model_calls_por_rol[rol] += 1
        limites = self.configuracion.datos["limits"]["model_requests"]
        self._comprobar_aviso("model_calls", limites["run"], self.model_calls, "calls", "run", fase, rol)
        self._comprobar_aviso(f"model_calls_{rol}", limites["roles"][rol], self.model_calls_por_rol[rol], "calls", "role", fase, rol)

    def registrar_uso_modelo(
        self,
        input_tokens: int,
        output_tokens: int,
        total_tokens: int,
        cached_input_tokens: int | None,
        reasoning_output_tokens: int | None,
        fase: str,
        rol: str,
    ) -> Decimal:
        """Acumula los tokens y el coste y comprueba los límites correspondientes."""
        valores = (input_tokens, output_tokens, total_tokens)
        if any(not isinstance(valor, int) or isinstance(valor, bool) or valor < 0 for valor in valores):
            raise CapaComunError("Los tokens informados deben ser enteros no negativos")
        if total_tokens != input_tokens + output_tokens:
            raise CapaComunError("total_tokens debe coincidir con input_tokens más output_tokens")
        cached = cached_input_tokens or 0
        reasoning = reasoning_output_tokens or 0
        if cached < 0 or cached > input_tokens or reasoning < 0 or reasoning > output_tokens:
            raise CapaComunError("El desglose de tokens no es coherente")

        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.total_tokens += total_tokens
        self.cached_input_tokens += cached
        self.reasoning_output_tokens += reasoning
        coste = self._calcular_coste(input_tokens, output_tokens, cached)
        self.cost_usd += coste

        limites = self.configuracion.datos["limits"]["tokens"]
        for tipo, configurado, observado in (
            ("input_tokens", limites["run_input_max"], self.input_tokens),
            ("output_tokens", limites["run_output_max"], self.output_tokens),
            ("total_tokens", limites["run_total_max"], self.total_tokens),
        ):
            self._comprobar_aviso(tipo, configurado, observado, "tokens", "run", fase, rol)
            if observado >= configurado:
                self._emitir_limite(tipo, configurado, observado, "tokens", "run", fase, rol, True)

        coste_maximo = Decimal(str(self.configuracion.datos["pricing"]["budgets"]["maximum_per_run"]))
        coste_aviso = Decimal(str(self.configuracion.datos["pricing"]["budgets"]["warning_per_run"]))
        if self.cost_usd >= coste_aviso:
            self._emitir_limite("cost_warning", float(coste_aviso), float(self.cost_usd), "USD", "run", fase, rol, False)
        if self.cost_usd >= coste_maximo:
            self._emitir_limite("cost", float(coste_maximo), float(self.cost_usd), "USD", "run", fase, rol, True)
        return coste

    def autorizar_herramienta(
        self,
        rol: str,
        herramienta: str,
        fase: str,
        automatic: bool = False,
    ) -> bool:
        """Comprueba las cuotas globales y por rol para solicitar una herramienta."""
        if rol not in self.tool_calls_por_rol or herramienta not in self.tool_calls_por_rol[rol]:
            raise CapaComunError("Rol o herramienta no reconocidos")
        if automatic and herramienta == "validate_outputs":
            return True
        limites = self.configuracion.datos["limits"]["model_requested_tool_calls"]
        if self.tool_calls >= limites["run"]:
            self._emitir_limite("tool_calls", limites["run"], self.tool_calls, "calls", "run", fase, rol, True)
            return False
        limite_rol = limites["roles"][rol][herramienta]
        observado = self.tool_calls_por_rol[rol][herramienta]
        if observado >= limite_rol:
            self._emitir_limite(f"tool_calls_{rol}_{herramienta}", limite_rol, observado, "calls", "role", fase, rol, True)
            return False
        return True

    def registrar_herramienta_iniciada(
        self,
        rol: str,
        herramienta: str,
        fase: str,
        automatic: bool = False,
    ) -> None:
        """Incrementa el contador de llamadas a herramientas, sin incluir las validaciones automáticas."""
        if automatic and herramienta == "validate_outputs":
            return
        self.tool_calls += 1
        self.tool_calls_por_rol[rol][herramienta] += 1
        limites = self.configuracion.datos["limits"]["model_requested_tool_calls"]
        self._comprobar_aviso("tool_calls", limites["run"], self.tool_calls, "calls", "run", fase, rol)

    def registrar_resultado_herramienta(self, success: bool) -> None:
        """Incrementa el contador de llamadas finalizadas correctamente."""
        if success:
            self.tool_successes += 1

    def registrar_reintento(self, fase: str, rol: str) -> bool:
        """Comprueba el máximo global y contabiliza un nuevo reintento."""
        limite = self.configuracion.datos["limits"]["retries"]["run_total"]
        if self.retries >= limite:
            self._emitir_limite("retries", limite, self.retries, "retries", "run", fase, rol, True)
            return False
        self.retries += 1
        self._comprobar_aviso("retries", limite, self.retries, "retries", "run", fase, rol)
        return True

    def registrar_error(self, error_id: str, severity: str) -> None:
        """Cuenta los errores y excluye las advertencias."""
        if severity != "warning":
            self.error_ids.add(error_id)

    def registrar_tiempo_python(self, segundos: float, fase: str, rol: str) -> None:
        """Acumula el tiempo de Python y comprueba su límite."""
        if segundos < 0:
            raise CapaComunError("El tiempo de Python no puede ser negativo")
        self.python_time_seconds += segundos
        limite = self.configuracion.datos["tools"]["execute_python"]["cumulative_time_max_seconds"]
        self._comprobar_aviso("python_time", limite, self.python_time_seconds, "seconds", "run", fase, rol)
        if self.python_time_seconds >= limite:
            self._emitir_limite("python_time", limite, self.python_time_seconds, "seconds", "run", fase, rol, True)

    def resumen(self) -> dict[str, Any]:
        """Devuelve los totales de consumo, errores y reintentos."""
        return {
            "model_calls": self.model_calls,
            "turns": self.model_calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "reasoning_output_tokens": self.reasoning_output_tokens,
            "estimated_cost": {
                "amount": float(self.cost_usd),
                "currency": self.configuracion.datos["pricing"]["currency"],
                "pricing_table_id": self.configuracion.datos["pricing"]["table_version"],
            },
            "tool_calls": self.tool_calls,
            "tool_successes": self.tool_successes,
            "errors": len(self.error_ids),
            "retries": self.retries,
            "python_time_seconds": round(self.python_time_seconds, 6),
        }

    @property
    def limites_alcanzados(self) -> tuple[str, ...]:
        """Devuelve los límites que han provocado un bloqueo."""
        return tuple(sorted(self._alcanzados))

    def _calcular_coste(self, input_tokens: int, output_tokens: int, cached: int) -> Decimal:
        """Calcula el coste según los tokens de entrada, caché y salida."""
        precios = self.configuracion.datos["pricing"]["per_million_tokens"]
        no_cached = input_tokens - cached
        millon = Decimal("1000000")
        return (
            Decimal(no_cached) * Decimal(str(precios["input_uncached"]))
            + Decimal(cached) * Decimal(str(precios["input_cached"]))
            + Decimal(output_tokens) * Decimal(str(precios["output"]))
        ) / millon

    def _ajustar_por_coste(self, input_tokens: int, max_output: int) -> int:
        """Reduce la salida permitida para respetar el presupuesto restante."""
        precios = self.configuracion.datos["pricing"]["per_million_tokens"]
        maximo = Decimal(str(self.configuracion.datos["pricing"]["budgets"]["maximum_per_run"]))
        coste_entrada = Decimal(input_tokens) * Decimal(str(precios["input_uncached"])) / Decimal("1000000")
        disponible = maximo - self.cost_usd - coste_entrada
        if disponible <= 0:
            return 0
        asequible = math.floor(
            disponible * Decimal("1000000") / Decimal(str(precios["output"]))
        )
        return min(max_output, max(asequible, 0))

    def _comprobar_aviso(
        self,
        tipo: str,
        configurado: int | float,
        observado: int | float,
        unidad: str,
        alcance: str,
        fase: str,
        rol: str,
    ) -> None:
        """Comprueba si el consumo alcanza el umbral de advertencia."""
        umbral = float(self.configuracion.datos["limits"]["warning_threshold_ratio"])
        if observado >= configurado * umbral:
            self._emitir_limite(tipo, configurado, observado, unidad, alcance, fase, rol, False)

    def _emitir_limite(
        self,
        tipo: str,
        configurado: int | float,
        observado: int | float,
        unidad: str,
        alcance: str,
        fase: str,
        rol: str,
        alcanzado: bool,
    ) -> None:
        """Registra el aviso o bloqueo de un límite solo si todavía no se ha registrado."""
        clave = f"{tipo}:{alcance}"
        registrados = self._alcanzados if alcanzado else self._avisados
        if clave in registrados:
            return
        registrados.add(clave)
        if alcanzado:
            self._alcanzados.add(clave)
        self.traza.registrar(
            "limit_reached" if alcanzado else "limit_warning",
            fase,
            "analyst" if rol.startswith("analyst") else rol,
            "common_runtime",
            {
                "limit_type": tipo,
                "configured_value": configurado,
                "unit": unidad,
                "observed_value": observado,
                "scope": alcance,
                "action": "block_new_operation" if alcanzado else "warning",
            },
        )
