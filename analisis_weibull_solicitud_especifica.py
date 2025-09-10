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
    
    def sustituir_funcion_densidad(self, resultado: Dict) -> None:
        """Sustituir parámetros en la función de densidad f(v) - Ecuación 1"""
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
        
        # Graficar función de densidad vs histograma
        velocidades = resultado['velocidades']
        v = np.linspace(0.1, np.max(velocidades) * 1.2, 1000)
        f_v = (k/c) * np.power(v/c, k-1) * np.exp(-np.power(v/c, k))
        
        plt.figure(figsize=(12, 8))
        plt.hist(velocidades, bins=40, density=True, alpha=0.6, color='lightblue',
                edgecolor='black', label='Datos observados')
        plt.plot(v, f_v, 'r-', linewidth=3, 
                label=f'f(v) Weibull (k={k:.3f}, c={c:.2f})')
        plt.xlabel('Velocidad del viento (m/s)')
        plt.ylabel('Densidad de probabilidad')
        plt.title(f'Función de Densidad de Weibull - {municipio}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
        
        print(f"✅ Función de densidad calculada y graficada")
    
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
        
        for municipio in [municipio_1, municipio_2]:
            resultado = self.calcular_parametros_weibull(municipio)
            self.sustituir_funcion_densidad(resultado)
        
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


def main():
    """Función principal"""
    analizador = AnalisisWeibullEspecifico("Datos.xlsx")
    analizador.ejecutar_analisis_completo()
    return analizador


if __name__ == "__main__":
    analizador = main()
