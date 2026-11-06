"""Utilidades deterministas de rutas, JSON y hashes."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .errores import ConfiguracionError, RutaNoAutorizadaError


def descongelar(valor: Any) -> Any:
    """Convierte estructuras inmutables en valores JSON serializables."""

    if isinstance(valor, Mapping):
        return {
            str(clave): descongelar(contenido)
            for clave, contenido in valor.items()
        }
    if isinstance(valor, (list, tuple)):
        return [descongelar(contenido) for contenido in valor]
    return valor


def json_canonico(valor: Any) -> str:
    """Serializa datos de forma estable para estimaciones y hashes."""

    return json.dumps(
        descongelar(valor),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def sha256_json(valor: Any) -> str:
    """Calcula el SHA-256 de una estructura JSON canónica."""

    return hashlib.sha256(json_canonico(valor).encode("utf-8")).hexdigest().upper()


def utc_actual() -> str:
    """Devuelve el instante UTC con el formato empleado por la traza."""

    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00",
        "Z",
    )


def cargar_json_sin_duplicados(ruta: Path) -> tuple[dict[str, Any], bytes]:
    """Carga JSON UTF-8 y rechaza claves duplicadas en cualquier objeto."""

    try:
        contenido = ruta.read_bytes()
    except OSError as exc:
        raise ConfiguracionError(f"No puede leerse el archivo JSON: {ruta.name}") from exc

    try:
        texto = contenido.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ConfiguracionError(f"El archivo JSON no utiliza UTF-8: {ruta.name}") from exc

    def construir_objeto(pares: list[tuple[str, Any]]) -> dict[str, Any]:
        resultado: dict[str, Any] = {}
        for clave, valor in pares:
            if clave in resultado:
                raise ConfiguracionError(f"Clave JSON duplicada: {clave}")
            resultado[clave] = valor
        return resultado

    def rechazar_constante(constante: str) -> None:
        raise ConfiguracionError(f"Constante JSON no permitida: {constante}")

    try:
        datos = json.loads(
            texto,
            object_pairs_hook=construir_objeto,
            parse_constant=rechazar_constante,
        )
    except json.JSONDecodeError as exc:
        raise ConfiguracionError(
            f"JSON inválido en {ruta.name}, línea {exc.lineno}, columna {exc.colno}"
        ) from exc

    if not isinstance(datos, dict):
        raise ConfiguracionError(f"La raíz de {ruta.name} debe ser un objeto JSON")

    return datos, contenido


def sha256_bytes(contenido: bytes) -> str:
    """Devuelve el SHA-256 en mayúsculas para facilitar la comparación."""

    return hashlib.sha256(contenido).hexdigest().upper()


def sha256_archivo(ruta: Path, bloque: int = 1024 * 1024) -> str:
    """Calcula SHA-256 por bloques sin cargar el archivo completo en memoria."""

    digest = hashlib.sha256()
    try:
        with ruta.open("rb") as archivo:
            while fragmento := archivo.read(bloque):
                digest.update(fragmento)
    except OSError as exc:
        raise ConfiguracionError(f"No puede leerse el archivo para calcular su hash: {ruta.name}") from exc
    return digest.hexdigest().upper()


def resolver_ruta_relativa(raiz: Path, valor: str) -> Path:
    """Resuelve una ruta relativa y confirma que permanece dentro de la raíz."""

    if not isinstance(valor, str) or not valor.strip():
        raise RutaNoAutorizadaError("La ruta relativa no puede estar vacía")

    ruta_declarada = Path(valor)
    if ruta_declarada.is_absolute() or ruta_declarada.drive:
        raise RutaNoAutorizadaError(f"No se permiten rutas absolutas: {valor}")

    raiz_resuelta = raiz.resolve()
    candidata = (raiz_resuelta / ruta_declarada).resolve()
    try:
        candidata.relative_to(raiz_resuelta)
    except ValueError as exc:
        raise RutaNoAutorizadaError(f"La ruta sale de la raíz autorizada: {valor}") from exc
    return candidata


def validar_identificador(valor: str, nombre: str) -> str:
    """Acepta identificadores seguros para trazas y nombres de carpeta."""

    if not isinstance(valor, str) or not valor:
        raise ConfiguracionError(f"{nombre} debe ser una cadena no vacía")
    permitidos = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-")
    if len(valor) > 160 or valor[0] in ".-" or any(caracter not in permitidos for caracter in valor):
        raise ConfiguracionError(f"{nombre} contiene caracteres no autorizados: {valor}")
    return valor
