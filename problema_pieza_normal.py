"""
Problema de Distribución Normal - Largo de una Pieza

Enunciado:
Se busca determinar la probabilidad de que al tomar una pieza y medir su largo, 
éste esté a máximo una desviación estándar de la media. El largo se distribuye 
normalmente con media 2 cm y desviación estándar de 0,05 cm.

Opciones de respuesta:
a) 1,96
b) 0,68
c) 0
d) 0,95
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math

def resolver_problema_pieza_normal():
    """
    Resuelve el problema de la pieza con distribución normal
    """
    print("="*70)
    print("PROBLEMA: LARGO DE PIEZA CON DISTRIBUCIÓN NORMAL")
    print("="*70)
    
    # Datos del problema
    mu = 2.0    # media en cm
    sigma = 0.05  # desviación estándar en cm
    
    print(f"Datos del problema:")
    print(f"- Media (μ): {mu} cm")
    print(f"- Desviación estándar (σ): {sigma} cm")
    print(f"- Distribución: Normal N({mu}, {sigma}²)")
    print()
    
    print("PREGUNTA:")
    print("¿Cuál es la probabilidad de que el largo esté a máximo")
    print("una desviación estándar de la media?")
    print()
    
    # Esto significa: P(μ - σ ≤ X ≤ μ + σ)
    limite_inferior = mu - sigma
    limite_superior = mu + sigma
    
    print("INTERPRETACIÓN MATEMÁTICA:")
    print("P(μ - σ ≤ X ≤ μ + σ)")
    print(f"P({mu} - {sigma} ≤ X ≤ {mu} + {sigma})")
    print(f"P({limite_inferior} ≤ X ≤ {limite_superior})")
    print()
    
    # Estandarización
    print("ESTANDARIZACIÓN:")
    print("Z = (X - μ) / σ")
    print("Para el límite inferior: Z₁ = (μ - σ - μ) / σ = -σ/σ = -1")
    print("Para el límite superior: Z₂ = (μ + σ - μ) / σ = σ/σ = 1")
    print()
    print("Por lo tanto: P(-1 ≤ Z ≤ 1)")
    print()
    
    # Cálculo usando distribución normal estándar
    prob_z1 = stats.norm.cdf(1) - stats.norm.cdf(-1)
    
    print("CÁLCULO CON DISTRIBUCIÓN NORMAL ESTÁNDAR:")
    print("P(-1 ≤ Z ≤ 1) = Φ(1) - Φ(-1)")
    print(f"P(-1 ≤ Z ≤ 1) = {stats.norm.cdf(1):.6f} - {stats.norm.cdf(-1):.6f}")
    print(f"P(-1 ≤ Z ≤ 1) = {prob_z1:.6f}")
    print()
    
    # Verificación con la distribución original
    prob_original = stats.norm.cdf(limite_superior, mu, sigma) - stats.norm.cdf(limite_inferior, mu, sigma)
    
    print("VERIFICACIÓN CON DISTRIBUCIÓN ORIGINAL:")
    print(f"P({limite_inferior} ≤ X ≤ {limite_superior}) = {prob_original:.6f}")
    print()
    
    # Regla empírica (68-95-99.7)
    print("REGLA EMPÍRICA (68-95-99.7):")
    print("Para cualquier distribución normal:")
    print("• ~68% de los datos están dentro de 1σ de la media")
    print("• ~95% de los datos están dentro de 2σ de la media") 
    print("• ~99.7% de los datos están dentro de 3σ de la media")
    print()
    
    # Análisis de opciones
    print("ANÁLISIS DE LAS OPCIONES:")
    opciones = {
        'a': 1.96,
        'b': 0.68,
        'c': 0.0,
        'd': 0.95
    }
    
    resultado = prob_z1
    
    for opcion, valor in opciones.items():
        diferencia = abs(valor - resultado)
        print(f"Opción {opcion}: {valor} - Diferencia: {diferencia:.4f}")
    
    # Encontrar la opción más cercana
    opcion_correcta = min(opciones.items(), key=lambda x: abs(x[1] - resultado))
    print(f"\nLa opción más cercana es: {opcion_correcta[0]} ({opcion_correcta[1]})")
    
    return resultado, mu, sigma

def explicacion_regla_empirica():
    """
    Explica la regla empírica en detalle
    """
    print("\n" + "="*70)
    print("EXPLICACIÓN DETALLADA: REGLA EMPÍRICA")
    print("="*70)
    
    print("La regla empírica (también llamada regla 68-95-99.7) establece que")
    print("para CUALQUIER distribución normal:")
    print()
    
    # Cálculos precisos
    prob_1sigma = stats.norm.cdf(1) - stats.norm.cdf(-1)
    prob_2sigma = stats.norm.cdf(2) - stats.norm.cdf(-2)
    prob_3sigma = stats.norm.cdf(3) - stats.norm.cdf(-3)
    
    print(f"• P(μ - 1σ ≤ X ≤ μ + 1σ) ≈ {prob_1sigma:.4f} ≈ 68%")
    print(f"• P(μ - 2σ ≤ X ≤ μ + 2σ) ≈ {prob_2sigma:.4f} ≈ 95%")
    print(f"• P(μ - 3σ ≤ X ≤ μ + 3σ) ≈ {prob_3sigma:.6f} ≈ 99.7%")
    print()
    
    print("VALORES EXACTOS:")
    print(f"• 1σ: {prob_1sigma:.6f}")
    print(f"• 2σ: {prob_2sigma:.6f}")
    print(f"• 3σ: {prob_3sigma:.6f}")
    print()
    
    print("NOTA IMPORTANTE:")
    print("El valor 1.96 en las opciones corresponde al valor Z crítico")
    print("para un nivel de confianza del 95% (α = 0.05), no a una probabilidad.")
    print("P(-1.96 ≤ Z ≤ 1.96) ≈ 0.95")

def graficar_distribucion_normal(mu, sigma):
    """
    Grafica la distribución normal y marca las áreas relevantes
    """
    # Crear rango de valores
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    y = stats.norm.pdf(x, mu, sigma)
    
    # Crear la gráfica
    plt.figure(figsize=(12, 8))
    
    # Gráfica principal
    plt.plot(x, y, 'b-', linewidth=2, label=f'N({mu}, {sigma}²)')
    
    # Sombrear área dentro de 1σ
    x_fill = x[(x >= mu - sigma) & (x <= mu + sigma)]
    y_fill = stats.norm.pdf(x_fill, mu, sigma)
    plt.fill_between(x_fill, y_fill, alpha=0.3, color='red', 
                     label='Área dentro de 1σ (≈68%)')
    
    # Líneas verticales
    plt.axvline(x=mu, color='black', linestyle='-', alpha=0.8, label=f'Media = {mu}')
    plt.axvline(x=mu - sigma, color='red', linestyle='--', alpha=0.8, 
                label=f'μ - σ = {mu - sigma}')
    plt.axvline(x=mu + sigma, color='red', linestyle='--', alpha=0.8, 
                label=f'μ + σ = {mu + sigma}')
    
    # Líneas para 2σ y 3σ
    plt.axvline(x=mu - 2*sigma, color='orange', linestyle=':', alpha=0.6, 
                label=f'μ - 2σ = {mu - 2*sigma}')
    plt.axvline(x=mu + 2*sigma, color='orange', linestyle=':', alpha=0.6, 
                label=f'μ + 2σ = {mu + 2*sigma}')
    
    plt.xlabel('Largo (cm)')
    plt.ylabel('Densidad de probabilidad')
    plt.title('Distribución Normal del Largo de la Pieza')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Agregar texto con la probabilidad
    prob = stats.norm.cdf(1) - stats.norm.cdf(-1)
    plt.text(mu, max(y)*0.8, f'P(μ-σ ≤ X ≤ μ+σ) = {prob:.4f}', 
             ha='center', va='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    return plt

def comparacion_valores_criticos():
    """
    Compara diferentes valores críticos comunes
    """
    print("\n" + "="*70)
    print("COMPARACIÓN DE VALORES CRÍTICOS COMUNES")
    print("="*70)
    
    valores_z = [1, 1.645, 1.96, 2, 2.576, 3]
    nombres = ["1σ", "90% confianza", "95% confianza", "2σ", "99% confianza", "3σ"]
    
    print("Valor Z\tNombre\t\t\tP(-Z ≤ Z ≤ Z)")
    print("-" * 50)
    
    for z, nombre in zip(valores_z, nombres):
        prob = stats.norm.cdf(z) - stats.norm.cdf(-z)
        print(f"{z}\t{nombre:<15}\t{prob:.6f}")

if __name__ == "__main__":
    # Resolver el problema principal
    resultado, mu, sigma = resolver_problema_pieza_normal()
    
    # Explicación de la regla empírica
    explicacion_regla_empirica()
    
    # Comparación de valores críticos
    comparacion_valores_criticos()
    
    # Crear gráfica
    print("\nGenerando gráfica...")
    graficar_distribucion_normal(mu, sigma)
    
    print("\n" + "="*70)
    print("CONCLUSIÓN FINAL")
    print("="*70)
    print(f"La probabilidad de que el largo esté a máximo una desviación")
    print(f"estándar de la media es: {resultado:.4f}")
    print()
    print("RESPUESTA CORRECTA: b) 0,68")
    print()
    print("EXPLICACIÓN:")
    print("Este es un resultado fundamental de la regla empírica para")
    print("distribuciones normales: aproximadamente 68% de los datos")
    print("caen dentro de una desviación estándar de la media.")
    print("="*70)