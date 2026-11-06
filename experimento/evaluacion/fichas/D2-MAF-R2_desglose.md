# Evaluación D2-MAF-R2

**Índice final:** 83,90/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D2_online_retail__microsoft_agent_framework__r02__20260902T193706356985Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D2](../02_ficha_D2_online_retail.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D2_online_retail__microsoft_agent_framework__r02__20260902T193706356985Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D2-MAF-R2_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 91,49 |
| Q3 Validez del tratamiento de los datos | 91,67 |
| Q4 Detección de problemas y riesgos | 85,11 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 45,00 |
| Q8 Cobertura del informe | 93,18 |
| Q9 Fidelidad del informe | 99,33 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

Las ocho etapas tienen evidencia válida:

| Etapa | Nota | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001/002/004, perfil, plan y documentación pública |
| E2 Estructura, tipos y calidad | 1 | STAT-002/003/005/006 |
| E3 Preparación y decisiones de análisis | 1 | CSV, TR-001 a TR-004 y STAT-007 |
| E4 Estadística descriptiva | 1 | STAT-005/008/009/010 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-011/012/013/014/015 |
| E6 Visualizaciones | 1 | Tres PNG válidos e integrados |
| E7 Problemas, riesgos y anomalías | 1 | Seis comprobaciones, siete incidencias y STAT-016/017 |
| E8 Informe final | 1 | Alcance, preparación, resultados y límites integrados |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 91,49

Se cumplen 28 de las 32 comprobaciones previstas, que suman 43 de los 47 puntos:

| Controles | Resultado | Evidencia o motivo |
| --- | --- | --- |
| C01–C07 | Correctos | Estructura, fechas y ausencias. STAT-001/002/004 |
| C08 | Ausente | No presenta cuántos registros tienen ausentes simultáneamente CustomerID y Description |
| C09 | Correcto | 5268 duplicados después del primero. STAT-003 |
| C10 | Correcto | Los 541.909 registros originales menos los 5.268 duplicados dan 536.641 registros. STAT-001 y STAT-003 |
| C11–C27 | Correctos | Entidades, signos, precios, suma de Quantity, extremos, neto, positivos y C. STAT-005/008/009/010 |
| C28 | Ausente | No presenta el importe neto después de excluir los duplicados exactos |
| C29 | Ausente | Presenta los recuentos del Reino Unido y del conjunto completo, pero no su porcentaje |
| C30 | Correcto | La serie mensual de ventas positivas identifica noviembre de 2011 como máximo, con 1.509.496,33 GBP. STAT-011 y FIG-001 |
| C31 | Correcto | 647 códigos con varias descripciones recortadas. STAT-006 y equivalencia externa |
| C32 | Ausente | El código construye una tabla de registros por factura, pero no la guarda ni calcula y comunica su mediana |

`Q2 = 100 x 43 / 47 = 91,49`

## Q3 Validez del tratamiento de los datos: 91,67

| Decisión | Nota | Justificación y evidencia |
| --- | ---: | --- |
| D01 Identificadores | 1 | Identificadores guardados como texto, conservando sus valores y los datos ausentes. TR-001 |
| D02 Fecha-hora | 1 | El CSV conserva la fecha y la hora de todos los registros. TR-002 |
| D03 Importe | 1 | Identidad correcta y agregados definidos. STAT-005/008/009/011 |
| D04 Unidades | 1 | Distingue líneas, facturas, clientes y pares de conceptos. STAT-010/013/014 |
| D05 Cancelaciones | 1 | Conserva e identifica las cancelaciones y cuantifica sus registros e importes. STAT-004/009 |
| D06 Cliente ausente | 1 | Conserva las filas en los análisis generales y limita los análisis de clientes a los registros con identificador disponible. STAT-014/017 |
| D07 Descripción ausente | 1 | Conserva ausencias sin inventar ni reconstruir etiquetas |
| D08 Duplicados | 0 | Conserva los duplicados, pero no compara los resultados con y sin esas filas. ISSUE-003 |
| D09 Ajustes | 1 | Identifica por separado las cantidades negativas sin marca de cancelación, los precios cero y los precios negativos. STAT-005/009 |
| D10 Extremos | 1 | Conserva valores, aporta cuantiles y representación logarítmica. STAT-008/016, FIG-003 |
| D11 Mes final | 1 | Diciembre 2011 marcado como parcial. STAT-004, ISSUE-006 |
| D12 Categorías | 1 | Top limitado y detalle original conservado. STAT-012, FIG-002 |

`Q3 = 100 x 11 / 12 = 91,67`

## Q4 Detección de problemas y riesgos: 85,11

Se detectan por completo ocho de los diez riesgos de referencia (K = 8), se identifican dos riesgos adicionales válidos (A = 2) y se registra una afirmación sin respaldo suficiente (F = 1). Diez de los once hallazgos son válidos, lo que da una precisión del 90,91 %, mientras que la cobertura de los riesgos de referencia es del 80 %. Ambas medidas se combinan mediante F1 para obtener la puntuación de Q4.

| Riesgo | Resultado | Evidencia |
| --- | --- | --- |
| R01 Ausencias | Detectado | STAT-002/017, ISSUE-001/002 |
| R02 Duplicados | Detectado | STAT-003, ISSUE-003 |
| R03 Cancelaciones y signos | Detectado | STAT-004/005/009 e informe42 |
| R04 Negativos sin C | Detectado | 1336 casos en STAT-005/009 e informe75 |
| R05 Precios cero y negativos | Detectado | STAT-005 e informe75 |
| R06 Unidad e identificadores | Detectado | Perfil, TR-001, STAT-010 e informe3/17 |
| R07 Mes final parcial | Detectado | STAT-004, ISSUE-006 e informe5/76 |
| R08 Concentración UK | Parcial | El informe describe la concentración del importe en el Reino Unido, pero no interpreta específicamente su concentración sobre los registros originales. STAT-012 y líneas 50/64/91 del informe |
| R09 Asimetría y extremos | Detectado | STAT-005/008/016, ISSUE-007 |
| R10 Definiciones monetarias | Parcial | Neto, positivos y C presentes, sin efecto deduplicado |
| A01 Varias descripciones para un mismo código | Adicional válido | STAT-006, ISSUE-005 y líneas 34/73/87 del informe |
| A02 Conceptos facturados que no son productos físicos | Adicional válido | La línea 52 distingue artículos y conceptos facturados y menciona DOTCOM POSTAGE. STAT-013 |
| F01 Diciembre 2010 incompleto | Sin respaldo | STAT-004, ISSUE-006 e informe48/60/76/95 |

`Q4 = 100 x [2 x (10 / 11) x (8 / 10)] / [(10 / 11) + (8 / 10)] = 85,11`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina distribuciones generales y de ventas positivas, tipos de operación, evolución temporal, países, artículos, clientes, asociaciones, valores extremos y ausencias por país. Recibe 3 de 4 puntos porque no cuantifica el efecto de excluir duplicados.

Evidencia: STAT-005/008/009/011/012/013/014/015/016/017.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

El informe relaciona los valores extremos con las clasificaciones, las ausencias con las limitaciones del análisis de clientes y las unidades analizadas con los agregados. Recibe 3 de 4 puntos porque afirma sin respaldo suficiente que diciembre de 2010 está incompleto y no interpreta cómo cambiarían los resultados al excluir duplicados.

Evidencia: informe líneas 30/42/44/48/50/52/54/68/83/85.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 45,00

Las puntuaciones 4, 0, 3, 2 y 0 suman 9/20, equivalentes a 45,00.

| Objetivo | Nota 0–4 | Justificación |
| --- | ---: | --- |
| V01 Evolución | 4 | FIG-001 neto y positivo por mes, ejes y unidades claros, con definición y advertencia sobre el mes final |
| V02 Cancelaciones/ajustes | 0 | No hay gráficos específicos sobre cancelaciones, cantidades negativas sin esa marca o precios cero y negativos |
| V03 Distribuciones | 3 | FIG-003 muestra la distribución positiva completa en escala logarítmica, pero no representa valores cero o negativos |
| V04 Países | 2 | FIG-002 representa correctamente los importes, pero el valor del Reino Unido dificulta comparar los demás países |
| V05 Productos/conceptos/clientes | 0 | Las estadísticas contienen clasificaciones de productos y clientes, pero ninguna figura representa su concentración |

`Q7 = 100 x 9 / 20 = 45,00`

## Q8 Cobertura del informe: 93,18

| Unidad | Peso | Nota | Evidencia o motivo |
| --- | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | Informe3/5/21 |
| U02 Ausencias e impacto | 2 | 1 | Informe9/30/72/73/81 |
| U03 Unidades | 2 | 1 | Informe3/15/17/44/52 |
| U04 Duplicados y decisión | 2 | 1 | Informe32/74 |
| U05 C y negativos | 2 | 1 | Informe5/42/75 |
| U06 Ajustes | 2 | 1 | Informe75 comunica negativos sin C, precios cero y dos negativos |
| U07 Agregados monetarios | 2 | 0,5 | Comunica importes netos, positivos y de cancelaciones, pero no el efecto de excluir duplicados |
| U08 Evolución y mes final | 2 | 1 | Describe la evolución y la cobertura incompleta de diciembre de 2011. FIG-001 muestra noviembre como máximo de ventas positivas, aunque el texto destaca el máximo neto |
| U09 Concentración UK | 2 | 1 | Informe50/64 distingue composición observada de explicación causal, sin atribuir rendimiento ajustado |
| U10 Cardinalidad y conceptos | 1 | 1 | Informe15/34/52/87 distingue artículos de conceptos y muestra DOTCOM POSTAGE |
| U11 Asimetría y extremos | 2 | 1 | Informe38/44/52/68 |
| U12 Cobertura y límites | 1 | 0,5 | Explica las ausencias y la incertidumbre sobre ajustes y duplicados, pero no indica que los datos proceden de una sola empresa |

`Q8 = 100 x 20,5 / 22 = 93,18`

## Q9 Fidelidad del informe: 99,33

Se respaldan 149 de las 150 afirmaciones evaluadas. AF150 carece de respaldo suficiente porque el informe presenta diciembre de 2010 como incompleto sin evidencia que permita demostrarlo.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 149 / 150 = 99,33`

## Q10 Claridad y coherencia: 75,00

El informe presenta una estructura organizada, explica qué registros incluye en cada análisis y aporta referencias que permiten localizar las evidencias. Recibe 3 de 4 puntos porque desarrolla poco el significado de algunas variables y afirma sin respaldo suficiente que diciembre de 2010 está incompleto.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada. S = sin respaldo suficiente.

| ID | Líneas del informe | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3/5/13/15/17/21/91 | Libro XLSX con hoja Online Retail | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF002 | 3/5/13/15/17/21/91 | 541909 líneas originales | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF003 | 3/5/13/15/17/21/91 | Ocho variables fuente | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF004 | 3/5/13/15/17/21/91 | Lista de ocho campos fuente correcta | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF005 | 3/5/13/15/17/21/91 | Una fila es una línea de factura | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF006 | 3/5/13/15/17/21/91 | Conteos de líneas, facturas y clientes no son intercambiables | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF007 | 3/5/13/15/17/21/91 | La factura puede contener varias líneas | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF008 | 3/5/13/15/17/21/91 | Primera fecha-hora 2010-12-01T08:26:00 | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF009 | 3/5/13/15/17/21/91 | Última fecha-hora 2011-12-09T12:50:00 | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF010 | 3/5/13/15/17/21/91 | C indica cancelación según documentación | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF011 | 3/5/13/15/17/21/91 | 9288 líneas C | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF012 | 3/5/13/15/17/21/91 | C representa1,71% de líneas | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF013 | 3/5/13/15/17/21/91 | 25900 facturas distintas | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF014 | 3/5/13/15/17/21/91 | 4070 StockCode distintos | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF015 | 3/5/13/15/17/21/91 | 4372 clientes identificados distintos | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF016 | 3/5/13/15/17/21/91 | 38 países | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF017 | 3/5/13/15/17/21/91 | Identificadores nominales, no medidas continuas | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF018 | 3/5/13/15/17/21/91 | Análisis por cliente restringido a identificadores disponibles | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF019 | 3/5/13/15/17/21/91 | EDA descriptivo limitado al archivo | R | STAT-001/002/004/007/010, diccionario y evento16 |
| AF020 | 3/21/25/26/27/28/34/87/97 | Se conservaron 541909 filas | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF021 | 3/21/25/26/27/28/34/87/97 | Once columnas preparadas | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF022 | 3/21/25/26/27/28/34/87/97 | Tres derivadas añadidas | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF023 | 3/21/25/26/27/28/34/87/97 | Derivadas is_cancelled, line_amount e invoice_month | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF024 | 3/21/25/26/27/28/34/87/97 | InvoiceNo serializado como identificador nominal | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF025 | 3/21/25/26/27/28/34/87/97 | StockCode serializado como identificador nominal | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF026 | 3/21/25/26/27/28/34/87/97 | CustomerID serializado nominal nullable sin sufijo decimal | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF027 | 3/21/25/26/27/28/34/87/97 | CustomerID conserva ausencias | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF028 | 3/21/25/26/27/28/34/87/97 | InvoiceDate confirmado como fecha-hora | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF029 | 3/21/25/26/27/28/34/87/97 | Quantity confirmada numérica | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF030 | 3/21/25/26/27/28/34/87/97 | UnitPrice confirmado numérico | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF031 | 3/21/25/26/27/28/34/87/97 | is_cancelled usa prefijo C | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF032 | 3/21/25/26/27/28/34/87/97 | line_amount es Quantity por UnitPrice | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF033 | 3/21/25/26/27/28/34/87/97 | invoice_month procede de InvoiceDate | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF034 | 3/21/25/26/27/28/34/87/97 | No hubo imputación | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF035 | 3/21/25/26/27/28/34/87/97 | No se eliminaron filas idénticas | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF036 | 3/21/25/26/27/28/34/87/97 | No se eliminaron cantidades negativas | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF037 | 3/21/25/26/27/28/34/87/97 | No se eliminaron precios cero | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF038 | 3/21/25/26/27/28/34/87/97 | No se eliminaron extremos | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF039 | 3/21/25/26/27/28/34/87/97 | No se forzó correspondencia StockCode–Description | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF040 | 3/21/25/26/27/28/34/87/97 | Se conservaron textos de Description | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF041 | 3/21/25/26/27/28/34/87/97 | Se especifica qué registros se incluyen en cada análisis | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF042 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Neto total9747747,93 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF043 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe neto no acredita ingreso realizado | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF044 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe neto no acredita pago | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF045 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe neto no mide rentabilidad | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF046 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 135080 CustomerID ausentes | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF047 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | CustomerID ausente24,93% | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF048 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 1454 Description ausentes | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF049 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Description ausente0,27% | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF050 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Las demás columnas fuente no tienen ausencias | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF051 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 133600 ausencias CustomerID en UK | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF052 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | UK concentra98,90% de ausencias CustomerID | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF053 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 5268 duplicados exactos después del primero | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF054 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Duplicados0,97% | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF055 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | No existe identificador independiente de línea | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF056 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Origen técnico o legítimo de repetidos no resuelto | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF057 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 647 códigos con varias descripciones recortadas | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF058 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Mediana Quantity3 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF059 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Quantity mínima-80995 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF060 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Quantity máxima80995 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF061 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | P99 Quantity100 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF062 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Mediana UnitPrice2,08 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF063 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Precio mínimo-11062,06 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF064 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Precio máximo38970 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF065 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Mediana importe total9,75 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF066 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | P99 importe total180 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF067 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe mínimo-168469,60 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF068 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe máximo168469,60 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF069 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Quantity asimétrica y extrema | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF070 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | UnitPrice asimétrico y extremo | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF071 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe asimétrico y extremo | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF072 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Población positiva excluye C | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF073 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Población positiva exige Quantity>0 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF074 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Población positiva exige UnitPrice>0 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF075 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 530104 líneas positivas | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF076 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Mediana importe positivo9,90 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF077 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | P99 importe positivo183,60 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF078 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Total positivo10666684,54 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF079 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 3836 facturas C | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF080 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Unidades C -277574 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF081 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe C -896812,49 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF082 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Unidades sin C5454024 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF083 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe sin C10644560,42 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF084 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 1336 Quantity negativas sin C | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF085 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 2515 precios cero sin C | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF086 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Separar C no elimina todas las particularidades de signo y precio | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF087 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 406829 líneas identificadas | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF088 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 75,07% de líneas identificadas | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF089 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Mediana importe por cliente648,08 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF090 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Media importe por cliente1898,46 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF091 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Máximo importe por cliente279489,02 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF092 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Asimetría y concentración del importe agregado por cliente | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF093 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Neto septiembre2011 de 1019687,62 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF094 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Neto octubre2011 de 1070704,67 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF095 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Neto noviembre2011 de 1461756,25 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF096 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Aumento neto septiembre–noviembre2011 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF097 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Neto UK8187806,36 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF098 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | UK84,00% del importe neto total | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF099 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Netherlands neto284661,54 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF100 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | EIRE neto263276,82 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF101 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Germany neto221698,21 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF102 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | France neto197403,90 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF103 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | La concentración geográfica describe composición, no causas | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF104 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Ranking positivo incluye artículos y conceptos facturados | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF105 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Par DOT DOTCOM POSTAGE primero por importe positivo | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF106 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe positivo de ese par206248,77 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF107 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Par22423 REGENCY CAKESTAND 3 TIER segundo | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF108 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe positivo de ese par174484,74 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF109 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Par23843 PAPER CRAFT , LITTLE BIRDIE tercero | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF110 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Importe positivo de ese par168469,60 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF111 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Ese par23843 tiene una sola línea | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF112 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Esa línea tiene80995 unidades | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF113 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Rankings y medias sensibles a pedidos grandes | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF114 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Correlación de Spearman entre Quantity y UnitPrice en las ventas positivas: −0,403 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF115 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Spearman sobre530104 líneas | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF116 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Es asociación de rangos, no causalidad ni elasticidad | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF117 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 5279 importes positivos por encima de p99 | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF118 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Máximo positivo168469,60 GBP | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF119 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 10624 cantidades negativas | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF120 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | 2515 precios cero | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF121 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Dos precios negativos | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF122 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Noviembre2011 máximo neto entre meses completos | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF123 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Las cancelaciones son minoritarias en líneas | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF124 | 7/9/15/30/32/34/38/40/42/44/48/50/52/54/64/68/75/77/91/93/95 | Las cancelaciones tienen importe agregado negativo | R | STAT-002/003/005/006/008/009/010/011/012/013/014/015/016/017 |
| AF125 | 58/60/62/64/66/68 | FIG-001 distingue neto y positivo | R | Tres PNG abiertos, STAT-011/012/016 y evento16 |
| AF126 | 58/60/62/64/66/68 | La serie neta incluye cancelaciones y ajustes | R | Tres PNG abiertos, STAT-011/012/016 y evento16 |
| AF127 | 58/60/62/64/66/68 | FIG-002 muestra diez países por importe neto | R | Tres PNG abiertos, STAT-011/012/016 y evento16 |
| AF128 | 58/60/62/64/66/68 | UK domina la escala visual | R | Tres PNG abiertos, STAT-011/012/016 y evento16 |
| AF129 | 58/60/62/64/66/68 | FIG-003 usa log10 de importes positivos | R | Tres PNG abiertos, STAT-011/012/016 y evento16 |
| AF130 | 58/60/62/64/66/68 | La transformación visual evita que la cola domine la escala lineal | R | Tres PNG abiertos, STAT-011/012/016 y evento16 |
| AF131 | 58/60/62/64/66/68 | Se conservan los extremos sin recorte | R | Tres PNG abiertos, STAT-011/012/016 y evento16 |
| AF132 | 58/60/62/64/66/68 | Las figuras son descriptivas, no pruebas causales | R | Tres PNG abiertos, STAT-011/012/016 y evento16 |
| AF133 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | No se conoce el mecanismo de ausencia CustomerID | R | Campos fuente, preparación, estadísticas e incidencias |
| AF134 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | Ausencias limitan análisis por cliente | R | Campos fuente, preparación, estadísticas e incidencias |
| AF135 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | No se reconstruyó Description desde StockCode | R | Campos fuente, preparación, estadísticas e incidencias |
| AF136 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | No hay catálogo fiable que determine la variante correcta | R | Campos fuente, preparación, estadísticas e incidencias |
| AF137 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | La documentación no permite clasificar con certeza todos los precios cero | R | Campos fuente, preparación, estadísticas e incidencias |
| AF138 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | La documentación no permite clasificar todos los negativos sin C | R | Campos fuente, preparación, estadísticas e incidencias |
| AF139 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | La documentación no clasifica todos los conceptos especiales ni extremos | R | Campos fuente, preparación, estadísticas e incidencias |
| AF140 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | No hay información sobre pagos | R | Campos fuente, preparación, estadísticas e incidencias |
| AF141 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | No hay campos de costes | R | Campos fuente, preparación, estadísticas e incidencias |
| AF142 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | No hay margen documentado | R | Campos fuente, preparación, estadísticas e incidencias |
| AF143 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | No hay descuentos no registrados observables | R | Campos fuente, preparación, estadísticas e incidencias |
| AF144 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | No hay devoluciones emparejadas explícitamente | R | Campos fuente, preparación, estadísticas e incidencias |
| AF145 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | No hay estado final de transacción | R | Campos fuente, preparación, estadísticas e incidencias |
| AF146 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | Importe calculado no equivale necesariamente a ventas realizadas o ingreso contable | R | Campos fuente, preparación, estadísticas e incidencias |
| AF147 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | No se confirmaron errores en extremos o repetidos | R | Campos fuente, preparación, estadísticas e incidencias |
| AF148 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | Diciembre 2011 solo alcanza el día9 | R | Campos fuente, preparación, estadísticas e incidencias |
| AF149 | 5/72/73/74/75/76/77/81/83/85/87/93/97 | Diciembre 2011 es parcial frente a un mes calendario completo | R | Campos fuente, preparación, estadísticas e incidencias |
| AF150 | 48/60/76/95 | Diciembre 2010 no es un mes completo por ser el primer mes y empezar el día1 | S | La primera transacción del día1 no acredita truncamiento mensual. La documentación y STAT-004/011 no prueban actividad mensual anterior omitida. ISSUE-006 repite el diagnóstico sin demostrarlo. |