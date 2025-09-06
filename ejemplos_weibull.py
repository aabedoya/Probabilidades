"""
Ejemplos Prácticos y Aplicaciones de la Distribución de Weibull
===============================================================

Este script contiene ejemplos prácticos de aplicación de la distribución de Weibull
en diferentes campos como:
- Análisis de confiabilidad
- Análisis de supervivencia
- Meteorología (velocidad del viento)
- Control de calidad
- Análisis de fatiga de materiales

Autor: Proyecto Probabilidades
Fecha: 3 de septiembre de 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from distribucion_weibull import DistribucionWeibull, comparar_distribuciones_weibull
import seaborn as sns
from typing import List, Tuple

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


def ejemplo_confiabilidad_componentes():
    """
    Ejemplo: Análisis de confiabilidad de componentes electrónicos

    En ingeniería de confiabilidad, la distribución de Weibull se usa para modelar
    el tiempo hasta la falla de componentes. Diferentes valores de k indican:
    - k < 1: Mortalidad infantil (fallas tempranas)
    - k = 1: Fallas aleatorias (distribución exponencial)
    - k > 1: Desgaste/envejecimiento
    """
    print("=== EJEMPLO: ANÁLISIS DE CONFIABILIDAD DE COMPONENTES ===")
    print()

    # Definir tres tipos de componentes con diferentes comportamientos
    componentes = {
        'Semiconductor (k<1)': DistribucionWeibull(k=0.8, lambda_param=1000),  # Mortalidad infantil
        'Resistor (k=1)': DistribucionWeibull(k=1.0, lambda_param=1000),       # Fallas aleatorias
        'Rodamiento (k>1)': DistribucionWeibull(k=3.0, lambda_param=1000)      # Desgaste
    }

    # Crear gráfica de confiabilidad
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    t = np.linspace(0, 2000, 1000)  # Tiempo en horas
    colors = ['red', 'blue', 'green']

    for i, (nombre, weibull) in enumerate(componentes.items()):
        color = colors[i]

        # Función de supervivencia (confiabilidad)
        confiabilidad = weibull.survival_function(t)
        ax1.plot(t, confiabilidad, color=color, linewidth=2, label=nombre)

        # Función de densidad de probabilidad (densidad de fallas)
        pdf = weibull.pdf(t)
        ax2.plot(t, pdf, color=color, linewidth=2, label=nombre)

        # Función de riesgo (tasa de fallas)
        riesgo = weibull.hazard_function(t[t > 0])
        ax3.plot(t[t > 0], riesgo, color=color, linewidth=2, label=nombre)

        # Función de riesgo acumulativo
        t_pos = t[t > 0]
        riesgo_acum = -np.log(weibull.survival_function(t_pos))
        ax4.plot(t_pos, riesgo_acum, color=color, linewidth=2, label=nombre)

    # Configurar gráficas
    ax1.set_title('Función de Confiabilidad R(t)')
    ax1.set_xlabel('Tiempo (horas)')
    ax1.set_ylabel('Confiabilidad')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.set_title('Densidad de Fallas f(t)')
    ax2.set_xlabel('Tiempo (horas)')
    ax2.set_ylabel('Densidad')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    ax3.set_title('Tasa de Fallas h(t)')
    ax3.set_xlabel('Tiempo (horas)')
    ax3.set_ylabel('Tasa de fallas')
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    ax4.set_title('Tasa de Fallas Acumulativa H(t)')
    ax4.set_xlabel('Tiempo (horas)')
    ax4.set_ylabel('H(t)')
    ax4.grid(True, alpha=0.3)
    ax4.legend()

    plt.suptitle('Análisis de Confiabilidad de Componentes', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # Calcular métricas importantes
    print("Métricas de confiabilidad:")
    print("-" * 40)
    for nombre, weibull in componentes.items():
        print(f"\n{nombre}:")
        print(f"  Tiempo medio hasta falla (MTTF): {weibull.media():.1f} horas")
        print(f"  Tiempo mediano hasta falla: {weibull.mediana():.1f} horas")
        print(f"  Confiabilidad a 500 horas: {weibull.survival_function(500):.3f}")
        print(f"  Confiabilidad a 1000 horas: {weibull.survival_function(1000):.3f}")
        print(f"  Confiabilidad a 1500 horas: {weibull.survival_function(1500):.3f}")


def ejemplo_velocidad_viento():
    """
    Ejemplo: Modelado de velocidad del viento para energía eólica

    La distribución de Weibull es muy utilizada en meteorología para modelar
    la velocidad del viento, lo cual es crucial para el diseño de parques eólicos.
    """
    print("\n\n=== EJEMPLO: VELOCIDAD DEL VIENTO PARA ENERGÍA EÓLICA ===")
    print()

    # Datos típicos de velocidad de viento en diferentes ubicaciones
    ubicaciones = {
        'Costa marítima': DistribucionWeibull(k=2.2, lambda_param=7.5),    # Vientos más constantes
        'Llanura': DistribucionWeibull(k=2.0, lambda_param=6.0),           # Vientos moderados
        'Montaña': DistribucionWeibull(k=1.8, lambda_param=8.2)            # Vientos más variables
    }

    # Generar datos de velocidad de viento
    v = np.linspace(0, 20, 1000)  # Velocidad en m/s

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    colors = ['blue', 'green', 'orange']

    # Datos para análisis energético
    resultados_energia = {}

    for i, (ubicacion, weibull) in enumerate(ubicaciones.items()):
        color = colors[i]

        # Distribución de velocidades
        pdf = weibull.pdf(v)
        ax1.plot(v, pdf, color=color, linewidth=2, label=ubicacion)
        ax1.fill_between(v, pdf, alpha=0.3, color=color)

        # Función de distribución acumulativa
        cdf = weibull.cdf(v)
        ax2.plot(v, cdf, color=color, linewidth=2, label=ubicacion)

        # Generar muestras para histograma
        muestras = weibull.generar_muestras(10000, random_state=42)
        ax3.hist(muestras, bins=50, density=True, alpha=0.6, color=color, 
                label=ubicacion, edgecolor='black')

        # Calcular potencia eólica disponible (P ∝ v³)
        # Simplificado: P = 0.5 * densidad_aire * Area * v³
        # Usando densidad del aire = 1.225 kg/m³, Area = 1 m² (normalizado)
        potencia_especifica = 0.5 * 1.225 * v**3  # W/m²
        potencia_promedio = np.trapz(pdf * potencia_especifica, v)

        # Almacenar resultados
        resultados_energia[ubicacion] = {
            'velocidad_media': weibull.media(),
            'velocidad_mediana': weibull.mediana(),
            'potencia_promedio': potencia_promedio,
            'factor_capacidad': potencia_promedio / (0.5 * 1.225 * weibull.media()**3) # type: ignore
        }

        print(f"{ubicacion}:")
        print(f"  Velocidad media: {weibull.media():.2f} m/s")
        print(f"  Velocidad mediana: {weibull.mediana():.2f} m/s")
        print(f"  Potencia específica promedio: {potencia_promedio:.1f} W/m²")
        print(f"  % de tiempo con v > 3 m/s: {(1-weibull.cdf(3))*100:.1f}%")
        print(f"  % de tiempo con v > 12 m/s: {(1-weibull.cdf(12))*100:.1f}%")
        print()

    # Gráfica de potencia vs velocidad
    v_potencia = np.linspace(0, 15, 100)
    potencia_teorica = 0.5 * 1.225 * v_potencia**3
    ax4.plot(v_potencia, potencia_teorica, 'k-', linewidth=2, label='P ∝ v³')
    ax4.axhline(y=1000, color='red', linestyle='--', alpha=0.7, label='1 kW/m²')
    ax4.axvline(x=3, color='red', linestyle=':', alpha=0.7, label='v_cut-in = 3 m/s')
    ax4.axvline(x=12, color='red', linestyle=':', alpha=0.7, label='v_rated = 12 m/s')

    # Configurar gráficas
    ax1.set_title('Distribución de Velocidades del Viento')
    ax1.set_xlabel('Velocidad (m/s)')
    ax1.set_ylabel('Densidad de probabilidad')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.set_title('Función de Distribución Acumulativa')
    ax2.set_xlabel('Velocidad (m/s)')
    ax2.set_ylabel('Probabilidad acumulada')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    ax3.set_title('Histograma de Muestras Simuladas')
    ax3.set_xlabel('Velocidad (m/s)')
    ax3.set_ylabel('Frecuencia relativa')
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    ax4.set_title('Potencia Eólica Específica')
    ax4.set_xlabel('Velocidad (m/s)')
    ax4.set_ylabel('Potencia (W/m²)')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    ax4.set_ylim(0, 2000)

    plt.suptitle('Análisis de Velocidad del Viento para Energía Eólica', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()


def ejemplo_control_calidad():
    """
    Ejemplo: Control de calidad en procesos de manufactura

    La distribución de Weibull se usa para modelar la distribución de defectos
    o el tiempo de vida de productos manufacturados.
    """
    print("\n\n=== EJEMPLO: CONTROL DE CALIDAD EN MANUFACTURA ===")
    print()

    # Simular tres procesos de manufactura con diferentes niveles de calidad
    procesos = {
        'Proceso A (Excelente)': DistribucionWeibull(k=4.0, lambda_param=1000),
        'Proceso B (Bueno)': DistribucionWeibull(k=2.5, lambda_param=800),
        'Proceso C (Mejorable)': DistribucionWeibull(k=1.5, lambda_param=600)
    }

    # Generar datos de vida útil (en horas de operación)
    n_productos = 1000
    datos_procesos = {}

    for nombre, weibull in procesos.items():
        datos = weibull.generar_muestras(n_productos, random_state=42)
        datos_procesos[nombre] = datos

    # Crear DataFrame para análisis
    df_list = []
    for proceso, datos in datos_procesos.items():
        df_temp = pd.DataFrame({
            'vida_util': datos,
            'proceso': proceso
        })
        df_list.append(df_temp)

    df_calidad = pd.concat(df_list, ignore_index=True)

    # Análisis estadístico
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    # Boxplot comparativo
    df_calidad.boxplot(column='vida_util', by='proceso', ax=ax1)
    ax1.set_title('Distribución de Vida Útil por Proceso')
    ax1.set_xlabel('Proceso')
    ax1.set_ylabel('Vida útil (horas)')

    # Histogramas
    for i, (proceso, datos) in enumerate(datos_procesos.items()):
        ax2.hist(datos, bins=30, alpha=0.7, label=proceso, density=True)
    ax2.set_title('Histogramas de Vida Útil')
    ax2.set_xlabel('Vida útil (horas)')
    ax2.set_ylabel('Densidad')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Curvas de supervivencia (confiabilidad)
    t = np.linspace(0, 1500, 1000)
    for proceso, weibull in procesos.items():
        supervivencia = weibull.survival_function(t)
        ax3.plot(t, supervivencia, linewidth=2, label=proceso)
    ax3.set_title('Curvas de Confiabilidad')
    ax3.set_xlabel('Tiempo (horas)')
    ax3.set_ylabel('Confiabilidad')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Q-Q plot entre procesos
    from scipy import stats
    stats.probplot(datos_procesos['Proceso A (Excelente)'],
                dist=stats.norm, plot=ax4) # type: ignore
    ax4.set_title('Q-Q Plot - Proceso A vs Normal')
    ax4.grid(True, alpha=0.3)

    plt.suptitle('Análisis de Control de Calidad', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # Calcular métricas de calidad
    print("Métricas de calidad por proceso:")
    print("-" * 50)

    especificacion_minima = 500  # Vida útil mínima requerida

    for proceso, weibull in procesos.items():
        datos = datos_procesos[proceso]

        # Estadísticas descriptivas
        media = np.mean(datos)
        mediana = np.median(datos)
        q25, q75 = np.percentile(datos, [25, 75])

        # Métricas de calidad
        prob_cumple_especificacion = weibull.survival_function(especificacion_minima)
        prob_falla_temprana = weibull.cdf(200)  # Falla antes de 200 horas

        print(f"\n{proceso}:")
        print(f"  Media: {media:.1f} horas")
        print(f"  Mediana: {mediana:.1f} horas")
        print(f"  Rango intercuartílico: {q25:.1f} - {q75:.1f} horas")
        print(f"  Probabilidad de cumplir especificación (>{especificacion_minima}h): {prob_cumple_especificacion:.3f}")
        print(f"  Probabilidad de falla temprana (<200h): {prob_falla_temprana:.3f}")
        print(f"  Índice de capacidad (Cp aproximado): {(media - especificacion_minima) / (3 * np.std(datos)):.3f}")


def ejemplo_analisis_supervivencia():
    """
    Ejemplo: Análisis de supervivencia en estudios médicos

    La distribución de Weibull es fundamental en análisis de supervivencia
    para modelar tiempos hasta eventos (muerte, recaída, etc.)
    """
    print("\n\n=== EJEMPLO: ANÁLISIS DE SUPERVIVENCIA MÉDICA ===")
    print()

    # Simular tres grupos de tratamiento
    tratamientos = {
        'Grupo Control': DistribucionWeibull(k=1.2, lambda_param=24),      # Supervivencia base
        'Tratamiento A': DistribucionWeibull(k=1.5, lambda_param=36),     # Tratamiento moderado
        'Tratamiento B': DistribucionWeibull(k=2.0, lambda_param=48)      # Tratamiento efectivo
    }

    # Generar tiempos de supervivencia (en meses)
    n_pacientes = 200
    datos_supervivencia = {}

    np.random.seed(42)
    for grupo, weibull in tratamientos.items():
        # Generar tiempos de supervivencia
        tiempos = weibull.generar_muestras(n_pacientes)

        # Simular censura (algunos pacientes no experimentan el evento durante el estudio)
        tiempo_seguimiento = 60  # 5 años de seguimiento
        censura = np.random.random(n_pacientes) < 0.3  # 30% censurados

        tiempos_observados = np.minimum(tiempos, tiempo_seguimiento)
        eventos = (tiempos <= tiempo_seguimiento) & ~censura

        datos_supervivencia[grupo] = {
            'tiempos': tiempos_observados,
            'eventos': eventos,
            'weibull': weibull
        }

    # Crear gráficas de análisis de supervivencia
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    t = np.linspace(0, 60, 1000)  # Tiempo en meses
    colors = ['red', 'blue', 'green']

    for i, (grupo, datos) in enumerate(datos_supervivencia.items()):
        color = colors[i]
        weibull = datos['weibull']
        tiempos = datos['tiempos']
        eventos = datos['eventos']

        # Curva de supervivencia teórica
        supervivencia_teorica = weibull.survival_function(t)
        ax1.plot(t, supervivencia_teorica, color=color, linewidth=2, 
                label=f'{grupo} (teórica)')

        # Estimador de Kaplan-Meier (supervivencia empírica)
        tiempos_unicos = np.sort(np.unique(tiempos[eventos]))
        supervivencia_km = []

        s_t = 1.0
        for tiempo in tiempos_unicos:
            n_riesgo = np.sum(tiempos >= tiempo)
            n_eventos = np.sum((tiempos == tiempo) & eventos)
            if n_riesgo > 0:
                s_t *= (1 - n_eventos / n_riesgo)
            supervivencia_km.append(s_t)

        if tiempos_unicos.size > 0:
            ax1.step(tiempos_unicos, supervivencia_km, color=color, linestyle='--', 
                    where='post', alpha=0.7, label=f'{grupo} (K-M)')

        # Función de riesgo
        riesgo = weibull.hazard_function(t[t > 0])
        ax2.plot(t[t > 0], riesgo, color=color, linewidth=2, label=grupo)

        # Histograma de tiempos de supervivencia (solo eventos)
        tiempos_eventos = tiempos[eventos]
        if len(tiempos_eventos) > 0:
            ax3.hist(tiempos_eventos, bins=20, alpha=0.6, color=color, 
                    label=grupo, density=True)

    # Tabla de vida
    intervalos = np.arange(0, 61, 12)  # Intervalos de 12 meses
    tabla_vida = pd.DataFrame()

    for grupo, datos in datos_supervivencia.items():
        weibull = datos['weibull']
        supervivencias = [weibull.survival_function(t) for t in intervalos]
        tabla_vida[grupo] = supervivencias

    tabla_vida.index = [f'{i}-{i+12}' for i in intervalos[:-1]] + ['60+'] # type: ignore

    # Mostrar tabla de vida como heatmap
    im = ax4.imshow(tabla_vida.values.T, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax4.set_xticks(range(len(tabla_vida.index)))
    ax4.set_xticklabels(tabla_vida.index)
    ax4.set_yticks(range(len(tabla_vida.columns)))
    ax4.set_yticklabels(tabla_vida.columns)
    ax4.set_title('Tabla de Vida (Probabilidad de Supervivencia)')

    # Añadir valores en el heatmap
    for i in range(len(tabla_vida.columns)):
        for j in range(len(tabla_vida.index)):
            ax4.text(j, i, f'{tabla_vida.iloc[j, i]:.2f}',
                    ha='center', va='center', color='black', fontsize=8)

    plt.colorbar(im, ax=ax4, shrink=0.8)

    # Configurar gráficas
    ax1.set_title('Curvas de Supervivencia')
    ax1.set_xlabel('Tiempo (meses)')
    ax1.set_ylabel('Probabilidad de supervivencia')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_ylim(0, 1)

    ax2.set_title('Funciones de Riesgo')
    ax2.set_xlabel('Tiempo (meses)')
    ax2.set_ylabel('Tasa de riesgo')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    ax3.set_title('Distribución de Tiempos de Supervivencia')
    ax3.set_xlabel('Tiempo (meses)')
    ax3.set_ylabel('Densidad')
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    plt.suptitle('Análisis de Supervivencia Médica', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # Calcular estadísticas de supervivencia
    print("Estadísticas de supervivencia:")
    print("-" * 40)

    for grupo, datos in datos_supervivencia.items():
        weibull = datos['weibull']

        supervivencia_1_año = weibull.survival_function(12)
        supervivencia_3_años = weibull.survival_function(36)
        supervivencia_5_años = weibull.survival_function(60)

        tiempo_mediano = weibull.mediana()
        tiempo_medio = weibull.media()

        print(f"\n{grupo}:")
        print(f"  Tiempo medio de supervivencia: {tiempo_medio:.1f} meses")
        print(f"  Tiempo mediano de supervivencia: {tiempo_mediano:.1f} meses")
        print(f"  Supervivencia a 1 año: {supervivencia_1_año:.3f}")
        print(f"  Supervivencia a 3 años: {supervivencia_3_años:.3f}")
        print(f"  Supervivencia a 5 años: {supervivencia_5_años:.3f}")


def ejemplo_comparacion_parametros():
    """
    Ejemplo: Efecto de los parámetros en la forma de la distribución
    """
    print("\n\n=== EJEMPLO: EFECTO DE LOS PARÁMETROS ===")
    print()

    # Efecto del parámetro de forma k
    print("Efecto del parámetro de forma k:")
    print("- k < 1: Función decreciente (mortalidad infantil)")
    print("- k = 1: Función exponencial (fallas aleatorias)")
    print("- k > 1: Función con moda (desgaste/envejecimiento)")
    print("- k >> 1: Distribución se aproxima a la normal")

    # Crear comparaciones
    parametros_k = [
        (0.5, 1.0, "k=0.5 (Mortalidad infantil)"),
        (1.0, 1.0, "k=1.0 (Exponencial)"),
        (2.0, 1.0, "k=2.0 (Rayleigh)"),
        (3.5, 1.0, "k=3.5 (Desgaste)")
    ]

    parametros_lambda = [
        (2.0, 0.5, "λ=0.5"),
        (2.0, 1.0, "λ=1.0"),
        (2.0, 1.5, "λ=1.5"),
        (2.0, 2.0, "λ=2.0")
    ]

    # Gráficas comparativas
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    x = np.linspace(0, 4, 1000)

    # Efecto de k
    for k, lam, label in parametros_k:
        weibull = DistribucionWeibull(k, lam)
        ax1.plot(x, weibull.pdf(x), linewidth=2, label=label)
        ax2.plot(x, weibull.hazard_function(x[x > 0]), linewidth=2, label=label)

    # Efecto de λ
    for k, lam, label in parametros_lambda:
        weibull = DistribucionWeibull(k, lam)
        ax3.plot(x, weibull.pdf(x), linewidth=2, label=label)
        ax4.plot(x, weibull.cdf(x), linewidth=2, label=label)

    # Configurar gráficas
    ax1.set_title('Efecto del parámetro k en la PDF')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.set_title('Efecto del parámetro k en la función de riesgo')
    ax2.set_xlabel('x')
    ax2.set_ylabel('h(x)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 5)

    ax3.set_title('Efecto del parámetro λ en la PDF')
    ax3.set_xlabel('x')
    ax3.set_ylabel('f(x)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    ax4.set_title('Efecto del parámetro λ en la CDF')
    ax4.set_xlabel('x')
    ax4.set_ylabel('F(x)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.suptitle('Efecto de los Parámetros en la Distribución de Weibull',
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()


def main():
    """
    Función principal que ejecuta todos los ejemplos
    """
    print("PROYECTO DE DISTRIBUCIÓN DE WEIBULL")
    print("=" * 50)
    print("Ejemplos prácticos y aplicaciones")
    print()

    # Ejecutar todos los ejemplos
    ejemplo_confiabilidad_componentes()
    ejemplo_velocidad_viento()
    ejemplo_control_calidad()
    ejemplo_analisis_supervivencia()
    ejemplo_comparacion_parametros()

    print("\n" + "=" * 50)
    print("¡Análisis completado!")
    print("Los ejemplos muestran la versatilidad de la distribución de Weibull")
    print("en diferentes campos de aplicación.")


if __name__ == "__main__":
    main()
