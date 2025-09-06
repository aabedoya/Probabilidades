@echo off
REM ===================================================
REM Script de comandos pytest para Proyecto Weibull
REM ===================================================

set PYTHON_EXE="C:/Users/neo/OneDrive/Documentos/Probabilidades/.venv/Scripts/python.exe"

echo 🧪 COMANDOS PYTEST DISPONIBLES
echo ===============================
echo.
echo 1. Ejecutar todas las pruebas basicas
echo 2. Ejecutar con cobertura de codigo
echo 3. Ejecutar solo pruebas rapidas (sin lentas)
echo 4. Ejecutar con reporte HTML de cobertura
echo 5. Ejecutar en modo verbose detallado
echo 6. Salir
echo.

:menu
set /p opcion="Selecciona una opcion (1-6): "

if "%opcion%"=="1" goto pruebas_basicas
if "%opcion%"=="2" goto pruebas_cobertura
if "%opcion%"=="3" goto pruebas_rapidas
if "%opcion%"=="4" goto reporte_html
if "%opcion%"=="5" goto verbose_detallado
if "%opcion%"=="6" goto salir

echo ❌ Opcion invalida, intenta de nuevo
goto menu

:pruebas_basicas
echo 🚀 Ejecutando pruebas basicas...
%PYTHON_EXE% -m pytest test_weibull_basico.py -v
echo.
goto menu

:pruebas_cobertura
echo 📊 Ejecutando pruebas con cobertura de codigo...
%PYTHON_EXE% -m pytest test_weibull_basico.py --cov=analisis_detallado_sustitucion --cov-report=term-missing
echo.
goto menu

:pruebas_rapidas
echo ⚡ Ejecutando solo pruebas rapidas...
%PYTHON_EXE% -m pytest test_weibull_basico.py -v -m "not slow"
echo.
goto menu

:reporte_html
echo 🌐 Generando reporte HTML de cobertura...
%PYTHON_EXE% -m pytest test_weibull_basico.py --cov=analisis_detallado_sustitucion --cov-report=html
echo ✅ Reporte HTML generado en: htmlcov/index.html
echo.
goto menu

:verbose_detallado
echo 🔍 Ejecutando pruebas con detalle maximo...
%PYTHON_EXE% -m pytest test_weibull_basico.py -vvv --tb=long --capture=no
echo.
goto menu

:salir
echo ✅ Saliendo del script de pruebas
pause
exit
