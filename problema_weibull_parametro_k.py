"""
Problema de Distribución de Weibull - Parámetro k
Calcular el parámetro k de la distribución de Weibull para datos de velocidad del viento

Datos de velocidad media diaria (m/s):
1. 7.92    6. 15.12
2. 10.08   7. 3.96
3. 18.00   8. 6.84
4. 21.96   9. 7.92
5. 15.12   10. 3.96

Opciones para k: 18.41, 34.24, 23.43, 1.9
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar
import math

def calcular_parametro_k_weibull():
    print("=" * 80)
    print("CÁLCULO DEL PARÁMETRO k DE LA DISTRIBUCIÓN DE WEIBULL")
    print("=" * 80)
    
    # Datos de velocidad del viento
    velocidades = np.array([7.92, 10.08, 18.00, 21.96, 15.12, 15.12, 3.96, 6.84, 7.92, 3.96])
    
    print(f"\n1️⃣ DATOS DE VELOCIDAD DEL VIENTO:")
    print(f"   Velocidades (m/s): {velocidades}")
    print(f"   Número de observaciones: {len(velocidades)}")
    print(f"   Velocidad media: {np.mean(velocidades):.3f} m/s")
    print(f"   Desviación estándar: {np.std(velocidades, ddof=1):.3f} m/s")
    
    print(f"\n2️⃣ DISTRIBUCIÓN DE WEIBULL:")
    print(f"   Función de densidad: f(x) = (k/λ)(x/λ)^(k-1) * exp(-(x/λ)^k)")
    print(f"   Parámetros:")
    print(f"   • k = parámetro de forma (shape)")
    print(f"   • λ = parámetro de escala (scale)")
    
    # Método 1: Usando scipy.stats.weibull_min.fit()
    print(f"\n3️⃣ MÉTODO 1: MÁXIMA VEROSIMILITUD (SCIPY):")
    
    # Ajustar distribución Weibull
    # weibull_min usa parametrización: f(x) = c/x * (x/λ)^c * exp(-(x/λ)^c)
    # donde c es el parámetro de forma (equivalente a k)
    params = stats.weibull_min.fit(velocidades, floc=0)  # floc=0 fija la ubicación en 0
    k_scipy = params[0]  # parámetro de forma
    loc_scipy = params[1]  # parámetro de ubicación (fijado en 0)
    lambda_scipy = params[2]  # parámetro de escala
    
    print(f"   Parámetros estimados:")
    print(f"   • k (forma) = {k_scipy:.4f}")
    print(f"   • λ (escala) = {lambda_scipy:.4f}")
    print(f"   • ubicación = {loc_scipy:.4f}")
    
    # Método 2: Método de momentos aproximado
    print(f"\n4️⃣ MÉTODO 2: MÉTODO DE MOMENTOS:")
    
    # Para Weibull: E[X] = λ * Γ(1 + 1/k)
    # Var[X] = λ² * [Γ(1 + 2/k) - Γ²(1 + 1/k)]
    
    media = np.mean(velocidades)
    varianza = np.var(velocidades, ddof=1)
    cv = np.std(velocidades, ddof=1) / media  # coeficiente de variación
    
    print(f"   Media muestral: {media:.4f}")
    print(f"   Varianza muestral: {varianza:.4f}")
    print(f"   Coeficiente de variación: {cv:.4f}")
    
    # Aproximación inicial para k usando el coeficiente de variación
    # CV ≈ √[Γ(1 + 2/k)/Γ²(1 + 1/k) - 1]
    # Para valores típicos de CV, k ≈ 1/CV^1.2 (aproximación empírica)
    k_aprox = 1 / (cv ** 1.2)
    print(f"   k aproximado (método empírico): {k_aprox:.4f}")
    
    # Método 3: Método gráfico (regresión lineal de Weibull plot)
    print(f"\n5️⃣ MÉTODO 3: MÉTODO GRÁFICO (WEIBULL PLOT):")
    
    # Ordenar datos
    velocidades_ordenadas = np.sort(velocidades)
    n = len(velocidades)
    
    # Calcular probabilidades empíricas usando fórmula de Weibull
    # F(i) = i/(n+1) para el i-ésimo valor ordenado
    prob_empiricas = np.arange(1, n+1) / (n + 1)
    
    # Transformación para linearizar: ln(-ln(1-F)) = k*ln(x) - k*ln(λ)
    # y = k*x + b, donde y = ln(-ln(1-F)), x = ln(velocidad)
    
    # Filtrar probabilidades para evitar log(0)
    prob_validas = prob_empiricas[prob_empiricas < 0.999]
    vel_validas = velocidades_ordenadas[:len(prob_validas)]
    
    y = np.log(-np.log(1 - prob_validas))
    x = np.log(vel_validas)
    
    # Regresión lineal
    coef = np.polyfit(x, y, 1)
    k_grafico = coef[0]  # pendiente = k
    b = coef[1]  # intersección = -k*ln(λ)
    lambda_grafico = np.exp(-b / k_grafico)
    
    print(f"   Regresión lineal: y = {k_grafico:.4f}x + {b:.4f}")
    print(f"   k (parámetro de forma) = {k_grafico:.4f}")
    print(f"   λ (parámetro de escala) = {lambda_grafico:.4f}")
    
    # Comparar con las opciones
    opciones = [18.41, 34.24, 23.43, 1.9]
    
    print(f"\n6️⃣ COMPARACIÓN CON LAS OPCIONES:")
    print(f"   Opciones disponibles: {opciones}")
    
    # Usar el resultado de scipy como referencia principal
    k_final = k_scipy
    
    diferencias = [abs(k_final - opcion) for opcion in opciones]
    mejor_opcion_idx = diferencias.index(min(diferencias))
    mejor_opcion = opciones[mejor_opcion_idx]
    
    print(f"\n   Resultados de diferentes métodos:")
    print(f"   • Scipy (MLE): k = {k_scipy:.4f}")
    print(f"   • Método gráfico: k = {k_grafico:.4f}")
    print(f"   • Método empírico: k = {k_aprox:.4f}")
    
    print(f"\n   Comparación con opciones:")
    for i, opcion in enumerate(opciones, 1):
        diferencia = abs(k_final - opcion)
        marca = "✅" if diferencia == min(diferencias) else "❌"
        print(f"   Opción {i}: k = {opcion} - Diferencia: {diferencia:.4f} {marca}")
    
    # Verificación adicional
    print(f"\n7️⃣ VERIFICACIÓN:")
    print(f"   Usando k = {k_final:.4f} y λ = {lambda_scipy:.4f}:")
    
    # Calcular media teórica
    from scipy.special import gamma
    media_teorica = lambda_scipy * gamma(1 + 1/k_final)
    print(f"   • Media teórica: {media_teorica:.4f} m/s")
    print(f"   • Media observada: {media:.4f} m/s")
    print(f"   • Error: {abs(media_teorica - media):.4f} m/s")
    
    print(f"\n🎯 CONCLUSIÓN:")
    print(f"   El parámetro k de la distribución de Weibull es: {k_final:.4f}")
    print(f"   La opción más cercana es: {mejor_opcion}")
    
    return k_final, mejor_opcion

if __name__ == "__main__":
    k, opcion = calcular_parametro_k_weibull()
    print(f"\n🎯 RESPUESTA: {opcion}")