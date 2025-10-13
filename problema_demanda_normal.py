"""
Problema de Distribución Normal - Demanda de Producto

Enunciado:
La demanda de consumo de cierto producto sigue una distribución normal con 
media 1200 unidades y varianza 10000. ¿Cuál es la probabilidad de que las 
ventas superen las 1000 unidades?

Opciones de respuesta:
a) 0.9767
b) 0.0228
c) 0.9772
d) 0.4772
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math

def resolver_problema_demanda_normal():
    """
    Resuelve el problema de demanda con distribución normal
    """
    print("="*70)
    print("PROBLEMA: DEMANDA DE PRODUCTO CON DISTRIBUCIÓN NORMAL")
    print("="*70)
    
    # Datos del problema
    mu = 1200      # media en unidades
    varianza = 10000    # varianza
    sigma = math.sqrt(varianza)  # desviación estándar
    valor_critico = 1000  # unidades
    
    print(f"Datos del problema:")
    print(f"- Media (μ): {mu} unidades")
    print(f"- Varianza (σ²): {varianza}")
    print(f"- Desviación estándar (σ): {sigma} unidades")
    print(f"- Distribución: Normal N({mu}, {varianza})")
    print(f"- Valor crítico: {valor_critico} unidades")
    print()
    
    print("PREGUNTA:")
    print("¿Cuál es la probabilidad de que las ventas superen las 1000 unidades?")
    print("P(X > 1000) = ?")
    print()
    
    # Estandarización
    z = (valor_critico - mu) / sigma
    
    print("PASO 1: ESTANDARIZACIÓN")
    print("Z = (X - μ) / σ")
    print(f"Z = ({valor_critico} - {mu}) / {sigma}")
    print(f"Z = {valor_critico - mu} / {sigma}")
    print(f"Z = {z}")
    print()
    
    # Cálculo de la probabilidad
    print("PASO 2: CÁLCULO DE PROBABILIDAD")
    print("P(X > 1000) = P(Z > z)")
    print(f"P(X > 1000) = P(Z > {z})")
    print()
    
    # P(Z > z) = 1 - P(Z ≤ z) = 1 - Φ(z)
    prob_z_menor_igual = stats.norm.cdf(z)
    prob_x_mayor = 1 - prob_z_menor_igual
    
    print("P(Z > z) = 1 - P(Z ≤ z) = 1 - Φ(z)")
    print(f"P(Z > {z}) = 1 - Φ({z})")
    print(f"P(Z > {z}) = 1 - {prob_z_menor_igual:.6f}")
    print(f"P(Z > {z}) = {prob_x_mayor:.6f}")
    print()
    
    # Verificación directa
    prob_directa = 1 - stats.norm.cdf(valor_critico, mu, sigma)
    print("VERIFICACIÓN DIRECTA:")
    print(f"P(X > {valor_critico}) = {prob_directa:.6f}")
    print()
    
    # Análisis de opciones
    print("ANÁLISIS DE LAS OPCIONES:")
    opciones = {
        'a': 0.9767,
        'b': 0.0228,
        'c': 0.9772,
        'd': 0.4772
    }
    
    resultado = prob_x_mayor
    
    print(f"Nuestro resultado: {resultado:.6f}")
    print()
    
    for opcion, valor in opciones.items():
        diferencia = abs(valor - resultado)
        print(f"Opción {opcion}: {valor} - Diferencia: {diferencia:.6f}")
    
    # Encontrar la opción más cercana
    opcion_correcta = min(opciones.items(), key=lambda x: abs(x[1] - resultado))
    print(f"\nLa opción más cercana es: {opcion_correcta[0]} ({opcion_correcta[1]})")
    
    return resultado, mu, sigma, z

def analisis_detallado(mu, sigma, z, resultado):
    """
    Proporciona análisis adicional del problema
    """
    print("\n" + "="*70)
    print("ANÁLISIS DETALLADO")
    print("="*70)
    
    print("INTERPRETACIÓN DEL VALOR Z:")
    print(f"Z = {z} significa que 1000 unidades está {abs(z)} desviaciones")
    print("estándar POR DEBAJO de la media.")
    print("Como es un valor Z negativo, esperamos una probabilidad alta")
    print("para P(X > 1000).")
    print()
    
    # Verificación usando la tabla Z
    print("VERIFICACIÓN CON PROPIEDADES DE LA NORMAL ESTÁNDAR:")
    print(f"Φ({z}) = {stats.norm.cdf(z):.6f}")
    print(f"P(Z > {z}) = 1 - {stats.norm.cdf(z):.6f} = {resultado:.6f}")
    print()
    
    # Cálculo de percentiles
    print("ANÁLISIS DE PERCENTILES:")
    valor_1000 = stats.norm.cdf(1000, mu, sigma)
    print(f"1000 unidades corresponde al percentil {valor_1000*100:.2f}")
    print(f"Esto significa que {valor_1000*100:.2f}% de las demandas son ≤ 1000")
    print(f"Y {(1-valor_1000)*100:.2f}% de las demandas son > 1000")
    print()
    
    # Otros valores de interés
    print("OTROS VALORES DE INTERÉS:")
    valores_criticos = [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600]
    
    print("Valor\tP(X > valor)\tPercentil")
    print("-" * 35)
    for valor in valores_criticos:
        prob_mayor = 1 - stats.norm.cdf(valor, mu, sigma)
        percentil = stats.norm.cdf(valor, mu, sigma) * 100
        print(f"{valor}\t{prob_mayor:.4f}\t\t{percentil:.1f}%")

def verificacion_calculo_manual():
    """
    Verifica el cálculo paso a paso manualmente
    """
    print("\n" + "="*70)
    print("VERIFICACIÓN MANUAL DEL CÁLCULO")
    print("="*70)
    
    mu = 1200
    varianza = 10000
    sigma = 100
    x = 1000
    
    print("DATOS:")
    print(f"μ = {mu}")
    print(f"σ² = {varianza}")
    print(f"σ = √{varianza} = {sigma}")
    print(f"X = {x}")
    print()
    
    print("CÁLCULO DE Z:")
    print("Z = (X - μ) / σ")
    print(f"Z = ({x} - {mu}) / {sigma}")
    print(f"Z = {x - mu} / {sigma}")
    print(f"Z = {(x - mu) / sigma}")
    print()
    
    z_calculado = (x - mu) / sigma
    
    # Usando tabla normal estándar aproximada
    print("CONSULTA EN TABLA NORMAL ESTÁNDAR:")
    print(f"Para Z = {z_calculado}:")
    print("Φ(-2.00) ≈ 0.0228")
    print("Por lo tanto:")
    print("P(X > 1000) = P(Z > -2.00) = 1 - Φ(-2.00)")
    print("P(X > 1000) = 1 - 0.0228 = 0.9772")

def graficar_distribucion_demanda(mu, sigma, valor_critico=1000):
    """
    Grafica la distribución normal de la demanda
    """
    # Crear rango de valores
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    y = stats.norm.pdf(x, mu, sigma)
    
    # Crear la gráfica
    plt.figure(figsize=(12, 8))
    
    # Gráfica principal
    plt.plot(x, y, 'b-', linewidth=2, label=f'N({mu}, {sigma}²)')
    
    # Sombrear área P(X > 1000)
    x_fill = x[x >= valor_critico]
    y_fill = stats.norm.pdf(x_fill, mu, sigma)
    plt.fill_between(x_fill, y_fill, alpha=0.3, color='green', 
                     label=f'P(X > {valor_critico}) ≈ 0.9772')
    
    # Líneas verticales importantes
    plt.axvline(x=mu, color='red', linestyle='-', alpha=0.8, 
                label=f'Media = {mu}')
    plt.axvline(x=valor_critico, color='orange', linestyle='--', alpha=0.8, 
                label=f'Valor crítico = {valor_critico}')
    
    # Marcar desviaciones estándar
    for i in range(-3, 4):
        x_pos = mu + i * sigma
        if i != 0:
            plt.axvline(x=x_pos, color='gray', linestyle=':', alpha=0.5)
    
    plt.xlabel('Demanda (unidades)')
    plt.ylabel('Densidad de probabilidad')
    plt.title('Distribución Normal de la Demanda del Producto')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Agregar texto con la probabilidad
    prob = 1 - stats.norm.cdf(valor_critico, mu, sigma)
    plt.text(mu + sigma, max(y)*0.6, f'P(X > {valor_critico}) = {prob:.4f}', 
             ha='center', va='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    return plt

if __name__ == "__main__":
    # Resolver el problema principal
    resultado, mu, sigma, z = resolver_problema_demanda_normal()
    
    # Análisis detallado
    analisis_detallado(mu, sigma, z, resultado)
    
    # Verificación manual
    verificacion_calculo_manual()
    
    # Crear gráfica
    print("\nGenerando gráfica...")
    graficar_distribucion_demanda(mu, sigma)
    
    print("\n" + "="*70)
    print("CONCLUSIÓN FINAL")
    print("="*70)
    print(f"La probabilidad de que las ventas superen las 1000 unidades es: {resultado:.4f}")
    print()
    print("RESPUESTA CORRECTA: c) 0.9772")
    print()
    print("EXPLICACIÓN:")
    print("Con una media de 1200 y σ = 100, el valor 1000 está 2 desviaciones")
    print("estándar por debajo de la media (Z = -2.0). Esto significa que es")
    print("muy probable (97.72%) que las ventas superen las 1000 unidades.")
    print("="*70)