"""
Tests básicos para el Proyecto Weibull
======================================

Este archivo contiene pruebas unitarias para validar
las funciones del análisis de Weibull usando pytest.

Para ejecutar las pruebas:
pytest test_weibull_basico.py -v

Para ejecutar con cobertura:
pytest test_weibull_basico.py --cov=analisis_detallado_sustitucion -v
"""

import pytest
import numpy as np
import pandas as pd
from scipy.special import gamma
import sys
import os

# Agregar el directorio actual al path para importar nuestros módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar nuestras clases
from analisis_detallado_sustitucion import AnalisisDetalladoWeibull


class TestAnalisisWeibull:
    """Clase de pruebas para el análisis de Weibull"""
    
    @pytest.fixture
    def datos_muestra(self):
        """Crear datos de muestra para las pruebas"""
        np.random.seed(42)  # Para reproducibilidad
        
        # Generar datos sintéticos de velocidad del viento
        velocidades = np.random.weibull(2.5, 1000) * 10  # Escalar a m/s
        temperaturas = np.random.normal(25, 5, 1000)  # Temperaturas en °C
        
        # Crear DataFrame similar al real
        datos = pd.DataFrame({
            'vel_viento (m/s)': velocidades,
            'T (°C)': temperaturas,
            'Municipio': ['TestCity'] * 1000
        })
        
        return datos
    
    @pytest.fixture
    def analizador(self, datos_muestra, tmp_path):
        """Crear una instancia del analizador con datos de prueba"""
        # Crear archivo temporal Excel para testing
        archivo_test = tmp_path / "datos_test.xlsx"
        datos_muestra.to_excel(archivo_test, index=False)
        
        analizador = AnalisisDetalladoWeibull(str(archivo_test))
        analizador.datos = datos_muestra
        return analizador
    
    def test_carga_datos(self, analizador):
        """Probar que los datos se cargan correctamente"""
        assert not analizador.datos.empty
        assert 'vel_viento (m/s)' in analizador.datos.columns
        assert 'T (°C)' in analizador.datos.columns
        assert len(analizador.datos) > 0
    
    def test_calculo_estadisticas_basicas(self, datos_muestra):
        """Probar cálculo de estadísticas básicas"""
        velocidades = datos_muestra['vel_viento (m/s)'].values
        
        media = np.mean(velocidades)
        std = np.std(velocidades, ddof=1)
        cv = std / media
        
        # Verificar que los valores están en rangos razonables
        assert 0 < media < 50  # Velocidad media razonable
        assert 0 < std < media  # Desviación estándar positiva
        assert 0 < cv < 2  # Coeficiente de variación razonable
    
    def test_calculo_parametros_weibull(self, datos_muestra):
        """Probar cálculo de parámetros k y c de Weibull"""
        velocidades = datos_muestra['vel_viento (m/s)'].values
        
        # Calcular estadísticas
        v_promedio = float(np.mean(velocidades))
        sigma = float(np.std(velocidades, ddof=1))
        coef_variacion = sigma / v_promedio
        
        # Calcular parámetros Weibull
        k = np.power(coef_variacion, -1.09)
        gamma_val = gamma(1 + 1/k)
        c = v_promedio / gamma_val
        
        # Verificaciones
        assert k > 0, "Parámetro k debe ser positivo"
        assert c > 0, "Parámetro c debe ser positivo"
        assert 0.5 < k < 10, f"Parámetro k fuera de rango esperado: {k}"
        assert 0 < c < 100, f"Parámetro c fuera de rango esperado: {c}"
        
        # Verificar consistencia matemática
        v_teorica = c * gamma(1 + 1/k)
        error_relativo = abs(v_teorica - v_promedio) / v_promedio
        assert error_relativo < 0.01, f"Error en verificación matemática: {error_relativo*100:.4f}%"
    
    def test_funcion_densidad_weibull(self, datos_muestra):
        """Probar evaluación de la función de densidad"""
        velocidades = datos_muestra['vel_viento (m/s)'].values
        
        # Calcular parámetros
        v_promedio = float(np.mean(velocidades))
        sigma = float(np.std(velocidades, ddof=1))
        coef_variacion = sigma / v_promedio
        
        k = np.power(coef_variacion, -1.09)
        c = v_promedio / gamma(1 + 1/k)
        
        # Evaluar función de densidad en varios puntos
        v_test = np.array([1, 5, 10, 15, 20])
        
        for v in v_test:
            if v > 0:
                f_v = (k/c) * np.power(v/c, k-1) * np.exp(-np.power(v/c, k))
                
                # Verificaciones
                assert f_v >= 0, f"Densidad negativa en v={v}: {f_v}"
                assert not np.isnan(f_v), f"Densidad NaN en v={v}"
                assert not np.isinf(f_v), f"Densidad infinita en v={v}"
    
    def test_coeficientes_variacion(self, datos_muestra):
        """Probar cálculo de coeficientes de variación"""
        vel_cv = datos_muestra['vel_viento (m/s)'].std() / datos_muestra['vel_viento (m/s)'].mean()
        temp_cv = datos_muestra['T (°C)'].std() / datos_muestra['T (°C)'].mean()
        
        # Verificar rangos razonables
        assert 0 < vel_cv < 2, f"CV velocidad fuera de rango: {vel_cv}"
        assert 0 < temp_cv < 1, f"CV temperatura fuera de rango: {temp_cv}"
    
    def test_validacion_entrada_datos(self):
        """Probar validación de datos de entrada"""
        # Datos inválidos
        datos_invalidos = pd.DataFrame({
            'vel_viento (m/s)': [-1, 0, 100],  # Valores problemáticos
            'T (°C)': [25, 30, 35],
            'Municipio': ['Test1', 'Test2', 'Test3']
        })
        
        # Verificar que no hay velocidades negativas después del filtrado
        velocidades_validas = datos_invalidos['vel_viento (m/s)'][datos_invalidos['vel_viento (m/s)'] > 0]
        assert all(velocidades_validas > 0)
    
    def test_propiedades_matematicas_weibull(self):
        """Probar propiedades matemáticas conocidas de Weibull"""
        # Parámetros conocidos
        k = 2.0  # Weibull → Rayleigh
        c = 10.0
        
        # Media teórica usando gamma
        media_teorica = c * gamma(1 + 1/k)
        
        # Para k=2, gamma(1.5) = 0.5 * sqrt(π) ≈ 0.88623
        gamma_esperado = 0.5 * np.sqrt(np.pi)
        media_esperada = c * gamma_esperado
        
        error = abs(media_teorica - media_esperada) / media_esperada
        assert error < 0.01, f"Error en propiedad matemática de Weibull k=2: {error}"
        
        # Verificar que la media está en el rango correcto
        assert 8 < media_teorica < 12, f"Media fuera de rango esperado: {media_teorica}"


class TestIntegracionCompleta:
    """Pruebas de integración para el flujo completo"""
    
    @pytest.mark.slow
    def test_flujo_completo_con_datos_reales(self):
        """Probar flujo completo con datos reales (si están disponibles)"""
        archivo_datos = "Datos.xlsx"
        
        if os.path.exists(archivo_datos):
            analizador = AnalisisDetalladoWeibull(archivo_datos)
            analizador.cargar_datos_completos()
            
            # Verificar carga de datos
            assert not analizador.datos.empty
            assert len(analizador.datos) > 1000  # Debe tener suficientes datos
            
            # Verificar columnas necesarias
            columnas_requeridas = ['vel_viento (m/s)', 'T (°C)', 'Municipio']
            for columna in columnas_requeridas:
                assert columna in analizador.datos.columns
        else:
            pytest.skip("Archivo de datos reales no disponible")


def test_instalacion_pytest():
    """Verificar que pytest está correctamente instalado"""
    assert pytest.__version__ is not None
    print(f"pytest versión: {pytest.__version__}")


def test_dependencias_proyecto():
    """Verificar que todas las dependencias están instaladas"""
    try:
        import pandas
        import numpy
        import scipy
        import matplotlib
        import seaborn
        import openpyxl
        
        print("✅ Todas las dependencias están instaladas:")
        print(f"  pandas: {pandas.__version__}")
        print(f"  numpy: {numpy.__version__}")
        print(f"  scipy: {scipy.__version__}")
        print(f"  matplotlib: {matplotlib.__version__}")
        
    except ImportError as e:
        pytest.fail(f"Dependencia faltante: {e}")


if __name__ == "__main__":
    # Permitir ejecutar las pruebas directamente
    pytest.main([__file__, "-v"])
