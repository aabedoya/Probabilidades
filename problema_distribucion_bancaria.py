"""
Problema de Distribuciones - Atención de Clientes en Banco

Un gerente bancario quiere optimizar el tiempo de atención:
- ANTES de capacitación: 5 personas cada 15 minutos
- DESPUÉS de capacitación: 4 personas cada 10 minutos
- Jornada laboral: 8 horas

¿Qué tipo de distribución describe esta variable aleatoria?

Opciones: Bernoulli, Poisson, Hipergeométrica, Binomial
"""

def analizar_distribucion_bancaria():
    print("=" * 80)
    print("ANÁLISIS DE DISTRIBUCIONES - ATENCIÓN DE CLIENTES EN BANCO")
    print("=" * 80)
    
    print("\n1️⃣ CARACTERÍSTICAS DEL PROBLEMA:")
    print("   • Variable: Número de personas atendidas en un tiempo dado")
    print("   • Contexto: Conteo de eventos en intervalos de tiempo")
    print("   • Antes: 5 personas / 15 minutos")
    print("   • Después: 4 personas / 10 minutos")
    print("   • Pregunta: ¿Cuántas personas en 8 horas?")
    
    # Calcular tasas por hora
    print("\n2️⃣ CÁLCULO DE TASAS POR HORA:")
    
    # Antes de la capacitación
    personas_antes_15min = 5
    minutos_antes = 15
    tasa_antes_por_minuto = personas_antes_15min / minutos_antes
    tasa_antes_por_hora = tasa_antes_por_minuto * 60
    
    print(f"   ANTES de capacitación:")
    print(f"   • {personas_antes_15min} personas en {minutos_antes} minutos")
    print(f"   • Tasa: {tasa_antes_por_minuto:.3f} personas/minuto")
    print(f"   • Tasa: {tasa_antes_por_hora:.1f} personas/hora")
    
    # Después de la capacitación
    personas_despues_10min = 4
    minutos_despues = 10
    tasa_despues_por_minuto = personas_despues_10min / minutos_despues
    tasa_despues_por_hora = tasa_despues_por_minuto * 60
    
    print(f"   DESPUÉS de capacitación:")
    print(f"   • {personas_despues_10min} personas en {minutos_despues} minutos")
    print(f"   • Tasa: {tasa_despues_por_minuto:.3f} personas/minuto")
    print(f"   • Tasa: {tasa_despues_por_hora:.1f} personas/hora")
    
    # Calcular para 8 horas
    horas_jornada = 8
    personas_antes_jornada = tasa_antes_por_hora * horas_jornada
    personas_despues_jornada = tasa_despues_por_hora * horas_jornada
    
    print(f"\n3️⃣ PERSONAS ATENDIDAS EN {horas_jornada} HORAS:")
    print(f"   • ANTES: {personas_antes_jornada:.0f} personas")
    print(f"   • DESPUÉS: {personas_despues_jornada:.0f} personas")
    print(f"   • Mejora: {personas_despues_jornada - personas_antes_jornada:.0f} personas adicionales")
    
    print("\n4️⃣ ANÁLISIS DE TIPOS DE DISTRIBUCIÓN:")
    
    print("\n   🔹 BERNOULLI:")
    print("   • Características: Solo 2 resultados (éxito/fracaso)")
    print("   • Aplicación: Un solo ensayo")
    print("   • ¿Se ajusta?: ❌ No, aquí contamos múltiples eventos")
    
    print("\n   🔹 BINOMIAL:")
    print("   • Características: n ensayos independientes, probabilidad constante")
    print("   • Aplicación: Número de éxitos en n ensayos")
    print("   • ¿Se ajusta?: ❌ No, no tenemos ensayos fijos ni probabilidad de éxito/fracaso")
    
    print("\n   🔹 HIPERGEOMÉTRICA:")
    print("   • Características: Muestreo sin reposición de población finita")
    print("   • Aplicación: Selección de elementos de grupos específicos")
    print("   • ¿Se ajusta?: ❌ No, no hay muestreo sin reposición")
    
    print("\n   🔹 POISSON:")
    print("   • Características: Conteo de eventos en tiempo/espacio fijo")
    print("   • Condiciones:")
    print("     - Eventos ocurren independientemente")
    print("     - Tasa promedio constante (λ)")
    print("     - Probabilidad de múltiples eventos simultáneos ≈ 0")
    print("   • ¿Se ajusta?: ✅ SÍ")
    print("     - Contamos clientes atendidos en intervalos de tiempo")
    print("     - Tasa promedio conocida")
    print("     - Eventos independientes")
    
    print("\n5️⃣ JUSTIFICACIÓN DETALLADA - DISTRIBUCIÓN POISSON:")
    print("   ✅ Variable: X = número de clientes atendidos en tiempo t")
    print("   ✅ Parámetro λ = tasa promedio por unidad de tiempo")
    print(f"   ✅ Antes: λ₁ = {tasa_antes_por_hora:.1f} clientes/hora")
    print(f"   ✅ Después: λ₂ = {tasa_despues_por_hora:.1f} clientes/hora")
    print("   ✅ Para t horas: λₜ = λ × t")
    print("   ✅ Fórmula: P(X = k) = (λᵗe^(-λt)) / k!")
    
    print("\n6️⃣ EJEMPLO DE APLICACIÓN:")
    print("   Si queremos la probabilidad de atender exactamente k clientes en t horas:")
    print("   • Antes: P(X = k) = ((20×t)^k × e^(-20×t)) / k!")
    print("   • Después: P(X = k) = ((24×t)^k × e^(-24×t)) / k!")
    
    print(f"\n🎯 CONCLUSIÓN:")
    print(f"   La distribución de la variable aleatoria es de tipo: POISSON")
    print(f"   ")
    print(f"   Razón: Se cuenta el número de eventos (clientes atendidos)")
    print(f"   en intervalos de tiempo fijos, con tasa promedio constante.")
    
    return "Poisson"

if __name__ == "__main__":
    resultado = analizar_distribucion_bancaria()
    print(f"\n🎯 RESPUESTA: {resultado}")