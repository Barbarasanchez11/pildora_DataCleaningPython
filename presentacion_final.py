"""
🎯 Píldora Final: Data Cleaning Avanzado en Python
=================================================

Script principal para ejecutar la píldora completa de Data Cleaning.
Incluye menú interactivo y todas las funcionalidades integradas.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Configurar visualizaciones
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class PildoraDataCleaning:
    """Clase principal para la píldora de Data Cleaning"""
    
    def __init__(self):
        self.datos = {}
        self.resultados = {}
        self.configuracion = {
            'mostrar_graficos': True,
            'pausar_entre_secciones': True,
            'guardar_resultados': True
        }
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def pausar(self, mensaje="Presiona Enter para continuar..."):
        """Pausa la ejecución esperando input del usuario"""
        if self.configuracion['pausar_entre_secciones']:
            input(f"\n{mensaje}")
    
    def mostrar_titulo(self, titulo, caracter="="):
        """Muestra un título formateado"""
        print(f"\n{caracter * 60}")
        print(f"{titulo}")
        print(f"{caracter * 60}")
    
    def crear_datos_ejemplo(self):
        """Crea datos de ejemplo para la píldora"""
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
    
    def introduccion(self):
        """Introducción de la píldora"""
        self.limpiar_pantalla()
        self.mostrar_titulo("🎯 PÍLDORA: DATA CLEANING AVANZADO EN PYTHON")
        
        print("¡Hola a todos! 👋")
        print()
        print("Mi compañero nos ha mostrado los fundamentos del data cleaning.")
        print("Ahora vamos a ver técnicas más avanzadas que realmente marcan")
        print("la diferencia en la calidad de tus análisis.")
        print()
        print("🔍 LO QUE VAMOS A APRENDER:")
        print("• Detección inteligente de outliers")
        print("• Limpieza de texto con regex avanzadas")
        print("• Casos prácticos del mundo real")
        print("• Pipeline automatizado y reutilizable")
        print("• Buenas prácticas de documentación")
        print()
        print("⏱️ Duración: 30 minutos")
        print("🎯 Objetivo: Técnicas que usarás en proyectos reales")
        print()
        
        self.pausar("¿Listo para comenzar? Presiona Enter...")
    
    def parte_1_outliers(self):
        """Parte 1: Detección de Outliers"""
        self.limpiar_pantalla()
        self.mostrar_titulo("🔍 PARTE 1: DETECCIÓN INTELIGENTE DE OUTLIERS")
        
        print("Los outliers pueden arruinar tu análisis. Vamos a ver cómo")
        print("detectarlos de manera inteligente usando diferentes métodos.")
        print()
        
        df = self.datos['outliers']
        columnas = ['precio', 'cantidad', 'descuento', 'edad_cliente']
        
        print(f"📊 Dataset: {len(df)} registros")
        print(f"📈 Columnas: {', '.join(columnas)}")
        print()
        
        # Mostrar estadísticas básicas
        print("📈 ESTADÍSTICAS BÁSICAS:")
        print(df[columnas].describe().round(2))
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
        
        print("\n💡 CUÁNDO USAR CADA MÉTODO:")
        print("• Z-Score: Datos normalmente distribuidos")
        print("• IQR: Datos con distribución sesgada")
        print("• Isolation Forest: Múltiples variables (recomendado)")
        
        self.pausar("Presiona Enter para continuar...")
        return df
    
    def parte_2_limpieza_texto(self):
        """Parte 2: Limpieza de Texto"""
        self.limpiar_pantalla()
        self.mostrar_titulo("🧹 PARTE 2: LIMPIEZA DE TEXTO CON REGEX")
        
        print("Los datos de texto son los más sucios. Vamos a ver cómo")
        print("limpiarlos usando expresiones regulares y técnicas avanzadas.")
        print()
        
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
        
        print("\n🔧 PATRONES REGEX CLAVE:")
        print("• Teléfonos: r'^(\\+34|0034|34)?[6-9]\\d{8}$'")
        print("• Emails: r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'")
        print("• HTML: r'<[^>]+>' (eliminar etiquetas)")
        
        self.resultados['texto'] = df
        self.pausar("Presiona Enter para continuar...")
        return df
    
    def parte_3_casos_practicos(self):
        """Parte 3: Casos Prácticos"""
        self.limpiar_pantalla()
        self.mostrar_titulo("🎯 PARTE 3: CASOS PRÁCTICOS COMPLEJOS")
        
        print("Ahora vamos a ver casos reales que encontrarás en el trabajo:")
        print("datos de e-commerce y series temporales.")
        print()
        
        # Caso E-commerce
        print("🛒 CASO 1: DATASET DE E-COMMERCE")
        print("-" * 40)
        print("Problemas típicos:")
        print("• Precios en diferentes monedas")
        print("• Categorías inconsistentes")
        print("• Descripciones con HTML")
        print()
        
        df_ecommerce = self.datos['ecommerce']
        print("Datos originales:")
        print(df_ecommerce.to_string(index=False))
        print()
        
        # Normalizar precios
        def normalizar_precio(precio_str):
            patron = r'([\d,\.]+)\s*([€$£¥]|EUR|USD|GBP|JPY)'
            match = re.search(patron, precio_str, re.IGNORECASE)
            if match:
                precio_texto = match.group(1)
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
        print("-" * 40)
        print("Problemas típicos:")
        print("• Timestamps en diferentes formatos")
        print("• Zonas horarias inconsistentes")
        print("• Gaps temporales")
        print()
        
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
        
        print("\n💡 LECCIONES CLAVE:")
        print("• E-commerce: Normalizar monedas y categorías")
        print("• Temporal: Detectar frecuencia y rellenar gaps")
        print("• Siempre validar antes de procesar")
        
        self.resultados['casos'] = {
            'ecommerce': df_ecommerce,
            'temporal': df_temporal
        }
        
        self.pausar("Presiona Enter para continuar...")
        return df_ecommerce, df_temporal
    
    def parte_4_pipeline(self):
        """Parte 4: Pipeline Automatizado"""
        self.limpiar_pantalla()
        self.mostrar_titulo("⚙️ PARTE 4: PIPELINE AUTOMATIZADO")
        
        print("La clave del éxito: automatizar y documentar todo.")
        print("Vamos a ver cómo crear un pipeline reutilizable.")
        print()
        
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
        
        print("\n💡 CARACTERÍSTICAS DEL PIPELINE:")
        print("• Configuración flexible")
        print("• Logging detallado")
        print("• Validación automática")
        print("• Reportes documentados")
        print("• Manejo de errores robusto")
        
        self.resultados['pipeline'] = df_limpio
        self.pausar("Presiona Enter para continuar...")
        return df_limpio
    
    def conclusion(self):
        """Conclusión de la píldora"""
        self.limpiar_pantalla()
        self.mostrar_titulo("🎉 CONCLUSIÓN Y PRÓXIMOS PASOS")
        
        print("¡Excelente trabajo! Hemos cubierto las técnicas más importantes")
        print("de data cleaning avanzado en Python.")
        print()
        print("📚 RESUMEN DE LO APRENDIDO:")
        print("✅ Detección inteligente de outliers")
        print("✅ Limpieza de texto con regex")
        print("✅ Casos prácticos reales")
        print("✅ Pipeline automatizado")
        print("✅ Buenas prácticas de documentación")
        print()
        print("🚀 PRÓXIMOS PASOS:")
        print("1. Practica con tus propios datasets")
        print("2. Adapta el pipeline a tus necesidades")
        print("3. Comparte conocimiento con tu equipo")
        print("4. Mantén actualizada tu documentación")
        print()
        print("💡 RECUERDA:")
        print("• La calidad de los datos determina la calidad del análisis")
        print("• Automatiza todo lo que puedas")
        print("• Documenta cada decisión")
        print("• Valida siempre los resultados")
        print()
        print("❓ ¿PREGUNTAS?")
        print("Estoy aquí para ayudarte con cualquier duda.")
        print()
        print("¡Gracias por tu atención! 🙏")
    
    def ejecutar_presentacion_completa(self):
        """Ejecuta la presentación completa"""
        print("🚀 INICIANDO PÍLDORA COMPLETA")
        print("Duración estimada: 30 minutos")
        print()
        
        # Crear datos
        self.crear_datos_ejemplo()
        
        # Introducción
        self.introduccion()
        
        # Partes de la píldora
        self.parte_1_outliers()
        self.parte_2_limpieza_texto()
        self.parte_3_casos_practicos()
        self.parte_4_pipeline()
        
        # Conclusión
        self.conclusion()
        
        print("\n🎉 ¡Píldora completada!")
        self.pausar("Presiona Enter para volver al menú...")
    
    def ejecutar_demo_rapida(self):
        """Ejecuta una demostración rápida"""
        self.limpiar_pantalla()
        self.mostrar_titulo("⚡ DEMO RÁPIDA: DATA CLEANING AVANZADO")
        
        print("Versión condensada para demostración rápida")
        print()
        
        # Crear datos
        self.crear_datos_ejemplo()
        
        # Demo rápida de outliers
        print("🔍 DETECCIÓN DE OUTLIERS:")
        df_outliers = self.datos['outliers']
        z_scores = np.abs((df_outliers[['precio', 'cantidad']] - df_outliers[['precio', 'cantidad']].mean()) / df_outliers[['precio', 'cantidad']].std())
        outliers = (z_scores > 3).any(axis=1)
        print(f"Outliers detectados: {outliers.sum()}")
        print()
        
        # Demo rápida de limpieza de texto
        print("🧹 LIMPIEZA DE TEXTO:")
        df_texto = self.datos['texto']
        
        def limpiar_telefono_rapido(telefono):
            numeros = re.sub(r'[^\d]', '', str(telefono))
            if len(numeros) == 9:
                return f"+34-{numeros[:3]}-{numeros[3:6]}-{numeros[6:9]}"
            return None
        
        telefonos_limpios = df_texto['telefono'].apply(limpiar_telefono_rapido)
        print(f"Teléfonos válidos: {telefonos_limpios.notna().sum()}")
        print()
        
        # Demo rápida de pipeline
        print("⚙️ PIPELINE AUTOMATIZADO:")
        df_demo = pd.DataFrame({
            'id': range(1, 21),
            'nombre': [f'Usuario_{i}' for i in range(1, 21)],
            'edad': np.random.normal(35, 10, 20)
        })
        df_demo = df_demo.drop_duplicates()
        print(f"Pipeline completado: {len(df_demo)} filas procesadas")
        print()
        
        print("✅ Demo completada!")
        self.pausar("Presiona Enter para volver al menú...")
    
    def menu_principal(self):
        """Menú principal de la píldora"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_titulo("🎯 PÍLDORA: DATA CLEANING AVANZADO EN PYTHON")
            
            print("Selecciona una opción:")
            print("1. 🚀 Píldora completa (30 min)")
            print("2. ⚡ Demo rápida (10 min)")
            print("3. 🔍 Solo detección de outliers")
            print("4. 🧹 Solo limpieza de texto")
            print("5. 🎯 Solo casos prácticos")
            print("6. ⚙️ Solo pipeline automatizado")
            print("7. 📊 Ver datos disponibles")
            print("8. ❌ Salir")
            print()
            
            opcion = input("Ingresa tu opción (1-8): ").strip()
            
            if opcion == "1":
                self.ejecutar_presentacion_completa()
            elif opcion == "2":
                self.ejecutar_demo_rapida()
            elif opcion == "3":
                self.crear_datos_ejemplo()
                self.parte_1_outliers()
            elif opcion == "4":
                self.crear_datos_ejemplo()
                self.parte_2_limpieza_texto()
            elif opcion == "5":
                self.crear_datos_ejemplo()
                self.parte_3_casos_practicos()
            elif opcion == "6":
                self.crear_datos_ejemplo()
                self.parte_4_pipeline()
            elif opcion == "7":
                self.mostrar_datos()
            elif opcion == "8":
                print("¡Hasta luego! 👋")
                break
            else:
                print("❌ Opción no válida. Intenta de nuevo.")
                self.pausar("Presiona Enter para continuar...")
    
    def mostrar_datos(self):
        """Muestra información sobre los datos disponibles"""
        self.limpiar_pantalla()
        self.mostrar_titulo("📊 DATOS DISPONIBLES")
        
        if not self.datos:
            self.crear_datos_ejemplo()
        
        for nombre, df in self.datos.items():
            print(f"📦 {nombre.upper()}:")
            print(f"  Filas: {len(df)}")
            print(f"  Columnas: {len(df.columns)}")
            print(f"  Columnas: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
            print()
        
        self.pausar("Presiona Enter para volver al menú...")
    
    def ejecutar(self):
        """Ejecuta la píldora"""
        print("🎯 Iniciando Píldora de Data Cleaning Avanzado...")
        self.crear_datos_ejemplo()
        self.menu_principal()

def main():
    """Función principal"""
    try:
        pildora = PildoraDataCleaning()
        pildora.ejecutar()
    except KeyboardInterrupt:
        print("\n\n👋 Píldora interrumpida. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error durante la píldora: {e}")
        print("Por favor, verifica que todas las dependencias estén instaladas.")

if __name__ == "__main__":
    main()
