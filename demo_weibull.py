"""
DEMO DE LA APLICACIÓN EDUCATIVA DE WEIBULL
==========================================

Esta es una demostración automática de la aplicación educativa completa.
Ejecuta todas las actividades con ciudades preseleccionadas para mostrar
el funcionamiento paso a paso.
"""

from analisis_weibull_educativo import AnalisisWeibullEducativo
import numpy as np

def demo_aplicacion():
    """Demostración automática de la aplicación"""
    
    # Crear instancia
    analizador = AnalisisWeibullEducativo("Datos.xlsx")
    
    # Mostrar bienvenida
    analizador.mostrar_bienvenida()
    
    # Cargar datos
    if not analizador.cargar_datos():
        print("❌ Error al cargar datos")
        return
    
    # Selección automática de ciudades para demo
    print("\n🎯 DEMO: SELECCIÓN AUTOMÁTICA DE CIUDADES")
    print("=" * 50)
    analizador.ciudades_seleccionadas = ["Riohacha", "Cartagena"]
    print(f"🎉 CIUDADES SELECCIONADAS PARA DEMO:")
    print(f"   1️⃣ {analizador.ciudades_seleccionadas[0]}")
    print(f"   2️⃣ {analizador.ciudades_seleccionadas[1]}")
    
    # Extraer datos
    analizador.extraer_datos_ciudades()
    
    # Ejecutar todas las actividades
    print(f"\n🚀 INICIANDO ANÁLISIS COMPLETO...")
    
    # Datos estadísticos básicos iniciales
    analizador.mostrar_estadisticos_basicos()
    
    # Semana 3
    ciudad_mayor_var = analizador.actividad_1_histogramas_y_variabilidad()
    resultados_weibull = analizador.actividad_2_parametros_weibull()
    
    # Semana 4
    analizador.actividad_3_graficar_distribucion(resultados_weibull)
    velocidades_caracteristicas = analizador.actividad_4_velocidades_caracteristicas(resultados_weibull)
    
    # Semana 5
    analizador.actividad_5_cuartiles_y_rango(resultados_weibull)
    analizador.actividad_6_probabilidad_entre_cuartiles(resultados_weibull)
    analizador.actividad_7_probabilidad_percentil60(resultados_weibull)
    
    # Mostrar resumen final en modo demo (sin pedir input)
    analizador.mostrar_resumen_final(ciudad_mayor_var, velocidades_caracteristicas, modo_demo=True)
    
    # Generar PDF automáticamente en la demo
    print(f"\n📄 GENERANDO REPORTE PDF AUTOMÁTICAMENTE...")
    archivo_pdf = analizador.generar_reporte_pdf("demo_reporte_weibull.pdf")
    
    if archivo_pdf:
        print(f"\n🎉 ¡Reporte PDF de la demo generado!")
        print(f"   📁 Archivo: {archivo_pdf}")

    print(f"\n✨ DEMO COMPLETADA - LA APLICACIÓN FUNCIONA PERFECTAMENTE ✨")
    print(f"\nPara usar la versión interactiva:")
    print(f"1. Ejecuta: analisis_weibull_educativo.py")
    print(f"2. Selecciona tus ciudades preferidas")
    print(f"3. Sigue las instrucciones paso a paso")

if __name__ == "__main__":
    demo_aplicacion()