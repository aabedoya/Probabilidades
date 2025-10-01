"""
Problema de Distribución Binomial - Éxito de Nuevo Producto

Datos:
- Probabilidad de éxito del producto: p = 0.65
- Número de personas encuestadas: n = 10
- Pregunta: P(X ≤ 4) donde X = número de personas que comprarían el producto

Opciones de respuesta:
0.9057, 0.1256, 0.0943, 0.8768
"""

import math
from scipy import stats

def resolver_binomial_producto():
    print("=" * 80)
    print("PROBLEMA DE DISTRIBUCIÓN BINOMIAL - ÉXITO DE NUEVO PRODUCTO")
    print("=" * 80)
    
    # Parámetros del problema
    n = 10      # Número de ensayos (personas encuestadas)
    p = 0.65    # Probabilidad de éxito (comprar el producto)
    q = 1 - p   # Probabilidad de fracaso
    
    print(f"\n1️⃣ IDENTIFICACIÓN DEL PROBLEMA:")
    print(f"   • Tipo: Distribución Binomial")
    print(f"   • n = {n} (personas encuestadas)")
    print(f"   • p = {p} (probabilidad de comprar)")
    print(f"   • q = {q} (probabilidad de no comprar)")
    print(f"   • Variable X = número de personas que comprarían")
    print(f"   • Pregunta: P(X ≤ 4)")
    
    print(f"\n2️⃣ FÓRMULA DE DISTRIBUCIÓN BINOMIAL:")
    print(f"   P(X = k) = C(n,k) × p^k × q^(n-k)")
    print(f"   P(X ≤ 4) = P(X=0) + P(X=1) + P(X=2) + P(X=3) + P(X=4)")
    
    # Calcular cada probabilidad individual
    print(f"\n3️⃣ CÁLCULOS INDIVIDUALES:")
    
    probabilidades = []
    total_acumulada = 0
    
    for k in range(5):  # k = 0, 1, 2, 3, 4
        # Coeficiente binomial
        coef_binomial = math.comb(n, k)
        
        # Probabilidad para k éxitos
        prob_k = coef_binomial * (p ** k) * (q ** (n - k))
        probabilidades.append(prob_k)
        total_acumulada += prob_k
        
        print(f"   P(X={k}) = C({n},{k}) × {p}^{k} × {q}^{n-k}")
        print(f"   P(X={k}) = {coef_binomial} × {p**k:.6f} × {q**(n-k):.6f}")
        print(f"   P(X={k}) = {prob_k:.6f}")
        print()
    
    print(f"4️⃣ PROBABILIDAD ACUMULADA:")
    print(f"   P(X ≤ 4) = {' + '.join([f'{p:.6f}' for p in probabilidades])}")
    print(f"   P(X ≤ 4) = {total_acumulada:.6f}")
    
    # Verificación usando scipy
    prob_scipy = stats.binom.cdf(4, n, p)
    print(f"\n5️⃣ VERIFICACIÓN CON SCIPY:")
    print(f"   stats.binom.cdf(4, {n}, {p}) = {prob_scipy:.6f}")
    
    # Redondear a 4 decimales
    resultado = round(total_acumulada, 4)
    
    print(f"\n6️⃣ RESULTADO FINAL:")
    print(f"   P(X ≤ 4) = {resultado}")
    
    # Comparar con las opciones
    opciones = [0.9057, 0.1256, 0.0943, 0.8768]
    print(f"\n7️⃣ COMPARACIÓN CON LAS OPCIONES:")
    
    for i, opcion in enumerate(opciones, 1):
        diferencia = abs(resultado - opcion)
        marca = "✅" if diferencia < 0.01 else "❌"
        print(f"   Opción {i}: {opcion} - Diferencia: {diferencia:.4f} {marca}")
    
    # Encontrar la opción más cercana
    diferencias = [abs(resultado - opcion) for opcion in opciones]
    mejor_opcion_idx = diferencias.index(min(diferencias))
    mejor_opcion = opciones[mejor_opcion_idx]
    
    print(f"\n🎯 RESPUESTA CORRECTA:")
    print(f"   La opción más cercana es: {mejor_opcion}")
    
    return resultado, mejor_opcion

if __name__ == "__main__":
    resultado, opcion_correcta = resolver_binomial_producto()
    print(f"\n🎯 RESPUESTA: {opcion_correcta}")