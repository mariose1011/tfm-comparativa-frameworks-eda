# Comparativa de frameworks de agentes para análisis exploratorio de datos

Material del Trabajo Fin de Máster de Mario Saavedra Elías sobre la comparación de LangGraph, CrewAI y Microsoft Agent Framework en tareas de análisis exploratorio de datos tabulares.

Los tres adaptadores comparten datos, prompts, herramientas, límites y criterios de evaluación. Cada framework organiza las intervenciones del Planificador, el Analista y el Revisor.

## Contenido

| Ruta | Contenido |
| --- | --- |
| [`frameworks/`](frameworks/README.md) | Adaptadores, dependencias, instrucciones y pruebas simuladas. |
| [`experimento/capa_comun/`](experimento/capa_comun/README.md) | Herramientas, validación de resultados, trazas y controles compartidos. |
| [`experimento/contrato_comun_v1.0.md`](experimento/contrato_comun_v1.0.md) | Contrato del experimento: etapas, roles, resultados, herramientas, prompts y límites. |
| [`experimento/configuracion/`](experimento/configuracion/README.md) | Configuración experimental definitiva. |
| [`experimento/evaluacion/`](experimento/evaluacion/README.md) | Protocolo, guías, puntuaciones finales y fichas de evaluación. |
| [`datasets/`](datasets/README.md) | Entradas, archivos originales, referencias de evaluación y comprobaciones de integridad. |
| [`Revision_Bibliografica_TFM.xlsx`](Revision_Bibliografica_TFM.xlsx) | Registro de la revisión bibliográfica y de la selección de frameworks. |

El piloto utiliza D0, un conjunto sintético. La campaña definitiva comprende tres repeticiones por framework sobre D1 Bike Sharing y D2 Online Retail: dieciocho ejecuciones en total. Su identificación se recoge en el [registro de D1 y D2](experimento/REGISTRO_EJECUCIONES_D1_D2.md); el piloto se documenta en el [registro de D0](experimento/REGISTRO_EJECUCIONES_D0.md).

## Instalación

Las ejecuciones definitivas se realizaron con Python 3.12.13 y un entorno independiente para cada framework. Los entornos virtuales y las credenciales no se distribuyen.

La creación de los entornos y la instalación de las dependencias se explican en el [README de frameworks](frameworks/README.md#instalación-de-entornos).

## Comprobaciones locales

Las siguientes comprobaciones no envían peticiones al modelo ni requieren una clave de API. Sus instrucciones se encuentran en:

- [Capa común](experimento/capa_comun/README.md): validación de la configuración y las entradas experimentales, y pruebas de los componentes compartidos.
- [Datasets](datasets/README.md): comprobación de los archivos originales, las entradas y las referencias de evaluación.
- Pruebas simuladas de los adaptadores: [LangGraph](frameworks/langgraph/README_EXPERIMENTO.md), [CrewAI](frameworks/crewai/README_EXPERIMENTO.md) y [Microsoft Agent Framework](frameworks/microsoft_agent_framework/README_EXPERIMENTO.md).

## Ejecuciones con el modelo

Las ejecuciones reales requieren una clave propia en `OPENAI_API_KEY` y acceso al modelo indicado en la configuración. Consumen crédito de la API.

Las instrucciones de ejecución se encuentran en:

- [LangGraph](frameworks/langgraph/README_EXPERIMENTO.md).
- [CrewAI](frameworks/crewai/README_EXPERIMENTO.md).
- [Microsoft Agent Framework](frameworks/microsoft_agent_framework/README_EXPERIMENTO.md).

Cada nueva ejecución guarda sus resultados en una carpeta propia dentro de `outputs/experimento/`.

## Evaluación y evidencias originales

El [Excel de evaluación](experimento/evaluacion/Evaluacion_calidad.xlsx) recoge las puntuaciones y justificaciones. Las [fichas](experimento/evaluacion/fichas/) contienen el desglose por métrica y los archivos JSON de comprobaciones.

Los resultados y las trazas originales de las dieciocho ejecuciones definitivas se incluyen en [`outputs/experimento/`](outputs/experimento/). Las fichas de evaluación enlazan a la carpeta correspondiente a cada ejecución.

## Datos y atribución

- **D0:** datos sintéticos generados para el piloto; se incluye su generador.
- **D1:** Fanaee-T, H. (2013). *Bike Sharing*. UCI Machine Learning Repository. [DOI: 10.24432/C5W894](https://doi.org/10.24432/C5W894).
- **D2:** Chen, D. (2015). *Online Retail*. UCI Machine Learning Repository. [DOI: 10.24432/C5BW33](https://doi.org/10.24432/C5BW33).

Los datasets D1 y D2 se distribuyen con licencia [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). Su procedencia, licencia y los hashes de los archivos están registrados en [`datasets/manifest.json`](datasets/manifest.json). Esta licencia corresponde a esos datasets, no al conjunto del código del repositorio.

La carpeta `datasets/reference_private/` contiene los valores y criterios de referencia que no se facilitaron a los agentes durante el experimento. Se incluye para permitir la revisión de la evaluación.