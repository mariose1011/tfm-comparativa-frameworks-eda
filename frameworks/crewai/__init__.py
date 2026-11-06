"""Configuración local del entorno de CrewAI para el TFM."""

from __future__ import annotations

import os
from pathlib import Path


CARPETA_CREWAI = Path(__file__).resolve().parent
CARPETA_STORAGE = CARPETA_CREWAI / ".storage"
CARPETA_LOCAL_APPDATA = CARPETA_CREWAI / ".local_appdata"

CARPETA_STORAGE.mkdir(exist_ok=True)
CARPETA_LOCAL_APPDATA.mkdir(exist_ok=True)

os.environ["CREWAI_STORAGE_DIR"] = str(CARPETA_STORAGE)
os.environ["LOCALAPPDATA"] = str(CARPETA_LOCAL_APPDATA)
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TRACING_ENABLED"] = "false"

