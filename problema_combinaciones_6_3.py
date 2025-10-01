"""
Problema de Combinaciones
¿De cuántas maneras pueden seleccionarse tres elementos de un grupo de seis?
Utilice las letras A, B, C, D, E y F.
"""

import math
from itertools import combinations

def resolver_combinaciones():
    print("=" * 70)
    print("PROBLEMA DE COMBINACIONES - SELECCIÓN DE 3 DE 6 ELEMENTOS")
    print("=" * 70)
    
    # Datos del problema
    n = 6  # Total de elementos (A, B, C, D, E, F)
    r = 3  # Elementos a seleccionar
    elementos = ['A', 'B', 'C', 'D', 'E', 'F']
    
    print(f"\n1️⃣ DATOS DEL PROBLEMA:")
    print(f"   Elementos disponibles: {elementos}")
    print(f"   Total de elementos (n) = {n}")
    print(f"   Elementos a seleccionar (r) = {r}")
    print(f"   Tipo de problema: COMBINACIONES (el orden NO importa)")
    
    # Fórmula de combinaciones
    print(f"\n2️⃣ FÓRMULA DE COMBINACIONES:")
    print(f"   C(n,r) = n! / (r! × (n-r)!)")
    print(f"   C(6,3) = 6! / (3! × 3!)")
    
    # Cálculo paso a paso
    factorial_6 = math.factorial(6)
    factorial_3 = math.factorial(3)
    factorial_3_bis = math.factorial(3)
    
    print(f"\n3️⃣ CÁLCULO PASO A PASO:")
    print(f"   6! = {factorial_6}")
    print(f"   3! = {factorial_3}")
    print(f"   3! = {factorial_3_bis}")
    print(f"   C(6,3) = {factorial_6} / ({factorial_3} × {factorial_3_bis})")
    print(f"   C(6,3) = {factorial_6} / {factorial_3 * factorial_3_bis}")
    
    resultado = factorial_6 // (factorial_3 * factorial_3_bis)
    print(f"   C(6,3) = {resultado}")
    
    # Verificación usando función built-in
    resultado_verificacion = math.comb(6, 3)
    print(f"\n4️⃣ VERIFICACIÓN:")
    print(f"   math.comb(6,3) = {resultado_verificacion}")
    
    # Enumerar todas las combinaciones
    print(f"\n5️⃣ TODAS LAS COMBINACIONES POSIBLES:")
    todas_combinaciones = list(combinations(elementos, 3))
    
    for i, combo in enumerate(todas_combinaciones, 1):
        print(f"   {i:2d}. {''.join(combo)}")
    
    print(f"\n   Total de combinaciones encontradas: {len(todas_combinaciones)}")
    
    print(f"\n6️⃣ RESULTADO FINAL:")
    print(f"   Número de maneras de seleccionar 3 elementos de 6 = {resultado}")
    
    return resultado

if __name__ == "__main__":
    resultado = resolver_combinaciones()
    print(f"\n🎯 RESPUESTA: {resultado}")