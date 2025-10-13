"""
SOLUCIÓN CONCISA: Problema de Demanda Normal

ENUNCIADO:
Demanda ~ Normal(μ=1200, σ²=10000)
¿P(X > 1000) = ?

SOLUCIÓN PASO A PASO:
"""

from scipy import stats
import math

print("="*50)
print("SOLUCIÓN PASO A PASO")
print("="*50)

# Datos
mu = 1200
varianza = 10000
sigma = math.sqrt(varianza)
x = 1000

print(f"Datos: μ = {mu}, σ² = {varianza}, σ = {sigma}")
print(f"Buscar: P(X > {x})")
print()

print("PASO 1: ESTANDARIZACIÓN")
z = (x - mu) / sigma
print(f"Z = (X - μ)/σ = ({x} - {mu})/{sigma} = {z}")
print()

print("PASO 2: PROBABILIDAD")
print(f"P(X > {x}) = P(Z > {z})")
print(f"P(Z > {z}) = 1 - Φ({z})")

phi_z = stats.norm.cdf(z)
resultado = 1 - phi_z

print(f"P(Z > {z}) = 1 - {phi_z:.6f}")
print(f"P(Z > {z}) = {resultado:.6f}")
print()

print("VERIFICACIÓN CON TABLA Z:")
print("Para Z = -2.00: Φ(-2.00) ≈ 0.0228")
print("Por tanto: P(Z > -2.00) = 1 - 0.0228 = 0.9772")
print()

print("ANÁLISIS DE OPCIONES:")
opciones = [0.9767, 0.0228, 0.9772, 0.4772]
letras = ['a', 'b', 'c', 'd']

for letra, opcion in zip(letras, opciones):
    diferencia = abs(opcion - resultado)
    marca = "✓" if diferencia < 0.001 else " "
    print(f"{marca} {letra}) {opcion} (diferencia: {diferencia:.6f})")

print()
print("="*50)
print("RESPUESTA: c) 0.9772")
print("="*50)

print("\nRAZONAMIENTO:")
print("• 1000 está 2σ por debajo de la media")
print("• Z = -2 es un valor bastante alejado hacia la izquierda")
print("• La mayoría de los datos (97.72%) estará por encima")
print("• Solo 2.28% estará por debajo de 1000")