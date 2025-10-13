"""
SOLUCIÓN DETALLADA: Problema del Microchip con Distribución Exponencial

ENUNCIADO:
Se estima que el tiempo transcurrido hasta la falla de un microchip de un computador 
se distribuye exponencialmente con media de tres años. Una compañía ofrece garantía 
por el primer año de uso. ¿Qué porcentaje de pólizas tendrá que pagar una reclamación?

DESARROLLO MATEMÁTICO:
"""

import math

print("="*80)
print("SOLUCIÓN PASO A PASO")
print("="*80)

print("PASO 1: Identificar los parámetros")
print("-" * 40)
print("• Variable aleatoria X: Tiempo hasta la falla del microchip")
print("• Distribución: Exponencial")
print("• Media (μ): 3 años")
print("• Período de garantía: 1 año")
print()

print("PASO 2: Determinar el parámetro λ")
print("-" * 40)
print("Para una distribución exponencial:")
print("μ = E[X] = 1/λ")
print("Por lo tanto: λ = 1/μ")
print(f"λ = 1/3 = {1/3:.6f}")
print()

print("PASO 3: Función de distribución exponencial")
print("-" * 40)
print("Función de densidad: f(x) = λe^(-λx), x ≥ 0")
print("Función de distribución acumulativa: F(x) = 1 - e^(-λx), x ≥ 0")
print()

print("PASO 4: Calcular la probabilidad de reclamación")
print("-" * 40)
print("Necesitamos: P(X ≤ 1) = F(1)")
print("P(X ≤ 1) = 1 - e^(-λ×1)")
lambda_val = 1/3
print(f"P(X ≤ 1) = 1 - e^(-{lambda_val:.6f}×1)")
print(f"P(X ≤ 1) = 1 - e^(-{lambda_val:.6f})")
exp_val = math.exp(-lambda_val)
print(f"P(X ≤ 1) = 1 - {exp_val:.6f}")
prob = 1 - exp_val
print(f"P(X ≤ 1) = {prob:.6f}")
print()

print("PASO 5: Convertir a porcentaje")
print("-" * 40)
porcentaje = prob * 100
print(f"Porcentaje = {prob:.6f} × 100% = {porcentaje:.2f}%")
print()

print("PASO 6: Verificar con las opciones")
print("-" * 40)
print("a) 28.35%")
print("b) 0.7189")
print("c) 71.89%") 
print("d) 0.2835")
print()
print(f"Nuestro resultado: {porcentaje:.2f}%")
print("Nota: La opción b) en decimal sería 71.89%, y la opción d) en decimal sería 28.35%")
print()

print("="*80)
print("RESPUESTA FINAL")
print("="*80)
print(f"El porcentaje de pólizas que tendrá reclamación es: {porcentaje:.2f}%")
print()
print("RESPUESTA CORRECTA: a) 28.35%")
print("(También podría ser d) 0.2835 si se interpreta como decimal)")
print("="*80)

print("\nINTERPRETACIÓN:")
print(f"• {porcentaje:.2f}% de los microchips fallarán durante el primer año")
print(f"• {100-porcentaje:.2f}% de los microchips sobrevivirán el primer año")
print("• La compañía deberá pagar aproximadamente 1 de cada 4 pólizas de garantía")