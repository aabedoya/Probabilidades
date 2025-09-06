# Proyecto de Distribución de Weibull

## 📊 Descripción

Este proyecto implementa un análisis completo de la **distribución de probabilidad de Weibull**, incluyendo su implementación matemática, visualizaciones interactivas y aplicaciones prácticas en diversos campos como análisis de confiabilidad, meteorología y control de calidad.

## 🎯 Objetivos

- Implementar la distribución de Weibull desde sus fundamentos matemáticos
- Proporcionar herramientas de análisis y visualización
- Demostrar aplicaciones prácticas en diferentes campos
- Crear ejemplos educativos e interactivos

## 📁 Estructura del Proyecto

```
Probabilidades/
├── distribucion_weibull.py    # Implementación principal de la clase DistribucionWeibull
├── ejemplos_weibull.py        # Ejemplos prácticos y aplicaciones
├── notebook_weibull.ipynb     # Notebook interactivo con análisis completo
├── README.md                  # Este archivo
└── otros archivos...
```

## 🔧 Instalación y Requisitos

### Requisitos del sistema
- Python 3.8 o superior
- Entorno virtual (recomendado)

### Dependencias
```bash
pip install numpy scipy matplotlib pandas seaborn
```

Las librerías principales utilizadas son:
- **numpy**: Cálculos numéricos y arrays
- **scipy**: Funciones estadísticas avanzadas
- **matplotlib**: Visualización de datos
- **pandas**: Manipulación de datos
- **seaborn**: Visualizaciones estadísticas mejoradas

### Configuración del proyecto
```bash
# Clonar o descargar el proyecto
cd Probabilidades

# Crear entorno virtual (opcional pero recomendado)
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En macOS/Linux:
source .venv/bin/activate

# Instalar dependencias
pip install numpy scipy matplotlib pandas seaborn
```

## 📚 Fundamentos Matemáticos

### Función de Densidad de Probabilidad (PDF)

La distribución de Weibull está definida por:

```
f(x) = (k/λ) * (x/λ)^(k-1) * e^(-(x/λ)^k)
```

donde:
- `k > 0`: **parámetro de forma** (shape parameter)
- `λ > 0`: **parámetro de escala** (scale parameter)
- `x ≥ 0`: variable aleatoria

### Función de Distribución Acumulativa (CDF)

```
F(x) = 1 - e^(-(x/λ)^k)
```

### Función de Supervivencia (Confiabilidad)

```
S(x) = e^(-(x/λ)^k)
```

### Función de Riesgo (Hazard Function)

```
h(x) = (k/λ) * (x/λ)^(k-1)
```

## 🚀 Uso Básico

### Ejemplo rápido

```python
from distribucion_weibull import DistribucionWeibull

# Crear una distribución de Weibull
weibull = DistribucionWeibull(k=2.0, lambda_param=1.5)

# Calcular probabilidades
prob_density = weibull.pdf(1.0)         # Densidad en x=1
prob_cumulative = weibull.cdf(1.0)      # Probabilidad acumulada hasta x=1
reliability = weibull.survival_function(1.0)  # Confiabilidad en x=1

# Generar muestras aleatorias
muestras = weibull.generar_muestras(1000, random_state=42)

# Obtener estadísticas
print(f"Media: {weibull.media():.3f}")
print(f"Mediana: {weibull.mediana():.3f}")
print(f"Desviación estándar: {weibull.desviacion_estandar():.3f}")

# Crear visualizaciones
weibull.graficar_distribucion()
```

### Análisis de muestras

```python
# Analizar muestras generadas
estadisticas = weibull.analizar_muestras(n_muestras=5000)
print(estadisticas)
```

### Comparar distribuciones

```python
from distribucion_weibull import comparar_distribuciones_weibull

# Comparar diferentes parámetros
parametros = [(1.0, 1.0), (2.0, 1.0), (3.0, 1.0)]
etiquetas = ['Exponencial', 'Rayleigh', 'k=3.0']
comparar_distribuciones_weibull(parametros, etiquetas)
```

## 📖 Casos de Uso y Aplicaciones

### 1. Análisis de Confiabilidad
```python
# Modelar vida útil de componentes electrónicos
componente = DistribucionWeibull(k=2.3, lambda_param=10000)  # 10,000 horas promedio

# Calcular confiabilidad a 5,000 horas
confiabilidad = componente.survival_function(5000)
print(f"Confiabilidad: {confiabilidad:.3f}")
```

### 2. Análisis de Velocidad del Viento
```python
# Modelar velocidad del viento para energía eólica
viento = DistribucionWeibull(k=2.1, lambda_param=8.5)  # k=2.1, λ=8.5 m/s

# Probabilidad de velocidades útiles (>3 m/s)
prob_util = 1 - viento.cdf(3)
print(f"Probabilidad de vientos útiles: {prob_util:.3f}")
```

### 3. Control de Calidad
```python
# Modelar tiempo de vida de productos
producto = DistribucionWeibull(k=1.8, lambda_param=2000)

# Calcular porcentaje que cumple especificación mínima
especificacion = 1500  # horas mínimas
cumple_spec = producto.survival_function(especificacion)
print(f"% que cumple especificación: {cumple_spec*100:.1f}%")
```

## 📊 Interpretación de Parámetros

### Parámetro de forma (k)
- **k < 1**: Mortalidad infantil (tasa de fallas decreciente)
- **k = 1**: Fallas aleatorias (distribución exponencial)
- **k > 1**: Desgaste/envejecimiento (tasa de fallas creciente)
- **k ≈ 2**: Distribución de Rayleigh
- **k ≈ 3.6**: Aproximación a distribución normal

### Parámetro de escala (λ)
- Controla la escala temporal de la distribución
- Valores más altos → distribución "estirada" hacia la derecha
- Valores más bajos → distribución "comprimida" hacia la izquierda

## 📈 Archivos del Proyecto

### `distribucion_weibull.py`
Implementación principal que incluye:
- Clase `DistribucionWeibull` con todos los métodos estadísticos
- Cálculo de PDF, CDF, supervivencia y función de riesgo
- Generación de muestras aleatorias
- Estadísticas descriptivas (media, mediana, moda, varianza)
- Múltiples opciones de visualización
- Análisis comparativo de parámetros

### `ejemplos_weibull.py`
Casos de uso prácticos:
- **Análisis de confiabilidad**: Componentes electrónicos con diferentes comportamientos
- **Velocidad del viento**: Aplicaciones en energía eólica
- **Control de calidad**: Análisis de procesos de manufactura
- **Análisis de supervivencia**: Estudios médicos y epidemiológicos
- **Comparación de parámetros**: Efectos visuales de k y λ

### `notebook_weibull.ipynb`
Notebook interactivo que incluye:
- Tutorial paso a paso
- Ejercicios prácticos resueltos
- Visualizaciones interactivas
- Comparaciones de distribuciones
- Casos de estudio detallados

## 🔍 Funcionalidades Avanzadas

### Análisis Estadístico Completo
- Cálculo de momentos (media, varianza, asimetría, curtosis)
- Percentiles y cuartiles
- Intervalos de confianza
- Estadísticas de orden

### Visualizaciones Avanzadas
- Gráficas de densidad y distribución acumulativa
- Curvas de supervivencia y funciones de riesgo
- Comparaciones paramétricas
- Análisis de muestras con Q-Q plots
- Histogramas vs curvas teóricas

### Aplicaciones Específicas
- Análisis de confiabilidad industrial
- Modelado meteorológico
- Estudios de supervivencia médica
- Control de calidad estadístico
- Análisis de fatiga de materiales

## 🧪 Ejemplos de Validación

### Test de Bondad de Ajuste
```python
# Generar datos y verificar ajuste
muestras = weibull.generar_muestras(1000)
estadisticas = weibull.analizar_muestras(muestras)

# Comparar estadísticas muestrales vs teóricas
print(f"Media teórica: {weibull.media():.3f}")
print(f"Media muestral: {estadisticas['media_muestral']:.3f}")
```

### Convergencia de Muestras
```python
# Verificar convergencia con diferentes tamaños de muestra
for n in [100, 1000, 10000]:
    muestras = weibull.generar_muestras(n)
    media_muestral = np.mean(muestras)
    print(f"n={n:5d}: media = {media_muestral:.4f}")
```

## 📚 Referencias Teóricas

1. **Weibull, W.** (1951). "A statistical distribution function of wide applicability". Journal of Applied Mechanics, 18(3), 293-297.

2. **Rinne, H.** (2008). "The Weibull Distribution: A Handbook". CRC Press.

3. **Murthy, D.N.P., Xie, M., & Jiang, R.** (2004). "Weibull Models". John Wiley & Sons.

4. **Lawless, J.F.** (2011). "Statistical Models and Methods for Lifetime Data". John Wiley & Sons.

## 🤝 Contribuciones

Este proyecto está abierto a contribuciones. Las áreas de mejora incluyen:

- Nuevos métodos de estimación de parámetros
- Aplicaciones adicionales en diferentes campos
- Mejoras en visualizaciones
- Optimizaciones de rendimiento
- Documentación adicional

## 📞 Contacto y Soporte

Para preguntas, sugerencias o reportar problemas:

- **Proyecto**: Distribución de Weibull
- **Curso**: Probabilidades
- **Fecha**: 3 de septiembre de 2025

## 📜 Licencia

Este proyecto está desarrollado con fines educativos para el curso de Probabilidades.

---

**¡Disfruta explorando la distribución de Weibull!** 🎯📊✨

*La distribución de Weibull: versátil, potente y fundamental en el análisis estadístico moderno.*
