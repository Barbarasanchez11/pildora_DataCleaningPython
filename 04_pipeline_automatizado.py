"""
Pipeline Automatizado de Data Cleaning
======================================

Este módulo implementa un pipeline completo y reutilizable para limpieza de datos:
1. Clase DataCleaner con métodos configurables
2. Logging de transformaciones
3. Testing de calidad de datos
4. Documentación automática de decisiones
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

class DataCleaner:
    """
    Pipeline automatizado para limpieza de datos
    
    Características:
    - Configuración flexible de transformaciones
    - Logging detallado de cambios
    - Validación de calidad de datos
    - Documentación automática
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa el limpiador de datos
        
        Args:
            config: Configuración personalizada del pipeline
        """
        self.config = config or self._configuracion_default()
        self.transformaciones = []
        self.logger = self._configurar_logging()
        self.estadisticas = {}
        
    def _configuracion_default(self) -> Dict:
        """Configuración por defecto del pipeline"""
        return {
            'eliminar_duplicados': True,
            'manejar_nulos': True,
            'estandarizar_texto': True,
            'detectar_outliers': False,
            'validar_formatos': True,
            'logging_detallado': True,
            'umbral_outliers': 3.0,
            'metodo_imputacion': 'median',  # 'mean', 'median', 'mode', 'forward_fill'
            'texto_minusculas': True,
            'texto_espacios': True
        }
    
    def _configurar_logging(self) -> logging.Logger:
        """Configura el sistema de logging"""
        logger = logging.getLogger('DataCleaner')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _registrar_transformacion(self, operacion: str, detalles: Dict):
        """Registra una transformación aplicada"""
        transformacion = {
            'timestamp': datetime.now().isoformat(),
            'operacion': operacion,
            'detalles': detalles
        }
        self.transformaciones.append(transformacion)
        
        if self.config['logging_detallado']:
            self.logger.info(f"Transformación: {operacion} - {detalles}")
    
    def eliminar_duplicados(self, df: pd.DataFrame) -> pd.DataFrame:
        """Elimina duplicados del DataFrame"""
        if not self.config['eliminar_duplicados']:
            return df
        
        filas_originales = len(df)
        df_limpio = df.drop_duplicates()
        filas_eliminadas = filas_originales - len(df_limpio)
        
        self._registrar_transformacion(
            'eliminar_duplicados',
            {
                'filas_originales': filas_originales,
                'filas_eliminadas': filas_eliminadas,
                'filas_restantes': len(df_limpio)
            }
        )
        
        return df_limpio
    
    def manejar_valores_nulos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Maneja valores nulos según la configuración"""
        if not self.config['manejar_nulos']:
            return df
        
        df_limpio = df.copy()
        nulos_por_columna = df.isnull().sum()
        
        for columna in df.columns:
            if nulos_por_columna[columna] > 0:
                if df[columna].dtype in ['int64', 'float64']:
                    # Columnas numéricas
                    if self.config['metodo_imputacion'] == 'mean':
                        valor_imputacion = df[columna].mean()
                    elif self.config['metodo_imputacion'] == 'median':
                        valor_imputacion = df[columna].median()
                    elif self.config['metodo_imputacion'] == 'forward_fill':
                        df_limpio[columna] = df[columna].fillna(method='ffill')
                        continue
                    else:
                        valor_imputacion = df[columna].median()
                    
                    df_limpio[columna] = df[columna].fillna(valor_imputacion)
                else:
                    # Columnas de texto
                    df_limpio[columna] = df[columna].fillna('UNKNOWN')
        
        self._registrar_transformacion(
            'manejar_valores_nulos',
            {
                'nulos_por_columna': nulos_por_columna.to_dict(),
                'metodo_imputacion': self.config['metodo_imputacion']
            }
        )
        
        return df_limpio
    
    def estandarizar_texto(self, df: pd.DataFrame) -> pd.DataFrame:
        """Estandariza columnas de texto"""
        if not self.config['estandarizar_texto']:
            return df
        
        df_limpio = df.copy()
        columnas_texto = df.select_dtypes(include=['object']).columns
        
        for columna in columnas_texto:
            if self.config['texto_minusculas']:
                df_limpio[columna] = df_limpio[columna].astype(str).str.lower()
            
            if self.config['texto_espacios']:
                df_limpio[columna] = df_limpio[columna].str.strip()
                df_limpio[columna] = df_limpio[columna].str.replace(r'\s+', ' ', regex=True)
        
        self._registrar_transformacion(
            'estandarizar_texto',
            {
                'columnas_procesadas': list(columnas_texto),
                'minusculas': self.config['texto_minusculas'],
                'espacios': self.config['texto_espacios']
            }
        )
        
        return df_limpio
    
    def detectar_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detecta outliers en columnas numéricas"""
        if not self.config['detectar_outliers']:
            return df
        
        df_limpio = df.copy()
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
        outliers_detectados = {}
        
        for columna in columnas_numericas:
            # Método Z-score
            z_scores = np.abs((df[columna] - df[columna].mean()) / df[columna].std())
            outliers = z_scores > self.config['umbral_outliers']
            outliers_detectados[columna] = outliers.sum()
            
            # Marcar outliers
            df_limpio[f'{columna}_outlier'] = outliers
        
        self._registrar_transformacion(
            'detectar_outliers',
            {
                'columnas_analizadas': list(columnas_numericas),
                'outliers_por_columna': outliers_detectados,
                'umbral': self.config['umbral_outliers']
            }
        )
        
        return df_limpio
    
    def validar_formatos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Valida formatos de datos específicos"""
        if not self.config['validar_formatos']:
            return df
        
        df_limpio = df.copy()
        validaciones = {}
        
        # Validar emails
        columnas_email = [col for col in df.columns if 'email' in col.lower()]
        for columna in columnas_email:
            patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            emails_validos = df[columna].astype(str).str.match(patron_email, na=False)
            validaciones[f'{columna}_emails_validos'] = emails_validos.sum()
        
        # Validar teléfonos (formato español)
        columnas_telefono = [col for col in df.columns if 'telefono' in col.lower() or 'phone' in col.lower()]
        for columna in columnas_telefono:
            patron_telefono = r'^(\+34|0034|34)?[6-9]\d{8}$'
            telefonos_validos = df[columna].astype(str).str.match(patron_telefono, na=False)
            validaciones[f'{columna}_telefonos_validos'] = telefonos_validos.sum()
        
        self._registrar_transformacion(
            'validar_formatos',
            {
                'validaciones': validaciones
            }
        )
        
        return df_limpio
    
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica todas las transformaciones configuradas
        
        Args:
            df: DataFrame a limpiar
            
        Returns:
            DataFrame limpio
        """
        self.logger.info(f"Iniciando limpieza de datos - {len(df)} filas, {len(df.columns)} columnas")
        
        # Guardar estadísticas iniciales
        self.estadisticas['inicial'] = {
            'filas': len(df),
            'columnas': len(df.columns),
            'nulos_totales': df.isnull().sum().sum(),
            'duplicados': df.duplicated().sum()
        }
        
        df_limpio = df.copy()
        
        # Aplicar transformaciones en orden
        df_limpio = self.eliminar_duplicados(df_limpio)
        df_limpio = self.manejar_valores_nulos(df_limpio)
        df_limpio = self.estandarizar_texto(df_limpio)
        df_limpio = self.detectar_outliers(df_limpio)
        df_limpio = self.validar_formatos(df_limpio)
        
        # Guardar estadísticas finales
        self.estadisticas['final'] = {
            'filas': len(df_limpio),
            'columnas': len(df_limpio.columns),
            'nulos_totales': df_limpio.isnull().sum().sum(),
            'duplicados': df_limpio.duplicated().sum()
        }
        
        self.logger.info("Limpieza de datos completada")
        return df_limpio
    
    def generar_reporte(self) -> Dict:
        """Genera un reporte detallado de la limpieza"""
        reporte = {
            'timestamp': datetime.now().isoformat(),
            'configuracion': self.config,
            'estadisticas': self.estadisticas,
            'transformaciones': self.transformaciones,
            'resumen': {
                'filas_eliminadas': self.estadisticas['inicial']['filas'] - self.estadisticas['final']['filas'],
                'nulos_imputados': self.estadisticas['inicial']['nulos_totales'] - self.estadisticas['final']['nulos_totales'],
                'transformaciones_aplicadas': len(self.transformaciones)
            }
        }
        
        return reporte
    
    def guardar_reporte(self, archivo: str):
        """Guarda el reporte en un archivo JSON"""
        reporte = self.generar_reporte()
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Reporte guardado en: {archivo}")

class ValidadorCalidad:
    """Clase para validar la calidad de los datos limpios"""
    
    def __init__(self):
        self.reglas = []
    
    def agregar_regla(self, nombre: str, funcion: Callable, descripcion: str):
        """Agrega una regla de validación personalizada"""
        self.reglas.append({
            'nombre': nombre,
            'funcion': funcion,
            'descripcion': descripcion
        })
    
    def validar(self, df: pd.DataFrame) -> Dict:
        """Ejecuta todas las reglas de validación"""
        resultados = {
            'timestamp': datetime.now().isoformat(),
            'reglas_ejecutadas': len(self.reglas),
            'resultados': []
        }
        
        for regla in self.reglas:
            try:
                resultado = regla['funcion'](df)
                resultados['resultados'].append({
                    'regla': regla['nombre'],
                    'descripcion': regla['descripcion'],
                    'paso': resultado,
                    'error': None
                })
            except Exception as e:
                resultados['resultados'].append({
                    'regla': regla['nombre'],
                    'descripcion': regla['descripcion'],
                    'paso': False,
                    'error': str(e)
                })
        
        return resultados

def crear_datos_demo():
    """Crea datos de demostración para el pipeline"""
    np.random.seed(42)
    
    datos = {
        'id': range(1, 101),
        'nombre': [f'Usuario_{i}' for i in range(1, 101)],
        'email': [f'usuario{i}@email.com' for i in range(1, 101)],
        'telefono': [f'+34-666-{i:03d}-{i+100:03d}' for i in range(1, 101)],
        'edad': np.random.normal(35, 10, 100),
        'salario': np.random.normal(50000, 15000, 100),
        'fecha_registro': pd.date_range('2023-01-01', periods=100, freq='D')
    }
    
    df = pd.DataFrame(datos)
    
    # Introducir problemas intencionalmente
    # Duplicados
    df = pd.concat([df, df.iloc[:5]], ignore_index=True)
    
    # Valores nulos
    df.loc[10:15, 'email'] = None
    df.loc[20:25, 'edad'] = np.nan
    
    # Texto inconsistente
    df.loc[30:35, 'nombre'] = df.loc[30:35, 'nombre'].str.upper()
    df.loc[40:45, 'nombre'] = '  ' + df.loc[40:45, 'nombre'] + '  '
    
    # Outliers
    df.loc[50, 'salario'] = 500000
    df.loc[51, 'edad'] = 150
    
    return df

def demostrar_pipeline():
    """Demuestra el uso del pipeline automatizado"""
    print("🚀 DEMOSTRACIÓN: PIPELINE AUTOMATIZADO DE DATA CLEANING")
    print("=" * 70)
    
    # Crear datos de demostración
    df_original = crear_datos_demo()
    print(f"Datos originales: {len(df_original)} filas, {len(df_original.columns)} columnas")
    print(f"Valores nulos: {df_original.isnull().sum().sum()}")
    print(f"Duplicados: {df_original.duplicated().sum()}")
    
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
    df_limpio = limpiador.fit_transform(df_original)
    
    print(f"\nDatos limpios: {len(df_limpio)} filas, {len(df_limpio.columns)} columnas")
    print(f"Valores nulos: {df_limpio.isnull().sum().sum()}")
    print(f"Duplicados: {df_limpio.duplicated().sum()}")
    
    # Generar reporte
    reporte = limpiador.generar_reporte()
    print(f"\n📊 REPORTE DE LIMPIEZA:")
    print(f"Filas eliminadas: {reporte['resumen']['filas_eliminadas']}")
    print(f"Nulos imputados: {reporte['resumen']['nulos_imputados']}")
    print(f"Transformaciones aplicadas: {reporte['resumen']['transformaciones_aplicadas']}")
    
    # Guardar reporte
    limpiador.guardar_reporte('reporte_limpieza.json')
    
    # Validación de calidad
    validador = ValidadorCalidad()
    
    # Agregar reglas de validación
    validador.agregar_regla(
        'sin_duplicados',
        lambda df: df.duplicated().sum() == 0,
        'No debe haber duplicados'
    )
    
    validador.agregar_regla(
        'sin_nulos',
        lambda df: df.isnull().sum().sum() == 0,
        'No debe haber valores nulos'
    )
    
    validador.agregar_regla(
        'emails_validos',
        lambda df: df['email'].str.contains('@').all(),
        'Todos los emails deben ser válidos'
    )
    
    # Ejecutar validación
    resultado_validacion = validador.validar(df_limpio)
    
    print(f"\n✅ VALIDACIÓN DE CALIDAD:")
    for resultado in resultado_validacion['resultados']:
        estado = "✅" if resultado['paso'] else "❌"
        print(f"{estado} {resultado['regla']}: {resultado['descripcion']}")
        if resultado['error']:
            print(f"   Error: {resultado['error']}")
    
    return df_limpio, reporte

def main():
    """Función principal para demostrar el pipeline"""
    print("🎯 PIPELINE AUTOMATIZADO DE DATA CLEANING")
    print("=" * 60)
    
    # Ejecutar demostración
    df_limpio, reporte = demostrar_pipeline()
    
    print(f"\n💡 MEJORES PRÁCTICAS IMPLEMENTADAS:")
    print("=" * 50)
    print("• Pipeline configurable y reutilizable")
    print("• Logging detallado de todas las transformaciones")
    print("• Validación automática de calidad de datos")
    print("• Reportes documentados para auditoría")
    print("• Manejo de errores robusto")
    print("• Configuración flexible por proyecto")
    
    return df_limpio, reporte

if __name__ == "__main__":
    # Ejecutar demostración
    resultado = main()
