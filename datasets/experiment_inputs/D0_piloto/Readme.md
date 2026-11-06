# D0_piloto — Pedidos sintéticos

## Finalidad

Este dataset se utilizará exclusivamente para validar el protocolo técnico antes de ejecutar el experimento definitivo con D1 y D2. Sus resultados no formarán parte de la comparación final de frameworks.

El archivo ha sido generado de forma sintética y no contiene información de personas o empresas reales. Cada fila representa un pedido.

## Archivo de entrada

- `pedidos_piloto.csv`
- Formato: CSV en UTF-8, separado por comas.
- Periodo general: primer semestre de 2025.
- Unidad de observación: pedido.

## Diccionario de variables

| Variable | Descripción |
| --- | --- |
| `order_id` | Identificador nominal del pedido. |
| `order_date` | Fecha del pedido en formato `AAAA-MM-DD`. |
| `region` | Región comercial. |
| `channel` | Canal por el que se registró el pedido. |
| `customer_type` | Tipo de cliente. |
| `product_category` | Categoría del producto o servicio. |
| `units` | Número de unidades solicitadas. |
| `unit_price_eur` | Precio unitario en euros. |
| `discount_rate` | Descuento expresado como proporción entre 0 y 1. |
| `delivery_days` | Días transcurridos hasta la entrega; no debería ser negativo. |
| `satisfaction_score` | Valoración de satisfacción de 1 a 5. |
| `returned` | Indicador binario: 1 si el pedido fue devuelto y 0 en caso contrario. |
| `net_amount_eur` | Importe neto registrado. La relación esperada es `units × unit_price_eur × (1 - discount_rate)`. |

## Tarea

Realizar un análisis exploratorio de datos tabulares que cubra carga e inspección, estructura y tipos, calidad de datos, preparación, estadística descriptiva, relaciones y agregaciones relevantes, evolución temporal, visualizaciones, detección de problemas y elaboración de un informe final.

Las decisiones de limpieza deben justificarse y conservar trazabilidad. No se solicita entrenar modelos predictivos ni realizar inferencias causales.
