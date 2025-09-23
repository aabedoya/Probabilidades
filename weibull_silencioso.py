"""
APLICACIÓN WEIBULL INTERACTIVA PARA GENERACIÓN DE PDF
=====================================================

Esta aplicación permite seleccionar 2 ciudades interactivamente y
genera un PDF completo con todo el contenido educativo de Weibull.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from scipy import stats
from generador_pdf_weibull import GeneradorPDFWeibull
from datetime import datetime

class AnalisisWeibullInteractivo:
    """
    Clase para análisis de Weibull con selección interactiva de ciudades
    que genera PDF completo con contenido educativo
    """
    
    def __init__(self, archivo_excel="Datos.xlsx"):
        self.archivo_excel = archivo_excel
        self.datos = None
        self.ciudades_disponibles = ['Riohacha', 'Barranquilla', 'Cartagena', 'Valledupar', 
                                    'Santa Marta', 'Montería', 'Sincelejo', 'Caucasia', 
                                    'Magangué', 'El Banco']
        self.ciudades_seleccionadas = []
        self.datos_ciudades = {}
        self.resultados = {}
        
    def cargar_datos(self) -> bool:
        """Cargar datos sin mostrar información"""
        try:
            if not os.path.exists(self.archivo_excel):
                return False
                
            self.datos = pd.read_excel(self.archivo_excel)
            
            columnas_requeridas = ['Municipio', 'vel_viento (m/s)', 'T (°C)']
            if not all(col in self.datos.columns for col in columnas_requeridas):
                return False
                
            municipios_en_datos = set(self.datos['Municipio'].unique())
            ciudades_validas = [c for c in self.ciudades_disponibles if c in municipios_en_datos]
            
            if len(ciudades_validas) < 2:
                return False
                
            self.ciudades_disponibles = ciudades_validas
            return True
            
        except Exception as e:
            return False
    
    def seleccionar_ciudades_interactivo(self):
        """Selección interactiva de 2 ciudades por el usuario"""
        print("\n🏙️ CIUDADES DISPONIBLES PARA ANÁLISIS")
        print("=" * 50)
        print(f"{'#':<3} {'Ciudad':<15} {'Registros':<10} {'Vel.Media':<12} {'Temp.Media'}")
        print("-" * 50)
        
        # Mostrar estadísticas de cada ciudad
        ciudades_info = []
        for i, ciudad in enumerate(self.ciudades_disponibles, 1):
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            vel_media = datos_ciudad['vel_viento (m/s)'].mean()
            temp_media = datos_ciudad['T (°C)'].mean()
            registros = len(datos_ciudad)
            
            ciudades_info.append({
                'ciudad': ciudad,
                'registros': registros,
                'vel_media': vel_media,
                'temp_media': temp_media
            })
            
            print(f"{i:<3} {ciudad:<15} {registros:<10} {vel_media:<12.2f} {temp_media:.1f}°C")
        
        print(f"\n🎯 SELECCIÓN DE CIUDADES")
        print("=" * 30)
        print("Debes seleccionar 2 ciudades diferentes para el análisis")
        
        ciudades_seleccionadas = []
        
        # Seleccionar 2 ciudades
        for i in range(2):
            while True:
                try:
                    print(f"\n📍 Selecciona la ciudad #{i+1}:")
                    opcion = input(f"Ingresa el número (1-{len(self.ciudades_disponibles)}): ").strip()
                    
                    if not opcion:
                        print("❌ Por favor ingresa un número válido")
                        continue
                    
                    try:
                        numero = int(opcion)
                    except ValueError:
                        print("❌ Por favor ingresa un número válido")
                        continue
                    
                    if numero < 1 or numero > len(self.ciudades_disponibles):
                        print(f"❌ Número fuera de rango. Debe estar entre 1 y {len(self.ciudades_disponibles)}")
                        continue
                    
                    ciudad_elegida = self.ciudades_disponibles[numero - 1]
                    
                    if ciudad_elegida in ciudades_seleccionadas:
                        print("❌ Esta ciudad ya fue seleccionada. Elige una diferente.")
                        continue
                    
                    ciudades_seleccionadas.append(ciudad_elegida)
                    print(f"✅ {ciudad_elegida} seleccionada")
                    break
                    
                except (ValueError, KeyboardInterrupt):
                    print("❌ Entrada inválida. Intenta de nuevo.")
                    
        self.ciudades_seleccionadas = ciudades_seleccionadas
        
        print(f"\n🎉 CIUDADES SELECCIONADAS:")
        print(f"   1️⃣ {ciudades_seleccionadas[0]}")
        print(f"   2️⃣ {ciudades_seleccionadas[1]}")
        
        return True
        
    def extraer_datos_ciudades(self):
        """Extraer datos de las ciudades seleccionadas"""
        for ciudad in self.ciudades_seleccionadas:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            self.datos_ciudades[ciudad] = datos_ciudad
    
    def calcular_estadisticos_basicos(self):
        """Calcular estadísticos básicos para todas las ciudades"""
        for ciudad in self.ciudades_seleccionadas:
            datos_ciudad = self.datos_ciudades[ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            
            media = viento.mean()
            mediana = viento.median()
            moda = viento.mode()
            desviacion = viento.std()
            minimo = viento.min()
            maximo = viento.max()
            rango = maximo - minimo
            cv = desviacion / media
            
            self.resultados[ciudad] = {
                'media': media,
                'mediana': mediana,
                'moda': moda,
                'desviacion': desviacion,
                'minimo': minimo,
                'maximo': maximo,
                'rango': rango,
                'cv': cv
            }
    
    def calcular_parametros_weibull(self):
        """Calcular parámetros Weibull"""
        for ciudad in self.ciudades_seleccionadas:
            datos = self.resultados[ciudad]
            cv = datos['cv']
            media = datos['media']
            
            # Parámetros Weibull
            k = cv ** (-1.09)
            gamma_value = gamma(1 + 1/k)
            c = media / gamma_value
            
            self.resultados[ciudad].update({
                'k': k,
                'c': c,
                'gamma_value': gamma_value
            })
    
    def calcular_velocidades_caracteristicas(self):
        """Calcular velocidades características"""
        for ciudad in self.ciudades_seleccionadas:
            k = self.resultados[ciudad]['k']
            c = self.resultados[ciudad]['c']
            
            # Velocidad más probable
            v_mp = c * ((k-1)/k)**(1/k)
            
            # Velocidad de máxima energía
            v_maxE = c * ((k+2)/k)**(1/k)
            
            self.resultados[ciudad].update({
                'v_mp': v_mp,
                'v_maxE': v_maxE
            })
    
    def calcular_cuartiles(self):
        """Calcular cuartiles y rango intercuartílico"""
        for ciudad in self.ciudades_seleccionadas:
            k = self.resultados[ciudad]['k']
            c = self.resultados[ciudad]['c']
            
            # Cuartiles
            q1 = c * ((-np.log(1-0.25)) ** (1/k))
            q3 = c * ((-np.log(1-0.75)) ** (1/k))
            iqr = q3 - q1
            
            self.resultados[ciudad].update({
                'q1': q1,
                'q3': q3,
                'iqr': iqr
            })
    
    def calcular_probabilidades(self):
        """Calcular probabilidades entre cuartiles y percentil 60"""
        for ciudad in self.ciudades_seleccionadas:
            k = self.resultados[ciudad]['k']
            c = self.resultados[ciudad]['c']
            q1 = self.resultados[ciudad]['q1']
            q3 = self.resultados[ciudad]['q3']
            
            # Probabilidad entre cuartiles (siempre 50%)
            prob_cuartiles = 0.5
            
            # Percentil 60 y probabilidad superior
            p60 = c * ((-np.log(1-0.60)) ** (1/k))
            prob_superior_p60 = 0.4  # Por definición
            
            self.resultados[ciudad].update({
                'prob_cuartiles': prob_cuartiles,
                'p60': p60,
                'prob_superior_p60': prob_superior_p60
            })
    
    def ejecutar_analisis_completo(self):
        """Ejecutar análisis completo con selección interactiva de ciudades"""
        if not self.cargar_datos():
            return False
            
        # Selección interactiva de ciudades
        if not self.seleccionar_ciudades_interactivo():
            return False
            
        self.extraer_datos_ciudades()
        self.calcular_estadisticos_basicos()
        self.calcular_parametros_weibull()
        self.calcular_velocidades_caracteristicas()
        self.calcular_cuartiles()
        self.calcular_probabilidades()
        
        return True
    
    def generar_pdf_silencioso(self, nombre_archivo=None):
        """Generar PDF sin mostrar progreso"""
        if nombre_archivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ciudades_str = "_".join(self.ciudades_seleccionadas)
            nombre_archivo = f"reporte_weibull_silencioso_{ciudades_str}_{timestamp}.pdf"
        
        generador = GeneradorPDFWeibull(
            datos=self.datos,
            ciudades_seleccionadas=self.ciudades_seleccionadas,
            resultados_analisis=self.resultados
        )
        
        ruta_completa = generador.generar_reporte_completo(nombre_archivo)
        return ruta_completa

def main():
    """Función principal del análisis con selección de ciudades"""
    
    # Mensaje de bienvenida
    print("🌪️" + "=" * 70)
    print("    ANÁLISIS WEIBULL - GENERACIÓN DE PDF EDUCATIVO")
    print("=" * 72)
    print("📚 Genera un PDF completo con todo el análisis educativo")
    print("🎯 Selecciona 2 ciudades para el análisis comparativo")
    print("📊 PDF incluye todas las semanas y actividades")
    print("=" * 72)
    
    # Crear analizador
    analizador = AnalisisWeibullInteractivo("Datos.xlsx")
    
    # Ejecutar análisis completo
    if analizador.ejecutar_analisis_completo():
        # Generar PDF
        ruta_pdf = analizador.generar_pdf_silencioso()
        
        # Solo mostrar resultado final
        print(f"✅ Análisis completado exitosamente")
        print(f"📄 PDF generado: {os.path.basename(ruta_pdf)}")
        print(f"📍 Ubicación: {ruta_pdf}")
        print(f"🏙️ Ciudades analizadas: {', '.join(analizador.ciudades_seleccionadas)}")
        
        return True
    else:
        print("❌ Error al ejecutar el análisis")
        return False

if __name__ == "__main__":
    exito = main()
    if exito:
        print("\n🎉 ¡Análisis completado! El PDF contiene todo el contenido educativo.")
        print("📚 Perfecto para estudiar - todas las semanas y actividades incluidas.")
    else:
        print("\n💥 Error en el proceso - Verifica que el archivo Datos.xlsx esté disponible.")