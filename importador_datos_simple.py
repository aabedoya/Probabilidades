"""
Importador Simplificado de Datos Excel para Análisis de Weibull
===============================================================

Versión simplificada y robusta para importar datos meteorológicos
desde archivos Excel y prepararlos para análisis de distribución de Weibull.

Autor: Proyecto Probabilidades
Fecha: 3 de septiembre de 2025
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class ImportadorSimple:
    """Importador simplificado para datos de viento"""
    
    def __init__(self, archivo_excel: str = "Datos.xlsx"):
        self.archivo_excel = archivo_excel
        self.datos = None
    
    def cargar_datos(self) -> pd.DataFrame:
        """
        Cargar datos desde Excel
        
        Returns:
        --------
        pd.DataFrame
            Datos cargados
        """
        print(f"📁 Cargando datos desde: {self.archivo_excel}")
        
        if not Path(self.archivo_excel).exists():
            raise FileNotFoundError(f"❌ Archivo no encontrado: {self.archivo_excel}")
        
        # Cargar datos
        self.datos = pd.read_excel(self.archivo_excel)
        
        # Mostrar información básica
        print(f"✅ Datos cargados: {self.datos.shape[0]:,} registros × {self.datos.shape[1]} columnas")
        
        return self.datos
    
    def obtener_municipios(self) -> List[str]:
        """
        Obtener lista de municipios disponibles
        
        Returns:
        --------
        List[str]
            Lista de municipios
        """
        if self.datos is None:
            self.cargar_datos()
        
        municipios = sorted(self.datos['Municipio'].unique())
        
        print(f"\n🏙️ MUNICIPIOS DISPONIBLES ({len(municipios)}):")
        print("=" * 50)
        
        # Mostrar estadísticas por municipio
        for i, municipio in enumerate(municipios, 1):
            datos_mun = self.datos[self.datos['Municipio'] == municipio]
            n_registros = len(datos_mun)
            vel_media = datos_mun['vel_viento (m/s)'].mean()
            vel_std = datos_mun['vel_viento (m/s)'].std()
            fecha_min = datos_mun['fecha'].min().strftime('%Y-%m-%d')
            fecha_max = datos_mun['fecha'].max().strftime('%Y-%m-%d')
            
            print(f"{i:2d}. {municipio:<15} | {fecha_min} a {fecha_max} | {n_registros:4d} días | v̅={vel_media:5.1f}±{vel_std:.1f} m/s")
        
        return municipios
    
    def extraer_velocidades_municipio(self, 
                                    municipio: str,
                                    fecha_inicio: Optional[str] = None,
                                    fecha_fin: Optional[str] = None,
                                    vel_min: float = 0.5,
                                    vel_max: float = 40.0) -> Dict:
        """
        Extraer velocidades de viento para un municipio
        
        Parameters:
        -----------
        municipio : str
            Nombre del municipio
        fecha_inicio : str, opcional
            Fecha de inicio (formato YYYY-MM-DD)
        fecha_fin : str, opcional
            Fecha de fin (formato YYYY-MM-DD)
        vel_min : float
            Velocidad mínima válida (m/s)
        vel_max : float
            Velocidad máxima válida (m/s)
            
        Returns:
        --------
        Dict
            Datos procesados del municipio
        """
        if self.datos is None:
            self.cargar_datos()
        
        # Filtrar por municipio
        datos_municipio = self.datos[self.datos['Municipio'] == municipio].copy()
        
        if datos_municipio.empty:
            raise ValueError(f"❌ No se encontraron datos para: {municipio}")
        
        # Filtrar por fechas si se especifican
        if fecha_inicio:
            datos_municipio = datos_municipio[datos_municipio['fecha'] >= fecha_inicio]
        if fecha_fin:
            datos_municipio = datos_municipio[datos_municipio['fecha'] <= fecha_fin]
        
        # Extraer velocidades y aplicar filtros de calidad
        velocidades_originales = datos_municipio['vel_viento (m/s)'].values
        n_original = len(velocidades_originales)
        
        # Filtrar por rango de velocidades
        velocidades_filtradas = velocidades_originales[
            (velocidades_originales >= vel_min) & 
            (velocidades_originales <= vel_max)
        ]
        
        n_filtrado = len(velocidades_filtradas)
        porcentaje_valido = (n_filtrado / n_original) * 100 if n_original > 0 else 0
        
        # Calcular estadísticas
        estadisticas = {
            'municipio': municipio,
            'n_original': n_original,
            'n_filtrado': n_filtrado,
            'porcentaje_valido': porcentaje_valido,
            'velocidad_media': float(np.mean(velocidades_filtradas)),
            'velocidad_mediana': float(np.median(velocidades_filtradas)),
            'desviacion_estandar': float(np.std(velocidades_filtradas, ddof=1)),
            'velocidad_min': float(np.min(velocidades_filtradas)),
            'velocidad_max': float(np.max(velocidades_filtradas)),
            'fecha_inicio': datos_municipio['fecha'].min().strftime('%Y-%m-%d'),
            'fecha_fin': datos_municipio['fecha'].max().strftime('%Y-%m-%d')
        }
        
        # Calcular coeficiente de variación
        estadisticas['coef_variacion'] = estadisticas['desviacion_estandar'] / estadisticas['velocidad_media']
        
        resultado = {
            'municipio': municipio,
            'velocidades': velocidades_filtradas,
            'estadisticas': estadisticas
        }
        
        # Mostrar resumen
        self._mostrar_resumen(estadisticas)
        
        return resultado
    
    def _mostrar_resumen(self, stats: Dict) -> None:
        """Mostrar resumen estadístico"""
        print(f"\n📍 RESUMEN - {stats['municipio'].upper()}")
        print("=" * 40)
        print(f"📊 Datos procesados:")
        print(f"   • Registros válidos: {stats['n_filtrado']:,} ({stats['porcentaje_valido']:.1f}%)")
        print(f"   • Período: {stats['fecha_inicio']} a {stats['fecha_fin']}")
        
        print(f"\n🌬️ Estadísticas de velocidad del viento:")
        print(f"   • Media: {stats['velocidad_media']:.2f} m/s")
        print(f"   • Mediana: {stats['velocidad_mediana']:.2f} m/s") 
        print(f"   • Desv. estándar: {stats['desviacion_estandar']:.2f} m/s")
        print(f"   • Rango: {stats['velocidad_min']:.1f} - {stats['velocidad_max']:.1f} m/s")
        print(f"   • Coef. variación: {stats['coef_variacion']:.3f}")
    
    def extraer_multiples_municipios(self, municipios: List[str], **kwargs) -> Dict[str, Dict]:
        """
        Extraer datos para múltiples municipios
        
        Parameters:
        -----------
        municipios : List[str]
            Lista de municipios
        **kwargs
            Argumentos para extraer_velocidades_municipio
            
        Returns:
        --------
        Dict[str, Dict]
            Datos de todos los municipios
        """
        resultados = {}
        
        print(f"\n🔄 PROCESANDO {len(municipios)} MUNICIPIOS...")
        print("=" * 50)
        
        for i, municipio in enumerate(municipios, 1):
            try:
                print(f"\n[{i}/{len(municipios)}] Procesando: {municipio}")
                resultado = self.extraer_velocidades_municipio(municipio, **kwargs)
                resultados[municipio] = resultado
                
            except Exception as e:
                print(f"⚠️ Error procesando {municipio}: {e}")
                continue
        
        print(f"\n✅ Procesamiento completado: {len(resultados)}/{len(municipios)} municipios")
        
        # Mostrar tabla comparativa
        if resultados:
            self._mostrar_tabla_comparativa(resultados)
        
        return resultados
    
    def _mostrar_tabla_comparativa(self, resultados: Dict[str, Dict]) -> None:
        """Mostrar tabla comparativa de municipios"""
        print(f"\n📊 TABLA COMPARATIVA DE MUNICIPIOS")
        print("=" * 80)
        
        # Encabezado
        print(f"{'Municipio':<15} {'N_Datos':<8} {'Media':<8} {'Mediana':<9} {'Desv_Est':<9} {'Min':<7} {'Max':<7} {'CV':<7}")
        print("-" * 80)
        
        # Datos por municipio
        for municipio, datos in resultados.items():
            stats = datos['estadisticas']
            print(f"{municipio:<15} {stats['n_filtrado']:<8} {stats['velocidad_media']:<8.2f} "
                  f"{stats['velocidad_mediana']:<9.2f} {stats['desviacion_estandar']:<9.2f} "
                  f"{stats['velocidad_min']:<7.1f} {stats['velocidad_max']:<7.1f} {stats['coef_variacion']:<7.3f}")
    
    def exportar_para_weibull(self, 
                            resultados: Dict[str, Dict],
                            archivo_salida: str = "datos_weibull_colombia.xlsx") -> None:
        """
        Exportar datos en formato adecuado para análisis de Weibull
        
        Parameters:
        -----------
        resultados : Dict[str, Dict]
            Resultados de municipios procesados
        archivo_salida : str
            Nombre del archivo de salida
        """
        print(f"\n📁 Exportando datos a: {archivo_salida}")
        
        with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
            
            # Hoja 1: Resumen estadístico
            resumen_data = []
            for municipio, datos in resultados.items():
                stats = datos['estadisticas']
                resumen_data.append({
                    'Municipio': municipio,
                    'N_Datos': stats['n_filtrado'],
                    'Fecha_Inicio': stats['fecha_inicio'],
                    'Fecha_Fin': stats['fecha_fin'],
                    'Velocidad_Media_m_s': stats['velocidad_media'],
                    'Desviacion_Estandar_m_s': stats['desviacion_estandar'],
                    'Velocidad_Min_m_s': stats['velocidad_min'],
                    'Velocidad_Max_m_s': stats['velocidad_max'],
                    'Coef_Variacion': stats['coef_variacion']
                })
            
            df_resumen = pd.DataFrame(resumen_data)
            df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
            
            # Hoja 2: Datos consolidados (formato para ecuaciones_weibull_especificas.py)
            datos_consolidados = {}
            for municipio, datos in resultados.items():
                velocidades = datos['velocidades']
                # Crear serie de días (asumiendo datos diarios)
                dias = list(range(1, len(velocidades) + 1))
                datos_consolidados[f'Dia'] = dias
                datos_consolidados[municipio] = velocidades
            
            # Ajustar a la misma longitud
            max_len = max(len(v) if isinstance(v, (list, np.ndarray)) else 1 for v in datos_consolidados.values())
            for key, values in datos_consolidados.items():
                if key != 'Dia' and len(values) < max_len:
                    # Rellenar con NaN si es necesario
                    valores_extendidos = list(values) + [np.nan] * (max_len - len(values))
                    datos_consolidados[key] = valores_extendidos
                elif key == 'Dia':
                    datos_consolidados[key] = list(range(1, max_len + 1))
            
            df_consolidado = pd.DataFrame(datos_consolidados)
            df_consolidado.to_excel(writer, sheet_name='Datos_Weibull', index=False)
            
            # Hojas individuales por municipio
            for municipio, datos in resultados.items():
                df_municipio = pd.DataFrame({
                    'Dia': range(1, len(datos['velocidades']) + 1),
                    'Velocidad_m_s': datos['velocidades']
                })
                
                nombre_hoja = municipio.replace(' ', '_')[:31]  # Excel limit
                df_municipio.to_excel(writer, sheet_name=nombre_hoja, index=False)
        
        print(f"✅ Datos exportados exitosamente")
        print(f"   • Archivo: {archivo_salida}")
        print(f"   • Hojas: Resumen, Datos_Weibull, + {len(resultados)} hojas individuales")


def ejemplo_importacion_completa():
    """Ejemplo completo de importación de datos reales"""
    print("🌪️ IMPORTACIÓN DE DATOS REALES DE COLOMBIA PARA ANÁLISIS WEIBULL")
    print("=" * 70)
    
    # 1. Crear importador
    importador = ImportadorSimple("Datos.xlsx")
    
    # 2. Mostrar municipios disponibles
    municipios = importador.obtener_municipios()
    
    # 3. Seleccionar municipios con mejores características para Weibull
    # (alta velocidad media y buena cantidad de datos)
    municipios_seleccionados = ['Riohacha', 'San Andrés', 'Barranquilla', 'Valledupar']
    
    print(f"\n🎯 MUNICIPIOS SELECCIONADOS:")
    for i, municipio in enumerate(municipios_seleccionados, 1):
        print(f"   {i}. {municipio}")
    
    # 4. Extraer datos con filtros de calidad
    datos_procesados = importador.extraer_multiples_municipios(
        municipios_seleccionados,
        fecha_inicio='2021-01-01',  # Período común para todos
        fecha_fin='2024-08-31',
        vel_min=1.0,  # Filtros de calidad
        vel_max=35.0
    )
    
    # 5. Exportar para uso con análisis de Weibull
    if datos_procesados:
        importador.exportar_para_weibull(datos_procesados)
        
        print(f"\n🎉 IMPORTACIÓN COMPLETADA CON ÉXITO")
        print(f"   • Municipios procesados: {len(datos_procesados)}")
        print(f"   • Datos listos para análisis de Weibull")
        print(f"   • Archivo generado: datos_weibull_colombia.xlsx")
    
    return importador, datos_procesados


if __name__ == "__main__":
    # Ejecutar importación completa
    importador, datos = ejemplo_importacion_completa()
