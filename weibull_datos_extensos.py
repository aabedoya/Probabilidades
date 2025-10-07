"""
Análisis de Distribución de Weibull - Datos Extensos de Velocidad del Viento
118 mediciones de velocidad del viento en febrero

Preguntas:
a) Parámetro k: opciones 5.24, 8.24, 4.31, 7.81, 1.25
b) Parámetro c: opciones 3.91, 5.89, 1.57, 7.21
c) Percentil 75: opciones 0.8, 2.1, 3.5, 4.1, 1.6
d) P(V > percentil 75): opciones 0.15, 0.42, 0.25, 0.61, 0.34
"""

import numpy as np
from scipy import stats
from scipy.special import gamma
import math

def analizar_weibull_datos_extensos():
    print("=" * 80)
    print("ANÁLISIS DE WEIBULL - DATOS EXTENSOS (118 MEDICIONES)")
    print("=" * 80)
    
    # Datos de velocidad del viento (118 mediciones)
    velocidades = np.array([
        # Días 1-10
        0.7, 0.7, 0.8, 0.8, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9,
        # Días 11-20
        1.0, 1.0, 1.0, 1.0, 1.0, 1.1, 1.1, 1.1, 1.1, 1.1,
        # Días 21-30
        1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.2, 1.2, 1.2, 1.2,
        # Días 31-40
        1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2,
        # Días 41-50
        1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3,
        # Días 51-60
        1.3, 1.3, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4,
        # Días 61-70
        1.4, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
        # Días 71-80
        1.5, 1.5, 1.5, 1.5, 1.5, 1.6, 1.6, 1.6, 1.6, 1.6,
        # Días 81-90
        1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6,
        # Días 91-100
        1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7,
        # Días 101-110
        1.7, 1.7, 1.8, 1.8, 1.8, 1.8, 1.8, 1.9, 1.9, 1.9,
        # Días 111-118
        2.0, 2.0, 2.1, 2.3, 2.5, 2.5, 2.6, 2.6
    ])
    
    print(f"\n📊 ESTADÍSTICAS DESCRIPTIVAS:")
    print(f"   Número de observaciones: {len(velocidades)}")
    print(f"   Media: {np.mean(velocidades):.4f} m/s")
    print(f"   Mediana: {np.median(velocidades):.4f} m/s")
    print(f"   Desviación estándar: {np.std(velocidades, ddof=1):.4f} m/s")
    print(f"   Mínimo: {np.min(velocidades):.1f} m/s")
    print(f"   Máximo: {np.max(velocidades):.1f} m/s")
    
    # Percentiles empíricos para comparación
    percentiles = [25, 50, 75, 90, 95]
    print(f"\n   Percentiles empíricos:")
    for p in percentiles:
        valor = np.percentile(velocidades, p)
        print(f"   P{p}: {valor:.2f} m/s")
    
    print(f"\n1️⃣ ESTIMACIÓN DE PARÁMETROS DE WEIBULL:")
    
    # Método de máxima verosimilitud usando scipy
    params = stats.weibull_min.fit(velocidades, floc=0)
    k_estimado = params[0]  # parámetro de forma
    loc = params[1]         # parámetro de ubicación (fijado en 0)
    c_estimado = params[2]  # parámetro de escala
    
    print(f"   Método de Máxima Verosimilitud (scipy):")
    print(f"   • k (forma) = {k_estimado:.4f}")
    print(f"   • c (escala) = {c_estimado:.4f}")
    print(f"   • ubicación = {loc:.4f}")
    
    # Verificación del ajuste
    media_teorica = c_estimado * gamma(1 + 1/k_estimado)
    print(f"\n   Verificación del ajuste:")
    print(f"   • Media teórica: {media_teorica:.4f} m/s")
    print(f"   • Media observada: {np.mean(velocidades):.4f} m/s")
    print(f"   • Error absoluto: {abs(media_teorica - np.mean(velocidades)):.4f} m/s")
    
    # 2. COMPARACIÓN CON OPCIONES PARA k
    print(f"\n2️⃣ PARÁMETRO k:")
    print(f"   k estimado = {k_estimado:.2f}")
    
    opciones_k = [5.24, 8.24, 4.31, 7.81, 1.25]
    diferencias_k = [abs(k_estimado - op) for op in opciones_k]
    mejor_k_idx = diferencias_k.index(min(diferencias_k))
    mejor_k = opciones_k[mejor_k_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_k, 1):
        diff = abs(k_estimado - opcion)
        marca = "✅" if diff == min(diferencias_k) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # 3. COMPARACIÓN CON OPCIONES PARA c
    print(f"\n3️⃣ PARÁMETRO c:")
    print(f"   c estimado = {c_estimado:.2f}")
    
    opciones_c = [3.91, 5.89, 1.57, 7.21]
    diferencias_c = [abs(c_estimado - op) for op in opciones_c]
    mejor_c_idx = diferencias_c.index(min(diferencias_c))
    mejor_c = opciones_c[mejor_c_idx]
    
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_c, 1):
        diff = abs(c_estimado - opcion)
        marca = "✅" if diff == min(diferencias_c) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # 4. CÁLCULO DEL PERCENTIL 75
    print(f"\n4️⃣ PERCENTIL 75:")
    
    # Percentil 75 teórico usando la distribución de Weibull
    # F(x) = 1 - exp(-(x/c)^k) = 0.75
    # exp(-(x/c)^k) = 0.25
    # -(x/c)^k = ln(0.25)
    # (x/c)^k = -ln(0.25) = ln(4)
    # x = c * (ln(4))^(1/k)
    
    percentil_75_teorico = c_estimado * (math.log(4)) ** (1/k_estimado)
    percentil_75_empirico = np.percentile(velocidades, 75)
    
    print(f"   Fórmula: P75 = c × (ln(4))^(1/k)")
    print(f"   P75 teórico = {c_estimado:.4f} × ({math.log(4):.4f})^(1/{k_estimado:.4f})")
    print(f"   P75 teórico = {percentil_75_teorico:.4f} m/s")
    print(f"   P75 empírico = {percentil_75_empirico:.4f} m/s")
    
    # Usar scipy para verificar
    percentil_75_scipy = stats.weibull_min.ppf(0.75, k_estimado, loc=0, scale=c_estimado)
    print(f"   P75 scipy = {percentil_75_scipy:.4f} m/s")
    
    opciones_p75 = [0.8, 2.1, 3.5, 4.1, 1.6]
    diferencias_p75 = [abs(percentil_75_teorico - op) for op in opciones_p75]
    mejor_p75_idx = diferencias_p75.index(min(diferencias_p75))
    mejor_p75 = opciones_p75[mejor_p75_idx]
    
    print(f"\n   🎯 PERCENTIL 75 = {percentil_75_teorico:.2f} m/s")
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_p75, 1):
        diff = abs(percentil_75_teorico - opcion)
        marca = "✅" if diff == min(diferencias_p75) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # 5. PROBABILIDAD P(V > P75)
    print(f"\n5️⃣ PROBABILIDAD P(V > PERCENTIL 75):")
    
    # Por definición, P(V > P75) = 1 - 0.75 = 0.25
    prob_teorica = 0.25
    
    # Verificar usando la función de supervivencia
    prob_scipy = 1 - stats.weibull_min.cdf(percentil_75_teorico, k_estimado, loc=0, scale=c_estimado)
    
    # Verificar empíricamente
    prob_empirica = np.sum(velocidades > percentil_75_empirico) / len(velocidades)
    
    print(f"   Por definición: P(V > P75) = 0.25")
    print(f"   Verificación scipy: {prob_scipy:.4f}")
    print(f"   Verificación empírica: {prob_empirica:.4f}")
    
    opciones_prob = [0.15, 0.42, 0.25, 0.61, 0.34]
    diferencias_prob = [abs(prob_teorica - op) for op in opciones_prob]
    mejor_prob_idx = diferencias_prob.index(min(diferencias_prob))
    mejor_prob = opciones_prob[mejor_prob_idx]
    
    print(f"\n   🎯 P(V > P75) = {prob_teorica:.2f}")
    print(f"   Comparación con opciones:")
    for i, opcion in enumerate(opciones_prob, 1):
        diff = abs(prob_teorica - opcion)
        marca = "✅" if diff == min(diferencias_prob) else "❌"
        print(f"   {i}) {opcion} - Diferencia: {diff:.2f} {marca}")
    
    # Análisis adicional de la distribución
    print(f"\n6️⃣ ANÁLISIS ADICIONAL:")
    print(f"   Histograma de frecuencias:")
    valores_unicos, frecuencias = np.unique(velocidades, return_counts=True)
    for val, freq in zip(valores_unicos, frecuencias):
        porcentaje = (freq / len(velocidades)) * 100
        print(f"   {val:.1f} m/s: {freq:2d} observaciones ({porcentaje:4.1f}%)")
    
    # Resumen final
    print(f"\n🎯 RESUMEN DE RESPUESTAS:")
    print(f"   a) Parámetro k: {mejor_k}")
    print(f"   b) Parámetro c: {mejor_c}")
    print(f"   c) Percentil 75: {mejor_p75}")
    print(f"   d) P(V > P75): {mejor_prob}")
    
    return {
        'k': mejor_k,
        'c': mejor_c,
        'percentil_75': mejor_p75,
        'probabilidad': mejor_prob,
        'k_estimado': k_estimado,
        'c_estimado': c_estimado,
        'p75_calculado': percentil_75_teorico
    }

if __name__ == "__main__":
    resultados = analizar_weibull_datos_extensos()
    print(f"\n🎯 RESPUESTAS FINALES:")
    for clave, valor in resultados.items():
        if 'estimado' not in clave and 'calculado' not in clave:
            print(f"   {clave}: {valor}")