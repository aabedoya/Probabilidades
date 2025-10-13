"""
VERIFICACIÓN FINAL: Problema de Colesterol en Hombres

DATOS DEL PROBLEMA:
- Hombre de 35 años (grupo 20-40 años)
- μ = 200 mg/dL, σ = 25 mg/dL
- Pregunta: P(X > 195) = ?
"""

from scipy import stats
import math

print("="*60)
print("VERIFICACIÓN FINAL")
print("="*60)

# Parámetros
mu = 200
sigma = 25
x = 195

print(f"Parámetros: μ = {mu}, σ = {sigma}")
print(f"Valor crítico: {x} mg/dL")
print()

# Cálculo paso a paso
print("CÁLCULO DETALLADO:")
print("1. Estandarización:")
z = (x - mu) / sigma
print(f"   Z = ({x} - {mu}) / {sigma} = {z}")
print()

print("2. Probabilidad acumulada:")
phi_z = stats.norm.cdf(z)
print(f"   Φ({z}) = {phi_z:.6f}")
print()

print("3. Probabilidad objetivo:")
prob_mayor = 1 - phi_z
print(f"   P(X > {x}) = 1 - Φ({z}) = {prob_mayor:.6f}")
print()

# Verificación con múltiples métodos
print("VERIFICACIONES:")
print("Método 1 (manual):")
prob1 = 1 - stats.norm.cdf(z)
print(f"   P(Z > {z}) = {prob1:.6f}")

print("Método 2 (directo):")
prob2 = 1 - stats.norm.cdf(x, mu, sigma)
print(f"   P(X > {x}) = {prob2:.6f}")

print("Método 3 (complementaria):")
prob3 = stats.norm.sf(x, mu, sigma)  # survival function = 1 - cdf
print(f"   sf({x}) = {prob3:.6f}")

print()
print("TODAS LAS VERIFICACIONES COINCIDEN" if abs(prob1 - prob2) < 1e-10 and abs(prob2 - prob3) < 1e-10 else "ERROR EN CÁLCULOS")
print()

# Análisis final de opciones
print("ANÁLISIS FINAL DE OPCIONES:")
opciones = [0.6306, 0.3694, 0.4207, 0.5793]
letras = ['a', 'b', 'c', 'd']

resultado_final = prob_mayor

for i, (letra, valor) in enumerate(zip(letras, opciones)):
    diferencia = abs(valor - resultado_final)
    if diferencia < 0.001:
        print(f"✓ {letra}) {valor} - CORRECTO (diferencia: {diferencia:.6f})")
    else:
        print(f"  {letra}) {valor} - diferencia: {diferencia:.6f}")

print()
print("="*60)
print(f"RESPUESTA VERIFICADA: d) 0.5793")
print(f"PROBABILIDAD EXACTA: {resultado_final:.6f}")
print("="*60)

# Interpretación final
print("\nINTERPRETACIÓN:")
print("• 195 mg/dL está 0.2σ por debajo de la media")
print("• Esto corresponde al percentil 42.1")
print("• Por tanto, 57.93% de los hombres tendrán > 195 mg/dL")
print("• La respuesta d) 0.5793 es la correcta")