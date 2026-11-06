"""Regenera los valores de referencia privados de D1 Bike Sharing.

Este script no debe estar disponible dentro del entorno de los agentes.
Lee exclusivamente la copia congelada usada como entrada experimental y
escribe un JSON auditable con comprobaciones descriptivas y de calidad.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
DATASETS_DIR = HERE.parents[1]
INPUT_PATH = DATASETS_DIR / "experiment_inputs" / "D1_bike_sharing" / "hour.csv"
OUTPUT_PATH = HERE / "reference_values.json"


def as_number(value):
    """Convierte escalares de pandas/numpy a tipos JSON estandar."""
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def series_dict(series: pd.Series, digits: int | None = None) -> dict[str, int | float]:
    result: dict[str, int | float] = {}
    for key, value in series.items():
        number = as_number(value)
        if isinstance(number, float) and digits is not None:
            number = round(number, digits)
        result[str(key)] = number
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main() -> None:
    df = pd.read_csv(INPUT_PATH)
    dates = pd.to_datetime(df["dteday"], format="%Y-%m-%d", errors="raise")
    timestamps = dates + pd.to_timedelta(df["hr"], unit="h")

    expected_timestamps = pd.date_range(
        dates.min(), dates.max() + pd.Timedelta(hours=23), freq="h"
    )
    missing_timestamps = expected_timestamps.difference(pd.DatetimeIndex(timestamps))

    cnt = df["cnt"]
    total_users = int(cnt.sum())
    registered_total = int(df["registered"].sum())
    casual_total = int(df["casual"].sum())

    year_summary = df.groupby("yr").agg(
        rows=("cnt", "size"),
        total_cnt=("cnt", "sum"),
        mean_cnt=("cnt", "mean"),
        median_cnt=("cnt", "median"),
        casual_total=("casual", "sum"),
        registered_total=("registered", "sum"),
    )

    def grouped_summary(column: str) -> dict[str, dict[str, int | float]]:
        grouped = df.groupby(column)["cnt"].agg(["count", "sum", "mean", "median"])
        output: dict[str, dict[str, int | float]] = {}
        for key, row in grouped.iterrows():
            output[str(key)] = {
                "count": int(row["count"]),
                "sum": int(row["sum"]),
                "mean": round(float(row["mean"]), 6),
                "median": round(float(row["median"]), 6),
            }
        return output

    reference = {
        "generated_from": {
            "path": "datasets/experiment_inputs/D1_bike_sharing/hour.csv",
            "sha256": sha256(INPUT_PATH),
        },
        "structure": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": list(df.columns),
            "unique_dates": int(dates.nunique()),
            "date_min": dates.min().date().isoformat(),
            "date_max": dates.max().date().isoformat(),
            "timestamp_min": timestamps.min().isoformat(),
            "timestamp_max": timestamps.max().isoformat(),
            "expected_hourly_slots": int(len(expected_timestamps)),
            "observed_hourly_slots": int(timestamps.nunique()),
            "missing_hourly_slots": int(len(missing_timestamps)),
            "missing_hourly_slots_by_year": series_dict(
                pd.Series(missing_timestamps.year).value_counts().sort_index()
            ),
        },
        "quality": {
            "missing_cells_total": int(df.isna().sum().sum()),
            "missing_by_column": series_dict(df.isna().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "duplicate_instant": int(df["instant"].duplicated().sum()),
            "instant_min": int(df["instant"].min()),
            "instant_max": int(df["instant"].max()),
            "instant_is_complete_sequence": bool(
                df["instant"].tolist() == list(range(1, len(df) + 1))
            ),
            "cnt_identity_errors": int(
                (df["cnt"] != df["casual"] + df["registered"]).sum()
            ),
            "out_of_range_counts": {
                "season": int((~df["season"].between(1, 4)).sum()),
                "yr": int((~df["yr"].between(0, 1)).sum()),
                "mnth": int((~df["mnth"].between(1, 12)).sum()),
                "hr": int((~df["hr"].between(0, 23)).sum()),
                "holiday": int((~df["holiday"].between(0, 1)).sum()),
                "weekday": int((~df["weekday"].between(0, 6)).sum()),
                "workingday": int((~df["workingday"].between(0, 1)).sum()),
                "weathersit": int((~df["weathersit"].between(1, 4)).sum()),
                "temp_normalized": int((~df["temp"].between(0, 1)).sum()),
                "atemp_normalized": int((~df["atemp"].between(0, 1)).sum()),
                "hum_normalized": int((~df["hum"].between(0, 1)).sum()),
                "windspeed_normalized": int((~df["windspeed"].between(0, 1)).sum()),
                "negative_user_counts": int(
                    (df[["casual", "registered", "cnt"]] < 0).any(axis=1).sum()
                ),
            },
            "unique_values": series_dict(df.nunique(dropna=False)),
        },
        "overall": {
            "cnt_sum": total_users,
            "cnt_mean": round(float(cnt.mean()), 6),
            "cnt_median": round(float(cnt.median()), 6),
            "cnt_std_sample": round(float(cnt.std(ddof=1)), 6),
            "cnt_min": int(cnt.min()),
            "cnt_q1": round(float(cnt.quantile(0.25)), 6),
            "cnt_q3": round(float(cnt.quantile(0.75)), 6),
            "cnt_max": int(cnt.max()),
            "casual_sum": casual_total,
            "registered_sum": registered_total,
            "casual_share": round(casual_total / total_users, 9),
            "registered_share": round(registered_total / total_users, 9),
        },
        "normalized_ranges": {
            "temp": {"min": float(df["temp"].min()), "max": float(df["temp"].max())},
            "atemp": {"min": float(df["atemp"].min()), "max": float(df["atemp"].max())},
            "hum": {"min": float(df["hum"].min()), "max": float(df["hum"].max())},
            "windspeed": {
                "min": float(df["windspeed"].min()),
                "max": float(df["windspeed"].max()),
            },
        },
        "by_year": {
            str(key): {
                name: round(float(value), 6) if name in {"mean_cnt", "median_cnt"} else int(value)
                for name, value in row.items()
            }
            for key, row in year_summary.iterrows()
        },
        "year_change": {
            "total_cnt_2012_vs_2011_pct": round(
                (year_summary.loc[1, "total_cnt"] / year_summary.loc[0, "total_cnt"] - 1)
                * 100,
                6,
            ),
            "mean_cnt_2012_vs_2011_pct": round(
                (year_summary.loc[1, "mean_cnt"] / year_summary.loc[0, "mean_cnt"] - 1)
                * 100,
                6,
            ),
        },
        "by_season": grouped_summary("season"),
        "by_month": grouped_summary("mnth"),
        "by_hour": grouped_summary("hr"),
        "by_workingday": grouped_summary("workingday"),
        "by_workingday_user_type": {
            str(key): {
                name: round(float(value), 6)
                for name, value in row.items()
            }
            for key, row in df.groupby("workingday")[["casual", "registered", "cnt"]]
            .mean()
            .iterrows()
        },
        "peak_hour_by_workingday": {
            str(key): {
                "hour": int(grouped.droplevel(0).idxmax()),
                "mean_cnt": round(float(grouped.max()), 6),
            }
            for key, grouped in df.groupby(["workingday", "hr"])["cnt"]
            .mean()
            .groupby(level=0)
        },
        "by_weather": grouped_summary("weathersit"),
        "by_weekday": grouped_summary("weekday"),
        "correlations_pearson": {
            name: round(float(df[name].corr(cnt)), 6)
            for name in ["temp", "atemp", "hum", "windspeed", "casual", "registered"]
        },
    }

    OUTPUT_PATH.write_text(
        json.dumps(reference, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
