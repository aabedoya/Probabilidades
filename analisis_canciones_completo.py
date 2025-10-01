"""
Análisis adicional - ¿Podría ser permutaciones?
Verificando si el problema se refiere a permutaciones en lugar de combinaciones
"""

import math

def analisis_completo_canciones():
    print("=" * 80)
    print("ANÁLISIS COMPLETO - COMBINACIONES vs PERMUTACIONES")
    print("=" * 80)
    
    n = 15  # Total de canciones
    r = 2   # Canciones a seleccionar
    
    print(f"\n🤔 REVISIÓN DEL PROBLEMA:")
    print(f"   'Un asistente debe escoger las 2 canciones SIN REPETIRLAS'")
    print(f"   ¿Importa el ORDEN en que se solicitan?")
    
    # Combinaciones (orden NO importa)
    combinaciones = math.comb(n, r)
    print(f"\n1️⃣ SI EL ORDEN NO IMPORTA (COMBINACIONES):")
    print(f"   C(15,2) = 15!/(2!×13!) = (15×14)/(2×1) = {combinaciones}")
    print(f"   Ejemplo: 'Canción A y Canción B' = 'Canción B y Canción A'")
    
    # Permutaciones (orden SÍ importa)
    permutaciones = math.perm(n, r)
    print(f"\n2️⃣ SI EL ORDEN SÍ IMPORTA (PERMUTACIONES):")
    print(f"   P(15,2) = 15!/(15-2)! = 15!/13! = 15×14 = {permutaciones}")
    print(f"   Ejemplo: 'Primera: Canción A, Segunda: Canción B' ≠ 'Primera: Canción B, Segunda: Canción A'")
    
    # Comparar con las opciones
    opciones = [123, 210, 245, 120]
    
    print(f"\n3️⃣ COMPARACIÓN CON LAS OPCIONES:")
    print(f"   Opciones disponibles: {opciones}")
    print(f"   Resultado Combinaciones: {combinaciones}")
    print(f"   Resultado Permutaciones: {permutaciones}")
    
    # Buscar la opción más cercana
    diferencias_comb = [abs(combinaciones - op) for op in opciones]
    diferencias_perm = [abs(permutaciones - op) for op in opciones]
    
    mejor_comb_idx = diferencias_comb.index(min(diferencias_comb))
    mejor_perm_idx = diferencias_perm.index(min(diferencias_perm))
    
    print(f"\n4️⃣ ANÁLISIS DE DIFERENCIAS:")
    for i, opcion in enumerate(opciones):
        diff_comb = abs(combinaciones - opcion)
        diff_perm = abs(permutaciones - opcion)
        print(f"   Opción {opcion}:")
        print(f"     vs Combinaciones: diferencia {diff_comb}")
        print(f"     vs Permutaciones: diferencia {diff_perm}")
    
    print(f"\n5️⃣ ANÁLISIS DEL CONTEXTO:")
    print(f"   El problema dice 'escoger las canciones'")
    print(f"   En un concierto, típicamente importa el ORDEN:")
    print(f"   - Primera canción vs Segunda canción")
    print(f"   - ¿Cuál abre el set? ¿Cuál cierra?")
    
    # Verificar si alguna opción coincide con cálculos alternativos
    print(f"\n6️⃣ VERIFICACIÓN DE CÁLCULOS ALTERNATIVOS:")
    
    # ¿Podría ser C(15,2) pero mal calculado?
    comb_manual = (15 * 14) // 2
    print(f"   C(15,2) manual: (15×14)/2 = {comb_manual}")
    
    # ¿Podría ser que incluyeran repeticiones?
    con_repeticion = 15 * 15  # Si se pudiera repetir
    print(f"   Con repetición: 15×15 = {con_repeticion}")
    
    # La opción más cercana
    if min(diferencias_comb) < min(diferencias_perm):
        mejor_opcion = opciones[mejor_comb_idx]
        tipo = "Combinaciones"
        diferencia = min(diferencias_comb)
    else:
        mejor_opcion = opciones[mejor_perm_idx]
        tipo = "Permutaciones"
        diferencia = min(diferencias_perm)
    
    print(f"\n🎯 CONCLUSIÓN:")
    print(f"   La respuesta matemáticamente correcta para:")
    print(f"   - Combinaciones (orden no importa): {combinaciones}")
    print(f"   - Permutaciones (orden importa): {permutaciones}")
    print(f"   ")
    print(f"   La opción más cercana es: {mejor_opcion}")
    print(f"   Interpretando el problema como: {tipo}")
    print(f"   Diferencia: {diferencia}")
    
    # Buscar la opción exacta más cercana a 105
    opcion_mas_cercana_105 = min(opciones, key=lambda x: abs(x - 105))
    print(f"\n   Para nuestro resultado de 105, la opción más cercana es: {opcion_mas_cercana_105}")
    
    return mejor_opcion

if __name__ == "__main__":
    resultado = analisis_completo_canciones()