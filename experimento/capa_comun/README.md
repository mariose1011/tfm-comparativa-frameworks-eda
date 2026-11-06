# Capa común del experimento

## Función

Este paquete reúne las funciones compartidas por LangGraph, CrewAI y Microsoft Agent Framework para preparar las ejecuciones, proporcionar las herramientas, validar los resultados, controlar los límites, calcular los costes y registrar el desarrollo del experimento.

Cada adaptador organiza las intervenciones de los roles mediante los componentes de su framework y utiliza las funciones de esta capa para realizar las operaciones comunes.

La función de cada archivo Python se explica en [RESUMEN_ARCHIVOS_PYTHON.md](RESUMEN_ARCHIVOS_PYTHON.md).

## Dependencias compartidas

Las versiones comunes están fijadas en `requirements.txt`. Los entornos de los tres frameworks incluyen este archivo para que los análisis utilicen las mismas versiones de NumPy, pandas, openpyxl, SciPy, Matplotlib y Seaborn.

## Comprobación de solo lectura

Desde la raíz del TFM puede ejecutarse:

```powershell
frameworks\langgraph\.venv\Scripts\python.exe -m experimento.capa_comun validar
```

El comando valida la configuración y los tres datasets. No crea ni modifica resultados.

## Pruebas automatizadas

La capa común dispone de 37 pruebas que comprueban la configuración, los datasets D0, D1 y D2, las herramientas, los controles de ejecución de Python, los límites, la traza, la validación de los resultados y la asignación del estado final.

Para ejecutarlas desde la raíz del proyecto con el entorno de LangGraph:
```powershell
frameworks\langgraph\.venv\Scripts\python.exe -m unittest discover -s experimento\capa_comun\tests -t . -v
```
El comando busca y ejecuta las pruebas de `experimento/capa_comun/tests` y muestra el resultado de cada una. Estas comprobaciones utilizan archivos temporales y no requieren llamadas a OpenAI.

Las mismas pruebas pueden ejecutarse con los entornos de CrewAI y Microsoft Agent Framework, sustituyendo la ruta del intérprete de Python. Esto permite comprobar que las funciones compartidas funcionan con las dependencias instaladas en cada entorno.

## Documentación relacionada

- **Interfaz común de los adaptadores:** reparto de responsabilidades entre los frameworks y la capa común.
- **Registro de las ejecuciones definitivas:** identificación de las ejecuciones incluidas, los intentos invalidados y la corrección técnica v1.0.1.
- **Documentación de evaluación:** métricas, puntuaciones y evidencias utilizadas para valorar los resultados.