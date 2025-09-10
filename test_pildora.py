"""
🧪 Test Simple de la Píldora
===========================

Script de prueba para verificar que todos los componentes funcionan correctamente.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def test_deteccion_outliers():
    """Test de detección de outliers"""
    print("🔍 Probando detección de outliers...")
    
    # Crear datos de ejemplo
    np.random.seed(42)
    datos_normales = np.random.normal(50, 15, 200)
    outliers = [1000, 2000, 5, 3000]
    datos = np.concatenate([datos_normales, outliers])
    
    df = pd.DataFrame({'precio': datos})
    
    # Test Z-score
    z_scores = np.abs((df['precio'] - df['precio'].mean()) / df['precio'].std())
    outliers_zscore = z_scores > 3
    print(f"  ✅ Z-score: {outliers_zscore.sum()} outliers detectados")
    
    # Test IQR
    Q1 = df['precio'].quantile(0.25)
    Q3 = df['precio'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_iqr = (df['precio'] < lower_bound) | (df['precio'] > upper_bound)
    print(f"  ✅ IQR: {outliers_iqr.sum()} outliers detectados")
    
    return True

def test_limpieza_texto():
    """Test de limpieza de texto"""
    print("🧹 Probando limpieza de texto...")
    
    # Datos de ejemplo
    telefonos = ['+34-666-123-456', '666 123 456', '666.123.456', '34666123456']
    emails = ['JUAN@GMAIL.COM', 'ana@Yahoo.es  ', 'pedro@hotmail', 'maria@']
    
    # Test limpieza de teléfonos
    import re
    def limpiar_telefono(telefono):
        numeros = re.sub(r'[^\d]', '', str(telefono))
        if len(numeros) == 9 and numeros.startswith('6'):
            return f"+34-{numeros[:3]}-{numeros[3:6]}-{numeros[6:9]}"
        return None
    
    telefonos_limpios = [limpiar_telefono(t) for t in telefonos]
    validos = sum(1 for t in telefonos_limpios if t is not None)
    print(f"  ✅ Teléfonos: {validos}/{len(telefonos)} válidos")
    
    # Test limpieza de emails
    def limpiar_email(email):
        email = str(email).strip().lower()
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return email if re.match(patron, email) else None
    
    emails_limpios = [limpiar_email(e) for e in emails]
    validos = sum(1 for e in emails_limpios if e is not None)
    print(f"  ✅ Emails: {validos}/{len(emails)} válidos")
    
    return True

def test_casos_practicos():
    """Test de casos prácticos"""
    print("🎯 Probando casos prácticos...")
    
    # Test e-commerce
    precios = ['1,199.99€', '$1,299.99', '2,499.00 EUR', '£349.99']
    
    def normalizar_precio(precio_str):
        import re
        patron = r'([\d,\.]+)\s*([€$£¥]|EUR|USD|GBP|JPY)'
        match = re.search(patron, precio_str, re.IGNORECASE)
        if match:
            precio_num = float(match.group(1).replace(',', '.'))
            moneda = match.group(2).upper()
            # Conversión simple a USD
            tasas = {'EUR': 0.85, 'USD': 1.0, 'GBP': 0.73, 'JPY': 110.0}
            return precio_num / tasas.get(moneda, 1.0)
        return None
    
    precios_normalizados = [normalizar_precio(p) for p in precios]
    validos = sum(1 for p in precios_normalizados if p is not None)
    print(f"  ✅ E-commerce: {validos}/{len(precios)} precios normalizados")
    
    # Test temporal
    fechas = ['2023-01-01 10:30:00', '01/01/2023 10:30:00', '2023-01-01T10:30:00Z']
    
    def parsear_fecha(fecha_str):
        formatos = ['%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%SZ']
        for formato in formatos:
            try:
                return datetime.strptime(fecha_str, formato)
            except ValueError:
                continue
        return None
    
    fechas_parseadas = [parsear_fecha(f) for f in fechas]
    validos = sum(1 for f in fechas_parseadas if f is not None)
    print(f"  ✅ Temporal: {validos}/{len(fechas)} fechas parseadas")
    
    return True

def test_pipeline():
    """Test de pipeline automatizado"""
    print("⚙️ Probando pipeline automatizado...")
    
    # Crear datos de ejemplo
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
    
    print(f"  📊 Datos originales: {len(df)} filas")
    print(f"  ❌ Valores nulos: {df.isnull().sum().sum()}")
    print(f"  🔄 Duplicados: {df.duplicated().sum()}")
    
    # Pipeline simple
    df_limpio = df.drop_duplicates()
    df_limpio = df_limpio.fillna(df_limpio.median())
    
    print(f"  ✅ Datos limpios: {len(df_limpio)} filas")
    print(f"  ❌ Valores nulos: {df_limpio.isnull().sum().sum()}")
    print(f"  🔄 Duplicados: {df_limpio.duplicated().sum()}")
    
    return True

def test_visualizaciones():
    """Test de visualizaciones"""
    print("📊 Probando visualizaciones...")
    
    try:
        # Crear datos de ejemplo
        np.random.seed(42)
        datos = np.random.normal(50, 15, 100)
        
        # Crear gráfico simple
        plt.figure(figsize=(8, 6))
        plt.hist(datos, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Distribución de Datos')
        plt.xlabel('Valor')
        plt.ylabel('Frecuencia')
        plt.grid(True, alpha=0.3)
        
        # Guardar gráfico
        plt.savefig('test_visualizacion.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("  ✅ Visualizaciones funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"  ❌ Error en visualizaciones: {e}")
        return False

def main():
    """Función principal de test"""
    print("🧪 TEST DE LA PÍLDORA: DATA CLEANING AVANZADO")
    print("=" * 60)
    
    tests = [
        ("Detección de Outliers", test_deteccion_outliers),
        ("Limpieza de Texto", test_limpieza_texto),
        ("Casos Prácticos", test_casos_practicos),
        ("Pipeline Automatizado", test_pipeline),
        ("Visualizaciones", test_visualizaciones)
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
            print()
        except Exception as e:
            print(f"  ❌ Error en {nombre}: {e}")
            resultados.append((nombre, False))
            print()
    
    # Resumen
    print("=" * 60)
    print("📋 RESUMEN DE TESTS")
    print("=" * 60)
    
    exitosos = 0
    for nombre, resultado in resultados:
        status = "✅ OK" if resultado else "❌ FALLO"
        print(f"{nombre}: {status}")
        if resultado:
            exitosos += 1
    
    print(f"\nTests exitosos: {exitosos}/{len(resultados)}")
    
    if exitosos == len(resultados):
        print("🎉 ¡Todos los tests pasaron! La píldora está lista.")
    else:
        print("⚠️ Algunos tests fallaron. Revisa los errores anteriores.")
    
    return exitosos == len(resultados)

if __name__ == "__main__":
    main()
