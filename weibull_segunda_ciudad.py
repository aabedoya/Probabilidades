"""
Nuevo Problema de Distribución de Weibull - Segunda Ciudad
Calcular todos los parámetros y métricas para una nueva ciudad

Datos de velocidad media diaria (m/s):
1. 5.04    6. 3.96
2. 2.88    7. 3.96
3. 2.16    8. 9.00
4. 6.12    9. 3.96
5. 9.00    10. 9.00

Preguntas:
a) Parámetro k: opciones 13.24, 3.13, 8.41, 2.23
b) Parámetro c: opciones 7.24, 15.23, 3.41, 6.22
c) Velocidad más probable: opciones 2.4, 5.31, 9.26, 4.77
d) Velocidad máxima energía: opciones 5.31, 8.28, 1.43, 12.25
e) P(V > 9 m/s): opciones 10.2%, 14.3%, 5.1%, 24.1%
"""

import numpy as np
from scipy import stats
from scipy.special import gamma
import math

def resolver_weibull_segunda_ciudad():
    print("=" * 80)
    print("DISTRIBUCIÓN DE WEIBULL - SEGUNDA CIUDAD")
    print("=" * 80)
    
    # Nuevos datos de velocidad del viento
    velocidades = np.array([5.04, 2.88, 2.16, 6.12, 9.00, 3.96, 3.96, 9.00, 3.96, 9.00])
    
    print(f"\n📊 DATOS DE LA SEGUNDA CIUDAD:")
    print(f"   Velocidades: {velocidades}")
    print(f"   Número de observaciones: {len(velocidades)}")
    print(f"   Media observada: {np.mean(velocidades):.3f} m/s")
    print(f"   Desviación estándar: {np.std(velocidades, ddof=1):.3f} m/s")
    print(f"   Mínimo: {np.min(velocidades):.2f} m/s")
    print(f"   Máximo: {np.max(velocidades):.2f} m/s")
    
    # 1. CÁLCULO DEL PARÁMETRO k
    print(f"\n1️⃣ CÁLCULO DEL PARÁMETRO k (FORMA):")
    
    # Método 1: Máxima verosimilitud usando scipy
    params_scipy = stats.weibull_min.fit(velocidades, floc=0)
    k_scipy = params_scipy[0]
    loc_scipy = params_scipy[1]
    lambda_scipy = params_scipy[2]
    
    print(f"   Método scipy (MLE):")
    print(f"   • k = {k_scipy:.4f}")
    print(f"   • λ = {lambda_scipy:.4f}")
    print(f"   • ubicación = {loc_scipy:.4f}")
    
    # Método 2: Método gráfico (regresión lineal)
    velocidades_ordenadas = np.sort(velocidades)
    n = len(velocidades)
    prob_empiricas = np.arange(1, n+1) / (n + 1)
    
    # Filtrar para evitar problemas con log(0)
    prob_validas = prob_empiricas[prob_empiricas < 0.99]
    vel_validas = velocidades_ordenadas[:len(prob_validas)]
    
    y = np.log(-np.log(1 - prob_validas))
    x = np.log(vel_validas)
    
    coef = np.polyfit(x, y, 1)
    k_grafico = coef[0]
    b = coef[1]
    lambda_grafico = np.exp(-b / k_grafico)
    
    print(f"   Método gráfico (regresión):")
    print(f"   • k = {k_grafico:.4f}")
    print(f"   • λ = {lambda_grafico:.4f}")
    
    # Usar el resultado de scipy como principal
    k = k_scipy
    
    print(f"\n   🎯 PARÁMETRO k = {k:.2f}")
    
    # Comparar con opciones para k
    opciones_k = [13.24, 3.13, 8.41, 2.23]
    diferencias_k = [abs(k - op) for op in opciones_k]
    mejor_k_idx = diferencias_k.index(min(diferencias_k))
    mejor_k = opciones_k[mejor_k_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_k, 1):
        diff = abs(k - opcion)
        marca = "✅" if diff == min(diferencias_k) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # 2. CÁLCULO DEL PARÁMETRO c (λ)
    print(f"\n2️⃣ CÁLCULO DEL PARÁMETRO c (ESCALA):")
    
    # Usar el k estimado y recalcular c usando método de momentos
    media_observada = np.mean(velocidades)
    gamma_factor = gamma(1 + 1/k)
    c_calculado = media_observada / gamma_factor
    
    print(f"   Usando k = {k:.4f}")
    print(f"   Fórmula: c = Media / Γ(1 + 1/k)")
    print(f"   Γ(1 + 1/{k:.4f}) = {gamma_factor:.4f}")
    print(f"   c = {media_observada:.3f} / {gamma_factor:.4f} = {c_calculado:.4f}")
    
    # También usar el valor de scipy para comparación
    c = lambda_scipy
    
    print(f"\n   🎯 PARÁMETRO c = {c:.2f}")
    
    # Comparar con opciones para c
    opciones_c = [7.24, 15.23, 3.41, 6.22]
    diferencias_c = [abs(c - op) for op in opciones_c]
    mejor_c_idx = diferencias_c.index(min(diferencias_c))
    mejor_c = opciones_c[mejor_c_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_c, 1):
        diff = abs(c - opcion)
        marca = "✅" if diff == min(diferencias_c) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # 3. VELOCIDAD MÁS PROBABLE (MODA)
    print(f"\n3️⃣ VELOCIDAD MÁS PROBABLE (MODA):")
    
    if k > 1:
        factor_moda = ((k - 1) / k) ** (1 / k)
        moda = c * factor_moda
        print(f"   Para k > 1: Moda = c × ((k-1)/k)^(1/k)")
        print(f"   Factor = ((k-1)/k)^(1/k) = (({k:.4f}-1)/{k:.4f})^(1/{k:.4f}) = {factor_moda:.4f}")
        print(f"   Moda = {c:.4f} × {factor_moda:.4f} = {moda:.4f} m/s")
    else:
        moda = 0
        print(f"   Para k ≤ 1, la moda es 0")
    
    print(f"\n   🎯 VELOCIDAD MÁS PROBABLE = {moda:.2f} m/s")
    
    # Comparar con opciones para moda
    opciones_moda = [2.4, 5.31, 9.26, 4.77]
    diferencias_moda = [abs(moda - op) for op in opciones_moda]
    mejor_moda_idx = diferencias_moda.index(min(diferencias_moda))
    mejor_moda = opciones_moda[mejor_moda_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_moda, 1):
        diff = abs(moda - opcion)
        marca = "✅" if diff == min(diferencias_moda) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # 4. VELOCIDAD PARA MÁXIMA ENERGÍA EÓLICA
    print(f"\n4️⃣ VELOCIDAD PARA MÁXIMA ENERGÍA EÓLICA:")
    
    factor_energia = ((k + 2) / k) ** (1 / k)
    v_max_energia = c * factor_energia
    
    print(f"   Energía ∝ v³, máximo en: v_max = c × ((k+2)/k)^(1/k)")
    print(f"   Factor = ((k+2)/k)^(1/k) = (({k:.4f}+2)/{k:.4f})^(1/{k:.4f}) = {factor_energia:.4f}")
    print(f"   v_max = {c:.4f} × {factor_energia:.4f} = {v_max_energia:.4f} m/s")
    
    print(f"\n   🎯 VELOCIDAD MÁXIMA ENERGÍA = {v_max_energia:.2f} m/s")
    
    # Comparar con opciones para energía
    opciones_energia = [5.31, 8.28, 1.43, 12.25]
    diferencias_energia = [abs(v_max_energia - op) for op in opciones_energia]
    mejor_energia_idx = diferencias_energia.index(min(diferencias_energia))
    mejor_energia = opciones_energia[mejor_energia_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_energia, 1):
        diff = abs(v_max_energia - opcion)
        marca = "✅" if diff == min(diferencias_energia) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # 5. PROBABILIDAD P(V > 9 m/s)
    print(f"\n5️⃣ PROBABILIDAD P(V > 9 m/s):")
    
    v_limite = 9.0
    exponente = -(v_limite / c) ** k
    prob_mayor_9 = math.exp(exponente)
    porcentaje = prob_mayor_9 * 100
    
    print(f"   Función de supervivencia: P(V > x) = exp(-(x/c)^k)")
    print(f"   P(V > {v_limite}) = exp(-({v_limite}/{c:.4f})^{k:.4f})")
    print(f"   P(V > {v_limite}) = exp({exponente:.4f})")
    print(f"   P(V > {v_limite}) = {prob_mayor_9:.6f}")
    print(f"   P(V > {v_limite}) = {porcentaje:.2f}%")
    
    print(f"\n   🎯 PROBABILIDAD P(V > 9) = {porcentaje:.1f}%")
    
    # Comparar con opciones para probabilidad
    opciones_prob = [10.2, 14.3, 5.1, 24.1]
    diferencias_prob = [abs(porcentaje - op) for op in opciones_prob]
    mejor_prob_idx = diferencias_prob.index(min(diferencias_prob))
    mejor_prob = opciones_prob[mejor_prob_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_prob, 1):
        diff = abs(porcentaje - opcion)
        marca = "✅" if diff == min(diferencias_prob) else "❌"
        print(f"   {i}) {opcion}% - Diferencia: {diff:.1f}% {marca}")
    
    # Verificación con scipy
    print(f"\n6️⃣ VERIFICACIÓN CON SCIPY:")
    prob_scipy = 1 - stats.weibull_min.cdf(v_limite, k, loc=0, scale=c)
    print(f"   P(V > 9) usando scipy: {prob_scipy * 100:.2f}%")
    
    # Verificación de ajuste
    print(f"\n7️⃣ VERIFICACIÓN DEL AJUSTE:")
    media_teorica = c * gamma(1 + 1/k)
    print(f"   Media teórica: {media_teorica:.3f} m/s")
    print(f"   Media observada: {media_observada:.3f} m/s")
    print(f"   Error absoluto: {abs(media_teorica - media_observada):.3f} m/s")
    
    # Resumen final
    print(f"\n🎯 RESUMEN DE RESPUESTAS - SEGUNDA CIUDAD:")
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
    resultados = resolver_weibull_segunda_ciudad()
    print(f"\n🎯 RESPUESTAS FINALES:")
    for clave, valor in resultados.items():
        print(f"   {clave}: {valor}")