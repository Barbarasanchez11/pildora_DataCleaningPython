
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
warnings.filterwarnings('ignore')

# Configurar visualizaciones
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Importar módulos de la píldora
try:
    from deteccion_outliers import (
        crear_datos_ejemplo, detectar_outliers_zscore, 
        detectar_outliers_iqr, detectar_outliers_isolation_forest,
        comparar_metodos_outliers, visualizar_outliers
    )
    from limpieza_texto import (
        LimpiadorTexto, crear_datos_sucios,
        demostrar_limpieza_telefonos, demostrar_limpieza_emails,
        demostrar_limpieza_nombres, demostrar_limpieza_html
    )
    from casos_practicos import (
        LimpiadorEcommerce, LimpiadorTemporal,
        crear_datos_ecommerce_sucios, crear_datos_temporales_sucios,
        caso_ecommerce, caso_temporal
    )
    from pipeline_automatizado import (
        DataCleaner, ValidadorCalidad, crear_datos_demo, demostrar_pipeline
    )
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
