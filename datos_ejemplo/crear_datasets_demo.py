"""
Generador de Datasets de Demostración
=====================================

Este script crea datasets de ejemplo para la píldora de Data Cleaning.
Incluye datos con problemas típicos que se encuentran en proyectos reales.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json

def crear_dataset_ecommerce():
    """Crea dataset de e-commerce con problemas típicos"""
    np.random.seed(42)
    
    # Productos base
    productos_base = [
        "iPhone 13 Pro Max 256GB",
        "Samsung Galaxy S21 Ultra",
        "MacBook Pro 16\" M1 Pro",
        "Sony WH-1000XM4 Headphones",
        "Nintendo Switch OLED",
        "iPad Air 5th Gen",
        "Dell XPS 13 Laptop",
        "AirPods Pro 2nd Gen",
        "Samsung 4K Smart TV 55\"",
        "PlayStation 5 Console"
    ]
    
    # Precios en diferentes monedas y formatos
    precios_sucios = [
        "1,199.99€", "$1,299.99", "2,499.00 EUR", "£349.99", "349.99 USD",
        "1,099.00€", "$1,199.00", "2,299.00 EUR", "£299.99", "299.99 USD",
        "1,899.00€", "$2,099.00", "3,499.00 EUR", "£1,799.99", "1,799.99 USD",
        "299.99€", "$349.99", "399.00 EUR", "£279.99", "279.99 USD",
        "349.99€", "$399.99", "449.00 EUR", "£329.99", "329.99 USD"
    ]
    
    # Categorías inconsistentes
    categorias_sucias = [
        "electronics", "Electrónica", "tech", "Electronics", "gaming",
        "computers", "Computadoras", "laptops", "Laptops", "audio",
        "Audio", "headphones", "Headphones", "consoles", "Consolas",
        "tablets", "Tablets", "smartphones", "Smartphones", "tv"
    ]
    
    # Descripciones con HTML
    descripciones_html = [
        '<p>El <strong>iPhone 13 Pro Max</strong> con <em>256GB</em> de almacenamiento</p>',
        'Samsung Galaxy S21 Ultra con cámara de 108MP',
        '<div>MacBook Pro 16" con chip <b>M1 Pro</b></div>',
        'Sony WH-1000XM4 - <span>Auriculares inalámbricos</span>',
        'Nintendo Switch OLED - <i>Consola de videojuegos</i>',
        '<p>iPad Air 5ta generación con <strong>chip M1</strong></p>',
        'Dell XPS 13 - Laptop ultradelgado',
        '<div>AirPods Pro 2da generación con <em>cancelación de ruido</em></div>',
        'Samsung 4K Smart TV 55" - <b>Televisor inteligente</b>',
        'PlayStation 5 - <span>Consola de nueva generación</span>'
    ]
    
    # Generar datos
    datos = []
    for i in range(50):
        datos.append({
            'producto_id': f'PROD-{i+1:03d}',
            'nombre': random.choice(productos_base),
            'precio': random.choice(precios_sucios),
            'categoria': random.choice(categorias_sucias),
            'descripcion': random.choice(descripciones_html),
            'sku': f'SKU-{random.randint(1000, 9999)}',
            'stock': random.randint(0, 100),
            'fecha_creacion': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S'),
            'rating': round(random.uniform(3.0, 5.0), 1),
            'reviews': random.randint(0, 1000)
        })
    
    return pd.DataFrame(datos)

def crear_dataset_clientes():
    """Crea dataset de clientes con datos sucios típicos"""
    np.random.seed(42)
    
    # Nombres con problemas
    nombres_sucios = [
        '  Juan Pérez  ', 'ANA GARCÍA', 'pedro lópez', 'MARÍA DEL CARMEN',
        'José María', '  carlos ruiz  ', 'Ana María', 'Pedro-José',
        'María José', 'Carlos', 'Ana', 'Pedro', '  LUIS MARTÍNEZ  ',
        'carmen garcía', 'JOSÉ ANTONIO', '  maría  ', 'Francisco',
        'Isabel', 'Miguel', 'Laura', 'David', 'Cristina', 'Antonio'
    ]
    
    # Emails con problemas
    emails_sucios = [
        'JUAN@GMAIL.COM', 'ana@Yahoo.es  ', 'pedro@hotmail', 'maria@',
        'jose@empresa.com', '  luis@correo.es  ', 'carlos@', 'ana@yahoo',
        'maria@empresa.co.uk', 'pedro@hotmail.com', 'jose@', 'luis@correo',
        'CARLOS@GMAIL.COM', '  isabel@yahoo.es  ', 'miguel@', 'laura@empresa',
        'david@correo.com', 'cristina@hotmail', 'antonio@', 'francisco@empresa'
    ]
    
    # Teléfonos con diferentes formatos
    telefonos_sucios = [
        '+34-666-123-456', '666 123 456', '666.123.456', '34666123456',
        '0034-666-123-456', '666123456', '666-123-456', '6661234567',
        '555-123-456', '123456789', '666-123-45', '666-123-4567',
        '+34-611-234-567', '611 234 567', '611.234.567', '34611234567',
        '0034-611-234-567', '611234567', '611-234-567', '6112345678'
    ]
    
    # Direcciones con problemas
    direcciones_sucias = [
        'C/ Mayor, 123', 'Av. de la Constitución, 45', 'Pl. España, 1',
        'Calle del Sol, 67', 'Avenida de la Paz, 89', 'Plaza Mayor, 12',
        'C/ San Juan, 34', 'Avda. de la Libertad, 56', 'Pl. de la Iglesia, 78',
        'Calle Real, 90', 'Avenida Central, 11', 'Plaza Nueva, 22',
        'C/ Gran Vía, 100', 'Av. de la Castellana, 200', 'Pl. de Cibeles, 1',
        'Calle Alcalá, 50', 'Avenida de América, 75', 'Plaza de España, 3'
    ]
    
    # Generar datos
    datos = []
    for i in range(100):
        datos.append({
            'cliente_id': f'CLI-{i+1:03d}',
            'nombre': random.choice(nombres_sucios),
            'email': random.choice(emails_sucios),
            'telefono': random.choice(telefonos_sucios),
            'direccion': random.choice(direcciones_sucias),
            'edad': random.randint(18, 80),
            'fecha_registro': (datetime.now() - timedelta(days=random.randint(1, 1000))).strftime('%Y-%m-%d'),
            'ultima_compra': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d') if random.random() > 0.3 else None,
            'total_compras': round(random.uniform(0, 5000), 2) if random.random() > 0.3 else 0
        })
    
    return pd.DataFrame(datos)

def crear_dataset_temporal():
    """Crea dataset temporal con problemas típicos"""
    np.random.seed(42)
    
    # Crear fechas base con gaps intencionales
    fechas_base = []
    fecha_inicio = datetime(2023, 1, 1, 0, 0, 0)
    
    for i in range(100):
        # Crear gaps intencionales
        if i % 10 == 0:
            fecha_inicio += timedelta(hours=random.randint(1, 6))
        else:
            fecha_inicio += timedelta(hours=2)
        
        fechas_base.append(fecha_inicio)
    
    # Agregar fechas en formato diferente
    fechas_mixtas = []
    for fecha in fechas_base:
        if random.random() > 0.7:  # 30% en formato diferente
            fechas_mixtas.append(fecha.strftime('%d/%m/%Y %H:%M:%S'))
        else:
            fechas_mixtas.append(fecha.strftime('%Y-%m-%d %H:%M:%S'))
    
    # Generar datos meteorológicos con tendencias
    datos = []
    temperatura_base = 20
    humedad_base = 65
    presion_base = 1013
    
    for i, fecha_str in enumerate(fechas_mixtas):
        # Simular tendencia diaria
        hora = datetime.strptime(fecha_str.split()[1], '%H:%M:%S').hour
        factor_diario = np.sin((hora - 6) * np.pi / 12) if 6 <= hora <= 18 else 0
        
        # Simular ruido
        ruido_temp = np.random.normal(0, 2)
        ruido_hum = np.random.normal(0, 3)
        ruido_pres = np.random.normal(0, 0.5)
        
        datos.append({
            'timestamp': fecha_str,
            'temperatura': round(temperatura_base + factor_diario * 5 + ruido_temp, 1),
            'humedad': max(0, min(100, round(humedad_base + factor_diario * 10 + ruido_hum))),
            'presion': round(presion_base + factor_diario * 2 + ruido_pres, 1),
            'zona_horaria': 'Europe/Madrid',
            'estacion': 'invierno' if i < 25 else 'primavera' if i < 50 else 'verano' if i < 75 else 'otoño'
        })
    
    return pd.DataFrame(datos)

def crear_dataset_outliers():
    """Crea dataset con outliers para demostración"""
    np.random.seed(42)
    
    # Datos normales
    n_normal = 200
    datos_normales = {
        'precio': np.random.normal(50, 15, n_normal),
        'cantidad': np.random.poisson(5, n_normal),
        'descuento': np.random.beta(2, 5, n_normal),
        'edad_cliente': np.random.normal(35, 10, n_normal),
        'satisfaccion': np.random.normal(4.0, 0.8, n_normal)
    }
    
    # Agregar outliers intencionalmente
    outliers = {
        'precio': [1000, 2000, 5, 3000, 1500, 2500],
        'cantidad': [1, 1, 50, 1, 100, 2],
        'descuento': [0.9, 0.95, 0.1, 0.99, 0.05, 0.98],
        'edad_cliente': [120, 5, 200, 0, 150, 2],
        'satisfaccion': [1.0, 1.5, 5.0, 0.5, 1.2, 4.9]
    }
    
    # Combinar datos
    df_normales = pd.DataFrame(datos_normales)
    df_outliers = pd.DataFrame(outliers)
    
    df_completo = pd.concat([df_normales, df_outliers], ignore_index=True)
    df_completo['id'] = range(len(df_completo))
    df_completo['tipo'] = ['normal'] * n_normal + ['outlier'] * len(outliers['precio'])
    
    return df_completo

def guardar_datasets():
    """Guarda todos los datasets en archivos CSV"""
    print("📊 Creando datasets de demostración...")
    
    # Crear datasets
    df_ecommerce = crear_dataset_ecommerce()
    df_clientes = crear_dataset_clientes()
    df_temporal = crear_dataset_temporal()
    df_outliers = crear_dataset_outliers()
    
    # Guardar en CSV
    df_ecommerce.to_csv('datos_ejemplo/ecommerce_sucio.csv', index=False, encoding='utf-8')
    df_clientes.to_csv('datos_ejemplo/clientes_sucio.csv', index=False, encoding='utf-8')
    df_temporal.to_csv('datos_ejemplo/temporal_sucio.csv', index=False, encoding='utf-8')
    df_outliers.to_csv('datos_ejemplo/outliers_demo.csv', index=False, encoding='utf-8')
    
    # Crear archivo de metadatos
    metadatos = {
        'ecommerce_sucio.csv': {
            'descripcion': 'Dataset de e-commerce con precios en múltiples monedas, categorías inconsistentes y descripciones HTML',
            'problemas': ['Precios en diferentes monedas', 'Categorías inconsistentes', 'Descripciones con HTML', 'SKUs no validados'],
            'filas': len(df_ecommerce),
            'columnas': list(df_ecommerce.columns)
        },
        'clientes_sucio.csv': {
            'descripcion': 'Dataset de clientes con datos de contacto inconsistentes y formatos mixtos',
            'problemas': ['Nombres con espacios extra', 'Emails en mayúsculas', 'Teléfonos en diferentes formatos', 'Direcciones inconsistentes'],
            'filas': len(df_clientes),
            'columnas': list(df_clientes.columns)
        },
        'temporal_sucio.csv': {
            'descripcion': 'Dataset temporal con fechas en diferentes formatos y gaps temporales',
            'problemas': ['Fechas en diferentes formatos', 'Gaps temporales', 'Zona horaria inconsistente', 'Frecuencia irregular'],
            'filas': len(df_temporal),
            'columnas': list(df_temporal.columns)
        },
        'outliers_demo.csv': {
            'descripcion': 'Dataset con outliers intencionales para demostrar técnicas de detección',
            'problemas': ['Outliers univariados', 'Outliers multivariados', 'Valores extremos', 'Datos inconsistentes'],
            'filas': len(df_outliers),
            'columnas': list(df_outliers.columns)
        }
    }
    
    with open('datos_ejemplo/metadatos.json', 'w', encoding='utf-8') as f:
        json.dump(metadatos, f, indent=2, ensure_ascii=False)
    
    print("✅ Datasets creados exitosamente:")
    print(f"  📦 ecommerce_sucio.csv: {len(df_ecommerce)} filas")
    print(f"  👥 clientes_sucio.csv: {len(df_clientes)} filas")
    print(f"  ⏰ temporal_sucio.csv: {len(df_temporal)} filas")
    print(f"  📈 outliers_demo.csv: {len(df_outliers)} filas")
    print(f"  📋 metadatos.json: Información detallada")
    
    return metadatos

if __name__ == "__main__":
    metadatos = guardar_datasets()
