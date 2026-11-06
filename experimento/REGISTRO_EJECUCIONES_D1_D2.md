# Registro de las ejecuciones definitivas de D1 y D2

**Fecha de preparación:** 31 de agosto de 2026 y 2 de septiembre de 2026
**Ejecuciones incluidas:** 18  
**Intentos invalidados:** 2

## Criterio de ordenación

Las ejecuciones se realizaron de forma secuencial. Dentro de cada dataset se organizaron en tres bloques, uno por repetición, y el orden de los frameworks cambió de forma cíclica para que cada uno ocupara una vez la primera, la segunda y la tercera posición.

Las siguientes tablas identifican las ejecuciones incluidas y su estado final. El comentario 'con corrección' señala que se utilizó la intervención adicional del Analista solicitada por el Revisor.

## D1 Bike Sharing

| Orden | Repetición | Framework | Estado | Run ID |
| ---: | ---: | --- | --- | --- |
| 1 | 1 | LangGraph | Completada | `D1_bike_sharing__langgraph__r01__20260831T172857425785Z` |
| 2 | 1 | CrewAI | Completada | `D1_bike_sharing__crewai__r01__20260831T173704649061Z` |
| 3 | 1 | Microsoft Agent Framework | Completada con corrección | `D1_bike_sharing__microsoft_agent_framework__r01__20260831T174252477482Z` |
| 4 | 2 | CrewAI | Completada con corrección | `D1_bike_sharing__crewai__r02__20260831T175303870628Z` |
| 5 | 2 | Microsoft Agent Framework | Parcial evaluable por límite | `D1_bike_sharing__microsoft_agent_framework__r02__20260831T175750234109Z` |
| 6 | 2 | LangGraph | Completada | `D1_bike_sharing__langgraph__r02__20260831T180229010000Z` |
| 7 | 3 | Microsoft Agent Framework | Completada con corrección | `D1_bike_sharing__microsoft_agent_framework__r03__20260831T213622746167Z` |
| 8 | 3 | LangGraph | Parcial evaluable por límites, con corrección | `D1_bike_sharing__langgraph__r03__20260831T214132905916Z` |
| 9 | 3 | CrewAI | Completada con corrección | `D1_bike_sharing__crewai__r03__20260831T214619590910Z` |

## D2 Online Retail

| Orden | Repetición | Framework | Estado | Run ID |
| ---: | ---: | --- | --- | --- |
| 10 | 1 | LangGraph | Completada | `D2_online_retail__langgraph__r01__20260902T170409927746Z` |
| 11 | 1 | CrewAI | Completada con corrección | `D2_online_retail__crewai__r01__20260902T171610603875Z` |
| 12 | 1 | Microsoft Agent Framework | Completada con corrección | `D2_online_retail__microsoft_agent_framework__r01__20260902T172454433424Z` |
| 13 | 2 | CrewAI | Completada | `D2_online_retail__crewai__r02__20260902T193106552358Z` |
| 14 | 2 | Microsoft Agent Framework | Completada | `D2_online_retail__microsoft_agent_framework__r02__20260902T193706356985Z` |
| 15 | 2 | LangGraph | Completada | `D2_online_retail__langgraph__r02__20260902T194427911777Z` |
| 16 | 3 | Microsoft Agent Framework | Completada | `D2_online_retail__microsoft_agent_framework__r03__20260902T200335090326Z` |
| 17 | 3 | LangGraph | Completada | `D2_online_retail__langgraph__r03__20260902T200956928988Z` |
| 18 | 3 | CrewAI | Completada con corrección | `D2_online_retail__crewai__r03__20260902T212422402094Z` |

## Ejecuciones invalidadas por causas externas

| Run ID | Motivo | Tokens | Tratamiento |
| --- | --- | ---: | --- |
| `D1_bike_sharing__langgraph__r01__20260831T172756966855Z` | Los dos intentos de conexión con OpenAI terminaron con errores. No se obtuvo una respuesta del modelo y la traza registró cero tokens. | 0 | Se conservó la traza y se repitió la combinación. La ejecución sustituta es la incluida en la primera fila de la tabla de D1. |

## Ejecuciones invalidadas por defectos técnicos

| Run ID | Motivo | Tokens | Tratamiento |
| --- | --- | ---: | --- |
| `D2_online_retail__crewai__r03__20260902T210324127427Z` | La respuesta del Planificador incumplió el formato exacto de los apartados E1 a E8. La ejecución terminó sin aplicar la reparación de formato permitida por la configuración v1.0 porque el mecanismo no estaba implementado. | 21528 | Se conservó la traza, se incorporó el mecanismo de reparación a los tres adaptadores y se repitió esta combinación. |