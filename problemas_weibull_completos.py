"""
Problemas Adicionales de Distribución de Weibull
Usando los datos de velocidad del viento y k = 1.9 calculado anteriormente

Datos: [7.92, 10.08, 18.00, 21.96, 15.12, 15.12, 3.96, 6.84, 7.92, 3.96]

Preguntas:
b) Parámetro c (λ): opciones 35.13, 12.5, 3.11, 27.54
c) Velocidad más probable: opciones 8.45, 15.31, 29.26, 32.4
d) Velocidad para máxima energía eólica: opciones 21.43, 2.31, 12.25, 18.2
e) P(V > 18 m/s): opciones 24.3%, 13.5%, 10.1%, 4.1%
"""

import numpy as np
from scipy import stats
from scipy.special import gamma
import math

def resolver_problemas_weibull_completos():
    print("=" * 80)
    print("PROBLEMAS COMPLETOS DE DISTRIBUCIÓN DE WEIBULL")
    print("=" * 80)
    
    # Datos de velocidad del viento
    velocidades = np.array([7.92, 10.08, 18.00, 21.96, 15.12, 15.12, 3.96, 6.84, 7.92, 3.96])
    
    print(f"\n📊 DATOS INICIALES:")
    print(f"   Velocidades: {velocidades}")
    print(f"   Media observada: {np.mean(velocidades):.3f} m/s")
    print(f"   Del problema anterior: k = 1.9")
    
    # Usar k = 1.9 (del problema anterior) y recalcular λ con este valor fijo
    k = 1.9
    
    # Método de momentos para calcular λ dado k
    # E[X] = λ * Γ(1 + 1/k)
    # λ = E[X] / Γ(1 + 1/k)
    
    media_observada = np.mean(velocidades)
    gamma_factor = gamma(1 + 1/k)
    lambda_calculado = media_observada / gamma_factor
    
    print(f"\n1️⃣ CÁLCULO DEL PARÁMETRO c (λ) - ESCALA:")
    print(f"   Usando k = {k}")
    print(f"   Fórmula: λ = Media / Γ(1 + 1/k)")
    print(f"   Γ(1 + 1/{k}) = Γ({1 + 1/k:.4f}) = {gamma_factor:.4f}")
    print(f"   λ = {media_observada:.3f} / {gamma_factor:.4f} = {lambda_calculado:.4f}")
    
    # También verificar con scipy para comparación
    params_scipy = stats.weibull_min.fit(velocidades, floc=0)
    k_scipy = params_scipy[0]
    lambda_scipy = params_scipy[2]
    
    print(f"   Verificación con scipy: λ = {lambda_scipy:.4f} (k = {k_scipy:.4f})")
    
    # Usar lambda_calculado como parámetro c
    c = lambda_calculado
    
    print(f"\n   🎯 PARÁMETRO c = {c:.2f}")
    
    # Opciones para parámetro c
    opciones_c = [35.13, 12.5, 3.11, 27.54]
    diferencias_c = [abs(c - op) for op in opciones_c]
    mejor_c_idx = diferencias_c.index(min(diferencias_c))
    mejor_c = opciones_c[mejor_c_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_c, 1):
        diff = abs(c - opcion)
        marca = "✅" if diff == min(diferencias_c) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # 2. Velocidad más probable (moda)
    print(f"\n2️⃣ VELOCIDAD MÁS PROBABLE (MODA):")
    print(f"   Fórmula para k > 1: Moda = λ * ((k-1)/k)^(1/k)")
    
    if k > 1:
        factor_moda = ((k - 1) / k) ** (1 / k)
        moda = c * factor_moda
        print(f"   Factor = ((k-1)/k)^(1/k) = (({k}-1)/{k})^(1/{k}) = {factor_moda:.4f}")
        print(f"   Moda = {c:.4f} × {factor_moda:.4f} = {moda:.4f} m/s")
    else:
        moda = 0
        print(f"   Para k ≤ 1, la moda es 0")
    
    print(f"\n   🎯 VELOCIDAD MÁS PROBABLE = {moda:.2f} m/s")
    
    # Opciones para velocidad más probable
    opciones_moda = [8.45, 15.31, 29.26, 32.4]
    diferencias_moda = [abs(moda - op) for op in opciones_moda]
    mejor_moda_idx = diferencias_moda.index(min(diferencias_moda))
    mejor_moda = opciones_moda[mejor_moda_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_moda, 1):
        diff = abs(moda - opcion)
        marca = "✅" if diff == min(diferencias_moda) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # 3. Velocidad para máxima energía eólica
    print(f"\n3️⃣ VELOCIDAD PARA MÁXIMA ENERGÍA EÓLICA:")
    print(f"   La energía eólica es proporcional a v³")
    print(f"   Máximo de E[v³] para Weibull: v_max = λ * ((k+2)/k)^(1/k)")
    
    factor_energia = ((k + 2) / k) ** (1 / k)
    v_max_energia = c * factor_energia
    
    print(f"   Factor = ((k+2)/k)^(1/k) = (({k}+2)/{k})^(1/{k}) = {factor_energia:.4f}")
    print(f"   v_max_energia = {c:.4f} × {factor_energia:.4f} = {v_max_energia:.4f} m/s")
    
    print(f"\n   🎯 VELOCIDAD MÁXIMA ENERGÍA = {v_max_energia:.2f} m/s")
    
    # Opciones para velocidad máxima energía
    opciones_energia = [21.43, 2.31, 12.25, 18.2]
    diferencias_energia = [abs(v_max_energia - op) for op in opciones_energia]
    mejor_energia_idx = diferencias_energia.index(min(diferencias_energia))
    mejor_energia = opciones_energia[mejor_energia_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_energia, 1):
        diff = abs(v_max_energia - opcion)
        marca = "✅" if diff == min(diferencias_energia) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # 4. Probabilidad P(V > 18 m/s)
    print(f"\n4️⃣ PROBABILIDAD P(V > 18 m/s):")
    print(f"   Función de supervivencia: S(x) = P(X > x) = exp(-(x/λ)^k)")
    
    v_limite = 18
    exponente = -(v_limite / c) ** k
    prob_mayor_18 = math.exp(exponente)
    porcentaje = prob_mayor_18 * 100
    
    print(f"   P(V > {v_limite}) = exp(-({v_limite}/{c:.4f})^{k})")
    print(f"   P(V > {v_limite}) = exp({exponente:.4f})")
    print(f"   P(V > {v_limite}) = {prob_mayor_18:.6f}")
    print(f"   P(V > {v_limite}) = {porcentaje:.2f}%")
    
    print(f"\n   🎯 PROBABILIDAD P(V > 18) = {porcentaje:.1f}%")
    
    # Opciones para probabilidad
    opciones_prob = [24.3, 13.5, 10.1, 4.1]
    diferencias_prob = [abs(porcentaje - op) for op in opciones_prob]
    mejor_prob_idx = diferencias_prob.index(min(diferencias_prob))
    mejor_prob = opciones_prob[mejor_prob_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_prob, 1):
        diff = abs(porcentaje - opcion)
        marca = "✅" if diff == min(diferencias_prob) else "❌"
        print(f"   {i}) {opcion}% - Diferencia: {diff:.1f}% {marca}")
    
    # Verificación adicional con scipy
    print(f"\n5️⃣ VERIFICACIÓN CON SCIPY:")
    prob_scipy = 1 - stats.weibull_min.cdf(v_limite, k, loc=0, scale=c)
    print(f"   P(V > 18) usando scipy: {prob_scipy * 100:.2f}%")
    
    # Resumen de respuestas
    print(f"\n🎯 RESUMEN DE RESPUESTAS:")
    print(f"   b) Parámetro c: {mejor_c}")
    print(f"   c) Velocidad más probable: {mejor_moda}")
    print(f"   d) Velocidad máxima energía: {mejor_energia}")
    print(f"   e) P(V > 18 m/s): {mejor_prob}%")
    
    return {
        'parametro_c': mejor_c,
        'velocidad_probable': mejor_moda,
        'velocidad_energia': mejor_energia,
        'probabilidad_18': mejor_prob
    }

if __name__ == "__main__":
    resultados = resolver_problemas_weibull_completos()
    print(f"\n🎯 RESPUESTAS FINALES:")
    for clave, valor in resultados.items():
        print(f"   {clave}: {valor}")