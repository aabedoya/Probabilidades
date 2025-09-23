#!/usr/bin/env python3
"""
Script mejorado para eliminar completamente los prints y usar el demo silencioso
"""

def create_silent_demo():
    """Crear un demo que no use prints ni inputs interactivos"""
    
    content = '''#!/usr/bin/env python3
"""
Demo silencioso del análisis Weibull que genera solo PDF sin salida en terminal
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analisis_weibull_educativo import AnalisisWeibullEducativo
from datetime import datetime

def demo_silencioso():
    """Demo que genera PDF sin mostrar nada en terminal"""
    
    try:
        # Crear instancia del analizador
        analizador = AnalisisWeibullEducativo()
        
        # Cargar datos (sin salida en terminal)
        if not analizador.cargar_datos():
            return False
        
        # Seleccionar ciudades automáticamente para demo
        analizador.ciudades_seleccionadas = ['Riohacha', 'Cartagena']
        
        # Extraer datos sin mostrar en terminal
        analizador.extraer_datos_ciudades_seleccionadas()
        
        # Realizar todos los análisis
        analizador.mostrar_estadisticos_basicos()
        analizador.calcular_parametros_weibull()
        analizador.mostrar_tabla_funcion_densidad()
        
        # Actividades de todas las semanas
        analizador.actividad_1_histogramas_variabilidad()
        analizador.actividad_2_parametros_weibull()
        analizador.actividad_3_distribucion_vs_histograma()
        analizador.actividad_4_velocidades_caracteristicas(analizador.resultados)
        analizador.actividad_5_cuartiles_rango()
        analizador.actividad_6_probabilidad_cuartiles()
        analizador.actividad_7_probabilidad_percentil_60()
        
        # Generar PDF sin mostrar resumen final
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ciudades_str = "_".join(analizador.ciudades_seleccionadas)
        nombre_pdf = f"reporte_weibull_silencioso_{ciudades_str}_{timestamp}.pdf"
        
        # Generar PDF silenciosamente
        analizador.generar_reporte_pdf(nombre_pdf)
        
        # Solo mostrar confirmación de PDF generado
        print(f"✅ PDF generado exitosamente: {nombre_pdf}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en demo silencioso: {e}")
        return False

if __name__ == "__main__":
    exito = demo_silencioso()
    if exito:
        print("🎉 Demo silencioso completado exitosamente")
    else:
        print("❌ Error en el demo silencioso")
'''
    
    with open('demo_silencioso.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Demo silencioso creado: demo_silencioso.py")

if __name__ == "__main__":
    create_silent_demo()