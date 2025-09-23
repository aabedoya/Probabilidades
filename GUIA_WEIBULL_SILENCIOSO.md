# 📄 Aplicación Weibull Interactiva - Selección de Ciudades + PDF

## 🎯 **Objetivo**
Esta aplicación permite **seleccionar interactivamente 2 ciudades** de tu elección y genera un PDF profesional completo con todo el contenido educativo de análisis Weibull para estudio.

## ✨ **Características Principales**

### 🏙️ **Selección Interactiva de Ciudades**
- **Lista todas las ciudades disponibles** con estadísticas
- **Selección manual** de 2 ciudades diferentes
- **Información previa** de velocidad media y registros por ciudad

### 📚 **Contenido Educativo Completo en PDF**
- **Estadísticas básicas** detalladas para ambas ciudades
- **Parámetros Weibull** con cálculos paso a paso
- **Todas las Semanas 3, 4 y 5** incluidas:
  - 📊 **Semana 3**: Histogramas, variabilidad, parámetros Weibull
  - ⚡ **Semana 4**: Distribución vs histograma, velocidades características
  - 🎯 **Semana 5**: Cuartiles, probabilidades, percentiles

### 🎨 **PDF Profesional**
- Formato educativo completo
- Análisis comparativo entre las ciudades seleccionadas
- Fórmulas matemáticas detalladas
- Explicaciones paso a paso

## 🚀 **Cómo Usar**

### **Ejecutar Aplicación Interactiva**
```bash
python weibull_silencioso.py
```

**Proceso interactivo:**
```
🌪️======================================================================
    ANÁLISIS WEIBULL - GENERACIÓN DE PDF EDUCATIVO
========================================================================
� Genera un PDF completo con todo el análisis educativo
🎯 Selecciona 2 ciudades para el análisis comparativo
📊 PDF incluye todas las semanas y actividades
========================================================================

🏙️ CIUDADES DISPONIBLES PARA ANÁLISIS
==================================================
#   Ciudad          Registros  Vel.Media    Temp.Media
--------------------------------------------------
1   Riohacha        1331       16.84        29.3°C
2   Barranquilla    1705       12.49        27.9°C
3   Cartagena       1705       11.38        28.4°C
4   Valledupar      1332       13.98        29.5°C
5   Santa Marta     1332       11.33        29.1°C

🎯 SELECCIÓN DE CIUDADES
==============================
Debes seleccionar 2 ciudades diferentes para el análisis

📍 Selecciona la ciudad #1:
Ingresa el número (1-5): 1
✅ Riohacha seleccionada

📍 Selecciona la ciudad #2:
Ingresa el número (1-5): 5
✅ Santa Marta seleccionada

🎉 CIUDADES SELECCIONADAS:
   1️⃣ Riohacha
   2️⃣ Santa Marta
```

**Resultado final:**
```
✅ Análisis completado exitosamente
📄 PDF generado: reporte_weibull_silencioso_Riohacha_Santa Marta_20250922_230932.pdf
🏙️ Ciudades analizadas: Riohacha, Santa Marta
🎉 ¡Análisis completado! El PDF contiene todo el contenido educativo.
```

### **Método 2: Usar como Módulo**
```python
from weibull_silencioso import AnalisisWeibullSilencioso

# Crear analizador
analizador = AnalisisWeibullSilencioso("Datos.xlsx")

# Ejecutar análisis completo
if analizador.ejecutar_analisis_completo():
    # Generar PDF
    ruta_pdf = analizador.generar_pdf_silencioso("mi_reporte.pdf")
    print(f"PDF generado: {ruta_pdf}")
```

## 📁 **Archivos Generados**

### **Nombre del PDF**
- Formato: `reporte_weibull_silencioso_[Ciudad1]_[Ciudad2]_[YYYYMMDD_HHMMSS].pdf`
- Ejemplo: `reporte_weibull_silencioso_Riohacha_Cartagena_20250922_230436.pdf`

### **Ubicación**
- Mismo directorio de la aplicación
- Ruta completa mostrada en terminal

## 🏙️ **Ciudades Analizadas**

Por defecto se analizan:
- **Riohacha** (mayor potencial eólico)
- **Cartagena** (comparación)

## 📖 **Contenido del PDF**

### **1. Información General**
- Datos del dataset
- Estadísticas básicas por ciudad

### **2. Parámetros Weibull**
- Cálculo de k (forma) y c (escala)
- Derivaciones matemáticas paso a paso
- Función de densidad f(v)

### **3. Semana 3: Análisis de Variabilidad**
- **Actividad 1**: Histogramas y coeficiente de variación
- **Actividad 2**: Cálculo detallado de parámetros Weibull

### **4. Semana 4: Distribución y Velocidades**
- **Actividad 3**: Distribución Weibull vs histograma
- **Actividad 4**: Velocidades características (v_mp, v_maxE)

### **5. Semana 5: Probabilidades**
- **Actividad 5**: Cuartiles y rango intercuartílico
- **Actividad 6**: Probabilidad entre cuartiles
- **Actividad 7**: Probabilidad superior al percentil 60

## 🎯 **Ventajas para Estudio**

### **📚 Material de Estudio Completo**
- **Todo en un solo PDF** - No necesitas revisar terminal
- **Explicaciones paso a paso** - Ideal para entender cada cálculo
- **Fórmulas completas** - Con sustituciones de valores

### **🎨 Presentación Profesional**
- **Formato educativo** organizado por semanas y actividades
- **Tablas claras** con todos los resultados
- **Cálculos detallados** para cada ciudad

### **🚀 Eficiencia**
- **Ejecución rápida** - Solo se muestra el resultado final
- **Sin interrupciones** - No requiere inputs del usuario
- **Reproducible** - Mismos resultados en cada ejecución

## 🔧 **Requisitos**

- Python 3.7+
- pandas, numpy, matplotlib, scipy
- reportlab (para generación de PDF)
- Archivo `Datos.xlsx` en el mismo directorio

## ✅ **Instalación de Dependencias**

```bash
pip install pandas numpy matplotlib scipy reportlab openpyxl
```

## 📝 **Ejemplo de Uso Completo**

```bash
# 1. Asegurar que tienes el archivo de datos
ls Datos.xlsx

# 2. Ejecutar análisis silencioso
python weibull_silencioso.py

# 3. El PDF se genera automáticamente
# ✅ Análisis completado exitosamente
# 📄 PDF generado: reporte_weibull_silencioso_Riohacha_Cartagena_20250922_230436.pdf

# 4. Abrir el PDF para estudiar
# [El PDF contiene todo el análisis educativo completo]
```

## 🎉 **¡Perfecto para Estudio!**

Esta aplicación es ideal para:
- **Estudiantes** que necesitan el material completo en PDF
- **Profesores** que quieren generar reportes educativos
- **Presentaciones** donde solo se necesita el resultado final
- **Documentación** de análisis de energía eólica

**🎯 Todo el contenido educativo está en el PDF - ¡Perfecto para estudiar sin distracciones de terminal!**