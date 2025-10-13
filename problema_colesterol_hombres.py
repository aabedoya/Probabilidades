"""
Problema de Distribución Normal - Niveles de Colesterol en Hombres

Información de la tabla:
- El colesterol es una grasa necesaria para el funcionamiento del cuerpo
- Un nivel alto aumenta el riesgo de enfermedades cardiovasculares
- La tabla muestra niveles normales en personas sanas

TABLA DE DATOS:
EDAD (Años) | HOMBRES                    | MUJERES
           | MEDIA | DESVIACIÓN ESTÁNDAR | MEDIA | DESVIACIÓN ESTÁNDAR
           | (mg/dL)| (mg/dL)            | (mg/dL)| (mg/dL)
< 20       | 165   | 9                  | 160   | 8
20-40      | 200   | 25                 | 190   | 15
>40        | 210   | 20                 | 195   | 10

PREGUNTA:
¿Cuál es la probabilidad de que al seleccionar un hombre al azar de 35 años 
tenga un nivel de colesterol superior a 195 mg/dL?

Opciones de respuesta:
a) 0.6306
b) 0.3694
c) 0.4207
d) 0.5793
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math

def resolver_problema_colesterol():
    """
    Resuelve el problema del colesterol en hombres de 35 años
    """
    print("="*75)
    print("PROBLEMA: NIVELES DE COLESTEROL EN HOMBRES")
    print("="*75)
    
    # Identificar el grupo de edad para 35 años
    print("PASO 1: IDENTIFICAR EL GRUPO DE EDAD")
    print("Hombre de 35 años → Grupo 20-40 años")
    print()
    
    # Datos del problema para hombres de 20-40 años
    mu = 200      # media en mg/dL
    sigma = 25    # desviación estándar en mg/dL
    valor_critico = 195  # mg/dL
    
    print("PASO 2: EXTRAER PARÁMETROS DE LA TABLA")
    print(f"Para hombres de 20-40 años:")
    print(f"- Media (μ): {mu} mg/dL")
    print(f"- Desviación estándar (σ): {sigma} mg/dL")
    print(f"- Distribución: Normal N({mu}, {sigma}²)")
    print(f"- Valor crítico: {valor_critico} mg/dL")
    print()
    
    print("PREGUNTA:")
    print(f"¿P(X > {valor_critico}) = ?")
    print("donde X = nivel de colesterol de un hombre de 35 años")
    print()
    
    # Estandarización
    z = (valor_critico - mu) / sigma
    
    print("PASO 3: ESTANDARIZACIÓN")
    print("Z = (X - μ) / σ")
    print(f"Z = ({valor_critico} - {mu}) / {sigma}")
    print(f"Z = {valor_critico - mu} / {sigma}")
    print(f"Z = {z}")
    print()
    
    # Cálculo de la probabilidad
    print("PASO 4: CÁLCULO DE PROBABILIDAD")
    print(f"P(X > {valor_critico}) = P(Z > {z})")
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
    print("PASO 5: ANÁLISIS DE LAS OPCIONES")
    opciones = {
        'a': 0.6306,
        'b': 0.3694,
        'c': 0.4207,
        'd': 0.5793
    }
    
    resultado = prob_x_mayor
    
    print(f"Nuestro resultado: {resultado:.6f}")
    print()
    
    diferencias = []
    for opcion, valor in opciones.items():
        diferencia = abs(valor - resultado)
        diferencias.append((opcion, valor, diferencia))
        print(f"Opción {opcion}: {valor} - Diferencia: {diferencia:.6f}")
    
    # Encontrar la opción más cercana
    opcion_correcta = min(diferencias, key=lambda x: x[2])
    print(f"\nLa opción más cercana es: {opcion_correcta[0]} ({opcion_correcta[1]})")
    
    return resultado, mu, sigma, z, opcion_correcta

def verificacion_manual():
    """
    Verificación manual del cálculo
    """
    print("\n" + "="*75)
    print("VERIFICACIÓN MANUAL")
    print("="*75)
    
    mu = 200
    sigma = 25
    x = 195
    
    print("DATOS:")
    print(f"μ = {mu} mg/dL")
    print(f"σ = {sigma} mg/dL")
    print(f"X = {x} mg/dL")
    print()
    
    print("CÁLCULO DE Z:")
    z = (x - mu) / sigma
    print(f"Z = ({x} - {mu}) / {sigma} = {x - mu} / {sigma} = {z}")
    print()
    
    print("INTERPRETACIÓN:")
    print(f"Z = {z} significa que {x} mg/dL está {abs(z)} desviaciones estándar")
    print("POR DEBAJO de la media.")
    print("Como es un valor Z negativo, esperamos una probabilidad ALTA")
    print(f"para P(X > {x}).")
    print()
    
    print("TABLA NORMAL ESTÁNDAR:")
    print(f"Para Z = {z}:")
    phi_z = stats.norm.cdf(z)
    print(f"Φ({z}) = {phi_z:.6f}")
    print(f"P(Z > {z}) = 1 - {phi_z:.6f} = {1 - phi_z:.6f}")

def analisis_contextual():
    """
    Análisis contextual del problema
    """
    print("\n" + "="*75)
    print("ANÁLISIS CONTEXTUAL")
    print("="*75)
    
    print("INTERPRETACIÓN MÉDICA:")
    print("• El nivel promedio de colesterol en hombres de 20-40 años es 200 mg/dL")
    print("• Un nivel de 195 mg/dL está LIGERAMENTE por debajo del promedio")
    print("• Solo 0.2 desviaciones estándar por debajo de la media")
    print("• Por tanto, es MUY PROBABLE que un hombre tenga > 195 mg/dL")
    print()
    
    # Calcular algunos percentiles
    mu, sigma = 200, 25
    valores = [175, 185, 195, 200, 205, 215, 225]
    
    print("TABLA DE PROBABILIDADES:")
    print("Valor (mg/dL)\tP(X > valor)\tPercentil")
    print("-" * 45)
    for valor in valores:
        prob_mayor = 1 - stats.norm.cdf(valor, mu, sigma)
        percentil = stats.norm.cdf(valor, mu, sigma) * 100
        print(f"{valor}\t\t{prob_mayor:.4f}\t\t{percentil:.1f}%")

def verificar_opcion_complementaria(resultado):
    """
    Verifica si alguna opción corresponde a la probabilidad complementaria
    """
    print("\n" + "="*75)
    print("VERIFICACIÓN DE PROBABILIDAD COMPLEMENTARIA")
    print("="*75)
    
    prob_complementaria = 1 - resultado
    print(f"P(X ≤ 195) = 1 - P(X > 195) = 1 - {resultado:.6f} = {prob_complementaria:.6f}")
    print()
    
    opciones = {
        'a': 0.6306,
        'b': 0.3694,
        'c': 0.4207,
        'd': 0.5793
    }
    
    print("COMPARACIÓN CON LAS OPCIONES:")
    print(f"P(X > 195) = {resultado:.6f}")
    print(f"P(X ≤ 195) = {prob_complementaria:.6f}")
    print()
    
    for opcion, valor in opciones.items():
        diff_mayor = abs(valor - resultado)
        diff_menor = abs(valor - prob_complementaria)
        
        if diff_mayor < 0.01:
            print(f"Opción {opcion}: {valor} ≈ P(X > 195) ✓")
        elif diff_menor < 0.01:
            print(f"Opción {opcion}: {valor} ≈ P(X ≤ 195)")
        else:
            print(f"Opción {opcion}: {valor} (no coincide)")

def graficar_distribucion_colesterol(mu, sigma, valor_critico=195):
    """
    Grafica la distribución del colesterol
    """
    # Crear rango de valores
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    y = stats.norm.pdf(x, mu, sigma)
    
    # Crear la gráfica
    plt.figure(figsize=(12, 8))
    
    # Gráfica principal
    plt.plot(x, y, 'b-', linewidth=2, label=f'N({mu}, {sigma}²)')
    
    # Sombrear área P(X > 195)
    x_fill = x[x >= valor_critico]
    y_fill = stats.norm.pdf(x_fill, mu, sigma)
    plt.fill_between(x_fill, y_fill, alpha=0.3, color='red', 
                     label=f'P(X > {valor_critico}) ≈ 0.5793')
    
    # Líneas verticales importantes
    plt.axvline(x=mu, color='green', linestyle='-', alpha=0.8, 
                label=f'Media = {mu} mg/dL')
    plt.axvline(x=valor_critico, color='red', linestyle='--', alpha=0.8, 
                label=f'Valor crítico = {valor_critico} mg/dL')
    
    # Marcar desviaciones estándar
    for i in range(-3, 4):
        x_pos = mu + i * sigma
        if i != 0:
            plt.axvline(x=x_pos, color='gray', linestyle=':', alpha=0.3)
    
    plt.xlabel('Nivel de Colesterol (mg/dL)')
    plt.ylabel('Densidad de probabilidad')
    plt.title('Distribución Normal del Colesterol en Hombres de 20-40 años')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Agregar texto con la probabilidad
    prob = 1 - stats.norm.cdf(valor_critico, mu, sigma)
    plt.text(mu - 0.5*sigma, max(y)*0.7, f'P(X > {valor_critico}) = {prob:.4f}', 
             ha='center', va='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    return plt

if __name__ == "__main__":
    # Resolver el problema principal
    resultado, mu, sigma, z, opcion_correcta = resolver_problema_colesterol()
    
    # Verificación manual
    verificacion_manual()
    
    # Análisis contextual
    analisis_contextual()
    
    # Verificar probabilidad complementaria
    verificar_opcion_complementaria(resultado)
    
    # Crear gráfica
    print("\nGenerando gráfica...")
    graficar_distribucion_colesterol(mu, sigma)
    
    print("\n" + "="*75)
    print("CONCLUSIÓN FINAL")
    print("="*75)
    print(f"La probabilidad de que un hombre de 35 años tenga")
    print(f"colesterol superior a 195 mg/dL es: {resultado:.6f}")
    print()
    print(f"RESPUESTA CORRECTA: {opcion_correcta[0]}) {opcion_correcta[1]}")
    print()
    print("EXPLICACIÓN:")
    print("195 mg/dL está ligeramente por debajo de la media (200 mg/dL),")
    print("por lo que es muy probable que un hombre supere este nivel.")
    print("="*75)