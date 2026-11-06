"""Lectura y consulta de los resultados de la ejecución actual."""

from __future__ import annotations

import base64
import json
import random
import re
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from .configuracion import ConfiguracionExperimento
from .ejecucion import ContextoEjecucion
from .utilidades import cargar_json_sin_duplicados, sha256_archivo
from .validacion import _metadatos_png


class ErrorConsulta(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _json_valor(valor: Any) -> Any:
    """Adapta los valores de pandas para incluirlos en la respuesta."""
    if valor is None or valor is pd.NA:
        return None
    if hasattr(valor, "item"):
        try:
            valor = valor.item()
        except (TypeError, ValueError):
            pass
    if isinstance(valor, pd.Timestamp):
        return valor.isoformat()
    try:
        if bool(pd.isna(valor)):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(valor, (str, int, float, bool)):
        return valor
    return str(valor)


def _registros(tabla: pd.DataFrame, posiciones: list[int]) -> list[dict[str, Any]]:
    """Convierte cada fila seleccionada en un diccionario con los nombres y valores de sus columnas."""
    return [
        {
            str(nombre): _json_valor(tabla.iloc[posicion, indice])
            for indice, nombre in enumerate(tabla.columns)
        }
        for posicion in posiciones
    ]


class LectorResultados:
    """Permite consultar los resultados autorizados sin que el modelo elija sus rutas."""

    def __init__(
        self,
        configuracion: ConfiguracionExperimento,
        contexto: ContextoEjecucion,
    ) -> None:
        self.configuracion = configuracion
        self.contexto = contexto
        self._maximo_fragmento = configuracion.datos["limits"]["sizes"][
            "read_output_chunk_max_characters"
        ]

    def consultar(self, argumentos: Mapping[str, Any]) -> dict[str, Any]:
        """Comprueba la consulta y la dirige al lector correspondiente."""
        requeridos = {"artifact", "query", "selector", "cursor"}
        if set(argumentos) != requeridos:
            raise ErrorConsulta(
                "INVALID_ARGUMENT",
                "read_output requiere artifact, query, selector y cursor",
            )
        artifact = argumentos["artifact"]
        query = argumentos["query"]
        selector = argumentos["selector"]
        cursor = argumentos["cursor"]
        if artifact not in {
            "plan",
            "prepared_data",
            "statistics",
            "issues",
            "figures",
            "report",
        }:
            raise ErrorConsulta("INVALID_ARGUMENT", "El artefacto solicitado no está autorizado")
        permitidas = {
            "plan": {"summary", "full", "section", "next"},
            "report": {"summary", "full", "section", "next"},
            "statistics": {"summary", "full", "id", "next"},
            "issues": {"summary", "full", "id", "next"},
            "prepared_data": {"summary"},
            "figures": {"summary", "id"},
        }
        if query not in permitidas[artifact]:
            raise ErrorConsulta(
                "INVALID_ARGUMENT",
                "La consulta no está permitida para el artefacto seleccionado",
            )
        if query in {"id", "section"} and (
            not isinstance(selector, str) or not selector.strip()
        ):
            raise ErrorConsulta("INVALID_ARGUMENT", "La consulta requiere selector")
        if query == "next" and (not isinstance(cursor, str) or not cursor):
            raise ErrorConsulta("INVALID_ARGUMENT", "La consulta next requiere cursor")
        if query not in {"id", "section"} and selector is not None:
            raise ErrorConsulta("INVALID_ARGUMENT", "selector debe ser null para esta consulta")
        if query != "next" and cursor is not None:
            raise ErrorConsulta("INVALID_ARGUMENT", "cursor debe ser null para esta consulta")

        if artifact in {"plan", "report"}:
            return self._markdown(artifact, query, selector, cursor)
        if artifact in {"statistics", "issues"}:
            return self._json(artifact, query, selector, cursor)
        if artifact == "prepared_data":
            return self._prepared_data(query)
        return self._figures(query, selector)

    def _ruta_archivo(self, artifact: str) -> Path:
        """Localiza el archivo solicitado y comprueba que exista y no esté vacío."""
        nombres = {
            "plan": "plan.md",
            "report": "report.md",
            "statistics": "statistics.json",
            "issues": "issues.json",
            "prepared_data": "prepared_data.csv",
        }
        ruta = self.contexto.directorio_salida / nombres[artifact]
        if not ruta.is_file() or ruta.stat().st_size == 0:
            raise ErrorConsulta("NOT_FOUND", "El artefacto solicitado no existe o está vacío")
        return ruta

    def _base(
        self,
        artifact: str,
        query: str,
        content_type: str,
        content: Any,
        sha256: str | None,
        truncated: bool = False,
        next_cursor: str | None = None,
    ) -> dict[str, Any]:
        """Construye la respuesta común de una consulta."""
        return {
            "artifact": artifact,
            "query": query,
            "content_type": content_type,
            "content": content,
            "sha256": sha256,
            "truncated": truncated,
            "next_cursor": next_cursor,
        }

    def _markdown(
        self,
        artifact: str,
        query: str,
        selector: str | None,
        cursor: str | None,
    ) -> dict[str, Any]:
        """Consulta el plan o el informe completo, por secciones o por fragmentos."""
        ruta = self._ruta_archivo(artifact)
        try:
            texto = ruta.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise ErrorConsulta("SCHEMA_ERROR", "El Markdown no utiliza UTF-8") from exc
        hash_archivo = sha256_archivo(ruta)
        if query == "summary":
            encabezados = re.findall(r"(?m)^(#{1,6})\s+(.+?)\s*$", texto)
            return self._base(
                artifact,
                query,
                "markdown",
                {
                    "characters": len(texto),
                    "headings": [
                        {"level": len(marcas), "title": titulo}
                        for marcas, titulo in encabezados
                    ],
                },
                hash_archivo,
            )
        if query == "section":
            contenido = self._extraer_seccion(texto, selector or "")
            return self._paginar(
                artifact,
                query,
                "markdown",
                contenido,
                hash_archivo,
                0,
                "section",
                selector,
            )
        if query == "next":
            estado = self._decodificar_cursor(cursor or "", artifact, hash_archivo)
            if estado["source_query"] == "section":
                texto = self._extraer_seccion(texto, estado["selector"])
            return self._paginar(
                artifact,
                query,
                "markdown",
                texto,
                hash_archivo,
                estado["offset"],
                estado["source_query"],
                estado["selector"],
            )
        return self._paginar(
            artifact,
            query,
            "markdown",
            texto,
            hash_archivo,
            0,
            "full",
            None,
        )

    def _json(
        self,
        artifact: str,
        query: str,
        selector: str | None,
        cursor: str | None,
    ) -> dict[str, Any]:
        """Consulta los resultados JSON completos, resumidos o por identificador."""
        ruta = self._ruta_archivo(artifact)
        try:
            objeto, _ = cargar_json_sin_duplicados(ruta)
        except Exception as exc:
            raise ErrorConsulta("SCHEMA_ERROR", "El artefacto no es JSON estricto") from exc
        hash_archivo = sha256_archivo(ruta)
        if query == "summary":
            contenido = {
                "schema_version": objeto.get("schema_version"),
                "run_id": objeto.get("run_id"),
                "dataset_id": objeto.get("dataset_id"),
            }
            if artifact == "statistics":
                contenido.update(
                    {
                        "analyses_count": len(objeto.get("analyses", [])),
                        "figures_count": len(objeto.get("figures", [])),
                        "limitations_count": len(objeto.get("limitations", [])),
                        "profile": objeto.get("profile"),
                        "preparation_summary": objeto.get("preparation", {}).get("summary"),
                    }
                )
            else:
                contenido.update(
                    {
                        "checks_count": len(objeto.get("checks_performed", [])),
                        "issues_count": len(objeto.get("issues", [])),
                    }
                )
            return self._base(artifact, query, "json", contenido, hash_archivo)
        if query == "id":
            encontrado = self._buscar_id(objeto, selector or "")
            if encontrado is None:
                raise ErrorConsulta("NOT_FOUND", "No existe el identificador solicitado")
            texto = json.dumps(encontrado, ensure_ascii=False, indent=2, allow_nan=False)
            return self._paginar(
                artifact,
                query,
                "json",
                texto,
                hash_archivo,
                0,
                "id",
                selector,
            )
        texto = ruta.read_text(encoding="utf-8")
        if query == "next":
            estado = self._decodificar_cursor(cursor or "", artifact, hash_archivo)
            if estado["source_query"] == "id":
                encontrado = self._buscar_id(objeto, estado["selector"])
                if encontrado is None:
                    raise ErrorConsulta("NOT_FOUND", "Ya no existe el identificador del cursor")
                texto = json.dumps(
                    encontrado,
                    ensure_ascii=False,
                    indent=2,
                    allow_nan=False,
                )
            return self._paginar(
                artifact,
                query,
                "json",
                texto,
                hash_archivo,
                estado["offset"],
                estado["source_query"],
                estado["selector"],
            )
        return self._paginar(
            artifact,
            query,
            "json",
            texto,
            hash_archivo,
            0,
            "full",
            None,
        )

    def _extraer_seccion(self, texto: str, selector: str) -> str:
        """Extrae una sección Markdown."""
        patron = re.compile(rf"(?m)^(#{{1,6}})\s+{re.escape(selector)}\s*$")
        coincidencia = patron.search(texto)
        if coincidencia is None:
            raise ErrorConsulta("NOT_FOUND", "No existe la sección solicitada")
        nivel = len(coincidencia.group(1))
        siguiente = re.compile(rf"(?m)^#{{1,{nivel}}}\s+").search(
            texto,
            coincidencia.end(),
        )
        fin = siguiente.start() if siguiente else len(texto)
        return texto[coincidencia.start():fin].strip()

    def _buscar_id(self, valor: Any, selector: str) -> dict[str, Any] | None:
        """Busca un elemento por su identificador dentro de la estructura JSON."""
        if isinstance(valor, dict):
            if valor.get("id") == selector:
                return valor
            for contenido in valor.values():
                encontrado = self._buscar_id(contenido, selector)
                if encontrado is not None:
                    return encontrado
        elif isinstance(valor, list):
            for contenido in valor:
                encontrado = self._buscar_id(contenido, selector)
                if encontrado is not None:
                    return encontrado
        return None

    def _prepared_data(self, query: str) -> dict[str, Any]:
        """Resume las dimensiones, columnas y muestras de los datos preparados."""
        ruta = self._ruta_archivo("prepared_data")
        try:
            tabla = pd.read_csv(ruta, encoding="utf-8", low_memory=False)
        except Exception as exc:
            raise ErrorConsulta("SCHEMA_ERROR", "prepared_data.csv no puede cargarse") from exc
        filas = len(tabla)
        primeras = list(range(min(5, filas)))
        ultimas = [
            posicion
            for posicion in range(max(filas - 5, 0), filas)
            if posicion not in primeras
        ]
        candidatas = [
            posicion for posicion in range(filas) if posicion not in set(primeras + ultimas)
        ]
        generador = random.Random(self.configuracion.datos["security"]["experiment_seed"])
        aleatorias = generador.sample(candidatas, min(10, len(candidatas)))
        perfil = []
        for indice, nombre in enumerate(tabla.columns):
            serie = tabla.iloc[:, indice]
            perfil.append(
                {
                    "name": str(nombre),
                    "observed_type": str(serie.dtype),
                    "missing": int(serie.isna().sum()),
                    "cardinality": int(serie.nunique(dropna=True)),
                }
            )
        contenido = {
            "rows": filas,
            "columns": tabla.shape[1],
            "column_profile": perfil,
            "head_sample": _registros(tabla, primeras),
            "tail_sample": _registros(tabla, ultimas),
            "random_sample": _registros(tabla, aleatorias),
        }
        return self._base(
            "prepared_data",
            query,
            "table_summary",
            contenido,
            sha256_archivo(ruta),
        )

    def _figures(self, query: str, selector: str | None) -> dict[str, Any]:
        """Consulta la información de las figuras registradas sin enviar sus imágenes."""
        directorio = self.contexto.directorio_figuras
        ruta_statistics = self._ruta_archivo("statistics")
        try:
            estadisticas, _ = cargar_json_sin_duplicados(ruta_statistics)
        except Exception as exc:
            raise ErrorConsulta("SCHEMA_ERROR", "No puede leerse el registro de figuras") from exc
        registros = estadisticas.get("figures")
        if not isinstance(registros, list):
            raise ErrorConsulta("SCHEMA_ERROR", "statistics.figures no es una lista")
        metadatos = []
        for registro in registros:
            if not isinstance(registro, dict):
                continue
            ruta_relativa = registro.get("file")
            if not isinstance(ruta_relativa, str) or not ruta_relativa.startswith("figures/"):
                continue
            ruta = self.contexto.directorio_salida / Path(ruta_relativa)
            existe = ruta.is_file() and ruta.parent.resolve() == directorio.resolve()
            item = {
                "id": registro.get("id"),
                "file": ruta_relativa,
                "title": registro.get("title"),
                "objective": registro.get("objective"),
                "source_analysis_ids": registro.get("source_analysis_ids"),
                "exists": existe,
                "format": "png" if existe and ruta.suffix.casefold() == ".png" else None,
                "width": None,
                "height": None,
                "bytes": ruta.stat().st_size if existe else None,
                "sha256": sha256_archivo(ruta) if existe else None,
            }
            if existe:
                try:
                    item["width"], item["height"] = _metadatos_png(ruta)
                except ValueError:
                    item["format"] = "invalid"
            metadatos.append(item)
        if query == "id":
            coincidencias = [item for item in metadatos if item["id"] == selector]
            if len(coincidencias) != 1:
                raise ErrorConsulta("NOT_FOUND", "No existe la figura solicitada")
            return self._base(
                "figures",
                query,
                "figure_metadata",
                coincidencias[0],
                coincidencias[0]["sha256"],
            )
        return self._base(
            "figures",
            query,
            "figure_metadata",
            metadatos,
            None,
        )

    def _paginar(
        self,
        artifact: str,
        query: str,
        content_type: str,
        texto: str,
        hash_archivo: str,
        offset: int,
        source_query: str,
        selector: str | None,
    ) -> dict[str, Any]:
        """Devuelve el texto hasta el límite permitido y, si queda contenido, un código para leer la siguiente parte."""
        if offset < 0 or offset > len(texto):
            raise ErrorConsulta("INVALID_ARGUMENT", "El cursor contiene un desplazamiento inválido")
        fin = min(offset + self._maximo_fragmento, len(texto))
        fragmento = texto[offset:fin]
        truncado = fin < len(texto)
        siguiente = (
            self._codificar_cursor(
                artifact,
                hash_archivo,
                fin,
                source_query,
                selector,
            )
            if truncado
            else None
        )
        return self._base(
            artifact,
            query,
            content_type,
            fragmento,
            hash_archivo,
            truncado,
            siguiente,
        )

    def _codificar_cursor(
        self,
        artifact: str,
        hash_archivo: str,
        offset: int,
        source_query: str,
        selector: str | None,
    ) -> str:
        """Genera el código que indica desde dónde continuar la lectura."""
        contenido = json.dumps(
            {
                "artifact": artifact,
                "sha256": hash_archivo,
                "offset": offset,
                "source_query": source_query,
                "selector": selector,
            },
            separators=(",", ":"),
        ).encode("utf-8")
        return base64.urlsafe_b64encode(contenido).decode("ascii").rstrip("=")

    def _decodificar_cursor(
        self,
        cursor: str,
        artifact: str,
        hash_archivo: str,
    ) -> dict[str, Any]:
        """Interpreta el código de continuación y comprueba que corresponda al archivo actual."""
        try:
            relleno = "=" * (-len(cursor) % 4)
            estado = json.loads(
                base64.urlsafe_b64decode(cursor + relleno).decode("utf-8")
            )
        except Exception as exc:
            raise ErrorConsulta("INVALID_ARGUMENT", "El cursor no es válido") from exc
        if (
            not isinstance(estado, dict)
            or estado.get("artifact") != artifact
            or estado.get("sha256") != hash_archivo
            or not isinstance(estado.get("offset"), int)
            or estado.get("source_query") not in {"full", "section", "id"}
            or not (
                estado.get("selector") is None
                or isinstance(estado.get("selector"), str)
            )
        ):
            raise ErrorConsulta(
                "INVALID_ARGUMENT",
                "El cursor no corresponde al artefacto actual",
            )
        return estado
