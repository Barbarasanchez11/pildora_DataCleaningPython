# Píldora: Data Cleaning Avanzado en Python

## Estructura de la Presentación

### 1. Técnicas Avanzadas de Limpieza (15 minutos)
- **A) Detección Avanzada de Outliers**
  - Métodos estadísticos: Z-score, IQR modificado
  - Isolation Forest para outliers multivariados
  - Código práctico con ejemplos reales

- **B) Limpieza de Texto Avanzada**
  - Expresiones regulares (regex) para patrones complejos
  - Normalización de nombres, direcciones, teléfonos
  - Manejo de encoding (UTF-8, Latin-1)

- **C) Validación de Datos**
  - Reglas de negocio personalizadas
  - Validación cruzada entre columnas
  - Assert statements para verificar calidad

### 2. Casos Prácticos Complejos (10 minutos)
- **Caso 1: Dataset de E-commerce**
  - Precios en diferentes monedas
  - Categorías inconsistentes
  - Descripciones con HTML/caracteres especiales

- **Caso 2: Datos Temporales**
  - Timestamps en diferentes zonas horarias
  - Frecuencias irregulares
  - Gaps temporales

### 3. Automatización y Buenas Prácticas (5 minutos)
- Pipeline de limpieza reutilizable
- Logging de transformaciones
- Testing de calidad de datos
- Documentación de decisiones de limpieza

## Archivos Incluidos

- `01_deteccion_outliers.py` - Ejemplos de detección avanzada de outliers
- `02_limpieza_texto.py` - Limpieza de texto con regex
- `03_casos_practicos.py` - Casos prácticos complejos
- `04_pipeline_automatizado.py` - Pipeline de limpieza automatizado
- `05_presentacion_principal.py` - Archivo principal con guión completo
- `datos_ejemplo/` - Datasets de ejemplo para los casos prácticos