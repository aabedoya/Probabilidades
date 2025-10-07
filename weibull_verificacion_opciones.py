"""
Problema de Weibull - Ciudad con datos repetidos
Mismos datos de velocidad pero con opciones diferentes

Datos de velocidad media diaria (m/s):
[5.04, 2.88, 2.16, 6.12, 9.00, 3.96, 3.96, 9.00, 3.96, 9.00]

Preguntas con nuevas opciones:
a) Parámetro k: 2.23, 3.13, 13.24, 8.41
b) Parámetro c: 6.22, 15.23, 3.41, 7.24
c) Velocidad más probable: 9.26, 2.4, 5.31, 4.77
d) Velocidad máxima energía: 5.31, 12.25, 1.43, 8.28
e) P(V > 9 m/s): 14.3%, 5.1%, 10.2%, 24.1%
"""

import numpy as np
from scipy import stats
from scipy.special import gamma
import math

def resolver_weibull_opciones_nuevas():
    print("=" * 80)
    print("DISTRIBUCIÓN DE WEIBULL - VERIFICACIÓN CON NUEVAS OPCIONES")
    print("=" * 80)
    
    # Datos de velocidad del viento (mismos que en problema anterior)
    velocidades = np.array([5.04, 2.88, 2.16, 6.12, 9.00, 3.96, 3.96, 9.00, 3.96, 9.00])
    
    print(f"\n📊 DATOS DE VELOCIDAD:")
    print(f"   Velocidades: {velocidades}")
    print(f"   Media: {np.mean(velocidades):.3f} m/s")
    print(f"   Desviación estándar: {np.std(velocidades, ddof=1):.3f} m/s")
    print(f"   Número de observaciones: {len(velocidades)}")
    
    print(f"\n1️⃣ ESTIMACIÓN DE PARÁMETROS DE WEIBULL:")
    
    # Usar scipy para estimar parámetros
    params = stats.weibull_min.fit(velocidades, floc=0)
    k_estimado = params[0]  # parámetro de forma
    loc = params[1]         # parámetro de ubicación
    c_estimado = params[2]  # parámetro de escala
    
    print(f"   Parámetros estimados (scipy):")
    print(f"   • k (forma) = {k_estimado:.4f}")
    print(f"   • c (escala) = {c_estimado:.4f}")
    print(f"   • ubicación = {loc:.4f}")
    
    # Verificar ajuste
    media_teorica = c_estimado * gamma(1 + 1/k_estimado)
    print(f"   • Media teórica: {media_teorica:.3f} m/s")
    print(f"   • Error: {abs(media_teorica - np.mean(velocidades)):.3f} m/s")
    
    print(f"\n2️⃣ PARÁMETRO k:")
    print(f"   k estimado = {k_estimado:.2f}")
    
    opciones_k = [2.23, 3.13, 13.24, 8.41]
    diferencias_k = [abs(k_estimado - op) for op in opciones_k]
    mejor_k_idx = diferencias_k.index(min(diferencias_k))
    mejor_k = opciones_k[mejor_k_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_k, 1):
        diff = abs(k_estimado - opcion)
        marca = "✅" if diff == min(diferencias_k) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    print(f"\n3️⃣ PARÁMETRO c:")
    print(f"   c estimado = {c_estimado:.2f}")
    
    opciones_c = [6.22, 15.23, 3.41, 7.24]
    diferencias_c = [abs(c_estimado - op) for op in opciones_c]
    mejor_c_idx = diferencias_c.index(min(diferencias_c))
    mejor_c = opciones_c[mejor_c_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_c, 1):
        diff = abs(c_estimado - opcion)
        marca = "✅" if diff == min(diferencias_c) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    print(f"\n4️⃣ VELOCIDAD MÁS PROBABLE (MODA):")
    
    if k_estimado > 1:
        factor_moda = ((k_estimado - 1) / k_estimado) ** (1 / k_estimado)
        moda = c_estimado * factor_moda
        print(f"   Para k > 1: Moda = c × ((k-1)/k)^(1/k)")
        print(f"   Factor = ((k-1)/k)^(1/k) = {factor_moda:.4f}")
        print(f"   Moda = {c_estimado:.4f} × {factor_moda:.4f} = {moda:.4f} m/s")
    else:
        moda = 0
        print(f"   Para k ≤ 1, la moda es 0")
    
    print(f"\n   🎯 VELOCIDAD MÁS PROBABLE = {moda:.2f} m/s")
    
    opciones_moda = [9.26, 2.4, 5.31, 4.77]
    diferencias_moda = [abs(moda - op) for op in opciones_moda]
    mejor_moda_idx = diferencias_moda.index(min(diferencias_moda))
    mejor_moda = opciones_moda[mejor_moda_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_moda, 1):
        diff = abs(moda - opcion)
        marca = "✅" if diff == min(diferencias_moda) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    print(f"\n5️⃣ VELOCIDAD PARA MÁXIMA ENERGÍA EÓLICA:")
    
    factor_energia = ((k_estimado + 2) / k_estimado) ** (1 / k_estimado)
    v_max_energia = c_estimado * factor_energia
    
    print(f"   Energía ∝ v³, máximo en: v_max = c × ((k+2)/k)^(1/k)")
    print(f"   Factor = ((k+2)/k)^(1/k) = {factor_energia:.4f}")
    print(f"   v_max = {c_estimado:.4f} × {factor_energia:.4f} = {v_max_energia:.4f} m/s")
    
    print(f"\n   🎯 VELOCIDAD MÁXIMA ENERGÍA = {v_max_energia:.2f} m/s")
    
    opciones_energia = [5.31, 12.25, 1.43, 8.28]
    diferencias_energia = [abs(v_max_energia - op) for op in opciones_energia]
    mejor_energia_idx = diferencias_energia.index(min(diferencias_energia))
    mejor_energia = opciones_energia[mejor_energia_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_energia, 1):
        diff = abs(v_max_energia - opcion)
        marca = "✅" if diff == min(diferencias_energia) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    print(f"\n6️⃣ PROBABILIDAD P(V > 9 m/s):")
    
    v_limite = 9.0
    exponente = -(v_limite / c_estimado) ** k_estimado
    prob_mayor_9 = math.exp(exponente)
    porcentaje = prob_mayor_9 * 100
    
    print(f"   Función de supervivencia: P(V > x) = exp(-(x/c)^k)")
    print(f"   P(V > {v_limite}) = exp(-({v_limite}/{c_estimado:.4f})^{k_estimado:.4f})")
    print(f"   P(V > {v_limite}) = exp({exponente:.4f})")
    print(f"   P(V > {v_limite}) = {prob_mayor_9:.6f}")
    print(f"   P(V > {v_limite}) = {porcentaje:.2f}%")
    
    print(f"\n   🎯 PROBABILIDAD P(V > 9) = {porcentaje:.1f}%")
    
    opciones_prob = [14.3, 5.1, 10.2, 24.1]
    diferencias_prob = [abs(porcentaje - op) for op in opciones_prob]
    mejor_prob_idx = diferencias_prob.index(min(diferencias_prob))
    mejor_prob = opciones_prob[mejor_prob_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_prob, 1):
        diff = abs(porcentaje - opcion)
        marca = "✅" if diff == min(diferencias_prob) else "❌"
        print(f"   {i}) {opcion}% - Diferencia: {diff:.1f}% {marca}")
    
    # Verificación empírica
    prob_empirica = (np.sum(velocidades > v_limite) / len(velocidades)) * 100
    print(f"   Verificación empírica: {prob_empirica:.1f}%")
    
    # Verificación scipy
    prob_scipy = (1 - stats.weibull_min.cdf(v_limite, k_estimado, loc=0, scale=c_estimado)) * 100
    print(f"   Verificación scipy: {prob_scipy:.1f}%")
    
    print(f"\n7️⃣ ANÁLISIS ADICIONAL:")
    print(f"   Datos empíricos:")
    valores_unicos, frecuencias = np.unique(velocidades, return_counts=True)
    for val, freq in zip(valores_unicos, frecuencias):
        print(f"   {val:.2f} m/s: {freq} observaciones")
    
    print(f"   Observaciones ≥ 9 m/s: {np.sum(velocidades >= 9)} de {len(velocidades)}")
    print(f"   Porcentaje empírico ≥ 9 m/s: {(np.sum(velocidades >= 9)/len(velocidades))*100:.1f}%")
    
    # Resumen final
    print(f"\n🎯 RESUMEN DE RESPUESTAS:")
    print(f"   a) Parámetro k: {mejor_k}")
    print(f"   b) Parámetro c: {mejor_c}")
    print(f"   c) Velocidad más probable: {mejor_moda}")
    print(f"   d) Velocidad máxima energía: {mejor_energia}")
    print(f"   e) P(V > 9 m/s): {mejor_prob}%")
    
    return {
        'k': mejor_k,
        'c': mejor_c,
        'moda': mejor_moda,
        'energia': mejor_energia,
        'prob_9': mejor_prob
    }

if __name__ == "__main__":
    resultados = resolver_weibull_opciones_nuevas()
    print(f"\n🎯 RESPUESTAS FINALES:")
    for clave, valor in resultados.items():
        print(f"   {clave}: {valor}")