"""
Análisis de Velocidad del Viento con Distribución de Weibull
===========================================================

Este módulo implementa el análisis de velocidad del viento utilizando la distribución 
de Weibull con datos reales importados desde Excel. Calcula los parámetros k y c,
así como velocidades características importantes.

Ecuaciones implementadas:
- Ecuación 1: f(v) = (k/λ) * (v/λ)^(k-1) * e^(-(v/λ)^k)
- Ecuación 2: F(v) = 1 - e^(-(v/λ)^k)
- Ecuación 3: k = (σ/v̅)^(-1.09)
- Ecuación 4: c = v̅ / Γ(1+1/k)
- Ecuación 5: v_mp = c * ((k-1)/k)^(1/k)
- Ecuación 6: v_MAXE = c * ((k+2)/k)^(1/k)

Autor: Proyecto Probabilidades
Fecha: 3 de septiembre de 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import gamma
from scipy.optimize import minimize_scalar
from typing import Dict, List, Tuple, Optional
import warnings
from distribucion_weibull import DistribucionWeibull

# Configurar estilo de gráficas
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
warnings.filterwarnings('ignore')

class AnalisisVientoWeibull:
    """
    Clase para análisis de velocidad del viento usando distribución de Weibull
    con datos reales de múltiples ciudades
    """
    
    def __init__(self, archivo_datos: str = "Datos.xlsx"):
        """
        Inicializar el análisis con datos de Excel
        
        Parameters:
        -----------
        archivo_datos : str
            Ruta al archivo Excel con datos de velocidad del viento
        """
        self.archivo_datos = archivo_datos
        self.datos = None
        self.ciudades_seleccionadas = []
        self.parametros = {}
        self.distribuciones = {}
        self.resultados = {}
        
    def cargar_datos(self) -> pd.DataFrame:
        """
        Cargar datos desde el archivo Excel
        """
        try:
            self.datos = pd.read_excel(self.archivo_datos)
            print(f"✅ Datos cargados exitosamente desde {self.archivo_datos}")
            print(f"📊 Dimensiones: {self.datos.shape}")
            print(f"🏙️ Columnas disponibles: {list(self.datos.columns)}")
            return self.datos
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo {self.archivo_datos}")
            # Crear datos de ejemplo si no existe el archivo
            self.crear_datos_ejemplo()
            return self.datos
        except Exception as e:
            print(f"❌ Error al cargar datos: {str(e)}")
            return None
    
    def crear_datos_ejemplo(self) -> None:
        """
        Crear datos de ejemplo si no existe el archivo Excel
        """
        print("📝 Creando datos de ejemplo...")
        
        # Simular datos de velocidad del viento para dos ciudades
        np.random.seed(42)
        n_datos = 365  # Un año de datos diarios
        
        # Ciudad 1: Costa (vientos más consistentes)
        vientos_costa = np.random.weibull(2.2, n_datos) * 7.5
        
        # Ciudad 2: Interior (vientos más variables)
        vientos_interior = np.random.weibull(1.8, n_datos) * 6.0
        
        # Crear DataFrame
        self.datos = pd.DataFrame({
            'Dia': range(1, n_datos + 1),
            'Ciudad_Costa': vientos_costa,
            'Ciudad_Interior': vientos_interior
        })
        
        # Guardar datos de ejemplo
        self.datos.to_excel(self.archivo_datos, index=False)
        print(f"✅ Datos de ejemplo guardados en {self.archivo_datos}")
    
    def seleccionar_ciudades(self, ciudades: List[str]) -> None:
        """
        Seleccionar las ciudades para análisis
        
        Parameters:
        -----------
        ciudades : List[str]
            Lista con nombres de las ciudades (columnas) a analizar
        """
        if self.datos is None:
            print("❌ Error: Primero debe cargar los datos")
            return
        
        # Verificar que las ciudades existen en los datos
        ciudades_disponibles = [col for col in self.datos.columns if col != 'Dia']
        ciudades_validas = []
        
        for ciudad in ciudades:
            if ciudad in ciudades_disponibles:
                ciudades_validas.append(ciudad)
            else:
                print(f"⚠️ Advertencia: Ciudad '{ciudad}' no encontrada en los datos")
        
        if len(ciudades_validas) < 2:
            print("⚠️ Seleccionando automáticamente las dos primeras ciudades disponibles...")
            ciudades_validas = ciudades_disponibles[:2]
        
        self.ciudades_seleccionadas = ciudades_validas[:2]  # Máximo 2 ciudades
        print(f"🏙️ Ciudades seleccionadas: {self.ciudades_seleccionadas}")
    
    def calcular_parametros_weibull(self, velocidades: np.ndarray) -> Dict[str, float]:
        """
        Calcular parámetros k y c de la distribución de Weibull
        
        Usando las ecuaciones:
        - Ecuación 3: k = (σ/v̅)^(-1.09)
        - Ecuación 4: c = v̅ / Γ(1+1/k)
        
        Parameters:
        -----------
        velocidades : np.ndarray
            Array con datos de velocidad del viento
            
        Returns:
        --------
        Dict[str, float]
            Diccionario con parámetros calculados
        """
        # Estadísticas básicas
        v_media = np.mean(velocidades)
        sigma = np.std(velocidades, ddof=1)
        coef_variacion = sigma / v_media
        
        # Ecuación 3: k = (σ/v̅)^(-1.09)
        k = np.power(coef_variacion, -1.09)
        
        # Ecuación 4: c = v̅ / Γ(1+1/k)
        c = v_media / gamma(1 + 1/k)
        
        return {
            'v_media': v_media,
            'sigma': sigma,
            'coef_variacion': coef_variacion,
            'k': k,
            'c': c,
            'lambda_param': c  # Para compatibilidad con clase DistribucionWeibull
        }
    
    def calcular_velocidades_caracteristicas(self, k: float, c: float) -> Dict[str, float]:
        """
        Calcular velocidades características importantes
        
        Usando las ecuaciones:
        - Ecuación 5: v_mp = c * ((k-1)/k)^(1/k)
        - Ecuación 6: v_MAXE = c * ((k+2)/k)^(1/k)
        
        Parameters:
        -----------
        k : float
            Parámetro de forma
        c : float
            Parámetro de escala
            
        Returns:
        --------
        Dict[str, float]
            Diccionario con velocidades características
        """
        # Ecuación 5: Velocidad más probable
        if k > 1:
            v_mp = c * np.power((k-1)/k, 1/k)
        else:
            v_mp = 0.0  # Para k <= 1, la moda está en 0
        
        # Ecuación 6: Velocidad de máxima energía
        v_MAXE = c * np.power((k+2)/k, 1/k)
        
        # Otras velocidades de interés
        v_mediana = c * np.power(np.log(2), 1/k)
        v_media_teorica = c * gamma(1 + 1/k)
        
        return {
            'v_mp': v_mp,           # Velocidad más probable
            'v_MAXE': v_MAXE,       # Velocidad de máxima energía
            'v_mediana': v_mediana,  # Mediana
            'v_media_teorica': v_media_teorica  # Media teórica
        }
    
    def procesar_ciudades(self) -> None:
        """
        Procesar todas las ciudades seleccionadas
        """
        if not self.ciudades_seleccionadas:
            print("❌ Error: No hay ciudades seleccionadas")
            return
        
        print("\n🔄 Procesando ciudades seleccionadas...")
        print("=" * 50)
        
        for ciudad in self.ciudades_seleccionadas:
            velocidades = self.datos[ciudad].values
            
            print(f"\n📍 Procesando: {ciudad}")
            print("-" * 30)
            
            # Calcular parámetros de Weibull
            params = self.calcular_parametros_weibull(velocidades)
            self.parametros[ciudad] = params
            
            # Calcular velocidades características
            velocidades_caract = self.calcular_velocidades_caracteristicas(
                params['k'], params['c']
            )
            
            # Crear distribución de Weibull
            distribucion = DistribucionWeibull(k=params['k'], lambda_param=params['c'])
            self.distribuciones[ciudad] = distribucion
            
            # Almacenar resultados completos
            self.resultados[ciudad] = {
                'datos_originales': velocidades,
                'parametros': params,
                'velocidades_caracteristicas': velocidades_caract,
                'distribucion': distribucion
            }
            
            # Mostrar resultados
            print(f"Velocidad media observada: {params['v_media']:.2f} m/s")
            print(f"Desviación estándar: {params['sigma']:.2f} m/s")
            print(f"Coeficiente de variación: {params['coef_variacion']:.3f}")
            print(f"Parámetro k (forma): {params['k']:.3f}")
            print(f"Parámetro c (escala): {params['c']:.2f} m/s")
            print(f"Velocidad más probable (v_mp): {velocidades_caract['v_mp']:.2f} m/s")
            print(f"Velocidad de máxima energía (v_MAXE): {velocidades_caract['v_MAXE']:.2f} m/s")
    
    def generar_reporte_completo(self) -> pd.DataFrame:
        """
        Generar un reporte completo de todas las ciudades
        """
        if not self.resultados:
            print("❌ Error: No hay resultados para generar reporte")
            return None
        
        datos_reporte = []
        
        for ciudad, resultado in self.resultados.items():
            params = resultado['parametros']
            vel_caract = resultado['velocidades_caracteristicas']
            
            datos_reporte.append({
                'Ciudad': ciudad,
                'N_datos': len(resultado['datos_originales']),
                'V_media_obs (m/s)': params['v_media'],
                'Sigma (m/s)': params['sigma'],
                'Coef_Variacion': params['coef_variacion'],
                'k (forma)': params['k'],
                'c (escala) (m/s)': params['c'],
                'V_mp (m/s)': vel_caract['v_mp'],
                'V_MAXE (m/s)': vel_caract['v_MAXE'],
                'V_mediana (m/s)': vel_caract['v_mediana'],
                'V_media_teorica (m/s)': vel_caract['v_media_teorica']
            })
        
        reporte_df = pd.DataFrame(datos_reporte)
        return reporte_df
    
    def graficar_comparacion_ciudades(self, figsize: Tuple[int, int] = (16, 12)) -> None:
        """
        Crear gráficas comparativas entre ciudades
        """
        if len(self.resultados) < 2:
            print("❌ Error: Se necesitan al menos 2 ciudades para comparar")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
        colors = ['blue', 'red', 'green', 'orange']
        
        # Rango para las curvas teóricas
        v_max = max([np.max(resultado['datos_originales']) 
                    for resultado in self.resultados.values()]) * 1.2
        v = np.linspace(0, v_max, 1000)
        
        for i, (ciudad, resultado) in enumerate(self.resultados.items()):
            color = colors[i % len(colors)]
            distribucion = resultado['distribucion']
            datos = resultado['datos_originales']
            vel_caract = resultado['velocidades_caracteristicas']
            
            # 1. Histogramas vs PDF teórica
            ax1.hist(datos, bins=30, density=True, alpha=0.6, color=color, 
                    label=f'{ciudad} (datos)', edgecolor='black')
            ax1.plot(v, distribucion.pdf(v), color=color, linewidth=2, 
                    linestyle='--', label=f'{ciudad} (Weibull)')
            
            # 2. CDF empírica vs teórica
            datos_ordenados = np.sort(datos)
            cdf_empirica = np.arange(1, len(datos_ordenados) + 1) / len(datos_ordenados)
            
            ax2.plot(datos_ordenados, cdf_empirica, color=color, linewidth=2, 
                    label=f'{ciudad} (empírica)', marker='o', markersize=1)
            ax2.plot(v, distribucion.cdf(v), color=color, linewidth=2, 
                    linestyle='--', label=f'{ciudad} (teórica)')
            
            # 3. Comparación de PDFs
            ax3.plot(v, distribucion.pdf(v), color=color, linewidth=2, label=ciudad)
            ax3.axvline(vel_caract['v_mp'], color=color, linestyle=':', 
                       alpha=0.7, label=f'v_mp {ciudad}')
            ax3.axvline(vel_caract['v_MAXE'], color=color, linestyle='-.',
                       alpha=0.7, label=f'v_MAXE {ciudad}')
            
            # 4. Boxplot comparativo (se agregará después del loop)
        
        # Configurar gráficas
        ax1.set_title('Histograma de Datos vs PDF de Weibull')
        ax1.set_xlabel('Velocidad del viento (m/s)')
        ax1.set_ylabel('Densidad')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2.set_title('CDF Empírica vs Teórica')
        ax2.set_xlabel('Velocidad del viento (m/s)')
        ax2.set_ylabel('Probabilidad acumulada')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        ax3.set_title('Comparación de Distribuciones de Weibull')
        ax3.set_xlabel('Velocidad del viento (m/s)')
        ax3.set_ylabel('Densidad f(v)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Boxplot comparativo
        datos_boxplot = [resultado['datos_originales'] for resultado in self.resultados.values()]
        ciudades_nombres = list(self.resultados.keys())
        
        box_plot = ax4.boxplot(datos_boxplot, labels=ciudades_nombres, patch_artist=True)
        for i, patch in enumerate(box_plot['boxes']):
            patch.set_facecolor(colors[i % len(colors)])
            patch.set_alpha(0.6)
        
        ax4.set_title('Distribución de Velocidades por Ciudad')
        ax4.set_ylabel('Velocidad del viento (m/s)')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('Análisis Comparativo de Velocidad del Viento entre Ciudades', 
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def graficar_velocidades_caracteristicas(self, figsize: Tuple[int, int] = (14, 8)) -> None:
        """
        Graficar velocidades características para cada ciudad
        """
        if not self.resultados:
            print("❌ Error: No hay resultados para graficar")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        ciudades = list(self.resultados.keys())
        velocidades_mp = []
        velocidades_maxe = []
        velocidades_media = []
        velocidades_mediana = []
        
        for ciudad in ciudades:
            vel_caract = self.resultados[ciudad]['velocidades_caracteristicas']
            params = self.resultados[ciudad]['parametros']
            
            velocidades_mp.append(vel_caract['v_mp'])
            velocidades_maxe.append(vel_caract['v_MAXE'])
            velocidades_media.append(params['v_media'])
            velocidades_mediana.append(vel_caract['v_mediana'])
        
        # Gráfica de barras comparativa
        x = np.arange(len(ciudades))
        width = 0.2
        
        ax1.bar(x - 1.5*width, velocidades_mp, width, label='v_mp (más probable)', 
               alpha=0.8, color='skyblue')
        ax1.bar(x - 0.5*width, velocidades_maxe, width, label='v_MAXE (máx. energía)', 
               alpha=0.8, color='lightcoral')
        ax1.bar(x + 0.5*width, velocidades_media, width, label='v_media (observada)', 
               alpha=0.8, color='lightgreen')
        ax1.bar(x + 1.5*width, velocidades_mediana, width, label='v_mediana (teórica)', 
               alpha=0.8, color='gold')
        
        ax1.set_xlabel('Ciudad')
        ax1.set_ylabel('Velocidad (m/s)')
        ax1.set_title('Velocidades Características por Ciudad')
        ax1.set_xticks(x)
        ax1.set_xticklabels(ciudades)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfica de parámetros k y c
        parametros_k = [self.resultados[ciudad]['parametros']['k'] for ciudad in ciudades]
        parametros_c = [self.resultados[ciudad]['parametros']['c'] for ciudad in ciudades]
        
        ax2_twin = ax2.twinx()
        
        bars1 = ax2.bar(x - 0.2, parametros_k, 0.4, label='k (forma)', 
                       alpha=0.8, color='purple')
        bars2 = ax2_twin.bar(x + 0.2, parametros_c, 0.4, label='c (escala)', 
                            alpha=0.8, color='orange')
        
        ax2.set_xlabel('Ciudad')
        ax2.set_ylabel('Parámetro k', color='purple')
        ax2_twin.set_ylabel('Parámetro c (m/s)', color='orange')
        ax2.set_title('Parámetros de Weibull por Ciudad')
        ax2.set_xticks(x)
        ax2.set_xticklabels(ciudades)
        
        # Añadir valores sobre las barras
        for i, (k, c) in enumerate(zip(parametros_k, parametros_c)):
            ax2.text(i-0.2, k+0.05, f'{k:.2f}', ha='center', va='bottom')
            ax2_twin.text(i+0.2, c+0.1, f'{c:.2f}', ha='center', va='bottom')
        
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def calcular_potencial_eolico(self, densidad_aire: float = 1.225) -> Dict[str, Dict[str, float]]:
        """
        Calcular el potencial eólico para cada ciudad
        
        La potencia del viento es proporcional a v³
        P = 0.5 * ρ * A * v³
        
        Parameters:
        -----------
        densidad_aire : float
            Densidad del aire en kg/m³ (por defecto 1.225 kg/m³ a nivel del mar)
        """
        potencial = {}
        
        for ciudad, resultado in self.resultados.items():
            distribucion = resultado['distribucion']
            vel_caract = resultado['velocidades_caracteristicas']
            
            # Calcular potencia promedio integrando P(v) * f(v) dv
            v_max = 25  # m/s - velocidad máxima práctica
            v = np.linspace(0, v_max, 1000)
            
            # Potencia específica (por unidad de área)
            potencia_especifica = 0.5 * densidad_aire * v**3  # W/m²
            pdf_vals = distribucion.pdf(v)
            
            # Potencia promedio
            potencia_promedio = np.trapz(potencia_especifica * pdf_vals, v)
            
            # Potencia a velocidades características
            potencia_mp = 0.5 * densidad_aire * vel_caract['v_mp']**3
            potencia_maxe = 0.5 * densidad_aire * vel_caract['v_MAXE']**3
            
            # Factor de capacidad (asumiendo turbina con potencia nominal a 12 m/s)
            v_nominal = 12.0
            potencia_nominal = 0.5 * densidad_aire * v_nominal**3
            factor_capacidad = potencia_promedio / potencia_nominal
            
            potencial[ciudad] = {
                'potencia_promedio': potencia_promedio,  # W/m²
                'potencia_mp': potencia_mp,  # W/m² a velocidad más probable
                'potencia_maxe': potencia_maxe,  # W/m² a velocidad de máxima energía
                'factor_capacidad': factor_capacidad,  # Factor de capacidad
                'horas_equivalentes': factor_capacidad * 8760  # Horas equivalentes al año
            }
        
        return potencial
    
    def ejecutar_analisis_completo(self, ciudades: List[str] = None) -> None:
        """
        Ejecutar el análisis completo de velocidad del viento
        """
        print("🌪️ ANÁLISIS DE VELOCIDAD DEL VIENTO CON DISTRIBUCIÓN DE WEIBULL")
        print("=" * 70)
        
        # 1. Cargar datos
        self.cargar_datos()
        
        # 2. Seleccionar ciudades
        if ciudades is None:
            if self.datos is not None:
                ciudades_disponibles = [col for col in self.datos.columns if col != 'Dia']
                ciudades = ciudades_disponibles[:2]
        
        self.seleccionar_ciudades(ciudades)
        
        # 3. Procesar ciudades
        self.procesar_ciudades()
        
        # 4. Generar reporte
        print("\n📋 REPORTE COMPLETO")
        print("=" * 50)
        reporte = self.generar_reporte_completo()
        if reporte is not None:
            print(reporte.to_string(index=False, float_format='%.3f'))
        
        # 5. Calcular potencial eólico
        print("\n⚡ POTENCIAL EÓLICO")
        print("=" * 50)
        potencial = self.calcular_potencial_eolico()
        
        for ciudad, pot in potencial.items():
            print(f"\n📍 {ciudad}:")
            print(f"  Potencia promedio: {pot['potencia_promedio']:.1f} W/m²")
            print(f"  Potencia a v_mp: {pot['potencia_mp']:.1f} W/m²")
            print(f"  Potencia a v_MAXE: {pot['potencia_maxe']:.1f} W/m²")
            print(f"  Factor de capacidad: {pot['factor_capacidad']:.3f}")
            print(f"  Horas equivalentes/año: {pot['horas_equivalentes']:.0f} h")
        
        # 6. Crear visualizaciones
        print("\n📊 Generando gráficas...")
        self.graficar_comparacion_ciudades()
        self.graficar_velocidades_caracteristicas()
        
        print("\n✅ Análisis completo finalizado!")


def main():
    """
    Función principal para ejecutar el análisis
    """
    # Crear instancia del análisis
    analisis = AnalisisVientoWeibull("Datos.xlsx")
    
    # Ejecutar análisis completo
    # Se pueden especificar ciudades específicas: ['Ciudad_Costa', 'Ciudad_Interior']
    analisis.ejecutar_analisis_completo()


if __name__ == "__main__":
    main()
