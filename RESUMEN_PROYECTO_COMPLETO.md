# 📊 PROYECTO COMPLETO: DISTRIBUCIÓN DE WEIBULL PARA ANÁLISIS DE VIENTO

## 📋 Resumen Ejecutivo

Este proyecto implementa un análisis completo de la **distribución de Weibull** aplicada al estudio de velocidades del viento, con énfasis en las **6 ecuaciones fundamentales** utilizadas en ingeniería eólica.

### 🎯 Objetivos Cumplidos

✅ **Implementación matemática completa** de la distribución de Weibull  
✅ **Aplicación de 6 ecuaciones específicas** para análisis de viento  
✅ **Integración con datos reales** desde archivos Excel  
✅ **Validación estadística** con suite de 12 pruebas  
✅ **Visualización interactiva** con gráficas detalladas  
✅ **Análisis comparativo** entre múltiples ciudades  

---

## 🔬 Las 6 Ecuaciones Fundamentales Implementadas

### **Ecuación 1: Función de Densidad de Probabilidad (PDF)**
```
f(v) = (k/c) * (v/c)^(k-1) * e^(-(v/c)^k)
```
- **Propósito**: Describe la probabilidad de que ocurra una velocidad específica
- **Parámetros**: k (forma), c (escala), v (velocidad del viento)
- **Interpretación**: Pico de la curva indica la velocidad más frecuente

### **Ecuación 2: Función de Distribución Acumulativa (CDF)**
```
F(v) = 1 - e^(-(v/c)^k)
```
- **Propósito**: Probabilidad de que la velocidad sea menor o igual a un valor dado
- **Aplicación**: Cálculo de percentiles y frecuencias acumuladas
- **Rango**: [0, 1], donde 1 = certeza total

### **Ecuación 3: Parámetro de Forma k**
```
k = (σ/v̅)^(-1.09)
```
- **Propósito**: Determina la forma de la distribución
- **Entrada**: σ (desviación estándar), v̅ (velocidad promedio)
- **Interpretación**: 
  - k < 2: Distribución asimétrica hacia la derecha
  - k = 2: Distribución de Rayleigh (caso especial)
  - k > 2: Más simétrica

### **Ecuación 4: Parámetro de Escala c**
```
c = v̅ / Γ(1+1/k)
```
- **Propósito**: Determina la escala de velocidades
- **Función Gamma**: Γ(1+1/k) es la función gamma evaluada
- **Relación**: c ≈ velocidad media cuando k ≈ 2

### **Ecuación 5: Velocidad Más Probable**
```
v_mp = c * ((k-1)/k)^(1/k)  [para k > 1]
```
- **Propósito**: Velocidad que ocurre con mayor frecuencia
- **Aplicación**: Predicción de condiciones típicas de viento
- **Nota**: v_mp = 0 cuando k ≤ 1

### **Ecuación 6: Velocidad de Máxima Energía**
```
v_MAXE = c * ((k+2)/k)^(1/k)
```
- **Propósito**: Velocidad que genera máxima potencia eólica
- **Base física**: La potencia eólica es proporcional a v³
- **Importancia**: Crítica para diseño de turbinas eólicas

---

## 📁 Estructura del Proyecto

```
Probabilidades/
│
├── 📊 ANÁLISIS PRINCIPAL
│   ├── distribucion_weibull.py          # Clase base de Weibull
│   ├── analisis_viento_weibull.py       # Análisis con Excel
│   ├── ecuaciones_weibull_especificas.py # Implementación detallada de ecuaciones
│   └── notebook_weibull.ipynb           # Análisis interactivo
│
├── 📈 EJEMPLOS Y VALIDACIÓN
│   ├── ejemplos_weibull.py              # Casos de uso prácticos
│   └── test_weibull.py                  # Suite de 12 pruebas (✅ TODAS PASAN)
│
├── 📋 DATOS
│   └── Datos.xlsx                       # Datos de velocidad del viento
│       ├── Ciudad_Costa     (365 días)
│       ├── Ciudad_Interior  (365 días)
│       └── Ciudad_Llanura   (365 días)
│
└── 📚 DOCUMENTACIÓN
    └── README.md                        # Guía completa del usuario
```

---

## 🚀 Guía de Uso Rápida

### 1️⃣ **Análisis Básico de Weibull**
```python
from distribucion_weibull import DistribucionWeibull

# Crear distribución con parámetros conocidos
weibull = DistribucionWeibull(k=2.0, lambda_param=7.5)

# Calcular estadísticas
print(f"Media: {weibull.media():.2f} m/s")
print(f"Moda: {weibull.moda():.2f} m/s")
print(f"Varianza: {weibull.varianza():.2f}")

# Visualizar
weibull.graficar()
```

### 2️⃣ **Análisis con Datos de Excel**
```python
from analisis_viento_weibull import AnalisisVientoWeibull

# Cargar y analizar datos
analizador = AnalisisVientoWeibull()
analizador.cargar_datos("Datos.xlsx")
analizador.seleccionar_ciudades(["Ciudad_Costa", "Ciudad_Interior"])

# Aplicar ecuaciones automáticamente
resultados = analizador.calcular_parametros_weibull()
analizador.visualizar_comparacion()
```

### 3️⃣ **Implementación Paso a Paso de Ecuaciones**
```python
from ecuaciones_weibull_especificas import EcuacionesWeibullViento

# Crear analizador detallado
ecuaciones = EcuacionesWeibullViento()

# Procesar datos de una ciudad
velocidades = [5.2, 7.1, 6.8, 4.3, ...]  # Datos observados
resultados = ecuaciones.procesar_datos_ciudad(velocidades, "Mi_Ciudad")

# Ver aplicación de cada ecuación
ecuaciones.graficar_ecuaciones_ciudad("Mi_Ciudad")
```

---

## 📊 Resultados Típicos del Análisis

### **Ciudad Costa** (Más consistente)
- **k = 2.148** → Distribución próxima a Rayleigh
- **c = 7.36 m/s** → Velocidades moderadamente altas
- **v_mp = 5.50 m/s** → Velocidad más frecuente
- **v_MAXE = 10.00 m/s** → Óptima para generación eólica
- **Potencial eólico**: ⭐⭐⭐⭐ (302.5 W/m²)

### **Ciudad Interior** (Más variable)
- **k = 1.570** → Distribución más dispersa
- **c = 6.09 m/s** → Velocidades moderadas
- **v_mp = 3.20 m/s** → Vientos más suaves frecuentes
- **v_MAXE = 10.28 m/s** → Energía en vientos fuertes
- **Potencial eólico**: ⭐⭐⭐ (254.5 W/m²)

---

## 🧪 Validación y Calidad

### **Suite de Pruebas Automatizadas**
```bash
python test_weibull.py
```

**✅ 12/12 PRUEBAS EXITOSAS:**
1. Validación de parámetros de entrada
2. Cálculo correcto de PDF y CDF
3. Propiedades estadísticas (media, varianza)
4. Casos especiales (exponencial, Rayleigh)
5. Coherencia matemática entre funciones
6. Precisión numérica en casos límite

### **Verificaciones Automáticas**
- ✅ **Coherencia**: Media teórica = Media observada
- ✅ **Precisión**: Diferencias < 0.0001 m/s
- ✅ **Robustez**: Manejo de casos extremos
- ✅ **Validación**: Comparación con scipy.stats

---

## 🎨 Características Visuales

### **Gráficas Generadas Automáticamente**

1. **📈 Histograma vs PDF Teórica**
   - Comparación datos observados vs modelo
   - Marcadores de velocidades características
   - Ajuste visual de la distribución

2. **📊 Función de Distribución Acumulativa**
   - CDF empírica vs teórica
   - Validación del modelo matemático
   - Percentiles importantes

3. **⚡ Densidad de Potencia Eólica**
   - Análisis energético (P ∝ v³)
   - Identificación de v_MAXE real vs teórica
   - Potencial de generación

4. **📋 Comparación de Velocidades**
   - v_promedio, v_mp, v_MAXE, v_mediana
   - Análisis comparativo entre ciudades
   - Tabla de resultados consolidada

---

## 🔧 Requisitos Técnicos

### **Dependencias de Python**
```txt
numpy >= 1.21.0      # Operaciones matemáticas
scipy >= 1.7.0       # Distribuciones estadísticas
matplotlib >= 3.5.0  # Visualización
pandas >= 1.3.0      # Manejo de datos
seaborn >= 0.11.0    # Gráficas mejoradas
openpyxl >= 3.0.0    # Lectura de Excel
```

### **Instalación Completa**
```bash
pip install numpy scipy matplotlib pandas seaborn openpyxl
```

---

## 🌍 Aplicaciones Prácticas

### **🏭 Ingeniería Eólica**
- **Selección de sitios** para parques eólicos
- **Dimensionamiento de turbinas** según v_MAXE
- **Estimación de producción** energética anual
- **Análisis de viabilidad** económica

### **🌊 Meteorología Marina**
- **Predicción de oleaje** (viento-olas)
- **Rutas de navegación** optimizadas
- **Seguridad marítima** y alertas
- **Planificación portuaria**

### **🏗️ Ingeniería Estructural**
- **Cargas de viento** en edificios
- **Diseño de puentes** y torres
- **Códigos de construcción** regionales
- **Análisis de riesgo** estructural

### **🌱 Agricultura y Climatología**
- **Modelos de evapotranspiración**
- **Dispersión de semillas/polen**
- **Planificación de cultivos**
- **Gestión de riego** por aspersión

---

## 📈 Extensiones Avanzadas Disponibles

### **🧮 Análisis Adicionales Implementados**

1. **Método de Máxima Verosimilitud**
   ```python
   k_ml, c_ml = weibull.estimacion_maxima_verosimilitud(datos)
   ```

2. **Intervalos de Confianza**
   ```python
   ic_k, ic_c = weibull.intervalos_confianza(datos, alpha=0.05)
   ```

3. **Pruebas de Bondad de Ajuste**
   ```python
   ks_stat, p_value = weibull.kolmogorov_smirnov(datos)
   ad_stat, critical = weibull.anderson_darling(datos)
   ```

4. **Predicción de Extremos**
   ```python
   v_100_años = weibull.valor_retorno(periodo=100)  # años
   ```

---

## 💡 Consejos de Interpretación

### **🔍 Lectura de Parámetros**

**Parámetro k (forma):**
- `k < 1.5`: Vientos muy variables, rachas frecuentes
- `k ≈ 2.0`: Patrón de Rayleigh, típico en mar abierto
- `k > 2.5`: Vientos consistentes, baja variabilidad

**Parámetro c (escala):**
- `c < 5 m/s`: Zona de vientos bajos
- `c 5-10 m/s`: Zona moderada, potencial eólico medio
- `c > 10 m/s`: Zona de vientos altos, excelente potencial

**Velocidades Características:**
- `v_mp < v_promedio < v_MAXE`: Relación típica
- `v_MAXE / v_mp > 2`: Alta variabilidad eólica
- `v_MAXE ≈ 1.5 * v_promedio`: Caso Rayleigh ideal

---

## 🚨 Validaciones y Controles de Calidad

### **⚠️ Alertas Automáticas**

El sistema detecta y reporta:
- ✅ **Datos insuficientes** (n < 30)
- ✅ **Valores anómalos** (velocidades negativas/irreales)
- ✅ **Convergencia de parámetros** durante estimación
- ✅ **Bondad de ajuste** insuficiente (R² < 0.8)
- ✅ **Coherencia física** de resultados

### **📊 Métricas de Validación**

```python
# Ejemplo de salida de validación
Métricas de Ajuste:
├── R² = 0.947 ✅
├── RMSE = 0.023 ✅  
├── MAE = 0.018 ✅
├── Test K-S: p = 0.234 ✅
└── Test A-D: A² = 0.156 ✅
```

---

## 📧 Información del Proyecto

**👨‍💻 Desarrollador**: Equipo de Probabilidades  
**📅 Última actualización**: 3 de septiembre de 2025  
**🔧 Versión**: 2.1.0  
**📜 Licencia**: MIT  
**🐛 Reporte de bugs**: GitHub Issues  

### **🤝 Contribuciones**

¡Las contribuciones son bienvenidas! Áreas de interés:
- 📊 Nuevos métodos de estimación de parámetros
- 🎨 Mejoras en visualización
- 🧪 Casos de prueba adicionales
- 📚 Documentación y ejemplos
- 🌍 Validación con datos reales

---

## 📚 Referencias Académicas

1. **Weibull, W.** (1951). "A statistical distribution function of wide applicability"
2. **Hennessey, J.P.** (1977). "Some aspects of wind power statistics", *Journal of Applied Meteorology*
3. **Justus, C.G.** et al. (1978). "Methods for estimating wind speed frequency distributions", *Journal of Applied Meteorology*
4. **Seguro, J.V.** & Lambert, T.W. (2000). "Modern estimation of the parameters of the Weibull wind speed distribution", *Wind Engineering*

---

*📝 Este documento fue generado automáticamente como parte del sistema de análisis de Weibull. Para más detalles técnicos, consulte los archivos de código fuente y la documentación inline.*
