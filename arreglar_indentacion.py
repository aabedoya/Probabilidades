#!/usr/bin/env python3
"""
Script para arreglar los problemas de indentación después de comentar los prints
"""

import re

def arreglar_indentacion(archivo_path):
    """Arreglar bloques que se quedaron vacíos después de comentar prints"""
    
    with open(archivo_path, 'r', encoding='utf-8') as file:
        lineas = file.readlines()
    
    lineas_modificadas = []
    i = 0
    
    while i < len(lineas):
        linea_actual = lineas[i]
        lineas_modificadas.append(linea_actual)
        
        # Buscar patrones que requieren indentación
        if (re.match(r'^\s*(if|elif|else|try|except|for|while|with|def|class).*:$', linea_actual.strip()) and 
            linea_actual.strip().endswith(':')):
            
            # Encontrar la indentación esperada para el bloque
            indentacion_linea = len(linea_actual) - len(linea_actual.lstrip())
            indentacion_bloque = indentacion_linea + 4
            
            # Verificar si la siguiente línea está correctamente indentada
            if i + 1 < len(lineas):
                siguiente_linea = lineas[i + 1]
                
                # Si la siguiente línea está vacía o es un comentario sin indentación adecuada
                if (siguiente_linea.strip() == '' or 
                    (siguiente_linea.strip().startswith('#') and 
                     len(siguiente_linea) - len(siguiente_linea.lstrip()) <= indentacion_linea)):
                    
                    # Buscar si hay contenido real en el bloque
                    j = i + 1
                    hay_contenido = False
                    
                    while j < len(lineas):
                        linea_siguiente = lineas[j]
                        if linea_siguiente.strip() == '':
                            j += 1
                            continue
                        
                        indentacion_siguiente = len(linea_siguiente) - len(linea_siguiente.lstrip())
                        
                        # Si la línea tiene la indentación esperada y no es solo comentario
                        if (indentacion_siguiente >= indentacion_bloque and 
                            not linea_siguiente.strip().startswith('#')):
                            hay_contenido = True
                            break
                        # Si encontramos una línea con menor indentación, terminamos el bloque
                        elif indentacion_siguiente <= indentacion_linea:
                            break
                        
                        j += 1
                    
                    # Si no hay contenido real, agregar pass
                    if not hay_contenido:
                        pass_line = ' ' * indentacion_bloque + 'pass\n'
                        # Insertar pass en la posición correcta
                        lineas_modificadas.append(pass_line)
        
        i += 1
    
    # Escribir el archivo modificado
    with open(archivo_path, 'w', encoding='utf-8') as file:
        file.writelines(lineas_modificadas)
    
    print(f"✅ Problemas de indentación arreglados en {archivo_path}")

if __name__ == "__main__":
    archivo = "analisis_weibull_educativo.py"
    arreglar_indentacion(archivo)