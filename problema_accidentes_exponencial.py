"""
Problema de Distribución Exponencial - Accidentes de Tránsito

Datos:
- Accidentes siguen distribución Poisson: λ = 18 accidentes/día
- Tiempo entre accidentes sigue distribución exponencial
- Ambulancia tarda 30 minutos en llegar al hospital
- Pregunta: P(próximo accidente ocurra antes de 30 minutos)

Opciones: 0.6873, 0.5155, 0.3127, 0.4845
"""

import math

def resolver_accidentes_exponencial():
    print("=" * 80)
    print("PROBLEMA DE DISTRIBUCIÓN EXPONENCIAL - ACCIDENTES DE TRÁNSITO")
    print("=" * 80)
    
    # Datos del problema
    accidentes_por_dia = 18  # λ en accidentes/día
    tiempo_ambulancia_min = 30  # minutos
    horas_por_dia = 24
    minutos_por_dia = 24 * 60
    
    print(f"\n1️⃣ DATOS DEL PROBLEMA:")
    print(f"   • Accidentes por día: {accidentes_por_dia}")
    print(f"   • Distribución: Exponencial (tiempo entre accidentes)")
    print(f"   • Tiempo de ambulancia: {tiempo_ambulancia_min} minutos")
    print(f"   • Pregunta: P(próximo accidente < 30 min)")
    
    # Convertir tasa a minutos
    lambda_por_minuto = accidentes_por_dia / minutos_por_dia
    
    print(f"\n2️⃣ CONVERSIÓN DE TASA:")
    print(f"   • λ = {accidentes_por_dia} accidentes/día")
    print(f"   • λ = {accidentes_por_dia}/{minutos_por_dia} accidentes/minuto")
    print(f"   • λ = {lambda_por_minuto:.6f} accidentes/minuto")
    
    print(f"\n3️⃣ DISTRIBUCIÓN EXPONENCIAL:")
    print(f"   • Variable X = tiempo hasta el próximo accidente")
    print(f"   • Función de densidad: f(t) = λe^(-λt)")
    print(f"   • Función acumulada: F(t) = P(X ≤ t) = 1 - e^(-λt)")
    print(f"   • Parámetro: λ = {lambda_por_minuto:.6f} /minuto")
    
    # Calcular la probabilidad
    t = tiempo_ambulancia_min
    exponente = -lambda_por_minuto * t
    probabilidad = 1 - math.exp(exponente)
    
    print(f"\n4️⃣ CÁLCULO DE LA PROBABILIDAD:")
    print(f"   • P(X ≤ {t}) = 1 - e^(-λt)")
    print(f"   • P(X ≤ {t}) = 1 - e^(-{lambda_por_minuto:.6f} × {t})")
    print(f"   • P(X ≤ {t}) = 1 - e^({exponente:.6f})")
    print(f"   • P(X ≤ {t}) = 1 - {math.exp(exponente):.6f}")
    print(f"   • P(X ≤ {t}) = {probabilidad:.6f}")
    
    # Redondear a 4 decimales
    resultado = round(probabilidad, 4)
    
    print(f"\n5️⃣ RESULTADO:")
    print(f"   • P(próximo accidente < 30 min) = {resultado}")
    
    # Comparar con las opciones
    opciones = [0.6873, 0.5155, 0.3127, 0.4845]
    print(f"\n6️⃣ COMPARACIÓN CON LAS OPCIONES:")
    
    diferencias = []
    for i, opcion in enumerate(opciones, 1):
        diferencia = abs(resultado - opcion)
        diferencias.append(diferencia)
        marca = "✅" if diferencia < 0.01 else "❌"
        print(f"   Opción {i}: {opcion} - Diferencia: {diferencia:.4f} {marca}")
    
    # Encontrar la opción más cercana
    mejor_opcion_idx = diferencias.index(min(diferencias))
    mejor_opcion = opciones[mejor_opcion_idx]
    
    print(f"\n7️⃣ VERIFICACIÓN ADICIONAL:")
    print(f"   • Usando diferentes precisiones:")
    print(f"     - λ exacto = {accidentes_por_dia}/1440 = {accidentes_por_dia/1440}")
    print(f"     - e^(-λt) = e^(-{accidentes_por_dia/1440 * t:.4f}) = {math.exp(-accidentes_por_dia/1440 * t):.6f}")
    print(f"     - P(X ≤ 30) = 1 - {math.exp(-accidentes_por_dia/1440 * t):.6f} = {1 - math.exp(-accidentes_por_dia/1440 * t):.4f}")
    
    print(f"\n🎯 INTERPRETACIÓN:")
    print(f"   La probabilidad de {resultado:.4f} significa que hay un {resultado*100:.1f}%")
    print(f"   de probabilidad de que ocurra otro accidente antes de que")
    print(f"   la ambulancia termine de llevar al herido al hospital.")
    
    print(f"\n🎯 RESPUESTA CORRECTA:")
    print(f"   La opción más cercana es: {mejor_opcion}")
    
    return resultado, mejor_opcion

if __name__ == "__main__":
    resultado, opcion_correcta = resolver_accidentes_exponencial()
    print(f"\n🎯 RESPUESTA: {opcion_correcta}")