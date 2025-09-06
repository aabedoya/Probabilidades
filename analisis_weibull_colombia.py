"""
Análisis de Weibull con Datos Reales de Colombia
===============================================

Este script aplica las 6 ecuaciones específicas de Weibull a datos reales 
de velocidades del viento de 4 municipios colombianos:
- Riohacha (Costa Caribe - Altos vientos)
- San Andrés (Isla - Vientos marinos constantes)  
- Barranquilla (Costa - Vientos moderados)
- Valledupar (Interior - Vientos variables)

Ecuaciones implementadas:
1. f(v) = (k/c) * (v/c)^(k-1) * e^(-(v/c)^k)  - PDF
2. F(v) = 1 - e^(-(v/c)^k)                     - CDF
3. k = (σ/v̅)^(-1.09)                          - Parámetro de forma
4. c = v̅ / Γ(1+1/k)                          - Parámetro de escala
5. v_mp = c * ((k-1)/k)^(1/k)                 - Velocidad más probable  
6. v_MAXE = c * ((k+2)/k)^(1/k)              - Velocidad de máxima energía

Autor: Proyecto Probabilidades
Fecha: 3 de septiembre de 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from typing import Dict, List, Tuple
import seaborn as sns

# Configurar estilo de gráficas
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AnalisisWeibullColombia:
    """Análisis de Weibull específico para datos de Colombia"""
    
    def __init__(self, archivo_datos: str = "datos_weibull_colombia.xlsx"):
        """
        Inicializar analizador con datos de Colombia
        
        Parameters:
        -----------
        archivo_datos : str
            Ruta al archivo Excel con datos procesados
        """
        self.archivo_datos = archivo_datos
        self.datos_originales = None
        self.resultados_municipios = {}
        self.cargar_datos_colombia()
    
    def cargar_datos_colombia(self) -> None:
        """Cargar datos procesados de municipios colombianos"""
        try:
            # Cargar datos principales
            self.datos_originales = pd.read_excel(self.archivo_datos, sheet_name='Datos_Weibull')
            
            # Cargar resumen estadístico si existe
            try:
                self.resumen_estadistico = pd.read_excel(self.archivo_datos, sheet_name='Resumen')
            except:
                self.resumen_estadistico = None
            
            print(f"✅ Datos cargados: {self.datos_originales.shape}")
            print(f"🏙️ Municipios: {[col for col in self.datos_originales.columns if col != 'Dia']}")
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            raise
    
    def aplicar_ecuaciones_municipio(self, municipio: str) -> Dict:
        """
        Aplicar las 6 ecuaciones de Weibull a un municipio específico
        
        Parameters:
        -----------
        municipio : str
            Nombre del municipio
            
        Returns:
        --------
        Dict
            Resultados completos del análisis
        """
        if municipio not in self.datos_originales.columns:
            raise ValueError(f"❌ Municipio '{municipio}' no encontrado en los datos")
        
        # Extraer velocidades del viento (eliminar NaN)
        velocidades_serie = self.datos_originales[municipio]
        velocidades = velocidades_serie.dropna().values
        
        if len(velocidades) < 30:
            raise ValueError(f"❌ Datos insuficientes para {municipio}: {len(velocidades)} registros")
        
        print(f"\n{'='*60}")
        print(f"🌪️ ANÁLISIS DE WEIBULL - {municipio.upper()}")
        print(f"{'='*60}")
        
        # Estadísticas básicas observadas
        n_datos = len(velocidades)
        v_promedio = float(np.mean(velocidades))
        sigma = float(np.std(velocidades, ddof=1))
        v_min = float(np.min(velocidades))
        v_max = float(np.max(velocidades))
        
        print(f"📊 DATOS OBSERVADOS:")
        print(f"   • Registros: {n_datos:,}")
        print(f"   • Período: {n_datos} días de mediciones")
        print(f"   • Velocidad promedio (v̅): {v_promedio:.2f} m/s")
        print(f"   • Desviación estándar (σ): {sigma:.2f} m/s")
        print(f"   • Rango: {v_min:.1f} - {v_max:.1f} m/s")
        print(f"   • Coeficiente de variación: {sigma/v_promedio:.3f}")
        
        # Aplicar ecuaciones paso a paso
        print(f"\n🔬 APLICACIÓN DE ECUACIONES:")
        print(f"{'─'*45}")
        
        # Ecuación 3: Calcular parámetro k
        k = self.ecuacion_3_parametro_forma(v_promedio, sigma)
        print(f"📐 Ecuación 3: k = (σ/v̅)^(-1.09)")
        print(f"   k = ({sigma:.2f}/{v_promedio:.2f})^(-1.09) = {k:.3f}")
        
        # Ecuación 4: Calcular parámetro c  
        c = self.ecuacion_4_parametro_escala(v_promedio, k)
        gamma_val = gamma(1 + 1/k)
        print(f"📐 Ecuación 4: c = v̅ / Γ(1+1/k)")
        print(f"   c = {v_promedio:.2f} / {gamma_val:.3f} = {c:.2f} m/s")
        
        # Ecuación 5: Velocidad más probable
        v_mp = self.ecuacion_5_velocidad_mas_probable(k, c)
        print(f"📐 Ecuación 5: v_mp = c * ((k-1)/k)^(1/k)")
        if k > 1:
            ratio = (k-1)/k
            print(f"   v_mp = {c:.2f} * ({ratio:.3f})^({1/k:.3f}) = {v_mp:.2f} m/s")
        else:
            print(f"   v_mp = 0.00 m/s (k ≤ 1)")
            
        # Ecuación 6: Velocidad de máxima energía
        v_MAXE = self.ecuacion_6_velocidad_maxima_energia(k, c)
        ratio_maxe = (k+2)/k
        print(f"📐 Ecuación 6: v_MAXE = c * ((k+2)/k)^(1/k)")
        print(f"   v_MAXE = {c:.2f} * ({ratio_maxe:.3f})^({1/k:.3f}) = {v_MAXE:.2f} m/s")
        
        # Verificación matemática
        v_media_teorica = c * gamma(1 + 1/k)
        error_relativo = abs(v_media_teorica - v_promedio) / v_promedio * 100
        
        print(f"\n✅ VERIFICACIÓN MATEMÁTICA:")
        print(f"   • Media teórica: {v_media_teorica:.2f} m/s")
        print(f"   • Media observada: {v_promedio:.2f} m/s")
        print(f"   • Error relativo: {error_relativo:.3f}%")
        
        # Análisis de potencial eólico
        densidad_aire = 1.225  # kg/m³ a nivel del mar
        potencia_mp = 0.5 * densidad_aire * v_mp**3  # W/m²
        potencia_MAXE = 0.5 * densidad_aire * v_MAXE**3  # W/m²
        potencia_media = 0.5 * densidad_aire * v_promedio**3  # W/m²
        
        print(f"\n⚡ POTENCIAL EÓLICO:")
        print(f"   • Potencia en v_mp: {potencia_mp:.1f} W/m²")
        print(f"   • Potencia en v_MAXE: {potencia_MAXE:.1f} W/m²")
        print(f"   • Potencia promedio: {potencia_media:.1f} W/m²")
        
        # Clasificar el recurso eólico
        clasificacion = self._clasificar_recurso_eolico(v_promedio, k)
        print(f"   • Clasificación: {clasificacion}")
        
        # Almacenar resultados
        resultado = {
            'municipio': municipio,
            'datos_observados': {
                'n_datos': n_datos,
                'velocidades': velocidades,
                'v_promedio': v_promedio,
                'sigma': sigma,
                'v_min': v_min,
                'v_max': v_max,
                'coef_variacion': sigma/v_promedio
            },
            'parametros_weibull': {
                'k': k,
                'c': c,
                'gamma_factor': gamma_val
            },
            'velocidades_caracteristicas': {
                'v_mp': v_mp,
                'v_MAXE': v_MAXE,
                'v_media_teorica': v_media_teorica,
                'error_relativo_pct': error_relativo
            },
            'potencial_eolico': {
                'potencia_mp': potencia_mp,
                'potencia_MAXE': potencia_MAXE,
                'potencia_media': potencia_media,
                'clasificacion': clasificacion
            }
        }
        
        self.resultados_municipios[municipio] = resultado
        return resultado
    
    def ecuacion_1_pdf(self, v: np.ndarray, k: float, c: float) -> np.ndarray:
        """Ecuación 1: PDF de Weibull"""
        v = np.maximum(v, 1e-10)  # Evitar división por cero
        return (k/c) * np.power(v/c, k-1) * np.exp(-np.power(v/c, k))
    
    def ecuacion_2_cdf(self, v: np.ndarray, k: float, c: float) -> np.ndarray:
        """Ecuación 2: CDF de Weibull"""
        return 1 - np.exp(-np.power(v/c, k))
    
    def ecuacion_3_parametro_forma(self, v_promedio: float, sigma: float) -> float:
        """Ecuación 3: Parámetro de forma k"""
        return np.power(sigma/v_promedio, -1.09)
    
    def ecuacion_4_parametro_escala(self, v_promedio: float, k: float) -> float:
        """Ecuación 4: Parámetro de escala c"""
        return v_promedio / gamma(1 + 1/k)
    
    def ecuacion_5_velocidad_mas_probable(self, k: float, c: float) -> float:
        """Ecuación 5: Velocidad más probable"""
        if k <= 1:
            return 0.0
        return c * np.power((k-1)/k, 1/k)
    
    def ecuacion_6_velocidad_maxima_energia(self, k: float, c: float) -> float:
        """Ecuación 6: Velocidad de máxima energía"""
        return c * np.power((k+2)/k, 1/k)
    
    def _clasificar_recurso_eolico(self, v_promedio: float, k: float) -> str:
        """Clasificar el recurso eólico según estándares internacionales"""
        if v_promedio >= 10 and k >= 2:
            return "🟢 EXCELENTE - Ideal para generación eólica"
        elif v_promedio >= 8 and k >= 1.8:
            return "🟡 BUENO - Viable para generación eólica"
        elif v_promedio >= 6 and k >= 1.5:
            return "🟠 MODERADO - Posible con tecnología avanzada"
        else:
            return "🔴 LIMITADO - No recomendable para generación eólica"
    
    def generar_graficas_municipio(self, municipio: str, figsize: Tuple[int, int] = (16, 12)) -> None:
        """
        Generar gráficas completas para un municipio específico
        
        Parameters:
        -----------
        municipio : str
            Nombre del municipio
        figsize : Tuple[int, int]
            Tamaño de la figura
        """
        if municipio not in self.resultados_municipios:
            print(f"❌ Debe analizar {municipio} primero usando aplicar_ecuaciones_municipio()")
            return
        
        resultado = self.resultados_municipios[municipio]
        velocidades = resultado['datos_observados']['velocidades']
        k = resultado['parametros_weibull']['k']
        c = resultado['parametros_weibull']['c']
        v_mp = resultado['velocidades_caracteristicas']['v_mp']
        v_MAXE = resultado['velocidades_caracteristicas']['v_MAXE']
        v_promedio = resultado['datos_observados']['v_promedio']
        
        # Crear rango para las curvas teóricas
        v_max_plot = min(35, np.max(velocidades) * 1.2)
        v = np.linspace(0.1, v_max_plot, 1000)
        
        # Calcular funciones teóricas
        pdf_vals = self.ecuacion_1_pdf(v, k, c)
        cdf_vals = self.ecuacion_2_cdf(v, k, c)
        
        # Crear figura con 6 subgráficas
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Histograma vs PDF (Ecuación 1)
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.hist(velocidades, bins=50, density=True, alpha=0.7, color='lightblue', 
                edgecolor='black', label='Datos observados')
        ax1.plot(v, pdf_vals, 'r-', linewidth=3, label=f'PDF Weibull (Ec.1)')
        ax1.axvline(v_mp, color='green', linestyle='--', linewidth=2, label=f'v_mp = {v_mp:.1f} m/s')
        ax1.axvline(v_MAXE, color='purple', linestyle='-.', linewidth=2, label=f'v_MAXE = {v_MAXE:.1f} m/s')
        ax1.axvline(v_promedio, color='orange', linestyle=':', linewidth=2, label=f'v̅ = {v_promedio:.1f} m/s')
        
        ax1.set_title(f'Ecuación 1: PDF - {municipio}\nk = {k:.3f}, c = {c:.2f} m/s')
        ax1.set_xlabel('Velocidad del viento (m/s)')
        ax1.set_ylabel('Densidad de probabilidad')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. CDF (Ecuación 2)
        ax2 = fig.add_subplot(gs[0, 1])
        velocidades_ordenadas = np.sort(velocidades)
        cdf_empirica = np.arange(1, len(velocidades_ordenadas) + 1) / len(velocidades_ordenadas)
        
        ax2.plot(velocidades_ordenadas, cdf_empirica, 'bo', markersize=1, alpha=0.6, label='CDF empírica')
        ax2.plot(v, cdf_vals, 'r-', linewidth=3, label='CDF Weibull (Ec.2)')
        ax2.axvline(v_mp, color='green', linestyle='--', alpha=0.7)
        ax2.axvline(v_MAXE, color='purple', linestyle='-.', alpha=0.7)
        
        ax2.set_title(f'Ecuación 2: CDF - {municipio}')
        ax2.set_xlabel('Velocidad del viento (m/s)')
        ax2.set_ylabel('Probabilidad acumulada')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Análisis de potencia eólica
        ax3 = fig.add_subplot(gs[1, 0])
        densidad_potencia = 0.5 * 1.225 * v**3
        potencia_ponderada = densidad_potencia * pdf_vals
        
        ax3.plot(v, potencia_ponderada, 'g-', linewidth=3, label='Densidad de potencia ponderada')
        ax3.axvline(v_mp, color='green', linestyle='--', linewidth=2, label=f'v_mp = {v_mp:.1f} m/s')
        ax3.axvline(v_MAXE, color='purple', linestyle='-.', linewidth=2, label=f'v_MAXE = {v_MAXE:.1f} m/s')
        
        ax3.set_title(f'Análisis de Potencia Eólica - {municipio}')
        ax3.set_xlabel('Velocidad del viento (m/s)')
        ax3.set_ylabel('Potencia ponderada (W/m²)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Velocidades características
        ax4 = fig.add_subplot(gs[1, 1])
        velocidades_caract = {
            'v_promedio': v_promedio,
            'v_mediana': c * np.power(np.log(2), 1/k),
            'v_mp (Ec.5)': v_mp,
            'v_MAXE (Ec.6)': v_MAXE
        }
        
        nombres = list(velocidades_caract.keys())
        valores = list(velocidades_caract.values())
        colores = ['blue', 'cyan', 'green', 'purple']
        
        bars = ax4.bar(nombres, valores, color=colores, alpha=0.7, edgecolor='black')
        
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                    f'{valor:.1f} m/s', ha='center', va='bottom', fontweight='bold')
        
        ax4.set_title(f'Velocidades Características - {municipio}')
        ax4.set_ylabel('Velocidad (m/s)')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # 5. Serie temporal (muestra)
        ax5 = fig.add_subplot(gs[2, :])
        n_muestra = min(365, len(velocidades))  # Mostrar hasta 1 año
        dias_muestra = range(1, n_muestra + 1)
        vel_muestra = velocidades[:n_muestra]
        
        ax5.plot(dias_muestra, vel_muestra, 'b-', linewidth=1, alpha=0.7, label='Velocidades observadas')
        ax5.axhline(v_promedio, color='red', linestyle='-', linewidth=2, label=f'Promedio = {v_promedio:.1f} m/s')
        ax5.axhline(v_mp, color='green', linestyle='--', linewidth=2, label=f'v_mp = {v_mp:.1f} m/s')
        ax5.axhline(v_MAXE, color='purple', linestyle='-.', linewidth=2, label=f'v_MAXE = {v_MAXE:.1f} m/s')
        
        ax5.set_title(f'Serie Temporal de Velocidades - {municipio} (Primeros {n_muestra} días)')
        ax5.set_xlabel('Día')
        ax5.set_ylabel('Velocidad del viento (m/s)')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        plt.suptitle(f'Análisis Completo de Weibull - {municipio}', fontsize=16, fontweight='bold')
        plt.show()
    
    def analizar_todos_municipios(self) -> None:
        """Analizar todos los municipios disponibles"""
        municipios = [col for col in self.datos_originales.columns if col != 'Dia']
        
        print(f"\n🔄 ANALIZANDO {len(municipios)} MUNICIPIOS COLOMBIANOS...")
        print("=" * 70)
        
        for municipio in municipios:
            try:
                self.aplicar_ecuaciones_municipio(municipio)
            except Exception as e:
                print(f"⚠️ Error analizando {municipio}: {e}")
    
    def generar_comparacion_final(self, figsize: Tuple[int, int] = (18, 12)) -> None:
        """Generar gráficas comparativas finales entre todos los municipios"""
        if not self.resultados_municipios:
            print("❌ No hay resultados para comparar. Ejecute analizar_todos_municipios() primero.")
            return
        
        municipios = list(self.resultados_municipios.keys())
        colores = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
        
        # 1. Comparación de PDFs
        v_global = np.linspace(0.1, 35, 1000)
        for i, municipio in enumerate(municipios):
            resultado = self.resultados_municipios[municipio]
            k = resultado['parametros_weibull']['k']
            c = resultado['parametros_weibull']['c']
            
            pdf_vals = self.ecuacion_1_pdf(v_global, k, c)
            ax1.plot(v_global, pdf_vals, color=colores[i % len(colores)], linewidth=2, 
                    label=f'{municipio} (k={k:.2f}, c={c:.1f})')
        
        ax1.set_title('Comparación de PDFs - Ecuación 1')
        ax1.set_xlabel('Velocidad del viento (m/s)')
        ax1.set_ylabel('Densidad de probabilidad')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Parámetros k vs c
        params_k = [self.resultados_municipios[m]['parametros_weibull']['k'] for m in municipios]
        params_c = [self.resultados_municipios[m]['parametros_weibull']['c'] for m in municipios]
        
        ax2.scatter(params_k, params_c, s=100, alpha=0.7, c=colores[:len(municipios)])
        for i, municipio in enumerate(municipios):
            ax2.annotate(municipio, (params_k[i], params_c[i]), xytext=(5, 5), 
                        textcoords='offset points', fontsize=9)
        
        ax2.set_title('Parámetros de Weibull - Ecuaciones 3 y 4')
        ax2.set_xlabel('k (parámetro de forma)')
        ax2.set_ylabel('c (parámetro de escala - m/s)')
        ax2.grid(True, alpha=0.3)
        
        # 3. Velocidades características
        v_mp_vals = [self.resultados_municipios[m]['velocidades_caracteristicas']['v_mp'] for m in municipios]
        v_MAXE_vals = [self.resultados_municipios[m]['velocidades_caracteristicas']['v_MAXE'] for m in municipios]
        v_prom_vals = [self.resultados_municipios[m]['datos_observados']['v_promedio'] for m in municipios]
        
        x = np.arange(len(municipios))
        width = 0.25
        
        ax3.bar(x - width, v_prom_vals, width, label='v̅ (observada)', alpha=0.8)
        ax3.bar(x, v_mp_vals, width, label='v_mp (Ec. 5)', alpha=0.8)
        ax3.bar(x + width, v_MAXE_vals, width, label='v_MAXE (Ec. 6)', alpha=0.8)
        
        ax3.set_title('Velocidades Características - Ecuaciones 5 y 6')
        ax3.set_xlabel('Municipio')
        ax3.set_ylabel('Velocidad (m/s)')
        ax3.set_xticks(x)
        ax3.set_xticklabels(municipios, rotation=45)
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Potencial eólico
        potencias = [self.resultados_municipios[m]['potencial_eolico']['potencia_media'] for m in municipios]
        clasificaciones = [self.resultados_municipios[m]['potencial_eolico']['clasificacion'] for m in municipios]
        
        bars = ax4.bar(municipios, potencias, color=colores[:len(municipios)], alpha=0.7)
        
        for bar, potencia in zip(bars, potencias):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 20,
                    f'{potencia:.0f} W/m²', ha='center', va='bottom', fontweight='bold')
        
        ax4.set_title('Potencial Eólico Promedio')
        ax4.set_xlabel('Municipio')
        ax4.set_ylabel('Potencia (W/m²)')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.suptitle('Comparación de Ecuaciones de Weibull - Colombia', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        # Mostrar tabla resumen final
        self._mostrar_tabla_resumen_final()
    
    def _mostrar_tabla_resumen_final(self) -> None:
        """Mostrar tabla resumen final con todos los resultados"""
        print(f"\n📊 RESUMEN FINAL - ANÁLISIS DE WEIBULL COLOMBIA")
        print("=" * 90)
        
        print(f"{'Municipio':<12} {'k':<6} {'c(m/s)':<7} {'v_mp':<6} {'v_MAXE':<7} {'Pot(W/m²)':<10} {'Clasificación':<20}")
        print("-" * 90)
        
        for municipio, resultado in self.resultados_municipios.items():
            k = resultado['parametros_weibull']['k']
            c = resultado['parametros_weibull']['c']
            v_mp = resultado['velocidades_caracteristicas']['v_mp']
            v_MAXE = resultado['velocidades_caracteristicas']['v_MAXE']
            potencia = resultado['potencial_eolico']['potencia_media']
            clasificacion = resultado['potencial_eolico']['clasificacion'].split(' - ')[0]
            
            print(f"{municipio:<12} {k:<6.3f} {c:<7.2f} {v_mp:<6.2f} {v_MAXE:<7.2f} {potencia:<10.0f} {clasificacion:<20}")


def ejemplo_completo_colombia():
    """Ejemplo completo con datos reales de Colombia"""
    print("🇨🇴 ANÁLISIS COMPLETO DE WEIBULL - COLOMBIA")
    print("=" * 70)
    
    # 1. Crear analizador
    analizador = AnalisisWeibullColombia("datos_weibull_colombia.xlsx")
    
    # 2. Analizar todos los municipios
    analizador.analizar_todos_municipios()
    
    # 3. Generar gráficas individuales para municipios destacados
    municipios_destacados = ['Riohacha', 'San Andrés']  # Los de mejores vientos
    
    for municipio in municipios_destacados:
        analizador.generar_graficas_municipio(municipio)
    
    # 4. Generar comparación final
    analizador.generar_comparacion_final()
    
    return analizador


if __name__ == "__main__":
    # Ejecutar análisis completo
    analizador = ejemplo_completo_colombia()
