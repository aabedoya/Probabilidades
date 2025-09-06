"""
Proyecto de Distribución de Weibull
===================================

Este proyecto implementa la distribución de probabilidad de Weibull, incluyendo:
- Función de densidad de probabilidad (PDF)
- Función de distribución acumulativa (CDF)
- Generación de muestras aleatorias
- Visualización y análisis estadístico

La distribución de Weibull está definida por dos parámetros:
- k: parámetro de forma (shape parameter)
- λ: parámetro de escala (scale parameter)

Autor: Proyecto Probabilidades
Fecha: 3 de septiembre de 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.special import gamma
import pandas as pd
import seaborn as sns
from typing import Union, List, Tuple
import warnings

# Configurar el estilo de las gráficas
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DistribucionWeibull:
    """
    Clase para trabajar con la Distribución de Weibull

    Parámetros:
    -----------
    k : float
        Parámetro de forma (shape parameter), k > 0
    lambda_param : float
        Parámetro de escala (scale parameter), λ > 0
    """

    def __init__(self, k: float, lambda_param: float):
        """
        Inicializar la distribución de Weibull

        Parameters:
        -----------
        k : float
            Parámetro de forma (k > 0)
        lambda_param : float
            Parámetro de escala (λ > 0)
        """
        if k <= 0:
            raise ValueError("El parámetro de forma k debe ser mayor que 0")
        if lambda_param <= 0:
            raise ValueError("El parámetro de escala λ debe ser mayor que 0")

        self.k = k  # parámetro de forma
        self.lambda_param = lambda_param  # parámetro de escala
        self.weibull_dist = stats.weibull_min(c=k, scale=lambda_param)

    def pdf(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Función de densidad de probabilidad (PDF) de Weibull

        f(v) = (k/λ) * (v/λ)^(k-1) * e^(-(v/λ)^k)

        Parameters:
        -----------
        x : float o array-like
            Valores donde evaluar la PDF

        Returns:
        --------
        float o array-like
            Valores de la función de densidad
        """
        x = np.asarray(x)

        # Para valores negativos, la PDF es 0
        result = np.zeros_like(x, dtype=float)

        # Para valores no negativos
        mask = x >= 0
        x_pos = x[mask]

        if len(x_pos) > 0:
            # f(v) = (k/λ) * (v/λ)^(k-1) * e^(-(v/λ)^k)
            term1 = self.k / self.lambda_param
            term2 = np.power(x_pos / self.lambda_param, self.k - 1)
            term3 = np.exp(-np.power(x_pos / self.lambda_param, self.k))

            result[mask] = term1 * term2 * term3

        return result if x.shape else float(result)

    def cdf(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Función de distribución acumulativa (CDF) de Weibull

        F(v) = 1 - e^(-(v/λ)^k)

        Parameters:
        -----------
        x : float o array-like
            Valores donde evaluar la CDF

        Returns:
        --------
        float o array-like
            Valores de la función de distribución acumulativa
        """
        x = np.asarray(x)

        # Para valores negativos, la CDF es 0
        result = np.zeros_like(x, dtype=float)

        # Para valores no negativos
        mask = x >= 0
        x_pos = x[mask]

        if len(x_pos) > 0:
            # F(v) = 1 - e^(-(v/λ)^k)
            result[mask] = 1 - np.exp(-np.power(x_pos / self.lambda_param, self.k))

        return result if x.shape else float(result)

    def survival_function(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Función de supervivencia (1 - CDF)

        S(v) = e^(-(v/λ)^k)
        """
        return 1 - self.cdf(x)

    def hazard_function(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Función de riesgo (hazard function)

        h(v) = f(v) / S(v) = (k/λ) * (v/λ)^(k-1)
        """
        x = np.asarray(x)

        # Para valores negativos, la función de riesgo es 0
        result = np.zeros_like(x, dtype=float)

        # Para valores positivos
        mask = x > 0
        x_pos = x[mask]

        if len(x_pos) > 0:
            result[mask] = (self.k / self.lambda_param) * np.power(x_pos / self.lambda_param, self.k - 1)

        return result if x.shape else float(result)

    def generar_muestras(self, n: int, random_state: int = None) -> np.ndarray: # type: ignore
        """
        Generar muestras aleatorias de la distribución de Weibull

        Parameters:
        -----------
        n : int
            Número de muestras a generar
        random_state : int, opcional
            Semilla para la generación de números aleatorios

        Returns:
        --------
        numpy.ndarray
            Array con las muestras generadas
        """
        if random_state is not None:
            np.random.seed(random_state)

        return self.weibull_dist.rvs(size=n)

    def media(self) -> float:
        """
        Calcular la media de la distribución de Weibull

        E[X] = λ * Γ(1 + 1/k)
        """
        return self.lambda_param * gamma(1 + 1/self.k)

    def varianza(self) -> float:
        """
        Calcular la varianza de la distribución de Weibull

        Var[X] = λ² * [Γ(1 + 2/k) - Γ²(1 + 1/k)]
        """
        gamma1 = gamma(1 + 1/self.k)
        gamma2 = gamma(1 + 2/self.k)
        return self.lambda_param**2 * (gamma2 - gamma1**2)

    def desviacion_estandar(self) -> float:
        """
        Calcular la desviación estándar de la distribución
        """
        return np.sqrt(self.varianza())

    def moda(self) -> float:
        """
        Calcular la moda de la distribución de Weibull

        Moda = λ * ((k-1)/k)^(1/k) si k > 1, sino 0
        """
        if self.k <= 1:
            return 0.0
        else:
            return self.lambda_param * np.power((self.k - 1) / self.k, 1 / self.k)

    def mediana(self) -> float:
        """
        Calcular la mediana de la distribución de Weibull

        Mediana = λ * (ln(2))^(1/k)
        """
        return self.lambda_param * np.power(np.log(2), 1 / self.k)

    def percentil(self, p: float) -> float:
        """
        Calcular el percentil p de la distribución

        Parameters:
        -----------
        p : float
            Percentil a calcular (entre 0 y 1)
        """
        if not 0 <= p <= 1:
            raise ValueError("El percentil debe estar entre 0 y 1")

        return self.lambda_param * np.power(-np.log(1 - p), 1 / self.k)

    def resumen_estadistico(self) -> dict:
        """
        Obtener un resumen de las estadísticas de la distribución
        """
        return {
            'parametros': {
                'k (forma)': self.k,
                'λ (escala)': self.lambda_param
            },
            'medidas_tendencia_central': {
                'media': self.media(),
                'mediana': self.mediana(),
                'moda': self.moda()
            },
            'medidas_dispersion': {
                'varianza': self.varianza(),
                'desviacion_estandar': self.desviacion_estandar()
            },
            'percentiles': {
                'Q1 (25%)': self.percentil(0.25),
                'Q2 (50% - mediana)': self.percentil(0.50),
                'Q3 (75%)': self.percentil(0.75),
                'P90': self.percentil(0.90),
                'P95': self.percentil(0.95)
            }
        }

    def graficar_distribucion(self, x_max: float = None, n_puntos: int = 1000,  # type: ignore
                            figsize: Tuple[int, int] = (15, 10)) -> None:
        """
        Crear gráficas de la distribución de Weibull

        Parameters:
        -----------
        x_max : float, opcional
            Valor máximo para el eje x. Si no se especifica, se calcula automáticamente
        n_puntos : int
            Número de puntos para las curvas
        figsize : tuple
            Tamaño de la figura
        """
        if x_max is None:
            x_max = self.percentil(0.99) * 1.2

        x = np.linspace(0, x_max, n_puntos)

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle(f'Distribución de Weibull (k={self.k}, λ={self.lambda_param})',
                    fontsize=16, fontweight='bold')

        # PDF
        ax1.plot(x, self.pdf(x), 'b-', linewidth=2, label='PDF')
        ax1.fill_between(x, self.pdf(x), alpha=0.3, color='blue')
        ax1.set_title('Función de Densidad de Probabilidad (PDF)')
        ax1.set_xlabel('x')
        ax1.set_ylabel('f(x)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # CDF
        ax2.plot(x, self.cdf(x), 'r-', linewidth=2, label='CDF')
        ax2.set_title('Función de Distribución Acumulativa (CDF)')
        ax2.set_xlabel('x')
        ax2.set_ylabel('F(x)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # Función de Supervivencia
        ax3.plot(x, self.survival_function(x), 'g-', linewidth=2, label='Supervivencia')
        ax3.set_title('Función de Supervivencia')
        ax3.set_xlabel('x')
        ax3.set_ylabel('S(x)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Función de Riesgo
        x_hazard = x[x > 0]  # Evitar x=0 para la función de riesgo
        ax4.plot(x_hazard, self.hazard_function(x_hazard), 'm-', linewidth=2, label='Riesgo')
        ax4.set_title('Función de Riesgo (Hazard)')
        ax4.set_xlabel('x')
        ax4.set_ylabel('h(x)')
        ax4.grid(True, alpha=0.3)
        ax4.legend()

        plt.tight_layout()
        plt.show()

    def graficar_comparacion_parametros(self, k_valores: List[float] = None,  # type: ignore
                                    lambda_valores: List[float] = None, # type: ignore
                                    figsize: Tuple[int, int] = (15, 8)) -> None:
        """
        Comparar diferentes distribuciones de Weibull con diferentes parámetros
        """
        if k_valores is None:
            k_valores = [0.5, 1.0, 1.5, 2.0, 3.0]
        if lambda_valores is None:
            lambda_valores = [0.5, 1.0, 2.0]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Comparación variando k (manteniendo λ constante)
        x_max = 3.0
        x = np.linspace(0, x_max, 1000)

        for k in k_valores:
            weibull_temp = DistribucionWeibull(k, self.lambda_param)
            ax1.plot(x, weibull_temp.pdf(x), linewidth=2,
                    label=f'k={k}, λ={self.lambda_param}')

        ax1.set_title('Efecto del parámetro de forma k')
        ax1.set_xlabel('x')
        ax1.set_ylabel('f(x)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Comparación variando λ (manteniendo k constante)
        for lam in lambda_valores:
            weibull_temp = DistribucionWeibull(self.k, lam)
            ax2.plot(x, weibull_temp.pdf(x), linewidth=2,
                    label=f'k={self.k}, λ={lam}')

        ax2.set_title('Efecto del parámetro de escala λ')
        ax2.set_xlabel('x')
        ax2.set_ylabel('f(x)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.suptitle('Comparación de Distribuciones de Weibull', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()

    def analizar_muestras(self, muestras: np.ndarray = None, n_muestras: int = 1000, # type: ignore
                        random_state: int = 42, bins: int = 50) -> dict:
        """
        Analizar muestras de la distribución de Weibull
        """
        if muestras is None:
            muestras = self.generar_muestras(n_muestras, random_state)

        # Estadísticas descriptivas
        estadisticas = {
            'n_muestras': len(muestras),
            'media_muestral': np.mean(muestras),
            'mediana_muestral': np.median(muestras),
            'desv_std_muestral': np.std(muestras, ddof=1),
            'varianza_muestral': np.var(muestras, ddof=1),
            'min': np.min(muestras),
            'max': np.max(muestras),
            'q25': np.percentile(muestras, 25),
            'q75': np.percentile(muestras, 75)
        }

        # Comparar con valores teóricos
        estadisticas['media_teorica'] = self.media()
        estadisticas['mediana_teorica'] = self.mediana()
        estadisticas['desv_std_teorica'] = self.desviacion_estandar()

        # Crear gráficas
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Histograma vs PDF teórica
        ax1.hist(muestras, bins=bins, density=True, alpha=0.7, color='skyblue', 
                edgecolor='black', label='Histograma muestral')

        x_teorico = np.linspace(0, np.max(muestras) * 1.1, 1000)
        ax1.plot(x_teorico, self.pdf(x_teorico), 'r-', linewidth=2, 
                label='PDF teórica')
        ax1.set_title('Histograma de Muestras vs PDF Teórica')
        ax1.set_xlabel('x')
        ax1.set_ylabel('Densidad')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # CDF empírica vs teórica
        muestras_ordenadas = np.sort(muestras)
        cdf_empirica = np.arange(1, len(muestras_ordenadas) + 1) / len(muestras_ordenadas)

        ax2.plot(muestras_ordenadas, cdf_empirica, 'b-', linewidth=2, 
                label='CDF empírica')
        ax2.plot(muestras_ordenadas, self.cdf(muestras_ordenadas), 'r--', linewidth=2,
                label='CDF teórica')
        ax2.set_title('CDF Empírica vs Teórica')
        ax2.set_xlabel('x')
        ax2.set_ylabel('F(x)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Q-Q plot
        stats.probplot(muestras, dist=self.weibull_dist, plot=ax3) # type: ignore
        ax3.set_title('Q-Q Plot')
        ax3.grid(True, alpha=0.3)

        # Boxplot
        ax4.boxplot(muestras, vert=True)
        ax4.set_title('Diagrama de Caja')
        ax4.set_ylabel('Valores')
        ax4.grid(True, alpha=0.3)

        plt.suptitle(f'Análisis de Muestras - Weibull(k={self.k}, λ={self.lambda_param})',
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()

        return estadisticas

    def __str__(self) -> str:
        """Representación en string de la distribución"""
        return f"Distribución de Weibull(k={self.k}, λ={self.lambda_param})"

    def __repr__(self) -> str:
        """Representación técnica de la distribución"""
        return f"DistribucionWeibull(k={self.k}, lambda_param={self.lambda_param})"


def comparar_distribuciones_weibull(parametros_lista: List[Tuple[float, float]],
                                etiquetas: List[str] = None, # type: ignore
                                x_max: float = 5.0,
                                figsize: Tuple[int, int] = (12, 8)) -> None:
    """
    Comparar múltiples distribuciones de Weibull en una sola gráfica

    Parameters:
    -----------
    parametros_lista : List[Tuple[float, float]]
        Lista de tuplas (k, λ) para cada distribución
    etiquetas : List[str], opcional
        Etiquetas para cada distribución
    x_max : float
        Valor máximo para el eje x
    figsize : Tuple[int, int]
        Tamaño de la figura
    """
    if etiquetas is None:
        etiquetas = [f'k={k}, λ={lam}' for k, lam in parametros_lista]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    x = np.linspace(0, x_max, 1000)
    colors = plt.cm.tab10(np.linspace(0, 1, len(parametros_lista))) # type: ignore

    for i, ((k, lam), etiqueta) in enumerate(zip(parametros_lista, etiquetas)):
        weibull = DistribucionWeibull(k, lam)

        ax1.plot(x, weibull.pdf(x), color=colors[i], linewidth=2, label=etiqueta)
        ax2.plot(x, weibull.cdf(x), color=colors[i], linewidth=2, label=etiqueta)

    ax1.set_title('Funciones de Densidad de Probabilidad')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.set_title('Funciones de Distribución Acumulativa')
    ax2.set_xlabel('x')
    ax2.set_ylabel('F(x)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.suptitle('Comparación de Distribuciones de Weibull', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()


# Función para ejemplos de uso
def ejemplos_uso():
    """
    Función con ejemplos de uso de la clase DistribucionWeibull
    """
    print("=== EJEMPLOS DE USO DE LA DISTRIBUCIÓN DE WEIBULL ===\n")

    # Ejemplo 1: Creación básica
    print("1. Creación de una distribución de Weibull")
    print("-" * 40)
    weibull = DistribucionWeibull(k=2.0, lambda_param=1.5)
    print(f"Distribución creada: {weibull}")
    print(f"Resumen estadístico:")
    resumen = weibull.resumen_estadistico()

    for categoria, datos in resumen.items():
        print(f"\n{categoria.replace('_', ' ').title()}:")
        for nombre, valor in datos.items():
            print(f"  {nombre}: {valor:.4f}")

    # Ejemplo 2: Evaluación de funciones
    print("\n\n2. Evaluación de funciones en puntos específicos")
    print("-" * 50)
    x_test = [0.5, 1.0, 1.5, 2.0]
    print(f"Valores de x: {x_test}")
    print(f"PDF f(x):     {[weibull.pdf(x) for x in x_test]}")
    print(f"CDF F(x):     {[weibull.cdf(x) for x in x_test]}")
    print(f"Supervivencia S(x): {[weibull.survival_function(x) for x in x_test]}")
    print(f"Riesgo h(x):  {[weibull.hazard_function(x) for x in x_test]}")

    # Ejemplo 3: Generación de muestras
    print("\n\n3. Generación y análisis de muestras")
    print("-" * 40)
    muestras = weibull.generar_muestras(1000, random_state=42)
    print(f"Generadas {len(muestras)} muestras")
    print(f"Media muestral: {np.mean(muestras):.4f} (teórica: {weibull.media():.4f})")
    print(f"Desv. estándar muestral: {np.std(muestras, ddof=1):.4f} (teórica: {weibull.desviacion_estandar():.4f})")

    return weibull


if __name__ == "__main__":
    # Ejecutar ejemplos cuando se ejecute el script directamente
    weibull_ejemplo = ejemplos_uso()

    # Crear las gráficas
    print("\n\nGenerando gráficas...")
    weibull_ejemplo.graficar_distribucion()
    weibull_ejemplo.graficar_comparacion_parametros()

    # Analizar muestras
    estadisticas = weibull_ejemplo.analizar_muestras()
    print("\n\nEstadísticas de las muestras generadas:")
    for key, value in estadisticas.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")
