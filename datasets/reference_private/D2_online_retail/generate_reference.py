"""Regenera los valores privados de referencia de D2 Online Retail.

El script debe ejecutarse fuera del entorno accesible para los agentes. Lee la
copia congelada del libro original y conserva varias definiciones de importe
para que el corrector no imponga una única decisión de limpieza.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
DATASETS_DIR = HERE.parents[1]
INPUT_PATH = DATASETS_DIR / "experiment_inputs" / "D2_online_retail" / "Online Retail.xlsx"
OUTPUT_PATH = HERE / "reference_values.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def numeric_summary(series: pd.Series) -> dict[str, int | float]:
    return {
        "sum": round(float(series.sum()), 6),
        "mean": round(float(series.mean()), 6),
        "median": round(float(series.median()), 6),
        "std_sample": round(float(series.std(ddof=1)), 6),
        "min": round(float(series.min()), 6),
        "q1": round(float(series.quantile(0.25)), 6),
        "q3": round(float(series.quantile(0.75)), 6),
        "max": round(float(series.max()), 6),
    }


def main() -> None:
    df = pd.read_excel(INPUT_PATH)
    invoice = df["InvoiceNo"].astype(str).str.strip()
    is_cancel = invoice.str.upper().str.startswith("C")
    is_adjustment_invoice = invoice.str.upper().str.startswith("A")
    negative_quantity = df["Quantity"] < 0
    zero_price = df["UnitPrice"] == 0
    negative_price = df["UnitPrice"] < 0
    positive_sale = (df["Quantity"] > 0) & (df["UnitPrice"] > 0) & ~is_cancel
    line_total = df["Quantity"] * df["UnitPrice"]
    duplicated = df.duplicated(keep="first")

    monthly = pd.DataFrame(
        {
            "period": df["InvoiceDate"].dt.to_period("M").astype(str),
            "raw_value": line_total,
            "positive_value": line_total.where(positive_sale, 0),
            "cancellation_value": line_total.where(is_cancel, 0),
            "rows": 1,
        }
    ).groupby("period").agg(
        rows=("rows", "sum"),
        raw_value=("raw_value", "sum"),
        positive_value=("positive_value", "sum"),
        cancellation_value=("cancellation_value", "sum"),
    )

    country = pd.DataFrame(
        {
            "country": df["Country"],
            "rows": 1,
            "raw_value": line_total,
            "positive_value": line_total.where(positive_sale, 0),
        }
    ).groupby("country").agg(
        rows=("rows", "sum"),
        raw_value=("raw_value", "sum"),
        positive_value=("positive_value", "sum"),
    ).sort_values("positive_value", ascending=False)

    product_positive = (
        df.loc[positive_sale]
        .assign(line_total=line_total.loc[positive_sale])
        .groupby("StockCode")
        .agg(
            rows=("StockCode", "size"),
            quantity=("Quantity", "sum"),
            value=("line_total", "sum"),
        )
    )

    invoice_line_counts = df.groupby("InvoiceNo", dropna=False).size()
    description_counts_by_stock = (
        df.dropna(subset=["Description"])
        .assign(Description_normalized=lambda x: x["Description"].astype(str).str.strip().str.upper())
        .groupby("StockCode")["Description_normalized"]
        .nunique()
    )

    uk_rows = int((df["Country"] == "United Kingdom").sum())
    unique_invoices = int(df["InvoiceNo"].nunique(dropna=True))

    def representative_description(stock_code: object) -> str | None:
        descriptions = (
            df.loc[df["StockCode"] == stock_code, "Description"]
            .dropna()
            .astype(str)
            .str.strip()
        )
        if descriptions.empty:
            return None
        return str(descriptions.mode().iloc[0])

    top_quantity_code = product_positive["quantity"].idxmax()
    top_value_code = product_positive["value"].idxmax()

    reference = {
        "generated_from": {
            "path": "datasets/experiment_inputs/D2_online_retail/Online Retail.xlsx",
            "sha256": sha256(INPUT_PATH),
        },
        "structure": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": list(df.columns),
            "date_min": df["InvoiceDate"].min().isoformat(),
            "date_max": df["InvoiceDate"].max().isoformat(),
            "distinct_calendar_dates": int(df["InvoiceDate"].dt.date.nunique()),
            "distinct_timestamps": int(df["InvoiceDate"].nunique()),
            "distinct_month_periods": int(df["InvoiceDate"].dt.to_period("M").nunique()),
            "first_month": str(df["InvoiceDate"].dt.to_period("M").min()),
            "last_month": str(df["InvoiceDate"].dt.to_period("M").max()),
            "last_month_is_partial": True,
        },
        "missingness": {
            "missing_cells_total": int(df.isna().sum().sum()),
            "by_column": {key: int(value) for key, value in df.isna().sum().items()},
            "customer_id_rows": int(df["CustomerID"].isna().sum()),
            "customer_id_share": round(float(df["CustomerID"].isna().mean()), 9),
            "description_rows": int(df["Description"].isna().sum()),
            "description_share": round(float(df["Description"].isna().mean()), 9),
            "both_customer_and_description_rows": int(
                (df["CustomerID"].isna() & df["Description"].isna()).sum()
            ),
        },
        "identifiers_and_cardinality": {
            "unique_invoices": unique_invoices,
            "unique_stock_codes": int(df["StockCode"].nunique(dropna=True)),
            "unique_descriptions": int(df["Description"].nunique(dropna=True)),
            "unique_customers_non_null": int(df["CustomerID"].nunique(dropna=True)),
            "unique_countries": int(df["Country"].nunique(dropna=True)),
            "invoice_lines": numeric_summary(invoice_line_counts),
            "stock_codes_with_multiple_normalized_descriptions": int(
                (description_counts_by_stock > 1).sum()
            ),
            "max_normalized_descriptions_for_one_stock_code": int(
                description_counts_by_stock.max()
            ),
        },
        "duplicates": {
            "duplicate_rows_after_first": int(duplicated.sum()),
            "duplicate_share": round(float(duplicated.mean()), 9),
            "rows_after_drop_duplicates": int((~duplicated).sum()),
            "raw_value_removed_if_deduplicated": round(float(line_total.loc[duplicated].sum()), 6),
            "raw_value_after_deduplication": round(float(line_total.loc[~duplicated].sum()), 6),
        },
        "quantities_and_prices": {
            "quantity": numeric_summary(df["Quantity"]),
            "unit_price": numeric_summary(df["UnitPrice"]),
            "negative_quantity_rows": int(negative_quantity.sum()),
            "negative_quantity_share": round(float(negative_quantity.mean()), 9),
            "zero_quantity_rows": int((df["Quantity"] == 0).sum()),
            "zero_price_rows": int(zero_price.sum()),
            "zero_price_share": round(float(zero_price.mean()), 9),
            "negative_price_rows": int(negative_price.sum()),
            "negative_price_share": round(float(negative_price.mean()), 9),
        },
        "cancellations_and_adjustments": {
            "cancellation_rows": int(is_cancel.sum()),
            "cancellation_row_share": round(float(is_cancel.mean()), 9),
            "cancellation_invoices": int(df.loc[is_cancel, "InvoiceNo"].nunique()),
            "cancellation_invoice_share": round(
                float(df.loc[is_cancel, "InvoiceNo"].nunique() / unique_invoices), 9
            ),
            "cancellation_rows_with_negative_quantity": int(
                (is_cancel & negative_quantity).sum()
            ),
            "cancellation_rows_without_negative_quantity": int(
                (is_cancel & ~negative_quantity).sum()
            ),
            "negative_quantity_rows_without_c_prefix": int(
                (~is_cancel & negative_quantity).sum()
            ),
            "adjustment_invoice_rows_a_prefix": int(is_adjustment_invoice.sum()),
            "adjustment_invoices_a_prefix": int(
                df.loc[is_adjustment_invoice, "InvoiceNo"].nunique()
            ),
        },
        "values_sterling": {
            "raw_line_total": numeric_summary(line_total),
            "raw_net_value_all_rows": round(float(line_total.sum()), 6),
            "positive_sale_rows": int(positive_sale.sum()),
            "positive_sale_value": round(float(line_total.loc[positive_sale].sum()), 6),
            "cancellation_value": round(float(line_total.loc[is_cancel].sum()), 6),
            "negative_quantity_non_cancel_value": round(
                float(line_total.loc[~is_cancel & negative_quantity].sum()), 6
            ),
            "negative_price_value": round(float(line_total.loc[negative_price].sum()), 6),
            "zero_price_value": round(float(line_total.loc[zero_price].sum()), 6),
        },
        "country_concentration": {
            "uk_rows": uk_rows,
            "uk_row_share": round(uk_rows / len(df), 9),
            "uk_positive_value": round(float(country.loc["United Kingdom", "positive_value"]), 6),
            "uk_positive_value_share": round(
                float(country.loc["United Kingdom", "positive_value"] / line_total.loc[positive_sale].sum()),
                9,
            ),
            "top_countries_by_positive_value": [
                {
                    "country": str(key),
                    "rows": int(row["rows"]),
                    "positive_value": round(float(row["positive_value"]), 6),
                }
                for key, row in country.head(5).iterrows()
            ],
        },
        "temporal": {
            "monthly": {
                str(key): {
                    "rows": int(row["rows"]),
                    "raw_value": round(float(row["raw_value"]), 6),
                    "positive_value": round(float(row["positive_value"]), 6),
                    "cancellation_value": round(float(row["cancellation_value"]), 6),
                }
                for key, row in monthly.iterrows()
            },
            "highest_complete_month_by_positive_value": {
                "period": str(monthly.loc[monthly.index != "2011-12", "positive_value"].idxmax()),
                "value": round(
                    float(monthly.loc[monthly.index != "2011-12", "positive_value"].max()), 6
                ),
            },
        },
        "products_positive_sales": {
            "top_stock_code_by_quantity": {
                "stock_code": str(top_quantity_code),
                "representative_description": representative_description(top_quantity_code),
                "quantity": int(product_positive["quantity"].max()),
            },
            "top_stock_code_by_value": {
                "stock_code": str(top_value_code),
                "representative_description": representative_description(top_value_code),
                "value": round(float(product_positive["value"].max()), 6),
            },
        },
    }

    OUTPUT_PATH.write_text(
        json.dumps(reference, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
