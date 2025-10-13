"""
Problema de Distribución Exponencial - Microchip de Computador

Enunciado:
Se estima que el tiempo transcurrido hasta la falla de un microchip de un computador 
se distribuye exponencialmente con media de tres años. Una compañía ofrece garantía 
por el primer año de uso. ¿Qué porcentaje de pólizas tendrá que pagar una reclamación?

Opciones de respuesta:
a) 28.35%
b) 0.7189
c) 71.89%
d) 0.2835
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math

def resolver_problema_microchip():
    """
    Resuelve el problema del microchip con distribución exponencial
    """
    print("="*60)
    print("PROBLEMA: MICROCHIP CON DISTRIBUCIÓN EXPONENCIAL")
    print("="*60)
    
    # Datos del problema
    media = 3  # años
    tiempo_garantia = 1  # año
    
    print(f"Datos del problema:")
    print(f"- Media de tiempo hasta la falla: {media} años")
    print(f"- Período de garantía: {tiempo_garantia} año")
    print()
    
    # Para distribución exponencial: E[X] = 1/λ
    # Por lo tanto: λ = 1/E[X] = 1/media
    lambda_param = 1 / media
    
    print(f"Parámetro λ de la distribución exponencial:")
    print(f"λ = 1/μ = 1/{media} = {lambda_param:.4f}")
    print()
    
    # Función de densidad de probabilidad exponencial:
    # f(x) = λ * e^(-λx) para x ≥ 0
    
    # Función de distribución acumulativa:
    # F(x) = 1 - e^(-λx) para x ≥ 0
    
    # Probabilidad de falla dentro del primer año (reclamación de garantía)
    # P(X ≤ 1) = F(1) = 1 - e^(-λ*1)
    
    prob_falla_primer_año = 1 - math.exp(-lambda_param * tiempo_garantia)
    porcentaje_reclamaciones = prob_falla_primer_año * 100
    
    print("CÁLCULO DE LA PROBABILIDAD:")
    print(f"P(X ≤ {tiempo_garantia}) = 1 - e^(-λ*{tiempo_garantia})")
    print(f"P(X ≤ {tiempo_garantia}) = 1 - e^(-{lambda_param:.4f}*{tiempo_garantia})")
    print(f"P(X ≤ {tiempo_garantia}) = 1 - e^(-{lambda_param:.4f})")
    print(f"P(X ≤ {tiempo_garantia}) = 1 - {math.exp(-lambda_param):.4f}")
    print(f"P(X ≤ {tiempo_garantia}) = {prob_falla_primer_año:.4f}")
    print()
    
    print("RESULTADO:")
    print(f"Probabilidad de reclamación: {prob_falla_primer_año:.4f}")
    print(f"Porcentaje de pólizas con reclamación: {porcentaje_reclamaciones:.2f}%")
    print()
    
    # Verificación con scipy
    prob_scipy = stats.expon.cdf(tiempo_garantia, scale=media)
    print("VERIFICACIÓN CON SCIPY:")
    print(f"P(X ≤ {tiempo_garantia}) usando scipy: {prob_scipy:.4f}")
    print(f"Porcentaje usando scipy: {prob_scipy * 100:.2f}%")
    print()
    
    # Análisis de las opciones
    print("ANÁLISIS DE LAS OPCIONES:")
    opciones = {
        'a': 28.35,
        'b': 0.7189 * 100,  # Convertir a porcentaje
        'c': 71.89,
        'd': 0.2835 * 100   # Convertir a porcentaje
    }
    
    for opcion, valor in opciones.items():
        diferencia = abs(valor - porcentaje_reclamaciones)
        print(f"Opción {opcion}: {valor}% - Diferencia: {diferencia:.2f}%")
    
    # Encontrar la opción más cercana
    opcion_correcta = min(opciones.items(), key=lambda x: abs(x[1] - porcentaje_reclamaciones))
    print(f"\nLa opción más cercana es: {opcion_correcta[0]} ({opcion_correcta[1]}%)")
    
    return prob_falla_primer_año, porcentaje_reclamaciones, lambda_param

def graficar_distribucion(lambda_param, tiempo_garantia=1):
    """
    Grafica la distribución exponencial y marca el área de reclamaciones
    """
    # Crear rango de valores
    x = np.linspace(0, 10, 1000)
    y = lambda_param * np.exp(-lambda_param * x)
    
    # Crear la gráfica
    plt.figure(figsize=(12, 8))
    
    # Subplot 1: Función de densidad
    plt.subplot(2, 1, 1)
    plt.plot(x, y, 'b-', linewidth=2, label=f'f(x) = {lambda_param:.4f}e^(-{lambda_param:.4f}x)')
    
    # Sombrear área de reclamaciones (0 a 1 año)
    x_fill = x[x <= tiempo_garantia]
    y_fill = lambda_param * np.exp(-lambda_param * x_fill)
    plt.fill_between(x_fill, y_fill, alpha=0.3, color='red', 
                     label=f'Área de reclamaciones (0-{tiempo_garantia} año)')
    
    plt.axvline(x=tiempo_garantia, color='red', linestyle='--', 
                label=f'Fin de garantía ({tiempo_garantia} año)')
    plt.axvline(x=3, color='green', linestyle='--', alpha=0.7, 
                label='Media (3 años)')
    
    plt.xlabel('Tiempo hasta la falla (años)')
    plt.ylabel('Densidad de probabilidad')
    plt.title('Distribución Exponencial - Tiempo hasta falla del microchip')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Función de distribución acumulativa
    plt.subplot(2, 1, 2)
    F_x = 1 - np.exp(-lambda_param * x)
    plt.plot(x, F_x, 'g-', linewidth=2, label=f'F(x) = 1 - e^(-{lambda_param:.4f}x)')
    
    # Marcar el punto de interés
    prob_1_año = 1 - np.exp(-lambda_param * tiempo_garantia)
    plt.plot(tiempo_garantia, prob_1_año, 'ro', markersize=8, 
             label=f'P(X ≤ {tiempo_garantia}) = {prob_1_año:.4f}')
    
    plt.axhline(y=prob_1_año, color='red', linestyle=':', alpha=0.7)
    plt.axvline(x=tiempo_garantia, color='red', linestyle=':', alpha=0.7)
    
    plt.xlabel('Tiempo hasta la falla (años)')
    plt.ylabel('Probabilidad acumulada')
    plt.title('Función de Distribución Acumulativa')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return plt

def analisis_adicional(lambda_param):
    """
    Proporciona análisis adicional del problema
    """
    print("\n" + "="*60)
    print("ANÁLISIS ADICIONAL")
    print("="*60)
    
    # Probabilidad de NO tener reclamación (supervivencia al primer año)
    prob_supervivencia = math.exp(-lambda_param * 1)
    print(f"Probabilidad de NO reclamación (supervivencia): {prob_supervivencia:.4f}")
    print(f"Porcentaje de microchips que NO fallan en el primer año: {prob_supervivencia * 100:.2f}%")
    print()
    
    # Tiempo mediano (cuando F(x) = 0.5)
    tiempo_mediano = -math.log(0.5) / lambda_param
    print(f"Tiempo mediano hasta la falla: {tiempo_mediano:.2f} años")
    
    # Probabilidades en diferentes períodos
    periodos = [0.5, 1, 1.5, 2, 3, 5]
    print("\nProbabilidades de falla en diferentes períodos:")
    for t in periodos:
        prob = 1 - math.exp(-lambda_param * t)
        print(f"P(X ≤ {t} años) = {prob:.4f} ({prob*100:.2f}%)")

if __name__ == "__main__":
    # Resolver el problema principal
    prob, porcentaje, lambda_val = resolver_problema_microchip()
    
    # Crear gráfica
    print("\nGenerando gráfica...")
    graficar_distribucion(lambda_val)
    
    # Análisis adicional
    analisis_adicional(lambda_val)
    
    print("\n" + "="*60)
    print("CONCLUSIÓN FINAL")
    print("="*60)
    print(f"El porcentaje de pólizas que tendrá reclamación es: {porcentaje:.2f}%")
    print("La respuesta correcta es la opción a) 28.35%")