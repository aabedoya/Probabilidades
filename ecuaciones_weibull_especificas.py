"""
Implementación Específica de las Ecuaciones de Weibull para Velocidad del Viento
================================================================================

Este script implementa las ecuaciones específicas mencionadas en el proyecto:

Ecuación 1: f(v) = (k/λ) * (v/λ)^(k-1) * e^(-(v/λ)^k)
Ecuación 2: F(v) = 1 - e^(-(v/λ)^k) 
Ecuación 3: k = (σ/v̅)^(-1.09)
Ecuación 4: c = v̅ / Γ(1+1/k)
Ecuación 5: v_mp = c * ((k-1)/k)^(1/k)
Ecuación 6: v_MAXE = c * ((k+2)/k)^(1/k)

Donde:
- v̅: promedio de velocidad del viento (m/s)
- σ: desviación estándar de velocidad del viento
- k: parámetro de forma de la distribución
- c: parámetro de escala de la distribución (equivalente a λ)
- v_mp: velocidad del viento más probable
- v_MAXE: velocidad del viento que entrega máxima energía eólica

Autor: Proyecto Probabilidades
Fecha: 3 de septiembre de 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import gamma
from typing import Tuple, Dict, List
import seaborn as sns

# Configurar estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class EcuacionesWeibullViento:
    """
    Implementación específica de las ecuaciones de Weibull para análisis de viento
    """
    
    def __init__(self):
        self.datos_procesados = {}
    
    def ecuacion_1_pdf(self, v: np.ndarray, k: float, c: float) -> np.ndarray:
        """
        Ecuación 1: Función de densidad de probabilidad de Weibull
        
        f(v) = (k/c) * (v/c)^(k-1) * e^(-(v/c)^k)
        
        Parameters:
        -----------
        v : np.ndarray
            Velocidades del viento (m/s)
        k : float
            Parámetro de forma
        c : float
            Parámetro de escala (m/s)
            
        Returns:
        --------
        np.ndarray
            Valores de la función de densidad
        """
        # Evitar división por cero y valores negativos
        v = np.maximum(v, 1e-10)
        
        # f(v) = (k/c) * (v/c)^(k-1) * e^(-(v/c)^k)
        termino1 = k / c
        termino2 = np.power(v / c, k - 1)
        termino3 = np.exp(-np.power(v / c, k))
        
        return termino1 * termino2 * termino3
    
    def ecuacion_2_cdf(self, v: np.ndarray, k: float, c: float) -> np.ndarray:
        """
        Ecuación 2: Función de distribución acumulativa de Weibull
        
        F(v) = 1 - e^(-(v/c)^k)
        
        Parameters:
        -----------
        v : np.ndarray
            Velocidades del viento (m/s)
        k : float
            Parámetro de forma
        c : float
            Parámetro de escala (m/s)
            
        Returns:
        --------
        np.ndarray
            Valores de la función de distribución acumulativa
        """
        # F(v) = 1 - e^(-(v/c)^k)
        return 1 - np.exp(-np.power(v / c, k))
    
    def ecuacion_3_parametro_k(self, v_promedio: float, sigma: float) -> float:
        """
        Ecuación 3: Cálculo del parámetro de forma k
        
        k = (σ/v̅)^(-1.09)
        
        Parameters:
        -----------
        v_promedio : float
            Velocidad promedio del viento (m/s)
        sigma : float
            Desviación estándar de la velocidad del viento (m/s)
            
        Returns:
        --------
        float
            Parámetro de forma k
        """
        coeficiente_variacion = sigma / v_promedio
        
        # k = (σ/v̅)^(-1.09)
        k = np.power(coeficiente_variacion, -1.09)
        
        return k
    
    def ecuacion_4_parametro_c(self, v_promedio: float, k: float) -> float:
        """
        Ecuación 4: Cálculo del parámetro de escala c
        
        c = v̅ / Γ(1+1/k)
        
        Parameters:
        -----------
        v_promedio : float
            Velocidad promedio del viento (m/s)
        k : float
            Parámetro de forma
            
        Returns:
        --------
        float
            Parámetro de escala c (m/s)
        """
        # c = v̅ / Γ(1+1/k)
        c = v_promedio / gamma(1 + 1/k)
        
        return c
    
    def ecuacion_5_velocidad_mas_probable(self, k: float, c: float) -> float:
        """
        Ecuación 5: Velocidad del viento más probable
        
        v_mp = c * ((k-1)/k)^(1/k)
        
        Parameters:
        -----------
        k : float
            Parámetro de forma
        c : float
            Parámetro de escala (m/s)
            
        Returns:
        --------
        float
            Velocidad más probable (m/s)
        """
        if k <= 1:
            return 0.0  # Para k ≤ 1, la moda está en v = 0
        
        # v_mp = c * ((k-1)/k)^(1/k)
        v_mp = c * np.power((k - 1) / k, 1 / k)
        
        return v_mp
    
    def ecuacion_6_velocidad_maxima_energia(self, k: float, c: float) -> float:
        """
        Ecuación 6: Velocidad de máxima energía eólica
        
        v_MAXE = c * ((k+2)/k)^(1/k)
        
        Parameters:
        -----------
        k : float
            Parámetro de forma
        c : float
            Parámetro de escala (m/s)
            
        Returns:
        --------
        float
            Velocidad de máxima energía (m/s)
        """
        # v_MAXE = c * ((k+2)/k)^(1/k)
        v_MAXE = c * np.power((k + 2) / k, 1 / k)
        
        return v_MAXE
    
    def procesar_datos_ciudad(self, velocidades, nombre_ciudad: str) -> Dict:
        """
        Procesar datos de una ciudad aplicando todas las ecuaciones
        
        Parameters:
        -----------
        velocidades : array-like
            Array con velocidades del viento observadas
        nombre_ciudad : str
            Nombre de la ciudad
            
        Returns:
        --------
        Dict
            Diccionario con todos los resultados calculados
        """
        # Convertir a numpy array y estadísticas básicas de los datos observados
        velocidades = np.asarray(velocidades)
        v_promedio = float(np.mean(velocidades))
        sigma = float(np.std(velocidades, ddof=1))
        v_min = np.min(velocidades)
        v_max = np.max(velocidades)
        n_datos = len(velocidades)
        
        print(f"\n{'='*60}")
        print(f"📍 ANÁLISIS PARA: {nombre_ciudad.upper()}")
        print(f"{'='*60}")
        print(f"📊 Datos observados:")
        print(f"   • Número de observaciones: {n_datos}")
        print(f"   • Velocidad mínima: {v_min:.2f} m/s")
        print(f"   • Velocidad máxima: {v_max:.2f} m/s")
        print(f"   • Velocidad promedio (v̅): {v_promedio:.2f} m/s")
        print(f"   • Desviación estándar (σ): {sigma:.2f} m/s")
        print(f"   • Coeficiente de variación: {sigma/v_promedio:.3f}")
        
        # Aplicar ecuaciones secuencialmente
        print(f"\n🔬 APLICACIÓN DE ECUACIONES:")
        print(f"{'─'*40}")
        
        # Ecuación 3: Calcular k
        k = self.ecuacion_3_parametro_k(v_promedio, sigma)
        print(f"📐 Ecuación 3: k = (σ/v̅)^(-1.09)")
        print(f"   k = ({sigma:.2f}/{v_promedio:.2f})^(-1.09) = {k:.3f}")
        
        # Ecuación 4: Calcular c
        c = self.ecuacion_4_parametro_c(v_promedio, k)
        gamma_value = gamma(1 + 1/k)
        print(f"📐 Ecuación 4: c = v̅ / Γ(1+1/k)")
        print(f"   c = {v_promedio:.2f} / Γ(1+1/{k:.3f}) = {v_promedio:.2f} / {gamma_value:.3f} = {c:.2f} m/s")
        
        # Ecuación 5: Velocidad más probable
        v_mp = self.ecuacion_5_velocidad_mas_probable(k, c)
        print(f"📐 Ecuación 5: v_mp = c * ((k-1)/k)^(1/k)")
        if k > 1:
            ratio = (k-1)/k
            print(f"   v_mp = {c:.2f} * (({k:.3f}-1)/{k:.3f})^(1/{k:.3f})")
            print(f"   v_mp = {c:.2f} * ({ratio:.3f})^({1/k:.3f}) = {v_mp:.2f} m/s")
        else:
            print(f"   v_mp = 0.00 m/s (k ≤ 1)")
        
        # Ecuación 6: Velocidad de máxima energía
        v_MAXE = self.ecuacion_6_velocidad_maxima_energia(k, c)
        ratio_maxe = (k+2)/k
        print(f"📐 Ecuación 6: v_MAXE = c * ((k+2)/k)^(1/k)")
        print(f"   v_MAXE = {c:.2f} * (({k:.3f}+2)/{k:.3f})^(1/{k:.3f})")
        print(f"   v_MAXE = {c:.2f} * ({ratio_maxe:.3f})^({1/k:.3f}) = {v_MAXE:.2f} m/s")
        
        # Verificación: calcular media teórica y compararla con la observada
        v_media_teorica = c * gamma(1 + 1/k)
        print(f"\n✅ VERIFICACIÓN:")
        print(f"   • Media teórica: c * Γ(1+1/k) = {v_media_teorica:.2f} m/s")
        print(f"   • Media observada: {v_promedio:.2f} m/s")
        print(f"   • Diferencia: {abs(v_media_teorica - v_promedio):.4f} m/s")
        
        # Almacenar resultados
        resultados = {
            'nombre_ciudad': nombre_ciudad,
            'datos_originales': velocidades,
            'estadisticas_observadas': {
                'n_datos': n_datos,
                'v_min': v_min,
                'v_max': v_max,
                'v_promedio': v_promedio,
                'sigma': sigma,
                'coef_variacion': sigma/v_promedio
            },
            'parametros_weibull': {
                'k': k,
                'c': c
            },
            'velocidades_caracteristicas': {
                'v_mp': v_mp,
                'v_MAXE': v_MAXE,
                'v_media_teorica': v_media_teorica
            }
        }
        
        self.datos_procesados[nombre_ciudad] = resultados
        return resultados
    
    def graficar_ecuaciones_ciudad(self, nombre_ciudad: str, figsize: Tuple[int, int] = (16, 10)) -> None:
        """
        Crear gráficas detalladas mostrando las ecuaciones para una ciudad
        """
        if nombre_ciudad not in self.datos_procesados:
            print(f"❌ Error: No hay datos procesados para {nombre_ciudad}")
            return
        
        datos = self.datos_procesados[nombre_ciudad]
        velocidades_obs = datos['datos_originales']
        k = datos['parametros_weibull']['k']
        c = datos['parametros_weibull']['c']
        v_mp = datos['velocidades_caracteristicas']['v_mp']
        v_MAXE = datos['velocidades_caracteristicas']['v_MAXE']
        
        # Crear rango de velocidades para las curvas
        v_max_plot = min(25, np.max(velocidades_obs) * 1.3)
        v = np.linspace(0.1, v_max_plot, 1000)
        
        # Calcular las funciones usando las ecuaciones
        pdf_vals = self.ecuacion_1_pdf(v, k, c)
        cdf_vals = self.ecuacion_2_cdf(v, k, c)
        
        # Crear figura con subgráficas
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
        
        # 1. Histograma vs PDF (Ecuación 1)
        ax1.hist(velocidades_obs, bins=30, density=True, alpha=0.7, 
                color='lightblue', edgecolor='black', label='Datos observados')
        ax1.plot(v, pdf_vals, 'r-', linewidth=3, 
                label=f'PDF Weibull\n(Ecuación 1)')
        ax1.axvline(v_mp, color='green', linestyle='--', linewidth=2, 
                   label=f'v_mp = {v_mp:.1f} m/s')
        ax1.axvline(v_MAXE, color='purple', linestyle='-.', linewidth=2,
                   label=f'v_MAXE = {v_MAXE:.1f} m/s')
        
        ax1.set_title(f'Ecuación 1: f(v) = (k/c)·(v/c)^(k-1)·e^(-(v/c)^k)\n'
                     f'k = {k:.3f}, c = {c:.2f} m/s')
        ax1.set_xlabel('Velocidad del viento (m/s)')
        ax1.set_ylabel('Densidad de probabilidad')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. CDF (Ecuación 2)
        velocidades_ordenadas = np.sort(velocidades_obs)
        cdf_empirica = np.arange(1, len(velocidades_ordenadas) + 1) / len(velocidades_ordenadas)
        
        ax2.plot(velocidades_ordenadas, cdf_empirica, 'bo', markersize=2, alpha=0.6,
                label='CDF empírica')
        ax2.plot(v, cdf_vals, 'r-', linewidth=3, 
                label='CDF Weibull\n(Ecuación 2)')
        ax2.axvline(v_mp, color='green', linestyle='--', alpha=0.7)
        ax2.axvline(v_MAXE, color='purple', linestyle='-.', alpha=0.7)
        
        ax2.set_title(f'Ecuación 2: F(v) = 1 - e^(-(v/c)^k)')
        ax2.set_xlabel('Velocidad del viento (m/s)')
        ax2.set_ylabel('Probabilidad acumulada')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Densidad de potencia eólica (proporcional a v³)
        potencia_densidad = 0.5 * 1.225 * v**3  # W/m² (ρ = 1.225 kg/m³)
        potencia_ponderada = potencia_densidad * pdf_vals
        
        ax3.plot(v, potencia_ponderada, 'g-', linewidth=3, label='Densidad de potencia\nponderada')
        ax3.axvline(v_mp, color='green', linestyle='--', linewidth=2,
                   label=f'v_mp = {v_mp:.1f} m/s')
        ax3.axvline(v_MAXE, color='purple', linestyle='-.', linewidth=2,
                   label=f'v_MAXE = {v_MAXE:.1f} m/s')
        
        # Marcar el máximo de potencia ponderada
        idx_max_potencia = np.argmax(potencia_ponderada)
        v_max_potencia_real = v[idx_max_potencia]
        ax3.axvline(v_max_potencia_real, color='red', linestyle=':', linewidth=2,
                   label=f'v_máx_real = {v_max_potencia_real:.1f} m/s')
        
        ax3.set_title('Densidad de Potencia Eólica Ponderada\nP(v) × f(v)')
        ax3.set_xlabel('Velocidad del viento (m/s)')
        ax3.set_ylabel('Densidad de potencia ponderada')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Comparación de velocidades características
        velocidades_caract = {
            'v_promedio': datos['estadisticas_observadas']['v_promedio'],
            'v_mp (Ec.5)': v_mp,
            'v_MAXE (Ec.6)': v_MAXE,
            'v_mediana': c * np.power(np.log(2), 1/k)
        }
        
        nombres = list(velocidades_caract.keys())
        valores = list(velocidades_caract.values())
        colores = ['blue', 'green', 'purple', 'orange']
        
        bars = ax4.bar(nombres, valores, color=colores, alpha=0.7, edgecolor='black')
        
        # Añadir valores sobre las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{valor:.1f} m/s', ha='center', va='bottom', fontweight='bold')
        
        ax4.set_title('Velocidades Características Calculadas')
        ax4.set_ylabel('Velocidad (m/s)')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.suptitle(f'Análisis Completo con Ecuaciones de Weibull - {nombre_ciudad}', 
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def comparar_ciudades_ecuaciones(self, figsize: Tuple[int, int] = (16, 8)) -> None:
        """
        Comparar resultados de las ecuaciones entre ciudades
        """
        if len(self.datos_procesados) < 2:
            print("❌ Error: Se necesitan al menos 2 ciudades para comparar")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
        
        ciudades = list(self.datos_procesados.keys())
        colores = ['blue', 'red', 'green', 'orange', 'purple']
        
        # Datos para comparación
        params_k = []
        params_c = []
        v_mp_vals = []
        v_MAXE_vals = []
        v_promedio_vals = []
        
        for ciudad in ciudades:
            datos = self.datos_procesados[ciudad]
            params_k.append(datos['parametros_weibull']['k'])
            params_c.append(datos['parametros_weibull']['c'])
            v_mp_vals.append(datos['velocidades_caracteristicas']['v_mp'])
            v_MAXE_vals.append(datos['velocidades_caracteristicas']['v_MAXE'])
            v_promedio_vals.append(datos['estadisticas_observadas']['v_promedio'])
        
        # 1. Comparación de parámetros k y c
        x = np.arange(len(ciudades))
        width = 0.35
        
        ax1_twin = ax1.twinx()
        bars1 = ax1.bar(x - width/2, params_k, width, label='k (forma)', 
                       color='skyblue', alpha=0.8)
        bars2 = ax1_twin.bar(x + width/2, params_c, width, label='c (escala)', 
                           color='lightcoral', alpha=0.8)
        
        ax1.set_xlabel('Ciudad')
        ax1.set_ylabel('Parámetro k', color='blue')
        ax1_twin.set_ylabel('Parámetro c (m/s)', color='red')
        ax1.set_title('Ecuaciones 3 y 4: Parámetros de Weibull')
        ax1.set_xticks(x)
        ax1.set_xticklabels(ciudades, rotation=45)
        
        # Añadir valores sobre las barras
        for i, (k, c) in enumerate(zip(params_k, params_c)):
            ax1.text(i - width/2, k + 0.05, f'{k:.2f}', ha='center', va='bottom')
            ax1_twin.text(i + width/2, c + 0.1, f'{c:.2f}', ha='center', va='bottom')
        
        # 2. Comparación de velocidades características
        ax2.bar(x - width, v_promedio_vals, width, label='v̅ (observada)', 
               color='lightgreen', alpha=0.8)
        ax2.bar(x, v_mp_vals, width, label='v_mp (Ec. 5)', 
               color='gold', alpha=0.8)
        ax2.bar(x + width, v_MAXE_vals, width, label='v_MAXE (Ec. 6)', 
               color='plum', alpha=0.8)
        
        ax2.set_xlabel('Ciudad')
        ax2.set_ylabel('Velocidad (m/s)')
        ax2.set_title('Ecuaciones 5 y 6: Velocidades Características')
        ax2.set_xticks(x)
        ax2.set_xticklabels(ciudades, rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. PDFs comparativas
        v_max_global = 20
        v = np.linspace(0.1, v_max_global, 1000)
        
        for i, ciudad in enumerate(ciudades):
            datos = self.datos_procesados[ciudad]
            k = datos['parametros_weibull']['k']
            c = datos['parametros_weibull']['c']
            
            pdf_vals = self.ecuacion_1_pdf(v, k, c)
            ax3.plot(v, pdf_vals, color=colores[i % len(colores)], linewidth=2, 
                    label=f'{ciudad} (k={k:.2f}, c={c:.1f})')
        
        ax3.set_title('Comparación de PDFs (Ecuación 1)')
        ax3.set_xlabel('Velocidad del viento (m/s)')
        ax3.set_ylabel('Densidad de probabilidad')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Tabla de resultados
        ax4.axis('tight')
        ax4.axis('off')
        
        tabla_datos = []
        for i, ciudad in enumerate(ciudades):
            datos = self.datos_procesados[ciudad]
            tabla_datos.append([
                ciudad,
                f"{datos['parametros_weibull']['k']:.3f}",
                f"{datos['parametros_weibull']['c']:.2f}",
                f"{datos['velocidades_caracteristicas']['v_mp']:.2f}",
                f"{datos['velocidades_caracteristicas']['v_MAXE']:.2f}"
            ])
        
        tabla = ax4.table(cellText=tabla_datos,
                         colLabels=['Ciudad', 'k (Ec.3)', 'c (Ec.4)', 'v_mp (Ec.5)', 'v_MAXE (Ec.6)'],
                         cellLoc='center',
                         loc='center')
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.scale(1, 2)
        
        # Colorear encabezados
        for i in range(len(['Ciudad', 'k (Ec.3)', 'c (Ec.4)', 'v_mp (Ec.5)', 'v_MAXE (Ec.6)'])):
            tabla[(0, i)].set_facecolor('#40466e')
            tabla[(0, i)].set_text_props(weight='bold', color='white')
        
        ax4.set_title('Resumen de Resultados de las Ecuaciones')
        
        plt.suptitle('Comparación de Ecuaciones de Weibull entre Ciudades', 
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()


def ejemplo_completo_ecuaciones():
    """
    Ejemplo completo usando las ecuaciones específicas
    """
    print("🌪️ IMPLEMENTACIÓN DE ECUACIONES ESPECÍFICAS DE WEIBULL PARA VIENTO")
    print("=" * 70)
    
    # Crear instancia
    ecuaciones = EcuacionesWeibullViento()
    
    # Cargar datos
    try:
        datos = pd.read_excel("Datos.xlsx")
        ciudades_disponibles = [col for col in datos.columns if col != 'Dia']
        
        print(f"📊 Datos cargados: {datos.shape}")
        print(f"🏙️ Ciudades disponibles: {ciudades_disponibles}")
        
        # Procesar las dos primeras ciudades
        ciudades_seleccionadas = ciudades_disponibles[:2]
        
        for ciudad in ciudades_seleccionadas:
            velocidades = np.asarray(datos[ciudad].values)
            ecuaciones.procesar_datos_ciudad(velocidades, ciudad)
            
            # Crear gráficas individuales para cada ciudad
            ecuaciones.graficar_ecuaciones_ciudad(ciudad)
        
        # Comparar ciudades
        print(f"\n🔄 Comparando ciudades...")
        ecuaciones.comparar_ciudades_ecuaciones()
        
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo Datos.xlsx")
        print("Ejecute primero el script para crear datos de ejemplo")


if __name__ == "__main__":
    ejemplo_completo_ecuaciones()
