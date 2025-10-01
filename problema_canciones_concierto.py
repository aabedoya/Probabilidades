"""
Problema de Combinaciones - Selección de Canciones en Concierto

Un artista debe interpretar 2 canciones de su primer álbum que tiene 15 canciones.
Un asistente debe escoger las 2 canciones SIN REPETIRLAS.

¿De cuántas formas diferentes puede seleccionar las canciones?

Opciones:
- 123 formas diferentes de solicitar las canciones
- 210 formas diferentes de seleccionarlas  
- 245 formas diferentes de seleccionar las canciones
- 120 formas diferentes de escoger las canciones
"""

import math
from itertools import combinations

def resolver_canciones_concierto():
    print("=" * 80)
    print("PROBLEMA DE COMBINACIONES - SELECCIÓN DE CANCIONES EN CONCIERTO")
    print("=" * 80)
    
    # Datos del problema
    n = 15  # Total de canciones en el álbum
    r = 2   # Canciones a seleccionar
    
    print(f"\n1️⃣ ANÁLISIS DEL PROBLEMA:")
    print(f"   • Total de canciones en el álbum: {n}")
    print(f"   • Canciones a seleccionar: {r}")
    print(f"   • Restricción: SIN REPETIR canciones")
    print(f"   • Pregunta: ¿De cuántas formas se pueden seleccionar?")
    
    print(f"\n2️⃣ TIPO DE PROBLEMA:")
    print(f"   • Es un problema de COMBINACIONES (no permutaciones)")
    print(f"   • Razón: El ORDEN no importa en la selección")
    print(f"   • Seleccionar {r} elementos de un conjunto de {n}")
    
    print(f"\n3️⃣ FÓRMULA DE COMBINACIONES:")
    print(f"   C(n,r) = n! / (r! × (n-r)!)")
    print(f"   C({n},{r}) = {n}! / ({r}! × {n-r}!)")
    
    # Cálculo paso a paso
    factorial_n = math.factorial(n)
    factorial_r = math.factorial(r)
    factorial_n_minus_r = math.factorial(n - r)
    
    print(f"\n4️⃣ CÁLCULO PASO A PASO:")
    print(f"   {n}! = {factorial_n}")
    print(f"   {r}! = {factorial_r}")
    print(f"   ({n}-{r})! = {n-r}! = {factorial_n_minus_r}")
    
    print(f"\n   C({n},{r}) = {factorial_n} / ({factorial_r} × {factorial_n_minus_r})")
    print(f"   C({n},{r}) = {factorial_n} / {factorial_r * factorial_n_minus_r}")
    
    resultado = factorial_n // (factorial_r * factorial_n_minus_r)
    print(f"   C({n},{r}) = {resultado}")
    
    # Verificación con función built-in
    resultado_verificacion = math.comb(n, r)
    print(f"\n5️⃣ VERIFICACIÓN:")
    print(f"   math.comb({n},{r}) = {resultado_verificacion}")
    
    # Método alternativo más simple
    metodo_simple = (n * (n-1)) // (2 * 1)
    print(f"   Método alternativo: ({n} × {n-1}) / (2 × 1) = {metodo_simple}")
    
    # Comparar con las opciones
    opciones = [
        (123, "formas diferentes de solicitar las canciones"),
        (210, "formas diferentes de seleccionarlas"),
        (245, "formas diferentes de seleccionar las canciones"),
        (120, "formas diferentes de escoger las canciones")
    ]
    
    print(f"\n6️⃣ COMPARACIÓN CON LAS OPCIONES:")
    for i, (valor, descripcion) in enumerate(opciones, 1):
        marca = "✅" if valor == resultado else "❌"
        print(f"   Opción {i}: {valor} {descripcion} {marca}")
    
    # Encontrar la opción correcta
    opcion_correcta = None
    for i, (valor, descripcion) in enumerate(opciones, 1):
        if valor == resultado:
            opcion_correcta = f"Opción {i}: {descripcion}"
            break
    
    print(f"\n7️⃣ VERIFICACIÓN ENUMERANDO ALGUNAS COMBINACIONES:")
    print(f"   Ejemplos de combinaciones (mostrando primeras 10):")
    
    # Simular con canciones numeradas del 1 al 15
    canciones = list(range(1, n+1))
    todas_combinaciones = list(combinations(canciones, r))
    
    for i, combo in enumerate(todas_combinaciones[:10], 1):
        print(f"   {i:2d}. Canciones {combo[0]} y {combo[1]}")
    
    if len(todas_combinaciones) > 10:
        print(f"   ... (y {len(todas_combinaciones) - 10} combinaciones más)")
    
    print(f"   Total de combinaciones: {len(todas_combinaciones)}")
    
    print(f"\n🎯 RESPUESTA CORRECTA:")
    print(f"   El asistente {opcion_correcta}")
    print(f"   Número total de formas: {resultado}")
    
    return resultado, opcion_correcta

if __name__ == "__main__":
    resultado, opcion = resolver_canciones_concierto()
    print(f"\n🎯 RESPUESTA: {resultado} formas diferentes")