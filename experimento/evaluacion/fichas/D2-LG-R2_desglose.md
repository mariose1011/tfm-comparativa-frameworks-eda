# Evaluación D2-LG-R2

**Índice final:** 84,41/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D2_online_retail__langgraph__r02__20260902T194427911777Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D2](../02_ficha_D2_online_retail.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D2_online_retail__langgraph__r02__20260902T194427911777Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D2-LG-R2_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 82,98 |
| Q3 Validez del tratamiento de los datos | 91,67 |
| Q4 Detección de problemas y riesgos | 85,11 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 65,00 |
| Q8 Cobertura del informe | 90,91 |
| Q9 Fidelidad del informe | 99,48 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

Las ocho etapas tienen evidencia válida:

| Etapa | Nota | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001, perfil, documentación pública y evento7 |
| E2 Estructura, tipos y calidad | 1 | STAT-002/003/004/005 |
| E3 Preparación y decisiones de análisis | 1 | CSV, TR-001–004 y STAT-006 |
| E4 Estadística descriptiva | 1 | STAT-004/007/008 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-009/010/011/012/013 |
| E6 Visualizaciones | 1 | Cuatro PNG válidos e integrados |
| E7 Problemas, riesgos y anomalías | 1 | Seis comprobaciones, siete incidencias y STAT-014 |
| E8 Informe final | 1 | Alcance, preparación, resultados y límites integrados |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 82,98

Se cumplen 26 de las 32 comprobaciones previstas, que suman 39 de los 47 puntos ponderados. Las seis restantes no cuentan con el resultado requerido.

| Controles | Resultado | Evidencia o motivo |
| --- | --- | --- |
| C01–C07 | Correctos | Estructura, fechas y ausencias. STAT-001/002/005 |
| C08 | Ausente | No presenta cuántos registros tienen ausentes simultáneamente CustomerID y Description |
| C09 | Correcto | 5268 duplicados después del primero. STAT-003 |
| C10 | Correcto | Los 541.909 registros originales menos los 5.268 duplicados dan 536.641 registros. Las cifras proceden de STAT-001 y STAT-003; la ejecución no elimina esas filas |
| C11–C20 | Correctos | Entidades, cancelaciones, signos y precios. STAT-004/007 |
| C21 | Correcto | Las cantidades mensuales de STAT-009 suman 5.176.450 unidades y abarcan los trece meses del conjunto de datos |
| C22–C26 | Correctos | Extremos, importe neto y población positiva. STAT-004/007/008/009 |
| C27 | Ausente | No presenta el importe total de los registros identificados como cancelaciones |
| C28 | Ausente | No presenta el importe neto que resulta de excluir los duplicados exactos |
| C29 | Ausente | Los 485.123 registros del Reino Unido corresponden al grupo de ventas positivas y el 84,61 % representa su participación en el importe de ese grupo. No presenta su porcentaje sobre todos los registros originales |
| C30 | Ausente | La serie mensual de STAT-009 corresponde al importe neto, no al de las ventas positivas. El campo gross_line_amount contiene los mismos valores que el neto |
| C31 | Correcto | 	Identifica 647 códigos asociados a varias descripciones después de eliminar los espacios iniciales y finales. STAT-013 y comprobación de equivalencia |
| C32 | Ausente | Presenta el número de facturas por cliente, pero no el número de registros por factura |

`Q2 = 100 x 39 / 47 = 82,98`

## Q3 Validez del tratamiento de los datos: 91,67

| Decisión | Nota | Justificación y evidencia |
| --- | ---: | --- |
| D01 Identificadores | 1 | Identificadores como texto, con sus valores y ausencias conservados. TR-001 |
| D02 Fecha-hora | 1 | CSV conserva fecha y hora en todas las filas. TR-002 |
| D03 Importe | 1 | Identidad correcta, filtros y agregados definidos. STAT-006/008/009 |
| D04 Unidades | 1 | Distingue líneas, facturas, clientes y pares de artículos. STAT-007/011/012 |
| D05 Cancelaciones | 1 | C conservado, identificado y cuantificado. STAT-004/007 |
| D06 Cliente ausente | 1 | Retiene filas globales y restringe clientes a identificadores presentes. STAT-007/012 |
| D07 Descripción ausente | 1 | Conserva ausencias sin inventar etiquetas |
| D08 Duplicados | 0 | Conserva los duplicados, pero no compara los resultados con y sin esas filas. ISSUE-003 |
| D09 Ajustes | 1 | Separa negativos sin C, precios cero y negativos. STAT-004 |
| D10 Extremos | 1 | Conserva valores, cuantiles, cribado IQR y escala logarítmica. STAT-008/014, FIG-003 |
| D11 Mes final | 1 | Diciembre2011 marcado como parcial. STAT-005, ISSUE-005 |
| D12 Categorías | 1 | Limita los gráficos a las categorías principales y conserva el detalle original. STAT-010/011 y FIG-002/004 |

`Q3 = 100 x 11 / 12 = 91,67`

## Q4 Detección de problemas y riesgos: 85,11


| Riesgo | Resultado | Evidencia |
| --- | --- | --- |
| R01 Ausencias | Detectado | STAT-002, ISSUE-001/002 |
| R02 Duplicados | Detectado | STAT-003, ISSUE-003 |
| R03 C y signos | Detectado | STAT-004/007 e informe37/39 |
| R04 Negativos sin C | Detectado | 1336 casos, STAT-004 e informe39/100 |
| R05 Precios cero y negativos | Detectado | STAT-004 e informe39/100 |
| R06 Unidad e identificadores | Detectado | Perfil, TR-001 e informe3/15/23 |
| R07 Mes final parcial | Detectado | STAT-005, ISSUE-005 e informe60 |
| R08 Concentración en líneas originales | Parcial | Predominio monetario positivo, sin cuota de líneas originales |
| R09 Asimetría y extremos | Detectado | STAT-004/008/014, ISSUE-007 |
| R10 Definiciones monetarias | Parcial | Neto y positivos definidos, sin importe C ni efecto deduplicado |
| A01 Varias descripciones para un mismo código | Adicional válido | STAT-013, ISSUE-006 y líneas 72/104 del informe |
| A02 Códigos de gastos de envío y operaciones manuales | Adicional válido | Las líneas 66/90 del informe distinguen estos conceptos de los productos mediante los códigos DOT, POST y M |
| F01 Diciembre2010 incompleto | Sin respaldo | Inferencia en informe60/102/116 e ISSUE-005 |

Se detectan por completo ocho de los diez riesgos de referencia (K = 8), se identifican dos riesgos adicionales válidos (A = 2) y se registra una afirmación sin respaldo suficiente (F = 1). Por tanto, diez de los once hallazgos son válidos, lo que da una precisión del 90,91 %, mientras que la cobertura de los riesgos de referencia es del 80 %. Ambas medidas se combinan mediante F1 para obtener la puntuación de Q4.

`Q4 = 100 x [2 x (10 / 11) x (8 / 10)] / [(10 / 11) + (8 / 10)] = 85,11`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina distribuciones, evolución temporal, países, productos, clientes, asociaciones y valores extremos. Recibe 3 de 4 puntos porque no cuantifica cómo cambian los resultados al excluir duplicados ni compara específicamente el importe de las cancelaciones.

Evidencia: STAT-004 y STAT-008 a STAT-014.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

El informe relaciona los valores extremos con las medias y las clasificaciones, explica cómo las ausencias limitan el análisis de clientes y distingue asociación de causalidad. Recibe 3 de 4 puntos porque presenta diciembre de 2010 como incompleto sin evidencia suficiente y no interpreta cómo afectarían los duplicados a los importes.

Evidencia: líneas 54/60/64/66/68/70/94/98/106 del informe.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 65,00

| Objetivo | Nota 0–4 | Justificación |
| --- | ---: | --- |
| V01 Evolución | 4 | FIG-001 muestra neto mensual con unidades y definición claras. El informe integra la advertencia sobre diciembre2011 |
| V02 Cancelaciones/ajustes | 0 | No hay representación específica de C, negativos ni precios no positivos |
| V03 Distribuciones | 3 | FIG-003 conserva toda la distribución positiva en log10. No representa negativos o ceros |
| V04 Países | 2 | FIG-002 representa correctamente los importes, pero el valor del Reino Unido reduce la legibilidad de las diferencias entre los demás países |
| V05 Productos/conceptos/clientes | 4 | FIG-004 muestra top10 de pares identificables, métrica y unidades claras. El texto explica gastos de envío y registros manuales |

`Q7 = 100 x 13 / 20 = 65,00`

## Q8 Cobertura del informe: 90,91

| Unidad | Peso | Nota | Evidencia o motivo |
| --- | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | Informe3/21/60 |
| U02 Ausencias e impacto | 2 | 1 | Informe21/94/96/112 |
| U03 Unidades | 2 | 1 | Informe3/37/66/68 |
| U04 Duplicados y decisión | 2 | 1 | Informe33/98 |
| U05 C y negativos | 2 | 1 | Informe37/39/100 |
| U06 Ajustes | 2 | 1 | Informe39/100 separa negativos sin C, precios cero y negativos |
| U07 Agregados monetarios | 2 | 0,5 | Neto y positivos presentes, sin importe C ni efecto de deduplicar |
| U08 Evolución y máximo completo | 2 | 0,5 | Describe evolución y diciembre2011 parcial. Noviembre se identifica sobre neto, no sobre ventas positivas |
| U09 Concentración UK | 2 | 1 | Informe9/64/82 distingue composición observada de tamaño de mercado |
| U10 Cardinalidad y conceptos | 1 | 1 | Informe21/66/72/90 muestra códigos distintos y distingue portes/registros manuales |
| U11 Asimetría y extremos | 2 | 1 | Informe43–56/68/106 |
| U12 Cobertura y límites | 1 | 1 | Explica las limitaciones relacionadas con la empresa, el periodo, los datos ausentes, los ajustes y los duplicados |

`Q8 = 100 x 20 / 22 = 90,91`

## Q9 Fidelidad del informe: 99,48

Se respaldan 191 de las 192 afirmaciones evaluadas. AF192 carece de respaldo suficiente porque el informe presenta diciembre de 2010 como incompleto al no haber registros posteriores al día 23, sin evidencia de que se hayan omitido transacciones posteriores.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 191 / 192 = 99,48`

## Q10 Claridad y coherencia: 75,00

El informe presenta una estructura ordenada e identifica los filtros, las unidades, las referencias y las limitaciones. Recibe 3 de 4 puntos porque algunos campos no se explican suficientemente y se presenta diciembre de 2010 como incompleto sin justificarlo.

`Q10 = 100 x 3 / 4 = 75,00`

## Anexo · Inventario completo Q9

R = respaldada. S = sin respaldo suficiente.

| ID | Líneas | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | 541909 líneas de factura originales | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF002 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Ocho variables fuente | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF003 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | La fila no equivale a factura agregada | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF004 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | La fila no equivale necesariamente a compra completa | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF005 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | La fila no equivale a cliente | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF006 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Archivo XLSX y hoja Online Retail | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF007 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Transacciones de una empresa británica de comercio electrónico | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF008 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Periodo documentado diciembre 2010 – diciembre 2011 | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF009 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Prefijo C documentado como cancelación | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF010 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Variables InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID y Country presentes | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF011 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | InvoiceNo nominal | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF012 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | StockCode nominal | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF013 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | CustomerID nominal | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF014 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | CustomerID original float64 | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF015 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Otros identificadores originales object | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF016 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Copia preparada conserva 541909 filas | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF017 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Doce columnas preparadas | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF018 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Cuatro variables derivadas | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF019 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | InvoiceNo convertido a cadena | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF020 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | StockCode convertido a cadena | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF021 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | CustomerID entero nullable convertido a cadena | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF022 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | InvoiceDate conserva fecha y hora | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF023 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | CSV serializa fecha-hora de forma no ambigua | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF024 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Se recortaron espacios periféricos de Description | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF025 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Se recortaron espacios periféricos de Country | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF026 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | is_cancellation depende del prefijo C | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF027 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | line_amount=QuantityxUnitPrice | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF028 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Diferencia máxima de identidad en memoria0 | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF029 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | invoice_month deriva del mes | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF030 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | customer_identified marca identificadores presentes | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF031 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | No se imputó CustomerID | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF032 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | No se imputó Description | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF033 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | No se eliminaron duplicados | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF034 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | No se eliminaron cancelaciones | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF035 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | No se eliminaron extremos | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF036 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | No se eliminaron precios cero o signos negativos | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF037 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Importe de línea no es ingreso contable conciliado | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF038 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Importe de línea no mide cobros | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF039 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Importe de línea no mide margen | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF040 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Importe de línea no acredita entrega | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF041 | 3/5/13/15/17/21/23/27/28/29/30/31/33/122 | Importe de línea no mide rentabilidad | R | STAT-001/002/006/007, TR-001–004, evento16, CSV y diccionario público del evento7 |
| AF042 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Población positiva excluye C | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF043 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Población positiva exige Quantity>0 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF044 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Población positiva exige UnitPrice>0 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF045 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 530104 líneas positivas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF046 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 5588376 unidades positivas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF047 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Importe positivo10666684,54 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF048 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Mediana importe positivo9,90 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF049 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Media importe positivo20,12 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF050 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Importe positivo con cola derecha | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF051 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | UK importe positivo9025222,08 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF052 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | UK84,61% del importe positivo | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF053 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Netherlands segundo por importe positivo | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF054 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | EIRE tercero por importe positivo | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF055 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Germany cuarto por importe positivo | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF056 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | France quinto por importe positivo | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF057 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | CustomerID ausente135080 líneas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF058 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | CustomerID ausente24,93% | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF059 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Description ausente1454 líneas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF060 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Description ausente0,27% | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF061 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Sin ausencias InvoiceNo | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF062 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Sin ausencias StockCode | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF063 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Sin ausencias Quantity | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF064 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Sin ausencias InvoiceDate | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF065 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Sin ausencias UnitPrice | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF066 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Sin ausencias Country | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF067 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 4070 StockCode distintos | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF068 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 4372 clientes identificados originales | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF069 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 38 países | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF070 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 5268 duplicados después del primero | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF071 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | La igualdad de campos no determina el origen de los duplicados | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF072 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 25900 facturas distintas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF073 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 3836 facturas C | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF074 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 22064 facturas sin C | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF075 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 9288 líneas C | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF076 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Líneas C1,71% del total | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF077 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Todas las líneas C tienen Quantity negativa | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF078 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 1336 Quantity negativas sin C | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF079 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | El signo negativo no sustituye la regla C | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF080 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 2515 precios cero | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF081 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Dos precios negativos | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF082 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | No hay Quantity cero | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF083 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Mediana Quantity positiva3 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF084 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Mediana UnitPrice positivo2,08 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF085 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Media Quantity positiva10,54 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF086 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Media UnitPrice positivo3,91 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF087 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | P75 Quantity positiva10 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF088 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | P75 UnitPrice positivo4,13 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF089 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | P75 importe positivo17,70 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF090 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | P99 Quantity positiva100 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF091 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | P99 UnitPrice positivo16,98 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF092 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | P99 importe positivo183,60 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF093 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Máximo Quantity positivo80995 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF094 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Máximo UnitPrice positivo13541,33 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF095 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Máximo importe positivo168469,60 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF096 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Media, mediana y máximos muestran asimetría | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF097 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Quantity positiva asimétrica | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF098 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | UnitPrice positivo asimétrico | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF099 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | La media no describe por sí sola la línea típica | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF100 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Quantity completa mínima-80995 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF101 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Quantity completa máxima80995 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF102 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Importe completo mínimo-168469,60 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF103 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Importe completo máximo168469,60 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF104 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Primera fecha2010-12-01T08:26:00 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF105 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Última fecha2011-12-09T12:50:00 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF106 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Sin fechas no parseables | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF107 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Última transacción diciembre2010 día 23 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF108 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Última transacción diciembre2011 día9 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF109 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Diciembre2011 parcial | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF110 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Noviembre2011 máximo importe neto | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF111 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Noviembre neto1461756,25 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF112 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Noviembre84711 líneas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF113 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Octubre2011 segundo máximo importe neto | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF114 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Octubre neto1070704,67 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF115 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Octubre60742 líneas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF116 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Neto total9747747,93 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF117 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | UK485123 líneas positivas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF118 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | UK18019 facturas positivas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF119 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | UK4662390 unidades positivas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF120 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Netherlands285446,34 GBP positivos | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF121 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | EIRE283453,96 GBP positivos | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF122 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Germany228867,14 GBP positivos | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF123 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | France209715,11 GBP positivos | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF124 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | La comparación geográfica no está ajustada por tamaño de mercado | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF125 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | La comparación geográfica no prueba causalidad | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF126 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Par DOT DOTCOM POSTAGE primero por importe positivo | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF127 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Par DOT206248,77 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF128 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Par DOT706 líneas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF129 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Par22423 REGENCY CAKESTAND 3 TIER174484,74 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF130 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Par23843 PAPER CRAFT , LITTLE BIRDIE168469,60 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF131 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Par23843 una línea | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF132 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Par23843 80995 unidades | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF133 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Rankings incluyen DOT, POST y M | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF134 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Descripciones sugieren portes o registros manuales, no mercancías homogéneas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF135 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 4338 clientes en población positiva identificable | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF136 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Mediana facturas por cliente positivo2 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF137 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Mediana importe cliente positivo674,49 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF138 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Media importe cliente positivo2054,27 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF139 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Máximo importe cliente positivo280206,02 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF140 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Importe por cliente asimétrico y concentrado | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF141 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Análisis por cliente excluye ausencias | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF142 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Correlación de Spearman entre Quantity y UnitPrice en las ventas positivas: −0,403 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF143 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Spearman Quantity–importe positivo0,676 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF144 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Spearman UnitPrice–importe positivo0,338 | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF145 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Asociaciones no prueban causalidad | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF146 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 3958 códigos con descripción presente | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF147 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 647 códigos multidescripción recortada | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF148 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Máximo ocho descripciones por código | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF149 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Correspondencia código–descripción no unívoca | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF150 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Duplicados0,97% de líneas | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF151 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | No hay identificador independiente de línea | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF152 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Ausencias de Description limitan etiquetas sin impedir conservar StockCode | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF153 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Umbral superior IQR38,625 GBP | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF154 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | 42651 líneas positivas sobre el umbral | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF155 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | Porcentaje sobre umbral8,05% | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF156 | 7/9/21/33/37/39/45/46/47/48/49/50/54/56/60/62/64/66/68/70/72/94/96/98/100/104/106/122/124 | La regla IQR no prueba error | R | STAT-002/003/004/005/007/008/009/010/011/012/013/014 e incidencias |
| AF157 | 76/78/80/82/84/86/88/90 | FIG-001 muestra importe neto mensual de todas las líneas | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF158 | 76/78/80/82/84/86/88/90 | FIG-001 incluye cancelaciones | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF159 | 76/78/80/82/84/86/88/90 | Importe neto aumenta septiembre–noviembre2011 | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF160 | 76/78/80/82/84/86/88/90 | FIG-002 muestra diez países por importe positivo | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF161 | 76/78/80/82/84/86/88/90 | FIG-002 evidencia concentración UK | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF162 | 76/78/80/82/84/86/88/90 | UK supera cuatro quintas partes del importe positivo | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF163 | 76/78/80/82/84/86/88/90 | FIG-003 muestra log10 del importe positivo | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF164 | 76/78/80/82/84/86/88/90 | FIG-003 conserva cola superior sin recorte | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF165 | 76/78/80/82/84/86/88/90 | Las líneas de menor importe son más frecuentes que la cola alta | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF166 | 76/78/80/82/84/86/88/90 | FIG-004 muestra diez pares código–descripción por importe | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF167 | 76/78/80/82/84/86/88/90 | FIG-004 incluye DOTCOM POSTAGE | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF168 | 76/78/80/82/84/86/88/90 | FIG-004 incluye Manual | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF169 | 76/78/80/82/84/86/88/90 | No es un ranking puro de artículos físicos | R | Cuatro PNG abiertos, STAT-008/009/010/011/014 y código evento16 |
| AF170 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay fuente verificable para reconstruir CustomerID | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF171 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay fuente verificable para reconstruir Description | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF172 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | Mecanismo de ausencia CustomerID desconocido | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF173 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | Ausencia CustomerID limita representatividad del análisis por cliente | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF174 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No se extrapolaron importes por días | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF175 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No se ajustaron importes por días de actividad | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF176 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | Campos disponibles no resuelven catálogo código–descripción | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF177 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay evidencia para clasificar todos los extremos como errores | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF178 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay campos de pagos | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF179 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay campos de devoluciones efectivas emparejadas | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF180 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay notas de crédito conciliadas | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF181 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay costes | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF182 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay margen | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF183 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay inventario | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF184 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay estado de entrega | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF185 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No hay campañas | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF186 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | Documentación no clasifica concluyentemente negativos sin C | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF187 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | Documentación no clasifica concluyentemente precios cero | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF188 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | Documentación no clasifica concluyentemente precios negativos | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF189 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | No se determinó origen técnico o legítimo de duplicados | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF190 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | Las correlaciones son descriptivas | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF191 | 33/94/98/100/102/104/106/110/112/114/116/118/126 | Los agregados son descriptivos | R | Diccionario público, campos fuente, código e ISSUE-001–007 |
| AF192 | 60/78/102/116/126 | Diciembre2010 es parcial y no comparable a meses completos porque su última transacción es del día 23 | S | STAT-005 acredita la última transacción, no truncamiento de la extracción ni actividad posterior omitida. ISSUE-005 reconoce que se desconoce si coincide con el fin real de actividad. |
