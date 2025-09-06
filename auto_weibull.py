#!/usr/bin/env python3
"""
Auto-configurador para el Proyecto Weibull
==========================================

Este script maneja automáticamente la creación y activación
del entorno virtual, simplificando el uso del proyecto.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def detectar_python():
    """Detectar la versión de Python disponible"""
    comandos_python = ['python', 'python3', 'py']
    
    for cmd in comandos_python:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ Python detectado: {version}")
                return cmd
        except FileNotFoundError:
            continue
    
    print("❌ Python no encontrado en el sistema")
    sys.exit(1)


def crear_entorno_virtual(python_cmd):
    """Crear entorno virtual si no existe"""
    venv_path = Path('.venv')
    
    if not venv_path.exists():
        print("🔧 Creando entorno virtual...")
        try:
            subprocess.run([python_cmd, '-m', 'venv', '.venv'], check=True)
            print("✅ Entorno virtual creado exitosamente")
        except subprocess.CalledProcessError:
            print("❌ Error al crear entorno virtual")
            sys.exit(1)
    else:
        print("✅ Entorno virtual ya existe")


def obtener_python_venv():
    """Obtener ruta del Python del entorno virtual"""
    sistema = platform.system()
    
    if sistema == "Windows":
        return Path('.venv/Scripts/python.exe')
    else:
        return Path('.venv/bin/python')


def verificar_dependencias(python_venv):
    """Verificar e instalar dependencias necesarias"""
    dependencias = [
        'pandas', 'numpy', 'scipy', 
        'matplotlib', 'seaborn', 'openpyxl'
    ]
    
    print("🔍 Verificando dependencias...")
    
    for dep in dependencias:
        try:
            subprocess.run([str(python_venv), '-c', f'import {dep}'], 
                         check=True, capture_output=True)
            print(f"  ✅ {dep}")
        except subprocess.CalledProcessError:
            print(f"  ❌ {dep} - Instalando...")
            try:
                subprocess.run([str(python_venv), '-m', 'pip', 'install', dep], 
                             check=True, capture_output=True)
                print(f"  ✅ {dep} instalado")
            except subprocess.CalledProcessError:
                print(f"  ❌ Error instalando {dep}")
                return False
    
    return True


def ejecutar_analisis(python_venv, argumentos):
    """Ejecutar el análisis principal"""
    script_principal = 'analisis_detallado_sustitucion.py'
    
    if not Path(script_principal).exists():
        print(f"❌ Archivo {script_principal} no encontrado")
        return False
    
    print("🚀 Ejecutando análisis Weibull...")
    print("=" * 50)
    
    try:
        # Ejecutar con argumentos pasados al script
        cmd = [str(python_venv), script_principal] + argumentos
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando análisis: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⚠️ Ejecución interrumpida por el usuario")
        return False


def main():
    """Función principal del auto-configurador"""
    print("🌪️ AUTO-CONFIGURADOR PROYECTO WEIBULL")
    print("=" * 40)
    
    # 1. Detectar Python
    python_cmd = detectar_python()
    
    # 2. Crear entorno virtual
    crear_entorno_virtual(python_cmd)
    
    # 3. Obtener Python del entorno virtual
    python_venv = obtener_python_venv()
    
    if not python_venv.exists():
        print("❌ No se pudo acceder al Python del entorno virtual")
        sys.exit(1)
    
    # 4. Verificar/instalar dependencias
    if not verificar_dependencias(python_venv):
        print("❌ Error en instalación de dependencias")
        sys.exit(1)
    
    # 5. Ejecutar análisis con argumentos de línea de comandos
    argumentos = sys.argv[1:]  # Todo excepto el nombre del script
    
    if ejecutar_analisis(python_venv, argumentos):
        print("\n🎉 ¡Análisis completado exitosamente!")
    else:
        print("\n❌ El análisis terminó con errores")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
