# Variable respuesta del proyecto

## Diagnóstico breve

- El repositorio versionado implementa limpieza, exploración y clustering, pero no formaliza todavía una tarea supervisada.
- La exploración y los materiales analíticos asociados priorizan `hec_tipagre` como una de las variables categóricas centrales del fenómeno estudiado.
- El clustering actual usa `edad_limpia` y `total_hijos`, por lo que la línea de trabajo existente es descriptiva y no resuelve por sí sola la consigna de variable respuesta.

## Problema científico definido

Predecir la tipología de violencia registrada en `hec_tipagre` a partir de las características observables de la víctima, del agresor y del contexto del hecho contenidas en la base unificada del INE.

## Decisión metodológica

- Variable respuesta final: `hec_tipagre`
- Tipo de variable: cualitativa nominal
- Tipo de problema: clasificación multiclase

Se elige `hec_tipagre` porque representa directamente la modalidad de violencia reportada. Esto la vuelve más coherente con el fenómeno científico central del dataset que variables institucionales posteriores al hecho, como `ley_aplicable`, `tipo_medida`, `organismo_jurisdiccional` o `conducente`. Además, esta elección permite reutilizar como futuras variables explicativas a `edad_limpia`, `agr_edad`, `total_hijos`, `otras_victimas`, `anio_registro`, `vic_rel_agr`, `hec_area`, `sexo_limpio` y `quien_reporta`.

## Transformaciones aplicadas y recomendadas

### Prefab en proyecto 1

- Eliminación de columnas completamente vacías.
- Conversión de `fecha_hecho_limpia` a fecha.
- Conversión de columnas numéricas candidatas con reglas para `ninguno/a`, `98 y más` y tokens de faltantes.

### Formalizadas para la variable respuesta

- Normalización de texto con `strip` y mayúsculas sostenidas.
- Corrección de ruido de codificación (`mojibake`) para colapsar duplicados textuales equivalentes.
- Estandarización de separadores con guion en `hec_tipagre`.

Estas transformaciones no cambian el significado de la variable; únicamente eliminan ruido técnico. Con esta limpieza, `hec_tipagre` queda definida como la etiqueta supervisada del proyecto.

## Sección lista para informe

### Variable respuesta

Con base en la auditoría del repositorio, del dataset utilizado por el proyecto y de los artefactos analíticos disponibles, se define como variable respuesta final `hec_tipagre`, correspondiente a la tipología de la violencia registrada en cada caso. Esta variable es de naturaleza cualitativa nominal, por lo que el problema queda formalizado como uno de clasificación multiclase.

La elección de `hec_tipagre` se sustenta en que representa directamente el fenómeno científico central de la base de datos: la modalidad de agresión denunciada. A diferencia de variables institucionales como `ley_aplicable`, `tipo_medida`, `organismo_jurisdiccional` o `conducente`, que describen decisiones o rutas procesales posteriores al hecho, `hec_tipagre` captura el evento sustantivo que se busca explicar y predecir. Asimismo, esta variable ya ocupa un lugar central en la exploración del proyecto, donde ha sido utilizada en tablas de frecuencia y análisis relacionales, lo que refuerza su pertinencia metodológica.

Desde la perspectiva del diseño del problema, esta decisión permite reencauzar el proyecto desde un enfoque predominantemente descriptivo y de clustering hacia una formulación supervisada sin romper la lógica ya desarrollada. Las variables trabajadas en exploración y segmentación, como `edad_limpia`, `agr_edad`, `total_hijos`, `otras_victimas`, `anio_registro`, `vic_rel_agr`, `hec_area`, `sexo_limpio` y `quien_reporta`, quedan definidas como candidatas naturales a variables explicativas para etapas posteriores de modelación.

Antes de modelar, `hec_tipagre` debe mantenerse en una versión textual normalizada para asegurar consistencia semántica. En particular, se requiere estandarizar mayúsculas y espacios, así como corregir duplicados introducidos por errores de codificación de caracteres, por ejemplo `PSICOLÃ³GICA` frente a `PSICOLÓGICA` o `FÃ­SICA` frente a `FÍSICA`. Esta recodificación no altera el contenido sustantivo de la variable; únicamente elimina ruido técnico y deja la etiqueta lista para una tarea de clasificación supervisada.

## Tabla para informe

| Nombre de la variable | Tipo | Motivo de elección | Transformaciones aplicadas | Impacto esperado |
| --- | --- | --- | --- | --- |
| `hec_tipagre` | Cualitativa nominal; problema de clasificación multiclase | Representa directamente la modalidad de violencia del caso, ya es una variable priorizada en la exploración y permite reutilizar el trabajo descriptivo previo como base para predictores | Normalización de texto, mayúsculas sostenidas, corrección de mojibake y estandarización de separadores; no se fusionan categorías semánticamente distintas | Define una etiqueta supervisada defendible y alinea el proyecto con la consigna de variable respuesta y preparación del problema |
