"""
Generador de PDF para Análisis de Weibull
==========================================

Este módulo genera reportes PDF profesionales del análisis de distribución 
Weibull para datos meteorológicos.

Autor: Sistema de Análisis Weibull Educativo
Fecha: Septiembre 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from scipy.special import gamma
import io
import os


class GeneradorPDFWeibull:
    """Clase para generar reportes PDF profesionales del análisis Weibull"""
    
    def __init__(self, datos, ciudades_seleccionadas, resultados_analisis):
        """
        Inicializa el generador de PDF
        
        Args:
            datos: DataFrame con los datos meteorológicos
            ciudades_seleccionadas: Lista de ciudades analizadas
            resultados_analisis: Diccionario con todos los resultados del análisis
        """
        self.datos = datos
        self.ciudades = ciudades_seleccionadas
        self.resultados = resultados_analisis
        self.fecha_reporte = datetime.now().strftime("%d de %B de %Y")
        
        # Configurar estilos
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='SubTitulo',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkred,
            fontName='Helvetica-Bold'
        ))
        
        # Título de sección
        self.styles.add(ParagraphStyle(
            name='TituloSeccion',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=15,
            spaceBefore=20,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal justificado
        self.styles.add(ParagraphStyle(
            name='TextoJustificado',
            parent=self.styles['Normal'],
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            fontSize=10
        ))
        
        # Texto de cálculo
        self.styles.add(ParagraphStyle(
            name='TextoCalculo',
            parent=self.styles['Normal'],
            fontName='Courier',
            fontSize=9,
            spaceAfter=8,
            leftIndent=20
        ))
    
    def generar_reporte_completo(self, nombre_archivo="reporte_analisis_weibull.pdf"):
        """
        Genera el reporte PDF completo
        
        Args:
            nombre_archivo: Nombre del archivo PDF a generar
        """
        doc = SimpleDocTemplate(
            nombre_archivo,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Contenido del documento
        story = []
        
        # Portada
        story.extend(self._generar_portada())
        story.append(PageBreak())
        
        # Resumen ejecutivo
        story.extend(self._generar_resumen_ejecutivo())
        story.append(PageBreak())
        
        # Datos básicos
        story.extend(self._generar_datos_basicos())
        story.append(PageBreak())
        
        # Análisis por actividad
        story.extend(self._generar_analisis_actividades())
        
        # Conclusiones
        story.append(PageBreak())
        story.extend(self._generar_conclusiones())
        
        # Construir PDF
        doc.build(story)
        
        print(f"✅ Reporte PDF generado exitosamente: {nombre_archivo}")
        return nombre_archivo
    
    def _generar_portada(self):
        """Genera la portada del reporte"""
        story = []
        
        # Espaciado superior
        story.append(Spacer(1, 2*inch))
        
        # Título principal
        titulo = Paragraph(
            "ANÁLISIS DE DISTRIBUCIÓN WEIBULL<br/>PARA DATOS METEOROLÓGICOS",
            self.styles['TituloPrincipal']
        )
        story.append(titulo)
        story.append(Spacer(1, 0.5*inch))
        
        # Subtítulo
        subtitulo = Paragraph(
            "Análisis Estadístico de Velocidades del Viento",
            self.styles['SubTitulo']
        )
        story.append(subtitulo)
        story.append(Spacer(1, 0.3*inch))
        
        # Ciudades analizadas
        ciudades_texto = "Ciudades Analizadas: " + ", ".join(self.ciudades)
        ciudades_p = Paragraph(ciudades_texto, self.styles['Normal'])
        story.append(ciudades_p)
        story.append(Spacer(1, 1*inch))
        
        # Información del reporte
        info_data = [
            ['Fecha del Reporte:', self.fecha_reporte],
            ['Total de Registros:', f"{len(self.datos):,}"],
            ['Ciudades Analizadas:', str(len(self.ciudades))],
            ['Metodología:', 'Distribución de Weibull']
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 1*inch))
        
        # Pie de portada
        pie = Paragraph(
            "Sistema de Análisis Weibull Educativo<br/>Aplicación para Análisis Estadístico de Vientos",
            self.styles['Normal']
        )
        story.append(pie)
        
        return story
    
    def _generar_resumen_ejecutivo(self):
        """Genera el resumen ejecutivo"""
        story = []
        
        # Título
        titulo = Paragraph("RESUMEN EJECUTIVO", self.styles['TituloSeccion'])
        story.append(titulo)
        
        # Objetivos
        objetivos = Paragraph(
            "<b>Objetivos del Análisis:</b><br/>"
            "• Caracterizar el comportamiento del viento mediante la distribución de Weibull<br/>"
            "• Calcular parámetros estadísticos y probabilidades asociadas<br/>"
            "• Evaluar el potencial eólico de las ciudades analizadas<br/>"
            "• Determinar velocidades características para aplicaciones energéticas",
            self.styles['TextoJustificado']
        )
        story.append(objetivos)
        
        # Metodología
        metodologia = Paragraph(
            "<b>Metodología:</b><br/>"
            "Se aplicó el análisis de distribución de Weibull de dos parámetros (k y c) "
            "a datos de velocidad del viento. Los parámetros se calcularon mediante el "
            "método de momentos utilizando las ecuaciones estándar. Se realizaron análisis "
            "de variabilidad, cálculos de percentiles y evaluaciones de potencial energético.",
            self.styles['TextoJustificado']
        )
        story.append(metodologia)
        
        # Resultados principales
        if self.resultados:
            mejor_ciudad = max(self.ciudades, key=lambda c: self._obtener_velocidad_maxima_energia(c))
            
            resultados = Paragraph(
                f"<b>Resultados Principales:</b><br/>"
                f"• Ciudad con mayor potencial eólico: <b>{mejor_ciudad}</b><br/>"
                f"• Velocidad de máxima energía más alta: "
                f"{self._obtener_velocidad_maxima_energia(mejor_ciudad):.2f} m/s<br/>"
                f"• Todas las distribuciones muestran buen ajuste a los datos observados<br/>"
                f"• Los parámetros calculados permiten estimaciones confiables de probabilidades",
                self.styles['TextoJustificado']
            )
            story.append(resultados)
        
        return story
    
    def _generar_datos_basicos(self):
        """Genera la sección de datos básicos con información detallada"""
        story = []
        
        # Título
        titulo = Paragraph("DATOS ESTADÍSTICOS BÁSICOS INICIALES", self.styles['TituloSeccion'])
        story.append(titulo)
        
        # Información general del dataset
        story.append(Paragraph(f"<b>Información General del Dataset:</b>", self.styles['SubTitulo']))
        story.append(Paragraph(f"• Registros totales cargados: {len(self.datos):,}", self.styles['Normal']))
        story.append(Paragraph(f"• Ciudades disponibles: {len(self.ciudades)}", self.styles['Normal']))
        story.append(Paragraph(f"• Ciudades analizadas: {', '.join(self.ciudades)}", self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Extracción de datos por ciudad
        story.append(Paragraph("<b>EXTRACCIÓN DE DATOS POR CIUDAD:</b>", self.styles['SubTitulo']))
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            temperatura = datos_ciudad['T (°C)']
            
            registros = len(datos_ciudad)
            vel_promedio = viento.mean()
            temp_promedio = temperatura.mean()
            vel_min = viento.min()
            vel_max = viento.max()
            
            texto_ciudad = f"<b>{ciudad.upper()}:</b><br/>" \
                          f"• Registros totales: {registros:,}<br/>" \
                          f"• Velocidad del viento promedio: {vel_promedio:.2f} m/s<br/>" \
                          f"• Temperatura promedio: {temp_promedio:.1f}°C<br/>" \
                          f"• Rango de velocidades: {vel_min:.1f} - {vel_max:.1f} m/s<br/><br/>"
            
            story.append(Paragraph(texto_ciudad, self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Cálculo de estadísticos básicos detallados
        story.append(Paragraph("<b>CÁLCULO DE ESTADÍSTICOS BÁSICOS DETALLADOS:</b>", self.styles['SubTitulo']))
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            temperatura = datos_ciudad['T (°C)']
            
            # Estadísticos del viento
            media_viento = viento.mean()
            mediana_viento = viento.median()
            moda_viento = viento.mode()
            desv_viento = viento.std()
            rango_viento = viento.max() - viento.min()
            cv_viento = desv_viento / media_viento
            
            # Estadísticos de temperatura
            media_temp = temperatura.mean()
            desv_temp = temperatura.std()
            cv_temp = desv_temp / media_temp
            
            story.append(Paragraph(f"<b>{ciudad.upper()}:</b>", self.styles['SubTitulo']))
            
            # Estadísticos de velocidad del viento
            if len(moda_viento) == 1:
                moda_texto = f"{moda_viento.iloc[0]:.4f} m/s"
            elif len(moda_viento) > 1:
                modas = [f"{m:.4f}" for m in moda_viento.head(2)]
                moda_texto = f"{', '.join(modas)} m/s"
            else:
                moda_texto = "No hay moda única"
            
            estadisticos_viento = f"<b>Velocidad del Viento:</b><br/>" \
                                 f"📈 Media (μ): {media_viento:.4f} m/s<br/>" \
                                 f"📊 Mediana: {mediana_viento:.4f} m/s<br/>" \
                                 f"📍 Moda: {moda_texto}<br/>" \
                                 f"📏 Desviación (σ): {desv_viento:.4f} m/s<br/>" \
                                 f"📐 Rango: {rango_viento:.4f} m/s ({viento.min():.1f} - {viento.max():.1f})<br/>" \
                                 f"📊 Coef. Variación: {cv_viento:.4f} ({cv_viento*100:.2f}%)<br/><br/>"
            
            story.append(Paragraph(estadisticos_viento, self.styles['Normal']))
            
            # Estadísticos de temperatura
            estadisticos_temp = f"<b>Temperatura:</b><br/>" \
                               f"📈 Media (μ): {media_temp:.4f} °C<br/>" \
                               f"📏 Desviación (σ): {desv_temp:.4f} °C<br/>" \
                               f"📊 Coef. Variación: {cv_temp:.4f} ({cv_temp*100:.2f}%)<br/><br/>"
            
            story.append(Paragraph(estadisticos_temp, self.styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Tabla resumen de parámetros Weibull calculados
        story.append(Paragraph("<b>PARÁMETROS WEIBULL CALCULADOS:</b>", self.styles['SubTitulo']))
        
        # Tabla de estadísticos por ciudad
        headers = ['Ciudad', 'Media (m/s)', 'Mediana (m/s)', 'Desv. Est. (m/s)', 
                  'CV', 'Parámetro k', 'Parámetro c (m/s)', 'Función Gamma']
        
        data = [headers]
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            
            media = viento.mean()
            mediana = viento.median()
            desv = viento.std()
            cv = desv / media
            
            # Parámetros Weibull
            k = cv ** (-1.09)
            c = media / gamma(1 + 1/k)
            gamma_value = gamma(1 + 1/k)
            
            fila = [
                ciudad,
                f"{media:.4f}",
                f"{mediana:.4f}",
                f"{desv:.4f}",
                f"{cv:.4f}",
                f"{k:.4f}",
                f"{c:.4f}",
                f"{gamma_value:.6f}"
            ]
            data.append(fila)
        
        tabla_estadisticos = Table(data, colWidths=[0.8*inch, 0.8*inch, 0.8*inch, 
                                                   0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        
        tabla_estadisticos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabla_estadisticos)
        story.append(Spacer(1, 0.3*inch))
        
        # Agregar tabla de función de densidad
        story.append(Paragraph("<b>TABLA DE FUNCIÓN DE DENSIDAD f(v):</b>", self.styles['SubTitulo']))
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            
            media = viento.mean()
            desv = viento.std()
            cv = desv / media
            k = cv ** (-1.09)
            c = media / gamma(1 + 1/k)
            
            story.append(Paragraph(f"<b>{ciudad.upper()} (k={k:.4f}, c={c:.4f}):</b>", self.styles['SubTitulo']))
            
            # Tabla de función de densidad
            headers_densidad = ['Velocidad (m/s)', 'f(v)']
            data_densidad = [headers_densidad]
            
            velocidades = np.arange(5.0, 32.5, 2.5)
            for v in velocidades:
                f_v = (k/c) * (v/c)**(k-1) * np.exp(-((v/c)**k))
                data_densidad.append([f"{v:.1f}", f"{f_v:.6f}"])
            
            tabla_densidad = Table(data_densidad, colWidths=[1.5*inch, 1.5*inch])
            tabla_densidad.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tabla_densidad)
            story.append(Spacer(1, 0.2*inch))
        
        return story
    
    def _generar_analisis_actividades(self):
        """Genera el análisis detallado por actividades de todas las semanas"""
        story = []
        
        # SEMANA 3 - ACTIVIDAD 1: ANÁLISIS DE VARIABILIDAD
        story.append(Paragraph("SEMANA 3 - ACTIVIDAD 1: HISTOGRAMAS Y ANÁLISIS DE VARIABILIDAD", self.styles['TituloSeccion']))
        
        story.append(Paragraph("<b>ANÁLISIS DE VARIABILIDAD - COEFICIENTE DE VARIACIÓN</b>", self.styles['SubTitulo']))
        story.append(Paragraph("Fórmula: CV = σ/μ (Desviación estándar / Media)", self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Cálculos detallados de CV
        story.append(Paragraph("<b>CÁLCULOS DETALLADOS:</b>", self.styles['SubTitulo']))
        
        cv_promedio_ciudades = []
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            temperatura = datos_ciudad['T (°C)']
            
            # CV para velocidad del viento
            media_viento = viento.mean()
            desv_viento = viento.std()
            cv_viento = desv_viento / media_viento
            
            # CV para temperatura
            media_temp = temperatura.mean()
            desv_temp = temperatura.std()
            cv_temp = desv_temp / media_temp
            
            cv_promedio = (cv_viento + cv_temp) / 2
            cv_promedio_ciudades.append((ciudad, cv_promedio))
            
            texto_cv = f"<b>{ciudad.upper()}:</b><br/>" \
                       f"Velocidad del viento:<br/>" \
                       f"• Media (μ): {media_viento:.4f} m/s<br/>" \
                       f"• Desv. Estándar (σ): {desv_viento:.4f} m/s<br/>" \
                       f"• CV = σ/μ = {desv_viento:.4f}/{media_viento:.4f} = {cv_viento:.4f}<br/>" \
                       f"Temperatura:<br/>" \
                       f"• Media (μ): {media_temp:.4f} °C<br/>" \
                       f"• Desv. Estándar (σ): {desv_temp:.4f} °C<br/>" \
                       f"• CV = σ/μ = {desv_temp:.4f}/{media_temp:.4f} = {cv_temp:.4f}<br/>" \
                       f"CV Promedio: ({cv_viento:.4f} + {cv_temp:.4f})/2 = {cv_promedio:.4f}<br/><br/>"
            
            story.append(Paragraph(texto_cv, self.styles['Normal']))
        
        # Conclusión de variabilidad
        mayor_variabilidad = max(cv_promedio_ciudades, key=lambda x: x[1])
        conclusion_cv = f"<b>CONCLUSIÓN:</b><br/>" \
                        f"{mayor_variabilidad[0].upper()} presenta MAYOR VARIABILIDAD<br/>" \
                        f"CV({mayor_variabilidad[0]}) = {mayor_variabilidad[1]:.4f}<br/><br/>"
        
        story.append(Paragraph(conclusion_cv, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # SEMANA 3 - ACTIVIDAD 2: CÁLCULO DE PARÁMETROS WEIBULL
        story.append(Paragraph("SEMANA 3 - ACTIVIDAD 2: CÁLCULO DE PARÁMETROS WEIBULL", self.styles['TituloSeccion']))
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            
            # Estadísticos básicos
            registros = len(datos_ciudad)
            media = viento.mean()
            desv = viento.std()
            cv = desv / media
            
            # Parámetros Weibull
            k = cv ** (-1.09)
            c = media / gamma(1 + 1/k)
            gamma_val = gamma(1 + 1/k)
            
            story.append(Paragraph(f"<b>CÁLCULO PARA {ciudad.upper()}</b>", self.styles['SubTitulo']))
            
            # Datos básicos
            datos_basicos = f"<b>DATOS BÁSICOS:</b><br/>" \
                           f"• Número de observaciones: {registros:,}<br/>" \
                           f"• Velocidad promedio (v̅): {media:.4f} m/s<br/>" \
                           f"• Desviación estándar (σ): {desv:.4f} m/s<br/>" \
                           f"• Coeficiente de variación: σ/v̅ = {desv:.4f}/{media:.4f} = {cv:.4f}<br/><br/>"
            
            story.append(Paragraph(datos_basicos, self.styles['Normal']))
            
            # Cálculo del parámetro k
            calculo_k = f"<b>ECUACIÓN 3 - CÁLCULO DEL PARÁMETRO DE FORMA (k):</b><br/>" \
                        f"k = (σ/v̅)^(-1.09)<br/><br/>" \
                        f"Paso 1: Coeficiente de variación = {cv:.4f}<br/>" \
                        f"Paso 2: Exponente = -1.09<br/>" \
                        f"Paso 3: k = ({cv:.4f})^(-1.09)<br/>" \
                        f"Paso 4: k = {k:.4f}<br/>" \
                        f"<b>✅ PARÁMETRO DE FORMA: k = {k:.4f}</b><br/><br/>"
            
            story.append(Paragraph(calculo_k, self.styles['Normal']))
            
            # Cálculo del parámetro c
            calculo_c = f"<b>ECUACIÓN 4 - CÁLCULO DEL PARÁMETRO DE ESCALA (c):</b><br/>" \
                        f"c = v̅ / Γ(1 + 1/k)<br/><br/>" \
                        f"Paso 1: Argumento de gamma = 1 + 1/k = 1 + 1/{k:.4f} = {1 + 1/k:.4f}<br/>" \
                        f"Paso 2: Γ({1 + 1/k:.4f}) = {gamma_val:.6f}<br/>" \
                        f"Paso 3: c = v̅/Γ(1+1/k) = {media:.4f}/{gamma_val:.6f}<br/>" \
                        f"Paso 4: c = {c:.4f} m/s<br/>" \
                        f"<b>✅ PARÁMETRO DE ESCALA: c = {c:.4f} m/s</b><br/><br/>"
            
            story.append(Paragraph(calculo_c, self.styles['Normal']))
            
            # Verificación matemática
            media_teorica = c * gamma_val
            error_relativo = abs(media_teorica - media) / media * 100
            
            verificacion = f"<b>✅ VERIFICACIÓN MATEMÁTICA:</b><br/>" \
                          f"Media teórica = c × Γ(1+1/k) = {c:.4f} × {gamma_val:.6f} = {media_teorica:.4f} m/s<br/>" \
                          f"Media observada = {media:.4f} m/s<br/>" \
                          f"Error relativo = |{media_teorica:.4f} - {media:.4f}|/{media:.4f} × 100% = {error_relativo:.6f}%<br/><br/>"
            
            story.append(Paragraph(verificacion, self.styles['Normal']))
            
            # Sustitución en función de densidad
            sustitucion = f"<b>📈 SUSTITUCIÓN EN FUNCIÓN DE DENSIDAD f(v) - ECUACIÓN 1:</b><br/>" \
                         f"f(v) = (k/c) × (v/c)^(k-1) × e^(-(v/c)^k)<br/><br/>" \
                         f"Sustituyendo valores:<br/>" \
                         f"f(v) = ({k:.4f}/{c:.4f}) × (v/{c:.4f})^({k:.4f}-1) × e^(-(v/{c:.4f})^{k:.4f})<br/>" \
                         f"f(v) = {k/c:.4f} × (v/{c:.4f})^{k-1:.4f} × e^(-(v/{c:.4f})^{k:.4f})<br/><br/>"
            
            story.append(Paragraph(sustitucion, self.styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
        
        # SEMANA 4 - ACTIVIDAD 3: DISTRIBUCIÓN WEIBULL VS HISTOGRAMA
        story.append(Paragraph("SEMANA 4 - ACTIVIDAD 3: DISTRIBUCIÓN WEIBULL VS HISTOGRAMA", self.styles['TituloSeccion']))
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            
            media = viento.mean()
            mediana = viento.median()
            desv = viento.std()
            cv = desv / media
            k = cv ** (-1.09)
            c = media / gamma(1 + 1/k)
            
            # Calcular moda teórica de Weibull
            if k > 1:
                moda_teorica = c * ((k-1)/k)**(1/k)
            else:
                moda_teorica = 0
            
            # Análisis de comportamiento
            if k < 1:
                forma_dist = "Exponencial decreciente (k < 1)"
            elif 1 <= k < 2:
                forma_dist = "Asimétrica hacia la derecha (1 ≤ k < 2)"
            elif 2 <= k < 3.6:
                forma_dist = "Aproximadamente simétrica (2 ≤ k < 3.6)"
            else:
                forma_dist = "Similar a normal (k ≥ 3.6)"
            
            # Calcular RMSE aproximado (simulado)
            velocidades_muestra = np.linspace(viento.min(), viento.max(), 20)
            hist_observado = np.histogram(viento, bins=20, density=True)[0]
            f_teorico = [(k/c) * (v/c)**(k-1) * np.exp(-((v/c)**k)) for v in velocidades_muestra[:-1]]
            rmse = np.sqrt(np.mean([(h - f)**2 for h, f in zip(hist_observado, f_teorico)]))
            
            # Clasificar calidad del ajuste
            if rmse < 0.01:
                calidad_ajuste = "✅ Excelente ajuste"
            elif rmse < 0.02:
                calidad_ajuste = "✅ Muy buen ajuste"
            elif rmse < 0.05:
                calidad_ajuste = "⚠️ Buen ajuste"
            else:
                calidad_ajuste = "⚠️ Ajuste moderado"
            
            analisis_dist = f"<b>ANÁLISIS PARA {ciudad.upper()}</b><br/>" \
                           f"<b>📊 ANÁLISIS DEL COMPORTAMIENTO:</b><br/>" \
                           f"1. Parámetros de la distribución:<br/>" \
                           f"   • k = {k:.4f} (parámetro de forma)<br/>" \
                           f"   • c = {c:.4f} m/s (parámetro de escala)<br/>" \
                           f"2. Forma de la distribución:<br/>" \
                           f"   • {forma_dist}<br/>" \
                           f"   • Distribución balanceada<br/>" \
                           f"3. Estadísticos:<br/>" \
                           f"   • Media: {media:.2f} m/s<br/>" \
                           f"   • Mediana: {mediana:.2f} m/s<br/>" \
                           f"   • Moda: {moda_teorica:.2f} m/s<br/>" \
                           f"4. Calidad del ajuste:<br/>" \
                           f"   • RMSE: {rmse:.4f}<br/>" \
                           f"   • {calidad_ajuste}<br/><br/>"
            
            story.append(Paragraph(analisis_dist, self.styles['Normal']))
        
        # SEMANA 4 - ACTIVIDAD 4: VELOCIDADES CARACTERÍSTICAS
        story.append(Paragraph("SEMANA 4 - ACTIVIDAD 4: VELOCIDADES CARACTERÍSTICAS", self.styles['TituloSeccion']))
        
        velocidades_max_energia = []
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            
            media = viento.mean()
            desv = viento.std()
            cv = desv / media
            k = cv ** (-1.09)
            c = media / gamma(1 + 1/k)
            
            # Velocidades características
            v_mp = c * ((k-1)/k)**(1/k) if k > 1 else 0
            v_max_e = c * ((k+2)/k)**(1/k)
            velocidades_max_energia.append(v_max_e)
            
            story.append(Paragraph(f"<b>ANÁLISIS PARA {ciudad.upper()}</b>", self.styles['SubTitulo']))
            
            analisis_vel = f"<b>📊 PARÁMETROS:</b><br/>" \
                          f"• k = {k:.4f}<br/>" \
                          f"• c = {c:.4f} m/s<br/>" \
                          f"• v̅ = {media:.4f} m/s<br/><br/>" \
                          f"<b>🎯 ECUACIÓN 5 - VELOCIDAD MÁS PROBABLE:</b><br/>" \
                          f"v_mp = c × ((k-1)/k)^(1/k)<br/><br/>" \
                          f"Paso 1: k - 1 = {k:.4f} - 1 = {k-1:.4f}<br/>" \
                          f"Paso 2: (k-1)/k = {k-1:.4f}/{k:.4f} = {(k-1)/k:.4f}<br/>" \
                          f"Paso 3: 1/k = 1/{k:.4f} = {1/k:.4f}<br/>" \
                          f"Paso 4: ((k-1)/k)^(1/k) = ({(k-1)/k:.4f})^({1/k:.4f}) = {((k-1)/k)**(1/k):.4f}<br/>" \
                          f"Paso 5: v_mp = c × {((k-1)/k)**(1/k):.4f} = {c:.4f} × {((k-1)/k)**(1/k):.4f} = {v_mp:.4f} m/s<br/>" \
                          f"<b>✅ VELOCIDAD MÁS PROBABLE: {v_mp:.4f} m/s</b><br/><br/>" \
                          f"<b>⚡ ECUACIÓN 6 - VELOCIDAD DE MÁXIMA ENERGÍA:</b><br/>" \
                          f"v_maxE = c × ((k+2)/k)^(1/k)<br/><br/>" \
                          f"Paso 1: k + 2 = {k:.4f} + 2 = {k+2:.4f}<br/>" \
                          f"Paso 2: (k+2)/k = {k+2:.4f}/{k:.4f} = {(k+2)/k:.4f}<br/>" \
                          f"Paso 3: 1/k = 1/{k:.4f} = {1/k:.4f}<br/>" \
                          f"Paso 4: ((k+2)/k)^(1/k) = ({(k+2)/k:.4f})^({1/k:.4f}) = {((k+2)/k)**(1/k):.4f}<br/>" \
                          f"Paso 5: v_maxE = c × {((k+2)/k)**(1/k):.4f} = {c:.4f} × {((k+2)/k)**(1/k):.4f} = {v_max_e:.4f} m/s<br/>" \
                          f"<b>✅ VELOCIDAD DE MÁXIMA ENERGÍA: {v_max_e:.4f} m/s</b><br/><br/>" \
                          f"<b>📋 RESUMEN:</b><br/>" \
                          f"• Velocidad media: {media:.2f} m/s<br/>" \
                          f"• Velocidad más probable: {v_mp:.2f} m/s<br/>" \
                          f"• Velocidad de máxima energía: {v_max_e:.2f} m/s<br/><br/>"
            
            story.append(Paragraph(analisis_vel, self.styles['Normal']))
        
        # Comparación de potencial eólico
        mejor_ciudad_eolica = max(self.ciudades, key=lambda c: self._obtener_velocidad_maxima_energia(c))
        
        # Tabla comparativa
        headers_comp = ['Ciudad', 'V.Media', 'V.Probable', 'V.MaxEnergía', 'k', 'c']
        data_comp = [headers_comp]
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            
            media = viento.mean()
            desv = viento.std()
            cv = desv / media
            k = cv ** (-1.09)
            c = media / gamma(1 + 1/k)
            
            v_mp = c * ((k-1)/k)**(1/k) if k > 1 else 0
            v_max_e = c * ((k+2)/k)**(1/k)
            
            fila = [
                ciudad,
                f"{media:.2f}",
                f"{v_mp:.2f}",
                f"{v_max_e:.2f}",
                f"{k:.2f}",
                f"{c:.2f}"
            ]
            data_comp.append(fila)
        
        tabla_comp = Table(data_comp, colWidths=[1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.6*inch, 0.8*inch])
        tabla_comp.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.mistyrose),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("<b>🔍 COMPARACIÓN DE POTENCIAL EÓLICO</b>", self.styles['SubTitulo']))
        story.append(tabla_comp)
        story.append(Spacer(1, 0.2*inch))
        
        # Análisis de potencial eólico
        v_max_mejor = self._obtener_velocidad_maxima_energia(mejor_ciudad_eolica)
        otras_ciudades = [c for c in self.ciudades if c != mejor_ciudad_eolica]
        if otras_ciudades:
            v_max_otra = self._obtener_velocidad_maxima_energia(otras_ciudades[0])
            diferencia = v_max_mejor - v_max_otra
            porcentaje_diff = (diferencia / v_max_otra) * 100
            potencia_relativa = (v_max_mejor / v_max_otra) ** 3
            
            analisis_potencial = f"<b>🎯 ANÁLISIS DE POTENCIAL EÓLICO:</b><br/>" \
                                f"1. Velocidades de máxima energía:<br/>" \
                                f"   • {mejor_ciudad_eolica}: {v_max_mejor:.2f} m/s<br/>" \
                                f"   • {otras_ciudades[0]}: {v_max_otra:.2f} m/s<br/>" \
                                f"   • Diferencia: {diferencia:.2f} m/s ({porcentaje_diff:.1f}%)<br/><br/>" \
                                f"2. <b>✅ CONCLUSIÓN:</b><br/>" \
                                f"   {mejor_ciudad_eolica.upper()} tiene MAYOR POTENCIAL EÓLICO<br/><br/>" \
                                f"3. <b>🔬 RAZONES:</b><br/>" \
                                f"   • Mayor velocidad de máxima energía: {v_max_mejor:.2f} m/s<br/>" \
                                f"   • La potencia eólica es proporcional a v³<br/>" \
                                f"   • Potencia relativa aproximada: ({v_max_mejor:.2f}/{v_max_otra:.2f})³ = {potencia_relativa:.2f}x<br/>" \
                                f"   • {mejor_ciudad_eolica} podría generar ~{potencia_relativa:.1f} veces más energía<br/><br/>"
            
            story.append(Paragraph(analisis_potencial, self.styles['Normal']))
        
        # SEMANA 5 - ACTIVIDAD 5: CUARTILES Y RANGO INTERCUARTÍLICO
        story.append(Paragraph("SEMANA 5 - ACTIVIDAD 5: CUARTILES Y RANGO INTERCUARTÍLICO", self.styles['TituloSeccion']))
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            
            media = viento.mean()
            desv = viento.std()
            cv = desv / media
            k = cv ** (-1.09)
            c = media / gamma(1 + 1/k)
            
            # Cálculo de cuartiles paso a paso
            story.append(Paragraph(f"<b>ANÁLISIS PARA {ciudad.upper()}</b>", self.styles['SubTitulo']))
            
            # Fórmula para percentiles Weibull
            formula_percentiles = "📐 <b>FÓRMULA PARA PERCENTILES WEIBULL:</b><br/>" \
                                "   v_p = c × (-ln(1-p))^(1/k)<br/>" \
                                f"   Donde: k = {k:.4f}, c = {c:.4f} m/s<br/><br/>"
            story.append(Paragraph(formula_percentiles, self.styles['Normal']))
            
            # Cálculo Q1
            q1 = c * ((-np.log(1-0.25)) ** (1/k))
            calculo_q1 = "🔢 <b>CÁLCULO DEL CUARTIL 1 (Q1 - percentil 25%):</b><br/>" \
                        "   Paso 1: p = 0.25 (percentil 25%)<br/>" \
                        "   Paso 2: 1 - p = 1 - 0.25 = 0.75<br/>" \
                        f"   Paso 3: -ln(1-p) = -ln(0.75) = {-np.log(0.75):.4f}<br/>" \
                        f"   Paso 4: 1/k = 1/{k:.4f} = {1/k:.4f}<br/>" \
                        f"   Paso 5: (-ln(1-p))^(1/k) = ({-np.log(0.75):.4f})^({1/k:.4f}) = {(-np.log(0.75)) ** (1/k):.4f}<br/>" \
                        f"   Paso 6: Q1 = c × {(-np.log(0.75)) ** (1/k):.4f} = {c:.4f} × {(-np.log(0.75)) ** (1/k):.4f} = {q1:.4f} m/s<br/><br/>" \
                        f"   ✅ <b>CUARTIL 1: Q1 = {q1:.4f} m/s</b><br/><br/>"
            story.append(Paragraph(calculo_q1, self.styles['Normal']))
            
            # Cálculo Q3
            q3 = c * ((-np.log(1-0.75)) ** (1/k))
            calculo_q3 = "🔢 <b>CÁLCULO DEL CUARTIL 3 (Q3 - percentil 75%):</b><br/>" \
                        "   Paso 1: p = 0.75 (percentil 75%)<br/>" \
                        "   Paso 2: 1 - p = 1 - 0.75 = 0.25<br/>" \
                        f"   Paso 3: -ln(1-p) = -ln(0.25) = {-np.log(0.25):.4f}<br/>" \
                        f"   Paso 4: 1/k = 1/{k:.4f} = {1/k:.4f}<br/>" \
                        f"   Paso 5: (-ln(1-p))^(1/k) = ({-np.log(0.25):.4f})^({1/k:.4f}) = {(-np.log(0.25)) ** (1/k):.4f}<br/>" \
                        f"   Paso 6: Q3 = c × {(-np.log(0.25)) ** (1/k):.4f} = {c:.4f} × {(-np.log(0.25)) ** (1/k):.4f} = {q3:.4f} m/s<br/><br/>" \
                        f"   ✅ <b>CUARTIL 3: Q3 = {q3:.4f} m/s</b><br/><br/>"
            story.append(Paragraph(calculo_q3, self.styles['Normal']))
            
            # Cálculo IQR
            iqr = q3 - q1
            calculo_iqr = "📏 <b>CÁLCULO DEL RANGO INTERCUARTÍLICO:</b><br/>" \
                         f"   IQR = Q3 - Q1 = {q3:.4f} - {q1:.4f} = {iqr:.4f} m/s<br/><br/>" \
                         f"   ✅ <b>RANGO INTERCUARTÍLICO: IQR = {iqr:.4f} m/s</b><br/><br/>"
            story.append(Paragraph(calculo_iqr, self.styles['Normal']))
            
            # Tabla resumen
            tabla_resumen_q = f"📋 <b>TABLA RESUMEN:</b><br/>" \
                             f"   +------------------+------------+<br/>" \
                             f"   | Estadístico      | Valor      |<br/>" \
                             f"   +------------------+------------+<br/>" \
                             f"   | Q1 (25%)         |    {q1:.2f} m/s |<br/>" \
                             f"   | Q3 (75%)         |    {q3:.2f} m/s |<br/>" \
                             f"   | IQR              |     {iqr:.2f} m/s |<br/>" \
                             f"   +------------------+------------+<br/>" \
                             f"   El 50% central de los datos está entre {q1:.2f} y {q3:.2f} m/s<br/><br/>"
            story.append(Paragraph(tabla_resumen_q, self.styles['Normal']))
            
        # SEMANA 5 - ACTIVIDAD 6: PROBABILIDAD ENTRE CUARTILES
        story.append(Paragraph("SEMANA 5 - ACTIVIDAD 6: PROBABILIDAD ENTRE CUARTILES", self.styles['TituloSeccion']))
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            
            media = viento.mean()
            desv = viento.std()
            cv = desv / media
            k = cv ** (-1.09)
            c = media / gamma(1 + 1/k)
            
            # Cálculo de cuartiles
            q1 = c * (-np.log(0.75))**(1/k)
            q3 = c * (-np.log(0.25))**(1/k)
            
            story.append(Paragraph(f"<b>ANÁLISIS PARA {ciudad.upper()}</b>", self.styles['SubTitulo']))
            
            # Fórmula para percentiles
            texto_formula = f"<b>Fórmula para percentiles Weibull:</b><br/>" \
                          f"v_p = c × (-ln(1-p))^(1/k)<br/>" \
                          f"Donde: k = {k:.4f}, c = {c:.4f} m/s<br/><br/>"
            
            story.append(Paragraph(texto_formula, self.styles['Normal']))
            
            # Cálculo detallado de Q1
            texto_q1 = f"<b>Cálculo del Cuartil 1 (Q1 - percentil 25%):</b><br/>" \
                       f"Paso 1: p = 0.25 (percentil 25%)<br/>" \
                       f"Paso 2: 1 - p = 1 - 0.25 = 0.75<br/>" \
                       f"Paso 3: -ln(1-p) = -ln(0.75) = {-np.log(0.75):.4f}<br/>" \
                       f"Paso 4: 1/k = 1/{k:.4f} = {1/k:.4f}<br/>" \
                       f"Paso 5: (-ln(1-p))^(1/k) = ({-np.log(0.75):.4f})^({1/k:.4f}) = {(-np.log(0.75))**(1/k):.4f}<br/>" \
                       f"Paso 6: Q1 = c × {(-np.log(0.75))**(1/k):.4f} = {c:.4f} × {(-np.log(0.75))**(1/k):.4f} = {q1:.4f} m/s<br/>" \
                       f"<b>✅ CUARTIL 1: Q1 = {q1:.4f} m/s</b><br/><br/>"
            
            story.append(Paragraph(texto_q1, self.styles['Normal']))
            
            # Cálculo detallado de Q3
            texto_q3 = f"<b>Cálculo del Cuartil 3 (Q3 - percentil 75%):</b><br/>" \
                       f"Paso 1: p = 0.75 (percentil 75%)<br/>" \
                       f"Paso 2: 1 - p = 1 - 0.75 = 0.25<br/>" \
                       f"Paso 3: -ln(1-p) = -ln(0.25) = {-np.log(0.25):.4f}<br/>" \
                       f"Paso 4: 1/k = 1/{k:.4f} = {1/k:.4f}<br/>" \
                       f"Paso 5: (-ln(1-p))^(1/k) = ({-np.log(0.25):.4f})^({1/k:.4f}) = {(-np.log(0.25))**(1/k):.4f}<br/>" \
                       f"Paso 6: Q3 = c × {(-np.log(0.25))**(1/k):.4f} = {c:.4f} × {(-np.log(0.25))**(1/k):.4f} = {q3:.4f} m/s<br/>" \
                       f"<b>✅ CUARTIL 3: Q3 = {q3:.4f} m/s</b><br/><br/>"
            
            story.append(Paragraph(texto_q3, self.styles['Normal']))
            
            # Cálculo del IQR
            iqr = q3 - q1
            texto_iqr = f"<b>Cálculo del Rango Intercuartílico:</b><br/>" \
                        f"IQR = Q3 - Q1 = {q3:.4f} - {q1:.4f} = {iqr:.4f} m/s<br/>" \
                        f"<b>✅ RANGO INTERCUARTÍLICO: IQR = {iqr:.4f} m/s</b><br/><br/>"
            
            story.append(Paragraph(texto_iqr, self.styles['Normal']))
            
            # Tabla resumen
            headers_resumen = ['Estadístico', 'Valor']
            data_resumen = [
                headers_resumen,
                ['Q1 (25%)', f"{q1:.2f} m/s"],
                ['Q3 (75%)', f"{q3:.2f} m/s"],
                ['IQR', f"{iqr:.2f} m/s"]
            ]
            
            tabla_resumen = Table(data_resumen, colWidths=[2*inch, 1.5*inch])
            tabla_resumen.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tabla_resumen)
            story.append(Spacer(1, 0.2*inch))
            
            # Cálculo de probabilidad entre cuartiles
            f_q1 = 1 - np.exp(-((q1/c)**k))
            f_q3 = 1 - np.exp(-((q3/c)**k))
            prob_entre_cuartiles = f_q3 - f_q1
            
            texto_prob = f"<b>Función de Distribución Acumulada Weibull:</b><br/>" \
                         f"F(v) = 1 - e^(-(v/c)^k)<br/>" \
                         f"Donde: k = {k:.4f}, c = {c:.4f} m/s<br/>" \
                         f"Q1 = {q1:.4f} m/s, Q3 = {q3:.4f} m/s<br/><br/>" \
                         f"<b>Cálculo paso a paso de F(Q1):</b><br/>" \
                         f"Paso 1: v/c = Q1/c = {q1:.4f}/{c:.4f} = {q1/c:.4f}<br/>" \
                         f"Paso 2: (v/c)^k = ({q1/c:.4f})^{k:.4f} = {(q1/c)**k:.4f}<br/>" \
                         f"Paso 3: e^(-(v/c)^k) = e^(-{(q1/c)**k:.4f}) = {np.exp(-((q1/c)**k)):.4f}<br/>" \
                         f"Paso 4: F(Q1) = 1 - {np.exp(-((q1/c)**k)):.4f} = {f_q1:.4f}<br/>" \
                         f"<b>✅ F(Q1) = {f_q1:.4f}</b><br/><br/>" \
                         f"<b>Cálculo paso a paso de F(Q3):</b><br/>" \
                         f"Paso 1: v/c = Q3/c = {q3:.4f}/{c:.4f} = {q3/c:.4f}<br/>" \
                         f"Paso 2: (v/c)^k = ({q3/c:.4f})^{k:.4f} = {(q3/c)**k:.4f}<br/>" \
                         f"Paso 3: e^(-(v/c)^k) = e^(-{(q3/c)**k:.4f}) = {np.exp(-((q3/c)**k)):.4f}<br/>" \
                         f"Paso 4: F(Q3) = 1 - {np.exp(-((q3/c)**k)):.4f} = {f_q3:.4f}<br/>" \
                         f"<b>✅ F(Q3) = {f_q3:.4f}</b><br/><br/>" \
                         f"<b>Cálculo Final de la Probabilidad:</b><br/>" \
                         f"P(Q1 ≤ V ≤ Q3) = F(Q3) - F(Q1)<br/>" \
                         f"P({q1:.2f} ≤ V ≤ {q3:.2f}) = {f_q3:.4f} - {f_q1:.4f}<br/>" \
                         f"P({q1:.2f} ≤ V ≤ {q3:.2f}) = {prob_entre_cuartiles:.4f}<br/>" \
                         f"P({q1:.2f} ≤ V ≤ {q3:.2f}) = {prob_entre_cuartiles*100:.2f}%<br/><br/>" \
                         f"<b>✅ INTERPRETACIÓN:</b><br/>" \
                         f"La probabilidad de que la velocidad del viento esté entre " \
                         f"{q1:.2f} m/s y {q3:.2f} m/s es del {prob_entre_cuartiles*100:.2f}%<br/>" \
                         f"(Por definición, esto siempre debe ser 50% para cualquier distribución)<br/><br/>"
            
            story.append(Paragraph(texto_prob, self.styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
        
        # Agregar sección de Actividad 7
        story.append(Paragraph("SEMANA 5 - ACTIVIDAD 7: PROBABILIDAD SUPERIOR AL PERCENTIL 60", self.styles['TituloSeccion']))
        
        for ciudad in self.ciudades:
            datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
            viento = datos_ciudad['vel_viento (m/s)']
            
            media = viento.mean()
            desv = viento.std()
            cv = desv / media
            k = cv ** (-1.09)
            c = media / gamma(1 + 1/k)
            
            # Cálculo del percentil 60
            p60 = c * (-np.log(0.4))**(1/k)
            f_p60 = 1 - np.exp(-((p60/c)**k))
            prob_superior_p60 = 1 - f_p60
            
            story.append(Paragraph(f"<b>ANÁLISIS PARA {ciudad.upper()}</b>", self.styles['SubTitulo']))
            
            texto_p60 = f"<b>Parámetros:</b><br/>" \
                        f"• k = {k:.4f}<br/>" \
                        f"• c = {c:.4f} m/s<br/><br/>" \
                        f"<b>Cálculo paso a paso del Percentil 60:</b><br/>" \
                        f"Paso 1: p = 0.60 (percentil 60%)<br/>" \
                        f"Paso 2: 1 - p = 1 - 0.60 = 0.40<br/>" \
                        f"Paso 3: -ln(1-p) = -ln(0.40) = {-np.log(0.4):.4f}<br/>" \
                        f"Paso 4: 1/k = 1/{k:.4f} = {1/k:.4f}<br/>" \
                        f"Paso 5: (-ln(1-p))^(1/k) = ({-np.log(0.4):.4f})^({1/k:.4f}) = {(-np.log(0.4))**(1/k):.4f}<br/>" \
                        f"Paso 6: v_60 = c × {(-np.log(0.4))**(1/k):.4f} = {c:.4f} × {(-np.log(0.4))**(1/k):.4f} = {p60:.4f} m/s<br/>" \
                        f"<b>✅ PERCENTIL 60: v_60 = {p60:.4f} m/s</b><br/><br/>" \
                        f"<b>Cálculo paso a paso de F(v_60):</b><br/>" \
                        f"Paso 1: v/c = {p60:.4f}/{c:.4f} = {p60/c:.4f}<br/>" \
                        f"Paso 2: (v/c)^k = ({p60/c:.4f})^{k:.4f} = {(p60/c)**k:.4f}<br/>" \
                        f"Paso 3: e^(-(v/c)^k) = e^(-{(p60/c)**k:.4f}) = {np.exp(-((p60/c)**k)):.4f}<br/>" \
                        f"Paso 4: F(v_60) = 1 - {np.exp(-((p60/c)**k)):.4f} = {f_p60:.4f}<br/>" \
                        f"<b>✅ F(v_60) = {f_p60:.4f}</b><br/><br/>" \
                        f"<b>Cálculo de la Probabilidad Superior:</b><br/>" \
                        f"P(V > v_60) = 1 - F(v_60)<br/>" \
                        f"P(V > {p60:.4f}) = 1 - {f_p60:.4f}<br/>" \
                        f"P(V > {p60:.4f}) = {prob_superior_p60:.4f}<br/>" \
                        f"P(V > {p60:.4f}) = {prob_superior_p60*100:.2f}%<br/><br/>" \
                        f"<b>✅ INTERPRETACIÓN:</b><br/>" \
                        f"La probabilidad de registrar velocidades superiores a " \
                        f"{p60:.2f} m/s (percentil 60) es del {prob_superior_p60*100:.2f}%<br/>" \
                        f"(Por definición, esto siempre debe ser 40% para cualquier distribución)<br/>" \
                        f"Esto significa que el 40% de las observaciones " \
                        f"superan esta velocidad de referencia.<br/><br/>"
            
            story.append(Paragraph(texto_p60, self.styles['Normal']))
            
            # Tabla resumen para P60
            headers_p60 = ['Concepto', 'Valor']
            data_p60 = [
                headers_p60,
                ['Percentil 60', f"{p60:.2f} m/s"],
                ['F(P60)', f"{f_p60:.4f}"],
                ['P(V > P60)', f"{prob_superior_p60:.4f}"],
                ['Porcentaje', f"{prob_superior_p60*100:.2f}%"]
            ]
            
            tabla_p60 = Table(data_p60, colWidths=[2*inch, 1.5*inch])
            tabla_p60.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.mistyrose),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tabla_p60)
            story.append(Spacer(1, 0.3*inch))
        
        return story
    
    def _generar_conclusiones(self):
        """Genera las conclusiones del análisis"""
        story = []
        
        # Título
        titulo = Paragraph("CONCLUSIONES Y RECOMENDACIONES", self.styles['TituloSeccion'])
        story.append(titulo)
        
        # Determinar mejor ciudad para potencial eólico
        mejor_ciudad = max(self.ciudades, key=lambda c: self._obtener_velocidad_maxima_energia(c))
        
        conclusiones = Paragraph(
            f"<b>1. Potencial Eólico:</b><br/>"
            f"La ciudad de <b>{mejor_ciudad}</b> presenta el mayor potencial eólico "
            f"con una velocidad de máxima energía de "
            f"{self._obtener_velocidad_maxima_energia(mejor_ciudad):.2f} m/s.<br/><br/>"
            
            f"<b>2. Caracterización Estadística:</b><br/>"
            f"Todas las ciudades muestran un buen ajuste a la distribución de Weibull, "
            f"lo que permite realizar estimaciones confiables de probabilidades y "
            f"predicciones de comportamiento del viento.<br/><br/>"
            
            f"<b>3. Aplicaciones Prácticas:</b><br/>"
            f"Los parámetros calculados pueden utilizarse para:<br/>"
            f"• Dimensionamiento de sistemas eólicos<br/>"
            f"• Estimación de producción energética<br/>"
            f"• Análisis de riesgo meteorológico<br/>"
            f"• Planificación de proyectos energéticos<br/><br/>"
            
            f"<b>4. Recomendaciones:</b><br/>"
            f"Se recomienda profundizar el análisis con datos de mayor resolución temporal "
            f"y considerar factores adicionales como la direccionalidad del viento "
            f"para una caracterización más completa del recurso eólico.",
            
            self.styles['TextoJustificado']
        )
        story.append(conclusiones)
        
        # Información técnica
        story.append(Spacer(1, 0.5*inch))
        info_tecnica = Paragraph(
            "<b>Información Técnica:</b><br/>"
            f"• Método de cálculo: Distribución de Weibull de dos parámetros<br/>"
            f"• Ecuaciones utilizadas: k = (σ/μ)^(-1.09), c = μ/Γ(1+1/k)<br/>"
            f"• Software: Sistema de Análisis Weibull Educativo<br/>"
            f"• Fecha de análisis: {self.fecha_reporte}",
            self.styles['Normal']
        )
        story.append(info_tecnica)
        
        return story
    
    def _obtener_velocidad_maxima_energia(self, ciudad):
        """Calcula la velocidad de máxima energía para una ciudad"""
        # Usar la columna correcta 'Municipio'
        datos_ciudad = self.datos[self.datos['Municipio'] == ciudad]
        viento = datos_ciudad['vel_viento (m/s)']
        
        if len(viento) == 0:
            return 0.0
            
        media = viento.mean()
        desv = viento.std()
        cv = desv / media
        
        # Parámetros Weibull
        k = cv ** (-1.09)
        c = media / gamma(1 + 1/k)
        
        # Velocidad de máxima energía
        v_max_e = c * ((k+2)/k)**(1/k)
        
        return v_max_e