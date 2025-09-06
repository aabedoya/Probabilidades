@echo off
echo 🌪️ ACTIVANDO ENTORNO WEIBULL...
echo ======================================

REM Verificar si existe el entorno virtual
if not exist ".venv" (
    echo ⚠️ Entorno virtual no encontrado. Creando...
    python -m venv .venv
    echo ✅ Entorno virtual creado
)

REM Activar entorno
call .venv\Scripts\activate

REM Verificar si están instaladas las dependencias
python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando dependencias...
    pip install pandas numpy scipy matplotlib seaborn openpyxl
    echo ✅ Dependencias instaladas
)

echo 🚀 Entorno listo. Ejecutando análisis...
echo.

REM Ejecutar el script principal
python analisis_detallado_sustitucion.py %*

echo.
echo ✅ Análisis completado
pause
