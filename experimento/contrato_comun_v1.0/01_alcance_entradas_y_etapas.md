# Parte 1. Alcance, entradas, objetivo y etapas obligatorias

**Contrato:** v1.0

[← Índice](../contrato_comun_v1.0.md) · [Parte 2 →](02_roles_coordinacion_y_finalizacion.md)

## 1. Finalidad del contrato

Este documento define el alcance funcional común bajo el que se implementarán y evaluarán los tres frameworks. Su finalidad es evitar que las diferencias observadas se deban a que cada implementación haya recibido una tarea, información o criterio de finalización diferente.

El contrato será el mismo en el piloto y en el experimento definitivo. D0 se utilizará para comprobar y ajustar su viabilidad técnica. D1 y D2 se utilizarán para obtener los resultados finales.

La equivalencia exigida es semántica, no una reproducción idéntica del código interno. Cada framework podrá representar agentes, estados, mensajes y transiciones mediante sus mecanismos propios, pero deberá respetar el mismo alcance, entradas, etapas, restricciones y resultados requeridos.

## 2. Alcance del trabajo

El sistema realizará un análisis exploratorio de datos tabulares orientado a:

- Comprender la estructura y el significado del dataset.
- Examinar su calidad y detectar situaciones que puedan afectar al análisis.
- Preparar una copia de trabajo sin modificar el archivo de entrada.
- Obtener estadísticas descriptivas, agregaciones y relaciones relevantes.
- Generar visualizaciones adecuadas para los principales hallazgos.
- Interpretar los resultados con prudencia y trazabilidad.
- Elaborar un informe final coherente y respaldado por evidencias generadas durante la ejecución.

El sistema deberá decidir qué análisis concretos son pertinentes a partir del contenido del dataset y de su documentación pública. No se le facilitará la relación privada de problemas conocidos, resultados esperados, tolerancias ni reglas de corrección.

### 2.1. Actividades incluidas

- Carga de archivos CSV o XLSX mediante las herramientas proporcionadas.
- Inspección de las dimensiones, los nombres de las variables, los tipos de datos y lo que representa cada fila.
- Análisis de valores ausentes, duplicados, categorías, rangos e incoherencias.
- Conversión justificada de tipos y creación de variables derivadas útiles.
- Tratamiento justificado de problemas de calidad, incluida la decisión de no modificar los datos.
- Estadística descriptiva univariante y multivariante.
- Agregaciones temporales o categóricas cuando sean pertinentes.
- Análisis descriptivo de relaciones entre variables.
- Detección y examen de posibles anomalías o valores extremos.
- Visualizaciones legibles y vinculadas con objetivos analíticos.
- Interpretación, limitaciones y redacción del informe.

### 2.2. Actividades excluidas

- Entrenamiento, selección o comparación de modelos predictivos.
- Optimización de hiperparámetros o construcción de sistemas de predicción.
- No se permite deducir relaciones causa-efecto a partir de asociaciones observacionales.
- Consulta de fuentes externas para buscar explicaciones de los resultados.
- Modificación del archivo de entrada.
- Acceso a referencias privadas, fichas de corrección o resultados de otras ejecuciones.
- Solicitud de ayuda humana durante una ejecución.
- Incorporación de información no obtenida del dataset, de su documentación pública o de las herramientas autorizadas.

## 3. Unidad de ejecución
Una ejecución corresponde a un intento de realizar las ocho etapas obligatorias del análisis exploratorio sobre un único dataset. Cada ejecución parte de un estado nuevo, sin memoria ni resultados de ejecuciones anteriores.

La combinación experimental queda identificada por:

- Framework y versión.
- Dataset y hash de la entrada.
- Número de repetición.
- Modelo, proveedor y configuración.
- Versión del contrato común.
- Versión de los prompts, herramientas y límites.
- Fecha y hora de inicio.

Cada ejecución tendrá un identificador único y una carpeta de salida independiente. No podrá leer resultados producidos por otras ejecuciones.

## 4. Entradas comunes

Cada ejecución recibirá únicamente las siguientes entradas funcionales:

| Entrada | Contenido | Regla común |
| --- | --- | --- |
| Archivo del dataset | Un único archivo CSV o XLSX congelado. | Debe coincidir con el hash registrado en el manifiesto. Solo lectura. |
| Documentación pública | Diccionario de variables, procedencia y aclaraciones disponibles para el análisis. | No contendrá valores de referencia ni indicará los problemas que se espera detectar. |
| Instrucción común | Objetivo, etapas, restricciones y resultados requeridos. | La instrucción común exigirá el mismo objetivo, etapas, restricciones y resultados en los tres frameworks. |
| Identificador de ejecución | Código único formado a partir de framework, dataset y repetición. | Se utilizará para separar resultados y trazas. |
| Directorio de salida | Carpeta vacía y exclusiva de la ejecución. | Solo podrá escribirse dentro de esta ubicación. |
| Configuración experimental | Modelo, proveedor, límites y parámetros fijados. | Será común y no podrá modificarse durante la ejecución. |

### 4.1. Sustituciones permitidas entre datasets

El contrato se adaptará entre datasets cambiando únicamente:

- La ruta y el formato del archivo de entrada.
- La documentación pública asociada al dataset.
- El identificador de dataset y el hash esperado.
- El identificador y la carpeta de salida de la ejecución.

### 4.2. Información prohibida durante la ejecución

El entorno del agente no deberá permitir acceso a:

- `datasets/reference_private/`.
- `datasets/raw/`.
- Resultados de otros frameworks o repeticiones.
- Credenciales, archivos del proyecto o directorios ajenos a los autorizados.

## 5. Objetivo común de la ejecución

El objetivo asignado al sistema será:

> Realizar un análisis exploratorio completo, reproducible y trazable del dataset proporcionado. Examinar su estructura y calidad, preparar una copia de trabajo mediante decisiones justificadas, obtener estadísticas, relaciones y visualizaciones relevantes, detectar problemas o anomalías y elaborar un informe final respaldado por los resultados generados. No entrenar modelos predictivos ni realizar afirmaciones causales. Conservar el archivo original y documentar las transformaciones, supuestos y limitaciones.

La expresión "completo" se refiere al cumplimiento razonable de las ocho etapas definidas. El sistema conservará autonomía para elegir técnicas y tratamientos adecuados.

## 6. Ocho etapas obligatorias del EDA

Las etapas definen capacidades y evidencias requeridas. No obligan a utilizar una función estadística o un gráfico determinado. Una etapa solo se considerará realizada cuando existan resultados o registros que demuestren su ejecución.

### Etapa 1. Carga e inspección inicial

**Propósito:** verificar que el archivo puede leerse y establecer una primera comprensión de la tabla.

El sistema deberá:

- Identificar el archivo y formato de entrada.
- Cargar los datos sin modificar el original.
- Determinar dimensiones, columnas y una muestra estructural suficiente.
- Consultar la documentación pública disponible.
- Determinar qué representa cada fila del dataset. Si no puede determinarlo con seguridad a partir de los datos y la documentación disponible, deberá indicarlo expresamente y explicar qué aspectos no están claros.

**Evidencia mínima:** carga correcta, dimensiones observadas, columnas y descripción inicial de la unidad de análisis.

### Etapa 2. Estructura, tipos y calidad

**Propósito:** caracterizar la estructura y localizar problemas que condicionen los análisis posteriores.

El sistema deberá examinar los siguientes aspectos siempre que sean pertinentes y puedan evaluarse con la información disponible en el dataset y su documentación pública:

- Tipos de datos reales y esperados.
- Valores ausentes.
- Duplicados de filas o identificadores.
- Cardinalidad y consistencia de categorías.
- Rangos, signos, unidades e identidades documentadas.
- Fechas, cobertura temporal y posibles periodos incompletos.
- Valores extremos, incoherencias y otros riesgos analíticos.

**Evidencia mínima:** resumen cuantificado de calidad y relación trazable de los problemas o riesgos detectados.

### Etapa 3. Preparación y decisiones de análisis

**Propósito:** crear una copia preparada adecuada para el análisis manteniendo la trazabilidad respecto al archivo original.

El sistema deberá:

- Declarar las transformaciones aplicadas y su justificación.
- Corregir o convertir tipos cuando sea necesario.
- Definir el tratamiento de ausencias, duplicados, categorías inconsistentes y valores inválidos.
- Diferenciar valores extremos válidos de posibles errores antes de eliminarlos.
- Crear variables derivadas solo cuando aporten valor analítico.
- Conservar la población y las columnas necesarias para interpretar las decisiones adoptadas.

La decisión justificada de conservar un dato contará como una decisión válida de preparación. No deberá aplicarse una limpieza automática indiscriminada.

**Evidencia mínima:** copia preparada separada, registro de transformaciones y comparación básica antes-después.

### Etapa 4. Estadística descriptiva

**Propósito:** resumir correctamente el comportamiento básico de las variables relevantes.

El sistema deberá seleccionar medidas apropiadas según los tipos y distribuciones, incluyendo cuando proceda:

- Conteos y frecuencias.
- Tendencia central y dispersión.
- Cuantiles y rangos.
- Proporciones o tasas.
- Estadísticas por grupos relevantes.

Las cifras deben indicar qué datos se utilizan para calcularlas y, cuando corresponda, qué filtros o transformaciones se aplican.

**Evidencia mínima:** estadísticas reproducibles para las variables y grupos principales, conservadas en una salida estructurada.

### Etapa 5. Variables, agregaciones y relaciones

**Propósito:** pasar de una enumeración de estadísticas a un análisis de relaciones y patrones relevantes.

El sistema deberá:

- Examinar relaciones justificadas entre variables numéricas y categóricas.
- Realizar agregaciones temporales o por grupos cuando el dataset lo permita.
- Comparar segmentos relevantes evitando interpretar identificadores como medidas.
- Comprobar posibles redundancias o identidades entre variables.
- Diferenciar asociación, descripción y causalidad.

No se exige aplicar todas las técnicas posibles. Se priorizarán análisis pertinentes y comprensibles para el dataset.

**Evidencia mínima:** resultados de al menos varias relaciones o agregaciones justificadas y una interpretación vinculada a sus cifras.

### Etapa 6. Visualizaciones

**Propósito:** representar los patrones principales de manera técnicamente correcta y legible.

El sistema deberá:

- Elegir gráficos adecuados para la variable, relación u objetivo representado.
- Incluir títulos, ejes, unidades, leyendas y etiquetas cuando sean necesarios.
- Evitar escalas o agregaciones engañosas.
- Tratar la alta cardinalidad, densidad o presencia de extremos sin ocultar información relevante.
- Vincular cada visualización con una pregunta o hallazgo del análisis.

Generar más gráficos no implica mayor calidad. Se valorará el cumplimiento de los objetivos visuales pertinentes, no la cantidad.

**Evidencia mínima:** conjunto de figuras válidas, identificables y citadas o explicadas en el análisis.

### Etapa 7. Problemas, riesgos y anomalías

**Propósito:** consolidar las situaciones que afectan a la interpretación, reproducibilidad o validez del análisis.

El sistema deberá registrar:

- Problema o riesgo detectado.
- Evidencia cuantitativa o cualitativa que lo respalda.
- Variables o filas afectadas cuando puedan identificarse.
- Acción adoptada o recomendada.
- Consecuencia posible sobre los resultados.
- Nivel de incertidumbre cuando no pueda determinarse si se trata de un error.

No deberá presentar como anomalía cualquier valor extremo de forma automática ni inventar problemas sin evidencia.

**Evidencia mínima:** relación estructurada de problemas, decisiones y efectos potenciales.

### Etapa 8. Informe final

**Propósito:** integrar el análisis en un documento comprensible, verificable y prudente.

El informe deberá:

- Explicar el dataset y el alcance del análisis.
- Resumir la calidad y las decisiones de preparación.
- Presentar los hallazgos principales con cifras y visualizaciones de respaldo.
- Diferenciar hechos observados, interpretaciones y posibles explicaciones.
- Evitar afirmaciones causales no justificadas.
- Reconocer limitaciones, incertidumbres y decisiones que pueden cambiar los resultados.
- Mantener coherencia con las estadísticas, figuras y problemas registrados.

**Evidencia mínima:** informe final estructurado cuyas afirmaciones comprobables puedan rastrearse hasta las salidas de la ejecución.

## 7. Reglas transversales de las ocho etapas

1. **Trazabilidad:** toda cifra o afirmación comprobable deberá proceder del dataset y poder relacionarse con una salida generada.
2. **Reproducibilidad:**  debe quedar constancia del código o de las operaciones necesarias para obtener los resultados.
3. **Preservación:** el archivo de entrada no podrá modificarse ni sobrescribirse.
4. **Justificación:** limpiar, transformar o excluir observaciones requerirá una razón explícita.
5. **Prudencia:** no se convertirán asociaciones en conclusiones causales.
6. **Pertinencia:** no se premiará el volumen de análisis, código o visualizaciones si no contribuyen al objetivo.
7. **Equivalencia:** se aceptarán procedimientos diferentes que produzcan resultados válidos y trazables.
8. **Aislamiento:** solo podrán emplearse las entradas y herramientas autorizadas para la ejecución.

## 8. Relación con el piloto y el experimento definitivo

El piloto D0 permite comprobar que las tres implementaciones pueden aplicar este contrato y generar las evidencias necesarias para evaluar las etapas. Los ajustes derivados de esta comprobación se aplican a las tres implementaciones antes de fijar la versión definitiva. Durante las ejecuciones con D1 y D2 se mantienen el alcance, las entradas, el objetivo y las etapas establecidos.

---

[← Índice](../contrato_comun_v1.0.md) · [Parte 2 →](02_roles_coordinacion_y_finalizacion.md)
