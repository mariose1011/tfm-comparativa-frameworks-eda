# Datasets del experimento

Esta carpeta contiene el conjunto de datos sintético utilizado en el piloto y las copias de Bike Sharing y Online Retail empleadas para comparar LangGraph, CrewAI y Microsoft Agent Framework mediante un mismo procedimiento de análisis exploratorio de datos tabulares.

## Datasets seleccionados

| Código | Dataset | Entrada experimental | Fuente |
| --- | --- | --- | --- |
| D0 | Pedidos sintéticos, solo piloto | `experiment_inputs/D0_piloto/pedidos_piloto.csv` | Generación local reproducible |
| D1 | Bike Sharing, datos horarios | `experiment_inputs/D1_bike_sharing/hour.csv` | https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset |
| D2 | Online Retail, 2010-2011 | `experiment_inputs/D2_online_retail/Online Retail.xlsx` | https://archive.ics.uci.edu/dataset/352/online+retail |

D0 se utiliza exclusivamente para validar el protocolo, las implementaciones y el procedimiento de evaluación. Sus resultados no forman parte de la comparación final. D1 y D2 se utilizan completos, sin muestreo. En D1 se emplea únicamente `hour.csv`; `day.csv` se conserva como parte del paquete original, pero no es una entrada del experimento.

## Organización

- `raw/`: archivos descargados de UCI y contenido original extraído, conservados sin modificaciones. D0 no tiene una fuente externa ni una copia en esta carpeta.
- `experiment_inputs/`: archivos de entrada y documentación facilitados a los tres frameworks.
- `reference_private/`: fichas, valores de referencia y criterios de evaluación que no se facilitaron a los agentes.
- `manifest.json`: registro de la procedencia, las licencias, las fechas y los archivos de cada dataset, con sus tamaños y hashes SHA-256.
- `validate_datasets.py`: comprueba los archivos registrados, algunas características de los datos y su correspondencia con las referencias de evaluación.

## Conservación de las entradas

Los archivos originales de `experiment_inputs/` se conservan sin modificaciones. Su tamaño y su hash SHA-256 permiten comprobar que coinciden con las entradas registradas en `manifest.json`.

La preparación realizada por los agentes se guarda en los resultados de cada ejecución y no sobrescribe estas entradas.

Si se utiliza una entrada distinta en un experimento posterior, debe conservarse por separado, documentar los cambios y actualizar los valores de referencia afectados.

## Separación durante las ejecuciones

Los agentes solo tienen autorizado el acceso a los datos y la documentación del dataset asignado y a los resultados de su propia ejecución. No tienen autorizado consultar `raw/`, `reference_private/` ni los resultados de otras ejecuciones.

Las referencias de evaluación incluyen resultados esperados, márgenes de tolerancia, decisiones de preparación admitidas, riesgos conocidos, contenidos exigidos en el informe y objetivos visuales.

## Generación de las referencias

Los archivos de referencia pueden regenerarse mediante:
- D0: `reference_private/D0_piloto/generate_pilot.mjs`. Utiliza una semilla fija y también genera la entrada sintética del piloto.
- D1: `reference_private/D1_bike_sharing/generate_reference.py`.
- D2: `reference_private/D2_online_retail/generate_reference.py`

Estos scripts deben ejecutarse fuera del entorno de los agentes, ya que contienen información utilizada para evaluar sus resultados.

## Comprobación de los archivos

Desde la raíz del proyecto, con un entorno que tenga instalados `pandas` y `openpyxl`, se ejecuta:

```powershell
python datasets\validate_datasets.py
```

Si todas las comprobaciones se superan, el script muestra `VALIDATION_OK` y un resumen. La validación necesita las carpetas `raw/`, `experiment_inputs/` y `reference_private/`.