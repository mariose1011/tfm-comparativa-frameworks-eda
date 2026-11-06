# Referencias de evaluación

Esta carpeta contiene los valores y criterios de referencia de D0, D1 y D2. Su contenido no se facilitó a los agentes durante las ejecuciones.

Cada dataset dispone de:

- `ficha_referencia_*.md`: explicación del dataset, sus resultados esperados y sus criterios de evaluación.
- `reference_values.json`: valores calculados a partir de la entrada experimental.
- `evaluation_spec.json`: comprobaciones numéricas, pesos, decisiones de preparación, riesgos, contenidos del informe y objetivos visuales.
- Un script para generar los valores de referencia.

En D0, el script también genera el conjunto de datos sintético mediante una semilla fija.

Los archivos `evaluation_spec.json` conservan la especificación original. El [protocolo](../../experimento/evaluacion/01_protocolo_calidad_Q1_Q10_v0.1.md) y las guías de [D1](../../experimento/evaluacion/02_ficha_D1_bike_sharing.md) y [D2](../../experimento/evaluacion/02_ficha_D2_online_retail.md) recogen las reglas y aclaraciones aplicadas en la evaluación final.

Los generadores deben ejecutarse fuera del entorno de los agentes. Su ejecución sobrescribe los archivos que generan.