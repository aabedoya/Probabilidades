"""
ANÁLISIS DE WEIBULL EDUCATIVO - APLICACIÓN COMPLETA
===================================================

Esta aplicación permite:
1. Seleccionar 2 ciudades de forma interactiva
2. Realizar análisis completo de Weibull con explicaciones paso a paso
3. Mostrar todos los cálculos con sustitución de valores
4. Generar visualizaciones educativas

Actividades cubiertas:
- Semana 3: Actividades 1 y 2
- Semana 4: Actividades 3 y 4  
- Semana 5: Actividades 5, 6 y 7

Autor: Proyecto Probabilidades
Fecha: 22 de septiembre de 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import seaborn as sns
from typing import Tuple, Dict, List
import os

# Importar el generador de PDF
from generador_pdf_weibull import GeneradorPDFWeibull

# Configurar estilo de gráficas
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class AnalisisWeibullEducativo:
    """Análisis educativo completo de Weibull con selección interactiva de ciudades"""
    
    def __init__(self, archivo_excel: str = "Datos.xlsx"):
        """Inicializar con archivo de datos"""
        self.archivo_excel = archivo_excel
        self.datos = pd.DataFrame()
        self.ciudades_disponibles = [
            "Girardot", "Tumaco", "Bucaramanga", "Medellín", "Valledupar", 
            "San Andrés", "Guapí", "Mocoa", "Riohacha", "Cartagena"
        ]
        self.ciudades_seleccionadas = []
        self.resultados = {}
        
    def mostrar_bienvenida(self):
        """Mostrar mensaje de bienvenida"""
        # print("🌪️" + "=" * 70)
        # print("    ANÁLISIS DE WEIBULL EDUCATIVO - APLICACIÓN COMPLETA")
        # print("=" * 72)
        # print("📚 Esta aplicación te guiará paso a paso en el análisis de Weibull")
        # print("🎯 Aprenderás cómo calcular parámetros y probabilidades")
        # print("📊 Verás sustituciones de valores en todas las fórmulas")
        # print("=" * 72)
        pass
        
    def cargar_datos(self) -> bool:
        """Cargar y verificar datos"""
        try:
            # print("\n📁 CARGANDO DATOS METEOROLÓGICOS...")
            # print("-" * 40)
            
            if not os.path.exists(self.archivo_excel):
                # print(f"❌ Error: No se encontró el archivo {self.archivo_excel}")
                return False
                
            self.datos = pd.read_excel(self.archivo_excel)
            # print(f"✅ Datos cargados exitosamente: {self.datos.shape[0]:,} registros")
            
            # Verificar columnas necesarias
            columnas_requeridas = ['Municipio', 'vel_viento (m/s)', 'T (°C)']
            if not all(col in self.datos.columns for col in columnas_requeridas):
                # print("❌ Error: Faltan columnas requeridas en el archivo")
                return False
                
            # Verificar ciudades disponibles
            municipios_en_datos = set(self.datos['Municipio'].unique())
            ciudades_validas = [c for c in self.ciudades_disponibles if c in municipios_en_datos]
            
            if len(ciudades_validas) < 2:
                # print("❌ Error: No hay suficientes ciudades válidas en los datos")
                return False
                
            self.ciudades_disponibles = ciudades_validas
            # print(f"📍 Ciudades disponibles: {len(self.ciudades_disponibles)}")
            
            return True
            
        except Exception as e:
            # print(f"❌ Error al cargar datos: {str(e)}")
            return False
    
    def mostrar_ciudades_disponibles(self):
        """Mostrar ciudades disponibles con estadísticas"""
        # print(f"\n🏙️ CIUDADES DISPONIBLES PARA ANÁLISIS")
        # print("=" * 50)
        # print(f"{'#':<3} {'Ciudad':<15} {'Registros':<10} {'Vel.Media':<12} {'Temp.Media'}")
        # print("-" * 50)
        
        for i, ciudad in enumerate(self.ciudades_disponibles, 1):
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            vel_media = datos_ciudad['vel_viento (m/s)'].mean()
            temp_media = datos_ciudad['T (°C)'].mean()
            registros = len(datos_ciudad)
            
            # print(f"{i:<3} {ciudad:<15} {registros:<10} {vel_media:<12.2f} {temp_media:.1f}°C")
        pass
    
    def seleccionar_ciudades_interactivo(self) -> bool:
        """Selección interactiva de 2 ciudades"""
        self.mostrar_ciudades_disponibles()
        
        # print(f"\n🎯 SELECCIÓN DE CIUDADES")
        # print("=" * 30)
        # print("Debes seleccionar 2 ciudades diferentes para el análisis")
        
        ciudades_seleccionadas = []
        
        for i in range(2):
            while True:
                try:
                    # print(f"\n📍 Selecciona la ciudad #{i+1}:")
                    opcion = input(f"Ingresa el número (1-{len(self.ciudades_disponibles)}): ").strip()
                    
                    if not opcion.isdigit():
                        # print("❌ Por favor ingresa un número válido")
                        continue
                        
                    indice = int(opcion) - 1
                    
                    if indice < 0 or indice >= len(self.ciudades_disponibles):
                        # print(f"❌ Número fuera de rango. Debe estar entre 1 y {len(self.ciudades_disponibles)}")
                        continue
                        
                    ciudad_elegida = self.ciudades_disponibles[indice]
                    
                    if ciudad_elegida in ciudades_seleccionadas:
                        # print("❌ Esta ciudad ya fue seleccionada. Elige una diferente.")
                        continue
                        
                    ciudades_seleccionadas.append(ciudad_elegida)
                    # print(f"✅ {ciudad_elegida} seleccionada")
                    break
                    
                except (ValueError, KeyboardInterrupt):
                    # print("❌ Entrada inválida. Intenta de nuevo.")
                    pass
                    
        self.ciudades_seleccionadas = ciudades_seleccionadas
        
        # print(f"\n🎉 CIUDADES SELECCIONADAS:")
        # print(f"   1️⃣ {ciudades_seleccionadas[0]}")
        # print(f"   2️⃣ {ciudades_seleccionadas[1]}")
        
        return True
    
    def extraer_datos_ciudades(self):
        """Extraer y preparar datos de las ciudades seleccionadas"""
        # print(f"\n📊 EXTRAYENDO DATOS DE LAS CIUDADES SELECCIONADAS")
        # print("=" * 55)
        
        for ciudad in self.ciudades_seleccionadas:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad].copy()
            
            # Limpiar datos (remover valores nulos o extremos)
            datos_ciudad = datos_ciudad.dropna(subset=['vel_viento (m/s)', 'T (°C)'])
            
            # print(f"\n🏙️ {ciudad.upper()}:")
            # print(f"   • Registros totales: {len(datos_ciudad):,}")
            # print(f"   • Velocidad del viento promedio: {datos_ciudad['vel_viento (m/s)'].mean():.2f} m/s")
            # print(f"   • Temperatura promedio: {datos_ciudad['T (°C)'].mean():.1f}°C")
            # print(f"   • Rango de velocidades: {datos_ciudad['vel_viento (m/s)'].min():.1f} - {datos_ciudad['vel_viento (m/s)'].max():.1f} m/s")
            
            self.resultados[ciudad] = {
                'datos': datos_ciudad,
                'velocidades': datos_ciudad['vel_viento (m/s)'].values,
                'temperaturas': datos_ciudad['T (°C)'].values
            }
    
    def mostrar_estadisticos_basicos(self):
        """Mostrar estadísticos básicos iniciales y parámetros Weibull"""
        # print(f"\n" + "🔥" * 70)
        # print("DATOS ESTADÍSTICOS BÁSICOS INICIALES")
        # print("🔥" * 70)
        
        # print("📊 CÁLCULO DE ESTADÍSTICOS BÁSICOS")
        # print("="*60)
        
        # Cálculos estadísticos básicos para cada ciudad
        for ciudad in self.ciudades_seleccionadas:
            datos_ciudad = self.resultados[ciudad]['datos']
            viento = datos_ciudad['vel_viento (m/s)']
            
            # Cálculos estadísticos básicos
            media = viento.mean()
            mediana = viento.median()
            moda_valores = viento.mode()
            desviacion = viento.std()
            minimo = viento.min()
            maximo = viento.max()
            rango = maximo - minimo
            cv = desviacion / media
            
            # print(f"\n🏙️ {ciudad.upper()}:")
            # print("-" * 50)
            # print(f"   📈 Media (μ):           {media:.4f} m/s")
            # print(f"   📊 Mediana:            {mediana:.4f} m/s")
            if len(moda_valores) == 1:
                # print(f"   📍 Moda:               {moda_valores.iloc[0]:.4f} m/s")
                pass
            else:
                modas_str = ", ".join([f"{x:.4f}" for x in moda_valores.head(3)])
                # print(f"   📍 Modas:              {modas_str} m/s")
                pass
            # print(f"   📏 Desviación (σ):     {desviacion:.4f} m/s")
            # print(f"   📐 Rango:              {rango:.4f} m/s ({minimo:.1f} - {maximo:.1f})")
            # print(f"   📊 Coef. Variación:    {cv:.4f} ({cv*100:.2f}%)")
        
        # Cálculo de parámetros Weibull
        # print("\n" + "🔥"*70)
        # print("PARÁMETROS WEIBULL CALCULADOS")
        # print("🔥"*70)
        
        parametros_weibull = {}
        
        for ciudad in self.ciudades_seleccionadas:
            datos_ciudad = self.resultados[ciudad]['datos']
            viento = datos_ciudad['vel_viento (m/s)']
            
            # Cálculos estadísticos
            media = viento.mean()
            mediana = viento.median()
            moda_valores = viento.mode()
            desviacion = viento.std()
            minimo = viento.min()
            maximo = viento.max()
            rango = maximo - minimo
            cv = desviacion / media
            
            # Parámetros Weibull
            k = cv ** (-1.09)
            gamma_value = gamma(1 + 1/k)
            c = media / gamma_value
            
            parametros_weibull[ciudad] = {'k': k, 'c': c, 'gamma': gamma_value}
            
            # print(f"\n🏙️ {ciudad.upper()}:")
            # print("-" * 60)
            # print(f"   📈 Media (μ):           {media:.4f} m/s")
            # print(f"   📊 Mediana:            {mediana:.4f} m/s")
            if len(moda_valores) == 1:
                # print(f"   📍 Moda:               {moda_valores.iloc[0]:.4f} m/s")
            else:
                modas_str = ", ".join([f"{x:.4f}" for x in moda_valores.head(3)])
                # print(f"   📍 Modas:              {modas_str} m/s")
            # print(f"   📏 Desviación (σ):     {desviacion:.4f} m/s")
            # print(f"   📐 Rango:              {rango:.4f} m/s")
            # print(f"   📊 Coef. Variación:    {cv:.4f}")
            # print(f"   ⚡ Parámetro K:        {k:.4f}")
            # print(f"   🧮 Función Gamma:      {gamma_value:.6f}")
            # print(f"   📏 Parámetro C:        {c:.4f} m/s")
        
        # Tabla de función de densidad
        # print("\n" + "🔥"*70)
        # print("TABLA DE FUNCIÓN DE DENSIDAD f(v)")
        # print("🔥"*70)
        
        velocidades = np.arange(5, 31, 2.5)  # Velocidades de 5 a 30 m/s cada 2.5
        
        for ciudad in self.ciudades_seleccionadas:
            k = parametros_weibull[ciudad]['k']
            c = parametros_weibull[ciudad]['c']
            
            # print(f"\n🏙️ {ciudad.upper()} (k={k:.4f}, c={c:.4f}):")
            # print("-" * 50)
            # print("   Velocidad (m/s)  |    f(v)")
            # print("   " + "-"*17 + "|" + "-"*10)
            
            for v in velocidades:
                f_v = (k/c) * (v/c)**(k-1) * np.exp(-(v/c)**k)
                # print(f"        {v:6.1f}     |  {f_v:.6f}")

    def actividad_1_histogramas_y_variabilidad(self):
        """SEMANA 3 - ACTIVIDAD 1: Histogramas y análisis de variabilidad"""
        # print(f"\n" + "🔥" * 70)
        # print("SEMANA 3 - ACTIVIDAD 1: HISTOGRAMAS Y ANÁLISIS DE VARIABILIDAD")
        # print("🔥" * 70)
        
        ciudad1, ciudad2 = self.ciudades_seleccionadas
        
        # Crear histogramas
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        for i, ciudad in enumerate(self.ciudades_seleccionadas):
            datos = self.resultados[ciudad]
            velocidades = datos['velocidades']
            temperaturas = datos['temperaturas']
            
            # Histograma velocidades
            ax_vel = axes[0, i]
            n, bins, patches = ax_vel.hist(velocidades, bins=30, alpha=0.7, 
                                         color=['blue', 'red'][i], edgecolor='black', density=True)
            
            vel_mean = np.mean(velocidades)
            vel_std = np.std(velocidades, ddof=1)
            vel_cv = vel_std / vel_mean
            
            ax_vel.axvline(vel_mean, color='darkred', linestyle='--', linewidth=2, label=f'Media: {vel_mean:.2f}')
            ax_vel.set_title(f'Velocidad del Viento - {ciudad}', fontweight='bold', fontsize=12)
            ax_vel.set_xlabel('Velocidad (m/s)')
            ax_vel.set_ylabel('Densidad')
            ax_vel.legend()
            ax_vel.grid(True, alpha=0.3)
            
            # Histograma temperaturas
            ax_temp = axes[1, i]
            ax_temp.hist(temperaturas, bins=30, alpha=0.7, 
                        color=['green', 'orange'][i], edgecolor='black', density=True)
            
            temp_mean = np.mean(temperaturas)
            temp_std = np.std(temperaturas, ddof=1)
            temp_cv = temp_std / temp_mean
            
            ax_temp.axvline(temp_mean, color='darkred', linestyle='--', linewidth=2, label=f'Media: {temp_mean:.1f}')
            ax_temp.set_title(f'Temperatura - {ciudad}', fontweight='bold', fontsize=12)
            ax_temp.set_xlabel('Temperatura (°C)')
            ax_temp.set_ylabel('Densidad')
            ax_temp.legend()
            ax_temp.grid(True, alpha=0.3)
            
            # Guardar estadísticas
            self.resultados[ciudad].update({
                'vel_mean': vel_mean,
                'vel_std': vel_std,
                'vel_cv': vel_cv,
                'temp_mean': temp_mean,
                'temp_std': temp_std,
                'temp_cv': temp_cv
            })
        
        plt.suptitle(f'HISTOGRAMAS COMPARATIVOS - {ciudad1} vs {ciudad2}', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        # Análisis de variabilidad
        # print(f"\n📈 ANÁLISIS DE VARIABILIDAD - COEFICIENTE DE VARIACIÓN")
        # print("=" * 58)
        # print(f"🧮 FÓRMULA: CV = σ/μ (Desviación estándar / Media)")
        # print(f"")
        
        # print(f"📊 CÁLCULOS DETALLADOS:")
        # print("-" * 60)
        
        cv_totales = {}
        
        for ciudad in self.ciudades_seleccionadas:
            stats = self.resultados[ciudad]
            
            # print(f"\n🏙️ {ciudad.upper()}:")
            # print(f"   Velocidad del viento:")
            # print(f"     • Media (μ): {stats['vel_mean']:.4f} m/s")
            # print(f"     • Desv. Estándar (σ): {stats['vel_std']:.4f} m/s")
            # print(f"     • CV = σ/μ = {stats['vel_std']:.4f}/{stats['vel_mean']:.4f} = {stats['vel_cv']:.4f}")
            
            # print(f"   Temperatura:")
            # print(f"     • Media (μ): {stats['temp_mean']:.4f} °C")
            # print(f"     • Desv. Estándar (σ): {stats['temp_std']:.4f} °C")
            # print(f"     • CV = σ/μ = {stats['temp_std']:.4f}/{stats['temp_mean']:.4f} = {stats['temp_cv']:.4f}")
            
            cv_promedio = (stats['vel_cv'] + stats['temp_cv']) / 2
            cv_totales[ciudad] = cv_promedio
            # print(f"   CV Promedio: ({stats['vel_cv']:.4f} + {stats['temp_cv']:.4f})/2 = {cv_promedio:.4f}")
        
        # Determinar ciudad con mayor variabilidad
        ciudad_mayor_var = max(cv_totales, key=cv_totales.get)
        
        # print(f"\n🎯 CONCLUSIÓN:")
        # print(f"   {ciudad_mayor_var.upper()} presenta MAYOR VARIABILIDAD")
        # print(f"   CV({ciudad_mayor_var}) = {cv_totales[ciudad_mayor_var]:.4f}")
        
        # Diagramas de caja y bigotes
        self.generar_boxplots()
        
        return ciudad_mayor_var
    
    def generar_boxplots(self):
        """Generar diagramas de caja y bigotes comparativos"""
        # print(f"\n📦 DIAGRAMAS DE CAJA Y BIGOTES")
        # print("=" * 35)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Preparar datos para boxplot
        velocidades_data = []
        temperaturas_data = []
        labels = []
        
        for ciudad in self.ciudades_seleccionadas:
            velocidades_data.append(self.resultados[ciudad]['velocidades'])
            temperaturas_data.append(self.resultados[ciudad]['temperaturas'])
            labels.append(ciudad)
        
        # Boxplot velocidades
        bp1 = ax1.boxplot(velocidades_data, labels=labels, patch_artist=True)
        colors = ['lightblue', 'lightcoral']
        for patch, color in zip(bp1['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax1.set_title('Velocidades del Viento', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Velocidad (m/s)')
        ax1.grid(True, alpha=0.3)
        
        # Boxplot temperaturas
        bp2 = ax2.boxplot(temperaturas_data, labels=labels, patch_artist=True)
        colors_temp = ['lightgreen', 'wheat']
        for patch, color in zip(bp2['boxes'], colors_temp):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax2.set_title('Temperaturas', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Temperatura (°C)')
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle('DIAGRAMAS DE CAJA Y BIGOTES COMPARATIVOS', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        # print("✅ Diagramas generados - Permiten comparar distribuciones y outliers")
    
    def actividad_2_parametros_weibull(self):
        """SEMANA 3 - ACTIVIDAD 2: Calcular parámetros k y c de Weibull"""
        # print(f"\n" + "🔥" * 70)
        # print("SEMANA 3 - ACTIVIDAD 2: CÁLCULO DE PARÁMETROS WEIBULL")
        # print("🔥" * 70)
        
        resultados_weibull = {}
        
        for ciudad in self.ciudades_seleccionadas:
            # print(f"\n" + "="*60)
            # print(f"🧮 CÁLCULO PARA {ciudad.upper()}")
            # print("="*60)
            
            velocidades = self.resultados[ciudad]['velocidades']
            v_promedio = float(np.mean(velocidades))
            sigma = float(np.std(velocidades, ddof=1))
            coef_variacion = sigma / v_promedio
            
            # print(f"📊 DATOS BÁSICOS:")
            # print(f"   • Número de observaciones: {len(velocidades):,}")
            # print(f"   • Velocidad promedio (v̅): {v_promedio:.4f} m/s")
            # print(f"   • Desviación estándar (σ): {sigma:.4f} m/s")
            # print(f"   • Coeficiente de variación: σ/v̅ = {sigma:.4f}/{v_promedio:.4f} = {coef_variacion:.4f}")
            
            # ECUACIÓN 3: Parámetro k
            # print(f"\n🔢 ECUACIÓN 3 - CÁLCULO DEL PARÁMETRO DE FORMA (k):")
            # print(f"   k = (σ/v̅)^(-1.09)")
            # print(f"   ")
            # print(f"   Paso 1: Coeficiente de variación = {coef_variacion:.4f}")
            # print(f"   Paso 2: Exponente = -1.09")
            # print(f"   Paso 3: k = ({coef_variacion:.4f})^(-1.09)")
            
            k = np.power(coef_variacion, -1.09)
            # print(f"   Paso 4: k = {k:.4f}")
            # print(f"   ")
            # print(f"   ✅ PARÁMETRO DE FORMA: k = {k:.4f}")
            
            # ECUACIÓN 4: Parámetro c
            # print(f"\n🔢 ECUACIÓN 4 - CÁLCULO DEL PARÁMETRO DE ESCALA (c):")
            # print(f"   c = v̅ / Γ(1 + 1/k)")
            # print(f"   ")
            
            gamma_arg = 1 + 1/k
            gamma_val = gamma(gamma_arg)
            c = v_promedio / gamma_val
            
            # print(f"   Paso 1: Argumento de gamma = 1 + 1/k = 1 + 1/{k:.4f} = {gamma_arg:.4f}")
            # print(f"   Paso 2: Γ({gamma_arg:.4f}) = {gamma_val:.6f}")
            # print(f"   Paso 3: c = v̅/Γ(1+1/k) = {v_promedio:.4f}/{gamma_val:.6f}")
            # print(f"   Paso 4: c = {c:.4f} m/s")
            # print(f"   ")
            # print(f"   ✅ PARÁMETRO DE ESCALA: c = {c:.4f} m/s")
            
            # Verificación
            v_teorica = c * gamma(1 + 1/k)
            error_relativo = abs(v_teorica - v_promedio) / v_promedio * 100
            
            # print(f"\n✅ VERIFICACIÓN MATEMÁTICA:")
            # print(f"   Media teórica = c × Γ(1+1/k) = {c:.4f} × {gamma(1 + 1/k):.6f} = {v_teorica:.4f} m/s")
            # print(f"   Media observada = {v_promedio:.4f} m/s")
            # print(f"   Error relativo = |{v_teorica:.4f} - {v_promedio:.4f}|/{v_promedio:.4f} × 100% = {error_relativo:.6f}%")
            
            # Sustitución en función de densidad
            # print(f"\n📈 SUSTITUCIÓN EN FUNCIÓN DE DENSIDAD f(v) - ECUACIÓN 1:")
            # print(f"   f(v) = (k/c) × (v/c)^(k-1) × e^(-(v/c)^k)")
            # print(f"   ")
            
            k_sobre_c = k / c
            k_menos_1 = k - 1
            
            # print(f"   Sustituyendo valores:")
            # print(f"   f(v) = ({k:.4f}/{c:.4f}) × (v/{c:.4f})^({k:.4f}-1) × e^(-(v/{c:.4f})^{k:.4f})")
            # print(f"   f(v) = {k_sobre_c:.4f} × (v/{c:.4f})^{k_menos_1:.4f} × e^(-(v/{c:.4f})^{k:.4f})")
            
            resultados_weibull[ciudad] = {
                'k': k,
                'c': c,
                'v_promedio': v_promedio,
                'sigma': sigma,
                'velocidades': velocidades,
                'coef_variacion': coef_variacion
            }
        
        return resultados_weibull
    
    def actividad_3_graficar_distribucion(self, resultados_weibull):
        """SEMANA 4 - ACTIVIDAD 3: Graficar distribución vs histograma"""
        # print(f"\n" + "🔥" * 70)
        # print("SEMANA 4 - ACTIVIDAD 3: DISTRIBUCIÓN WEIBULL VS HISTOGRAMA")
        # print("🔥" * 70)
        
        for ciudad in self.ciudades_seleccionadas:
            # print(f"\n🏙️ ANÁLISIS PARA {ciudad.upper()}")
            # print("=" * 50)
            
            resultado = resultados_weibull[ciudad]
            k = resultado['k']
            c = resultado['c']
            velocidades = resultado['velocidades']
            
            # Crear gráfico detallado
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # Histograma normalizado
            n, bins, patches = ax.hist(velocidades, bins=40, density=True, alpha=0.6,
                                     color='skyblue', edgecolor='black', label='Datos observados')
            
            # Función de densidad Weibull
            v_max = np.max(velocidades) * 1.2
            v = np.linspace(0.1, v_max, 1000)
            f_v = (k/c) * np.power(v/c, k-1) * np.exp(-np.power(v/c, k))
            
            ax.plot(v, f_v, 'r-', linewidth=3, 
                   label=f'Distribución Weibull\nk={k:.3f}, c={c:.2f} m/s')
            
            # Estadísticos importantes
            v_mean = np.mean(velocidades)
            v_median = np.median(velocidades)
            v_mode = c * np.power((k-1)/k, 1/k) if k > 1 else 0
            
            ax.axvline(v_mean, color='green', linestyle='--', alpha=0.8,
                      label=f'Media: {v_mean:.2f} m/s')
            ax.axvline(v_median, color='orange', linestyle='--', alpha=0.8,
                      label=f'Mediana: {v_median:.2f} m/s')
            if k > 1:
                ax.axvline(v_mode, color='purple', linestyle='--', alpha=0.8,
                          label=f'Moda: {v_mode:.2f} m/s')
            
            ax.set_xlabel('Velocidad del viento (m/s)', fontsize=12)
            ax.set_ylabel('Densidad de probabilidad', fontsize=12)
            ax.set_title(f'Distribución de Weibull vs Datos Observados - {ciudad}',
                        fontsize=14, pad=20, fontweight='bold')
            ax.legend(loc='upper right', fontsize=10)
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
            # Análisis del comportamiento
            # print(f"📊 ANÁLISIS DEL COMPORTAMIENTO:")
            # print(f"   1. Parámetros de la distribución:")
            # print(f"      • k = {k:.4f} (parámetro de forma)")
            # print(f"      • c = {c:.4f} m/s (parámetro de escala)")
            
            # print(f"   2. Forma de la distribución:")
            if k < 1:
                # print(f"      • Exponencial decreciente (k < 1)")
                # print(f"      • Alta frecuencia de velocidades bajas")
            elif 1 <= k < 2:
                # print(f"      • Asimétrica positiva (1 ≤ k < 2)")
                # print(f"      • Sesgada hacia velocidades bajas")
            elif 2 <= k < 3.6:
                # print(f"      • Aproximadamente simétrica (2 ≤ k < 3.6)")
                # print(f"      • Distribución balanceada")
            else:
                # print(f"      • Similar a normal (k ≥ 3.6)")
                # print(f"      • Concentración alrededor de la media")
            
            # print(f"   3. Estadísticos:")
            # print(f"      • Media: {v_mean:.2f} m/s")
            # print(f"      • Mediana: {v_median:.2f} m/s")
            # print(f"      • Moda: {v_mode:.2f} m/s" if k > 1 else "      • Moda: No definida (k ≤ 1)")
            
            # Evaluar ajuste
            hist_centers = (bins[:-1] + bins[1:]) / 2
            f_v_hist = (k/c) * np.power(hist_centers/c, k-1) * np.exp(-np.power(hist_centers/c, k))
            rmse = np.sqrt(np.mean((n - f_v_hist)**2))
            
            # print(f"   4. Calidad del ajuste:")
            # print(f"      • RMSE: {rmse:.4f}")
            if rmse < 0.01:
                # print(f"      • ✅ Excelente ajuste")
            elif rmse < 0.02:
                # print(f"      • ✅ Muy buen ajuste")
            elif rmse < 0.05:
                # print(f"      • ⚠️ Buen ajuste")
            else:
                # print(f"      • ⚠️ Ajuste moderado")
    
    def actividad_4_velocidades_caracteristicas(self, resultados_weibull):
        """SEMANA 4 - ACTIVIDAD 4: Velocidades características"""
        # print(f"\n" + "🔥" * 70)
        # print("SEMANA 4 - ACTIVIDAD 4: VELOCIDADES CARACTERÍSTICAS")
        # print("🔥" * 70)
        
        velocidades_caracteristicas = {}
        
        for ciudad in self.ciudades_seleccionadas:
            # print(f"\n" + "="*60)
            # print(f"⚡ ANÁLISIS PARA {ciudad.upper()}")
            # print("="*60)
            
            resultado = resultados_weibull[ciudad]
            k = resultado['k']
            c = resultado['c']
            v_promedio = resultado['v_promedio']
            
            # print(f"📊 PARÁMETROS:")
            # print(f"   • k = {k:.4f}")
            # print(f"   • c = {c:.4f} m/s")
            # print(f"   • v̅ = {v_promedio:.4f} m/s")
            
            # ECUACIÓN 5: Velocidad más probable
            # print(f"\n🎯 ECUACIÓN 5 - VELOCIDAD MÁS PROBABLE:")
            # print(f"   v_mp = c × ((k-1)/k)^(1/k)")
            # print(f"   ")
            
            if k > 1:
                numerador = k - 1
                cociente = numerador / k
                exponente = 1 / k
                potencia = np.power(cociente, exponente)
                v_mp = c * potencia
                
                # print(f"   Paso 1: k - 1 = {k:.4f} - 1 = {numerador:.4f}")
                # print(f"   Paso 2: (k-1)/k = {numerador:.4f}/{k:.4f} = {cociente:.4f}")
                # print(f"   Paso 3: 1/k = 1/{k:.4f} = {exponente:.4f}")
                # print(f"   Paso 4: ((k-1)/k)^(1/k) = ({cociente:.4f})^({exponente:.4f}) = {potencia:.4f}")
                # print(f"   Paso 5: v_mp = c × {potencia:.4f} = {c:.4f} × {potencia:.4f} = {v_mp:.4f} m/s")
                # print(f"   ")
                # print(f"   ✅ VELOCIDAD MÁS PROBABLE: {v_mp:.4f} m/s")
            else:
                v_mp = 0
                # print(f"   ⚠️ Para k ≤ 1: v_mp = 0 m/s (función monótona decreciente)")
            
            # ECUACIÓN 6: Velocidad de máxima energía
            # print(f"\n⚡ ECUACIÓN 6 - VELOCIDAD DE MÁXIMA ENERGÍA:")
            # print(f"   v_maxE = c × ((k+2)/k)^(1/k)")
            # print(f"   ")
            
            numerador_E = k + 2
            cociente_E = numerador_E / k
            exponente_E = 1 / k
            potencia_E = np.power(cociente_E, exponente_E)
            v_maxE = c * potencia_E
            
            # print(f"   Paso 1: k + 2 = {k:.4f} + 2 = {numerador_E:.4f}")
            # print(f"   Paso 2: (k+2)/k = {numerador_E:.4f}/{k:.4f} = {cociente_E:.4f}")
            # print(f"   Paso 3: 1/k = 1/{k:.4f} = {exponente_E:.4f}")
            # print(f"   Paso 4: ((k+2)/k)^(1/k) = ({cociente_E:.4f})^({exponente_E:.4f}) = {potencia_E:.4f}")
            # print(f"   Paso 5: v_maxE = c × {potencia_E:.4f} = {c:.4f} × {potencia_E:.4f} = {v_maxE:.4f} m/s")
            # print(f"   ")
            # print(f"   ✅ VELOCIDAD DE MÁXIMA ENERGÍA: {v_maxE:.4f} m/s")
            
            # Guardar resultados
            velocidades_caracteristicas[ciudad] = {
                'v_media': v_promedio,
                'v_probable': v_mp,
                'v_maxE': v_maxE,
                'k': k,
                'c': c
            }
            
            # print(f"\n📋 RESUMEN:")
            # print(f"   • Velocidad media: {v_promedio:.2f} m/s")
            # print(f"   • Velocidad más probable: {v_mp:.2f} m/s")
            # print(f"   • Velocidad de máxima energía: {v_maxE:.2f} m/s")
        
        # Comparación entre ciudades
        self.comparar_potencial_eolico(velocidades_caracteristicas)
        
        return velocidades_caracteristicas
    
    def comparar_potencial_eolico(self, velocidades_caracteristicas):
        """Comparar potencial eólico entre ciudades"""
        # print(f"\n🔍 COMPARACIÓN DE POTENCIAL EÓLICO")
        # print("=" * 40)
        
        ciudad1, ciudad2 = self.ciudades_seleccionadas
        
        # print(f"\n📊 TABLA COMPARATIVA:")
        # print("-" * 75)
        # print(f"{'Ciudad':<12} {'V.Media':<10} {'V.Probable':<12} {'V.MaxEnergía':<13} {'k':<8} {'c'}")
        # print("-" * 75)
        
        for ciudad in self.ciudades_seleccionadas:
            datos = velocidades_caracteristicas[ciudad]
            # print(f"{ciudad:<12} {datos['v_media']:<10.2f} {datos['v_probable']:<12.2f} "
            #       f"{datos['v_maxE']:<13.2f} {datos['k']:<8.2f} {datos['c']:.2f}")
        
        # Determinar ciudad con mayor potencial
        v_maxE_1 = velocidades_caracteristicas[ciudad1]['v_maxE']
        v_maxE_2 = velocidades_caracteristicas[ciudad2]['v_maxE']
        
        if v_maxE_1 > v_maxE_2:
            ciudad_mayor = ciudad1
            v_mayor = v_maxE_1
            v_menor = v_maxE_2
        else:
            ciudad_mayor = ciudad2
            v_mayor = v_maxE_2
            v_menor = v_maxE_1
        
        diferencia_abs = v_mayor - v_menor
        diferencia_rel = (diferencia_abs / v_menor) * 100
        
        # print(f"\n🎯 ANÁLISIS DE POTENCIAL EÓLICO:")
        # print(f"   1. Velocidades de máxima energía:")
        # print(f"      • {ciudad1}: {v_maxE_1:.2f} m/s")
        # print(f"      • {ciudad2}: {v_maxE_2:.2f} m/s")
        # print(f"      • Diferencia: {diferencia_abs:.2f} m/s ({diferencia_rel:.1f}%)")
        
        # print(f"\n   2. ✅ CONCLUSIÓN:")
        # print(f"      {ciudad_mayor.upper()} tiene MAYOR POTENCIAL EÓLICO")
        
        # print(f"\n   3. 🔬 RAZONES:")
        # print(f"      • Mayor velocidad de máxima energía: {v_mayor:.2f} m/s")
        # print(f"      • La potencia eólica es proporcional a v³")
        
        # Cálculo aproximado de potencia relativa
        potencia_relativa = (v_mayor / v_menor) ** 3
        # print(f"      • Potencia relativa aproximada: ({v_mayor:.2f}/{v_menor:.2f})³ = {potencia_relativa:.2f}x")
        # print(f"      • {ciudad_mayor} podría generar ~{potencia_relativa:.1f} veces más energía")
    
    def actividad_5_cuartiles_y_rango(self, resultados_weibull):
        """SEMANA 5 - ACTIVIDAD 5: Cuartiles y rango intercuartílico"""
        # print(f"\n" + "🔥" * 70)
        # print("SEMANA 5 - ACTIVIDAD 5: CUARTILES Y RANGO INTERCUARTÍLICO")
        # print("🔥" * 70)
        
        resultados_cuartiles = {}
        
        for ciudad in self.ciudades_seleccionadas:
            # print(f"\n" + "="*60)
            # print(f"📊 ANÁLISIS PARA {ciudad.upper()}")
            # print("="*60)
            
            resultado = resultados_weibull[ciudad]
            k = resultado['k']
            c = resultado['c']
            
            # print(f"📐 FÓRMULA PARA PERCENTILES WEIBULL:")
            # print(f"   v_p = c × (-ln(1-p))^(1/k)")
            # print(f"   Donde: k = {k:.4f}, c = {c:.4f} m/s")
            # print(f"")
            
            # Cuartil 1 (percentil 25%)
            # print(f"🔢 CÁLCULO DEL CUARTIL 1 (Q1 - percentil 25%):")
            p1 = 0.25
            
            # print(f"   Paso 1: p = 0.25 (percentil 25%)")
            # print(f"   Paso 2: 1 - p = 1 - 0.25 = 0.75")
            
            ln_term_1 = -np.log(1 - p1)
            # print(f"   Paso 3: -ln(1-p) = -ln(0.75) = {ln_term_1:.4f}")
            
            exp_term_1 = 1/k
            # print(f"   Paso 4: 1/k = 1/{k:.4f} = {exp_term_1:.4f}")
            
            power_result_1 = np.power(ln_term_1, exp_term_1)
            # print(f"   Paso 5: (-ln(1-p))^(1/k) = ({ln_term_1:.4f})^({exp_term_1:.4f}) = {power_result_1:.4f}")
            
            Q1 = c * power_result_1
            # print(f"   Paso 6: Q1 = c × {power_result_1:.4f} = {c:.4f} × {power_result_1:.4f} = {Q1:.4f} m/s")
            # print(f"   ")
            # print(f"   ✅ CUARTIL 1: Q1 = {Q1:.4f} m/s")
            
            # Cuartil 3 (percentil 75%)
            # print(f"\n🔢 CÁLCULO DEL CUARTIL 3 (Q3 - percentil 75%):")
            p3 = 0.75
            
            # print(f"   Paso 1: p = 0.75 (percentil 75%)")
            # print(f"   Paso 2: 1 - p = 1 - 0.75 = 0.25")
            
            ln_term_3 = -np.log(1 - p3)
            # print(f"   Paso 3: -ln(1-p) = -ln(0.25) = {ln_term_3:.4f}")
            
            exp_term_3 = 1/k
            # print(f"   Paso 4: 1/k = 1/{k:.4f} = {exp_term_3:.4f}")
            
            power_result_3 = np.power(ln_term_3, exp_term_3)
            # print(f"   Paso 5: (-ln(1-p))^(1/k) = ({ln_term_3:.4f})^({exp_term_3:.4f}) = {power_result_3:.4f}")
            
            Q3 = c * power_result_3
            # print(f"   Paso 6: Q3 = c × {power_result_3:.4f} = {c:.4f} × {power_result_3:.4f} = {Q3:.4f} m/s")
            # print(f"   ")
            # print(f"   ✅ CUARTIL 3: Q3 = {Q3:.4f} m/s")
            
            # Rango intercuartílico
            IQR = Q3 - Q1
            # print(f"\n📏 CÁLCULO DEL RANGO INTERCUARTÍLICO:")
            # print(f"   IQR = Q3 - Q1 = {Q3:.4f} - {Q1:.4f} = {IQR:.4f} m/s")
            # print(f"   ")
            # print(f"   ✅ RANGO INTERCUARTÍLICO: IQR = {IQR:.4f} m/s")
            
            # Tabla resumen
            # print(f"\n📋 TABLA RESUMEN:")
            # print(f"   +------------------+------------+")
            # print(f"   | Estadístico      | Valor      |")
            # print(f"   +------------------+------------+")
            # print(f"   | Q1 (25%)         | {Q1:8.2f} m/s |")
            # print(f"   | Q3 (75%)         | {Q3:8.2f} m/s |")
            # print(f"   | IQR              | {IQR:8.2f} m/s |")
            # print(f"   +------------------+------------+")
            # print(f"   El 50% central de los datos está entre {Q1:.2f} y {Q3:.2f} m/s")
            
            resultados_cuartiles[ciudad] = {
                'Q1': Q1,
                'Q3': Q3,
                'IQR': IQR,
                'k': k,
                'c': c
            }
        
        return resultados_cuartiles
    
    def actividad_6_probabilidad_entre_cuartiles(self, resultados_weibull):
        """SEMANA 5 - ACTIVIDAD 6: Probabilidad entre cuartiles usando F(v)"""
        # print(f"\n" + "🔥" * 70)
        # print("SEMANA 5 - ACTIVIDAD 6: PROBABILIDAD ENTRE CUARTILES")
        # print("🔥" * 70)
        
        # Primero calcular cuartiles
        resultados_cuartiles = self.actividad_5_cuartiles_y_rango(resultados_weibull)
        
        for ciudad in self.ciudades_seleccionadas:
            # print(f"\n" + "="*60)
            # print(f"📈 ANÁLISIS PARA {ciudad.upper()}")
            # print("="*60)
            
            cuartiles = resultados_cuartiles[ciudad]
            Q1 = cuartiles['Q1']
            Q3 = cuartiles['Q3']
            k = cuartiles['k']
            c = cuartiles['c']
            
            # print(f"📐 FUNCIÓN DE DISTRIBUCIÓN ACUMULADA WEIBULL:")
            # print(f"   F(v) = 1 - e^(-(v/c)^k)")
            # print(f"   Donde: k = {k:.4f}, c = {c:.4f} m/s")
            # print(f"   Q1 = {Q1:.4f} m/s, Q3 = {Q3:.4f} m/s")
            # print(f"")
            
            # Cálculo de F(Q1)
            # print(f"🔢 CÁLCULO PASO A PASO DE F(Q1):")
            ratio_Q1 = Q1/c
            # print(f"   Paso 1: v/c = Q1/c = {Q1:.4f}/{c:.4f} = {ratio_Q1:.4f}")
            
            power_Q1 = np.power(ratio_Q1, k)
            # print(f"   Paso 2: (v/c)^k = ({ratio_Q1:.4f})^{k:.4f} = {power_Q1:.4f}")
            
            exp_Q1 = np.exp(-power_Q1)
            # print(f"   Paso 3: e^(-(v/c)^k) = e^(-{power_Q1:.4f}) = {exp_Q1:.4f}")
            
            F_Q1 = 1 - exp_Q1
            # print(f"   Paso 4: F(Q1) = 1 - {exp_Q1:.4f} = {F_Q1:.4f}")
            # print(f"   ")
            # print(f"   ✅ F(Q1) = {F_Q1:.4f}")
            
            # Cálculo de F(Q3)
            # print(f"\n🔢 CÁLCULO PASO A PASO DE F(Q3):")
            ratio_Q3 = Q3/c
            # print(f"   Paso 1: v/c = Q3/c = {Q3:.4f}/{c:.4f} = {ratio_Q3:.4f}")
            
            power_Q3 = np.power(ratio_Q3, k)
            # print(f"   Paso 2: (v/c)^k = ({ratio_Q3:.4f})^{k:.4f} = {power_Q3:.4f}")
            
            exp_Q3 = np.exp(-power_Q3)
            # print(f"   Paso 3: e^(-(v/c)^k) = e^(-{power_Q3:.4f}) = {exp_Q3:.4f}")
            
            F_Q3 = 1 - exp_Q3
            # print(f"   Paso 4: F(Q3) = 1 - {exp_Q3:.4f} = {F_Q3:.4f}")
            # print(f"   ")
            # print(f"   ✅ F(Q3) = {F_Q3:.4f}")
            
            # Probabilidad entre cuartiles
            prob_entre_cuartiles = F_Q3 - F_Q1
            porcentaje = prob_entre_cuartiles * 100
            
            # print(f"\n🎯 CÁLCULO FINAL DE LA PROBABILIDAD:")
            # print(f"   P(Q1 ≤ V ≤ Q3) = F(Q3) - F(Q1)")
            # print(f"   P({Q1:.2f} ≤ V ≤ {Q3:.2f}) = {F_Q3:.4f} - {F_Q1:.4f}")
            # print(f"   P({Q1:.2f} ≤ V ≤ {Q3:.2f}) = {prob_entre_cuartiles:.4f}")
            # print(f"   P({Q1:.2f} ≤ V ≤ {Q3:.2f}) = {porcentaje:.2f}%")
            
            # print(f"\n📋 TABLA RESUMEN:")
            # print(f"   +------------------+------------+")
            # print(f"   | Función          | Valor      |")
            # print(f"   +------------------+------------+")
            # print(f"   | F(Q1)            | {F_Q1:8.4f}   |")
            # print(f"   | F(Q3)            | {F_Q3:8.4f}   |")
            # print(f"   | P(Q1≤V≤Q3)       | {prob_entre_cuartiles:8.4f}   |")
            # print(f"   | Porcentaje       | {porcentaje:8.2f}%  |")
            # print(f"   +------------------+------------+")
            
            # print(f"\n✅ INTERPRETACIÓN:")
            # print(f"   La probabilidad de que la velocidad del viento esté entre")
            # print(f"   {Q1:.2f} m/s y {Q3:.2f} m/s es del {porcentaje:.2f}%")
            # print(f"   (Por definición, esto siempre debe ser 50% para cualquier distribución)")
    
    def actividad_7_probabilidad_percentil60(self, resultados_weibull):
        """SEMANA 5 - ACTIVIDAD 7: Probabilidad superior al percentil 60"""
        # print(f"\n" + "🔥" * 70)
        # print("SEMANA 5 - ACTIVIDAD 7: PROBABILIDAD SUPERIOR AL PERCENTIL 60")
        # print("🔥" * 70)
        
        for ciudad in self.ciudades_seleccionadas:
            # print(f"\n" + "="*60)
            # print(f"⚡ ANÁLISIS PARA {ciudad.upper()}")
            # print("="*60)
            
            resultado = resultados_weibull[ciudad]
            k = resultado['k']
            c = resultado['c']
            
            # print(f"📊 PARÁMETROS:")
            # print(f"   • k = {k:.4f}")
            # print(f"   • c = {c:.4f} m/s")
            # print(f"")
            
            # Calcular percentil 60
            # print(f"📐 CÁLCULO PASO A PASO DEL PERCENTIL 60:")
            p60 = 0.60
            
            # print(f"   Paso 1: p = 0.60 (percentil 60%)")
            # print(f"   Paso 2: 1 - p = 1 - 0.60 = 0.40")
            
            ln_term = -np.log(1 - p60)
            # print(f"   Paso 3: -ln(1-p) = -ln(0.40) = {ln_term:.4f}")
            
            exp_term = 1/k
            # print(f"   Paso 4: 1/k = 1/{k:.4f} = {exp_term:.4f}")
            
            power_result = np.power(ln_term, exp_term)
            # print(f"   Paso 5: (-ln(1-p))^(1/k) = ({ln_term:.4f})^({exp_term:.4f}) = {power_result:.4f}")
            
            percentil_60 = c * power_result
            # print(f"   Paso 6: v_60 = c × {power_result:.4f} = {c:.4f} × {power_result:.4f} = {percentil_60:.4f} m/s")
            # print(f"   ")
            # print(f"   ✅ PERCENTIL 60: v_60 = {percentil_60:.4f} m/s")
            
            # Calcular F(percentil_60)
            # print(f"\n📈 CÁLCULO PASO A PASO DE F(v_60):")
            ratio_p60 = percentil_60/c
            # print(f"   Paso 1: v/c = {percentil_60:.4f}/{c:.4f} = {ratio_p60:.4f}")
            
            power_p60 = np.power(ratio_p60, k)
            # print(f"   Paso 2: (v/c)^k = ({ratio_p60:.4f})^{k:.4f} = {power_p60:.4f}")
            
            exp_p60 = np.exp(-power_p60)
            # print(f"   Paso 3: e^(-(v/c)^k) = e^(-{power_p60:.4f}) = {exp_p60:.4f}")
            
            F_p60 = 1 - exp_p60
            # print(f"   Paso 4: F(v_60) = 1 - {exp_p60:.4f} = {F_p60:.4f}")
            # print(f"   ")
            # print(f"   ✅ F(v_60) = {F_p60:.4f}")
            
            # Probabilidad superior
            prob_superior_p60 = 1 - F_p60
            porcentaje_superior = prob_superior_p60 * 100
            
            # print(f"\n🎯 CÁLCULO DE LA PROBABILIDAD SUPERIOR:")
            # print(f"   P(V > v_60) = 1 - F(v_60)")
            # print(f"   P(V > {percentil_60:.4f}) = 1 - {F_p60:.4f}")
            # print(f"   P(V > {percentil_60:.4f}) = {prob_superior_p60:.4f}")
            # print(f"   P(V > {percentil_60:.4f}) = {porcentaje_superior:.2f}%")
            
            # print(f"\n📋 TABLA RESUMEN:")
            # print(f"   +------------------+------------+")
            # print(f"   | Concepto         | Valor      |")
            # print(f"   +------------------+------------+")
            # print(f"   | Percentil 60     | {percentil_60:8.2f} m/s |")
            # print(f"   | F(P60)           | {F_p60:8.4f}   |")
            # print(f"   | P(V > P60)       | {prob_superior_p60:8.4f}   |")
            # print(f"   | Porcentaje       | {porcentaje_superior:8.2f}%  |")
            # print(f"   +------------------+------------+")
            
            # print(f"\n✅ INTERPRETACIÓN:")
            # print(f"   La probabilidad de registrar velocidades superiores a")
            # print(f"   {percentil_60:.2f} m/s (percentil 60) es del {porcentaje_superior:.2f}%")
            # print(f"   (Por definición, esto siempre debe ser 40% para cualquier distribución)")
            # print(f"   Esto significa que el {porcentaje_superior:.0f}% de las observaciones")
            # print(f"   superan esta velocidad de referencia.")

    def ejecutar_aplicacion_completa(self):
        """Ejecutar la aplicación completa paso a paso"""
        # Inicio
        self.mostrar_bienvenida()
        
        # Cargar datos
        if not self.cargar_datos():
            return False
        
        # Selección interactiva
        if not self.seleccionar_ciudades_interactivo():
            return False
        
        # Extraer datos
        self.extraer_datos_ciudades()
        
        # Actividades
        # print(f"\n🚀 INICIANDO ANÁLISIS COMPLETO...")
        
        # Semana 3
        ciudad_mayor_var = self.actividad_1_histogramas_y_variabilidad()
        resultados_weibull = self.actividad_2_parametros_weibull()
        
        # Semana 4
        self.actividad_3_graficar_distribucion(resultados_weibull)
        velocidades_caracteristicas = self.actividad_4_velocidades_caracteristicas(resultados_weibull)
        
        # Semana 5
        self.actividad_5_cuartiles_y_rango(resultados_weibull)
        self.actividad_6_probabilidad_entre_cuartiles(resultados_weibull)
        self.actividad_7_probabilidad_percentil60(resultados_weibull)
        
        # Mostrar resumen final
        self.mostrar_resumen_final(ciudad_mayor_var, velocidades_caracteristicas)
        
        return True
    
    def mostrar_resumen_final(self, ciudad_mayor_var, velocidades_caracteristicas, modo_demo=False):
        """Mostrar resumen final del análisis"""
        # print(f"\n" + "🎉" * 70)
        # print("RESUMEN FINAL DEL ANÁLISIS")
        # print("🎉" * 70)
        
        ciudad1, ciudad2 = self.ciudades_seleccionadas
        
        # print(f"\n🏙️ CIUDADES ANALIZADAS:")
        # print(f"   1️⃣ {ciudad1}")
        # print(f"   2️⃣ {ciudad2}")
        
        # print(f"\n📊 RESULTADOS PRINCIPALES:")
        # print(f"   • Mayor variabilidad: {ciudad_mayor_var}")
        
        # Determinar mejor ciudad para energía eólica
        v_maxE_1 = velocidades_caracteristicas[ciudad1]['v_maxE']
        v_maxE_2 = velocidades_caracteristicas[ciudad2]['v_maxE']
        mejor_eolica = ciudad1 if v_maxE_1 > v_maxE_2 else ciudad2
        
        # print(f"   • Mejor potencial eólico: {mejor_eolica}")
        
        # print(f"\n✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        # print(f"   📈 Todas las gráficas generadas")
        # print(f"   🧮 Todos los cálculos realizados paso a paso")
        # print(f"   📚 Explicaciones educativas incluidas")
        
        # Preguntar si generar PDF solo si no es modo demo
        if not modo_demo:
            # print(f"\n" + "="*60)
            respuesta_pdf = input("¿Deseas generar un reporte PDF del análisis? (s/n): ").lower().strip()
            
            if respuesta_pdf in ['s', 'si', 'sí', 'y', 'yes']:
                archivo_pdf = self.generar_reporte_pdf()
                if archivo_pdf:
                    # print(f"\n🎉 ¡Reporte PDF generado exitosamente!")
                    # print(f"   Puedes encontrarlo en: {archivo_pdf}")
            else:
                # print(f"\n📋 Reporte PDF no generado")

    def generar_reporte_pdf(self, nombre_archivo=None):
        """
        Genera un reporte PDF completo del análisis
        
        Args:
            nombre_archivo: Nombre del archivo PDF (opcional)
        """
        if not self.ciudades_seleccionadas:
            # print("❌ No hay ciudades seleccionadas para generar el reporte")
            return None
            
        if nombre_archivo is None:
            fecha_actual = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            ciudades_str = "_".join(self.ciudades_seleccionadas)
            nombre_archivo = f"reporte_weibull_{ciudades_str}_{fecha_actual}.pdf"
        
        try:
            # print(f"\n📄 GENERANDO REPORTE PDF...")
            # print("="*60)
            
            # Crear el generador de PDF
            generador = GeneradorPDFWeibull(
                datos=self.datos,
                ciudades_seleccionadas=self.ciudades_seleccionadas,
                resultados_analisis=self.resultados
            )
            
            # Generar el reporte
            archivo_generado = generador.generar_reporte_completo(nombre_archivo)
            
            # print(f"✅ Reporte PDF generado exitosamente:")
            # print(f"   📁 Archivo: {archivo_generado}")
            # print(f"   📍 Ubicación: {os.path.abspath(archivo_generado)}")
            
            return archivo_generado
            
        except Exception as e:
            # print(f"❌ Error al generar el PDF: {str(e)}")
            return None


def main():
    """Función principal"""
    try:
        # print("Iniciando aplicación...")
        analizador = AnalisisWeibullEducativo("Datos.xlsx")
        
        if analizador.ejecutar_aplicacion_completa():
            # print(f"\n🎊 ¡ANÁLISIS FINALIZADO CON ÉXITO!")
        else:
            # print(f"\n❌ Error durante la ejecución")
            
    except KeyboardInterrupt:
        # print(f"\n⚠️ Aplicación interrumpida por el usuario")
    except Exception as e:
        # print(f"\n❌ Error inesperado: {str(e)}")


if __name__ == "__main__":
    main()