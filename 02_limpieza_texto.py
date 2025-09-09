"""
Limpieza Avanzada de Texto en Python
====================================

Este módulo demuestra técnicas avanzadas para limpiar datos de texto:
1. Expresiones regulares (regex) para patrones complejos
2. Normalización de nombres, direcciones, teléfonos
3. Manejo de encoding (UTF-8, Latin-1)
4. Validación de formatos de datos
"""

import pandas as pd
import numpy as np
import re
import unicodedata
from typing import Optional, List, Dict
import warnings
warnings.filterwarnings('ignore')

class LimpiadorTexto:
    """Clase para limpiar y normalizar datos de texto"""
    
    def __init__(self):
        self.patrones = self._definir_patrones()
    
    def _definir_patrones(self) -> Dict[str, str]:
        """Define patrones regex para diferentes tipos de datos"""
        return {
            'telefono_espana': r'^(\+34|0034|34)?[6-9]\d{8}$',
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'dni': r'^\d{8}[TRWAGMYFPDXBNJZSQVHLCKE]$',
            'codigo_postal': r'^\d{5}$',
            'fecha_es': r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$',
            'url': r'^https?://[^\s/$.?#].[^\s]*$'
        }
    
    def limpiar_telefono(self, telefono: str) -> Optional[str]:
        """
        Limpia y normaliza números de teléfono españoles
        
        Args:
            telefono: Número de teléfono en cualquier formato
            
        Returns:
            Teléfono normalizado o None si no es válido
        """
        if pd.isna(telefono) or not isinstance(telefono, str):
            return None
        
        # Extraer solo números
        numeros = re.sub(r'[^\d]', '', str(telefono))
        
        # Validar longitud
        if len(numeros) < 9 or len(numeros) > 11:
            return None
        
        # Normalizar formato español
        if numeros.startswith('34'):
            numeros = numeros[2:]
        elif numeros.startswith('0034'):
            numeros = numeros[4:]
        
        # Verificar que empiece por 6, 7, 8 o 9
        if not re.match(r'^[6-9]', numeros):
            return None
        
        # Formatear como +34-XXX-XXX-XXX
        if len(numeros) == 9:
            return f"+34-{numeros[:3]}-{numeros[3:6]}-{numeros[6:9]}"
        
        return None
    
    def limpiar_email(self, email: str) -> Optional[str]:
        """
        Limpia y valida direcciones de email
        
        Args:
            email: Dirección de email a limpiar
            
        Returns:
            Email limpio y normalizado o None si no es válido
        """
        if pd.isna(email) or not isinstance(email, str):
            return None
        
        # Limpiar espacios y convertir a minúsculas
        email = str(email).strip().lower()
        
        # Validar formato
        if not re.match(self.patrones['email'], email):
            return None
        
        return email
    
    def limpiar_nombre(self, nombre: str) -> Optional[str]:
        """
        Limpia y normaliza nombres de personas
        
        Args:
            nombre: Nombre a limpiar
            
        Returns:
            Nombre limpio y normalizado
        """
        if pd.isna(nombre) or not isinstance(nombre, str):
            return None
        
        # Limpiar espacios y caracteres especiales
        nombre = str(nombre).strip()
        
        # Eliminar caracteres no alfabéticos excepto espacios y guiones
        nombre = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]', '', nombre)
        
        # Normalizar espacios múltiples
        nombre = re.sub(r'\s+', ' ', nombre)
        
        # Formato título (primera letra de cada palabra en mayúscula)
        nombre = nombre.title()
        
        # Validar que no esté vacío
        if not nombre or len(nombre.strip()) < 2:
            return None
        
        return nombre
    
    def limpiar_direccion(self, direccion: str) -> Optional[str]:
        """
        Limpia y normaliza direcciones
        
        Args:
            direccion: Dirección a limpiar
            
        Returns:
            Dirección limpia y normalizada
        """
        if pd.isna(direccion) or not isinstance(direccion, str):
            return None
        
        # Limpiar espacios y caracteres especiales
        direccion = str(direccion).strip()
        
        # Eliminar caracteres de control
        direccion = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', direccion)
        
        # Normalizar espacios
        direccion = re.sub(r'\s+', ' ', direccion)
        
        # Capitalizar apropiadamente
        direccion = direccion.title()
        
        # Normalizar abreviaciones comunes
        reemplazos = {
            'C/': 'Calle ',
            'Av.': 'Avenida ',
            'Avda.': 'Avenida ',
            'Pl.': 'Plaza ',
            'Pza.': 'Plaza ',
            'Nº': 'Número ',
            'N°': 'Número '
        }
        
        for abrev, completo in reemplazos.items():
            direccion = direccion.replace(abrev, completo)
        
        return direccion if direccion else None
    
    def extraer_codigo_postal(self, texto: str) -> Optional[str]:
        """
        Extrae código postal de un texto
        
        Args:
            texto: Texto que puede contener código postal
            
        Returns:
            Código postal extraído o None
        """
        if pd.isna(texto) or not isinstance(texto, str):
            return None
        
        # Buscar patrón de 5 dígitos
        match = re.search(r'\b(\d{5})\b', str(texto))
        
        if match:
            return match.group(1)
        
        return None
    
    def normalizar_encoding(self, texto: str, encoding_original='latin-1') -> str:
        """
        Normaliza el encoding de un texto
        
        Args:
            texto: Texto a normalizar
            encoding_original: Encoding original del texto
            
        Returns:
            Texto con encoding UTF-8 normalizado
        """
        if pd.isna(texto) or not isinstance(texto, str):
            return ""
        
        try:
            # Intentar decodificar y recodificar
            texto_bytes = texto.encode(encoding_original)
            texto_utf8 = texto_bytes.decode('utf-8')
            return texto_utf8
        except (UnicodeDecodeError, UnicodeEncodeError):
            # Si falla, usar unicodedata para normalizar
            return unicodedata.normalize('NFKD', str(texto))
    
    def limpiar_html(self, texto: str) -> str:
        """
        Elimina etiquetas HTML de un texto
        
        Args:
            texto: Texto que puede contener HTML
            
        Returns:
            Texto sin etiquetas HTML
        """
        if pd.isna(texto) or not isinstance(texto, str):
            return ""
        
        # Eliminar etiquetas HTML
        texto_limpio = re.sub(r'<[^>]+>', '', str(texto))
        
        # Decodificar entidades HTML comunes
        entidades = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
            '&nbsp;': ' '
        }
        
        for entidad, caracter in entidades.items():
            texto_limpio = texto_limpio.replace(entidad, caracter)
        
        return texto_limpio.strip()
    
    def validar_dni(self, dni: str) -> bool:
        """
        Valida un DNI español
        
        Args:
            dni: DNI a validar
            
        Returns:
            True si el DNI es válido, False en caso contrario
        """
        if pd.isna(dni) or not isinstance(dni, str):
            return False
        
        dni = str(dni).strip().upper()
        
        # Verificar formato
        if not re.match(self.patrones['dni'], dni):
            return False
        
        # Verificar letra de control
        letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
        numero = int(dni[:8])
        letra_calculada = letras[numero % 23]
        
        return dni[8] == letra_calculada

def crear_datos_sucios():
    """Crea un dataset con datos de texto sucios para demostración"""
    datos_sucios = {
        'telefono': [
            '+34-666-123-456', '666 123 456', '666.123.456', '34666123456',
            '0034-666-123-456', '666123456', '666-123-456', '6661234567',
            '555-123-456', '123456789', '666-123-45', '666-123-4567'
        ],
        'email': [
            'JUAN@GMAIL.COM', 'ana@Yahoo.es  ', 'pedro@hotmail', 'maria@',
            'jose@empresa.com', '  luis@correo.es  ', 'carlos@', 'ana@yahoo',
            'maria@empresa.co.uk', 'pedro@hotmail.com', 'jose@', 'luis@correo'
        ],
        'nombre': [
            '  Juan Pérez  ', 'ANA GARCÍA', 'pedro lópez', 'MARÍA DEL CARMEN',
            'José María', '  carlos ruiz  ', 'Ana María', 'Pedro-José',
            'María José', 'Carlos', 'Ana', 'Pedro'
        ],
        'direccion': [
            'C/ Mayor, 123', 'Av. de la Constitución, 45', 'Pl. España, 1',
            'Calle del Sol, 67', 'Avenida de la Paz, 89', 'Plaza Mayor, 12',
            'C/ San Juan, 34', 'Avda. de la Libertad, 56', 'Pl. de la Iglesia, 78',
            'Calle Real, 90', 'Avenida Central, 11', 'Plaza Nueva, 22'
        ],
        'descripcion_html': [
            '<p>Producto <strong>excelente</strong> calidad</p>',
            '<div>Descripción con <em>énfasis</em></div>',
            '<span>Texto normal</span>',
            '<p>Múltiples <br/> líneas</p>',
            'Sin HTML',
            '<a href="#">Enlace</a> texto',
            '<p>Precio: <b>29.99€</b></p>',
            'Texto con &amp; símbolos',
            '<div>HTML <span>anidado</span></div>',
            'Texto normal sin etiquetas',
            '<p>Con <strong>negrita</strong> y <em>cursiva</em></p>',
            'Solo texto'
        ],
        'dni': [
            '12345678Z', '87654321X', '11223344A', '99887766B',
            '12345678z', '87654321x', '11223344a', '99887766b',
            '12345678Y', '87654321W', '11223344C', '99887766D'
        ]
    }
    
    return pd.DataFrame(datos_sucios)

def demostrar_limpieza_telefonos():
    """Demuestra la limpieza de números de teléfono"""
    print("📞 LIMPIEZA DE NÚMEROS DE TELÉFONO")
    print("=" * 50)
    
    limpiador = LimpiadorTexto()
    df = crear_datos_sucios()
    
    # Limpiar teléfonos
    df['telefono_limpio'] = df['telefono'].apply(limpiador.limpiar_telefono)
    
    # Mostrar resultados
    print("Resultados de limpieza de teléfonos:")
    print(df[['telefono', 'telefono_limpio']].to_string(index=False))
    
    # Estadísticas
    validos = df['telefono_limpio'].notna().sum()
    total = len(df)
    print(f"\nTeléfonos válidos: {validos}/{total} ({validos/total*100:.1f}%)")
    
    return df

def demostrar_limpieza_emails():
    """Demuestra la limpieza de direcciones de email"""
    print("\n📧 LIMPIEZA DE DIRECCIONES DE EMAIL")
    print("=" * 50)
    
    limpiador = LimpiadorTexto()
    df = crear_datos_sucios()
    
    # Limpiar emails
    df['email_limpio'] = df['email'].apply(limpiador.limpiar_email)
    
    # Mostrar resultados
    print("Resultados de limpieza de emails:")
    print(df[['email', 'email_limpio']].to_string(index=False))
    
    # Estadísticas
    validos = df['email_limpio'].notna().sum()
    total = len(df)
    print(f"\nEmails válidos: {validos}/{total} ({validos/total*100:.1f}%)")
    
    return df

def demostrar_limpieza_nombres():
    """Demuestra la limpieza de nombres"""
    print("\n👤 LIMPIEZA DE NOMBRES")
    print("=" * 50)
    
    limpiador = LimpiadorTexto()
    df = crear_datos_sucios()
    
    # Limpiar nombres
    df['nombre_limpio'] = df['nombre'].apply(limpiador.limpiar_nombre)
    
    # Mostrar resultados
    print("Resultados de limpieza de nombres:")
    print(df[['nombre', 'nombre_limpio']].to_string(index=False))
    
    return df

def demostrar_limpieza_html():
    """Demuestra la limpieza de texto con HTML"""
    print("\n🌐 LIMPIEZA DE TEXTO CON HTML")
    print("=" * 50)
    
    limpiador = LimpiadorTexto()
    df = crear_datos_sucios()
    
    # Limpiar HTML
    df['descripcion_limpia'] = df['descripcion_html'].apply(limpiador.limpiar_html)
    
    # Mostrar resultados
    print("Resultados de limpieza de HTML:")
    for i, row in df.iterrows():
        print(f"\nOriginal: {row['descripcion_html']}")
        print(f"Limpio:   {row['descripcion_limpia']}")
        print("-" * 40)
    
    return df

def demostrar_validacion_dni():
    """Demuestra la validación de DNI"""
    print("\n🆔 VALIDACIÓN DE DNI")
    print("=" * 50)
    
    limpiador = LimpiadorTexto()
    df = crear_datos_sucios()
    
    # Validar DNIs
    df['dni_valido'] = df['dni'].apply(limpiador.validar_dni)
    
    # Mostrar resultados
    print("Resultados de validación de DNI:")
    print(df[['dni', 'dni_valido']].to_string(index=False))
    
    # Estadísticas
    validos = df['dni_valido'].sum()
    total = len(df)
    print(f"\nDNIs válidos: {validos}/{total} ({validos/total*100:.1f}%)")
    
    return df

def pipeline_limpieza_completo():
    """Demuestra un pipeline completo de limpieza de texto"""
    print("\n🚀 PIPELINE COMPLETO DE LIMPIEZA DE TEXTO")
    print("=" * 60)
    
    limpiador = LimpiadorTexto()
    df = crear_datos_sucios()
    
    print("Datos originales:")
    print(df.head().to_string())
    
    # Aplicar todas las limpiezas
    df['telefono_limpio'] = df['telefono'].apply(limpiador.limpiar_telefono)
    df['email_limpio'] = df['email'].apply(limpiador.limpiar_email)
    df['nombre_limpio'] = df['nombre'].apply(limpiador.limpiar_nombre)
    df['direccion_limpia'] = df['direccion'].apply(limpiador.limpiar_direccion)
    df['descripcion_limpia'] = df['descripcion_html'].apply(limpiador.limpiar_html)
    df['dni_valido'] = df['dni'].apply(limpiador.validar_dni)
    
    print("\nDatos limpios:")
    columnas_limpias = [col for col in df.columns if 'limpio' in col or 'valido' in col]
    print(df[columnas_limpias].head().to_string())
    
    # Resumen de calidad
    print("\n📊 RESUMEN DE CALIDAD DE DATOS:")
    print("=" * 40)
    
    for col in ['telefono_limpio', 'email_limpio', 'nombre_limpio', 'dni_valido']:
        if col in df.columns:
            if 'valido' in col:
                validos = df[col].sum()
            else:
                validos = df[col].notna().sum()
            
            total = len(df)
            porcentaje = (validos / total) * 100
            print(f"{col}: {validos}/{total} ({porcentaje:.1f}%)")
    
    return df

def main():
    """Función principal para demostrar limpieza de texto"""
    print("🧹 DEMOSTRACIÓN: LIMPIEZA AVANZADA DE TEXTO")
    print("=" * 60)
    
    # Ejecutar todas las demostraciones
    df_telefonos = demostrar_limpieza_telefonos()
    df_emails = demostrar_limpieza_emails()
    df_nombres = demostrar_limpieza_nombres()
    df_html = demostrar_limpieza_html()
    df_dni = demostrar_validacion_dni()
    
    # Pipeline completo
    df_completo = pipeline_limpieza_completo()
    
    print("\n💡 MEJORES PRÁCTICAS:")
    print("=" * 30)
    print("• Siempre validar formatos antes de limpiar")
    print("• Usar regex específicas para cada tipo de dato")
    print("• Mantener logs de transformaciones aplicadas")
    print("• Probar con datos reales antes de producción")
    print("• Documentar reglas de limpieza para el equipo")
    
    return df_completo

if __name__ == "__main__":
    # Ejecutar demostración
    resultado = main()
