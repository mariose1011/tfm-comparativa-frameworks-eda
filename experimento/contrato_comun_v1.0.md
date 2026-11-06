# Contrato común del experimento v1.0

**Estado:** congelado para las ejecuciones definitivas D1 y D2  
**Aplicación prevista:** D0_piloto, D1_bike_sharing y D2_online_retail  
**Frameworks:** LangGraph, CrewAI y Microsoft Agent Framework

El contrato se divide en documentos independientes para facilitar su lectura y revisión.

## Contenido

1. [Parte 1. Alcance, entradas, objetivo y etapas obligatorias](contrato_comun_v1.0/01_alcance_entradas_y_etapas.md)  
   Secciones 1–8. Define el alcance del EDA tabular, las entradas, el objetivo común y las ocho etapas obligatorias.

2. [Parte 2. Roles, coordinación, corrección y finalización](contrato_comun_v1.0/02_roles_coordinacion_y_finalizacion.md)  
   Secciones 9–17. Define Planificador, Analista y Revisor, el flujo, la corrección opcional y los estados terminales.

3. [Parte 3. Archivos de salida y esquemas comunes](contrato_comun_v1.0/03_archivos_y_esquemas.md)  
   Secciones 18–28. Define `plan.md`, `prepared_data.csv`, `statistics.json`, `issues.json`, `figures/`, `report.md` y `trace.jsonl`.

4. [Parte 4. Herramientas y operaciones disponibles](contrato_comun_v1.0/04_herramientas.md)  
   Secciones 29–39. Define `inspect_dataset`, `execute_python`, `read_output`, `validate_outputs` y las operaciones automáticas.

5. [Parte 5. Traza común de la ejecución](contrato_comun_v1.0/05_traza.md)  
   Secciones 40–51. Define los eventos de `trace.jsonl` y su relación con las métricas P1–P14.

6. [Parte 6. Prompts comunes y formatos de respuesta](contrato_comun_v1.0/06_prompts_comunes.md)  
   Secciones 52–63. Define las instrucciones comunes y de cada rol, los formatos de respuesta, el aislamiento del contexto y los criterios de equivalencia y versionado.

7. [Parte 7. Límites cuantitativos y condiciones técnicas](contrato_comun_v1.0/07_limites_y_condiciones_tecnicas.md)  
   Secciones 64–78. Define la configuración del modelo, los máximos de tiempo, llamadas, tokens, herramientas y coste, las restricciones del entorno y su validación mediante D0.

## Artefactos de implementación

- [Configuración ejecutable congelada v1.0](configuracion/configuracion_experimento_v1.0.json)  
  Contiene los valores exactos que deberá cargar la capa común para aplicar el mismo contrato en los tres frameworks.
- [Guía de la configuración](configuracion/README.md)  
  Explica su finalidad, versionado, unidades, hash y forma prevista de uso.
- [Capa común del experimento](capa_comun/README.md)  
  Implementa las herramientas, validaciones, límites, trazabilidad, preparación y cierre compartidos por los tres frameworks.
- [Interfaz común de los adaptadores v1.0](adaptadores/INTERFAZ_COMUN_ADAPTADORES_v1.0.md)  
  Define la frontera entre la capa común y los mecanismos propios de LangGraph, CrewAI y Microsoft Agent Framework.
- [Adaptador experimental de LangGraph](../frameworks/langgraph/adaptador_experimento.py)  
  Implementa el flujo mediante nodos y transiciones de LangGraph.
- [Adaptador experimental de CrewAI](../frameworks/crewai/README_EXPERIMENTO.md)  
  Implementa el flujo mediante agentes y tareas secuenciales de CrewAI.
- [Adaptador experimental de Microsoft Agent Framework](../frameworks/microsoft_agent_framework/README_EXPERIMENTO.md)  
  Implementa el flujo mediante agentes y workflow de Microsoft Agent Framework.
- [Registro del piloto D0 y ajustes del entorno experimenta](REGISTRO_EJECUCIONES_D0.md)  
  Compara la validez técnica y las métricas P1 a P14 de las tres ejecuciones y documenta los ajustes ratificados antes de la congelación.
