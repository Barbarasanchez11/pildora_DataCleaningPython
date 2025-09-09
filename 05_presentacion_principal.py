"""
Píldora: Data Cleaning Avanzado en Python
==========================================

Archivo principal con guión completo de presentación
Incluye todos los ejemplos y casos prácticos integrados
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Importar módulos de la píldora
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

def introduccion():
    """Introducción de la presentación (2 minutos)"""
    print("PÍLDORA: DATA CLEANING AVANZADO EN PYTHON")
    print("=" * 60)
    print()
    print("¡Hola a todos! 👋")
    print()
    print("Mi compañero nos ha mostrado los fundamentos del data cleaning.")
    print("Ahora vamos a ver técnicas más avanzadas que usarás en proyectos")
    print("reales del día a día. Estas son las herramientas que realmente")
    print("marcan la diferencia en la calidad de tus análisis.")
    print()
    print("AGENDA DE HOY:")
    print("• Técnicas Avanzadas de Limpieza (15 min)")
    print("• Casos Prácticos Complejos (10 min)")
    print("• Automatización y Buenas Prácticas (5 min)")
    print()
    input("Presiona Enter para continuar...")

def parte_1_deteccion_outliers():
    """Parte 1: Detección Inteligente de Outliers (8 min)"""
    print("\n" + "="*60)
    print("PARTE 1: DETECCIÓN INTELIGENTE DE OUTLIERS")
    print("="*60)
    print()
    print("Los outliers pueden arruinar tu análisis. Vamos a ver cómo")
    print("detectarlos de manera inteligente usando diferentes métodos.")
    print()
    
    # Crear datos de ejemplo
    print("Creando dataset de ejemplo con outliers")
    df = crear_datos_ejemplo()
    columnas_numericas = ['precio', 'cantidad', 'descuento', 'edad_cliente']
    
    print(f"Dataset: {len(df)} registros")
    print(f"Columnas: {', '.join(columnas_numericas)}")
    print()
    
    # Mostrar estadísticas básicas
    print("ESTADÍSTICAS BÁSICAS:")
    print(df[columnas_numericas].describe().round(2))
    print()
    
    # Comparar métodos
    print(" COMPARANDO MÉTODOS DE DETECCIÓN:")
    df_comparacion = comparar_metodos_outliers(df, columnas_numericas)
    
    print("CUÁNDO USAR CADA MÉTODO:")
    print("• Z-Score: Datos normalmente distribuidos")
    print("• IQR: Datos con distribución sesgada")
    print("• Isolation Forest: Múltiples variables (recomendado)")
    print()
    
    input("Presiona Enter para continuar...")
    return df_comparacion

def parte_2_limpieza_texto():
    """Parte 2: Regex para Limpieza de Texto (7 min)"""
    print("\n" + "="*60)
    print("🧹 PARTE 2: LIMPIEZA DE TEXTO CON REGEX")
    print("="*60)
    print()
    print("Los datos de texto son los más sucios. Vamos a ver cómo")
    print("limpiarlos usando expresiones regulares y técnicas avanzadas.")
    print()
    
    # Demostrar limpieza de teléfonos
    print("LIMPIEZA DE TELÉFONOS:")
    df_telefonos = demostrar_limpieza_telefonos()
    print()
    
    # Demostrar limpieza de emails
    print("LIMPIEZA DE EMAILS:")
    df_emails = demostrar_limpieza_emails()
    print()
    
    # Demostrar limpieza de nombres
    print("LIMPIEZA DE NOMBRES:")
    df_nombres = demostrar_limpieza_nombres()
    print()
    
    # Demostrar limpieza de HTML
    print("LIMPIEZA DE HTML:")
    df_html = demostrar_limpieza_html()
    print()
    
    print("PATRONES REGEX CLAVE:")
    print("• Teléfonos: r'^(\+34|0034|34)?[6-9]\d{8}$'")
    print("• Emails: r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'")
    print("• HTML: r'<[^>]+>' (eliminar etiquetas)")
    print()
    
    input("Presiona Enter para continuar...")
    return df_telefonos, df_emails, df_nombres, df_html

def parte_3_casos_practicos():
    """Parte 3: Casos Prácticos Complejos (10 min)"""
    print("\n" + "="*60)
    print("PARTE 3: CASOS PRÁCTICOS COMPLEJOS")
    print("="*60)
    print()
    print("Ahora vamos a ver casos reales que encontrarás en el trabajo:")
    print("datos de e-commerce y series temporales.")
    print()
    
    # Caso E-commerce
    print("CASO 1: DATASET DE E-COMMERCE")
    print("-" * 40)
    print("Problemas típicos:")
    print("• Precios en diferentes monedas")
    print("• Categorías inconsistentes")
    print("• Descripciones con HTML")
    print()
    
    df_ecommerce = caso_ecommerce()
    print()
    
    # Caso Temporal
    print("CASO 2: DATOS TEMPORALES")
    print("-" * 40)
    print("Problemas típicos:")
    print("• Timestamps en diferentes formatos")
    print("• Zonas horarias inconsistentes")
    print("• Gaps temporales")
    print()
    
    df_temporal = caso_temporal()
    print()
    
    print("LECCIONES CLAVE:")
    print("• E-commerce: Normalizar monedas y categorías")
    print("• Temporal: Detectar frecuencia y rellenar gaps")
    print("• Siempre validar antes de procesar")
    print()
    
    input("Presiona Enter para continuar...")
    return df_ecommerce, df_temporal

def parte_4_pipeline_automatizado():
    """Parte 4: Pipeline Automatizado (5 min)"""
    print("\n" + "="*60)
    print("PARTE 4: PIPELINE AUTOMATIZADO")
    print("="*60)
    print()
    print("La clave del éxito: automatizar y documentar todo.")
    print("Vamos a ver cómo crear un pipeline reutilizable.")
    print()
    
    # Demostrar pipeline
    print("DEMOSTRANDO PIPELINE AUTOMATIZADO:")
    df_limpio, reporte = demostrar_pipeline()
    print()
    
    print("CARACTERÍSTICAS DEL PIPELINE:")
    print("• Configuración flexible")
    print("• Logging detallado")
    print("• Validación automática")
    print("• Reportes documentados")
    print("• Manejo de errores robusto")
    print()
    
    print("MEJORES PRÁCTICAS:")
    print("• Documenta todas las decisiones")
    print("• Prueba con datos reales")
    print("• Mantén logs de transformaciones")
    print("• Valida calidad automáticamente")
    print()
    
    input("Presiona Enter para continuar...")
    return df_limpio, reporte

def conclusion():
    """Conclusión de la presentación"""
    print("\n" + "="*60)
    print("CONCLUSIÓN Y PRÓXIMOS PASOS")
    print("="*60)
    print()
    print("¡Excelente trabajo! Hemos cubierto las técnicas más importantes")
    print("de data cleaning avanzado en Python.")
    print()
    print("RESUMEN DE LO APRENDIDO:")
    print("Detección inteligente de outliers")
    print("Limpieza de texto con regex")
    print("Casos prácticos reales")
    print("Pipeline automatizado")
    print("Buenas prácticas de documentación")
    print()
    print(" PRÓXIMOS PASOS:")
    print("1. Practica con tus propios datasets")
    print("2. Adapta el pipeline a tus necesidades")
    print("3. Comparte conocimiento con tu equipo")
    print("4. Mantén actualizada tu documentación")
    print()
    print(" ¿PREGUNTAS?")
    print("Estoy aquí para ayudarte con cualquier duda.")
    print()
    print("¡Gracias por tu atención!")

def ejecutar_presentacion_completa():
    """Ejecuta la presentación completa"""
    print("INICIANDO PRESENTACIÓN COMPLETA")
    print("=" * 60)
    print()
    print("Esta es la píldora completa de Data Cleaning Avanzado en Python.")
    print("Duración estimada: 30 minutos")
    print()
    
    # Introducción
    introduccion()
    
    # Parte 1: Detección de Outliers
    df_outliers = parte_1_deteccion_outliers()
    
    # Parte 2: Limpieza de Texto
    df_telefonos, df_emails, df_nombres, df_html = parte_2_limpieza_texto()
    
    # Parte 3: Casos Prácticos
    df_ecommerce, df_temporal = parte_3_casos_practicos()
    
    # Parte 4: Pipeline Automatizado
    df_limpio, reporte = parte_4_pipeline_automatizado()
    
    # Conclusión
    conclusion()
    
    return {
        'outliers': df_outliers,
        'texto': (df_telefonos, df_emails, df_nombres, df_html),
        'casos': (df_ecommerce, df_temporal),
        'pipeline': (df_limpio, reporte)
    }

def ejecutar_demo_rapida():
    """Ejecuta una demostración rápida (10 minutos)"""
    print("⚡ DEMO RÁPIDA: DATA CLEANING AVANZADO")
    print("=" * 50)
    print()
    print("Versión condensada para demostración rápida")
    print()
    
    # Crear datos de ejemplo
    print("Creando datos de ejemplo...")
    df = crear_datos_ejemplo()
    
    # Detección de outliers
    print("Detectando outliers...")
    df_outliers = detectar_outliers_isolation_forest(df, ['precio', 'cantidad'])
    print(f"Outliers detectados: {df_outliers['outlier_isolation'].sum()}")
    
    # Limpieza de texto
    print("Limpiando texto...")
    limpiador = LimpiadorTexto()
    df_texto = crear_datos_sucios()
    df_texto['telefono_limpio'] = df_texto['telefono'].apply(limpiador.limpiar_telefono)
    print(f"Teléfonos válidos: {df_texto['telefono_limpio'].notna().sum()}")
    
    # Pipeline automatizado
    print("Ejecutando pipeline...")
    df_demo = crear_datos_demo()
    cleaner = DataCleaner()
    df_limpio = cleaner.fit_transform(df_demo)
    print(f"Pipeline completado: {len(df_limpio)} filas procesadas")
    
    print("Demo completada!")
    return df_limpio

def main():
    """Función principal con menú de opciones"""
    print("PÍLDORA: DATA CLEANING AVANZADO EN PYTHON")
    print("=" * 60)
    print()
    print("Selecciona una opción:")
    print("1. Presentación completa (30 min)")
    print("2. Demo rápida (10 min)")
    print("3. Solo detección de outliers")
    print("4. Solo limpieza de texto")
    print("5. Solo casos prácticos")
    print("6. Solo pipeline automatizado")
    print()
    
    opcion = input("Ingresa tu opción (1-6): ").strip()
    
    if opcion == "1":
        resultado = ejecutar_presentacion_completa()
    elif opcion == "2":
        resultado = ejecutar_demo_rapida()
    elif opcion == "3":
        print("DETECCIÓN DE OUTLIERS")
        df = crear_datos_ejemplo()
        resultado = comparar_metodos_outliers(df, ['precio', 'cantidad', 'descuento'])
    elif opcion == "4":
        print("LIMPIEZA DE TEXTO")
        resultado = demostrar_limpieza_telefonos()
    elif opcion == "5":
        print("CASOS PRÁCTICOS")
        resultado = caso_ecommerce()
    elif opcion == "6":
        print("PIPELINE AUTOMATIZADO")
        resultado = demostrar_pipeline()
    else:
        print("Opción no válida. Ejecutando demo rápida...")
        resultado = ejecutar_demo_rapida()
    
    return resultado

if __name__ == "__main__":
    # Ejecutar presentación
    resultado = main()
