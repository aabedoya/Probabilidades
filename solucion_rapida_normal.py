"""
SOLUCIÓN RÁPIDA: Problema de Distribución Normal

ENUNCIADO:
Probabilidad de que una pieza esté a máximo una desviación estándar de la media.
Distribución: Normal con μ = 2 cm, σ = 0.05 cm

SOLUCIÓN DIRECTA:
"""

from scipy import stats

print("="*60)
print("SOLUCIÓN DIRECTA")
print("="*60)

print("PREGUNTA: P(μ - σ ≤ X ≤ μ + σ) = ?")
print()

print("CONCEPTO CLAVE: REGLA EMPÍRICA")
print("Para CUALQUIER distribución normal:")
print("• ~68% de los datos están dentro de 1σ")
print("• ~95% de los datos están dentro de 2σ")  
print("• ~99.7% de los datos están dentro de 3σ")
print()

print("CÁLCULO:")
print("P(-1 ≤ Z ≤ 1) donde Z ~ N(0,1)")

# Cálculo exacto
prob = stats.norm.cdf(1) - stats.norm.cdf(-1)
print(f"P(-1 ≤ Z ≤ 1) = {prob:.6f} ≈ 0.68")
print()

print("ANÁLISIS DE OPCIONES:")
print("a) 1,96 → Valor Z para 95% de confianza (NO es probabilidad)")
print("b) 0,68 → ✓ CORRECTO (68% = regla empírica para 1σ)")
print("c) 0 → Incorrecto")
print("d) 0,95 → Probabilidad para 2σ, no para 1σ")
print()

print("="*60)
print("RESPUESTA: b) 0,68")
print("="*60)
print("RAZÓN: Es la regla empírica fundamental de la distribución normal.")
print("Independientemente de los valores específicos de μ y σ,")
print("aproximadamente 68% de los datos siempre caen dentro de 1σ.")