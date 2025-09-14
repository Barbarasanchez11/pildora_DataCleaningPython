"""
Casos Prácticos Complejos de Data Cleaning
==========================================

Este módulo presenta casos prácticos reales de limpieza de datos:
1. Dataset de E-commerce con múltiples problemas
2. Datos temporales con zonas horarias y frecuencias irregulares
3. Técnicas específicas para cada tipo de problema
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class LimpiadorEcommerce:
    """Clase especializada para limpiar datos de e-commerce"""
    
    def __init__(self):
        self.monedas = {
            '€': 'EUR', 'EUR': 'EUR', 'euros': 'EUR',
            '$': 'USD', 'USD': 'USD', 'dollars': 'USD',
            '£': 'GBP', 'GBP': 'GBP', 'pounds': 'GBP',
            '¥': 'JPY', 'JPY': 'JPY', 'yen': 'JPY'
        }
        
        self.tasas_cambio = {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.73,
            'JPY': 110.0
        }
    
    def normalizar_precio(self, precio_str: str) -> Optional[float]:
        """
        Normaliza precios en diferentes monedas a USD
        
        Args:
            precio_str: String con precio y moneda
            
        Returns:
            Precio normalizado en USD o None si no es válido
        """
        if pd.isna(precio_str) or not isinstance(precio_str, str):
            return None
        
        # Extraer número y moneda
        precio_str = str(precio_str).strip()
        
        # Buscar patrón de precio con moneda
        patron_precio = r'([\d,\.]+)\s*([€$£¥]|EUR|USD|GBP|JPY|euros?|dollars?|pounds?|yen)'
        match = re.search(patron_precio, precio_str, re.IGNORECASE)
        
        if not match:
            # Intentar solo número
            numeros = re.findall(r'[\d,\.]+', precio_str)
            if numeros:
                try:
                    precio_num = self._parsear_numero(numeros[0])
                    return precio_num  # Asumir USD por defecto
                except ValueError:
                    return None
            return None
        
        precio_num = self._parsear_numero(match.group(1))
        moneda_str = match.group(2).upper()
        
        # Normalizar moneda
        moneda = self.monedas.get(moneda_str, 'USD')
        
        # Convertir a USD
        if moneda in self.tasas_cambio:
            return precio_num / self.tasas_cambio[moneda]
        
        return precio_num
    
    def _parsear_numero(self, numero_str: str) -> float:
        """
        Parsea números en formato europeo o americano
        
        Args:
            numero_str: String con número
            
        Returns:
            Número como float
        """
        # Limpiar espacios
        numero_str = numero_str.strip()
        
        # Detectar formato europeo (1.099,00) vs americano (1,099.00)
        if ',' in numero_str and '.' in numero_str:
            # Ambos separadores presentes
            if numero_str.rfind(',') > numero_str.rfind('.'):
                # Formato europeo: 1.099,00
                numero_str = numero_str.replace('.', '').replace(',', '.')
            else:
                # Formato americano: 1,099.00
                numero_str = numero_str.replace(',', '')
        elif ',' in numero_str:
            # Solo coma - verificar si es decimal o miles
            partes = numero_str.split(',')
            if len(partes) == 2 and len(partes[1]) <= 2:
                # Formato europeo: 1099,00
                numero_str = numero_str.replace(',', '.')
            else:
                # Formato americano: 1,099
                numero_str = numero_str.replace(',', '')
        
        return float(numero_str)
    
    def limpiar_categoria(self, categoria: str) -> str:
        """
        Normaliza categorías de productos
        
        Args:
            categoria: Categoría original
            
        Returns:
            Categoría normalizada
        """
        if pd.isna(categoria) or not isinstance(categoria, str):
            return 'UNKNOWN'
        
        categoria = str(categoria).strip().lower()
        
        # Mapeo de categorías similares
        mapeo_categorias = {
            'electronics': ['electronic', 'electrónica', 'electrónicos', 'tech'],
            'clothing': ['ropa', 'vestimenta', 'clothes', 'fashion'],
            'books': ['libros', 'book', 'literatura'],
            'home': ['hogar', 'casa', 'home & garden', 'decoración'],
            'sports': ['deportes', 'sport', 'fitness', 'ejercicio'],
            'beauty': ['belleza', 'cosmética', 'makeup', 'skincare'],
            'toys': ['juguetes', 'toy', 'juegos', 'games'],
            'automotive': ['automóvil', 'auto', 'car', 'vehículos']
        }
        
        # Buscar categoría más similar
        for categoria_estandar, variantes in mapeo_categorias.items():
            if any(var in categoria for var in variantes):
                return categoria_estandar.upper()
        
        return categoria.upper()
    
    def limpiar_descripcion(self, descripcion: str) -> str:
        """
        Limpia descripciones de productos con HTML y caracteres especiales
        
        Args:
            descripcion: Descripción original
            
        Returns:
            Descripción limpia
        """
        if pd.isna(descripcion) or not isinstance(descripcion, str):
            return ''
        
        # Eliminar HTML
        descripcion = re.sub(r'<[^>]+>', '', str(descripcion))
        
        # Decodificar entidades HTML
        entidades = {
            '&amp;': '&', '&lt;': '<', '&gt;': '>',
            '&quot;': '"', '&#39;': "'", '&nbsp;': ' '
        }
        
        for entidad, caracter in entidades.items():
            descripcion = descripcion.replace(entidad, caracter)
        
        # Limpiar caracteres especiales excesivos
        descripcion = re.sub(r'[^\w\s.,!?()-]', '', descripcion)
        
        # Normalizar espacios
        descripcion = re.sub(r'\s+', ' ', descripcion).strip()
        
        return descripcion
    
    def validar_sku(self, sku: str) -> bool:
        """
        Valida formato de SKU (Stock Keeping Unit)
        
        Args:
            sku: SKU a validar
            
        Returns:
            True si el SKU es válido
        """
        if pd.isna(sku) or not isinstance(sku, str):
            return False
        
        sku = str(sku).strip()
        
        # SKU debe tener al menos 3 caracteres alfanuméricos
        if len(sku) < 3:
            return False
        
        # Solo caracteres alfanuméricos y guiones
        if not re.match(r'^[A-Z0-9-]+$', sku.upper()):
            return False
        
        return True

class LimpiadorTemporal:
    """Clase especializada para limpiar datos temporales"""
    
    def __init__(self):
        self.zonas_horarias = {
            'ES': 'Europe/Madrid',
            'US': 'America/New_York',
            'UK': 'Europe/London',
            'JP': 'Asia/Tokyo',
            'AU': 'Australia/Sydney'
        }
    
    def parsear_fecha_flexible(self, fecha_str: str) -> Optional[datetime]:
        """
        Parsea fechas en diferentes formatos
        
        Args:
            fecha_str: String con fecha
            
        Returns:
            Objeto datetime o None si no se puede parsear
        """
        if pd.isna(fecha_str) or not isinstance(fecha_str, str):
            return None
        
        fecha_str = str(fecha_str).strip()
        
        # Formatos comunes
        formatos = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y',
            '%d-%m-%Y %H:%M:%S',
            '%d-%m-%Y',
            '%m/%d/%Y %H:%M:%S',
            '%m/%d/%Y',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%fZ'
        ]
        
        for formato in formatos:
            try:
                return datetime.strptime(fecha_str, formato)
            except ValueError:
                continue
        
        return None
    
    def normalizar_zona_horaria(self, fecha: datetime, zona_original: str = 'UTC') -> datetime:
        """
        Normaliza zona horaria de una fecha
        
        Args:
            fecha: Fecha a normalizar
            zona_original: Zona horaria original
            
        Returns:
            Fecha en UTC
        """
        if pd.isna(fecha) or not isinstance(fecha, datetime):
            return None
        
        try:
            # Si la fecha no tiene zona horaria, asumir la especificada
            if fecha.tzinfo is None:
                tz = pytz.timezone(zona_original)
                fecha = tz.localize(fecha)
            
            # Convertir a UTC
            return fecha.astimezone(pytz.UTC)
        
        except Exception:
            return fecha
    
    def detectar_frecuencia(self, serie_temporal: pd.Series) -> str:
        """
        Detecta la frecuencia de una serie temporal
        
        Args:
            serie_temporal: Serie temporal
            
        Returns:
            Frecuencia detectada
        """
        if len(serie_temporal) < 2:
            return 'unknown'
        
        # Calcular diferencias entre fechas consecutivas
        diferencias = serie_temporal.diff().dropna()
        
        if len(diferencias) == 0:
            return 'unknown'
        
        # Frecuencia más común
        frecuencia_comun = diferencias.mode().iloc[0] if len(diferencias.mode()) > 0 else diferencias.iloc[0]
        
        # Mapear a frecuencias estándar
        if frecuencia_comun <= timedelta(minutes=1):
            return 'minutely'
        elif frecuencia_comun <= timedelta(hours=1):
            return 'hourly'
        elif frecuencia_comun <= timedelta(days=1):
            return 'daily'
        elif frecuencia_comun <= timedelta(weeks=1):
            return 'weekly'
        elif frecuencia_comun <= timedelta(days=30):
            return 'monthly'
        else:
            return 'yearly'
    
    def rellenar_gaps_temporales(self, df: pd.DataFrame, columna_fecha: str, 
                                frecuencia: str = 'D') -> pd.DataFrame:
        """
        Rellena gaps en series temporales
        
        Args:
            df: DataFrame con datos temporales
            columna_fecha: Nombre de la columna de fecha
            frecuencia: Frecuencia deseada ('D'=diaria, 'H'=horaria, etc.)
            
        Returns:
            DataFrame con gaps rellenados
        """
        df_limpio = df.copy()
        
        # Establecer fecha como índice
        df_limpio[columna_fecha] = pd.to_datetime(df_limpio[columna_fecha])
        df_limpio = df_limpio.set_index(columna_fecha)
        
        # Crear rango completo de fechas
        rango_completo = pd.date_range(
            start=df_limpio.index.min(),
            end=df_limpio.index.max(),
            freq=frecuencia
        )
        
        # Reindexar con rango completo
        df_limpio = df_limpio.reindex(rango_completo)
        
        return df_limpio.reset_index()

def crear_datos_ecommerce_sucios():
    """Crea datos de e-commerce con problemas típicos"""
    datos = {
        'producto_id': ['PROD-001', 'PROD-002', 'PROD-003', 'PROD-004', 'PROD-005'],
        'nombre': [
            'iPhone 13 Pro Max 256GB',
            'Samsung Galaxy S21 Ultra',
            'MacBook Pro 16" M1 Pro',
            'Sony WH-1000XM4 Headphones',
            'Nintendo Switch OLED'
        ],
        'precio': [
            '1,199.99€',
            '$1,299.99',
            '2,499.00 EUR',
            '£349.99',
            '349.99 USD'
        ],
        'categoria': [
            'electronics',
            'Electrónica',
            'tech',
            'Electronics',
            'gaming'
        ],
        'descripcion': [
            '<p>El <strong>iPhone 13 Pro Max</strong> con <em>256GB</em> de almacenamiento</p>',
            'Samsung Galaxy S21 Ultra con cámara de 108MP',
            '<div>MacBook Pro 16" con chip <b>M1 Pro</b></div>',
            'Sony WH-1000XM4 - Auriculares inalámbricos',
            'Nintendo Switch OLED - Consola de videojuegos'
        ],
        'sku': [
            'IPH13PM256',
            'SGS21U-256',
            'MBP16-M1P',
            'SONY-WH1000XM4',
            'NSW-OLED'
        ],
        'stock': [50, 25, 10, 100, 75],
        'fecha_creacion': [
            '2023-01-15 10:30:00',
            '2023-01-16 14:22:00',
            '2023-01-17 09:15:00',
            '2023-01-18 16:45:00',
            '2023-01-19 11:30:00'
        ]
    }
    
    return pd.DataFrame(datos)

def crear_datos_temporales_sucios():
    """Crea datos temporales con problemas típicos"""
    # Crear fechas con gaps y formatos inconsistentes
    fechas_base = [
        '2023-01-01 00:00:00',
        '2023-01-01 02:00:00',
        '2023-01-01 04:00:00',
        '2023-01-01 06:00:00',
        '2023-01-01 08:00:00',
        '2023-01-01 10:00:00',
        '2023-01-01 12:00:00',
        '2023-01-01 14:00:00',
        '2023-01-01 16:00:00',
        '2023-01-01 18:00:00',
        '2023-01-01 20:00:00',
        '2023-01-01 22:00:00'
    ]
    
    # Agregar algunas fechas en formato diferente
    fechas_mixtas = fechas_base + [
        '01/01/2023 23:00:00',
        '02/01/2023 01:00:00',
        '02/01/2023 03:00:00'
    ]
    
    # Crear datos con gaps intencionales
    datos = {
        'timestamp': fechas_mixtas,
        'temperatura': [20.5, 21.2, 22.1, 23.5, 24.8, 25.2, 26.1, 25.8, 24.5, 23.2, 22.0, 21.5, 20.8, 19.5, 18.2],
        'humedad': [65, 67, 69, 71, 73, 75, 77, 76, 74, 72, 70, 68, 66, 64, 62],
        'presion': [1013.2, 1012.8, 1012.5, 1012.1, 1011.8, 1011.5, 1011.2, 1011.5, 1011.8, 1012.1, 1012.4, 1012.7, 1013.0, 1013.3, 1013.6],
        'zona_horaria': ['Europe/Madrid'] * len(fechas_mixtas)
    }
    
    return pd.DataFrame(datos)

def caso_ecommerce():
    """Caso práctico 1: Limpieza de datos de E-commerce"""
    print("🛒 CASO PRÁCTICO 1: DATASET DE E-COMMERCE")
    print("=" * 60)
    
    # Crear datos sucios
    df = crear_datos_ecommerce_sucios()
    limpiador = LimpiadorEcommerce()
    
    print("Datos originales:")
    print(df.to_string(index=False))
    
    # Aplicar limpiezas
    df['precio_normalizado'] = df['precio'].apply(limpiador.normalizar_precio)
    df['categoria_limpia'] = df['categoria'].apply(limpiador.limpiar_categoria)
    df['descripcion_limpia'] = df['descripcion'].apply(limpiador.limpiar_descripcion)
    df['sku_valido'] = df['sku'].apply(limpiador.validar_sku)
    
    print("\nDatos limpios:")
    columnas_limpias = ['producto_id', 'precio_normalizado', 'categoria_limpia', 'sku_valido']
    print(df[columnas_limpias].to_string(index=False))
    
    # Análisis de calidad
    print("\n📊 ANÁLISIS DE CALIDAD:")
    print(f"Precios válidos: {df['precio_normalizado'].notna().sum()}/{len(df)}")
    print(f"SKUs válidos: {df['sku_valido'].sum()}/{len(df)}")
    print(f"Categorías únicas: {df['categoria_limpia'].nunique()}")
    
    # Estadísticas de precios
    print(f"\nPrecios normalizados (USD):")
    print(f"  Media: ${df['precio_normalizado'].mean():.2f}")
    print(f"  Mediana: ${df['precio_normalizado'].median():.2f}")
    print(f"  Rango: ${df['precio_normalizado'].min():.2f} - ${df['precio_normalizado'].max():.2f}")
    
    return df

def caso_temporal():
    """Caso práctico 2: Limpieza de datos temporales"""
    print("\n⏰ CASO PRÁCTICO 2: DATOS TEMPORALES")
    print("=" * 60)
    
    # Crear datos sucios
    df = crear_datos_temporales_sucios()
    limpiador = LimpiadorTemporal()
    
    print("Datos originales:")
    print(df.head().to_string(index=False))
    
    # Parsear fechas
    df['timestamp_parsed'] = df['timestamp'].apply(limpiador.parsear_fecha_flexible)
    
    # Normalizar zona horaria
    df['timestamp_utc'] = df.apply(
        lambda row: limpiador.normalizar_zona_horaria(
            row['timestamp_parsed'], 
            row['zona_horaria']
        ), axis=1
    )
    
    # Detectar frecuencia
    serie_temporal = df['timestamp_utc'].dropna()
    frecuencia = limpiador.detectar_frecuencia(serie_temporal)
    
    print(f"\nFrecuencia detectada: {frecuencia}")
    
    # Rellenar gaps temporales
    df_limpio = limpiador.rellenar_gaps_temporales(
        df.dropna(subset=['timestamp_utc']), 
        'timestamp_utc', 
        '2H'  # Cada 2 horas
    )
    
    print(f"\nDatos con gaps rellenados:")
    print(f"Registros originales: {len(df)}")
    print(f"Registros después de rellenar: {len(df_limpio)}")
    
    # Análisis de gaps
    gaps_originales = len(df_limpio) - len(df)
    print(f"Gaps rellenados: {gaps_originales}")
    
    return df_limpio

def pipeline_completo():
    """Pipeline completo para ambos casos"""
    print("\n🚀 PIPELINE COMPLETO DE LIMPIEZA")
    print("=" * 60)
    
    # Caso E-commerce
    df_ecommerce = caso_ecommerce()
    
    # Caso Temporal
    df_temporal = caso_temporal()
    
    print("\n💡 LECCIONES APRENDIDAS:")
    print("=" * 40)
    print("• E-commerce: Normalizar monedas y categorías es crucial")
    print("• Temporal: Detectar frecuencia y rellenar gaps mejora análisis")
    print("• Validación: Verificar formatos antes de procesar")
    print("• Documentación: Registrar todas las transformaciones")
    
    return df_ecommerce, df_temporal

def main():
    """Función principal para demostrar casos prácticos"""
    print("🎯 DEMOSTRACIÓN: CASOS PRÁCTICOS COMPLEJOS")
    print("=" * 60)
    
    # Ejecutar pipeline completo
    df_ecommerce, df_temporal = pipeline_completo()
    
    return df_ecommerce, df_temporal

if __name__ == "__main__":
    # Ejecutar demostración
    resultado = main()
