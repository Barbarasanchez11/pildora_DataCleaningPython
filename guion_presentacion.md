# 🎯 Guión Completo: Píldora Data Cleaning Avanzado en Python

## 📋 Información General
- **Duración**: 30 minutos (25 min presentación + 5 min preguntas)
- **Audiencia**: Desarrolladores/Data Scientists con conocimientos básicos de Python
- **Objetivo**: Mostrar técnicas avanzadas de limpieza de datos para proyectos reales

---

## 🚀 Introducción (2 minutos)

### Saludo y Contexto
"Hola a todos! 👋 Mi compañero nos ha mostrado los fundamentos del data cleaning. Ahora vamos a ver técnicas más avanzadas que realmente marcan la diferencia en la calidad de tus análisis."

### Puntos clave a transmitir:
- ✅ Estas son técnicas del mundo real que usarás en proyectos
- ✅ Van más allá de `dropna()` y `fillna()`
- ✅ La diferencia entre un análisis mediocre y uno profesional
- ✅ 30 minutos que cambiarán tu forma de trabajar con datos

### Agenda visual:
```
📊 Técnicas Avanzadas (15 min)
   ├── Detección inteligente de outliers
   ├── Limpieza de texto con regex
   └── Validación de datos
🎯 Casos Prácticos (10 min)
   ├── E-commerce con múltiples problemas
   └── Series temporales complejas
⚙️ Automatización (5 min)
   ├── Pipeline reutilizable
   └── Buenas prácticas
```

## Parte 1: Detección Inteligente de Outliers (8 min)

### A) Métodos Estadísticos Tradicionales (3 min)
```python
# Mostrar Z-score y IQR
def detectar_outliers_zscore(df, columnas, threshold=3):
    # Código para Z-score
    pass

def detectar_outliers_iqr(df, columnas, factor=1.5):
    # Código para IQR
    pass
```

**Puntos a destacar:**
- Z-score: Mejor para datos normalmente distribuidos
- IQR: Más robusto para datos sesgados
- Mostrar cuándo fallan estos métodos

### B) Isolation Forest para Outliers Multivariados (5 min)
```python
# Código práctico con ejemplos reales
def detectar_outliers_isolation_forest(df, columnas, contamination=0.1):
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    outliers = iso_forest.fit_predict(df[columnas])
    return outliers
```

**Puntos a destacar:**
- Mejor para múltiples variables
- Detecta outliers complejos
- Configuración del parámetro contamination

## Parte 2: Limpieza de Texto Avanzada (7 min)

### A) Expresiones Regulares para Patrones Complejos (4 min)
```python
# Datos sucios típicos de CRM
clientes_sucios = pd.DataFrame({
    'telefono': ['+34-666-123-456', '666 123 456', '666.123.456'],
    'email': ['JUAN@GMAIL.COM', 'ana@Yahoo.es  ', 'pedro@hotmail'],
    'nombre': ['  Juan Pérez  ', 'ANA GARCÍA', 'pedro lópez']
})

def limpiar_telefonos(telefono):
    numeros = re.sub(r'[^\d]', '', str(telefono))
    if numeros.startswith('34'):
        numeros = numeros[2:]
    return f"+34-{numeros[:3]}-{numeros[3:6]}-{numeros[6:9]}" if len(numeros) == 9 else None
```

**Puntos a destacar:**
- Patrones regex específicos para cada tipo
- Validación de formatos
- Normalización consistente

### B) Manejo de Encoding y HTML (3 min)
```python
def limpiar_html(texto):
    # Eliminar etiquetas HTML
    texto_limpio = re.sub(r'<[^>]+>', '', str(texto))
    # Decodificar entidades HTML
    entidades = {'&amp;': '&', '&lt;': '<', '&gt;': '>'}
    for entidad, caracter in entidades.items():
        texto_limpio = texto_limpio.replace(entidad, caracter)
    return texto_limpio.strip()
```

## Parte 3: Casos Prácticos Complejos (10 min)

### Caso 1: Dataset de E-commerce (5 min)
```python
# Ejemplo: Limpiar datos de productos con múltiples problemas
- Precios en diferentes monedas
- Categorías inconsistentes  
- Descripciones con HTML/caracteres especiales
```

**Problemas a resolver:**
- Normalizar precios a una moneda base
- Estandarizar categorías
- Limpiar descripciones HTML

### Caso 2: Datos Temporales (5 min)
```python
# Manejo de series temporales sucias
- Timestamps en diferentes zonas horarias
- Frecuencias irregulares
- Gaps temporales
```

**Problemas a resolver:**
- Parsear fechas en diferentes formatos
- Normalizar zonas horarias
- Rellenar gaps temporales

## Parte 4: Automatización y Buenas Prácticas (5 min)

### A) Pipeline de Limpieza Reutilizable (3 min)
```python
class DataCleaner:
    def __init__(self):
        self.transformations = []
    
    def fit_transform(self, df):
        # 1. Eliminar duplicados exactos
        # 2. Estandarizar columnas de texto
        # 3. Manejar valores nulos con estrategia inteligente
        # 4. Log de transformaciones
        pass
```

### B) Logging y Testing (2 min)
```python
# Logging de transformaciones
print(f"Filas eliminadas (duplicados): {len(df) - len(df_clean)}")
print(f"Valores nulos imputados: {df.isnull().sum().sum()}")

# Testing de calidad de datos
def validar_calidad(df):
    assert df.duplicated().sum() == 0, "Hay duplicados"
    assert df.isnull().sum().sum() == 0, "Hay valores nulos"
    return True
```

## Conclusión (3 min)

### Puntos clave:
- Resumir técnicas aprendidas
- Enfatizar la importancia de la automatización
- Mencionar próximos pasos
- Abrir para preguntas

### Frases de cierre:
"Estas son las técnicas que realmente marcan la diferencia en la calidad de tus análisis. La clave está en automatizar, documentar y validar todo lo que haces."

## Notas para el Presentador

### Antes de empezar:
- Verificar que todos los módulos se importan correctamente
- Tener datos de ejemplo preparados
- Probar la visualización de gráficos

### Durante la presentación:
- Pausar para preguntas después de cada parte
- Mostrar el código en vivo cuando sea posible
- Explicar el "por qué" detrás de cada técnica

### Si algo falla:
- Tener versiones simplificadas de los ejemplos
- Explicar el concepto aunque el código no funcione
- Mantener la calma y seguir con la presentación

### Tiempo estimado:
- Introducción: 2 min
- Parte 1: 8 min
- Parte 2: 7 min
- Parte 3: 10 min
- Parte 4: 5 min
- Conclusión: 3 min
- **Total: 35 minutos** (con 5 min de buffer para preguntas)
