
"""
🎯 Píldora Interactiva: Data Cleaning Avanzado en Python
========================================================

Script principal para la presentación interactiva de la píldora.
Incluye menú de navegación, ejemplos en vivo y visualizaciones.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
import sys
import importlib.util
warnings.filterwarnings('ignore')

# Configurar visualizaciones
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Función para importar módulos con nombres que empiezan con números
def importar_modulo(nombre_archivo, nombre_modulo):
    """Importa un módulo desde un archivo con nombre que empieza con número"""
    try:
        spec = importlib.util.spec_from_file_location(nombre_modulo, nombre_archivo)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        return modulo
    except Exception as e:
        print(f"❌ Error importando {nombre_archivo}: {e}")
        return None

# Importar módulos de la píldora
try:
    # Importar módulos usando importlib
    deteccion_outliers = importar_modulo('01_deteccion_outliers.py', 'deteccion_outliers')
    limpieza_texto = importar_modulo('02_limpieza_texto.py', 'limpieza_texto')
    casos_practicos = importar_modulo('03_casos_practicos.py', 'casos_practicos')
    pipeline_automatizado = importar_modulo('04_pipeline_automatizado.py', 'pipeline_automatizado')
    
    # Verificar que todos los módulos se importaron correctamente
    if not all([deteccion_outliers, limpieza_texto, casos_practicos, pipeline_automatizado]):
        raise ImportError("No se pudieron importar todos los módulos necesarios")
        
    # Extraer las funciones y clases necesarias
    crear_datos_ejemplo = deteccion_outliers.crear_datos_ejemplo
    detectar_outliers_zscore = deteccion_outliers.detectar_outliers_zscore
    detectar_outliers_iqr = deteccion_outliers.detectar_outliers_iqr
    detectar_outliers_isolation_forest = deteccion_outliers.detectar_outliers_isolation_forest
    comparar_metodos_outliers = deteccion_outliers.comparar_metodos_outliers
    visualizar_outliers = deteccion_outliers.visualizar_outliers
    
    LimpiadorTexto = limpieza_texto.LimpiadorTexto
    crear_datos_sucios = limpieza_texto.crear_datos_sucios
    demostrar_limpieza_telefonos = limpieza_texto.demostrar_limpieza_telefonos
    demostrar_limpieza_emails = limpieza_texto.demostrar_limpieza_emails
    demostrar_limpieza_nombres = limpieza_texto.demostrar_limpieza_nombres
    demostrar_limpieza_html = limpieza_texto.demostrar_limpieza_html
    
    LimpiadorEcommerce = casos_practicos.LimpiadorEcommerce
    LimpiadorTemporal = casos_practicos.LimpiadorTemporal
    crear_datos_ecommerce_sucios = casos_practicos.crear_datos_ecommerce_sucios
    crear_datos_temporales_sucios = casos_practicos.crear_datos_temporales_sucios
    caso_ecommerce = casos_practicos.caso_ecommerce
    caso_temporal = casos_practicos.caso_temporal
    
    DataCleaner = pipeline_automatizado.DataCleaner
    ValidadorCalidad = pipeline_automatizado.ValidadorCalidad
    crear_datos_demo = pipeline_automatizado.crear_datos_demo
    demostrar_pipeline = pipeline_automatizado.demostrar_pipeline
    
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Asegúrate de que todos los archivos estén en el mismo directorio")
    sys.exit(1)

class PresentacionInteractiva:
    """Clase principal para manejar la presentación interactiva"""
    
    def __init__(self):
        self.datos_cargados = {}
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
    
    def cargar_datos_demo(self):
        """Carga los datasets de demostración"""
        print("📊 Cargando datasets de demostración...")
        
        try:
            # Cargar datasets desde archivos CSV
            self.datos_cargados = {
                'ecommerce': pd.read_csv('datos_ejemplo/ecommerce_sucio.csv'),
                'clientes': pd.read_csv('datos_ejemplo/clientes_sucio.csv'),
                'temporal': pd.read_csv('datos_ejemplo/temporal_sucio.csv'),
                'outliers': pd.read_csv('datos_ejemplo/outliers_demo.csv')
            }
            
            print("✅ Datasets cargados exitosamente:")
            for nombre, df in self.datos_cargados.items():
                print(f"  📦 {nombre}: {len(df)} filas, {len(df.columns)} columnas")
            
        except FileNotFoundError:
            print("⚠️ Archivos de datos no encontrados. Creando datasets...")
            # Crear datasets si no existen
            from datos_ejemplo.crear_datasets_demo import guardar_datasets
            guardar_datasets()
            self.cargar_datos_demo()
    
    def introduccion(self):
        """Introducción de la presentación"""
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
        
        # Usar datos de outliers
        df = self.datos_cargados['outliers']
        columnas_numericas = ['precio', 'cantidad', 'descuento', 'edad_cliente', 'satisfaccion']
        
        print(f"📊 Dataset: {len(df)} registros")
        print(f"📈 Columnas numéricas: {', '.join(columnas_numericas)}")
        print()
        
        # Mostrar estadísticas básicas
        print("📈 ESTADÍSTICAS BÁSICAS:")
        print(df[columnas_numericas].describe().round(2))
        print()
        
        # Comparar métodos
        print("🔍 COMPARANDO MÉTODOS DE DETECCIÓN:")
        df_comparacion = comparar_metodos_outliers(df, columnas_numericas)
        
        print("\n💡 CUÁNDO USAR CADA MÉTODO:")
        print("• Z-Score: Datos normalmente distribuidos")
        print("• IQR: Datos con distribución sesgada")
        print("• Isolation Forest: Múltiples variables (recomendado)")
        print()
        
        # Crear visualizaciones
        print("📊 CREANDO VISUALIZACIONES...")
        self.crear_visualizacion_outliers(df_comparacion, columnas_numericas)
        
        # Guardar resultados
        self.resultados['outliers'] = df_comparacion
        
        self.pausar("Presiona Enter para continuar...")
        return df_comparacion
    
    def parte_2_limpieza_texto(self):
        """Parte 2: Limpieza de Texto"""
        self.limpiar_pantalla()
        self.mostrar_titulo("🧹 PARTE 2: LIMPIEZA DE TEXTO CON REGEX")
        
        print("Los datos de texto son los más sucios. Vamos a ver cómo")
        print("limpiarlos usando expresiones regulares y técnicas avanzadas.")
        print()
        
        # Usar datos de clientes
        df = self.datos_cargados['clientes']
        limpiador = LimpiadorTexto()
        
        print("📞 LIMPIEZA DE TELÉFONOS:")
        df['telefono_limpio'] = df['telefono'].apply(limpiador.limpiar_telefono)
        print(f"Teléfonos válidos: {df['telefono_limpio'].notna().sum()}/{len(df)}")
        print()
        
        print("📧 LIMPIEZA DE EMAILS:")
        df['email_limpio'] = df['email'].apply(limpiador.limpiar_email)
        print(f"Emails válidos: {df['email_limpio'].notna().sum()}/{len(df)}")
        print()
        
        print("👤 LIMPIEZA DE NOMBRES:")
        df['nombre_limpio'] = df['nombre'].apply(limpiador.limpiar_nombre)
        print(f"Nombres válidos: {df['nombre_limpio'].notna().sum()}/{len(df)}")
        print()
        
        print("🏠 LIMPIEZA DE DIRECCIONES:")
        df['direccion_limpia'] = df['direccion'].apply(limpiador.limpiar_direccion)
        print(f"Direcciones válidas: {df['direccion_limpia'].notna().sum()}/{len(df)}")
        print()
        
        print("🔧 PATRONES REGEX CLAVE:")
        print("• Teléfonos: r'^(\\+34|0034|34)?[6-9]\\d{8}$'")
        print("• Emails: r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'")
        print("• HTML: r'<[^>]+>' (eliminar etiquetas)")
        print()
        
        # Crear visualizaciones
        print("📊 CREANDO VISUALIZACIONES...")
        self.crear_visualizacion_texto(df)
        
        # Guardar resultados
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
        
        df_ecommerce = self.datos_cargados['ecommerce']
        limpiador_ecommerce = LimpiadorEcommerce()
        
        # Aplicar limpiezas
        df_ecommerce['precio_normalizado'] = df_ecommerce['precio'].apply(limpiador_ecommerce.normalizar_precio)
        df_ecommerce['categoria_limpia'] = df_ecommerce['categoria'].apply(limpiador_ecommerce.limpiar_categoria)
        df_ecommerce['descripcion_limpia'] = df_ecommerce['descripcion'].apply(limpiador_ecommerce.limpiar_descripcion)
        
        print(f"Precios normalizados: {df_ecommerce['precio_normalizado'].notna().sum()}/{len(df_ecommerce)}")
        print(f"Categorías únicas: {df_ecommerce['categoria_limpia'].nunique()}")
        print()
        
        # Caso Temporal
        print("⏰ CASO 2: DATOS TEMPORALES")
        print("-" * 40)
        print("Problemas típicos:")
        print("• Timestamps en diferentes formatos")
        print("• Zonas horarias inconsistentes")
        print("• Gaps temporales")
        print()
        
        df_temporal = self.datos_cargados['temporal']
        limpiador_temporal = LimpiadorTemporal()
        
        # Parsear fechas
        df_temporal['timestamp_parsed'] = df_temporal['timestamp'].apply(limpiador_temporal.parsear_fecha_flexible)
        print(f"Fechas parseadas: {df_temporal['timestamp_parsed'].notna().sum()}/{len(df_temporal)}")
        print()
        
        print("💡 LECCIONES CLAVE:")
        print("• E-commerce: Normalizar monedas y categorías")
        print("• Temporal: Detectar frecuencia y rellenar gaps")
        print("• Siempre validar antes de procesar")
        print()
        
        # Crear visualizaciones para casos prácticos
        print("📊 CREANDO VISUALIZACIONES...")
        self.crear_visualizacion_casos_practicos(df_ecommerce, df_temporal)
        
        # Guardar resultados
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
        
        # Crear datos de demostración
        df_demo = crear_datos_demo()
        print(f"📊 Datos de demostración: {len(df_demo)} filas")
        print(f"❌ Valores nulos: {df_demo.isnull().sum().sum()}")
        print(f"🔄 Duplicados: {df_demo.duplicated().sum()}")
        print()
        
        # Configurar pipeline
        config = {
            'eliminar_duplicados': True,
            'manejar_nulos': True,
            'estandarizar_texto': True,
            'detectar_outliers': True,
            'validar_formatos': True,
            'metodo_imputacion': 'median',
            'umbral_outliers': 2.5
        }
        
        # Crear limpiador
        limpiador = DataCleaner(config)
        
        # Aplicar limpieza
        print("🚀 Ejecutando pipeline...")
        df_limpio = limpiador.fit_transform(df_demo)
        
        print(f"✅ Pipeline completado:")
        print(f"  📊 Filas finales: {len(df_limpio)}")
        print(f"  ❌ Valores nulos: {df_limpio.isnull().sum().sum()}")
        print(f"  🔄 Duplicados: {df_limpio.duplicated().sum()}")
        print()
        
        # Generar reporte
        reporte = limpiador.generar_reporte()
        print("📊 REPORTE DE LIMPIEZA:")
        print(f"  🗑️ Filas eliminadas: {reporte['resumen']['filas_eliminadas']}")
        print(f"  🔧 Nulos imputados: {reporte['resumen']['nulos_imputados']}")
        print(f"  ⚙️ Transformaciones: {reporte['resumen']['transformaciones_aplicadas']}")
        print()
        
        # Crear visualizaciones del pipeline
        print("📊 CREANDO VISUALIZACIONES...")
        self.crear_visualizacion_pipeline(df_demo, df_limpio, reporte)
        
        # Guardar resultados
        self.resultados['pipeline'] = {
            'datos_limpios': df_limpio,
            'reporte': reporte
        }
        
        self.pausar("Presiona Enter para continuar...")
        return df_limpio, reporte
    
    def conclusion(self):
        """Conclusión de la presentación"""
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
    
    def menu_principal(self):
        """Menú principal de la presentación"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_titulo("🎯 PÍLDORA: DATA CLEANING AVANZADO EN PYTHON")
            
            print("Selecciona una opción:")
            print("1. 🚀 Presentación completa (30 min)")
            print("2. ⚡ Demo rápida (10 min)")
            print("3. 🔍 Solo detección de outliers")
            print("4. 🧹 Solo limpieza de texto")
            print("5. 🎯 Solo casos prácticos")
            print("6. ⚙️ Solo pipeline automatizado")
            print("7. 📊 Ver datasets disponibles")
            print("8. ❌ Salir")
            print()
            
            opcion = input("Ingresa tu opción (1-8): ").strip()
            
            if opcion == "1":
                self.ejecutar_presentacion_completa()
            elif opcion == "2":
                self.ejecutar_demo_rapida()
            elif opcion == "3":
                self.parte_1_outliers()
            elif opcion == "4":
                self.parte_2_limpieza_texto()
            elif opcion == "5":
                self.parte_3_casos_practicos()
            elif opcion == "6":
                self.parte_4_pipeline()
            elif opcion == "7":
                self.mostrar_datasets()
            elif opcion == "8":
                print("¡Hasta luego! 👋")
                break
            else:
                print("❌ Opción no válida. Intenta de nuevo.")
                self.pausar("Presiona Enter para continuar...")
    
    def ejecutar_presentacion_completa(self):
        """Ejecuta la presentación completa"""
        print("🚀 INICIANDO PRESENTACIÓN COMPLETA")
        print("Duración estimada: 30 minutos")
        print()
        
        # Cargar datos
        self.cargar_datos_demo()
        
        # Introducción
        self.introduccion()
        
        # Partes de la presentación
        self.parte_1_outliers()
        self.parte_2_limpieza_texto()
        self.parte_3_casos_practicos()
        self.parte_4_pipeline()
        
        # Conclusión
        self.conclusion()
        
        print("\n🎉 ¡Presentación completada!")
        self.pausar("Presiona Enter para volver al menú...")
    
    def ejecutar_demo_rapida(self):
        """Ejecuta una demostración rápida"""
        self.limpiar_pantalla()
        self.mostrar_titulo("⚡ DEMO RÁPIDA: DATA CLEANING AVANZADO")
        
        print("Versión condensada para demostración rápida")
        print()
        
        # Cargar datos
        self.cargar_datos_demo()
        
        # Demo rápida de outliers
        print("🔍 DETECCIÓN DE OUTLIERS:")
        df_outliers = self.datos_cargados['outliers']
        df_resultado = detectar_outliers_isolation_forest(df_outliers, ['precio', 'cantidad'])
        print(f"Outliers detectados: {df_resultado['outlier_isolation'].sum()}")
        print()
        
        # Demo rápida de limpieza de texto
        print("🧹 LIMPIEZA DE TEXTO:")
        limpiador = LimpiadorTexto()
        df_texto = self.datos_cargados['clientes']
        df_texto['telefono_limpio'] = df_texto['telefono'].apply(limpiador.limpiar_telefono)
        print(f"Teléfonos válidos: {df_texto['telefono_limpio'].notna().sum()}")
        print()
        
        # Demo rápida de pipeline
        print("⚙️ PIPELINE AUTOMATIZADO:")
        df_demo = crear_datos_demo()
        cleaner = DataCleaner()
        df_limpio = cleaner.fit_transform(df_demo)
        print(f"Pipeline completado: {len(df_limpio)} filas procesadas")
        print()
        
        print("✅ Demo completada!")
        self.pausar("Presiona Enter para volver al menú...")
    
    def mostrar_datasets(self):
        """Muestra información sobre los datasets disponibles"""
        self.limpiar_pantalla()
        self.mostrar_titulo("📊 DATASETS DISPONIBLES")
        
        if not self.datos_cargados:
            self.cargar_datos_demo()
        
        for nombre, df in self.datos_cargados.items():
            print(f"📦 {nombre.upper()}:")
            print(f"  Filas: {len(df)}")
            print(f"  Columnas: {len(df.columns)}")
            print(f"  Columnas: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
            print()
        
        self.pausar("Presiona Enter para volver al menú...")
    
    def crear_visualizacion_outliers(self, df, columnas):
        """Crea visualizaciones para la detección de outliers"""
        try:
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            axes = axes.ravel()
            
            # Métodos de detección
            metodos = ['zscore', 'iqr', 'isolation']
            
            for i, metodo in enumerate(metodos):
                if f'outlier_{metodo}' in df.columns:
                    # Box plot para cada método
                    ax = axes[i]
                    datos_por_columna = []
                    etiquetas = []
                    
                    for col in columnas[:4]:  # Máximo 4 columnas
                        datos_por_columna.append(df[col])
                        etiquetas.append(col)
                    
                    bp = ax.boxplot(datos_por_columna, labels=etiquetas, patch_artist=True)
                    ax.set_title(f'Box Plot - Método {metodo.upper()}')
                    ax.set_ylabel('Valores')
                    ax.tick_params(axis='x', rotation=45)
                    
                    # Colorear outliers
                    for patch in bp['boxes']:
                        patch.set_facecolor('lightblue')
            
            # Scatter plot comparativo
            ax = axes[3]
            if 'outlier_isolation' in df.columns:
                outliers_mask = df['outlier_isolation']
                ax.scatter(df[~outliers_mask].index, df[~outliers_mask]['precio'], 
                          alpha=0.6, label='Normal', color='blue', s=20)
                ax.scatter(df[outliers_mask].index, df[outliers_mask]['precio'], 
                          alpha=0.8, label='Outlier', color='red', s=50)
                ax.set_title('Outliers en Precio (Isolation Forest)')
                ax.set_xlabel('Índice del registro')
                ax.set_ylabel('Precio')
                ax.legend()
                ax.grid(True, alpha=0.3)
            
            # Comparación de métodos
            ax = axes[4]
            if all(f'outlier_{metodo}' in df.columns for metodo in metodos):
                comparacion = []
                for metodo in metodos:
                    comparacion.append(df[f'outlier_{metodo}'].sum())
                
                ax.bar(metodos, comparacion, color=['skyblue', 'lightgreen', 'salmon'])
                ax.set_title('Comparación de Métodos de Detección')
                ax.set_ylabel('Número de Outliers Detectados')
                ax.tick_params(axis='x', rotation=45)
                
                # Agregar valores en las barras
                for i, v in enumerate(comparacion):
                    ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
            
            # Distribución de datos
            ax = axes[5]
            if 'precio' in df.columns:
                ax.hist(df['precio'], bins=30, alpha=0.7, color='lightcoral', edgecolor='black')
                ax.set_title('Distribución de Precios')
                ax.set_xlabel('Precio')
                ax.set_ylabel('Frecuencia')
                ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('visualizacion_outliers.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✅ Visualización guardada como 'visualizacion_outliers.png'")
            
        except Exception as e:
            print(f"⚠️ Error creando visualización: {e}")
    
    def crear_visualizacion_texto(self, df):
        """Crea visualizaciones para la limpieza de texto"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # Antes vs Después de limpieza de teléfonos
            ax = axes[0, 0]
            if 'telefono' in df.columns and 'telefono_limpio' in df.columns:
                antes = df['telefono'].notna().sum()
                despues = df['telefono_limpio'].notna().sum()
                
                ax.bar(['Antes', 'Después'], [antes, despues], 
                      color=['lightcoral', 'lightgreen'])
                ax.set_title('Limpieza de Teléfonos')
                ax.set_ylabel('Registros Válidos')
                
                # Agregar valores en las barras
                ax.text(0, antes + 1, str(antes), ha='center', va='bottom')
                ax.text(1, despues + 1, str(despues), ha='center', va='bottom')
            
            # Antes vs Después de limpieza de emails
            ax = axes[0, 1]
            if 'email' in df.columns and 'email_limpio' in df.columns:
                antes = df['email'].notna().sum()
                despues = df['email_limpio'].notna().sum()
                
                ax.bar(['Antes', 'Después'], [antes, despues], 
                      color=['lightcoral', 'lightgreen'])
                ax.set_title('Limpieza de Emails')
                ax.set_ylabel('Registros Válidos')
                
                # Agregar valores en las barras
                ax.text(0, antes + 1, str(antes), ha='center', va='bottom')
                ax.text(1, despues + 1, str(despues), ha='center', va='bottom')
            
            # Distribución de categorías limpias
            ax = axes[1, 0]
            if 'categoria_limpia' in df.columns:
                categorias = df['categoria_limpia'].value_counts()
                ax.pie(categorias.values, labels=categorias.index, autopct='%1.1f%%', startangle=90)
                ax.set_title('Distribución de Categorías Limpias')
            
            # Longitud de descripciones limpias
            ax = axes[1, 1]
            if 'descripcion_limpia' in df.columns:
                longitudes = df['descripcion_limpia'].str.len().dropna()
                ax.hist(longitudes, bins=20, alpha=0.7, color='lightblue', edgecolor='black')
                ax.set_title('Distribución de Longitudes de Descripciones')
                ax.set_xlabel('Longitud de Caracteres')
                ax.set_ylabel('Frecuencia')
                ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('visualizacion_texto.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✅ Visualización guardada como 'visualizacion_texto.png'")
            
        except Exception as e:
            print(f"⚠️ Error creando visualización: {e}")
    
    def crear_visualizacion_pipeline(self, df_antes, df_despues, reporte):
        """Crea visualizaciones para el pipeline automatizado"""
        try:
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            
            # Comparación de filas antes y después
            ax = axes[0, 0]
            filas_antes = len(df_antes)
            filas_despues = len(df_despues)
            filas_eliminadas = filas_antes - filas_despues
            
            ax.bar(['Antes', 'Después'], [filas_antes, filas_despues], 
                  color=['lightcoral', 'lightgreen'])
            ax.set_title('Filas Antes vs Después del Pipeline')
            ax.set_ylabel('Número de Filas')
            
            # Agregar valores
            ax.text(0, filas_antes + 1, str(filas_antes), ha='center', va='bottom')
            ax.text(1, filas_despues + 1, str(filas_despues), ha='center', va='bottom')
            
            # Valores nulos antes y después
            ax = axes[0, 1]
            nulos_antes = df_antes.isnull().sum().sum()
            nulos_despues = df_despues.isnull().sum().sum()
            
            ax.bar(['Antes', 'Después'], [nulos_antes, nulos_despues], 
                  color=['lightcoral', 'lightgreen'])
            ax.set_title('Valores Nulos Antes vs Después')
            ax.set_ylabel('Número de Valores Nulos')
            
            # Agregar valores
            ax.text(0, nulos_antes + 0.5, str(nulos_antes), ha='center', va='bottom')
            ax.text(1, nulos_despues + 0.5, str(nulos_despues), ha='center', va='bottom')
            
            # Duplicados eliminados
            ax = axes[0, 2]
            duplicados = df_antes.duplicated().sum()
            ax.bar(['Duplicados Eliminados'], [duplicados], color='orange')
            ax.set_title('Duplicados Eliminados')
            ax.set_ylabel('Número de Duplicados')
            ax.text(0, duplicados + 0.1, str(duplicados), ha='center', va='bottom')
            
            # Transformaciones aplicadas
            ax = axes[1, 0]
            if 'transformaciones_aplicadas' in reporte['resumen']:
                transformaciones = reporte['resumen']['transformaciones_aplicadas']
                ax.bar(['Transformaciones'], [transformaciones], color='purple')
                ax.set_title('Transformaciones Aplicadas')
                ax.set_ylabel('Número de Transformaciones')
                ax.text(0, transformaciones + 0.1, str(transformaciones), ha='center', va='bottom')
            
            # Calidad de datos (antes vs después)
            ax = axes[1, 1]
            calidad_antes = ((filas_antes - nulos_antes) / (filas_antes * len(df_antes.columns))) * 100
            calidad_despues = ((filas_despues - nulos_despues) / (filas_despues * len(df_despues.columns))) * 100
            
            ax.bar(['Antes', 'Después'], [calidad_antes, calidad_despues], 
                  color=['lightcoral', 'lightgreen'])
            ax.set_title('Calidad de Datos (%)')
            ax.set_ylabel('Porcentaje de Completitud')
            ax.set_ylim(0, 100)
            
            # Agregar valores
            ax.text(0, calidad_antes + 1, f'{calidad_antes:.1f}%', ha='center', va='bottom')
            ax.text(1, calidad_despues + 1, f'{calidad_despues:.1f}%', ha='center', va='bottom')
            
            # Resumen de mejoras
            ax = axes[1, 2]
            mejoras = [
                f'Filas eliminadas: {filas_eliminadas}',
                f'Nulos imputados: {nulos_antes - nulos_despues}',
                f'Duplicados: {duplicados}',
                f'Calidad: +{calidad_despues - calidad_antes:.1f}%'
            ]
            
            ax.text(0.1, 0.8, 'MEJORAS LOGRADAS:', fontsize=12, fontweight='bold', transform=ax.transAxes)
            for i, mejora in enumerate(mejoras):
                ax.text(0.1, 0.6 - i*0.15, mejora, fontsize=10, transform=ax.transAxes)
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            plt.tight_layout()
            plt.savefig('visualizacion_pipeline.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✅ Visualización guardada como 'visualizacion_pipeline.png'")
            
        except Exception as e:
            print(f"⚠️ Error creando visualización: {e}")
    
    def crear_visualizacion_casos_practicos(self, df_ecommerce, df_temporal):
        """Crea visualizaciones para los casos prácticos"""
        try:
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            
            # E-commerce: Precios normalizados
            ax = axes[0, 0]
            if 'precio_normalizado' in df_ecommerce.columns:
                precios = df_ecommerce['precio_normalizado'].dropna()
                ax.hist(precios, bins=20, alpha=0.7, color='lightblue', edgecolor='black')
                ax.set_title('Distribución de Precios Normalizados (USD)')
                ax.set_xlabel('Precio (USD)')
                ax.set_ylabel('Frecuencia')
                ax.grid(True, alpha=0.3)
            
            # E-commerce: Categorías limpias
            ax = axes[0, 1]
            if 'categoria_limpia' in df_ecommerce.columns:
                categorias = df_ecommerce['categoria_limpia'].value_counts()
                ax.pie(categorias.values, labels=categorias.index, autopct='%1.1f%%', startangle=90)
                ax.set_title('Distribución de Categorías Limpias')
            
            # E-commerce: Comparación antes/después
            ax = axes[0, 2]
            if 'precio' in df_ecommerce.columns and 'precio_normalizado' in df_ecommerce.columns:
                try:
                    # Extraer números de precios originales de forma más robusta
                    precios_originales = []
                    for precio_str in df_ecommerce['precio'].dropna():
                        # Buscar números en el string
                        import re
                        numeros = re.findall(r'[\d,\.]+', str(precio_str))
                        if numeros:
                            try:
                                # Convertir a float manejando formatos europeos/americanos
                                num_str = numeros[0].replace(',', '.') if ',' in numeros[0] and '.' not in numeros[0] else numeros[0].replace(',', '')
                                precios_originales.append(float(num_str))
                            except:
                                continue
                    
                    precios_limpios = df_ecommerce['precio_normalizado'].dropna().tolist()
                    
                    if precios_originales and precios_limpios:
                        ax.boxplot([precios_originales, precios_limpios], 
                                  labels=['Originales', 'Normalizados'])
                        ax.set_title('Comparación de Precios')
                        ax.set_ylabel('Precio')
                        ax.grid(True, alpha=0.3)
                    else:
                        ax.text(0.5, 0.5, 'No hay datos suficientes\npara comparar', 
                               ha='center', va='center', transform=ax.transAxes)
                        ax.set_title('Comparación de Precios')
                except Exception as e:
                    ax.text(0.5, 0.5, f'Error en comparación:\n{str(e)[:50]}...', 
                           ha='center', va='center', transform=ax.transAxes)
                    ax.set_title('Comparación de Precios')
            
            # Temporal: Serie temporal
            ax = axes[1, 0]
            if 'timestamp_parsed' in df_temporal.columns and 'temperatura' in df_temporal.columns:
                df_temp = df_temporal.dropna(subset=['timestamp_parsed', 'temperatura'])
                if len(df_temp) > 0:
                    ax.plot(df_temp['timestamp_parsed'], df_temp['temperatura'], 
                           marker='o', markersize=3, alpha=0.7)
                    ax.set_title('Serie Temporal de Temperatura')
                    ax.set_xlabel('Tiempo')
                    ax.set_ylabel('Temperatura (°C)')
                    ax.tick_params(axis='x', rotation=45)
                    ax.grid(True, alpha=0.3)
            
            # Temporal: Distribución de variables
            ax = axes[1, 1]
            if 'temperatura' in df_temporal.columns and 'humedad' in df_temporal.columns:
                ax.scatter(df_temporal['temperatura'], df_temporal['humedad'], 
                          alpha=0.6, color='green')
                ax.set_title('Temperatura vs Humedad')
                ax.set_xlabel('Temperatura (°C)')
                ax.set_ylabel('Humedad (%)')
                ax.grid(True, alpha=0.3)
            
            # Resumen de mejoras
            ax = axes[1, 2]
            mejoras = []
            
            if 'precio_normalizado' in df_ecommerce.columns:
                precios_validos = df_ecommerce['precio_normalizado'].notna().sum()
                mejoras.append(f'Precios normalizados: {precios_validos}')
            
            if 'categoria_limpia' in df_ecommerce.columns:
                categorias_unicas = df_ecommerce['categoria_limpia'].nunique()
                mejoras.append(f'Categorías únicas: {categorias_unicas}')
            
            if 'timestamp_parsed' in df_temporal.columns:
                fechas_parseadas = df_temporal['timestamp_parsed'].notna().sum()
                mejoras.append(f'Fechas parseadas: {fechas_parseadas}')
            
            mejoras.append('Datos listos para análisis')
            
            ax.text(0.1, 0.8, 'MEJORAS LOGRADAS:', fontsize=12, fontweight='bold', transform=ax.transAxes)
            for i, mejora in enumerate(mejoras):
                ax.text(0.1, 0.6 - i*0.1, mejora, fontsize=10, transform=ax.transAxes)
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            plt.tight_layout()
            plt.savefig('visualizacion_casos_practicos.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✅ Visualización guardada como 'visualizacion_casos_practicos.png'")
            
        except Exception as e:
            print(f"⚠️ Error creando visualización: {e}")
    
    def ejecutar(self):
        """Ejecuta la presentación interactiva"""
        print("🎯 Iniciando Píldora de Data Cleaning Avanzado...")
        self.cargar_datos_demo()
        self.menu_principal()

def main():
    """Función principal"""
    try:
        presentacion = PresentacionInteractiva()
        presentacion.ejecutar()
    except KeyboardInterrupt:
        print("\n\n👋 Presentación interrumpida. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error durante la presentación: {e}")
        print("Por favor, verifica que todos los archivos estén presentes.")

if __name__ == "__main__":
    main()
