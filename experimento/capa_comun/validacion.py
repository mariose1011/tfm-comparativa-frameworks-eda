"""Comprobación de los archivos de salida y determinación del estado final de la ejecución."""

from __future__ import annotations

import re
import struct
import unicodedata
import zlib
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd

from .configuracion import ConfiguracionExperimento
from .ejecucion import ContextoEjecucion
from .traza import validar_archivo_traza
from .utilidades import cargar_json_sin_duplicados, sha256_archivo


ENCABEZADOS_PLAN = [
    "Identificación",
    "Comprensión inicial",
    "Preguntas analíticas",
    "Plan por etapas",
    "Visualizaciones previstas",
    "Supuestos y riesgos",
    "Criterios de finalización",
]
ENCABEZADOS_INFORME = [
    "Resumen ejecutivo",
    "Dataset y alcance",
    "Inspección, calidad y preparación",
    "Estadística descriptiva",
    "Variables, agregaciones y relaciones",
    "Visualizaciones y hallazgos",
    "Problemas, riesgos y anomalías",
    "Limitaciones e incertidumbres",
    "Conclusiones",
]
ARTEFACTOS = (
    "plan.md",
    "prepared_data.csv",
    "statistics.json",
    "issues.json",
    "figures/",
    "report.md",
    "trace.jsonl",
)


def _artefacto(nombre: str, ruta: Path) -> dict[str, Any]:
    """Recoge la existencia, el tamaño y el hash de una salida."""
    existe = ruta.is_dir() if nombre.endswith("/") else ruta.is_file()
    tamano = None
    hash_archivo = None
    if existe and ruta.is_file():
        tamano = ruta.stat().st_size
        hash_archivo = sha256_archivo(ruta)
    elif existe and ruta.is_dir():
        tamano = sum(
            archivo.stat().st_size
            for archivo in ruta.rglob("*")
            if archivo.is_file()
        )
    return {
        "name": nombre,
        "exists": existe,
        "size_bytes": tamano,
        "readable": False,
        "schema_valid": False,
        "sha256": hash_archivo,
        "errors": [],
        "warnings": [],
    }


def _normalizar(texto: str) -> str:
    """Elimina diferencias de mayúsculas y tildes al comparar textos."""
    descompuesto = unicodedata.normalize("NFKD", texto)
    return "".join(
        caracter for caracter in descompuesto if not unicodedata.combining(caracter)
    ).casefold()


def _secciones_markdown(texto: str) -> tuple[list[str], dict[str, str]]:
    """Separa los encabezados principales y el contenido de cada sección."""
    coincidencias = list(re.finditer(r"(?m)^# ([^#\r\n]+?)\s*$", texto))
    encabezados = [coincidencia.group(1).strip() for coincidencia in coincidencias]
    secciones: dict[str, str] = {}
    for indice, coincidencia in enumerate(coincidencias):
        fin = coincidencias[indice + 1].start() if indice + 1 < len(coincidencias) else len(texto)
        secciones[encabezados[indice]] = texto[coincidencia.end():fin].strip()
    return encabezados, secciones


def _comprobar_texto_privado(texto: str, errores: list[str]) -> None:
    """Busca posibles claves de API, rutas absolutas y referencias a carpetas privadas."""
    if re.search(r"sk-[A-Za-z0-9_-]{10,}", texto):
        errores.append("El contenido incluye un posible secreto")
    if re.search(r"(?i)(?<![A-Za-z0-9])[A-Z]:[\\/]", texto):
        errores.append("El contenido incluye una ruta absoluta de Windows")
    normalizado = texto.replace("\\", "/").casefold()
    if "datasets/raw" in normalizado or "datasets/reference_private" in normalizado:
        errores.append("El contenido referencia una ubicación privada")


def _es_entero(valor: Any, minimo: int = 0) -> bool:
    """Comprueba que el valor sea un entero y alcance el mínimo indicado."""
    return isinstance(valor, int) and not isinstance(valor, bool) and valor >= minimo


def _campos_requeridos(
    objeto: Any,
    campos: Iterable[str],
    ubicacion: str,
    errores: list[str],
) -> bool:
    """Comprueba que el objeto incluya los campos obligatorios."""
    if not isinstance(objeto, dict):
        errores.append(f"{ubicacion} debe ser un objeto")
        return False
    faltantes = [campo for campo in campos if campo not in objeto]
    if faltantes:
        errores.append(f"Faltan campos en {ubicacion}: {', '.join(faltantes)}")
        return False
    return True


def _ids_validos(
    elementos: Any,
    patron: str,
    ubicacion: str,
    errores: list[str],
) -> set[str]:
    """Comprueba el formato de los identificadores y detecta los repetidos."""
    if not isinstance(elementos, list):
        errores.append(f"{ubicacion} debe ser una lista")
        return set()
    ids: list[str] = []
    for indice, elemento in enumerate(elementos):
        if not isinstance(elemento, dict):
            errores.append(f"{ubicacion}[{indice}] debe ser un objeto")
            continue
        identificador = elemento.get("id")
        if not isinstance(identificador, str) or re.fullmatch(patron, identificador) is None:
            errores.append(f"Identificador inválido en {ubicacion}[{indice}]")
        else:
            ids.append(identificador)
    duplicados = sorted({identificador for identificador in ids if ids.count(identificador) > 1})
    if duplicados:
        errores.append(f"Identificadores duplicados en {ubicacion}: {', '.join(duplicados)}")
    return set(ids)


def _fecha_utc_valida(valor: Any) -> bool:
    """Comprueba que el texto represente una fecha con zona horaria."""
    if not isinstance(valor, str):
        return False
    try:
        fecha = datetime.fromisoformat(valor.replace("Z", "+00:00"))
    except ValueError:
        return False
    return fecha.tzinfo is not None and fecha.utcoffset() is not None


def _metadatos_png(ruta: Path) -> tuple[int, int]:
    """Comprueba los bloques del PNG y obtiene su ancho y alto."""
    contenido = ruta.read_bytes()
    if len(contenido) < 33 or contenido[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Firma PNG inválida")
    posicion = 8
    tipos: list[bytes] = []
    datos_idat: list[bytes] = []
    ancho = 0
    alto = 0
    while posicion < len(contenido):
        if posicion + 12 > len(contenido):
            raise ValueError("Bloque PNG truncado")
        longitud = struct.unpack(">I", contenido[posicion:posicion + 4])[0]
        tipo = contenido[posicion + 4:posicion + 8]
        fin_datos = posicion + 8 + longitud
        fin_bloque = fin_datos + 4
        if fin_bloque > len(contenido):
            raise ValueError("Longitud de bloque PNG inválida")
        datos = contenido[posicion + 8:fin_datos]
        crc_esperado = struct.unpack(">I", contenido[fin_datos:fin_bloque])[0]
        crc_real = zlib.crc32(tipo + datos) & 0xFFFFFFFF
        if crc_real != crc_esperado:
            raise ValueError("CRC inválido en un bloque PNG")
        tipos.append(tipo)
        if tipo == b"IHDR":
            if len(tipos) != 1 or longitud != 13:
                raise ValueError("Bloque IHDR inválido")
            ancho, alto = struct.unpack(">II", datos[:8])
        elif tipo == b"IDAT":
            datos_idat.append(datos)
        elif tipo == b"IEND":
            if longitud != 0 or fin_bloque != len(contenido):
                raise ValueError("Cierre PNG inválido")
            break
        posicion = fin_bloque
    if not tipos or tipos[0] != b"IHDR" or tipos[-1] != b"IEND" or not datos_idat:
        raise ValueError("Faltan bloques PNG obligatorios")
    try:
        zlib.decompress(b"".join(datos_idat))
    except zlib.error as exc:
        raise ValueError("Los datos de imagen PNG no pueden descomprimirse") from exc
    if ancho < 1 or alto < 1:
        raise ValueError("Dimensiones PNG inválidas")
    return ancho, alto


class ValidadorSalidas:
    """Comprueba la estructura de los archivos de salida y las referencias entre ellos, sin evaluar la calidad del análisis."""

    def __init__(
        self,
        configuracion: ConfiguracionExperimento,
        contexto: ContextoEjecucion,
    ) -> None:
        self.configuracion = configuracion
        self.contexto = contexto

    def validar(
        self,
        validation_id: str,
        pending_correction: bool = False,
    ) -> dict[str, Any]:
        """Reúne las comprobaciones de las salidas y devuelve un resultado conjunto."""
        raiz = self.contexto.directorio_salida
        artefactos = {
            nombre: _artefacto(nombre, raiz / nombre.rstrip("/"))
            for nombre in ARTEFACTOS
        }
        datos: dict[str, Any] = {}

        self._validar_plan(artefactos["plan.md"], raiz / "plan.md", datos)
        self._validar_preparados(
            artefactos["prepared_data.csv"],
            raiz / "prepared_data.csv",
            datos,
        )
        self._validar_statistics(
            artefactos["statistics.json"],
            raiz / "statistics.json",
            datos,
        )
        self._validar_issues(
            artefactos["issues.json"],
            raiz / "issues.json",
            datos,
        )
        self._validar_figuras(artefactos["figures/"], raiz / "figures", datos)
        self._validar_informe(artefactos["report.md"], raiz / "report.md", datos)
        self._validar_traza(artefactos["trace.jsonl"], raiz / "trace.jsonl")

        cross_checks = self._comprobaciones_cruzadas(datos, artefactos)
        if pending_correction:
            cross_checks["pending_correction"] = {
                "status": "error",
                "message": "Existe una solicitud de corrección sin atender",
            }
        else:
            cross_checks["pending_correction"] = {
                "status": "valid",
                "message": "No existe una solicitud de corrección pendiente",
            }

        lista = [artefactos[nombre] for nombre in ARTEFACTOS]
        error_count = sum(len(item["errors"]) for item in lista)
        warning_count = sum(len(item["warnings"]) for item in lista)
        errores_cruzados = sum(
            1 for comprobacion in cross_checks.values() if comprobacion["status"] == "error"
        )
        avisos_cruzados = sum(
            1 for comprobacion in cross_checks.values() if comprobacion["status"] == "warning"
        )
        error_count += errores_cruzados
        warning_count += avisos_cruzados

        faltantes = [item for item in lista if not item["exists"]]
        invalidos_presentes = [
            item for item in lista if item["exists"] and not item["schema_valid"]
        ]
        if invalidos_presentes or errores_cruzados:
            estado = "invalid"
        elif faltantes:
            estado = "incomplete"
        else:
            estado = "valid"

        if estado == "valid":
            resumen = "Los siete resultados cumplen la validación estructural común"
        elif estado == "incomplete":
            resumen = "Faltan uno o más resultados obligatorios"
        else:
            resumen = "Existen resultados o relaciones que incumplen el esquema común"
        return {
            "validation_id": validation_id,
            "validation_status": estado,
            "artifacts": lista,
            "cross_checks": cross_checks,
            "pending_correction": pending_correction,
            "error_count": error_count,
            "warning_count": warning_count,
            "summary": resumen,
        }

    def _comprobar_archivo_basico(
        self,
        resultado: dict[str, Any],
        ruta: Path,
        maximo: int,
    ) -> bool:
        """Comprueba que el archivo exista, no esté vacío, pueda leerse y respete su tamaño máximo."""
        if not resultado["exists"]:
            resultado["errors"].append("El artefacto obligatorio no existe")
            return False
        if resultado["size_bytes"] == 0:
            resultado["errors"].append("El artefacto está vacío")
            return False
        if resultado["size_bytes"] > maximo:
            resultado["errors"].append("El artefacto supera el tamaño máximo")
            return False
        try:
            ruta.open("rb").close()
        except OSError:
            resultado["errors"].append("El artefacto no puede leerse")
            return False
        resultado["readable"] = True
        return True

    def _validar_plan(
        self,
        resultado: dict[str, Any],
        ruta: Path,
        datos: dict[str, Any],
    ) -> None:
        """Comprueba los apartados, las etapas y la identificación del plan."""
        maximo = self.configuracion.datos["limits"]["sizes"]["files_max_bytes"]["plan.md"]
        if not self._comprobar_archivo_basico(resultado, ruta, maximo):
            return
        try:
            texto = ruta.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            resultado["errors"].append("plan.md no utiliza UTF-8")
            return
        encabezados, secciones = _secciones_markdown(texto)
        if encabezados != ENCABEZADOS_PLAN:
            resultado["errors"].append("Los encabezados principales de plan.md no coinciden")
        for encabezado in ENCABEZADOS_PLAN:
            if not secciones.get(encabezado, "").strip():
                resultado["errors"].append(f"La sección {encabezado} está vacía")

        plan_etapas = secciones.get("Plan por etapas", "")
        coincidencias = list(re.finditer(r"(?m)^## E([1-8])(?:\s|$).*", plan_etapas))
        if [int(coincidencia.group(1)) for coincidencia in coincidencias] != list(range(1, 9)):
            resultado["errors"].append("plan.md no contiene exactamente E1 a E8 en orden")
        campos = (
            "Objetivo",
            "Comprobaciones",
            "Variables o grupos",
            "Evidencia esperada",
            "Supuestos o dependencias",
        )
        for indice, coincidencia in enumerate(coincidencias):
            fin = coincidencias[indice + 1].start() if indice + 1 < len(coincidencias) else len(plan_etapas)
            contenido = _normalizar(plan_etapas[coincidencia.end():fin])
            for campo in campos:
                if _normalizar(campo) not in contenido:
                    resultado["errors"].append(
                        f"E{coincidencia.group(1)} no incluye el campo {campo}"
                    )

        identificacion = secciones.get("Identificación", "")
        esperados = (
            self.contexto.run_id,
            self.contexto.framework_id,
            self.contexto.dataset.dataset_id,
            self.configuracion.datos["versions"]["contract"],
            self.configuracion.datos["versions"]["prompts"],
        )
        for valor in esperados:
            if str(valor) not in identificacion:
                resultado["errors"].append(
                    "La identificación del plan no coincide con la ejecución"
                )
                break
        _comprobar_texto_privado(texto, resultado["errors"])
        resultado["schema_valid"] = not resultado["errors"]
        datos["plan_text"] = texto

    def _validar_preparados(
        self,
        resultado: dict[str, Any],
        ruta: Path,
        datos: dict[str, Any],
    ) -> None:
        """Comprueba la lectura del CSV preparado y revisa sus encabezados."""
        maximo = self.configuracion.datos["limits"]["sizes"]["files_max_bytes"][
            "run_directory_total"
        ]
        if not self._comprobar_archivo_basico(resultado, ruta, maximo):
            return
        try:
            tabla = pd.read_csv(ruta, encoding="utf-8", low_memory=False)
        except Exception:
            resultado["errors"].append("prepared_data.csv no puede cargarse como CSV UTF-8")
            return
        nombres = [str(nombre) for nombre in tabla.columns]
        if not nombres or any(not nombre.strip() for nombre in nombres):
            resultado["errors"].append("prepared_data.csv no contiene encabezados válidos")
        if len(nombres) != len(set(nombres)):
            resultado["errors"].append("prepared_data.csv contiene encabezados duplicados")
        if any(nombre.startswith("Unnamed:") for nombre in nombres):
            resultado["warnings"].append("Se ha observado una posible columna de índice artificial")
        resultado["schema_valid"] = not resultado["errors"]
        datos["prepared_table"] = tabla

    def _validar_statistics(
        self,
        resultado: dict[str, Any],
        ruta: Path,
        datos: dict[str, Any],
    ) -> None:
        """Revisa la estructura, los identificadores y las referencias de statistics.json."""
        maximo = self.configuracion.datos["limits"]["sizes"]["files_max_bytes"]["statistics.json"]
        if not self._comprobar_archivo_basico(resultado, ruta, maximo):
            return
        try:
            objeto, contenido = cargar_json_sin_duplicados(ruta)
        except Exception as exc:
            resultado["errors"].append(f"statistics.json no es JSON estricto: {exc}")
            return
        _comprobar_texto_privado(contenido.decode("utf-8"), resultado["errors"])
        raiz_obligatoria = {
            "schema_version",
            "run_id",
            "dataset_id",
            "generated_at_utc",
            "profile",
            "preparation",
            "analyses",
            "figures",
            "limitations",
        }
        claves = set(objeto)
        if not raiz_obligatoria.issubset(claves):
            resultado["errors"].append("Faltan campos obligatorios en statistics.json")
        if claves - raiz_obligatoria - {"extensions"}:
            resultado["errors"].append("statistics.json contiene campos raíz no autorizados")
        if objeto.get("schema_version") != "1.0":
            resultado["errors"].append("schema_version inválida en statistics.json")
        if objeto.get("run_id") != self.contexto.run_id:
            resultado["errors"].append("run_id no coincide en statistics.json")
        if objeto.get("dataset_id") != self.contexto.dataset.dataset_id:
            resultado["errors"].append("dataset_id no coincide en statistics.json")
        if not _fecha_utc_valida(objeto.get("generated_at_utc")):
            resultado["errors"].append("generated_at_utc no es una fecha UTC válida")

        profile = objeto.get("profile")
        campos_profile = {
            "original_rows",
            "original_columns",
            "prepared_rows",
            "prepared_columns",
            "unit_of_analysis",
            "columns",
        }
        if _campos_requeridos(profile, campos_profile, "profile", resultado["errors"]):
            if not _es_entero(profile["original_rows"]):
                resultado["errors"].append("profile.original_rows debe ser entero no negativo")
            if not _es_entero(profile["original_columns"], 1):
                resultado["errors"].append("profile.original_columns debe ser entero positivo")
            if not _es_entero(profile["prepared_rows"]):
                resultado["errors"].append("profile.prepared_rows debe ser entero no negativo")
            if not _es_entero(profile["prepared_columns"], 1):
                resultado["errors"].append("profile.prepared_columns debe ser entero positivo")
            if not isinstance(profile["unit_of_analysis"], str) or not profile["unit_of_analysis"].strip():
                resultado["errors"].append("profile.unit_of_analysis debe ser una cadena no vacía")
            columnas = profile["columns"]
            requeridos_columna = {
                "name",
                "origin",
                "source_name",
                "original_type",
                "prepared_type",
                "missing_original",
                "missing_prepared",
                "unique_prepared",
            }
            if not isinstance(columnas, list) or not columnas:
                resultado["errors"].append("profile.columns debe ser una lista no vacía")
            else:
                nombres = []
                for indice, columna in enumerate(columnas):
                    if not _campos_requeridos(
                        columna,
                        requeridos_columna,
                        f"profile.columns[{indice}]",
                        resultado["errors"],
                    ):
                        continue
                    nombres.append(columna["name"])
                    if columna["origin"] not in {"source", "derived"}:
                        resultado["errors"].append("origin inválido en profile.columns")
                    if not _es_entero(columna["missing_prepared"]):
                        resultado["errors"].append("missing_prepared debe ser entero no negativo")
                if len(nombres) != len(set(nombres)):
                    resultado["errors"].append("profile.columns contiene nombres duplicados")

        preparation = objeto.get("preparation")
        if _campos_requeridos(
            preparation,
            {"summary", "changes"},
            "preparation",
            resultado["errors"],
        ):
            if not isinstance(preparation["summary"], str) or not preparation["summary"].strip():
                resultado["errors"].append("preparation.summary debe ser una cadena no vacía")
            cambios = preparation["changes"]
            ids_cambios = _ids_validos(cambios, r"TR-\d{3}", "preparation.changes", resultado["errors"])
            requeridos_cambio = {
                "id",
                "action",
                "description",
                "justification",
                "affected_columns",
                "rows_affected",
                "before",
                "after",
            }
            if isinstance(cambios, list):
                for indice, cambio in enumerate(cambios):
                    _campos_requeridos(
                        cambio,
                        requeridos_cambio,
                        f"preparation.changes[{indice}]",
                        resultado["errors"],
                    )
            if not ids_cambios:
                resultado["warnings"].append("No se ha registrado ninguna decisión de preparación")

        analyses = objeto.get("analyses")
        ids_stats = _ids_validos(analyses, r"STAT-\d{3}", "analyses", resultado["errors"])
        requeridos_analysis = {
            "id",
            "stage",
            "analysis_type",
            "title",
            "variables",
            "population",
            "method",
            "result",
            "interpretation",
        }
        if isinstance(analyses, list):
            if not analyses:
                resultado["errors"].append("analyses no puede estar vacío")
            for indice, analysis in enumerate(analyses):
                if _campos_requeridos(
                    analysis,
                    requeridos_analysis,
                    f"analyses[{indice}]",
                    resultado["errors"],
                ) and analysis["stage"] not in {f"E{numero}" for numero in range(1, 8)}:
                    resultado["errors"].append(f"stage inválida en analyses[{indice}]")

        figuras = objeto.get("figures")
        ids_figuras = _ids_validos(figuras, r"FIG-\d{3}", "figures", resultado["errors"])
        requeridos_figura = {
            "id",
            "file",
            "title",
            "objective",
            "variables",
            "source_analysis_ids",
        }
        if isinstance(figuras, list):
            if not figuras:
                resultado["errors"].append("statistics.figures no puede estar vacío")
            for indice, figura in enumerate(figuras):
                if not _campos_requeridos(
                    figura,
                    requeridos_figura,
                    f"figures[{indice}]",
                    resultado["errors"],
                ):
                    continue
                referencias = figura["source_analysis_ids"]
                if not isinstance(referencias, list) or any(
                    referencia not in ids_stats for referencia in referencias
                ):
                    resultado["errors"].append(
                        f"source_analysis_ids no se resuelve en figures[{indice}]"
                    )
        limitaciones = objeto.get("limitations")
        if not isinstance(limitaciones, list) or any(
            not isinstance(valor, str) for valor in limitaciones
        ):
            resultado["errors"].append("limitations debe ser una lista de cadenas")

        resultado["schema_valid"] = not resultado["errors"]
        datos["statistics"] = objeto
        datos["stat_ids"] = ids_stats
        datos["figure_ids"] = ids_figuras

    def _validar_issues(
        self,
        resultado: dict[str, Any],
        ruta: Path,
        datos: dict[str, Any],
    ) -> None:
        """Revisa las comprobaciones de calidad y los problemas registrados en issues.json."""
        maximo = self.configuracion.datos["limits"]["sizes"]["files_max_bytes"]["issues.json"]
        if not self._comprobar_archivo_basico(resultado, ruta, maximo):
            return
        try:
            objeto, contenido = cargar_json_sin_duplicados(ruta)
        except Exception as exc:
            resultado["errors"].append(f"issues.json no es JSON estricto: {exc}")
            return
        _comprobar_texto_privado(contenido.decode("utf-8"), resultado["errors"])
        if set(objeto) != {
            "schema_version",
            "run_id",
            "dataset_id",
            "checks_performed",
            "issues",
        }:
            resultado["errors"].append("Los campos raíz de issues.json no coinciden")
        if objeto.get("schema_version") != "1.0":
            resultado["errors"].append("schema_version inválida en issues.json")
        if objeto.get("run_id") != self.contexto.run_id:
            resultado["errors"].append("run_id no coincide en issues.json")
        if objeto.get("dataset_id") != self.contexto.dataset.dataset_id:
            resultado["errors"].append("dataset_id no coincide en issues.json")

        checks = objeto.get("checks_performed")
        ids_checks = _ids_validos(checks, r"CHK-\d{3}", "checks_performed", resultado["errors"])
        campos_check = {"id", "category", "description", "outcome", "evidence_ids"}
        if isinstance(checks, list):
            if not checks:
                resultado["errors"].append("checks_performed no puede estar vacío")
            for indice, check in enumerate(checks):
                _campos_requeridos(
                    check,
                    campos_check,
                    f"checks_performed[{indice}]",
                    resultado["errors"],
                )

        issues = objeto.get("issues")
        ids_issues = _ids_validos(issues, r"ISSUE-\d{3}", "issues", resultado["errors"])
        campos_issue = {
            "id",
            "category",
            "status",
            "severity",
            "title",
            "description",
            "evidence",
            "affected_columns",
            "affected_row_count",
            "sample_row_ids",
            "decision",
            "action",
            "potential_effect",
            "uncertainty",
            "evidence_ids",
        }
        categorias = {
            "missing",
            "duplicate",
            "type",
            "category",
            "range",
            "identity",
            "temporal",
            "outlier",
            "other",
        }
        estados = {"detected", "suspected", "resolved", "retained", "unresolved"}
        severidades = {"info", "low", "medium", "high"}
        if isinstance(issues, list):
            for indice, issue in enumerate(issues):
                if not _campos_requeridos(
                    issue,
                    campos_issue,
                    f"issues[{indice}]",
                    resultado["errors"],
                ):
                    continue
                if issue["category"] not in categorias:
                    resultado["errors"].append(f"category inválida en issues[{indice}]")
                if issue["status"] not in estados:
                    resultado["errors"].append(f"status inválido en issues[{indice}]")
                if issue["severity"] not in severidades:
                    resultado["errors"].append(f"severity inválida en issues[{indice}]")

        resultado["schema_valid"] = not resultado["errors"]
        datos["issues"] = objeto
        datos["check_ids"] = ids_checks
        datos["issue_ids"] = ids_issues

    def _validar_figuras(
        self,
        resultado: dict[str, Any],
        ruta: Path,
        datos: dict[str, Any],
    ) -> None:
        """Comprueba los nombres, tamaños, cantidad y estructura de las imágenes PNG."""
        if not resultado["exists"]:
            resultado["errors"].append("El directorio figures no existe")
            return
        resultado["readable"] = True
        archivos = sorted(
            archivo for archivo in ruta.iterdir() if archivo.is_file()
        )
        png = [archivo for archivo in archivos if archivo.suffix.casefold() == ".png"]
        maximo_cantidad = self.configuracion.datos["limits"]["sizes"]["figures_max_count"]
        maximo_archivo = self.configuracion.datos["limits"]["sizes"]["files_max_bytes"][
            "single_figure_png"
        ]
        maximo_total = self.configuracion.datos["limits"]["sizes"]["files_max_bytes"][
            "figures_total"
        ]
        if not png:
            resultado["errors"].append("figures no contiene ninguna imagen PNG")
        if len(png) > maximo_cantidad:
            resultado["errors"].append("figures supera el número máximo de imágenes")
        if resultado["size_bytes"] is not None and resultado["size_bytes"] > maximo_total:
            resultado["errors"].append("figures supera el tamaño total máximo")
        if len(archivos) != len(png):
            resultado["errors"].append("figures contiene archivos que no son PNG")

        metadatos = []
        for archivo in png:
            if re.fullmatch(r"fig_\d{3}_[a-zA-Z0-9_-]+\.png", archivo.name) is None:
                resultado["errors"].append(f"Nombre de figura inválido: {archivo.name}")
            if archivo.stat().st_size > maximo_archivo:
                resultado["errors"].append(f"La figura supera el tamaño máximo: {archivo.name}")
            try:
                ancho, alto = _metadatos_png(archivo)
            except (OSError, ValueError) as exc:
                resultado["errors"].append(f"PNG inválido {archivo.name}: {exc}")
                continue
            metadatos.append(
                {
                    "file": f"figures/{archivo.name}",
                    "format": "png",
                    "width": ancho,
                    "height": alto,
                    "bytes": archivo.stat().st_size,
                    "sha256": sha256_archivo(archivo),
                }
            )
        resultado["schema_valid"] = not resultado["errors"]
        datos["figure_files"] = metadatos

    def _validar_informe(
        self,
        resultado: dict[str, Any],
        ruta: Path,
        datos: dict[str, Any],
    ) -> None:
        """Comprueba los apartados obligatorios y recoge las referencias del informe."""
        maximo = self.configuracion.datos["limits"]["sizes"]["files_max_bytes"]["report.md"]
        if not self._comprobar_archivo_basico(resultado, ruta, maximo):
            return
        try:
            texto = ruta.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            resultado["errors"].append("report.md no utiliza UTF-8")
            return
        encabezados, secciones = _secciones_markdown(texto)
        if encabezados != ENCABEZADOS_INFORME:
            resultado["errors"].append("Los encabezados principales de report.md no coinciden")
        for encabezado in ENCABEZADOS_INFORME:
            if not secciones.get(encabezado, "").strip():
                resultado["errors"].append(f"La sección {encabezado} está vacía")
        _comprobar_texto_privado(texto, resultado["errors"])
        referencias = {
            "STAT": set(re.findall(r"\[(STAT-\d{3})\]", texto)),
            "ISSUE": set(re.findall(r"\[(ISSUE-\d{3})\]", texto)),
            "FIG": set(re.findall(r"\[(FIG-\d{3})\]", texto)),
        }
        if not referencias["STAT"]:
            resultado["errors"].append("report.md no contiene referencias STAT")
        if not referencias["FIG"]:
            resultado["errors"].append("report.md no contiene referencias FIG")
        resultado["schema_valid"] = not resultado["errors"]
        datos["report_text"] = texto
        datos["report_references"] = referencias

    def _validar_traza(self, resultado: dict[str, Any], ruta: Path) -> None:
        """Comprueba la integridad de trace.jsonl y recoge sus errores o advertencias."""
        maximo = self.configuracion.datos["limits"]["sizes"]["files_max_bytes"]["trace.jsonl"]
        if not self._comprobar_archivo_basico(resultado, ruta, maximo):
            return
        try:
            integridad = validar_archivo_traza(ruta)
        except Exception:
            resultado["errors"].append("trace.jsonl no puede validarse")
            return
        if integridad.estado == "invalid":
            resultado["errors"].extend(integridad.comprobaciones_fallidas)
        elif integridad.estado == "incomplete":
            resultado["warnings"].append(
                "La traza es un prefijo recuperable pendiente del cierre de la ejecución"
            )
        resultado["schema_valid"] = integridad.estado != "invalid"

    def _comprobaciones_cruzadas(
        self,
        datos: Mapping[str, Any],
        artefactos: Mapping[str, dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        """Comprueba la coincidencia de dimensiones, referencias y figuras entre archivos."""
        resultado: dict[str, dict[str, Any]] = {}
        tabla = datos.get("prepared_table")
        estadisticas = datos.get("statistics")
        if isinstance(tabla, pd.DataFrame) and isinstance(estadisticas, dict):
            profile = estadisticas.get("profile", {})
            dimensiones_ok = (
                profile.get("prepared_rows") == tabla.shape[0]
                and profile.get("prepared_columns") == tabla.shape[1]
                and profile.get("original_rows") == self.contexto.dataset.filas_esperadas
                and profile.get("original_columns") == self.contexto.dataset.columnas_esperadas
            )
            columnas_perfil = profile.get("columns", [])
            nombres_perfil = [
                columna.get("name") for columna in columnas_perfil if isinstance(columna, dict)
            ]
            dimensiones_ok = dimensiones_ok and nombres_perfil == [
                str(nombre) for nombre in tabla.columns
            ]
            resultado["dimensions"] = {
                "status": "valid" if dimensiones_ok else "error",
                "message": (
                    "Las dimensiones y columnas coinciden"
                    if dimensiones_ok
                    else "Las dimensiones o columnas no coinciden entre archivos"
                ),
            }
        else:
            resultado["dimensions"] = {
                "status": "warning",
                "message": "No puede comprobarse la coincidencia de dimensiones",
            }

        stat_ids = set(datos.get("stat_ids", set()))
        issue_ids = set(datos.get("issue_ids", set()))
        figure_ids = set(datos.get("figure_ids", set()))
        issues = datos.get("issues")
        referencias_invalidas: list[str] = []
        if isinstance(issues, dict):
            for grupo in (issues.get("checks_performed", []), issues.get("issues", [])):
                if isinstance(grupo, list):
                    for elemento in grupo:
                        if isinstance(elemento, dict):
                            for referencia in elemento.get("evidence_ids", []):
                                if referencia not in stat_ids:
                                    referencias_invalidas.append(str(referencia))
        report_refs = datos.get("report_references", {})
        if isinstance(report_refs, dict):
            for referencia in report_refs.get("STAT", set()):
                if referencia not in stat_ids:
                    referencias_invalidas.append(referencia)
            for referencia in report_refs.get("ISSUE", set()):
                if referencia not in issue_ids:
                    referencias_invalidas.append(referencia)
            for referencia in report_refs.get("FIG", set()):
                if referencia not in figure_ids:
                    referencias_invalidas.append(referencia)
        resultado["references"] = {
            "status": "error" if referencias_invalidas else "valid",
            "message": (
                f"Referencias sin resolver: {', '.join(sorted(set(referencias_invalidas)))}"
                if referencias_invalidas
                else "Las referencias internas comprobadas se resuelven"
            ),
        }

        registros_figuras = []
        if isinstance(estadisticas, dict) and isinstance(estadisticas.get("figures"), list):
            registros_figuras = estadisticas["figures"]
        archivos_registrados = {
            figura.get("file") for figura in registros_figuras if isinstance(figura, dict)
        }
        archivos_reales = {
            figura["file"] for figura in datos.get("figure_files", [])
        }
        figuras_ok = bool(archivos_reales) and archivos_registrados == archivos_reales
        texto_informe = datos.get("report_text", "")
        if isinstance(texto_informe, str):
            figuras_ok = figuras_ok and all(
                archivo in texto_informe for archivo in archivos_reales
            )
        resultado["figures"] = {
            "status": "valid" if figuras_ok else "error",
            "message": (
                "Las figuras existen, están registradas y aparecen en el informe"
                if figuras_ok
                else "Las figuras reales, registradas y citadas no coinciden"
            ),
        }

        hash_actual = sha256_archivo(self.contexto.dataset.ruta_entrada)
        entrada_ok = hash_actual == self.contexto.dataset.sha256
        resultado["input_preserved"] = {
            "status": "valid" if entrada_ok else "error",
            "message": (
                "El archivo de entrada conserva su hash"
                if entrada_ok
                else "El archivo de entrada ha cambiado"
            ),
        }

        permitidos = {nombre.rstrip("/") for nombre in ARTEFACTOS}
        permitidos.add(self.configuracion.datos["output_contract"]["temporary_directory_name"])
        presentes = {ruta.name for ruta in self.contexto.directorio_salida.iterdir()}
        inesperados = sorted(presentes - permitidos)
        resultado["write_scope"] = {
            "status": "error" if inesperados else "valid",
            "message": (
                f"Entradas no autorizadas en el directorio: {', '.join(inesperados)}"
                if inesperados
                else "No se observan entradas fuera de la estructura autorizada"
            ),
        }
        return resultado


def determinar_estado_terminal(
    validacion: Mapping[str, Any],
    dataset_cargado: bool,
    *,
    limites_alcanzados: Iterable[str],
    flujo_roles_completo: bool,
    decision_revision: str | None,
    correccion_resuelta: bool = True,
) -> tuple[str, str]:
    """Asigna completed, partial o failed según las salidas y el desarrollo del flujo."""

    artefactos = {
        artefacto.get("name"): artefacto
        for artefacto in validacion.get("artifacts", [])
        if isinstance(artefacto, dict)
    }
    if not dataset_cargado:
        return "failed", "DATASET_NOT_LOADED"
    informe = artefactos.get("report.md", {})
    if not informe.get("schema_valid"):
        return "failed", "REPORT_MISSING_OR_INVALID"
    analiticos = [
        artefactos.get("statistics.json", {}),
        artefactos.get("issues.json", {}),
        artefactos.get("figures/", {}),
    ]
    if not any(artefacto.get("schema_valid") for artefacto in analiticos):
        return "failed", "NO_ANALYTICAL_OUTPUT"
    if tuple(limites_alcanzados):
        return "partial", "LIMIT_REACHED_WITH_EVALUABLE_OUTPUT"
    if not flujo_roles_completo:
        return "partial", "ROLE_FLOW_INCOMPLETE_WITH_EVALUABLE_OUTPUT"
    if decision_revision is None:
        return "partial", "REVIEW_DECISION_MISSING"
    if decision_revision == "cannot_review":
        return "partial", "REVIEW_CANNOT_REVIEW"
    if not correccion_resuelta:
        return "partial", "CORRECTION_UNRESOLVED"
    if (
        validacion.get("validation_status") == "valid"
        and not validacion.get("pending_correction")
    ):
        return "completed", "ALL_OUTPUTS_VALID"
    return "partial", "MINIMUM_EVALUABLE_OUTPUT_AVAILABLE"
