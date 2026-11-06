# Evaluación D2-MAF-R3

**Índice final: 84,13/100.** Evaluación cerrada el 6 de octubre de 2026.

Esta ficha recoge las puntuaciones y evidencias de D2-MAF-R3.

**Ejecución:** `D2_online_retail__microsoft_agent_framework__r03__20260902T200335090326Z`  
**Productos:** [carpeta original](../../../outputs/experimento/D2_online_retail__microsoft_agent_framework__r03__20260902T200335090326Z)  
**Reglas:** [protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D2](../02_ficha_D2_online_retail.md)  
**Comprobaciones:** [comprobaciones y evidencias](D2-MAF-R3_comprobaciones.json)

Las referencias STAT, ISSUE y FIG identifican estadísticas, problemas y figuras de la ejecución. Las referencias TR identifican las transformaciones registradas y los números de línea remiten a `report.md`.

## Resumen de puntuaciones

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 82,98 |
| Q3 Validez del tratamiento de los datos | 91,67 |
| Q4 Detección de problemas y riesgos | 85,11 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 60,00 |
| Q8 Cobertura del informe | 93,18 |
| Q9 Fidelidad del informe | 99,42 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

Las ocho etapas tienen evidencia válida:

| Etapa | Nota | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | Plan, STAT-001 y perfil |
| E2 Estructura, tipos y calidad | 1 | STAT-002–006 |
| E3 Preparación y decisiones de análisis | 1 | CSV, TR-001–004 y STAT-007 |
| E4 Estadística descriptiva | 1 | STAT-008/009/010 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-011–015 |
| E6 Visualizaciones | 1 | Cuatro PNG válidos e integrados |
| E7 Problemas, riesgos y anomalías | 1 | Siete incidencias, comprobaciones y extremos |
| E8 Informe final | 1 | Alcance, preparación, resultados y límites |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 82,98

Se consideran correctas 25 de las 32 comprobaciones, que suman 39 de los 47 puntos.

| Controles | Resultado | Evidencia o motivo |
| --- | --- | --- |
| C01–C07 | Correctos | Estructura, fechas y ausencias. STAT-001/002 |
| C08 | Ausente | No presenta cuántos registros tienen ausentes simultáneamente CustomerID y Description |
| C09 | Correcto | 5268 duplicados después del primero. STAT-003 |
| C10 | Correcto | Los 541.909 registros originales menos los 5.268 duplicados dan 536.641 registros. STAT-001 y STAT-003 |
| C11–C15 | Correctos | Entidades y líneas C. STAT-003/004 |
| C16 | Ausente | No presenta el número de facturas distintas cuyo identificador comienza por C |
| C17–C20 | Correctos | Signos y precios. STAT-004 |
| C21 | Correcto | 	La media de Quantity multiplicada por los 541.909 registros permite obtener 5.176.450 unidades. Se utiliza la precisión conservada en STAT-008 |
| C22–C23 | Correctos | Presenta las cantidades mínima y máxima del conjunto completo. STAT-008 |
| C24 | Correcto | Los trece importes netos mensuales de STAT-005 suman 9.747.747,934 GBP |
| C25–C26 | Correctos | Presenta el número de registros de ventas positivas y su importe total. STAT-009 |
| C27 | Ausente | No presenta el importe agregado de los registros con marca de cancelación |
| C28 | Ausente | No presenta el importe neto después de excluir los duplicados exactos |
| C29 | Ausente | Presenta 485.123 registros del Reino Unido dentro de las ventas positivas y un 84,61 % referido a su importe, pero no el porcentaje de registros del Reino Unido sobre el archivo original |
| C30 | Correcto | Noviembre2011 y 1509496,33 GBP positivos. STAT-011 e informe7/39 |
| C31 | Ausente | Identifica 650 códigos con varias descripciones originales, pero no los 647 obtenidos después de eliminar espacios iniciales y finales y convertir las descripciones a mayúsculas |
| C32 | Ausente | No presenta la mediana del número de registros por factura |

`Q2 = 100 x 39 / 47 = 82,98`

## Q3 Validez del tratamiento de los datos: 91,67

| Decisión | Nota | Justificación y evidencia |
| --- | ---: | --- |
| D01 Identificadores | 1 | Los identificadores se utilizan como etiquetas, no como cantidades. CustomerID se conserva como entero que admite valores ausentes. TR-001 |
| D02 Fecha-hora | 1 | CSV conserva fecha y hora fila a fila. TR-002 |
| D03 Importe | 1 | Identidad correcta y poblaciones explícitas. STAT-007/008/009 |
| D04 Unidades | 1 | Distingue líneas, facturas, clientes y productos. Perfil, STAT-003/013/014 |
| D05 Cancelaciones | 1 | C identificado y conservado, incluidos agregados netos. STAT-004/005 |
| D06 Cliente ausente | 1 | Conserva los registros sin CustomerID y compara sus resultados con los de los registros que sí tienen identificador. STAT-014 |
| D07 Descripción ausente | 1 | Conserva ausencias, sin completar el texto fuente |
| D08 Duplicados | 0 | Conserva los duplicados, pero no compara los resultados con y sin esas filas. ISSUE-003 |
| D09 Ajustes | 1 | Separa negativos sin C, precios cero y negativos. STAT-004 |
| D10 Extremos | 1 | Conserva datos y ofrece cuantiles, vallas IQR y vista central. STAT-009/010, FIG-003 |
| D11 Mes final | 1 | Diciembre 2011 identificado como parcial. Informe39 y ISSUE-006 |
| D12 Categorías | 1 | Limita los gráficos a las categorías principales y agrupa por StockCode. Utiliza la descripción más frecuente como etiqueta, sin modificar las descripciones originales. STAT-012/013 y FIG-002/004 |

`Q3 = 100 x 11 / 12 = 91,67`

## Q4 Detección de problemas y riesgos: 85,11

Se detectan por completo ocho de los diez riesgos de referencia y dos problemas adicionales válidos. Una advertencia carece de respaldo suficiente. La precisión es 10/11 y la cobertura, 8/10.

| Riesgo | Resultado | Evidencia |
| --- | --- | --- |
| R01 Ausencias | Detectado | STAT-002, ISSUE-001/002 |
| R02 Duplicados | Detectado | STAT-003, ISSUE-003 |
| R03 C y signos | Detectado | STAT-004 e informe37 |
| R04 Negativos sin C | Detectado | 1336 casos, STAT-004 e informe37 |
| R05 Precios cero y negativos | Detectado | STAT-004 e informe37 |
| R06 Unidad e identificadores | Detectado | Perfil, TR-001 e informe3/19/21 |
| R07 Mes final parcial | Detectado | Informe39/51, ISSUE-006 |
| R08 Concentración en líneas originales | Parcial | Predominio monetario positivo, sin cuota de líneas originales |
| R09 Asimetría y extremos | Detectado | STAT-008/009/010, ISSUE-007 |
| R10 Definiciones monetarias | Parcial | Neto y positivos definidos, sin importe C ni efecto deduplicado |
| A01 Varias descripciones para un mismo código | Adicional válido | STAT-006, ISSUE-005 e informe73 |
| A02 Conceptos especiales en los resultados por producto | Adicional válido | Informe43/83/91 identifica DOT, POST y M y pide cautela con productos o conceptos especiales |
| F01 Diciembre 2010 incompleto | Sin respaldo | Advertencia categórica en informe7/74 |

`Q4 = 100 x [2 x (10 / 11) x (8 / 10)] / [(10 / 11) + (8 / 10)] = 85,11`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina las distribuciones del conjunto completo y de las ventas positivas, identifica valores extremos y estudia la evolución temporal, los países, los productos y las diferencias entre registros con y sin identificador de cliente. También analiza la relación entre cantidad y precio mediante la correlación de Spearman. No alcanza el nivel 4 porque no compara los resultados con y sin duplicados ni cuantifica el importe agregado de las cancelaciones. Evidencia: STAT-008–015.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

El informe interpreta la asimetría, la concentración de los importes, una operación extrema y las diferencias entre registros con y sin identificador de cliente, sin atribuirles causas ni asociarlas a tipos de cliente no documentados. También advierte de las limitaciones para interpretar los códigos especiales como productos ordinarios. Sin embargo, presenta diciembre de 2010 como un mes incompleto sin respaldo suficiente y no desarrolla cómo cambian los importes al excluir duplicados o separar las cancelaciones. Evidencia: líneas 31, 33, 39, 41, 43, 45, 47, 74, 83 y 85 del informe.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 60,00

| Objetivo | Nota 0–4 | Justificación |
| --- | ---: | --- |
| V01 Evolución | 4 | FIG-001 positiva mensual, unidades y población claras. El informe integra la advertencia sobre diciembre 2011 |
| V02 Cancelaciones/ajustes | 0 | No hay representación específica de C, cantidades negativas ni precios no positivos |
| V03 Distribuciones | 2 | FIG-003 muestra los valores positivos hasta el percentil 99. El recorte está indicado, pero no se representan los valores superiores ni los valores cero o negativos |
| V04 Países | 2 | FIG-002 correcta, pero UK comprime al resto, sin vista complementaria |
| V05 Productos/conceptos/clientes | 4 | FIG-004 top10 por StockCode, importe definido e interpretación. Descripciones abreviadas auxiliares sin pérdida de identidad |

`Q7 = 100 x 12 / 20 = 60,00`

## Q8 Cobertura del informe: 93,18

Veinte y medio de veintidós puntos ponderados. Solo se acredita el informe y las figuras integradas, no información presente únicamente en el plan o las estadísticas.

| Unidad | Peso | Nota | Evidencia o motivo |
| --- | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | Informe3/19/89 |
| U02 Ausencias e impacto | 2 | 1 | Informe27/69/70/81 |
| U03 Unidades | 2 | 1 | Informe3/11/29/43/79 |
| U04 Duplicados y decisión | 2 | 1 | Informe23/29/71 |
| U05 C y negativos | 2 | 1 | Informe37/72 |
| U06 Ajustes | 2 | 1 | Informe37 cuantifica negativos sin C y precios cero/negativos |
| U07 Agregados monetarios | 2 | 0,5 | Distingue las ventas positivas y las cancelaciones, pero no comunica el importe neto total, el importe agregado de cancelaciones ni el efecto de excluir duplicados |
| U08 Evolución y mes final | 2 | 1 | Informe7/39/51, FIG-001 |
| U09 Concentración UK | 2 | 1 | Informe41/55, composición observada sin comparación causal de mercados |
| U10 Cardinalidad y conceptos | 1 | 1 | Informe43/63/83/91 distingue productos y conceptos especiales y advierte sobre DOT, POST y M |
| U11 Asimetría y extremos | 2 | 1 | Informe7/31/33/43/59 |
| U12 Cobertura y límites | 1 | 0,5 | Ausencias e incertidumbres explicadas. No indica una sola empresa |

`Q8 = 100 x 20,5 / 22 = 93,18`

## Q9 Fidelidad del informe: 99,42

Se respaldan 170 de las 171 afirmaciones evaluadas. AF171 carece de respaldo suficiente porque el informe presenta diciembre de 2010 como un mes incompleto por ser el primero del archivo, sin demostrar que falten registros de ese mes.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 170 / 171 = 99,42`

## Q10 Claridad y coherencia: 75,00

El informe presenta una estructura organizada, especifica qué registros incluye en cada análisis y aporta referencias que permiten localizar las evidencias. Sin embargo, el contexto y el significado de algunas variables no se explican suficientemente, y la advertencia sobre diciembre de 2010 introduce una incoherencia localizada.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada. S = sin respaldo suficiente.

| ID | Líneas del informe | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3/11/13/15/19/21/23/79/89 | Libro XLSX y hoja Online Retail | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF002 | 3/11/13/15/19/21/23/79/89 | 541909 líneas fuente | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF003 | 3/11/13/15/19/21/23/79/89 | Ocho campos originales | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF004 | 3/11/13/15/19/21/23/79/89 | Lista de ocho variables correcta | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF005 | 3/11/13/15/19/21/23/79/89 | Una fila es una línea de factura | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF006 | 3/11/13/15/19/21/23/79/89 | Una fila no es necesariamente una compra completa | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF007 | 3/11/13/15/19/21/23/79/89 | Una fila no es una factura agregada | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF008 | 3/11/13/15/19/21/23/79/89 | Una fila no equivale a un cliente | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF009 | 3/11/13/15/19/21/23/79/89 | Una factura puede ocupar varias filas | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF010 | 3/11/13/15/19/21/23/79/89 | Primera fecha-hora2010-12-01T08:26:00 | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF011 | 3/11/13/15/19/21/23/79/89 | Última fecha-hora2011-12-09T12:50:00 | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF012 | 3/11/13/15/19/21/23/79/89 | Country corresponde al país asociado al cliente | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF013 | 3/11/13/15/19/21/23/79/89 | Country no acredita destino del envío | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF014 | 3/11/13/15/19/21/23/79/89 | Country no acredita país de consumo | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF015 | 3/11/13/15/19/21/23/79/89 | Country no acredita residencia definitiva | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF016 | 3/11/13/15/19/21/23/79/89 | LineAmountGBP=QuantityxUnitPrice | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF017 | 3/11/13/15/19/21/23/79/89 | Importe expresado en GBP | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF018 | 3/11/13/15/19/21/23/79/89 | Diferencia de identidad en memoria0 | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF019 | 3/11/13/15/19/21/23/79/89 | Importe no acredita cobro | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF020 | 3/11/13/15/19/21/23/79/89 | Importe no acredita ingreso contable | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF021 | 3/11/13/15/19/21/23/79/89 | Importe no acredita margen | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF022 | 3/11/13/15/19/21/23/79/89 | Importe no acredita beneficio | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF023 | 3/11/13/15/19/21/23/79/89 | InvoiceNo original object | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF024 | 3/11/13/15/19/21/23/79/89 | StockCode original object | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF025 | 3/11/13/15/19/21/23/79/89 | CustomerID original decimal nominal | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF026 | 3/11/13/15/19/21/23/79/89 | Identificadores convertidos a tipos nominales | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF027 | 3/11/13/15/19/21/23/79/89 | InvoiceNo a texto | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF028 | 3/11/13/15/19/21/23/79/89 | StockCode a texto | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF029 | 3/11/13/15/19/21/23/79/89 | CustomerID a entero nullable | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF030 | 3/11/13/15/19/21/23/79/89 | La copia retiene541909 filas | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF031 | 3/11/13/15/19/21/23/79/89 | La copia retiene las ocho variables fuente | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF032 | 3/11/13/15/19/21/23/79/89 | Cuatro variables derivadas añadidas | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF033 | 3/11/13/15/19/21/23/79/89 | IsCancellation marca C | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF034 | 3/11/13/15/19/21/23/79/89 | Month identifica período mensual | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF035 | 3/11/13/15/19/21/23/79/89 | CustomerIDAvailable indica disponibilidad | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF036 | 3/11/13/15/19/21/23/79/89 | InvoiceDate conserva fecha y hora | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF037 | 3/11/13/15/19/21/23/79/89 | Fecha-hora serializada ISO8601 en CSV | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF038 | 3/11/13/15/19/21/23/79/89 | No se eliminan duplicados | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF039 | 3/11/13/15/19/21/23/79/89 | No se eliminan cancelaciones | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF040 | 3/11/13/15/19/21/23/79/89 | No se eliminan ceros | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF041 | 3/11/13/15/19/21/23/79/89 | No se eliminan ausencias | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF042 | 3/11/13/15/19/21/23/79/89 | No se eliminan extremos | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF043 | 3/11/13/15/19/21/23/79/89 | Fuente original no modificada | R | STAT-001/007, TR-001–004, CSV, evento16 y diccionario público |
| AF044 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Positivos excluye C | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF045 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Positivos exige Quantity>0 | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF046 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Positivos exige UnitPrice>0 | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF047 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Filtro es subconjunto analítico, no eliminación del CSV | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF048 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 530104 líneas positivas | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF049 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 19960 facturas positivas | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF050 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Importe positivo10666684,54 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF051 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Mediana importe positivo9,90 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF052 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | P99 importe positivo183,60 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF053 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Importe positivo marcadamente asimétrico | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF054 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | UK84,61% del importe positivo | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF055 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Noviembre2011 máximo mensual positivo | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF056 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Noviembre positivo1509496,33 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF057 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | CustomerID ausente135080 | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF058 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | CustomerID ausente24,927% | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF059 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Description ausente1454 | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF060 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Description ausente0,268% | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF061 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Sin ausencias InvoiceNo | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF062 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Sin ausencias StockCode | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF063 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Sin ausencias Quantity | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF064 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Sin ausencias InvoiceDate | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF065 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Sin ausencias UnitPrice | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF066 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Sin ausencias Country | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF067 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 25900 InvoiceNo distintos | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF068 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 4070 StockCode distintos | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF069 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 4372 CustomerID no ausentes distintos | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF070 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 38 países | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF071 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 5268 duplicados exactos después del primero | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF072 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Mediana Quantity positiva3 unidades | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF073 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | P99 Quantity positiva100 | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF074 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Máximo Quantity positiva80995 | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF075 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Mediana UnitPrice positivo2,08 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF076 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | P99 UnitPrice positivo16,98 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF077 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Máximo UnitPrice positivo13541,33 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF078 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | P25 importe positivo3,75 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF079 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | P75 importe positivo17,70 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF080 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Máximo importe positivo168469,60 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF081 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Quantity positiva presenta cola larga | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF082 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | UnitPrice positivo presenta cola larga | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF083 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 56363 líneas sobre valla superior IQR Quantity | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF084 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 37999 sobre valla superior IQR UnitPrice | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF085 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 42651 sobre valla superior IQR importe | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF086 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | La regla IQR no acredita error | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF087 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | C identifica cancelación según documentación | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF088 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 9288 líneas C | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF089 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | C1,714% del total | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF090 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Todas las líneas C tienen Quantity negativa | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF091 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 1336 negativas sin C | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF092 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Dos precios negativos | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF093 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 2515 precios cero | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF094 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Septiembre2011 positivo1058590,17 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF095 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Octubre2011 positivo1154979,30 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF096 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Aumento de importe positivo septiembre–noviembre | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF097 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Diciembre 2011 termina el día9 | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF098 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Diciembre 2011 parcial | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF099 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Diciembre 2011 positivo638792,68 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF100 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | UK485123 líneas positivas | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF101 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | UK18019 facturas positivas | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF102 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | UK9025222,08 GBP positivos | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF103 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Netherlands segundo por importe positivo | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF104 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Netherlands285446,34 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF105 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | EIRE tercero por importe positivo | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF106 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | EIRE283453,96 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF107 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Germany cuarto por importe positivo | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF108 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Germany228867,14 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF109 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | France quinto por importe positivo | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF110 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | France209715,11 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF111 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Agregación geográfica describe composición, no causalidad de mercados | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF112 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Ranking agrupa por StockCode | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF113 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | DOT primero por importe positivo | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF114 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | DOT descripción DOTCOM POSTAGE | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF115 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | DOT206248,77 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF116 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 22423 descripción REGENCY CAKESTAND 3 TIER | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF117 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 22423 importe174484,74 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF118 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 23843 descripción PAPER CRAFT , LITTLE BIRDIE | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF119 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 23843 importe168469,60 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF120 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 23843 una línea | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF121 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 23843 80995 unidades | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF122 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 23843 contribuye al máximo de cantidad e importe | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF123 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Ranking no mide margen ni rentabilidad | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF124 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Positivos sin cliente132220 líneas | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF125 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Positivos sin cliente24,942% | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF126 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Mediana importe sin cliente4,96 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF127 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Mediana importe con cliente11,80 GBP | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF128 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | La diferencia por disponibilidad no demuestra tipos de cliente distintos | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF129 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Correlación de Spearman entre Quantity y UnitPrice en las ventas positivas: −0,403. | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF130 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Asociación inversa en rangos | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF131 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Asociación no causal | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF132 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Correlación no acredita regla de precios | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF133 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | CustomerID no imputado | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF134 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Description no inventada | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF135 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Ranking no depende exclusivamente del texto descriptivo | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF136 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 3958 códigos con alguna descripción literal | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF137 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | 650 códigos con varias descripciones literales | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF138 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Multidescripción literal16,42% | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF139 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Correspondencia código–descripción no unívoca | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF140 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | Ausencias de cliente impiden atribución de parte de las líneas | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF141 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | No hay evidencia suficiente para eliminar todos los duplicados | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF142 | 5/7/23/27/29/31/33/37/39/41/43/45/47/69/70/71/73/75/81/91/93 | No hay evidencia suficiente para declarar errores todos los extremos | R | STAT-002–015, ISSUE-001–007 y recálculo externo |
| AF143 | 51/55/59/63 | FIG-001 muestra importe positivo mensual | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF144 | 51/55/59/63 | FIG-001 muestra aumento hacia noviembre2011 | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF145 | 51/55/59/63 | FIG-002 muestra diez países por importe positivo | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF146 | 51/55/59/63 | UK domina la escala de FIG-002 | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF147 | 51/55/59/63 | FIG-003 muestra Quantity positiva | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF148 | 51/55/59/63 | FIG-003 muestra UnitPrice positivo | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF149 | 51/55/59/63 | FIG-003 muestra importe positivo | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF150 | 51/55/59/63 | Los tres histogramas se recortan visualmente en P99 | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF151 | 51/55/59/63 | El recorte no elimina extremos de las estadísticas | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF152 | 51/55/59/63 | FIG-004 muestra diez StockCode por importe positivo | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF153 | 51/55/59/63 | Descripción modal usada como etiqueta auxiliar | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF154 | 51/55/59/63 | Agrupar por código evita fragmentar variantes textuales del mismo código | R | Cuatro PNG inspeccionados, STAT-006/009/010/011/012/013 y evento16 |
| AF155 | 23/69/70/71/72/73/75/79/81/83/85/93 | No hay identificador externo independiente de línea | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF156 | 23/69/70/71/72/73/75/79/81/83/85/93 | No se proporcionó catálogo externo de productos | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF157 | 23/69/70/71/72/73/75/79/81/83/85/93 | No se proporcionaron reglas contables | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF158 | 23/69/70/71/72/73/75/79/81/83/85/93 | No se proporcionaron comprobantes de envío | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF159 | 23/69/70/71/72/73/75/79/81/83/85/93 | No se proporcionaron criterios de validación de precios | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF160 | 23/69/70/71/72/73/75/79/81/83/85/93 | No se proporcionaron criterios de validación de cantidades | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF161 | 23/69/70/71/72/73/75/79/81/83/85/93 | Origen legítimo o técnico de duplicados no determinado | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF162 | 23/69/70/71/72/73/75/79/81/83/85/93 | Causa de variantes de Description no determinada | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF163 | 23/69/70/71/72/73/75/79/81/83/85/93 | Validez comercial de extremos no determinada | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF164 | 23/69/70/71/72/73/75/79/81/83/85/93 | Validez de códigos especiales DOT POST M no determinada | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF165 | 23/69/70/71/72/73/75/79/81/83/85/93 | Validez de líneas no positivas no determinada | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF166 | 23/69/70/71/72/73/75/79/81/83/85/93 | Conclusiones limitadas al archivo y período observado | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF167 | 23/69/70/71/72/73/75/79/81/83/85/93 | No se infiere estacionalidad | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF168 | 23/69/70/71/72/73/75/79/81/83/85/93 | No se infiere demanda generalizable | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF169 | 23/69/70/71/72/73/75/79/81/83/85/93 | No se infieren cambios causales | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF170 | 23/69/70/71/72/73/75/79/81/83/85/93 | No se establecen resultados contables definitivos | R | Diccionario, campos disponibles, ISSUE-001–007 y operaciones registradas |
| AF171 | 7/74 | Diciembre 2010 no debe compararse como mes calendario completo por ser el mes inicial observado | S | La primera transacción es del día1. No acredita extracción truncada ni actividad omitida. La formulación potencial de informe85 se excluye como hipótesis, no como hecho. |