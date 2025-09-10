# 🎯 Píldora: Data Cleaning Avanzado en Python

Una píldora completa sobre técnicas avanzadas de limpieza de datos en Python, diseñada para desarrolladores y data scientists que quieren llevar sus habilidades al siguiente nivel.

## 🚀 Inicio Rápido

### 1. Verificar Instalación
```bash
python verificar_instalacion.py
```

### 2. Ejecutar Presentación
```bash
python presentacion_interactiva.py
```

### 3. Opciones Disponibles
- 🚀 Presentación completa (30 min)
- ⚡ Demo rápida (10 min)
- 🔍 Módulos individuales
- 📊 Visualización de datasets

## 📚 Contenido de la Píldora

### 🔍 Parte 1: Detección Inteligente de Outliers (8 min)
- **Métodos estadísticos tradicionales**
  - Z-score para datos normalmente distribuidos
  - IQR para datos con distribución sesgada
  - Comparación de métodos y cuándo usar cada uno

- **Isolation Forest para outliers multivariados**
  - Detección de outliers complejos
  - Configuración del parámetro contamination
  - Visualizaciones interactivas

### 🧹 Parte 2: Limpieza de Texto con Regex (7 min)
- **Expresiones regulares para patrones complejos**
  - Teléfonos españoles: `r'^(\+34|0034|34)?[6-9]\d{8}$'`
  - Emails: `r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'`
  - HTML: `r'<[^>]+>'` (eliminar etiquetas)

- **Normalización avanzada**
  - Nombres, direcciones, teléfonos
  - Manejo de encoding (UTF-8, Latin-1)
  - Validación de formatos

### 🎯 Parte 3: Casos Prácticos Complejos (10 min)
- **Caso 1: Dataset de E-commerce**
  - Precios en diferentes monedas (€, $, £, ¥)
  - Categorías inconsistentes
  - Descripciones con HTML
  - Validación de SKUs

- **Caso 2: Datos Temporales**
  - Timestamps en diferentes formatos
  - Zonas horarias inconsistentes
  - Gaps temporales y frecuencias irregulares
  - Relleno inteligente de datos faltantes

### ⚙️ Parte 4: Pipeline Automatizado (5 min)
- **Pipeline de limpieza reutilizable**
  - Configuración flexible
  - Logging detallado de transformaciones
  - Validación automática de calidad

- **Buenas prácticas**
  - Documentación de decisiones
  - Testing de calidad de datos
  - Manejo de errores robusto

## 📁 Estructura del Proyecto

```
pildora_DataCleaningPython/
├── 📊 datos_ejemplo/                    # Datasets de demostración
│   ├── ecommerce_sucio.csv             # Datos de e-commerce con problemas
│   ├── clientes_sucio.csv              # Datos de clientes inconsistentes
│   ├── temporal_sucio.csv              # Series temporales con gaps
│   ├── outliers_demo.csv               # Dataset con outliers intencionales
│   ├── metadatos.json                  # Información de los datasets
│   └── crear_datasets_demo.py          # Generador de datos de ejemplo
├── 🔧 01_deteccion_outliers.py         # Detección avanzada de outliers
├── 🧹 02_limpieza_texto.py             # Limpieza de texto con regex
├── 🎯 03_casos_practicos.py            # Casos prácticos complejos
├── ⚙️ 04_pipeline_automatizado.py      # Pipeline de limpieza automatizado
├── 🎤 05_presentacion_principal.py     # Presentación original
├── 🚀 presentacion_interactiva.py      # Presentación interactiva mejorada
├── 🔧 verificar_instalacion.py         # Verificador de instalación
├── 📋 guion_presentacion.md            # Guión detallado de la presentación
├── 📦 requirements.txt                 # Dependencias del proyecto
└── 📖 README.md                        # Este archivo
```

## 🛠️ Instalación y Configuración

### Requisitos del Sistema
- Python 3.8 o superior
- 4GB RAM mínimo
- 500MB espacio en disco

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Verificación de la Instalación
```bash
python verificar_instalacion.py
```

## 🎯 Uso de la Píldora

### Presentación Completa
```bash
python presentacion_interactiva.py
# Seleccionar opción 1
```

### Demo Rápida
```bash
python presentacion_interactiva.py
# Seleccionar opción 2
```

### Módulos Individuales
```bash
# Solo detección de outliers
python presentacion_interactiva.py
# Seleccionar opción 3

# Solo limpieza de texto
python presentacion_interactiva.py
# Seleccionar opción 4

# Solo casos prácticos
python presentacion_interactiva.py
# Seleccionar opción 5

# Solo pipeline automatizado
python presentacion_interactiva.py
# Seleccionar opción 6
```

## 📊 Datasets Incluidos

### E-commerce Sucio (50 registros)
- Precios en múltiples monedas
- Categorías inconsistentes
- Descripciones con HTML
- SKUs no validados

### Clientes Sucio (100 registros)
- Nombres con espacios extra
- Emails en mayúsculas
- Teléfonos en diferentes formatos
- Direcciones inconsistentes

### Temporal Sucio (100 registros)
- Fechas en diferentes formatos
- Gaps temporales
- Zona horaria inconsistente
- Frecuencia irregular

### Outliers Demo (206 registros)
- Outliers univariados
- Outliers multivariados
- Valores extremos
- Datos inconsistentes

## 🔧 Características Técnicas

### Detección de Outliers
- Z-score con umbral configurable
- IQR con factor multiplicador
- Isolation Forest para multivariados
- Visualizaciones comparativas

### Limpieza de Texto
- Regex para patrones específicos
- Normalización de encoding
- Validación de formatos
- Manejo de HTML

### Pipeline Automatizado
- Configuración flexible
- Logging detallado
- Validación automática
- Reportes documentados

## 🎓 Objetivos de Aprendizaje

Al finalizar esta píldora, serás capaz de:

✅ **Detectar outliers** usando métodos estadísticos y de machine learning
✅ **Limpiar texto** con expresiones regulares avanzadas
✅ **Manejar casos complejos** de e-commerce y series temporales
✅ **Automatizar pipelines** de limpieza reutilizables
✅ **Documentar decisiones** de limpieza para el equipo
✅ **Validar calidad** de datos automáticamente

## 🤝 Contribuciones

Este proyecto está diseñado para ser educativo y colaborativo. Si encuentras errores o tienes sugerencias:

1. Abre un issue describiendo el problema
2. Propón mejoras en el código
3. Comparte casos de uso adicionales
4. Mejora la documentación

## 📞 Soporte

Si tienes problemas con la instalación o ejecución:

1. Ejecuta `python verificar_instalacion.py`
2. Revisa los errores reportados
3. Consulta la documentación de cada módulo
4. Abre un issue con detalles del problema

## 📄 Licencia

Este proyecto está bajo licencia MIT. Puedes usarlo libremente para fines educativos y comerciales.

---

**¡Disfruta aprendiendo Data Cleaning Avanzado en Python!** 🐍✨