"""Errores explícitos producidos por la capa común."""


class CapaComunError(Exception):
    """Error controlado de la capa común."""


class ConfiguracionError(CapaComunError):
    """La configuración falta, es inválida o contradice el contrato."""


class RutaNoAutorizadaError(CapaComunError):
    """Una ruta sale del espacio autorizado o no cumple la política común."""


class ManifiestoError(CapaComunError):
    """El manifiesto de datasets no cumple la estructura esperada."""


class HashNoCoincideError(CapaComunError):
    """El contenido real de un archivo no coincide con su hash registrado."""


class EjecucionError(CapaComunError):
    """No puede prepararse una ejecución válida y aislada."""
