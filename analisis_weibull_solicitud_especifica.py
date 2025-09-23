"""
Análisis de Weibull - Versión Específica para Solicitud
=======================================================

Este script responde exactamente a las dos solicitudes específicas:

1) Seleccionar 2 municipios y realizar histogramas de velocidad del viento 
   y temperatura, analizar variabilidad con coeficiente de variación, 
   y comparar con diagramas de caja y bigotes.

2) Calcular parámetros k y c usando ecuaciones 3 y 4, y sustituir en 
   la función de densidad f(v) (ecuación 1).

Autor: Proyecto Probabilidades
Fecha: 9 de septiembre de 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import seaborn as sns
from typing import Tuple, Dict

# Configurar estilo de gráficas
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class AnalisisWeibullEspecifico:
    """Análisis específico para las solicitudes planteadas"""
    
    def __init__(self, archivo_excel: str = "Datos.xlsx"):
        """Inicializar con archivo de datos"""
        self.archivo_excel = archivo_excel
        self.datos = pd.DataFrame()
        self.municipios_seleccionados = []
        self.resultados = {}
        
    def cargar_datos(self) -> None:
        """Cargar datos desde Excel"""
        print("🌪️ ANÁLISIS DE WEIBULL - SOLICITUD ESPECÍFICA")
        print("=" * 55)
        print("📁 Cargando datos meteorológicos...")
        
        self.datos = pd.read_excel(self.archivo_excel)
        print(f"✅ Datos cargados: {self.datos.shape[0]:,} registros")
        print(f"📍 Municipios disponibles: {sorted(self.datos['Municipio'].unique())}")
        
    def seleccionar_municipios(self) -> Tuple[str, str]:
        """Seleccionar 2 municipios para el análisis"""
        print(f"\n🎯 SELECCIÓN DE MUNICIPIOS PARA ANÁLISIS")
        print("=" * 45)
        
        municipios_disponibles = []
        for municipio in sorted(self.datos['Municipio'].unique()):
            datos_mun = self.datos[self.datos['Municipio'] == municipio]
            if len(datos_mun) > 100:
                municipios_disponibles.append(municipio)
        
        print(f"📋 MUNICIPIOS DISPONIBLES:")
        for i, municipio in enumerate(municipios_disponibles, 1):
            datos_mun = self.datos[self.datos['Municipio'] == municipio]
            vel_media = datos_mun['vel_viento (m/s)'].mean()
            print(f"   {i:2d}. {municipio:<12} (Vel.Media: {vel_media:5.2f} m/s)")
        
        print(f"\n🎯 MUNICIPIOS SELECCIONADOS:")
        municipio_1 = "Riohacha"    # Municipio costero norte
        municipio_2 = "Cartagena"   # Municipio costero centro
        
        print(f"   1️⃣ {municipio_1}")
        print(f"   2️⃣ {municipio_2}")
        
        self.municipios_seleccionados = [municipio_1, municipio_2]
        return municipio_1, municipio_2
    
    def generar_histogramas(self, municipio_1: str, municipio_2: str) -> None:
        """
        SOLICITUD 1: Generar histogramas de velocidad del viento y temperatura
        para cada municipio seleccionado
        """
        print(f"\n📊 SOLICITUD 1: HISTOGRAMAS Y ANÁLISIS DE VARIABILIDAD")
        print("=" * 60)
        
        # Extraer datos
        datos_mun1 = self.datos[self.datos['Municipio'] == municipio_1]
        datos_mun2 = self.datos[self.datos['Municipio'] == municipio_2]
        
        print(f"🔍 Datos extraídos:")
        print(f"   {municipio_1}: {len(datos_mun1):,} registros")
        print(f"   {municipio_2}: {len(datos_mun2):,} registros")
        
        # Crear histogramas (2x2)
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Histograma 1: Velocidad del viento - Municipio 1
        vel_1 = datos_mun1['vel_viento (m/s)']
        ax1.hist(vel_1, bins=30, alpha=0.7, color='blue', edgecolor='black', density=True)
        ax1.set_title(f'Velocidad del Viento - {municipio_1}', fontweight='bold')
        ax1.set_xlabel('Velocidad del viento (m/s)')
        ax1.set_ylabel('Densidad')
        ax1.grid(True, alpha=0.3)
        
        vel_mean_1 = vel_1.mean()
        vel_std_1 = vel_1.std()
        vel_cv_1 = vel_std_1 / vel_mean_1
        
        ax1.axvline(vel_mean_1, color='red', linestyle='--', linewidth=2)
        ax1.text(0.05, 0.95, f'Media: {vel_mean_1:.2f} m/s\nDesv.Est: {vel_std_1:.2f}\nCV: {vel_cv_1:.3f}',
                transform=ax1.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # Histograma 2: Velocidad del viento - Municipio 2
        vel_2 = datos_mun2['vel_viento (m/s)']
        ax2.hist(vel_2, bins=30, alpha=0.7, color='red', edgecolor='black', density=True)
        ax2.set_title(f'Velocidad del Viento - {municipio_2}', fontweight='bold')
        ax2.set_xlabel('Velocidad del viento (m/s)')
        ax2.set_ylabel('Densidad')
        ax2.grid(True, alpha=0.3)
        
        vel_mean_2 = vel_2.mean()
        vel_std_2 = vel_2.std()
        vel_cv_2 = vel_std_2 / vel_mean_2
        
        ax2.axvline(vel_mean_2, color='blue', linestyle='--', linewidth=2)
        ax2.text(0.05, 0.95, f'Media: {vel_mean_2:.2f} m/s\nDesv.Est: {vel_std_2:.2f}\nCV: {vel_cv_2:.3f}',
                transform=ax2.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
        
        # Histograma 3: Temperatura - Municipio 1
        temp_1 = datos_mun1['T (°C)']
        ax3.hist(temp_1, bins=30, alpha=0.7, color='green', edgecolor='black', density=True)
        ax3.set_title(f'Temperatura - {municipio_1}', fontweight='bold')
        ax3.set_xlabel('Temperatura (°C)')
        ax3.set_ylabel('Densidad')
        ax3.grid(True, alpha=0.3)
        
        temp_mean_1 = temp_1.mean()
        temp_std_1 = temp_1.std()
        temp_cv_1 = temp_std_1 / temp_mean_1
        
        ax3.axvline(temp_mean_1, color='red', linestyle='--', linewidth=2)
        ax3.text(0.05, 0.95, f'Media: {temp_mean_1:.1f} °C\nDesv.Est: {temp_std_1:.1f}\nCV: {temp_cv_1:.3f}',
                transform=ax3.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        
        # Histograma 4: Temperatura - Municipio 2
        temp_2 = datos_mun2['T (°C)']
        ax4.hist(temp_2, bins=30, alpha=0.7, color='orange', edgecolor='black', density=True)
        ax4.set_title(f'Temperatura - {municipio_2}', fontweight='bold')
        ax4.set_xlabel('Temperatura (°C)')
        ax4.set_ylabel('Densidad')
        ax4.grid(True, alpha=0.3)
        
        temp_mean_2 = temp_2.mean()
        temp_std_2 = temp_2.std()
        temp_cv_2 = temp_std_2 / temp_mean_2
        
        ax4.axvline(temp_mean_2, color='blue', linestyle='--', linewidth=2)
        ax4.text(0.05, 0.95, f'Media: {temp_mean_2:.1f} °C\nDesv.Est: {temp_std_2:.1f}\nCV: {temp_cv_2:.3f}',
                transform=ax4.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.suptitle(f'HISTOGRAMAS - {municipio_1} vs {municipio_2}', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        # Guardar resultados para análisis posterior
        self.resultados[municipio_1] = {
            'datos': datos_mun1,
            'vel_mean': vel_mean_1, 'vel_std': vel_std_1, 'vel_cv': vel_cv_1,
            'temp_mean': temp_mean_1, 'temp_std': temp_std_1, 'temp_cv': temp_cv_1
        }
        
        self.resultados[municipio_2] = {
            'datos': datos_mun2,
            'vel_mean': vel_mean_2, 'vel_std': vel_std_2, 'vel_cv': vel_cv_2,
            'temp_mean': temp_mean_2, 'temp_std': temp_std_2, 'temp_cv': temp_cv_2
        }
        
        print(f"✅ Histogramas generados para ambos municipios")
        
    def analizar_variabilidad(self, municipio_1: str, municipio_2: str) -> str:
        """Analizar cuál ciudad presenta mayor variabilidad usando CV"""
        print(f"\n📈 ANÁLISIS DE VARIABILIDAD - COEFICIENTE DE VARIACIÓN")
        print("=" * 58)
        
        datos_1 = self.resultados[municipio_1]
        datos_2 = self.resultados[municipio_2]
        
        print(f"📊 COEFICIENTES DE VARIACIÓN:")
        print(f"{'Variable':<18} {municipio_1:<12} {municipio_2:<12} {'Mayor Variabilidad'}")
        print("-" * 65)
        
        # Velocidad del viento
        cv_vel_1 = datos_1['vel_cv']
        cv_vel_2 = datos_2['vel_cv']
        mayor_var_vel = municipio_1 if cv_vel_1 > cv_vel_2 else municipio_2
        
        print(f"{'Velocidad Viento':<18} {cv_vel_1:<12.3f} {cv_vel_2:<12.3f} {mayor_var_vel}")
        
        # Temperatura
        cv_temp_1 = datos_1['temp_cv']
        cv_temp_2 = datos_2['temp_cv']
        mayor_var_temp = municipio_1 if cv_temp_1 > cv_temp_2 else municipio_2
        
        print(f"{'Temperatura':<18} {cv_temp_1:<12.3f} {cv_temp_2:<12.3f} {mayor_var_temp}")
        
        # Variabilidad general
        cv_promedio_1 = (cv_vel_1 + cv_temp_1) / 2
        cv_promedio_2 = (cv_vel_2 + cv_temp_2) / 2
        mayor_var_general = municipio_1 if cv_promedio_1 > cv_promedio_2 else municipio_2
        
        print(f"{'Promedio General':<18} {cv_promedio_1:<12.3f} {cv_promedio_2:<12.3f} {mayor_var_general}")
        
        print(f"\n🎯 RESPUESTA: {mayor_var_general.upper()} presenta MAYOR VARIABILIDAD")
        
        return mayor_var_general
        
    def generar_diagramas_caja_bigotes(self, municipio_1: str, municipio_2: str) -> None:
        """Generar diagramas de caja y bigotes para comparación"""
        print(f"\n📦 COMPARACIÓN CON DIAGRAMAS DE CAJA Y BIGOTES")
        print("=" * 50)
        
        datos_1 = self.resultados[municipio_1]['datos']
        datos_2 = self.resultados[municipio_2]['datos']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Boxplot velocidad del viento
        vel_data = [datos_1['vel_viento (m/s)'], datos_2['vel_viento (m/s)']]
        bp1 = ax1.boxplot(vel_data, tick_labels=[municipio_1, municipio_2], patch_artist=True)
        
        colors = ['lightblue', 'lightcoral']
        for patch, color in zip(bp1['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax1.set_title('Velocidades del Viento', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Velocidad (m/s)')
        ax1.grid(True, alpha=0.3)
        
        # Boxplot temperatura
        temp_data = [datos_1['T (°C)'], datos_2['T (°C)']]
        bp2 = ax2.boxplot(temp_data, tick_labels=[municipio_1, municipio_2], patch_artist=True)
        
        colors_temp = ['lightgreen', 'wheat']
        for patch, color in zip(bp2['boxes'], colors_temp):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax2.set_title('Temperaturas', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Temperatura (°C)')
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle(f'DIAGRAMAS DE CAJA Y BIGOTES - {municipio_1} vs {municipio_2}',
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        print(f"✅ Diagramas de caja y bigotes generados")
    
    def calcular_parametros_weibull(self, municipio: str) -> Dict:
        """
        SOLICITUD 2: Calcular parámetros k y c usando ecuaciones 3 y 4
        """
        print(f"\n🧮 SOLICITUD 2: CÁLCULO DE PARÁMETROS WEIBULL - {municipio.upper()}")
        print("=" * 65)
        
        # Extraer velocidades del viento
        velocidades = self.resultados[municipio]['datos']['vel_viento (m/s)'].values
        
        # Estadísticas básicas
        v_promedio = float(np.mean(velocidades))
        sigma = float(np.std(velocidades, ddof=1))
        coef_variacion = sigma / v_promedio
        
        print(f"📊 ESTADÍSTICAS BÁSICAS:")
        print(f"   • Velocidad promedio (v̅): {v_promedio:.4f} m/s")
        print(f"   • Desviación estándar (σ): {sigma:.4f} m/s")
        print(f"   • Coeficiente de variación (σ/v̅): {coef_variacion:.4f}")
        
        # ECUACIÓN 3: Cálculo del parámetro k
        print(f"\n🔢 ECUACIÓN 3: k = (σ/v̅)^(-1.09)")
        
        k = np.power(coef_variacion, -1.09)
        print(f"   ")
        print(f"   K = (σ/v̅)^(-1.09) = ({sigma:.4f}/{v_promedio:.4f})^(-1.09) = {k:.4f}")
        print(f"   ")
        print(f"   ✅ Parámetro de forma: k = {k:.4f}")
        
        # ECUACIÓN 4: Cálculo del parámetro c
        print(f"\n🔢 ECUACIÓN 4: c = v̅ / Γ(1+1/k)")
        gamma_arg = 1 + 1/k
        gamma_val = gamma(gamma_arg)
        
        c = v_promedio / gamma_val
        print(f"   ")
        print(f"   c = v̅/Γ(1+1/k) = {v_promedio:.4f}/Γ(1+1/{k:.4f})")
        print(f"     = {v_promedio:.4f}/{gamma_val:.4f} = {c:.4f}")
        print(f"   ")
        print(f"   ✅ Parámetro de escala: c = {c:.4f} m/s")
        
        # Verificación matemática
        v_teorica = c * gamma(1 + 1/k)
        error_relativo = abs(v_teorica - v_promedio) / v_promedio * 100
        
        print(f"\n✅ VERIFICACIÓN MATEMÁTICA:")
        print(f"   Media teórica: c × Γ(1+1/k) = {c:.4f} × {gamma(1 + 1/k):.6f} = {v_teorica:.4f} m/s")
        print(f"   Media observada: {v_promedio:.4f} m/s")
        print(f"   Error relativo: {error_relativo:.6f} %")
        
        return {
            'municipio': municipio,
            'k': k,
            'c': c,
            'v_promedio': v_promedio,
            'sigma': sigma,
            'velocidades': velocidades
        }
    
    def calcular_cuartiles_y_rango_intercuartilico(self, resultado: Dict) -> Dict:
        """
        ACTIVIDAD 5: Calcular Q1, Q3 y rango intercuartílico usando distribución Weibull
        """
        k = resultado['k']
        c = resultado['c']
        municipio = resultado['municipio']
        
        print(f"\n📊 ACTIVIDAD 5: CUARTILES Y RANGO INTERCUARTÍLICO - {municipio.upper()}")
        print("=" * 65)
        
        # Para distribución Weibull: F(v) = 1 - e^(-(v/c)^k)
        # Para percentil p: v_p = c × (-ln(1-p))^(1/k)
        
        print(f"📐 FÓRMULA PARA PERCENTILES WEIBULL:")
        print(f"   v_p = c × (-ln(1-p))^(1/k)")
        print(f"   Donde: k = {k:.4f}, c = {c:.4f} m/s")
        print(f"")
        
        # Cuartil 1 (percentil 25)
        p1 = 0.25
        ln_term_1 = -np.log(1 - p1)
        exp_term_1 = 1/k
        power_result_1 = np.power(ln_term_1, exp_term_1)
        Q1 = c * power_result_1
        
        print(f"� CÁLCULO DEL CUARTIL 1 (Q1 - percentil 25%):")
        print(f"   Q1 = c × (-ln(1-p))^(1/k)")
        print(f"   Q1 = {c:.4f} × (-ln(1-0.25))^(1/{k:.4f})")
        print(f"   Q1 = {c:.4f} × (-ln(0.75))^({exp_term_1:.4f})")
        print(f"   Q1 = {c:.4f} × ({ln_term_1:.4f})^({exp_term_1:.4f})")
        print(f"   Q1 = {c:.4f} × {power_result_1:.4f}")
        print(f"   Q1 = {Q1:.4f} m/s")
        
        # Cuartil 3 (percentil 75)
        p3 = 0.75
        ln_term_3 = -np.log(1 - p3)
        exp_term_3 = 1/k
        power_result_3 = np.power(ln_term_3, exp_term_3)
        Q3 = c * power_result_3
        
        print(f"\n🔢 CÁLCULO DEL CUARTIL 3 (Q3 - percentil 75%):")
        print(f"   Q3 = c × (-ln(1-p))^(1/k)")
        print(f"   Q3 = {c:.4f} × (-ln(1-0.75))^(1/{k:.4f})")
        print(f"   Q3 = {c:.4f} × (-ln(0.25))^({exp_term_3:.4f})")
        print(f"   Q3 = {c:.4f} × ({ln_term_3:.4f})^({exp_term_3:.4f})")
        print(f"   Q3 = {c:.4f} × {power_result_3:.4f}")
        print(f"   Q3 = {Q3:.4f} m/s")
        
        # Rango intercuartílico
        IQR = Q3 - Q1
        
        print(f"\n📏 RANGO INTERCUARTÍLICO (IQR):")
        print(f"   IQR = Q3 - Q1")
        print(f"   IQR = {Q3:.4f} - {Q1:.4f}")
        print(f"   IQR = {IQR:.4f} m/s")
        
        print(f"\n📋 TABLA RESUMEN:")
        print(f"   +------------------+------------+")
        print(f"   | Estadístico      | Valor      |")
        print(f"   +------------------+------------+")
        print(f"   | Q1 (25%)         | {Q1:8.2f} m/s |")
        print(f"   | Q3 (75%)         | {Q3:8.2f} m/s |")
        print(f"   | IQR              | {IQR:8.2f} m/s |")
        print(f"   +------------------+------------+")
        print(f"   El 50% central de los datos está entre {Q1:.2f} y {Q3:.2f} m/s")
        
        return {
            'municipio': municipio,
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            'k': k,
            'c': c
        }
    
    def calcular_probabilidad_entre_cuartiles(self, resultado_cuartiles: Dict) -> None:
        """
        ACTIVIDAD 6: Calcular probabilidad entre Q1 y Q3 usando F(v)
        """
        municipio = resultado_cuartiles['municipio']
        Q1 = resultado_cuartiles['Q1']
        Q3 = resultado_cuartiles['Q3']
        k = resultado_cuartiles['k']
        c = resultado_cuartiles['c']
        
        print(f"\n📈 ACTIVIDAD 6: PROBABILIDAD ENTRE CUARTILES - {municipio.upper()}")
        print("=" * 60)
        
        # Función de distribución acumulada Weibull: F(v) = 1 - e^(-(v/c)^k)
        print(f"📐 FUNCIÓN DE DISTRIBUCIÓN ACUMULADA WEIBULL:")
        print(f"   F(v) = 1 - e^(-(v/c)^k)")
        print(f"   Donde: k = {k:.4f}, c = {c:.4f} m/s")
        print(f"")
        
        # Cálculo paso a paso para F(Q1)
        ratio_Q1 = Q1/c
        power_Q1 = np.power(ratio_Q1, k)
        exp_Q1 = np.exp(-power_Q1)
        F_Q1 = 1 - exp_Q1
        
        print(f"🔢 CÁLCULO PASO A PASO DE F(Q1):")
        print(f"   F(Q1) = F({Q1:.4f}) = 1 - e^(-({Q1:.4f}/{c:.4f})^{k:.4f})")
        print(f"   ")
        print(f"   Paso 1: (v/c) = {Q1:.4f}/{c:.4f} = {ratio_Q1:.4f}")
        print(f"   Paso 2: (v/c)^k = ({ratio_Q1:.4f})^{k:.4f} = {power_Q1:.4f}")
        print(f"   Paso 3: e^(-(v/c)^k) = e^(-{power_Q1:.4f}) = {exp_Q1:.4f}")
        print(f"   Paso 4: F(Q1) = 1 - {exp_Q1:.4f} = {F_Q1:.4f}")
        
        # Cálculo paso a paso para F(Q3)
        ratio_Q3 = Q3/c
        power_Q3 = np.power(ratio_Q3, k)
        exp_Q3 = np.exp(-power_Q3)
        F_Q3 = 1 - exp_Q3
        
        print(f"\n🔢 CÁLCULO PASO A PASO DE F(Q3):")
        print(f"   F(Q3) = F({Q3:.4f}) = 1 - e^(-({Q3:.4f}/{c:.4f})^{k:.4f})")
        print(f"   ")
        print(f"   Paso 1: (v/c) = {Q3:.4f}/{c:.4f} = {ratio_Q3:.4f}")
        print(f"   Paso 2: (v/c)^k = ({ratio_Q3:.4f})^{k:.4f} = {power_Q3:.4f}")
        print(f"   Paso 3: e^(-(v/c)^k) = e^(-{power_Q3:.4f}) = {exp_Q3:.4f}")
        print(f"   Paso 4: F(Q3) = 1 - {exp_Q3:.4f} = {F_Q3:.4f}")
        
        # Probabilidad entre Q1 y Q3
        prob_entre_cuartiles = F_Q3 - F_Q1
        porcentaje = prob_entre_cuartiles * 100
        
        print(f"\n🎯 CÁLCULO FINAL DE LA PROBABILIDAD:")
        print(f"   P(Q1 ≤ V ≤ Q3) = F(Q3) - F(Q1)")
        print(f"   P({Q1:.2f} ≤ V ≤ {Q3:.2f}) = {F_Q3:.4f} - {F_Q1:.4f}")
        print(f"   P({Q1:.2f} ≤ V ≤ {Q3:.2f}) = {prob_entre_cuartiles:.4f}")
        print(f"   P({Q1:.2f} ≤ V ≤ {Q3:.2f}) = {porcentaje:.2f}%")
        
        print(f"\n📋 TABLA RESUMEN DE PROBABILIDADES:")
        print(f"   +------------------+------------+")
        print(f"   | Función          | Valor      |")
        print(f"   +------------------+------------+")
        print(f"   | F(Q1)            | {F_Q1:8.4f}   |")
        print(f"   | F(Q3)            | {F_Q3:8.4f}   |")
        print(f"   | P(Q1≤V≤Q3)       | {prob_entre_cuartiles:8.4f}   |")
        print(f"   | Porcentaje       | {porcentaje:8.2f}%  |")
        print(f"   +------------------+------------+")
        
        print(f"\n✅ INTERPRETACIÓN:")
        print(f"   La probabilidad de que la velocidad del viento esté entre")
        print(f"   {Q1:.2f} m/s y {Q3:.2f} m/s es del {porcentaje:.2f}%")
        print(f"   (Esto corresponde al 50% central de la distribución)")
    
    def calcular_probabilidad_superior_percentil60(self, resultado: Dict) -> None:
        """
        ACTIVIDAD 7: Calcular probabilidad de velocidades superiores al percentil 60
        """
        k = resultado['k']
        c = resultado['c']
        municipio = resultado['municipio']
        
        print(f"\n⚡ ACTIVIDAD 7: PROBABILIDAD SUPERIOR AL PERCENTIL 60 - {municipio.upper()}")
        print("=" * 70)
        
        # Calcular percentil 60 paso a paso
        p60 = 0.60
        ln_term = -np.log(1 - p60)
        exp_term = 1/k
        power_result = np.power(ln_term, exp_term)
        percentil_60 = c * power_result
        
        print(f"📐 CÁLCULO PASO A PASO DEL PERCENTIL 60:")
        print(f"   v_60 = c × (-ln(1-p))^(1/k)")
        print(f"   Donde: p = 0.60, k = {k:.4f}, c = {c:.4f} m/s")
        print(f"   ")
        print(f"   Paso 1: (1-p) = 1-0.60 = 0.40")
        print(f"   Paso 2: -ln(1-p) = -ln(0.40) = {ln_term:.4f}")
        print(f"   Paso 3: 1/k = 1/{k:.4f} = {exp_term:.4f}")
        print(f"   Paso 4: (-ln(1-p))^(1/k) = ({ln_term:.4f})^({exp_term:.4f}) = {power_result:.4f}")
        print(f"   Paso 5: v_60 = {c:.4f} × {power_result:.4f} = {percentil_60:.4f} m/s")
        
        # Calcular F(percentil_60) paso a paso
        ratio_p60 = percentil_60/c
        power_p60 = np.power(ratio_p60, k)
        exp_p60 = np.exp(-power_p60)
        F_p60 = 1 - exp_p60
        
        print(f"\n📈 CÁLCULO PASO A PASO DE F(v_60):")
        print(f"   F(v_60) = F({percentil_60:.4f}) = 1 - e^(-({percentil_60:.4f}/{c:.4f})^{k:.4f})")
        print(f"   ")
        print(f"   Paso 1: (v/c) = {percentil_60:.4f}/{c:.4f} = {ratio_p60:.4f}")
        print(f"   Paso 2: (v/c)^k = ({ratio_p60:.4f})^{k:.4f} = {power_p60:.4f}")
        print(f"   Paso 3: e^(-(v/c)^k) = e^(-{power_p60:.4f}) = {exp_p60:.4f}")
        print(f"   Paso 4: F(v_60) = 1 - {exp_p60:.4f} = {F_p60:.4f}")
        
        # Probabilidad de velocidades superiores al percentil 60
        prob_superior_p60 = 1 - F_p60
        porcentaje_superior = prob_superior_p60 * 100
        
        print(f"\n🎯 CÁLCULO DE LA PROBABILIDAD SUPERIOR:")
        print(f"   P(V > v_60) = 1 - F(v_60)")
        print(f"   P(V > {percentil_60:.4f}) = 1 - {F_p60:.4f}")
        print(f"   P(V > {percentil_60:.4f}) = {prob_superior_p60:.4f}")
        print(f"   P(V > {percentil_60:.4f}) = {porcentaje_superior:.2f}%")
        
        print(f"\n📋 TABLA RESUMEN:")
        print(f"   +------------------+------------+")
        print(f"   | Concepto         | Valor      |")
        print(f"   +------------------+------------+")
        print(f"   | Percentil 60     | {percentil_60:8.2f} m/s |")
        print(f"   | F(P60)           | {F_p60:8.4f}   |")
        print(f"   | P(V > P60)       | {prob_superior_p60:8.4f}   |")
        print(f"   | Porcentaje       | {porcentaje_superior:8.2f}%  |")
        print(f"   +------------------+------------+")
        
        print(f"\n✅ INTERPRETACIÓN:")
        print(f"   La probabilidad de registrar velocidades superiores a")
        print(f"   {percentil_60:.2f} m/s (percentil 60) es del {porcentaje_superior:.2f}%")
        print(f"   Esto significa que el {porcentaje_superior:.0f}% de las observaciones")
        print(f"   superan esta velocidad de referencia.")

    def calcular_velocidades_caracteristicas(self, resultado: Dict) -> Dict:
        """
        Calcular velocidades características usando ecuaciones 5 y 6:
        - Velocidad más probable (ec. 5)
        - Velocidad de máxima energía eólica (ec. 6)
        """
        k = resultado['k']
        c = resultado['c']
        municipio = resultado['municipio']
        
        print(f"\n⚡ VELOCIDADES CARACTERÍSTICAS - {municipio.upper()}")
        print("=" * 50)
        
        # ECUACIÓN 5: Velocidad más probable
        print(f"\n🎯 ECUACIÓN 5: v_mp = c × ((k-1)/k)^(1/k)")
        
        if k > 1:
            v_mp = c * np.power((k-1)/k, 1/k)
            print(f"   ")
            print(f"   v_mp = {c:.4f} × (({k:.4f}-1)/{k:.4f})^(1/{k:.4f})")
            print(f"   v_mp = {c:.4f} × ({k-1:.4f}/{k:.4f})^{1/k:.4f}")
            print(f"   v_mp = {v_mp:.4f} m/s")
        else:
            v_mp = 0
            print(f"   ⚠️ k ≤ 1: La velocidad más probable es 0 m/s")
            print(f"   (La función es monótona decreciente)")
        
        # ECUACIÓN 6: Velocidad de máxima energía
        print(f"\n⚡ ECUACIÓN 6: v_maxE = c × ((k+2)/k)^(1/k)")
        
        v_maxE = c * np.power((k+2)/k, 1/k)
        print(f"   ")
        print(f"   v_maxE = {c:.4f} × (({k:.4f}+2)/{k:.4f})^(1/{k:.4f})")
        print(f"   v_maxE = {c:.4f} × ({k+2:.4f}/{k:.4f})^{1/k:.4f}")
        print(f"   v_maxE = {v_maxE:.4f} m/s")
        
        # Análisis de resultados
        v_mean = resultado['v_promedio']
        print(f"\n📊 RESUMEN DE VELOCIDADES CARACTERÍSTICAS:")
        print(f"   • Velocidad media: {v_mean:.2f} m/s")
        print(f"   • Velocidad más probable: {v_mp:.2f} m/s")
        print(f"   • Velocidad de máxima energía: {v_maxE:.2f} m/s")
        
        return {
            'municipio': municipio,
            'v_media': v_mean,
            'v_probable': v_mp,
            'v_maxE': v_maxE
        }

    def sustituir_funcion_densidad(self, resultado: Dict) -> None:
        """
        Sustituir parámetros en la función de densidad f(v) - Ecuación 1 y analizar
        el comportamiento de la distribución
        """
        municipio = resultado['municipio']
        k = resultado['k']
        c = resultado['c']
        
        print(f"\n📈 SUSTITUCIÓN EN FUNCIÓN DE DENSIDAD f(v) - ECUACIÓN 1")
        print("=" * 58)
        print(f"📐 ECUACIÓN 1: f(v) = (k/c) × (v/c)^(k-1) × e^(-(v/c)^k)")
        print(f"")
        
        # Mostrar sustitución como en la imagen
        k_sobre_c = k / c
        k_menos_1 = k - 1
        
        print(f"   fᵥ = ({k:.4f}/{c:.4f}) × (v/{c:.4f})^{k:.4f}-1 × e^[-(v/{c:.4f})^{k:.4f}]")
        print(f"   ")
        print(f"   fᵥ = ({k_sobre_c:.4f}) × (v/{c:.4f})^{k_menos_1:.4f} × e^[-(v/{c:.4f})^{k:.4f}]")
        
        # Graficar función de densidad vs histograma con más detalles
        velocidades = resultado['velocidades']
        v_max = np.max(velocidades) * 1.2
        v = np.linspace(0.1, v_max, 1000)
        f_v = (k/c) * np.power(v/c, k-1) * np.exp(-np.power(v/c, k))
        
        # Configurar el estilo de la gráfica
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Graficar histograma normalizado
        n, bins, patches = ax.hist(velocidades, bins=40, density=True, alpha=0.6,
                                 color='skyblue', edgecolor='black',
                                 label='Datos observados')
        
        # Graficar función de densidad
        ax.plot(v, f_v, 'r-', linewidth=3, 
                label=f'Distribución Weibull\nk={k:.3f}, c={c:.2f} m/s')
        
        # Añadir líneas verticales para estadísticos importantes
        v_mean = np.mean(velocidades)
        v_median = np.median(velocidades)
        v_mode = c * np.power((k-1)/k, 1/k) if k > 1 else 0
        
        ax.axvline(v_mean, color='green', linestyle='--', alpha=0.8,
                  label=f'Media: {v_mean:.2f} m/s')
        ax.axvline(v_median, color='orange', linestyle='--', alpha=0.8,
                  label=f'Mediana: {v_median:.2f} m/s')
        ax.axvline(v_mode, color='purple', linestyle='--', alpha=0.8,
                  label=f'Moda: {v_mode:.2f} m/s')
        
        # Mejorar el aspecto visual
        ax.set_xlabel('Velocidad del viento (m/s)', fontsize=12)
        ax.set_ylabel('Densidad de probabilidad', fontsize=12)
        ax.set_title(f'Distribución de Weibull vs Datos Observados - {municipio}',
                    fontsize=14, pad=20, fontweight='bold')
        
        # Ajustar la leyenda
        ax.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=10)
        
        # Añadir cuadrícula
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Ajustar márgenes
        plt.tight_layout()
        plt.show()
        
        # Analizar el comportamiento
        print(f"\n📊 ANÁLISIS DEL COMPORTAMIENTO - {municipio.upper()}")
        print("=" * 50)
        print(f"1. Forma de la distribución:")
        if k < 1:
            print("   • Forma exponencial decreciente (k < 1)")
            print("   • Alta frecuencia de velocidades bajas")
        elif 1 < k < 2:
            print("   • Forma asimétrica positiva moderada (1 < k < 2)")
            print("   • Buena distribución de velocidades bajas y medias")
        elif 2 <= k < 3:
            print("   • Forma aproximadamente simétrica (2 ≤ k < 3)")
            print("   • Distribución balanceada de velocidades")
        else:
            print("   • Forma similar a la normal (k ≥ 3)")
            print("   • Concentración alrededor de la media")
        
        print(f"\n2. Estadísticos principales:")
        print(f"   • Media: {v_mean:.2f} m/s")
        print(f"   • Mediana: {v_median:.2f} m/s")
        print(f"   • Moda: {v_mode:.2f} m/s")
        
        print(f"\n3. Interpretación del ajuste:")
        # Calcular error cuadrático medio entre histograma y función
        hist_centers = (bins[:-1] + bins[1:]) / 2
        f_v_hist = (k/c) * np.power(hist_centers/c, k-1) * np.exp(-np.power(hist_centers/c, k))
        rmse = np.sqrt(np.mean((n - f_v_hist)**2))
        
        print(f"   • Error cuadrático medio: {rmse:.4f}")
        if rmse < 0.1:
            print("   • Excelente ajuste entre datos y modelo")
        elif rmse < 0.2:
            print("   • Buen ajuste entre datos y modelo")
        else:
            print("   • Ajuste moderado entre datos y modelo")
    
    def ejecutar_analisis_completo(self) -> None:
        """Ejecutar análisis completo respondiendo a las dos solicitudes específicas"""
        # Cargar datos
        self.cargar_datos()
        
        # Seleccionar municipios
        municipio_1, municipio_2 = self.seleccionar_municipios()
        
        # SOLICITUD 1: Histogramas y análisis de variabilidad
        self.generar_histogramas(municipio_1, municipio_2)
        municipio_mayor_variabilidad = self.analizar_variabilidad(municipio_1, municipio_2)
        self.generar_diagramas_caja_bigotes(municipio_1, municipio_2)
        
        # SOLICITUD 2: Parámetros Weibull para cada ciudad
        print(f"\n" + "="*70)
        print(f"SOLICITUD 2: CÁLCULO DE PARÁMETROS WEIBULL")
        print("="*70)
        
        resultados_weibull = {}
        velocidades_caracteristicas = {}
        
        for municipio in [municipio_1, municipio_2]:
            resultado = self.calcular_parametros_weibull(municipio)
            resultados_weibull[municipio] = resultado
            self.sustituir_funcion_densidad(resultado)
            velocidades_caracteristicas[municipio] = self.calcular_velocidades_caracteristicas(resultado)
        
        # SOLICITUD 3 y 4: Análisis comparativo del potencial eólico
        print(f"\n" + "="*70)
        print(f"ANÁLISIS COMPARATIVO DEL POTENCIAL EÓLICO")
        print("="*70)
        
        print(f"\n📊 TABLA COMPARATIVA DE VELOCIDADES CARACTERÍSTICAS")
        print("-" * 75)
        print(f"{'Municipio':<12} {'V. Media':<12} {'V. Probable':<12} {'V. Máx.Energía':<15} {'k':<8} {'c (m/s)'}")
        print("-" * 75)
        
        for municipio in [municipio_1, municipio_2]:
            v_caract = velocidades_caracteristicas[municipio]
            res_weibull = resultados_weibull[municipio]
            print(f"{municipio:<12} {v_caract['v_media']:<12.2f} "
                  f"{v_caract['v_probable']:<12.2f} {v_caract['v_maxE']:<15.2f} "
                  f"{res_weibull['k']:<8.2f} {res_weibull['c']:.2f}")
        
        print("\n🔍 ANÁLISIS DE POTENCIAL EÓLICO:")
        print("=" * 40)
        
        # Determinar ciudad con mayor potencial
        v_maxE_1 = velocidades_caracteristicas[municipio_1]['v_maxE']
        v_maxE_2 = velocidades_caracteristicas[municipio_2]['v_maxE']
        
        ciudad_mayor_potencial = municipio_1 if v_maxE_1 > v_maxE_2 else municipio_2
        diferencia_porcentual = abs(v_maxE_1 - v_maxE_2) / min(v_maxE_1, v_maxE_2) * 100
        
        print(f"1. Velocidades de máxima energía:")
        print(f"   • {municipio_1}: {v_maxE_1:.2f} m/s")
        print(f"   • {municipio_2}: {v_maxE_2:.2f} m/s")
        print(f"   • Diferencia porcentual: {diferencia_porcentual:.1f}%")
        
        print(f"\n2. Comparación de forma (k):")
        k1 = resultados_weibull[municipio_1]['k']
        k2 = resultados_weibull[municipio_2]['k']
        print(f"   • {municipio_1}: k = {k1:.2f}")
        print(f"   • {municipio_2}: k = {k2:.2f}")
        
        print(f"\n3. Conclusiones:")
        print(f"   • {ciudad_mayor_potencial.upper()} muestra mayor potencial eólico")
        print(f"   • Razones principales:")
        
        if ciudad_mayor_potencial == municipio_1:
            v_maxE = v_maxE_1
            k = k1
        else:
            v_maxE = v_maxE_2
            k = k2
            
        print(f"     - Mayor velocidad de máxima energía: {v_maxE:.2f} m/s")
        if k > 2:
            print(f"     - Distribución más estable (k = {k:.2f})")
            print(f"     - Menor variabilidad en las velocidades")
        elif 1.5 <= k <= 2:
            print(f"     - Distribución moderadamente variable (k = {k:.2f})")
            print(f"     - Balance entre estabilidad y rachas de viento")
        else:
            print(f"     - Alta variabilidad en velocidades (k = {k:.2f})")
            print(f"     - Requiere sistemas de control más robustos")
        
        # ACTIVIDADES 5, 6 y 7: Análisis estadístico adicional
        print(f"\n" + "="*70)
        print(f"ACTIVIDADES 5, 6 Y 7: ANÁLISIS ESTADÍSTICO ADICIONAL")
        print("="*70)
        
        resultados_cuartiles = {}
        
        for municipio in [municipio_1, municipio_2]:
            print(f"\n{'='*70}")
            print(f"ANÁLISIS PARA {municipio.upper()}")
            print("="*70)
            
            # Actividad 5: Cuartiles y rango intercuartílico
            resultado_cuartiles = self.calcular_cuartiles_y_rango_intercuartilico(resultados_weibull[municipio])
            resultados_cuartiles[municipio] = resultado_cuartiles
            
            # Actividad 6: Probabilidad entre cuartiles
            self.calcular_probabilidad_entre_cuartiles(resultado_cuartiles)
            
            # Actividad 7: Probabilidad superior al percentil 60
            self.calcular_probabilidad_superior_percentil60(resultados_weibull[municipio])
        
        # Comparación final de cuartiles entre ciudades
        print(f"\n" + "="*70)
        print(f"COMPARACIÓN FINAL DE CUARTILES ENTRE CIUDADES")
        print("="*70)
        
        print(f"\n📊 TABLA COMPARATIVA DE CUARTILES:")
        print("-" * 60)
        print(f"{'Municipio':<12} {'Q1 (m/s)':<12} {'Q3 (m/s)':<12} {'IQR (m/s)':<12}")
        print("-" * 60)
        
        for municipio in [municipio_1, municipio_2]:
            r_cuart = resultados_cuartiles[municipio]
            print(f"{municipio:<12} {r_cuart['Q1']:<12.2f} {r_cuart['Q3']:<12.2f} {r_cuart['IQR']:<12.2f}")
        
        print(f"\n🔍 INTERPRETACIÓN FINAL:")
        print(f"   • Rango intercuartílico más amplio indica mayor dispersión")
        print(f"   • Cuartiles más altos sugieren mejores condiciones eólicas")
        print(f"   • La probabilidad entre cuartiles es siempre 50% por definición")
        print(f"   • La probabilidad superior al percentil 60 es siempre 40% por definición")

        # Resumen final
        print(f"\n🎯 RESUMEN FINAL")
        print("=" * 30)
        print(f"✅ SOLICITUD 1 COMPLETADA:")
        print(f"   • Histogramas generados para {municipio_1} y {municipio_2}")
        print(f"   • Análisis de variabilidad: {municipio_mayor_variabilidad} presenta mayor variabilidad")
        print(f"   • Diagramas de caja y bigotes generados")
        print(f"")
        print(f"✅ SOLICITUD 2 COMPLETADA:")
        print(f"   • Parámetros k y c calculados usando ecuaciones 3 y 4")
        print(f"   • Valores sustituidos en función f(v) (ecuación 1)")
        print(f"   • Gráficas de funciones de densidad generadas")
        print(f"")
        print(f"✅ SOLICITUD 3 COMPLETADA:")
        print(f"   • Análisis detallado de la forma de las distribuciones")
        print(f"   • Comparación de ajuste entre datos y modelo")
        print(f"   • Interpretación del comportamiento de las variables")
        print(f"")
        print(f"✅ SOLICITUD 4 COMPLETADA:")
        print(f"   • Velocidades características calculadas (ec. 5 y 6)")
        print(f"   • Análisis comparativo del potencial eólico")
        print(f"   • {ciudad_mayor_potencial.upper()} identificada con mayor potencial")
        print(f"")
        print(f"✅ ACTIVIDAD 5 COMPLETADA:")
        print(f"   • Cuartiles Q1 y Q3 calculados para ambas ciudades")
        print(f"   • Rango intercuartílico determinado")
        print(f"")
        print(f"✅ ACTIVIDAD 6 COMPLETADA:")
        print(f"   • Probabilidad entre cuartiles calculada usando F(v)")
        print(f"   • Verificación teórica del 50% central")
        print(f"")
        print(f"✅ ACTIVIDAD 7 COMPLETADA:")
        print(f"   • Percentil 60 calculado para ambas ciudades")
        print(f"   • Probabilidad superior al percentil 60 determinada")


def main():
    """Función principal"""
    analizador = AnalisisWeibullEspecifico("Datos.xlsx")
    analizador.ejecutar_analisis_completo()
    return analizador


if __name__ == "__main__":
    analizador = main()
