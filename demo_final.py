"""
🎯 Demo Final: Píldora Data Cleaning Avanzado en Python
======================================================

Demo completa y funcional de la píldora de Data Cleaning.
Incluye todos los ejemplos y casos prácticos integrados.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
import warnings
warnings.filterwarnings('ignore')

# Configurar visualizaciones
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DemoDataCleaning:
    """Clase principal para la demo de Data Cleaning"""
    
    def __init__(self):
        self.datos = {}
        self.resultados = {}
    
    def crear_datos_ejemplo(self):
        """Crea datos de ejemplo para la demo"""
        print("📊 Creando datos de ejemplo...")
        
        # Datos de outliers
        np.random.seed(42)
        datos_normales = {
            'precio': np.random.normal(50, 15, 200),
            'cantidad': np.random.poisson(5, 200),
            'descuento': np.random.beta(2, 5, 200),
            'edad_cliente': np.random.normal(35, 10, 200)
        }
        
        outliers = {
            'precio': [1000, 2000, 5, 3000],
            'cantidad': [1, 1, 50, 1],
            'descuento': [0.9, 0.95, 0.1, 0.99],
            'edad_cliente': [120, 5, 200, 0]
        }
        
        df_normales = pd.DataFrame(datos_normales)
        df_outliers = pd.DataFrame(outliers)
        df_outliers_completo = pd.concat([df_normales, df_outliers], ignore_index=True)
        df_outliers_completo['id'] = range(len(df_outliers_completo))
        
        # Datos de texto sucio
        datos_texto = {
            'telefono': ['+34-666-123-456', '666 123 456', '666.123.456', '34666123456', '555-123-456'],
            'email': ['JUAN@GMAIL.COM', 'ana@Yahoo.es  ', 'pedro@hotmail', 'maria@', 'jose@empresa.com'],
            'nombre': ['  Juan Pérez  ', 'ANA GARCÍA', 'pedro lópez', 'MARÍA DEL CARMEN', 'José María'],
            'direccion': ['C/ Mayor, 123', 'Av. de la Constitución, 45', 'Pl. España, 1', 'Calle del Sol, 67', 'Avenida de la Paz, 89']
        }
        df_texto = pd.DataFrame(datos_texto)
        
        # Datos de e-commerce
        datos_ecommerce = {
            'producto': ['iPhone 13 Pro', 'Samsung Galaxy S21', 'MacBook Pro 16"', 'Sony WH-1000XM4', 'Nintendo Switch'],
            'precio': ['1,199.99€', '$1,299.99', '2,499.00 EUR', '£349.99', '349.99 USD'],
            'categoria': ['electronics', 'Electrónica', 'tech', 'Electronics', 'gaming'],
            'descripcion': [
                '<p>El <strong>iPhone 13 Pro</strong> con <em>256GB</em></p>',
                'Samsung Galaxy S21 Ultra con cámara de 108MP',
                '<div>MacBook Pro 16" con chip <b>M1 Pro</b></div>',
                'Sony WH-1000XM4 - <span>Auriculares inalámbricos</span>',
                'Nintendo Switch OLED - <i>Consola de videojuegos</i>'
            ]
        }
        df_ecommerce = pd.DataFrame(datos_ecommerce)
        
        # Datos temporales
        fechas_base = pd.date_range('2023-01-01', periods=20, freq='2H')
        fechas_mixtas = []
        for i, fecha in enumerate(fechas_base):
            if i % 5 == 0:
                fechas_mixtas.append(fecha.strftime('%d/%m/%Y %H:%M:%S'))
            else:
                fechas_mixtas.append(fecha.strftime('%Y-%m-%d %H:%M:%S'))
        
        datos_temporal = {
            'timestamp': fechas_mixtas,
            'temperatura': np.random.normal(20, 5, 20),
            'humedad': np.random.normal(65, 10, 20),
            'presion': np.random.normal(1013, 2, 20)
        }
        df_temporal = pd.DataFrame(datos_temporal)
        
        self.datos = {
            'outliers': df_outliers_completo,
            'texto': df_texto,
            'ecommerce': df_ecommerce,
            'temporal': df_temporal
        }
        
        print("✅ Datos creados exitosamente")
        return self.datos
    
    def demo_deteccion_outliers(self):
        """Demo de detección de outliers"""
        print("\n🔍 DEMO: DETECCIÓN DE OUTLIERS")
        print("=" * 50)
        
        df = self.datos['outliers']
        columnas = ['precio', 'cantidad', 'descuento', 'edad_cliente']
        
        print(f"Dataset: {len(df)} registros")
        print(f"Columnas: {', '.join(columnas)}")
        print()
        
        # Z-score
        print("📊 MÉTODO Z-SCORE:")
        z_scores = np.abs((df[columnas] - df[columnas].mean()) / df[columnas].std())
        outliers_zscore = (z_scores > 3).any(axis=1)
        print(f"Outliers detectados: {outliers_zscore.sum()}")
        
        # IQR
        print("\n📊 MÉTODO IQR:")
        outliers_iqr = pd.Series([False] * len(df))
        for col in columnas:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers_iqr |= (df[col] < lower_bound) | (df[col] > upper_bound)
        print(f"Outliers detectados: {outliers_iqr.sum()}")
        
        # Isolation Forest
        print("\n🤖 MÉTODO ISOLATION FOREST:")
        try:
            from sklearn.ensemble import IsolationForest
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            outliers_isolation = iso_forest.fit_predict(df[columnas]) == -1
            print(f"Outliers detectados: {outliers_isolation.sum()}")
        except ImportError:
            print("⚠️ scikit-learn no disponible, usando Z-score")
            outliers_isolation = outliers_zscore
        
        # Guardar resultados
        df['outlier_zscore'] = outliers_zscore
        df['outlier_iqr'] = outliers_iqr
        df['outlier_isolation'] = outliers_isolation
        
        self.resultados['outliers'] = df
        
        print("\n💡 RECOMENDACIONES:")
        print("• Z-Score: Mejor para datos normalmente distribuidos")
        print("• IQR: Más robusto para datos sesgados")
        print("• Isolation Forest: Ideal para múltiples variables")
        
        return df
    
    def demo_limpieza_texto(self):
        """Demo de limpieza de texto"""
        print("\n🧹 DEMO: LIMPIEZA DE TEXTO")
        print("=" * 50)
        
        df = self.datos['texto']
        print("Datos originales:")
        print(df.to_string(index=False))
        print()
        
        # Limpiar teléfonos
        def limpiar_telefono(telefono):
            numeros = re.sub(r'[^\d]', '', str(telefono))
            if len(numeros) == 9 and numeros.startswith('6'):
                return f"+34-{numeros[:3]}-{numeros[3:6]}-{numeros[6:9]}"
            return None
        
        df['telefono_limpio'] = df['telefono'].apply(limpiar_telefono)
        
        # Limpiar emails
        def limpiar_email(email):
            email = str(email).strip().lower()
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return email if re.match(patron, email) else None
        
        df['email_limpio'] = df['email'].apply(limpiar_email)
        
        # Limpiar nombres
        def limpiar_nombre(nombre):
            nombre = str(nombre).strip().title()
            nombre = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]', '', nombre)
            nombre = re.sub(r'\s+', ' ', nombre)
            return nombre if len(nombre) > 2 else None
        
        df['nombre_limpio'] = df['nombre'].apply(limpiar_nombre)
        
        # Limpiar direcciones
        def limpiar_direccion(direccion):
            direccion = str(direccion).strip().title()
            reemplazos = {
                'C/': 'Calle ',
                'Av.': 'Avenida ',
                'Pl.': 'Plaza '
            }
            for abrev, completo in reemplazos.items():
                direccion = direccion.replace(abrev, completo)
            return direccion
        
        df['direccion_limpia'] = df['direccion'].apply(limpiar_direccion)
        
        print("Datos limpios:")
        columnas_limpias = [col for col in df.columns if 'limpio' in col or 'limpia' in col]
        print(df[columnas_limpias].to_string(index=False))
        
        # Estadísticas
        print(f"\n📊 ESTADÍSTICAS DE LIMPIEZA:")
        for col in columnas_limpias:
            validos = df[col].notna().sum()
            total = len(df)
            print(f"{col}: {validos}/{total} ({validos/total*100:.1f}%)")
        
        self.resultados['texto'] = df
        return df
    
    def demo_casos_practicos(self):
        """Demo de casos prácticos"""
        print("\n🎯 DEMO: CASOS PRÁCTICOS")
        print("=" * 50)
        
        # Caso E-commerce
        print("🛒 CASO 1: E-COMMERCE")
        print("-" * 30)
        
        df_ecommerce = self.datos['ecommerce']
        print("Datos originales:")
        print(df_ecommerce.to_string(index=False))
        print()
        
        # Normalizar precios
        def normalizar_precio(precio_str):
            patron = r'([\d,\.]+)\s*([€$£¥]|EUR|USD|GBP|JPY)'
            match = re.search(patron, precio_str, re.IGNORECASE)
            if match:
                # Manejar diferentes formatos de números
                precio_texto = match.group(1)
                # Si tiene punto como separador de miles, reemplazarlo
                if '.' in precio_texto and ',' in precio_texto:
                    precio_texto = precio_texto.replace('.', '').replace(',', '.')
                elif ',' in precio_texto:
                    precio_texto = precio_texto.replace(',', '.')
                
                try:
                    precio_num = float(precio_texto)
                    moneda = match.group(2).upper()
                    tasas = {'EUR': 0.85, 'USD': 1.0, 'GBP': 0.73, 'JPY': 110.0}
                    return precio_num / tasas.get(moneda, 1.0)
                except ValueError:
                    return None
            return None
        
        df_ecommerce['precio_normalizado'] = df_ecommerce['precio'].apply(normalizar_precio)
        
        # Limpiar categorías
        def limpiar_categoria(categoria):
            categoria = str(categoria).strip().lower()
            mapeo = {
                'electronics': ['electronic', 'electrónica', 'electrónicos', 'tech'],
                'gaming': ['gaming', 'juegos', 'consolas']
            }
            for cat_estandar, variantes in mapeo.items():
                if any(var in categoria for var in variantes):
                    return cat_estandar.upper()
            return categoria.upper()
        
        df_ecommerce['categoria_limpia'] = df_ecommerce['categoria'].apply(limpiar_categoria)
        
        # Limpiar descripciones HTML
        def limpiar_html(texto):
            texto = re.sub(r'<[^>]+>', '', str(texto))
            entidades = {'&amp;': '&', '&lt;': '<', '&gt;': '>', '&nbsp;': ' '}
            for entidad, caracter in entidades.items():
                texto = texto.replace(entidad, caracter)
            return texto.strip()
        
        df_ecommerce['descripcion_limpia'] = df_ecommerce['descripcion'].apply(limpiar_html)
        
        print("Datos limpios:")
        columnas_limpias = [col for col in df_ecommerce.columns if 'limpio' in col or 'limpia' in col]
        print(df_ecommerce[['producto'] + columnas_limpias].to_string(index=False))
        
        # Caso Temporal
        print(f"\n⏰ CASO 2: DATOS TEMPORALES")
        print("-" * 30)
        
        df_temporal = self.datos['temporal']
        print("Datos originales:")
        print(df_temporal.head().to_string(index=False))
        print()
        
        # Parsear fechas
        def parsear_fecha(fecha_str):
            formatos = ['%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S']
            for formato in formatos:
                try:
                    return datetime.strptime(fecha_str, formato)
                except ValueError:
                    continue
            return None
        
        df_temporal['timestamp_parsed'] = df_temporal['timestamp'].apply(parsear_fecha)
        
        print(f"Fechas parseadas: {df_temporal['timestamp_parsed'].notna().sum()}/{len(df_temporal)}")
        
        self.resultados['casos'] = {
            'ecommerce': df_ecommerce,
            'temporal': df_temporal
        }
        
        return df_ecommerce, df_temporal
    
    def demo_pipeline_automatizado(self):
        """Demo de pipeline automatizado"""
        print("\n⚙️ DEMO: PIPELINE AUTOMATIZADO")
        print("=" * 50)
        
        # Crear datos de ejemplo con problemas
        np.random.seed(42)
        datos = {
            'id': range(1, 51),
            'nombre': [f'Usuario_{i}' for i in range(1, 51)],
            'email': [f'usuario{i}@email.com' for i in range(1, 51)],
            'edad': np.random.normal(35, 10, 50),
            'salario': np.random.normal(50000, 15000, 50)
        }
        
        df = pd.DataFrame(datos)
        
        # Introducir problemas
        df.loc[10:15, 'email'] = None
        df.loc[20:25, 'edad'] = np.nan
        df = pd.concat([df, df.iloc[:5]], ignore_index=True)  # Duplicados
        
        print(f"📊 Datos originales: {len(df)} filas")
        print(f"❌ Valores nulos: {df.isnull().sum().sum()}")
        print(f"🔄 Duplicados: {df.duplicated().sum()}")
        print()
        
        # Pipeline de limpieza
        print("🚀 Ejecutando pipeline...")
        
        # 1. Eliminar duplicados
        df_limpio = df.drop_duplicates()
        print(f"1. Duplicados eliminados: {len(df) - len(df_limpio)}")
        
        # 2. Manejar valores nulos
        df_limpio['email'] = df_limpio['email'].fillna('unknown@email.com')
        df_limpio['edad'] = df_limpio['edad'].fillna(df_limpio['edad'].median())
        print(f"2. Valores nulos imputados: {df.isnull().sum().sum() - df_limpio.isnull().sum().sum()}")
        
        # 3. Estandarizar texto
        df_limpio['nombre'] = df_limpio['nombre'].str.lower().str.strip()
        print(f"3. Texto estandarizado")
        
        # 4. Detectar outliers (Z-score)
        z_scores = np.abs((df_limpio['salario'] - df_limpio['salario'].mean()) / df_limpio['salario'].std())
        outliers = z_scores > 3
        df_limpio['outlier'] = outliers
        print(f"4. Outliers detectados: {outliers.sum()}")
        
        print(f"\n✅ Pipeline completado:")
        print(f"  📊 Filas finales: {len(df_limpio)}")
        print(f"  ❌ Valores nulos: {df_limpio.isnull().sum().sum()}")
        print(f"  🔄 Duplicados: {df_limpio.duplicated().sum()}")
        print(f"  📈 Outliers: {df_limpio['outlier'].sum()}")
        
        self.resultados['pipeline'] = df_limpio
        return df_limpio
    
    def demo_visualizaciones(self):
        """Demo de visualizaciones"""
        print("\n📊 DEMO: VISUALIZACIONES")
        print("=" * 50)
        
        try:
            # Crear datos de ejemplo
            np.random.seed(42)
            datos = np.random.normal(50, 15, 100)
            
            # Crear figura con subplots
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            
            # Histograma
            axes[0, 0].hist(datos, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            axes[0, 0].set_title('Distribución de Datos')
            axes[0, 0].set_xlabel('Valor')
            axes[0, 0].set_ylabel('Frecuencia')
            axes[0, 0].grid(True, alpha=0.3)
            
            # Box plot
            axes[0, 1].boxplot(datos, patch_artist=True, boxprops=dict(facecolor='lightgreen'))
            axes[0, 1].set_title('Box Plot')
            axes[0, 1].set_ylabel('Valor')
            axes[0, 1].grid(True, alpha=0.3)
            
            # Scatter plot
            x = np.random.normal(50, 15, 100)
            y = x + np.random.normal(0, 5, 100)
            axes[1, 0].scatter(x, y, alpha=0.6, color='coral')
            axes[1, 0].set_title('Scatter Plot')
            axes[1, 0].set_xlabel('X')
            axes[1, 0].set_ylabel('Y')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Time series
            fechas = pd.date_range('2023-01-01', periods=100, freq='D')
            valores = np.cumsum(np.random.randn(100))
            axes[1, 1].plot(fechas, valores, color='purple', linewidth=2)
            axes[1, 1].set_title('Serie Temporal')
            axes[1, 1].set_xlabel('Fecha')
            axes[1, 1].set_ylabel('Valor')
            axes[1, 1].tick_params(axis='x', rotation=45)
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('demo_visualizaciones.png', dpi=150, bbox_inches='tight')
            plt.show()
            
            print("✅ Visualizaciones creadas y guardadas como 'demo_visualizaciones.png'")
            
        except Exception as e:
            print(f"❌ Error creando visualizaciones: {e}")
    
    def ejecutar_demo_completa(self):
        """Ejecuta la demo completa"""
        print("🎯 DEMO COMPLETA: DATA CLEANING AVANZADO EN PYTHON")
        print("=" * 70)
        print()
        print("¡Hola! Esta es una demostración completa de técnicas avanzadas")
        print("de limpieza de datos en Python. Vamos a ver ejemplos prácticos")
        print("que puedes usar en tus proyectos reales.")
        print()
        
        # Crear datos
        self.crear_datos_ejemplo()
        
        # Ejecutar demos
        self.demo_deteccion_outliers()
        self.demo_limpieza_texto()
        self.demo_casos_practicos()
        self.demo_pipeline_automatizado()
        self.demo_visualizaciones()
        
        # Resumen final
        print("\n" + "=" * 70)
        print("🎉 DEMO COMPLETADA")
        print("=" * 70)
        print()
        print("📚 TÉCNICAS DEMOSTRADAS:")
        print("✅ Detección inteligente de outliers")
        print("✅ Limpieza de texto con regex")
        print("✅ Casos prácticos de e-commerce y temporales")
        print("✅ Pipeline automatizado de limpieza")
        print("✅ Visualizaciones de datos")
        print()
        print("💡 PRÓXIMOS PASOS:")
        print("1. Practica con tus propios datasets")
        print("2. Adapta las técnicas a tus necesidades")
        print("3. Comparte conocimiento con tu equipo")
        print("4. Mantén actualizada tu documentación")
        print()
        print("¡Gracias por tu atención! 🙏")

def main():
    """Función principal"""
    demo = DemoDataCleaning()
    demo.ejecutar_demo_completa()

if __name__ == "__main__":
    main()
