"""
Tests para verificar la correcta implementación de la Distribución de Weibull

Este archivo contiene tests para validar:
- Cálculos matemáticos correctos
- Casos especiales conocidos
- Propiedades estadísticas
- Generación de muestras

Autor: Proyecto Probabilidades
Fecha: 3 de septiembre de 2025
"""

import numpy as np
from scipy import stats
from scipy.special import gamma
import warnings
from distribucion_weibull import DistribucionWeibull

# Suprimir advertencias para tests
warnings.filterwarnings('ignore')

def test_creacion_distribucion():
    """Test básico de creación de distribución"""
    # Parámetros válidos
    weibull = DistribucionWeibull(k=2.0, lambda_param=1.0)
    assert weibull.k == 2.0
    assert weibull.lambda_param == 1.0

    # Parámetros inválidos deberían generar error
    try:
        weibull_invalido = DistribucionWeibull(k=-1.0, lambda_param=1.0)
        assert False, "Debería generar error con k negativo"
    except ValueError:
        pass

    try:
        weibull_invalido = DistribucionWeibull(k=1.0, lambda_param=-1.0)
        assert False, "Debería generar error con λ negativo"
    except ValueError:
        pass

def test_pdf_propiedades():
    """Test de propiedades de la PDF"""
    weibull = DistribucionWeibull(k=2.0, lambda_param=1.0)

    # PDF debe ser 0 para valores negativos
    assert weibull.pdf(-1.0) == 0.0
    assert weibull.pdf(-0.1) == 0.0

    # PDF debe ser positiva para valores positivos
    assert weibull.pdf(0.5) > 0
    assert weibull.pdf(1.0) > 0
    assert weibull.pdf(2.0) > 0

    # Integrar PDF debería dar aproximadamente 1
    x = np.linspace(0, 10, 10000)
    dx = x[1] - x[0]
    integral = np.sum(weibull.pdf(x)) * dx
    assert abs(integral - 1.0) < 0.01, f"Integral de PDF = {integral}, debería ser ≈ 1"

def test_cdf_propiedades():
    """Test de propiedades de la CDF"""
    weibull = DistribucionWeibull(k=2.0, lambda_param=1.0)

    # CDF debe ser 0 en x=0 y para valores negativos
    assert weibull.cdf(-1.0) == 0.0
    assert weibull.cdf(0.0) == 0.0

    # CDF debe ser monótona creciente
    x_vals = [0.5, 1.0, 1.5, 2.0, 3.0]
    cdf_vals = [weibull.cdf(x) for x in x_vals]
    for i in range(len(cdf_vals)-1):
        assert cdf_vals[i] <= cdf_vals[i+1], "CDF debe ser monótona creciente"

    # CDF debe tender a 1 para valores grandes
    assert weibull.cdf(100) > 0.999

def test_supervivencia_vs_cdf():
    """Test de relación entre función de supervivencia y CDF"""
    weibull = DistribucionWeibull(k=1.5, lambda_param=2.0)

    x_vals = [0.1, 0.5, 1.0, 2.0, 5.0]
    for x in x_vals:
        supervivencia = weibull.survival_function(x)
        cdf = weibull.cdf(x)
        diferencia = abs(supervivencia + cdf - 1.0)
        assert diferencia < 1e-10, f"S(x) + F(x) debe ser 1, diferencia = {diferencia}"

def test_caso_exponencial():
    """Test del caso especial k=1 (distribución exponencial)"""
    weibull = DistribucionWeibull(k=1.0, lambda_param=2.0)
    exponencial = stats.expon(scale=2.0)

    x_vals = [0.1, 0.5, 1.0, 2.0, 5.0]
    for x in x_vals:
        pdf_weibull = weibull.pdf(x)
        pdf_exponencial = exponencial.pdf(x) # type: ignore
        assert abs(pdf_weibull - pdf_exponencial) < 1e-10, \
            f"PDF no coincide en x={x}: Weibull={pdf_weibull}, Exp={pdf_exponencial}"

        cdf_weibull = weibull.cdf(x)
        cdf_exponencial = exponencial.cdf(x)
        assert abs(cdf_weibull - cdf_exponencial) < 1e-10, \
            f"CDF no coincide en x={x}: Weibull={cdf_weibull}, Exp={cdf_exponencial}"

def test_caso_rayleigh():
    """Test del caso especial k=2 (distribución de Rayleigh)"""
    # Para Rayleigh: σ = λ/√2, entonces λ = σ√2
    sigma = 1.0
    lambda_param = sigma * np.sqrt(2)

    weibull = DistribucionWeibull(k=2.0, lambda_param=lambda_param)
    rayleigh = stats.rayleigh(scale=sigma)

    x_vals = [0.1, 0.5, 1.0, 2.0]
    for x in x_vals:
        pdf_weibull = weibull.pdf(x)
        pdf_rayleigh = rayleigh.pdf(x) # type: ignore
        assert abs(pdf_weibull - pdf_rayleigh) < 1e-8, \
            f"PDF no coincide en x={x}: Weibull={pdf_weibull}, Rayleigh={pdf_rayleigh}"

def test_estadisticas():
    """Test de estadísticas calculadas"""
    weibull = DistribucionWeibull(k=2.0, lambda_param=1.0)

    # Media teórica: λ * Γ(1 + 1/k)
    media_teorica = 1.0 * gamma(1 + 1/2.0)  # Γ(1.5) = √π/2 ≈ 0.8862
    media_calculada = weibull.media()
    assert abs(media_teorica - media_calculada) < 1e-10, \
        f"Media incorrecta: teórica={media_teorica}, calculada={media_calculada}"

    # Para k=2, la media debe ser λ * Γ(1.5) ≈ 0.8862
    assert abs(media_calculada - gamma(1.5)) < 1e-10

    # Varianza
    gamma1 = gamma(1 + 1/2.0)
    gamma2 = gamma(1 + 2/2.0)  # Γ(2) = 1
    varianza_teorica = 1.0**2 * (gamma2 - gamma1**2)
    varianza_calculada = weibull.varianza()
    assert abs(varianza_teorica - varianza_calculada) < 1e-10, \
        f"Varianza incorrecta: teórica={varianza_teorica}, calculada={varianza_calculada}"

def test_percentiles():
    """Test de cálculo de percentiles"""
    weibull = DistribucionWeibull(k=2.0, lambda_param=1.0)

    # Percentil 50% debe ser igual a la mediana
    percentil_50 = weibull.percentil(0.5)
    mediana = weibull.mediana()
    assert abs(percentil_50 - mediana) < 1e-10, \
        f"Percentil 50% no coincide con mediana: P50={percentil_50}, mediana={mediana}"

    # Verificar algunos percentiles conocidos
    # Para Weibull(2,1), mediana = ln(2)^(1/2) ≈ 0.8326
    mediana_teorica = np.power(np.log(2), 1/2.0)
    assert abs(mediana - mediana_teorica) < 1e-10

    # El percentil debe ser monótono
    percentiles = [weibull.percentil(p) for p in [0.1, 0.25, 0.5, 0.75, 0.9]]
    for i in range(len(percentiles)-1):
        assert percentiles[i] <= percentiles[i+1], "Percentiles deben ser monótonos"

def test_funcion_riesgo():
    """Test de la función de riesgo"""
    weibull = DistribucionWeibull(k=2.0, lambda_param=1.0)

    x_vals = [0.1, 0.5, 1.0, 2.0, 5.0]
    for x in x_vals:
        # h(x) = f(x) / S(x)
        pdf = weibull.pdf(x)
        supervivencia = weibull.survival_function(x)
        riesgo_esperado = pdf / supervivencia if supervivencia > 0 else 0
        riesgo_calculado = weibull.hazard_function(x)

        if supervivencia > 1e-10:  # Evitar problemas numéricos
            assert abs(riesgo_esperado - riesgo_calculado) < 1e-8, \
                f"Función de riesgo incorrecta en x={x}: esperado={riesgo_esperado}, calculado={riesgo_calculado}"

    # Para k=2, h(x) = 2x (función lineal creciente)
    x = 1.0
    riesgo_teorico = 2 * x  # h(x) = (k/λ) * (x/λ)^(k-1) = 2 * x para k=2, λ=1
    riesgo_calculado = weibull.hazard_function(x)
    assert abs(riesgo_teorico - riesgo_calculado) < 1e-10

def test_generacion_muestras():
    """Test de generación de muestras aleatorias"""
    weibull = DistribucionWeibull(k=2.0, lambda_param=1.0)

    # Generar muestras grandes para verificar convergencia
    n = 10000
    muestras = weibull.generar_muestras(n, random_state=42)

    # Verificar que todas las muestras son no negativas
    assert np.all(muestras >= 0), "Todas las muestras deben ser no negativas"

    # Verificar convergencia de estadísticas
    media_muestral = np.mean(muestras)
    media_teorica = weibull.media()
    error_relativo = abs(media_muestral - media_teorica) / media_teorica
    assert error_relativo < 0.05, \
        f"Media muestral muy diferente de la teórica: muestral={media_muestral:.4f}, teórica={media_teorica:.4f}"

    # Verificar desviación estándar
    std_muestral = np.std(muestras, ddof=1)
    std_teorica = weibull.desviacion_estandar()
    error_relativo_std = abs(std_muestral - std_teorica) / std_teorica
    assert error_relativo_std < 0.1, \
        f"Desv. std. muestral muy diferente de la teórica: muestral={std_muestral:.4f}, teórica={std_teorica:.4f}"

def test_reproducibilidad():
    """Test de reproducibilidad con random_state"""
    weibull = DistribucionWeibull(k=1.5, lambda_param=2.0)

    # Generar muestras con la misma semilla
    muestras1 = weibull.generar_muestras(100, random_state=42)
    muestras2 = weibull.generar_muestras(100, random_state=42)

    # Deben ser idénticas
    assert np.array_equal(muestras1, muestras2), "Las muestras con misma semilla deben ser idénticas"

    # Con diferentes semillas deben ser diferentes
    muestras3 = weibull.generar_muestras(100, random_state=123)
    assert not np.array_equal(muestras1, muestras3), "Las muestras con diferentes semillas deben ser diferentes"

def test_casos_limite():
    """Test de casos límite y valores extremos"""
    weibull = DistribucionWeibull(k=0.1, lambda_param=1.0)  # k muy pequeño

    # PDF debe manejar k muy pequeño
    pdf_val = weibull.pdf(0.5)
    assert not np.isnan(pdf_val) and not np.isinf(pdf_val), "PDF debe ser finita para k pequeño"

    # k muy grande
    weibull_grande = DistribucionWeibull(k=10.0, lambda_param=1.0)
    pdf_grande = weibull_grande.pdf(1.0)
    assert not np.isnan(pdf_grande) and not np.isinf(pdf_grande), "PDF debe ser finita para k grande"

def run_all_tests():
    """Ejecutar todos los tests"""
    tests = [
        test_creacion_distribucion,
        test_pdf_propiedades,
        test_cdf_propiedades,
        test_supervivencia_vs_cdf,
        test_caso_exponencial,
        test_caso_rayleigh,
        test_estadisticas,
        test_percentiles,
        test_funcion_riesgo,
        test_generacion_muestras,
        test_reproducibilidad,
        test_casos_limite
    ]

    print("Ejecutando tests de la Distribución de Weibull...")
    print("=" * 60)

    tests_exitosos = 0
    tests_fallidos = 0

    for test_func in tests:
        try:
            test_func()
            print(f"✅ {test_func.__name__}: PASÓ")
            tests_exitosos += 1
        except Exception as e:
            print(f"❌ {test_func.__name__}: FALLÓ - {str(e)}")
            tests_fallidos += 1

    print("\n" + "=" * 60)
    print(f"Resumen: {tests_exitosos} tests exitosos, {tests_fallidos} tests fallidos")

    if tests_fallidos == 0:
        print("🎉 ¡Todos los tests pasaron exitosamente!")
    else:
        print(f"⚠️  Algunos tests fallaron. Revisar la implementación.")

    return tests_fallidos == 0

if __name__ == "__main__":
    success = run_all_tests()
    if not success:
        exit(1)
