/**
 * Regenera la entrada sintética y los valores privados de D0_piloto.
 *
 * Este archivo debe ejecutarse fuera del entorno de los agentes. Usa una
 * semilla fija y no depende de fuentes externas, por lo que la salida es
 * reproducible byte a byte.
 */

import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const datasetsDir = path.resolve(here, "..", "..");
const inputPath = path.join(
  datasetsDir,
  "experiment_inputs",
  "D0_piloto",
  "pedidos_piloto.csv",
);
const referencePath = path.join(here, "reference_values.json");

const seed = 20260808;
const baseRowCount = 240;
const columns = [
  "order_id",
  "order_date",
  "region",
  "channel",
  "customer_type",
  "product_category",
  "units",
  "unit_price_eur",
  "discount_rate",
  "delivery_days",
  "satisfaction_score",
  "returned",
  "net_amount_eur",
];

function mulberry32(initialSeed) {
  let state = initialSeed >>> 0;
  return () => {
    state += 0x6d2b79f5;
    let value = state;
    value = Math.imul(value ^ (value >>> 15), value | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

function chooseWeighted(random, entries) {
  const draw = random();
  let cumulative = 0;
  for (const [value, weight] of entries) {
    cumulative += weight;
    if (draw < cumulative) return value;
  }
  return entries.at(-1)[0];
}

function round(value, digits = 2) {
  const factor = 10 ** digits;
  return Math.round((value + Number.EPSILON) * factor) / factor;
}

function isoDateFromOffset(startUtc, dayOffset) {
  const date = new Date(startUtc + dayOffset * 86400000);
  return date.toISOString().slice(0, 10);
}

function csvCell(value) {
  if (value === null || value === undefined) return "";
  const text = String(value);
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function rowKey(row) {
  return JSON.stringify(columns.map((column) => row[column]));
}

function normalizeRegion(value) {
  if (value === null || value === undefined || String(value).trim() === "") return null;
  const normalized = String(value).trim().toLowerCase();
  return {
    norte: "Norte",
    sur: "Sur",
    este: "Este",
    oeste: "Oeste",
  }[normalized] ?? String(value).trim();
}

function normalizeChannel(value) {
  if (value === null || value === undefined || String(value).trim() === "") return null;
  const normalized = String(value).trim().toLowerCase();
  return {
    online: "Online",
    tienda: "Tienda",
    socio: "Socio",
  }[normalized] ?? String(value).trim();
}

function sum(values) {
  return values.reduce((total, value) => total + value, 0);
}

function mean(values) {
  return values.length === 0 ? null : sum(values) / values.length;
}

function median(values) {
  if (values.length === 0) return null;
  const ordered = [...values].sort((a, b) => a - b);
  const middle = Math.floor(ordered.length / 2);
  return ordered.length % 2 === 0
    ? (ordered[middle - 1] + ordered[middle]) / 2
    : ordered[middle];
}

function groupSummary(rows, keyFunction) {
  const groups = new Map();
  for (const row of rows) {
    const key = keyFunction(row);
    if (key === null || key === undefined || key === "") continue;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return Object.fromEntries(
    [...groups.entries()]
      .sort(([left], [right]) => String(left).localeCompare(String(right), "es"))
      .map(([key, group]) => {
        const recordedAmounts = group.map((row) => Number(row.net_amount_eur));
        const validDelivery = group
          .map((row) => row.delivery_days)
          .filter((value) => value !== null && value >= 0);
        return [
          key,
          {
            rows: group.length,
            recorded_net_sum: round(sum(recordedAmounts), 2),
            mean_recorded_net: round(mean(recordedAmounts), 6),
            mean_valid_delivery_days:
              validDelivery.length > 0 ? round(mean(validDelivery), 6) : null,
          },
        ];
      }),
  );
}

function sha256(buffer) {
  return crypto.createHash("sha256").update(buffer).digest("hex").toUpperCase();
}

function buildRows() {
  const random = mulberry32(seed);
  const startUtc = Date.UTC(2025, 0, 1);
  const regions = [
    ["Norte", 0.3],
    ["Sur", 0.25],
    ["Este", 0.25],
    ["Oeste", 0.2],
  ];
  const channels = [
    ["Online", 0.45],
    ["Tienda", 0.35],
    ["Socio", 0.2],
  ];
  const customerTypes = [
    ["Minorista", 0.55],
    ["Empresa", 0.35],
    ["Mayorista", 0.1],
  ];
  const products = [
    ["Equipamiento", 0.25],
    ["Consumibles", 0.35],
    ["Software", 0.2],
    ["Servicios", 0.2],
  ];
  const basePrice = {
    Equipamiento: 120,
    Consumibles: 18,
    Software: 240,
    Servicios: 85,
  };

  const rows = [];
  for (let index = 0; index < baseRowCount; index += 1) {
    const dayOffset = Math.floor((index * 160) / (baseRowCount - 1));
    const region = chooseWeighted(random, regions);
    const channel = chooseWeighted(random, channels);
    const customerType = chooseWeighted(random, customerTypes);
    const productCategory = chooseWeighted(random, products);

    let units;
    if (customerType === "Minorista") units = 1 + Math.floor(random() * 5);
    else if (customerType === "Empresa") units = 3 + Math.floor(random() * 13);
    else units = 12 + Math.floor(random() * 24);

    const unitPrice = round(
      basePrice[productCategory] * (0.82 + random() * 0.36),
      2,
    );
    const discountOptions =
      customerType === "Minorista"
        ? [0, 0.05]
        : customerType === "Empresa"
          ? [0.08, 0.1, 0.12]
          : [0.15, 0.18, 0.2];
    const discountRate = discountOptions[Math.floor(random() * discountOptions.length)];

    const channelBase = { Online: 3, Tienda: 1, Socio: 4 }[channel];
    const regionExtra = region === "Oeste" ? 1 : 0;
    const deliveryDays = Math.max(
      0,
      channelBase + regionExtra + Math.floor(random() * 3) - 1,
    );
    const returnProbability = 0.04 + (deliveryDays >= 5 ? 0.08 : 0);
    const returned = random() < returnProbability ? 1 : 0;
    const satisfactionScore = Math.max(
      1,
      Math.min(5, 5 - Math.floor(deliveryDays / 3) - returned + Math.floor(random() * 2)),
    );

    rows.push({
      order_id: `PED-${String(index + 1).padStart(4, "0")}`,
      order_date: isoDateFromOffset(startUtc, dayOffset),
      region,
      channel,
      customer_type: customerType,
      product_category: productCategory,
      units,
      unit_price_eur: unitPrice,
      discount_rate: discountRate,
      delivery_days: deliveryDays,
      satisfaction_score: satisfactionScore,
      returned,
      net_amount_eur: 0,
    });
  }

  // Ausencias controladas.
  for (const index of [33, 177]) rows[index].order_date = null;
  for (const index of [12, 91, 208]) rows[index].region = null;
  for (const index of [18, 58, 98, 138, 218]) rows[index].delivery_days = null;
  for (const index of [7, 27, 47, 67, 87, 107, 127, 147, 167, 187, 207, 227]) {
    rows[index].satisfaction_score = null;
  }

  // Variantes de escritura que representan las mismas categorías.
  rows[25].region = "norte";
  rows[55].region = " SUR";
  rows[125].region = "Este ";
  rows[155].region = "OESTE";
  rows[205].region = "nOrTe";
  rows[44].channel = "online ";
  rows[144].channel = "TIENDA";
  rows[204].channel = "socio";

  // Valores inválidos y un extremo válido de negocio mayorista.
  rows[67].discount_rate = -0.05;
  rows[201].discount_rate = 1.15;
  rows[88].delivery_days = -1;
  rows[199].delivery_days = -2;
  rows[150].customer_type = "Mayorista";
  rows[150].product_category = "Equipamiento";
  rows[150].units = 85;
  rows[150].discount_rate = 0.2;

  // El importe se calcula después de introducir las modificaciones anteriores.
  for (const row of rows) {
    row.net_amount_eur = round(
      row.units * row.unit_price_eur * (1 - row.discount_rate),
      2,
    );
  }

  // Cuatro importes registrados no coinciden con la relación documentada.
  const amountAdjustments = new Map([
    [31, 10],
    [104, -7.5],
    [167, 12.34],
    [223, -5],
  ]);
  for (const [index, adjustment] of amountAdjustments) {
    rows[index].net_amount_eur = round(rows[index].net_amount_eur + adjustment, 2);
  }

  // Seis duplicados exactos añadidos después de la primera aparición.
  for (const index of [9, 45, 87, 123, 165, 207]) rows.push({ ...rows[index] });

  return rows;
}

function buildReference(rows, inputSha256) {
  const missingByColumn = Object.fromEntries(
    columns.map((column) => [
      column,
      rows.filter((row) => row[column] === null || row[column] === undefined).length,
    ]),
  );
  const seenRows = new Set();
  let duplicateRows = 0;
  const deduplicatedRows = [];
  for (const row of rows) {
    const key = rowKey(row);
    if (seenRows.has(key)) duplicateRows += 1;
    else {
      seenRows.add(key);
      deduplicatedRows.push(row);
    }
  }

  const seenOrderIds = new Set();
  let duplicateOrderIds = 0;
  for (const row of rows) {
    if (seenOrderIds.has(row.order_id)) duplicateOrderIds += 1;
    else seenOrderIds.add(row.order_id);
  }

  const validDates = rows
    .map((row) => row.order_date)
    .filter((value) => value !== null)
    .sort();
  const rawRegionLabels = [...new Set(rows.map((row) => row.region).filter(Boolean))].sort();
  const rawChannelLabels = [...new Set(rows.map((row) => row.channel).filter(Boolean))].sort();
  const normalizedRegions = [
    ...new Set(rows.map((row) => normalizeRegion(row.region)).filter(Boolean)),
  ].sort();
  const normalizedChannels = [
    ...new Set(rows.map((row) => normalizeChannel(row.channel)).filter(Boolean)),
  ].sort();

  const recalculatedAmounts = rows.map((row) =>
    round(row.units * row.unit_price_eur * (1 - row.discount_rate), 2),
  );
  const identityErrors = rows.filter((row, index) =>
    Math.abs(row.net_amount_eur - recalculatedAmounts[index]) > 0.011,
  ).length;
  const units = rows.map((row) => row.units);
  const recordedAmounts = rows.map((row) => row.net_amount_eur);
  const satisfaction = rows
    .map((row) => row.satisfaction_score)
    .filter((value) => value !== null);
  const validDelivery = rows
    .map((row) => row.delivery_days)
    .filter((value) => value !== null && value >= 0);

  const byMonth = groupSummary(rows, (row) =>
    row.order_date === null ? null : row.order_date.slice(0, 7),
  );
  const completeMonthEntries = Object.entries(byMonth).filter(([month]) => month !== "2025-06");
  const highestCompleteMonth = completeMonthEntries.reduce((best, current) =>
    current[1].recorded_net_sum > best[1].recorded_net_sum ? current : best,
  );

  const byReturned = Object.fromEntries(
    [0, 1].map((returned) => {
      const group = rows.filter((row) => row.returned === returned);
      const groupSatisfaction = group
        .map((row) => row.satisfaction_score)
        .filter((value) => value !== null);
      return [
        String(returned),
        {
          rows: group.length,
          mean_satisfaction_non_null: round(mean(groupSatisfaction), 6),
        },
      ];
    }),
  );

  return {
    generated_from: {
      path: "datasets/experiment_inputs/D0_piloto/pedidos_piloto.csv",
      sha256: inputSha256,
      generator: "datasets/reference_private/D0_piloto/generate_pilot.mjs",
      generator_version: "1.0",
      seed,
    },
    structure: {
      rows: rows.length,
      columns: columns.length,
      column_names: columns,
      unique_order_ids: seenOrderIds.size,
      date_min: validDates[0],
      date_max: validDates.at(-1),
      months_present: Object.keys(byMonth).length,
      partial_last_month: "2025-06",
    },
    quality: {
      missing_cells_total: sum(Object.values(missingByColumn)),
      missing_by_column: missingByColumn,
      duplicate_rows_after_first: duplicateRows,
      rows_after_drop_duplicates: deduplicatedRows.length,
      duplicate_order_ids_after_first: duplicateOrderIds,
      raw_region_labels: rawRegionLabels,
      raw_region_label_count: rawRegionLabels.length,
      normalized_region_categories: normalizedRegions,
      normalized_region_category_count: normalizedRegions.length,
      raw_channel_labels: rawChannelLabels,
      raw_channel_label_count: rawChannelLabels.length,
      normalized_channel_categories: normalizedChannels,
      normalized_channel_category_count: normalizedChannels.length,
      invalid_discount_rows: rows.filter(
        (row) => row.discount_rate < 0 || row.discount_rate > 1,
      ).length,
      negative_delivery_rows: rows.filter(
        (row) => row.delivery_days !== null && row.delivery_days < 0,
      ).length,
      amount_identity_errors: identityErrors,
      high_unit_rows_50_or_more: rows.filter((row) => row.units >= 50).length,
    },
    overall: {
      units_sum: sum(units),
      units_mean: round(mean(units), 6),
      units_median: round(median(units), 6),
      units_max: Math.max(...units),
      recorded_net_sum: round(sum(recordedAmounts), 2),
      recalculated_net_sum: round(sum(recalculatedAmounts), 2),
      returned_rows: rows.filter((row) => row.returned === 1).length,
      return_rate: round(mean(rows.map((row) => row.returned)), 9),
      satisfaction_mean_non_null: round(mean(satisfaction), 6),
      valid_delivery_mean: round(mean(validDelivery), 6),
    },
    sensitivity: {
      recorded_net_after_exact_deduplication: round(
        sum(deduplicatedRows.map((row) => row.net_amount_eur)),
        2,
      ),
      recorded_net_difference_due_to_exact_duplicates: round(
        sum(recordedAmounts) - sum(deduplicatedRows.map((row) => row.net_amount_eur)),
        2,
      ),
    },
    temporal: {
      by_month: byMonth,
      highest_complete_month_by_recorded_net: {
        month: highestCompleteMonth[0],
        value: highestCompleteMonth[1].recorded_net_sum,
      },
    },
    by_region_normalized: groupSummary(rows, (row) => normalizeRegion(row.region)),
    by_channel_normalized: groupSummary(rows, (row) => normalizeChannel(row.channel)),
    by_product_category: groupSummary(rows, (row) => row.product_category),
    by_returned: byReturned,
  };
}

async function main() {
  const rows = buildRows();
  const csvLines = [
    columns.join(","),
    ...rows.map((row) => columns.map((column) => csvCell(row[column])).join(",")),
  ];
  const csvBuffer = Buffer.from(`${csvLines.join("\n")}\n`, "utf8");
  const inputSha256 = sha256(csvBuffer);
  const reference = buildReference(rows, inputSha256);

  if (reference.structure.rows !== 246 || reference.structure.columns !== 13) {
    throw new Error("La estructura generada no coincide con el diseño de D0.");
  }
  if (
    reference.quality.duplicate_rows_after_first !== 6 ||
    reference.quality.invalid_discount_rows !== 2 ||
    reference.quality.negative_delivery_rows !== 2 ||
    reference.quality.amount_identity_errors !== 4
  ) {
    throw new Error("Las anomalías controladas de D0 no coinciden con el diseño.");
  }

  await fs.mkdir(path.dirname(inputPath), { recursive: true });
  await fs.writeFile(inputPath, csvBuffer);
  await fs.writeFile(
    referencePath,
    `${JSON.stringify(reference, null, 2)}\n`,
    "utf8",
  );

  console.log(
    JSON.stringify({
      input: path.relative(datasetsDir, inputPath).replaceAll("\\", "/"),
      sha256: inputSha256,
      rows: reference.structure.rows,
      columns: reference.structure.columns,
      missing_cells: reference.quality.missing_cells_total,
      duplicate_rows: reference.quality.duplicate_rows_after_first,
    }),
  );
}

await main();
