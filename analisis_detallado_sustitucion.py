"""
Análisis Detallado de Weibull con Sustitución de Valores Paso a Paso
===================================================================

Este script realiza un análisis completo mostrando explícitamente las fases
de sustitución de valores en las ecuaciones de Weibull, incluyendo:

1) Selección de 2 municipios
2) Histogramas de velocidad del viento y temperatura
3) Análisis de variabilidad (coeficiente de variación) 
4) Comparación con diagramas de caja y bigotes
5) Cálculo paso a paso de parámetros k y c (ecuaciones 3 y 4)
6) Sustitución en la función de densidad f(v) (ecuación 1)

Autor: Proyecto Probabilidades
Fecha: 3 de septiembre de 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import seaborn as sns
from typing import Dict, Tuple

# Configurar estilo de gráficas
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class AnalisisDetalladoWeibull:
    """Análisis detallado con sustitución paso a paso de ecuaciones"""
    
    def __init__(self, archivo_excel: str = "Datos.xlsx"):
        """Inicializar con datos originales que incluyen temperatura"""
        self.archivo_excel = archivo_excel
        self.datos = pd.DataFrame()
        self.municipios_seleccionados = []
        self.resultados_municipios = {}
        
    def cargar_datos_completos(self) -> None:
        """Cargar datos completos incluyendo temperatura"""
        print("🌪️ ANÁLISIS DETALLADO DE WEIBULL - SUSTITUCIÓN PASO A PASO")
        print("=" * 70)
        print("📁 Cargando datos completos desde Excel...")
        
        self.datos = pd.read_excel(self.archivo_excel)
        
        print(f"✅ Datos cargados: {self.datos.shape[0]:,} registros")
        print(f"📊 Variables disponibles: {list(self.datos.columns)}")
        print(f"🏙️ Municipios disponibles: {sorted(self.datos['Municipio'].unique())}")
    
    def solicitar_municipios_usuario(self) -> Tuple[str, str]:
        """
        Solicitar al usuario que seleccione los dos municipios a comparar
        de forma interactiva
        
        Returns:
        --------
        Tuple[str, str]
            Nombres de los dos municipios seleccionados por el usuario
        """
        print(f"\n👤 SELECCIÓN INTERACTIVA DE MUNICIPIOS")
        print("=" * 50)
        
        # Obtener lista de municipios con suficientes datos
        municipios_disponibles = []
        
        for municipio in sorted(self.datos['Municipio'].unique()):
            datos_mun = self.datos[self.datos['Municipio'] == municipio]
            if len(datos_mun) > 100:  # Filtrar municipios con suficientes datos
                municipios_disponibles.append(municipio)
        
        print(f"📋 MUNICIPIOS DISPONIBLES PARA ANÁLISIS:")
        print("-" * 40)
        
        for i, municipio in enumerate(municipios_disponibles, 1):
            datos_mun = self.datos[self.datos['Municipio'] == municipio]
            vel_media = datos_mun['vel_viento (m/s)'].mean()
            n_datos = len(datos_mun)
            
            print(f"   {i:2d}. {municipio:<12} (Vel.Media: {vel_media:5.2f} m/s, Datos: {n_datos:,})")
        
        print(f"\n🎯 INSTRUCCIONES:")
        print(f"   • Selecciona 2 municipios diferentes para comparar")
        print(f"   • Ingresa el número correspondiente a cada municipio")
        print(f"   • Se recomienda comparar municipios con características contrastantes")
        
        # Solicitar primer municipio
        while True:
            try:
                print(f"\n1️⃣ Selecciona el PRIMER municipio:")
                opcion1 = input(f"   Ingresa el número (1-{len(municipios_disponibles)}): ").strip()
                indice1 = int(opcion1) - 1
                
                if 0 <= indice1 < len(municipios_disponibles):
                    municipio_1 = municipios_disponibles[indice1]
                    print(f"   ✅ Primer municipio seleccionado: {municipio_1}")
                    break
                else:
                    print(f"   ❌ Opción inválida. Ingresa un número entre 1 y {len(municipios_disponibles)}")
            except ValueError:
                print(f"   ❌ Por favor ingresa un número válido")
            except KeyboardInterrupt:
                print(f"\n\n⚠️ Operación cancelada por el usuario")
                print(f"🔄 Usando selección automática: Riohacha y Valledupar")
                return "Riohacha", "Valledupar"
        
        # Solicitar segundo municipio
        while True:
            try:
                print(f"\n2️⃣ Selecciona el SEGUNDO municipio (diferente al primero):")
                opcion2 = input(f"   Ingresa el número (1-{len(municipios_disponibles)}): ").strip()
                indice2 = int(opcion2) - 1
                
                if 0 <= indice2 < len(municipios_disponibles):
                    if indice2 != indice1:
                        municipio_2 = municipios_disponibles[indice2]
                        print(f"   ✅ Segundo municipio seleccionado: {municipio_2}")
                        break
                    else:
                        print(f"   ❌ No puedes seleccionar el mismo municipio dos veces")
                        print(f"       Ya seleccionaste: {municipio_1}")
                else:
                    print(f"   ❌ Opción inválida. Ingresa un número entre 1 y {len(municipios_disponibles)}")
            except ValueError:
                print(f"   ❌ Por favor ingresa un número válido")
            except KeyboardInterrupt:
                print(f"\n\n⚠️ Operación cancelada por el usuario")
                print(f"🔄 Usando selección automática: Riohacha y Valledupar")
                return "Riohacha", "Valledupar"
        
        # Mostrar selección final
        print(f"\n🎉 SELECCIÓN COMPLETADA:")
        print(f"   1️⃣ Primer municipio:  {municipio_1}")
        print(f"   2️⃣ Segundo municipio: {municipio_2}")
        
        # Mostrar estadísticas de comparación previa
        datos_1 = self.datos[self.datos['Municipio'] == municipio_1]
        datos_2 = self.datos[self.datos['Municipio'] == municipio_2]
        
        print(f"\n📊 COMPARACIÓN PREVIA:")
        print(f"   {municipio_1}:")
        print(f"      • Velocidad media: {datos_1['vel_viento (m/s)'].mean():.2f} m/s")
        print(f"      • Temperatura media: {datos_1['T (°C)'].mean():.1f} °C")
        print(f"      • Número de datos: {len(datos_1):,}")
        print(f"   {municipio_2}:")
        print(f"      • Velocidad media: {datos_2['vel_viento (m/s)'].mean():.2f} m/s")
        print(f"      • Temperatura media: {datos_2['T (°C)'].mean():.1f} °C")
        print(f"      • Número de datos: {len(datos_2):,}")
        
        self.municipios_seleccionados = [municipio_1, municipio_2]
        return municipio_1, municipio_2
        
    def seleccionar_municipios_contrastantes(self) -> Tuple[str, str]:
        """
        Seleccionar 2 municipios con características contrastantes
        para análisis comparativo
        
        Returns:
        --------
        Tuple[str, str]
            Nombres de los dos municipios seleccionados
        """
        print(f"\n🎯 FASE 1: SELECCIÓN DE MUNICIPIOS")
        print("=" * 50)
        
        # Calcular estadísticas básicas por municipio
        stats_municipios = []
        
        for municipio in sorted(self.datos['Municipio'].unique()):
            datos_mun = self.datos[self.datos['Municipio'] == municipio]
            
            if len(datos_mun) > 100:  # Filtrar municipios con suficientes datos
                stats = {
                    'municipio': municipio,
                    'n_datos': len(datos_mun),
                    'vel_media': datos_mun['vel_viento (m/s)'].mean(),
                    'vel_std': datos_mun['vel_viento (m/s)'].std(),
                    'vel_cv': datos_mun['vel_viento (m/s)'].std() / datos_mun['vel_viento (m/s)'].mean(),
                    'temp_media': datos_mun['T (°C)'].mean(),
                    'temp_std': datos_mun['T (°C)'].std(),
                    'temp_cv': datos_mun['T (°C)'].std() / datos_mun['T (°C)'].mean()
                }
                stats_municipios.append(stats)
        
        # Mostrar estadísticas para selección
        print("📊 Estadísticas por municipio:")
        print(f"{'Municipio':<12} {'N_Datos':<8} {'Vel_Media':<10} {'Vel_CV':<8} {'Temp_Media':<11} {'Temp_CV':<8}")
        print("-" * 65)
        
        for stats in stats_municipios:
            print(f"{stats['municipio']:<12} {stats['n_datos']:<8} {stats['vel_media']:<10.2f} "
                  f"{stats['vel_cv']:<8.3f} {stats['temp_media']:<11.1f} {stats['temp_cv']:<8.3f}")
        
        # Seleccionar municipios contrastantes
        # Criterio: uno con alta velocidad/baja variabilidad, otro con menor velocidad/alta variabilidad
        municipio_1 = "Riohacha"    # Alta velocidad, baja variabilidad
        municipio_2 = "Valledupar"  # Velocidad moderada, alta variabilidad
        
        self.municipios_seleccionados = [municipio_1, municipio_2]
        
        print(f"\n🎯 MUNICIPIOS SELECCIONADOS PARA ANÁLISIS COMPARATIVO:")
        print(f"   1️⃣ {municipio_1}: Representante de vientos costeros consistentes")
        print(f"   2️⃣ {municipio_2}: Representante de vientos interiores variables")
        
        return municipio_1, municipio_2
    
    def generar_histogramas_comparativos(self, municipio_1: str, municipio_2: str) -> None:
        """
        Generar histogramas de velocidad del viento y temperatura
        para ambos municipios
        """
        print(f"\n📊 FASE 2: HISTOGRAMAS COMPARATIVOS")
        print("=" * 50)
        
        # Extraer datos de ambos municipios
        datos_mun1 = self.datos[self.datos['Municipio'] == municipio_1]
        datos_mun2 = self.datos[self.datos['Municipio'] == municipio_2]
        
        # Crear figura con 4 subgráficas
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Histograma velocidad del viento - Municipio 1
        ax1.hist(datos_mun1['vel_viento (m/s)'], bins=30, alpha=0.7, color='blue', 
                edgecolor='black', density=True)
        ax1.set_title(f'Histograma Velocidad del Viento - {municipio_1}')
        ax1.set_xlabel('Velocidad del viento (m/s)')
        ax1.set_ylabel('Densidad')
        ax1.grid(True, alpha=0.3)
        
        # Agregar estadísticas
        vel_mean_1 = datos_mun1['vel_viento (m/s)'].mean()
        vel_std_1 = datos_mun1['vel_viento (m/s)'].std()
        vel_cv_1 = vel_std_1 / vel_mean_1
        
        ax1.axvline(vel_mean_1, color='red', linestyle='--', linewidth=2, label=f'Media = {vel_mean_1:.2f} m/s')
        ax1.text(0.05, 0.95, f'Media: {vel_mean_1:.2f} m/s\nDesv.Est: {vel_std_1:.2f} m/s\nCV: {vel_cv_1:.3f}',
                transform=ax1.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        ax1.legend()
        
        # 2. Histograma velocidad del viento - Municipio 2  
        ax2.hist(datos_mun2['vel_viento (m/s)'], bins=30, alpha=0.7, color='red',
                edgecolor='black', density=True)
        ax2.set_title(f'Histograma Velocidad del Viento - {municipio_2}')
        ax2.set_xlabel('Velocidad del viento (m/s)')
        ax2.set_ylabel('Densidad')
        ax2.grid(True, alpha=0.3)
        
        # Agregar estadísticas
        vel_mean_2 = datos_mun2['vel_viento (m/s)'].mean()
        vel_std_2 = datos_mun2['vel_viento (m/s)'].std()
        vel_cv_2 = vel_std_2 / vel_mean_2
        
        ax2.axvline(vel_mean_2, color='blue', linestyle='--', linewidth=2, label=f'Media = {vel_mean_2:.2f} m/s')
        ax2.text(0.05, 0.95, f'Media: {vel_mean_2:.2f} m/s\nDesv.Est: {vel_std_2:.2f} m/s\nCV: {vel_cv_2:.3f}',
                transform=ax2.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
        ax2.legend()
        
        # 3. Histograma temperatura - Municipio 1
        ax3.hist(datos_mun1['T (°C)'], bins=30, alpha=0.7, color='green',
                edgecolor='black', density=True)
        ax3.set_title(f'Histograma Temperatura - {municipio_1}')
        ax3.set_xlabel('Temperatura (°C)')
        ax3.set_ylabel('Densidad')
        ax3.grid(True, alpha=0.3)
        
        # Agregar estadísticas
        temp_mean_1 = datos_mun1['T (°C)'].mean()
        temp_std_1 = datos_mun1['T (°C)'].std()
        temp_cv_1 = temp_std_1 / temp_mean_1
        
        ax3.axvline(temp_mean_1, color='red', linestyle='--', linewidth=2, label=f'Media = {temp_mean_1:.1f} °C')
        ax3.text(0.05, 0.95, f'Media: {temp_mean_1:.1f} °C\nDesv.Est: {temp_std_1:.1f} °C\nCV: {temp_cv_1:.3f}',
                transform=ax3.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        ax3.legend()
        
        # 4. Histograma temperatura - Municipio 2
        ax4.hist(datos_mun2['T (°C)'], bins=30, alpha=0.7, color='orange',
                edgecolor='black', density=True)
        ax4.set_title(f'Histograma Temperatura - {municipio_2}')
        ax4.set_xlabel('Temperatura (°C)')
        ax4.set_ylabel('Densidad')
        ax4.grid(True, alpha=0.3)
        
        # Agregar estadísticas
        temp_mean_2 = datos_mun2['T (°C)'].mean()
        temp_std_2 = datos_mun2['T (°C)'].std()
        temp_cv_2 = temp_std_2 / temp_mean_2
        
        ax4.axvline(temp_mean_2, color='blue', linestyle='--', linewidth=2, label=f'Media = {temp_mean_2:.1f} °C')
        ax4.text(0.05, 0.95, f'Media: {temp_mean_2:.1f} °C\nDesv.Est: {temp_std_2:.1f} °C\nCV: {temp_cv_2:.3f}',
                transform=ax4.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        ax4.legend()
        
        plt.suptitle(f'Análisis Comparativo de Histogramas - {municipio_1} vs {municipio_2}',
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        # Guardar estadísticas para análisis posterior
        self.resultados_municipios[municipio_1] = {
            'datos': datos_mun1,
            'vel_mean': vel_mean_1,
            'vel_std': vel_std_1,
            'vel_cv': vel_cv_1,
            'temp_mean': temp_mean_1,
            'temp_std': temp_std_1,
            'temp_cv': temp_cv_1
        }
        
        self.resultados_municipios[municipio_2] = {
            'datos': datos_mun2,
            'vel_mean': vel_mean_2,
            'vel_std': vel_std_2,
            'vel_cv': vel_cv_2,
            'temp_mean': temp_mean_2,
            'temp_std': temp_std_2,
            'temp_cv': temp_cv_2
        }
        
        print(f"✅ Histogramas generados para {municipio_1} y {municipio_2}")
    
    def analizar_variabilidad_comparativa(self, municipio_1: str, municipio_2: str) -> str:
        """
        Analizar y comparar la variabilidad entre municipios usando 
        coeficientes de variación
        """
        print(f"\n📈 FASE 3: ANÁLISIS DE VARIABILIDAD")
        print("=" * 50)
        
        datos_1 = self.resultados_municipios[municipio_1]
        datos_2 = self.resultados_municipios[municipio_2]
        
        print(f"🔍 COEFICIENTES DE VARIACIÓN:")
        print(f"{'Variable':<20} {municipio_1:<15} {municipio_2:<15} {'Mayor Variabilidad':<20}")
        print("-" * 75)
        
        # Velocidad del viento
        cv_vel_1 = datos_1['vel_cv']
        cv_vel_2 = datos_2['vel_cv']
        mayor_var_vel = municipio_1 if cv_vel_1 > cv_vel_2 else municipio_2
        
        print(f"{'Velocidad Viento':<20} {cv_vel_1:<15.3f} {cv_vel_2:<15.3f} {mayor_var_vel:<20}")
        
        # Temperatura
        cv_temp_1 = datos_1['temp_cv']
        cv_temp_2 = datos_2['temp_cv']
        mayor_var_temp = municipio_1 if cv_temp_1 > cv_temp_2 else municipio_2
        
        print(f"{'Temperatura':<20} {cv_temp_1:<15.3f} {cv_temp_2:<15.3f} {mayor_var_temp:<20}")
        
        # Análisis general
        cv_promedio_1 = (cv_vel_1 + cv_temp_1) / 2
        cv_promedio_2 = (cv_vel_2 + cv_temp_2) / 2
        mayor_var_general = municipio_1 if cv_promedio_1 > cv_promedio_2 else municipio_2
        
        print(f"{'Promedio General':<20} {cv_promedio_1:<15.3f} {cv_promedio_2:<15.3f} {mayor_var_general:<20}")
        
        print(f"\n📊 CONCLUSIÓN SOBRE VARIABILIDAD:")
        print(f"   🎯 {mayor_var_general} presenta MAYOR VARIABILIDAD general")
        print(f"   📈 Velocidad del viento: {mayor_var_vel} es más variable")
        print(f"   🌡️ Temperatura: {mayor_var_temp} es más variable")
        
        # Interpretación de los coeficientes
        print(f"\n💡 INTERPRETACIÓN DE COEFICIENTES DE VARIACIÓN:")
        print(f"   • CV < 0.1 (10%): Baja variabilidad")
        print(f"   • CV 0.1-0.3 (10-30%): Variabilidad moderada") 
        print(f"   • CV > 0.3 (30%): Alta variabilidad")
        
        return mayor_var_general
    
    def generar_diagramas_caja_bigotes(self, municipio_1: str, municipio_2: str) -> None:
        """
        Generar diagramas de caja y bigotes para comparar las distribuciones
        """
        print(f"\n📦 FASE 4: DIAGRAMAS DE CAJA Y BIGOTES")
        print("=" * 50)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Preparar datos para boxplot
        datos_1 = self.resultados_municipios[municipio_1]['datos']
        datos_2 = self.resultados_municipios[municipio_2]['datos']
        
        # 1. Boxplot velocidad del viento
        vel_data = [datos_1['vel_viento (m/s)'], datos_2['vel_viento (m/s)']]
        bp1 = ax1.boxplot(vel_data, labels=[municipio_1, municipio_2], patch_artist=True)
        
        # Personalizar colores
        colors = ['lightblue', 'lightcoral']
        for patch, color in zip(bp1['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax1.set_title('Comparación de Velocidades del Viento', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Velocidad del viento (m/s)')
        ax1.grid(True, alpha=0.3)
        
        # Agregar estadísticas al gráfico
        stats_vel_1 = {
            'Q1': np.percentile(datos_1['vel_viento (m/s)'], 25),
            'Mediana': np.percentile(datos_1['vel_viento (m/s)'], 50),
            'Q3': np.percentile(datos_1['vel_viento (m/s)'], 75),
            'IQR': np.percentile(datos_1['vel_viento (m/s)'], 75) - np.percentile(datos_1['vel_viento (m/s)'], 25)
        }
        
        stats_vel_2 = {
            'Q1': np.percentile(datos_2['vel_viento (m/s)'], 25),
            'Mediana': np.percentile(datos_2['vel_viento (m/s)'], 50), 
            'Q3': np.percentile(datos_2['vel_viento (m/s)'], 75),
            'IQR': np.percentile(datos_2['vel_viento (m/s)'], 75) - np.percentile(datos_2['vel_viento (m/s)'], 25)
        }
        
        # 2. Boxplot temperatura
        temp_data = [datos_1['T (°C)'], datos_2['T (°C)']]
        bp2 = ax2.boxplot(temp_data, labels=[municipio_1, municipio_2], patch_artist=True)
        
        # Personalizar colores
        colors_temp = ['lightgreen', 'wheat']
        for patch, color in zip(bp2['boxes'], colors_temp):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax2.set_title('Comparación de Temperaturas', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Temperatura (°C)')
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle(f'Diagramas de Caja y Bigotes - {municipio_1} vs {municipio_2}',
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        # Mostrar interpretación estadística
        print(f"📊 INTERPRETACIÓN DE DIAGRAMAS DE CAJA Y BIGOTES:")
        print(f"\n🌪️ VELOCIDAD DEL VIENTO:")
        print(f"   {municipio_1}:")
        print(f"      • Q1: {stats_vel_1['Q1']:.2f} m/s | Mediana: {stats_vel_1['Mediana']:.2f} m/s | Q3: {stats_vel_1['Q3']:.2f} m/s")
        print(f"      • IQR (Rango intercuartílico): {stats_vel_1['IQR']:.2f} m/s")
        print(f"   {municipio_2}:")
        print(f"      • Q1: {stats_vel_2['Q1']:.2f} m/s | Mediana: {stats_vel_2['Mediana']:.2f} m/s | Q3: {stats_vel_2['Q3']:.2f} m/s")
        print(f"      • IQR (Rango intercuartílico): {stats_vel_2['IQR']:.2f} m/s")
        
        iqr_mayor_vel = municipio_1 if stats_vel_1['IQR'] > stats_vel_2['IQR'] else municipio_2
        print(f"      ➡️ Mayor dispersión (IQR): {iqr_mayor_vel}")
        
        print(f"✅ Diagramas de caja y bigotes generados exitosamente")
    
    def calcular_parametros_weibull_paso_a_paso(self, municipio: str) -> Dict:
        """
        Calcular parámetros k y c mostrando explícitamente cada paso
        de sustitución en las ecuaciones 3 y 4
        """
        print(f"\n🧮 CÁLCULO PASO A PASO DE PARÁMETROS WEIBULL - {municipio.upper()}")
        print("=" * 70)
        
        datos_municipio = self.resultados_municipios[municipio]['datos']
        velocidades = datos_municipio['vel_viento (m/s)'].values
        
        # Paso 1: Calcular estadísticas básicas
        print(f"📊 PASO 1: CÁLCULO DE ESTADÍSTICAS BÁSICAS")
        print("-" * 45)
        
        v_promedio = float(np.mean(velocidades))
        sigma = float(np.std(velocidades, ddof=1))
        n_datos = len(velocidades)
        
        print(f"   • Número de observaciones (n): {n_datos}")
        print(f"   • Velocidad promedio (v̅): {v_promedio:.4f} m/s")
        print(f"   • Desviación estándar (σ): {sigma:.4f} m/s") 
        print(f"   • Coeficiente de variación (σ/v̅): {sigma/v_promedio:.4f}")
        
        # Paso 2: Aplicar Ecuación 3 - Cálculo del parámetro k
        print(f"\n🔢 PASO 2: APLICACIÓN DE LA ECUACIÓN 3")
        print("-" * 45)
        print(f"📐 Ecuación 3: k = (σ/v̅)^(-1.09)")
        print(f"")
        print(f"   Sustitución de valores:")
        print(f"   k = ({sigma:.4f}/{v_promedio:.4f})^(-1.09)")
        
        coef_variacion = sigma / v_promedio
        print(f"   k = ({coef_variacion:.4f})^(-1.09)")
        
        k = np.power(coef_variacion, -1.09)
        print(f"   k = {k:.6f}")
        print(f"")
        print(f"   ✅ Parámetro de forma: k = {k:.4f}")
        
        # Paso 3: Aplicar Ecuación 4 - Cálculo del parámetro c
        print(f"\n🔢 PASO 3: APLICACIÓN DE LA ECUACIÓN 4")
        print("-" * 45)
        print(f"📐 Ecuación 4: c = v̅ / Γ(1+1/k)")
        print(f"")
        print(f"   Primero calculamos la función Gamma:")
        
        gamma_arg = 1 + 1/k
        gamma_val = gamma(gamma_arg)
        
        print(f"   Γ(1 + 1/k) = Γ(1 + 1/{k:.4f})")
        print(f"   Γ(1 + {1/k:.4f}) = Γ({gamma_arg:.4f})")
        print(f"   Γ({gamma_arg:.4f}) = {gamma_val:.6f}")
        print(f"")
        print(f"   Ahora sustituimos en la ecuación:")
        print(f"   c = {v_promedio:.4f} / {gamma_val:.6f}")
        
        c = v_promedio / gamma_val
        print(f"   c = {c:.6f}")
        print(f"")
        print(f"   ✅ Parámetro de escala: c = {c:.4f} m/s")
        
        # Paso 4: Verificación matemática
        print(f"\n✅ PASO 4: VERIFICACIÓN MATEMÁTICA")
        print("-" * 45)
        
        v_media_teorica = c * gamma(1 + 1/k)
        error_absoluto = abs(v_media_teorica - v_promedio)
        error_relativo = (error_absoluto / v_promedio) * 100
        
        print(f"   Media teórica: c × Γ(1+1/k) = {c:.4f} × {gamma(1 + 1/k):.6f} = {v_media_teorica:.4f} m/s")
        print(f"   Media observada: {v_promedio:.4f} m/s")
        print(f"   Error absoluto: {error_absoluto:.6f} m/s")
        print(f"   Error relativo: {error_relativo:.6f} %")
        
        if error_relativo < 0.01:
            print(f"   ✅ Verificación EXITOSA (error < 0.01%)")
        else:
            print(f"   ⚠️ Verificación con error: {error_relativo:.4f}%")
        
        # Guardar resultados
        resultado = {
            'municipio': municipio,
            'n_datos': n_datos,
            'v_promedio': v_promedio,
            'sigma': sigma,
            'coef_variacion': coef_variacion,
            'k': k,
            'c': c,
            'gamma_val': gamma_val,
            'v_media_teorica': v_media_teorica,
            'error_relativo_pct': error_relativo,
            'velocidades': velocidades
        }
        
        return resultado
    
    def sustituir_en_funcion_densidad(self, resultado_municipio: Dict) -> None:
        """
        Sustituir los parámetros calculados en la función de densidad f(v) 
        (Ecuación 1) y mostrar el proceso paso a paso
        """
        municipio = resultado_municipio['municipio']
        k = resultado_municipio['k']
        c = resultado_municipio['c']
        
        print(f"\n📈 PASO 5: SUSTITUCIÓN EN FUNCIÓN DE DENSIDAD f(v) - {municipio.upper()}")
        print("=" * 70)
        print(f"📐 Ecuación 1: f(v) = (k/c) × (v/c)^(k-1) × e^(-(v/c)^k)")
        print(f"")
        print(f"   Sustituyendo los parámetros calculados:")
        print(f"   k = {k:.4f}")
        print(f"   c = {c:.4f} m/s")
        print(f"")
        print(f"   f(v) = ({k:.4f}/{c:.4f}) × (v/{c:.4f})^({k:.4f}-1) × e^(-(v/{c:.4f})^{k:.4f})")
        
        # Simplificar el primer término
        k_sobre_c = k / c
        print(f"")
        print(f"   Simplificando el primer término:")
        print(f"   k/c = {k:.4f}/{c:.4f} = {k_sobre_c:.6f}")
        print(f"")
        print(f"   Simplificando el exponente del segundo término:")
        print(f"   k-1 = {k:.4f}-1 = {k-1:.4f}")
        print(f"")
        print(f"   Por lo tanto:")
        print(f"   f(v) = {k_sobre_c:.6f} × (v/{c:.4f})^{k-1:.4f} × e^(-(v/{c:.4f})^{k:.4f})")
        
        # Crear gráfica de la función de densidad
        v = np.linspace(0.1, np.max(resultado_municipio['velocidades']) * 1.2, 1000)
        
        # Calcular la función de densidad
        f_v = (k/c) * np.power(v/c, k-1) * np.exp(-np.power(v/c, k))
        
        # Generar gráfica
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Gráfica 1: Función de densidad vs histograma
        ax1.hist(resultado_municipio['velocidades'], bins=40, density=True, alpha=0.6, 
                color='lightblue', edgecolor='black', label='Datos observados')
        ax1.plot(v, f_v, 'r-', linewidth=3, label=f'f(v) Weibull')
        ax1.set_xlabel('Velocidad del viento (m/s)')
        ax1.set_ylabel('Densidad de probabilidad')
        ax1.set_title(f'Función de Densidad de Weibull - {municipio}\nk={k:.3f}, c={c:.2f} m/s')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfica 2: Evaluación en puntos específicos
        v_puntos = [5, 10, 15, 20]  # Velocidades específicas para evaluar
        f_puntos = []
        
        for v_punto in v_puntos:
            if v_punto <= np.max(v):
                f_punto = (k/c) * np.power(v_punto/c, k-1) * np.exp(-np.power(v_punto/c, k))
                f_puntos.append(f_punto)
                
                # Mostrar cálculo detallado
                print(f"\n   📍 Evaluando f({v_punto}) m/s:")
                print(f"      f({v_punto}) = {k_sobre_c:.6f} × ({v_punto}/{c:.4f})^{k-1:.4f} × e^(-({v_punto}/{c:.4f})^{k:.4f})")
                
                termino1 = k_sobre_c
                termino2 = np.power(v_punto/c, k-1)
                termino3 = np.exp(-np.power(v_punto/c, k))
                
                print(f"      f({v_punto}) = {termino1:.6f} × {termino2:.6f} × {termino3:.6f}")
                print(f"      f({v_punto}) = {f_punto:.6f}")
        
        # Graficar puntos específicos
        ax2.plot(v, f_v, 'b-', linewidth=2, label='f(v) Weibull')
        if f_puntos:
            ax2.scatter(v_puntos[:len(f_puntos)], f_puntos, color='red', s=100, zorder=5,
                       label='Puntos evaluados')
            
            # Agregar anotaciones
            for i, (v_p, f_p) in enumerate(zip(v_puntos[:len(f_puntos)], f_puntos)):
                ax2.annotate(f'f({v_p})={f_p:.4f}', 
                           xy=(v_p, f_p), xytext=(10, 10),
                           textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        ax2.set_xlabel('Velocidad del viento (m/s)')
        ax2.set_ylabel('Densidad de probabilidad')
        ax2.set_title(f'Evaluación de f(v) en Puntos Específicos - {municipio}')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        print(f"\n✅ Función de densidad f(v) calculada y graficada exitosamente")
        
        # Calcular algunas propiedades adicionales
        v_media_pdf = c * gamma(1 + 1/k)
        v_moda = c * np.power((k-1)/k, 1/k) if k > 1 else 0
        
        print(f"\n📊 PROPIEDADES DE LA DISTRIBUCIÓN:")
        print(f"   • Media de la distribución: {v_media_pdf:.4f} m/s")
        print(f"   • Moda (velocidad más probable): {v_moda:.4f} m/s")
        print(f"   • Parámetro k (forma): {k:.4f}")
        print(f"   • Parámetro c (escala): {c:.4f} m/s")
    
    def ejecutar_analisis_completo(self, interactivo: bool = True) -> None:
        """
        Ejecutar el análisis completo paso a paso
        
        Parameters:
        -----------
        interactivo : bool, optional
            Si True, solicita al usuario seleccionar los municipios.
            Si False, usa selección automática (por defecto True)
        """
        # Cargar datos
        self.cargar_datos_completos()
        
        # Seleccionar municipios (interactivo o automático)
        if interactivo:
            try:
                municipio_1, municipio_2 = self.solicitar_municipios_usuario()
            except Exception as e:
                print(f"\n⚠️ Error en selección interactiva: {e}")
                print(f"🔄 Cambiando a selección automática...")
                municipio_1, municipio_2 = self.seleccionar_municipios_contrastantes()
        else:
            municipio_1, municipio_2 = self.seleccionar_municipios_contrastantes()
        
        # Generar histogramas
        self.generar_histogramas_comparativos(municipio_1, municipio_2)
        
        # Analizar variabilidad
        municipio_mayor_variabilidad = self.analizar_variabilidad_comparativa(municipio_1, municipio_2)
        
        # Diagramas de caja y bigotes
        self.generar_diagramas_caja_bigotes(municipio_1, municipio_2)
        
        # Calcular parámetros Weibull para cada municipio
        print(f"\n🔬 ANÁLISIS DE WEIBULL PARA AMBOS MUNICIPIOS")
        print("=" * 70)
        
        for municipio in [municipio_1, municipio_2]:
            # Calcular parámetros paso a paso
            resultado = self.calcular_parametros_weibull_paso_a_paso(municipio)
            
            # Sustituir en función de densidad
            self.sustituir_en_funcion_densidad(resultado)
        
        # Resumen final
        print(f"\n🎯 RESUMEN FINAL DEL ANÁLISIS")
        print("=" * 50)
        print(f"✅ Municipios analizados: {municipio_1} y {municipio_2}")
        print(f"✅ Municipio con mayor variabilidad: {municipio_mayor_variabilidad}")
        print(f"✅ Parámetros k y c calculados para ambos municipios")
        print(f"✅ Funciones de densidad f(v) generadas exitosamente")
        print(f"✅ Todas las sustituciones mostradas paso a paso")


def ejecutar_analisis_detallado(interactivo: bool = True):
    """
    Función principal para ejecutar el análisis detallado
    
    Parameters:
    -----------
    interactivo : bool, optional
        Si True, solicita al usuario seleccionar los municipios.
        Si False, usa selección automática (por defecto True)
    """
    analizador = AnalisisDetalladoWeibull("Datos.xlsx")
    analizador.ejecutar_analisis_completo(interactivo=interactivo)
    return analizador


if __name__ == "__main__":
    import sys
    
    print("🌪️ ANÁLISIS DETALLADO DE WEIBULL - OPCIONES DE EJECUCIÓN")
    print("=" * 60)
    print("1️⃣ Modo INTERACTIVO: Tú seleccionas los municipios")
    print("2️⃣ Modo AUTOMÁTICO: Selección predeterminada (Riohacha vs Valledupar)")
    print()
    
    # Detectar si se está ejecutando desde terminal interactiva
    try:
        # Intentar obtener input del usuario
        if len(sys.argv) > 1 and sys.argv[1].lower() == 'auto':
            # Ejecutar en modo automático si se pasa 'auto' como argumento
            print("🔄 Ejecutando en modo AUTOMÁTICO (argumento 'auto' detectado)")
            analizador = ejecutar_analisis_detallado(interactivo=False)
        else:
            # Por defecto, ejecutar en modo interactivo
            print("👤 Ejecutando en modo INTERACTIVO")
            print("💡 Tip: Para ejecutar en modo automático, usa: python script.py auto")
            print()
            analizador = ejecutar_analisis_detallado(interactivo=True)
            
    except Exception as e:
        print(f"⚠️ Error durante la ejecución: {e}")
        print("🔄 Intentando ejecución en modo automático como respaldo...")
        analizador = ejecutar_analisis_detallado(interactivo=False)
