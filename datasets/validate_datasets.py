"""Valida integridad, estructura y referencias de los datasets congelados."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


DATASETS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = DATASETS_DIR.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def resolve_json_path(document: dict, dotted_path: str):
    value = document
    for part in dotted_path.split("."):
        value = value[part]
    return value


def main() -> None:
    manifest = json.loads((DATASETS_DIR / "manifest.json").read_text(encoding="utf-8"))

    checked_files = 0
    for dataset in manifest["datasets"]:
        for item in dataset["files"]:
            path = PROJECT_DIR / item["path"]
            assert path.is_file(), f"No existe: {path}"
            assert path.stat().st_size == item["bytes"], f"Tamaño incorrecto: {path}"
            assert sha256(path) == item["sha256"], f"Hash incorrecto: {path}"
            checked_files += 1

    d0_path = DATASETS_DIR / "experiment_inputs" / "D0_piloto" / "pedidos_piloto.csv"
    d0 = pd.read_csv(d0_path)
    assert d0.shape == (246, 13)
    assert int(d0.isna().sum().sum()) == 24
    assert int(d0.duplicated().sum()) == 6
    assert int(d0["order_id"].nunique()) == 240
    assert int((~d0["discount_rate"].between(0, 1)).sum()) == 2
    assert int((d0["delivery_days"] < 0).sum()) == 2

    d0_private_dir = DATASETS_DIR / "reference_private" / "D0_piloto"
    d0_values = json.loads(
        (d0_private_dir / "reference_values.json").read_text(encoding="utf-8")
    )
    d0_spec = json.loads(
        (d0_private_dir / "evaluation_spec.json").read_text(encoding="utf-8")
    )

    assert d0_values["generated_from"]["sha256"] == sha256(d0_path)
    assert d0_spec["input_sha256"] == sha256(d0_path)
    assert d0_spec["pilot_only"] is True
    assert len(d0_spec["automatic_checks"]) == 32
    assert len(d0_spec["known_risks"]) == 10
    assert len(d0_spec["information_units"]) == 11
    assert len(d0_spec["visual_objectives"]) == 4

    for check in d0_spec["automatic_checks"]:
        resolve_json_path(d0_values, check["reference_path"])

    d1_path = DATASETS_DIR / "experiment_inputs" / "D1_bike_sharing" / "hour.csv"
    d1 = pd.read_csv(d1_path)
    assert d1.shape == (17379, 17)
    assert int(d1.isna().sum().sum()) == 0
    assert int(d1.duplicated().sum()) == 0

    d2_path = DATASETS_DIR / "experiment_inputs" / "D2_online_retail" / "Online Retail.xlsx"
    d2 = pd.read_excel(d2_path)
    assert d2.shape == (541909, 8)
    assert pd.Timestamp(d2["InvoiceDate"].min()) == pd.Timestamp("2010-12-01 08:26:00")
    assert pd.Timestamp(d2["InvoiceDate"].max()) == pd.Timestamp("2011-12-09 12:50:00")

    d1_private_dir = DATASETS_DIR / "reference_private" / "D1_bike_sharing"
    d1_values = json.loads(
        (d1_private_dir / "reference_values.json").read_text(encoding="utf-8")
    )
    d1_spec = json.loads(
        (d1_private_dir / "evaluation_spec.json").read_text(encoding="utf-8")
    )

    assert d1_values["generated_from"]["sha256"] == sha256(d1_path)
    assert d1_spec["input_sha256"] == sha256(d1_path)
    assert len(d1_spec["automatic_checks"]) == 26
    assert len(d1_spec["known_risks"]) == 7
    assert len(d1_spec["information_units"]) == 12
    assert len(d1_spec["visual_objectives"]) == 5

    for check in d1_spec["automatic_checks"]:
        resolve_json_path(d1_values, check["reference_path"])

    d2_private_dir = DATASETS_DIR / "reference_private" / "D2_online_retail"
    d2_values = json.loads(
        (d2_private_dir / "reference_values.json").read_text(encoding="utf-8")
    )
    d2_spec = json.loads(
        (d2_private_dir / "evaluation_spec.json").read_text(encoding="utf-8")
    )

    assert d2_values["generated_from"]["sha256"] == sha256(d2_path)
    assert d2_spec["input_sha256"] == sha256(d2_path)
    assert len(d2_spec["automatic_checks"]) == 32
    assert len(d2_spec["known_risks"]) == 10
    assert len(d2_spec["information_units"]) == 12
    assert len(d2_spec["visual_objectives"]) == 5

    for check in d2_spec["automatic_checks"]:
        resolve_json_path(d2_values, check["reference_path"])

    print(
        "VALIDATION_OK",
        json.dumps(
            {
                "manifest_files": checked_files,
                "d0_shape": list(d0.shape),
                "d1_shape": list(d1.shape),
                "d2_shape": list(d2.shape),
                "d0": {
                    "automatic_checks": len(d0_spec["automatic_checks"]),
                    "known_risks": len(d0_spec["known_risks"]),
                    "information_units": len(d0_spec["information_units"]),
                    "visual_objectives": len(d0_spec["visual_objectives"]),
                },
                "d1": {
                    "automatic_checks": len(d1_spec["automatic_checks"]),
                    "known_risks": len(d1_spec["known_risks"]),
                    "information_units": len(d1_spec["information_units"]),
                    "visual_objectives": len(d1_spec["visual_objectives"]),
                },
                "d2": {
                    "automatic_checks": len(d2_spec["automatic_checks"]),
                    "known_risks": len(d2_spec["known_risks"]),
                    "information_units": len(d2_spec["information_units"]),
                    "visual_objectives": len(d2_spec["visual_objectives"]),
                },
            },
            ensure_ascii=False,
        ),
    )


if __name__ == "__main__":
    main()
