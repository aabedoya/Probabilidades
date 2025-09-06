# 🌪️ ANÁLISIS WEIBULL - GUÍA RÁPIDA DE USO

## 🚀 OPCIÓN 1: USO SÚPER SIMPLE (Recomendado)

### Windows:
```cmd
# Doble clic en ejecutar.bat
ejecutar.bat

# O desde cmd/PowerShell:
ejecutar.bat
ejecutar.bat auto    # Modo automático
```

### Cualquier Sistema:
```bash
# Una sola línea - hace todo automáticamente:
python auto_weibull.py

# Modo automático:
python auto_weibull.py auto
```

## 🛠️ OPCIÓN 2: SETUP MANUAL (Una sola vez)

```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno
## Windows:
.venv\Scripts\activate
## Mac/Linux:
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar análisis
python analisis_detallado_sustitucion.py
```

## 🔍 VERIFICAR QUE TODO FUNCIONE

```bash
# Verificar Python y dependencias:
python -c "import pandas, numpy, scipy, matplotlib; print('✅ Todo OK')"
```

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "ModuleNotFoundError"
```bash
# Instalar dependencia faltante:
pip install nombre_del_modulo
```

### Error: "Python not found"
```bash
# Verificar instalación de Python:
python --version
# o
python3 --version
# o
py --version
```

### Resetear completamente:
```bash
# Borrar entorno y empezar de nuevo:
rmdir /s .venv     # Windows
rm -rf .venv       # Mac/Linux

# Luego ejecutar auto_weibull.py de nuevo
```

## 🧪 EJECUTAR PRUEBAS (TESTING)

### Windows (Súper fácil):
```cmd
# Menú interactivo con todas las opciones:
ejecutar_tests.bat
```

### Comandos manuales:
```bash
# Pruebas básicas:
python -m pytest test_weibull_basico.py -v

# Con cobertura de código:
python -m pytest test_weibull_basico.py --cov=analisis_detallado_sustitucion --cov-report=term-missing

# Solo pruebas rápidas:
python -m pytest test_weibull_basico.py -m "not slow"

# Reporte HTML de cobertura:
python -m pytest test_weibull_basico.py --cov=analisis_detallado_sustitucion --cov-report=html
```

## 📊 ARCHIVOS DEL PROYECTO

```
Probabilidades/
├── 📄 Datos.xlsx                          # Datos meteorológicos
├── 🐍 analisis_detallado_sustitucion.py   # Script principal
├── 🚀 auto_weibull.py                     # Auto-configurador
├── 🔧 ejecutar.bat                        # Script Windows
├── 🧪 ejecutar_tests.bat                  # Script pruebas Windows
├── 🧪 test_weibull_basico.py              # Pruebas unitarias
├── ⚙️ pytest.ini                          # Configuración pytest
├── 📋 requirements.txt                    # Lista de dependencias
├── 📁 .venv/                              # Entorno virtual (auto-creado)
├── 📁 htmlcov/                            # Reportes HTML cobertura (auto-creado)
└── 📖 GUIA_USO.md                         # Este archivo
```

## 🎯 MODOS DE EJECUCIÓN

1. **Interactivo**: Tú eliges los municipios
2. **Automático**: Usa Riohacha vs Valledupar (agrega `auto`)

## 💡 TIPS IMPORTANTES

- ✅ **Siempre usar** `auto_weibull.py` para simplicidad máxima
- ✅ El archivo `Datos.xlsx` debe estar en la misma carpeta
- ✅ Internet requerido solo la primera vez (para instalar paquetes)
- ✅ Una vez instalado, funciona sin internet

## 🌟 VENTAJAS DE ESTE SETUP

1. **Un comando**: `python auto_weibull.py` hace todo
2. **Automático**: Instala lo que falta
3. **Portable**: Funciona en cualquier computadora
4. **Limpio**: No afecta otras instalaciones de Python
5. **Reproducible**: Mismos resultados en todas las máquinas
