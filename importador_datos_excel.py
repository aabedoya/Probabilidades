"""
Módulo de Importación de Datos Excel para Análisis de Weibull
===========================================================

Este módulo proporciona funciones especializadas para importar y procesar
datos meteorológicos desde archivos Excel, específicamente enfocado en el
análisis de velocidades del viento usando la distribución de Weibull.

Datos soportados:
- Archivos Excel (.xlsx, .xls)
- Datos meteorológicos con columnas de fecha, velocidad del viento y municipio
- Múltiples municipios/ciudades en un mismo archivo
- Filtrado por fechas y criterios de calidad

Autor: Proyecto Probabilidades
Fecha: 3 de septiembre de 2025
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path
import warnings
from datetime import datetime, date


class ImportadorDatosExcel:
    """
    Clase especializada para importar y procesar datos meteorológicos desde Excel
    """
    
    def __init__(self, archivo_excel: str = "Datos.xlsx"):
        """
        Inicializar el importador
        
        Parameters:
        -----------
        archivo_excel : str
            Ruta al archivo Excel con los datos
        """
        self.archivo_excel = archivo_excel
        self.datos_originales = None
        self.datos_procesados = {}
        self.metadatos = {}
        
    def cargar_archivo_excel(self, mostrar_info: bool = True) -> pd.DataFrame:
        """
        Cargar el archivo Excel y realizar validaciones básicas
        
        Parameters:
        -----------
        mostrar_info : bool
            Si mostrar información sobre los datos cargados
            
        Returns:
        --------
        pd.DataFrame
            DataFrame con los datos cargados
        """
        try:
            # Verificar si el archivo existe
            if not Path(self.archivo_excel).exists():
                raise FileNotFoundError(f"❌ No se encontró el archivo: {self.archivo_excel}")
            
            # Cargar datos
            print(f"📁 Cargando datos desde: {self.archivo_excel}")
            self.datos_originales = pd.read_excel(self.archivo_excel)
            
            if mostrar_info:
                self._mostrar_informacion_basica()
            
            # Validar columnas requeridas
            self._validar_estructura_datos()
            
            # Procesar fechas si es necesario
            self._procesar_columna_fecha()
            
            return self.datos_originales
            
        except Exception as e:
            print(f"❌ Error al cargar el archivo Excel: {e}")
            raise
    
    def _mostrar_informacion_basica(self) -> None:
        """Mostrar información básica sobre los datos cargados"""
        if self.datos_originales is None:
            return
            
        print(f"\n📊 INFORMACIÓN BÁSICA DEL ARCHIVO:")
        print(f"{'='*50}")
        print(f"📏 Dimensiones: {self.datos_originales.shape[0]:,} filas × {self.datos_originales.shape[1]} columnas")
        print(f"📅 Período: {self.datos_originales['fecha'].min().strftime('%Y-%m-%d')} a {self.datos_originales['fecha'].max().strftime('%Y-%m-%d')}")
        print(f"🏙️ Columnas disponibles:")
        for i, col in enumerate(self.datos_originales.columns, 1):
            tipo = str(self.datos_originales[col].dtype)
            print(f"   {i:2d}. {col:<25} ({tipo})")
    
    def _validar_estructura_datos(self) -> None:
        """Validar que el archivo tenga las columnas necesarias"""
        if self.datos_originales is None:
            raise ValueError("❌ No hay datos cargados")
            
        columnas_requeridas = ['fecha', 'vel_viento (m/s)', 'Municipio']
        columnas_faltantes = [col for col in columnas_requeridas if col not in self.datos_originales.columns]
        
        if columnas_faltantes:
            raise ValueError(f"❌ Columnas requeridas faltantes: {columnas_faltantes}")
        
        print("✅ Estructura de datos válida")
    
    def _procesar_columna_fecha(self) -> None:
        """Procesar y validar la columna de fecha"""
        if self.datos_originales is None:
            return
            
        if 'fecha' in self.datos_originales.columns:
            # Convertir a datetime si no lo está ya
            if not pd.api.types.is_datetime64_any_dtype(self.datos_originales['fecha']):
                self.datos_originales['fecha'] = pd.to_datetime(self.datos_originales['fecha'])
            
            # Crear columnas adicionales útiles
            self.datos_originales['año'] = self.datos_originales['fecha'].dt.year
            self.datos_originales['mes'] = self.datos_originales['fecha'].dt.month
            self.datos_originales['dia_año'] = self.datos_originales['fecha'].dt.dayofyear
    
    def obtener_municipios_disponibles(self) -> List[str]:
        """
        Obtener lista de municipios disponibles en los datos
        
        Returns:
        --------
        List[str]
            Lista de nombres de municipios
        """
        if self.datos_originales is None:
            self.cargar_archivo_excel()
        
        municipios = self.datos_originales['Municipio'].unique().tolist()
        municipios.sort()
        
        print(f"\n🏙️ MUNICIPIOS DISPONIBLES ({len(municipios)}):")
        print("="*40)
        
        # Mostrar información de cada municipio
        resumen_municipios = self.datos_originales.groupby('Municipio').agg({
            'fecha': ['min', 'max', 'count'],
            'vel_viento (m/s)': ['mean', 'std', 'min', 'max']
        }).round(2)
        
        for i, municipio in enumerate(municipios, 1):
            datos_municipio = resumen_municipios.loc[municipio]
            fecha_inicio = datos_municipio[('fecha', 'min')].strftime('%Y-%m-%d')
            fecha_fin = datos_municipio[('fecha', 'max')].strftime('%Y-%m-%d')
            n_datos = int(datos_municipio[('fecha', 'count')])
            vel_media = datos_municipio[('vel_viento (m/s)', 'mean')]
            vel_std = datos_municipio[('vel_viento (m/s)', 'std')]
            
            print(f"{i:2d}. {municipio:<15} | {fecha_inicio} a {fecha_fin} | {n_datos:4d} días | v̅={vel_media:5.1f}±{vel_std:.1f} m/s")
        
        return municipios
    
    def extraer_datos_municipio(self, municipio: str, 
                              fecha_inicio: Optional[Union[str, datetime, date]] = None,
                              fecha_fin: Optional[Union[str, datetime, date]] = None,
                              filtrar_outliers: bool = True,
                              vel_min: float = 0.0,
                              vel_max: float = 50.0) -> Dict:
        """
        Extraer datos de velocidad del viento para un municipio específico
        
        Parameters:
        -----------
        municipio : str
            Nombre del municipio a extraer
        fecha_inicio : str, datetime o date, opcional
            Fecha de inicio del período (formato: 'YYYY-MM-DD')
        fecha_fin : str, datetime o date, opcional
            Fecha de fin del período
        filtrar_outliers : bool
            Si filtrar valores atípicos automáticamente
        vel_min : float
            Velocidad mínima válida (m/s)
        vel_max : float
            Velocidad máxima válida (m/s)
            
        Returns:
        --------
        Dict
            Diccionario con datos procesados del municipio
        """
        if self.datos_originales is None:
            self.cargar_archivo_excel()
        
        # Filtrar por municipio
        datos_municipio = self.datos_originales[
            self.datos_originales['Municipio'] == municipio
        ].copy()
        
        if datos_municipio.empty:
            raise ValueError(f"❌ No se encontraron datos para el municipio: {municipio}")
        
        # Filtrar por fechas si se especifican
        if fecha_inicio:
            fecha_inicio = pd.to_datetime(fecha_inicio)
            datos_municipio = datos_municipio[datos_municipio['fecha'] >= fecha_inicio]
        
        if fecha_fin:
            fecha_fin = pd.to_datetime(fecha_fin)
            datos_municipio = datos_municipio[datos_municipio['fecha'] <= fecha_fin]
        
        # Extraer velocidades del viento
        velocidades = datos_municipio['vel_viento (m/s)'].values
        fechas = datos_municipio['fecha'].values
        
        # Aplicar filtros de calidad
        n_original = len(velocidades)
        
        # Filtro por rango de velocidades
        mask_rango = (velocidades >= vel_min) & (velocidades <= vel_max)
        velocidades = velocidades[mask_rango]
        fechas = fechas[mask_rango]
        
        # Filtro de outliers usando IQR si se solicita
        if filtrar_outliers:
            Q1 = np.percentile(velocidades, 25)
            Q3 = np.percentile(velocidades, 75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR
            
            mask_outliers = (velocidades >= limite_inferior) & (velocidades <= limite_superior)
            velocidades = velocidades[mask_outliers]
            fechas = fechas[mask_outliers]
        
        n_final = len(velocidades)
        
        # Calcular estadísticas básicas
        estadisticas = {
            'n_datos': n_final,
            'n_filtrados': n_original - n_final,
            'porcentaje_validos': (n_final / n_original) * 100,
            'fecha_inicio': fechas.min(),
            'fecha_fin': fechas.max(),
            'velocidad_media': np.mean(velocidades),
            'velocidad_mediana': np.median(velocidades),
            'desviacion_estandar': np.std(velocidades, ddof=1),
            'velocidad_min': np.min(velocidades),
            'velocidad_max': np.max(velocidades),
            'coeficiente_variacion': np.std(velocidades, ddof=1) / np.mean(velocidades)
        }
        
        # Crear resultado
        resultado = {
            'municipio': municipio,
            'velocidades': velocidades,
            'fechas': fechas,
            'estadisticas': estadisticas,
            'datos_adicionales': datos_municipio[mask_rango][mask_outliers] if filtrar_outliers else datos_municipio[mask_rango]
        }
        
        # Almacenar en caché
        self.datos_procesados[municipio] = resultado
        
        # Mostrar resumen
        self._mostrar_resumen_municipio(resultado)
        
        return resultado
    
    def _mostrar_resumen_municipio(self, datos: Dict) -> None:
        """Mostrar resumen estadístico de un municipio"""
        stats = datos['estadisticas']
        municipio = datos['municipio']
        
        print(f"\n📍 RESUMEN - {municipio.upper()}")
        print("="*40)
        print(f"📊 Datos procesados:")
        print(f"   • Registros válidos: {stats['n_datos']:,} ({stats['porcentaje_validos']:.1f}%)")
        print(f"   • Registros filtrados: {stats['n_filtrados']:,}")
        print(f"   • Período: {stats['fecha_inicio'].strftime('%Y-%m-%d')} a {stats['fecha_fin'].strftime('%Y-%m-%d')}")
        
        print(f"\n🌬️ Estadísticas de velocidad del viento:")
        print(f"   • Media: {stats['velocidad_media']:.2f} m/s")
        print(f"   • Mediana: {stats['velocidad_mediana']:.2f} m/s")
        print(f"   • Desv. estándar: {stats['desviacion_estandar']:.2f} m/s")
        print(f"   • Rango: {stats['velocidad_min']:.1f} - {stats['velocidad_max']:.1f} m/s")
        print(f"   • Coef. variación: {stats['coeficiente_variacion']:.3f}")
    
    def extraer_multiples_municipios(self, 
                                   municipios: List[str],
                                   **kwargs) -> Dict[str, Dict]:
        """
        Extraer datos para múltiples municipios
        
        Parameters:
        -----------
        municipios : List[str]
            Lista de nombres de municipios
        **kwargs
            Argumentos adicionales para extraer_datos_municipio
            
        Returns:
        --------
        Dict[str, Dict]
            Diccionario con datos de cada municipio
        """
        resultados = {}
        
        print(f"\n🔄 PROCESANDO {len(municipios)} MUNICIPIOS...")
        print("="*50)
        
        for i, municipio in enumerate(municipios, 1):
            try:
                print(f"\n[{i}/{len(municipios)}] Procesando: {municipio}")
                resultado = self.extraer_datos_municipio(municipio, **kwargs)
                resultados[municipio] = resultado
                
            except Exception as e:
                print(f"⚠️ Error procesando {municipio}: {e}")
                continue
        
        print(f"\n✅ Procesamiento completado: {len(resultados)}/{len(municipios)} municipios")
        return resultados
    
    def exportar_datos_procesados(self, 
                                archivo_salida: str = "datos_procesados_weibull.xlsx",
                                incluir_estadisticas: bool = True) -> None:
        """
        Exportar los datos procesados a un archivo Excel
        
        Parameters:
        -----------
        archivo_salida : str
            Nombre del archivo de salida
        incluir_estadisticas : bool
            Si incluir hoja con estadísticas resumidas
        """
        if not self.datos_procesados:
            print("⚠️ No hay datos procesados para exportar")
            return
        
        print(f"📁 Exportando datos a: {archivo_salida}")
        
        with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
            
            # Exportar datos de cada municipio
            for municipio, datos in self.datos_procesados.items():
                df_municipio = pd.DataFrame({
                    'fecha': datos['fechas'],
                    'velocidad_viento_m_s': datos['velocidades']
                })
                
                # Limpiar nombre de hoja (Excel no permite ciertos caracteres)
                nombre_hoja = municipio.replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                df_municipio.to_excel(writer, sheet_name=nombre_hoja, index=False)
            
            # Exportar resumen estadístico
            if incluir_estadisticas:
                estadisticas_resumen = []
                for municipio, datos in self.datos_procesados.items():
                    stats = datos['estadisticas']
                    estadisticas_resumen.append({
                        'Municipio': municipio,
                        'N_Datos': stats['n_datos'],
                        'Fecha_Inicio': stats['fecha_inicio'].strftime('%Y-%m-%d'),
                        'Fecha_Fin': stats['fecha_fin'].strftime('%Y-%m-%d'),
                        'Velocidad_Media_m_s': round(stats['velocidad_media'], 2),
                        'Desviacion_Estandar_m_s': round(stats['desviacion_estandar'], 2),
                        'Velocidad_Min_m_s': round(stats['velocidad_min'], 1),
                        'Velocidad_Max_m_s': round(stats['velocidad_max'], 1),
                        'Coef_Variacion': round(stats['coeficiente_variacion'], 3)
                    })
                
                df_estadisticas = pd.DataFrame(estadisticas_resumen)
                df_estadisticas.to_excel(writer, sheet_name='Resumen_Estadisticas', index=False)
        
        print(f"✅ Datos exportados exitosamente a {archivo_salida}")
    
    def comparar_municipios_estadisticamente(self, municipios: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Crear tabla comparativa de estadísticas entre municipios
        
        Parameters:
        -----------
        municipios : List[str], opcional
            Lista de municipios a comparar. Si None, usa todos los procesados
            
        Returns:
        --------
        pd.DataFrame
            DataFrame con comparación estadística
        """
        if municipios is None:
            municipios = list(self.datos_procesados.keys())
        
        if not municipios:
            print("⚠️ No hay municipios procesados para comparar")
            return pd.DataFrame()
        
        comparacion = []
        
        for municipio in municipios:
            if municipio in self.datos_procesados:
                datos = self.datos_procesados[municipio]
                stats = datos['estadisticas']
                velocidades = datos['velocidades']
                
                # Calcular percentiles
                p25 = np.percentile(velocidades, 25)
                p50 = np.percentile(velocidades, 50)
                p75 = np.percentile(velocidades, 75)
                p90 = np.percentile(velocidades, 90)
                p95 = np.percentile(velocidades, 95)
                
                comparacion.append({
                    'Municipio': municipio,
                    'N_Datos': stats['n_datos'],
                    'Media (m/s)': round(stats['velocidad_media'], 2),
                    'Mediana (m/s)': round(stats['velocidad_mediana'], 2),
                    'Desv_Est (m/s)': round(stats['desviacion_estandar'], 2),
                    'Min (m/s)': round(stats['velocidad_min'], 1),
                    'Max (m/s)': round(stats['velocidad_max'], 1),
                    'P25 (m/s)': round(p25, 1),
                    'P75 (m/s)': round(p75, 1),
                    'P90 (m/s)': round(p90, 1),
                    'P95 (m/s)': round(p95, 1),
                    'CV': round(stats['coeficiente_variacion'], 3),
                    'Días_Total': round((stats['fecha_fin'] - stats['fecha_inicio']).days + 1)
                })
        
        df_comparacion = pd.DataFrame(comparacion)
        
        print(f"\n📊 COMPARACIÓN ESTADÍSTICA DE MUNICIPIOS")
        print("="*80)
        print(df_comparacion.to_string(index=False))
        
        # Identificar características destacables
        print(f"\n🏆 RANKINGS:")
        print(f"   • Mayor velocidad media: {df_comparacion.loc[df_comparacion['Media (m/s)'].idxmax(), 'Municipio']} ({df_comparacion['Media (m/s)'].max():.1f} m/s)")
        print(f"   • Menor variabilidad: {df_comparacion.loc[df_comparacion['CV'].idxmin(), 'Municipio']} (CV = {df_comparacion['CV'].min():.3f})")
        print(f"   • Más datos: {df_comparacion.loc[df_comparacion['N_Datos'].idxmax(), 'Municipio']} ({df_comparacion['N_Datos'].max():,} registros)")
        
        return df_comparacion


def ejemplo_uso_importador():
    """
    Ejemplo completo de uso del importador de datos Excel
    """
    print("🌪️ EJEMPLO DE IMPORTACIÓN DE DATOS EXCEL PARA ANÁLISIS WEIBULL")
    print("="*70)
    
    # 1. Crear instancia del importador
    importador = ImportadorDatosExcel("Datos.xlsx")
    
    # 2. Cargar archivo y mostrar municipios disponibles
    importador.cargar_archivo_excel()
    municipios_disponibles = importador.obtener_municipios_disponibles()
    
    # 3. Seleccionar municipios para análisis (los primeros 3 con más datos)
    municipios_seleccionados = ['Barranquilla', 'Cartagena', 'Medellín']
    
    print(f"\n🎯 MUNICIPIOS SELECCIONADOS PARA ANÁLISIS:")
    for i, municipio in enumerate(municipios_seleccionados, 1):
        print(f"   {i}. {municipio}")
    
    # 4. Extraer datos de múltiples municipios
    datos_municipios = importador.extraer_multiples_municipios(
        municipios_seleccionados,
        fecha_inicio='2020-01-01',
        fecha_fin='2023-12-31',
        filtrar_outliers=True,
        vel_min=0.5,
        vel_max=40.0
    )
    
    # 5. Comparar estadísticamente
    comparacion = importador.comparar_municipios_estadisticamente(municipios_seleccionados)
    
    # 6. Exportar datos procesados
    importador.exportar_datos_procesados("datos_weibull_colombia.xlsx")
    
    print(f"\n✅ PROCESO COMPLETADO")
    print(f"   • Municipios procesados: {len(datos_municipios)}")
    print(f"   • Datos exportados a: datos_weibull_colombia.xlsx")
    print(f"   • Listos para análisis de Weibull")
    
    return importador, datos_municipios


if __name__ == "__main__":
    # Ejecutar ejemplo
    importador, datos = ejemplo_uso_importador()
