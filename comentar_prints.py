#!/usr/bin/env python3
"""
Script para comentar todos los prints en analisis_weibull_educativo.py
"""

import re

def comentar_prints(archivo_path):
    """Comentar todas las líneas que contengan print( en el archivo"""
    
    with open(archivo_path, 'r', encoding='utf-8') as file:
        lineas = file.readlines()
    
    lineas_modificadas = []
    
    for linea in lineas:
        # Si la línea contiene print( y no está ya comentada
        if 'print(' in linea and not linea.strip().startswith('#'):
            # Mantener la indentación original y agregar #
            indentacion = len(linea) - len(linea.lstrip())
            linea_comentada = ' ' * indentacion + '# ' + linea.lstrip()
            lineas_modificadas.append(linea_comentada)
        else:
            lineas_modificadas.append(linea)
    
    # Escribir el archivo modificado
    with open(archivo_path, 'w', encoding='utf-8') as file:
        file.writelines(lineas_modificadas)
    
    print(f"✅ Todos los prints han sido comentados en {archivo_path}")

if __name__ == "__main__":
    archivo = "analisis_weibull_educativo.py"
    comentar_prints(archivo)