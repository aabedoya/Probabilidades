"""
Teorema de Bayes - Completar la frase
El teorema de Bayes es una proposición que expresa una probabilidad ______________ 
de un evento _____________ teniendo entre sus aplicaciones la _______________
"""

def explicar_teorema_bayes():
    print("=" * 80)
    print("TEOREMA DE BAYES - COMPLETAR LA FRASE")
    print("=" * 80)
    
    print("\n📚 TEOREMA DE BAYES:")
    print("El teorema de Bayes es una proposición fundamental en probabilidad que permite")
    print("calcular probabilidades condicionales inversas.")
    
    print("\n🎯 FRASE A COMPLETAR:")
    frase_incompleta = """El teorema de Bayes es una proposición que expresa una probabilidad ______________ 
de un evento _____________ teniendo entre sus aplicaciones la _______________"""
    print(frase_incompleta)
    
    print("\n✅ FRASE COMPLETADA:")
    frase_completa = """El teorema de Bayes es una proposición que expresa una probabilidad CONDICIONAL 
de un evento ALEATORIO teniendo entre sus aplicaciones la INFERENCIA ESTADÍSTICA"""
    print(frase_completa)
    
    print("\n📖 EXPLICACIÓN DE CADA TÉRMINO:")
    print("\n1️⃣ PROBABILIDAD CONDICIONAL:")
    print("   • Es la probabilidad de que ocurra un evento A, dado que ha ocurrido otro evento B")
    print("   • Se denota como P(A|B)")
    print("   • El Teorema de Bayes permite calcular P(A|B) conociendo P(B|A)")
    
    print("\n2️⃣ EVENTO ALEATORIO:")
    print("   • Es un suceso cuyo resultado no se puede predecir con certeza")
    print("   • Tiene una probabilidad asociada de ocurrencia")
    print("   • El Teorema de Bayes trabaja con eventos aleatorios relacionados")
    
    print("\n3️⃣ INFERENCIA ESTADÍSTICA:")
    print("   • Es el proceso de obtener conclusiones sobre una población")
    print("   • Se basa en datos de una muestra")
    print("   • El Teorema de Bayes es fundamental en inferencia bayesiana")
    print("   • Permite actualizar creencias con nueva evidencia")
    
    print("\n🧮 FÓRMULA DEL TEOREMA DE BAYES:")
    print("   P(A|B) = [P(B|A) × P(A)] / P(B)")
    print("\n   Donde:")
    print("   • P(A|B) = Probabilidad a posteriori (lo que queremos calcular)")
    print("   • P(B|A) = Verosimilitud (probabilidad de observar B dado A)")
    print("   • P(A) = Probabilidad a priori (conocimiento previo sobre A)")
    print("   • P(B) = Evidencia (probabilidad marginal de B)")
    
    print("\n🎯 OTRAS APLICACIONES IMPORTANTES:")
    print("   • Diagnóstico médico")
    print("   • Filtros de spam en email")
    print("   • Reconocimiento de patrones")
    print("   • Análisis de riesgo")
    print("   • Machine Learning (clasificación bayesiana)")
    
    return "CONDICIONAL", "ALEATORIO", "INFERENCIA ESTADÍSTICA"

if __name__ == "__main__":
    palabras = explicar_teorema_bayes()
    print(f"\n🎯 RESPUESTAS:")
    print(f"   1ª palabra: {palabras[0]}")
    print(f"   2ª palabra: {palabras[1]}")
    print(f"   3ª palabra: {palabras[2]}")