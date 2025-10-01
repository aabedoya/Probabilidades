"""
Problema de Probabilidades - Preferencias de Vivienda por Género

Una encuesta sobre preferencias de vivir en ciudad vs urbanizaciones:
- 33% son mujeres
- De las mujeres, 43% prefieren vivir en la ciudad
- La probabilidad total (hombres + mujeres) de preferir la ciudad es 0.605

Pregunta: ¿Cuál es la probabilidad de que un hombre elegido al azar prefiera vivir en la ciudad?
"""

def resolver_problema_preferencias():
    print("=" * 80)
    print("PROBLEMA DE PROBABILIDADES - PREFERENCIAS DE VIVIENDA POR GÉNERO")
    print("=" * 80)
    
    # Definir eventos
    print("\n1️⃣ DEFINICIÓN DE EVENTOS:")
    print("   M = La persona es mujer")
    print("   H = La persona es hombre") 
    print("   C = La persona prefiere vivir en la ciudad")
    
    # Datos del problema
    P_M = 0.33        # 33% son mujeres
    P_H = 1 - P_M     # 67% son hombres (complemento)
    P_C_dado_M = 0.43 # 43% de las mujeres prefieren la ciudad
    P_C = 0.605       # 60.5% del total prefiere la ciudad
    
    print(f"\n2️⃣ DATOS CONOCIDOS:")
    print(f"   P(M) = {P_M}")
    print(f"   P(H) = {P_H}")
    print(f"   P(C|M) = {P_C_dado_M}")
    print(f"   P(C) = {P_C}")
    
    print(f"\n3️⃣ LO QUE BUSCAMOS:")
    print(f"   P(C|H) = Probabilidad de que un hombre prefiera la ciudad")
    
    # Aplicar teorema de probabilidad total
    print(f"\n4️⃣ TEOREMA DE PROBABILIDAD TOTAL:")
    print(f"   P(C) = P(C|M) × P(M) + P(C|H) × P(H)")
    print(f"   {P_C} = {P_C_dado_M} × {P_M} + P(C|H) × {P_H}")
    
    # Calcular P(C|M) × P(M)
    termino_mujeres = P_C_dado_M * P_M
    print(f"\n5️⃣ CÁLCULOS PASO A PASO:")
    print(f"   P(C|M) × P(M) = {P_C_dado_M} × {P_M} = {termino_mujeres}")
    
    # Despejar P(C|H)
    print(f"\n   Sustituyendo en la ecuación:")
    print(f"   {P_C} = {termino_mujeres} + P(C|H) × {P_H}")
    print(f"   P(C|H) × {P_H} = {P_C} - {termino_mujeres}")
    
    termino_hombres = P_C - termino_mujeres
    P_C_dado_H = termino_hombres / P_H
    
    print(f"   P(C|H) × {P_H} = {termino_hombres}")
    print(f"   P(C|H) = {termino_hombres} / {P_H}")
    print(f"   P(C|H) = {P_C_dado_H}")
    
    # Redondear a 4 decimales
    resultado = round(P_C_dado_H, 4)
    
    print(f"\n6️⃣ RESULTADO FINAL:")
    print(f"   P(C|H) = {resultado}")
    
    # Verificación
    print(f"\n7️⃣ VERIFICACIÓN:")
    verificacion = (P_C_dado_M * P_M) + (P_C_dado_H * P_H)
    print(f"   Verificando P(C) = P(C|M)×P(M) + P(C|H)×P(H)")
    print(f"   = {P_C_dado_M}×{P_M} + {P_C_dado_H}×{P_H}")
    print(f"   = {P_C_dado_M * P_M} + {P_C_dado_H * P_H}")
    print(f"   = {verificacion}")
    print(f"   ✅ Coincide con P(C) = {P_C}")
    
    return resultado

if __name__ == "__main__":
    resultado = resolver_problema_preferencias()
    print(f"\n🎯 RESPUESTA: {resultado}")