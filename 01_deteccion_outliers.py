"""
Detección Avanzada de Outliers en Python
========================================

Este módulo demuestra diferentes técnicas para detectar outliers:
1. Métodos estadísticos tradicionales (Z-score, IQR)
2. Isolation Forest para outliers multivariados
3. Comparación de métodos y cuándo usar cada uno
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuración para visualizaciones
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def crear_datos_ejemplo():
    """Crea un dataset de ejemplo con outliers para demostración"""
    np.random.seed(42)
    
    # Datos normales
    datos_normales = {
        'precio': np.random.normal(50, 15, 200),
        'cantidad': np.random.poisson(5, 200),
        'descuento': np.random.beta(2, 5, 200),
        'edad_cliente': np.random.normal(35, 10, 200)
    }
    
    # Agregar outliers intencionalmente
    outliers = {
        'precio': [1000, 2000, 5, 3000],
        'cantidad': [1, 1, 50, 1],
        'descuento': [0.9, 0.95, 0.1, 0.99],
        'edad_cliente': [120, 5, 200, 0]
    }
    
    df_normales = pd.DataFrame(datos_normales)
    df_outliers = pd.DataFrame(outliers)
    
    df_completo = pd.concat([df_normales, df_outliers], ignore_index=True)
    df_completo['id'] = range(len(df_completo))
    
    return df_completo

def detectar_outliers_zscore(df, columnas, threshold=3):
    """
    Detecta outliers usando Z-score
    
    Args:
        df: DataFrame con los datos
        columnas: Lista de columnas a analizar
        threshold: Umbral de Z-score (default: 3)
    
    Returns:
        DataFrame con columna 'outlier_zscore' indicando outliers
    """
    df_resultado = df.copy()
    df_resultado['outlier_zscore'] = False
    
    for col in columnas:
        z_scores = np.abs(stats.zscore(df[col].dropna()))
        outliers_mask = z_scores > threshold
        df_resultado.loc[outliers_mask, 'outlier_zscore'] = True
    
    return df_resultado

def detectar_outliers_iqr(df, columnas, factor=1.5):
    """
    Detecta outliers usando IQR (Interquartile Range)
    
    Args:
        df: DataFrame con los datos
        columnas: Lista de columnas a analizar
        factor: Factor multiplicador para IQR (default: 1.5)
    
    Returns:
        DataFrame con columna 'outlier_iqr' indicando outliers
    """
    df_resultado = df.copy()
    df_resultado['outlier_iqr'] = False
    
    for col in columnas:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        
        outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        df_resultado.loc[outliers_mask, 'outlier_iqr'] = True
    
    return df_resultado

def detectar_outliers_isolation_forest(df, columnas, contamination=0.1):
    """
    Detecta outliers usando Isolation Forest (mejor para múltiples variables)
    
    Args:
        df: DataFrame con los datos
        columnas: Lista de columnas a analizar
        contamination: Proporción esperada de outliers (default: 0.1)
    
    Returns:
        DataFrame con columna 'outlier_isolation' indicando outliers
    """
    df_resultado = df.copy()
    
    # Preparar datos para Isolation Forest
    datos_para_analisis = df[columnas].dropna()
    
    if len(datos_para_analisis) == 0:
        df_resultado['outlier_isolation'] = False
        return df_resultado
    
    # Aplicar Isolation Forest
    iso_forest = IsolationForest(
        contamination=contamination, 
        random_state=42,
        n_estimators=100
    )
    
    outliers = iso_forest.fit_predict(datos_para_analisis)
    
    # Crear máscara de outliers
    df_resultado['outlier_isolation'] = False
    indices_validos = datos_para_analisis.index
    df_resultado.loc[indices_validos[outliers == -1], 'outlier_isolation'] = True
    
    return df_resultado

def comparar_metodos_outliers(df, columnas):
    """
    Compara diferentes métodos de detección de outliers
    
    Args:
        df: DataFrame con los datos
        columnas: Lista de columnas a analizar
    
    Returns:
        DataFrame con comparación de métodos
    """
    print("🔍 COMPARACIÓN DE MÉTODOS DE DETECCIÓN DE OUTLIERS")
    print("=" * 60)
    
    # Aplicar todos los métodos
    df_zscore = detectar_outliers_zscore(df, columnas)
    df_iqr = detectar_outliers_iqr(df, columnas)
    df_isolation = detectar_outliers_isolation_forest(df, columnas)
    
    # Combinar resultados
    df_comparacion = df.copy()
    df_comparacion['outlier_zscore'] = df_zscore['outlier_zscore']
    df_comparacion['outlier_iqr'] = df_iqr['outlier_iqr']
    df_comparacion['outlier_isolation'] = df_isolation['outlier_isolation']
    
    # Calcular estadísticas
    total_outliers = {
        'Z-Score': df_comparacion['outlier_zscore'].sum(),
        'IQR': df_comparacion['outlier_iqr'].sum(),
        'Isolation Forest': df_comparacion['outlier_isolation'].sum()
    }
    
    print(f"Total de outliers detectados:")
    for metodo, cantidad in total_outliers.items():
        porcentaje = (cantidad / len(df)) * 100
        print(f"  {metodo}: {cantidad} ({porcentaje:.1f}%)")
    
    print(f"\nTotal de registros: {len(df)}")
    
    return df_comparacion

def visualizar_outliers(df, columnas, metodo='isolation'):
    """
    Crea visualizaciones para mostrar outliers detectados
    
    Args:
        df: DataFrame con los datos
        columnas: Lista de columnas a visualizar
        metodo: Método de detección a visualizar
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.ravel()
    
    for i, col in enumerate(columnas[:4]):
        ax = axes[i]
        
        # Crear scatter plot
        outliers_mask = df[f'outlier_{metodo}']
        
        # Datos normales
        ax.scatter(
            df[~outliers_mask].index, 
            df[~outliers_mask][col], 
            alpha=0.6, 
            label='Normal',
            color='blue'
        )
        
        # Outliers
        ax.scatter(
            df[outliers_mask].index, 
            df[outliers_mask][col], 
            alpha=0.8, 
            label='Outlier',
            color='red',
            s=100
        )
        
        ax.set_title(f'Outliers en {col} ({metodo.upper()})')
        ax.set_xlabel('Índice del registro')
        ax.set_ylabel(col)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def analizar_outliers_multivariados(df, columnas):
    """
    Análisis específico para outliers multivariados usando Isolation Forest
    """
    print("\n🎯 ANÁLISIS DE OUTLIERS MULTIVARIADOS")
    print("=" * 50)
    
    # Detectar outliers multivariados
    df_analisis = detectar_outliers_isolation_forest(df, columnas, contamination=0.1)
    
    # Mostrar outliers detectados
    outliers = df_analisis[df_analisis['outlier_isolation']]
    
    if len(outliers) > 0:
        print(f"Se detectaron {len(outliers)} outliers multivariados:")
        print("\nRegistros outliers:")
        print(outliers[columnas + ['id']].to_string(index=False))
        
        # Análisis de características de outliers
        print(f"\n📊 Características de los outliers:")
        for col in columnas:
            print(f"\n{col}:")
            print(f"  Media general: {df[col].mean():.2f}")
            print(f"  Media outliers: {outliers[col].mean():.2f}")
            print(f"  Diferencia: {abs(outliers[col].mean() - df[col].mean()):.2f}")
    else:
        print("No se detectaron outliers multivariados significativos.")
    
    return df_analisis

def main():
    """Función principal para demostrar detección de outliers"""
    print("🚀 DEMOSTRACIÓN: DETECCIÓN AVANZADA DE OUTLIERS")
    print("=" * 60)
    
    # Crear datos de ejemplo
    df = crear_datos_ejemplo()
    columnas_numericas = ['precio', 'cantidad', 'descuento', 'edad_cliente']
    
    print(f"Dataset creado con {len(df)} registros")
    print(f"Columnas numéricas: {', '.join(columnas_numericas)}")
    
    # Mostrar estadísticas básicas
    print(f"\n📈 ESTADÍSTICAS BÁSICAS:")
    print(df[columnas_numericas].describe().round(2))
    
    # Comparar métodos
    df_comparacion = comparar_metodos_outliers(df, columnas_numericas)
    
    # Análisis multivariado
    df_multivariado = analizar_outliers_multivariados(df, columnas_numericas)
    
    # Visualizaciones
    print(f"\n📊 Generando visualizaciones...")
    visualizar_outliers(df_comparacion, columnas_numericas, 'isolation')
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    print("=" * 30)
    print("• Z-Score: Mejor para datos normalmente distribuidos")
    print("• IQR: Más robusto para datos con distribución sesgada")
    print("• Isolation Forest: Ideal para detectar outliers multivariados")
    print("• Combinar métodos para análisis más completo")
    
    return df_comparacion

if __name__ == "__main__":
    # Ejecutar demostración
    resultado = main()
