"""
Problema de Distribución Normal - Niveles de Colesterol en Mujeres

Pregunta: ¿Cuál es la probabilidad de que al seleccionar una mujer con edad 
superior a los 40 años, tenga un nivel de colesterol entre 160 mg/dL y 190 mg/dL?

Datos de la tabla para mujeres > 40 años:
- Media (μ) = 195 mg/dL
- Desviación estándar (σ) = 10 mg/dL
- Distribución: Normal

Opciones de respuesta:
- 0.3951
- 0.3083
- 0.1524
- 0.1584
"""

import numpy as np
from scipy import stats
import math

def resolver_colesterol_mujeres():
    print("=" * 80)
    print("PROBLEMA DE DISTRIBUCIÓN NORMAL - NIVELES DE COLESTEROL")
    print("=" * 80)
    
    # Datos del problema para mujeres > 40 años
    mu = 195  # Media en mg/dL
    sigma = 10  # Desviación estándar en mg/dL
    limite_inferior = 160  # mg/dL
    limite_superior = 190  # mg/dL
    
    print(f"\n📊 DATOS DEL PROBLEMA:")
    print(f"   Población: Mujeres con edad > 40 años")
    print(f"   Media (μ): {mu} mg/dL")
    print(f"   Desviación estándar (σ): {sigma} mg/dL")
    print(f"   Distribución: Normal(μ={mu}, σ={sigma})")
    print(f"   Intervalo de interés: [{limite_inferior}, {limite_superior}] mg/dL")
    
    print(f"\n1️⃣ PREGUNTA:")
    print(f"   P({limite_inferior} ≤ X ≤ {limite_superior}) = ?")
    print(f"   donde X ~ N({mu}, {sigma}²)")
    
    print(f"\n2️⃣ ESTANDARIZACIÓN (CONVERSIÓN A Z):")
    print(f"   Fórmula: Z = (X - μ) / σ")
    
    # Calcular valores Z
    z_inferior = (limite_inferior - mu) / sigma
    z_superior = (limite_superior - mu) / sigma
    
    print(f"   Z₁ = ({limite_inferior} - {mu}) / {sigma} = {z_inferior}")
    print(f"   Z₂ = ({limite_superior} - {mu}) / {sigma} = {z_superior}")
    
    print(f"\n3️⃣ CÁLCULO DE PROBABILIDADES:")
    print(f"   P({limite_inferior} ≤ X ≤ {limite_superior}) = P({z_inferior} ≤ Z ≤ {z_superior})")
    print(f"   = Φ({z_superior}) - Φ({z_inferior})")
    
    # Calcular probabilidades usando scipy
    prob_z_superior = stats.norm.cdf(z_superior)
    prob_z_inferior = stats.norm.cdf(z_inferior)
    probabilidad_intervalo = prob_z_superior - prob_z_inferior
    
    print(f"   Φ({z_superior}) = {prob_z_superior:.6f}")
    print(f"   Φ({z_inferior}) = {prob_z_inferior:.6f}")
    print(f"   P({limite_inferior} ≤ X ≤ {limite_superior}) = {prob_z_superior:.6f} - {prob_z_inferior:.6f}")
    print(f"   P({limite_inferior} ≤ X ≤ {limite_superior}) = {probabilidad_intervalo:.6f}")
    
    # Verificación usando scipy directamente
    print(f"\n4️⃣ VERIFICACIÓN CON SCIPY:")
    prob_directa_superior = stats.norm.cdf(limite_superior, loc=mu, scale=sigma)
    prob_directa_inferior = stats.norm.cdf(limite_inferior, loc=mu, scale=sigma)
    prob_directa_intervalo = prob_directa_superior - prob_directa_inferior
    
    print(f"   P(X ≤ {limite_superior}) = {prob_directa_superior:.6f}")
    print(f"   P(X ≤ {limite_inferior}) = {prob_directa_inferior:.6f}")
    print(f"   P({limite_inferior} ≤ X ≤ {limite_superior}) = {prob_directa_intervalo:.6f}")
    
    print(f"\n5️⃣ INTERPRETACIÓN:")
    porcentaje = probabilidad_intervalo * 100
    print(f"   La probabilidad es {probabilidad_intervalo:.4f} o {porcentaje:.2f}%")
    print(f"   Esto significa que aproximadamente {porcentaje:.1f}% de las mujeres")
    print(f"   mayores de 40 años tienen colesterol entre 160 y 190 mg/dL")
    
    # Comparar con las opciones
    opciones = [0.3951, 0.3083, 0.1524, 0.1584]
    
    print(f"\n6️⃣ COMPARACIÓN CON LAS OPCIONES:")
    diferencias = [abs(probabilidad_intervalo - opcion) for opcion in opciones]
    mejor_opcion_idx = diferencias.index(min(diferencias))
    mejor_opcion = opciones[mejor_opcion_idx]
    
    for i, opcion in enumerate(opciones, 1):
        diferencia = abs(probabilidad_intervalo - opcion)
        porcentaje_opcion = opcion * 100
        marca = "✅" if diferencia == min(diferencias) else "❌"
        print(f"   Opción {i}: {opcion} ({porcentaje_opcion:.2f}%) - Diferencia: {diferencia:.6f} {marca}")
    
    print(f"\n7️⃣ ANÁLISIS ADICIONAL:")
    print(f"   El intervalo [160, 190] está:")
    print(f"   • 160 mg/dL: {(160-mu)/sigma:.1f} desviaciones estándar por debajo de la media")
    print(f"   • 190 mg/dL: {(190-mu)/sigma:.1f} desviaciones estándar por debajo de la media")
    print(f"   • Ambos valores están por debajo de la media de 195 mg/dL")
    
    # Verificación usando tabla Z estándar
    print(f"\n8️⃣ VERIFICACIÓN CON TABLA Z:")
    print(f"   Para Z = -3.5: Φ(-3.5) ≈ 0.0002 (muy cercano a 0)")
    print(f"   Para Z = -0.5: Φ(-0.5) ≈ 0.3085")
    print(f"   Diferencia: 0.3085 - 0.0002 ≈ 0.3083")
    
    print(f"\n🎯 RESULTADO FINAL:")
    print(f"   La probabilidad es: {probabilidad_intervalo:.4f}")
    print(f"   La respuesta correcta es: {mejor_opcion}")
    
    return probabilidad_intervalo, mejor_opcion

if __name__ == "__main__":
    prob, respuesta = resolver_colesterol_mujeres()
    print(f"\n🎯 RESPUESTA: {respuesta}")