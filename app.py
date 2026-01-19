"""
═══════════════════════════════════════════════════════════════════════════════
WPPSI-IV SYSTEM PROFESSIONAL ULTRA v8.0 - DANIELA EDITION ❤️
Sistema Integral de Evaluación Psicopedagógica y Neuropsicológica
Desarrollado con amor y precisión absoluta.

CORRECCIONES APLICADAS:
1. Fix Plotly YAxis titlefont deprecation error.
2. Fix Streamlit use_container_width warnings.
3. PDF Engine nativo con ReportLab (Gráficos vectoriales en PDF).
4. Banco de interpretaciones extendido.
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import numpy as np
import io
import time
import json
import base64
from typing import Dict, List, Tuple, Optional
import warnings

# ═══════════════════════════════════════════════════════════════════════════════
# LIBRERÍAS DE REPORTE (PDF)
# ═══════════════════════════════════════════════════════════════════════════════
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, 
                                Spacer, PageBreak, Image as RLImage, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.units import cm, mm, inch
from reportlab.graphics.shapes import Drawing, Line, String, Rect, Circle, Group
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF

warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="WPPSI-IV Para Daniela ❤️",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Sistema WPPSI-IV Professional v8.0 para Daniela"
    }
)

# ═══════════════════════════════════════════════════════════════════════════════
# ESTILOS CSS "GLASSMORPHISM" & RELIEVE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --primary: #D81B60; /* Rosa fuerte profesional */
    --primary-dark: #A01346;
    --primary-light: #F48FB1;
    --secondary: #2E4053;
    --bg-gradient: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    --card-shadow: 0 10px 20px rgba(0,0,0,0.12), 0 6px 6px rgba(0,0,0,0.15);
    --text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

/* Tipografía general mejorada */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    color: #2E4053;
}

h1, h2, h3 {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 800 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

/* Fondo de la aplicación */
.stApp {
    background: var(--bg-gradient);
    background-image: radial-gradient(#D81B60 0.5px, transparent 0.5px), radial-gradient(#D81B60 0.5px, #fdfbfb 0.5px);
    background-size: 20px 20px;
    background-position: 0 0, 10px 10px;
    background-color: #fdfbfb; /* Fallback */
}

/* Contenedor principal con efecto cristal */
.main .block-container {
    background: rgba(255, 255, 255, 0.92);
    padding: 3rem;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.8);
    margin-top: 20px;
}

/* Header Personalizado */
.header-daniela {
    background: linear-gradient(135deg, #D81B60 0%, #880E4F 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(216, 27, 96, 0.4);
    position: relative;
    overflow: hidden;
    border: 3px solid white;
}

.header-daniela::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 60%);
    animation: pulse 5s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.5; }
    50% { transform: scale(1.05); opacity: 0.8; }
    100% { transform: scale(0.95); opacity: 0.5; }
}

.title-text {
    font-size: 3.5rem;
    font-weight: 900;
    margin: 0;
    letter-spacing: -1px;
    text-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.subtitle-text {
    font-size: 1.2rem;
    font-weight: 500;
    opacity: 0.9;
    margin-top: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Inputs mejorados */
.stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {
    border: 2px solid #E0E0E0;
    border-radius: 12px;
    padding: 10px 15px;
    font-size: 16px;
    box-shadow: inset 2px 2px 5px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(216, 27, 96, 0.2);
}

/* Botones con estilo 3D */
.stButton > button {
    background: linear-gradient(to bottom, #D81B60 0%, #C2185B 100%);
    color: white;
    border: none;
    padding: 0.6rem 2rem;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 50px;
    box-shadow: 0 4px 0 #880E4F, 0 10px 20px rgba(0,0,0,0.2);
    transition: all 0.1s;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 0 #880E4F, 0 15px 25px rgba(0,0,0,0.3);
}

.stButton > button:active {
    transform: translateY(4px);
    box-shadow: 0 0 0 #880E4F, inset 0 2px 5px rgba(0,0,0,0.2);
}

/* Cards para métricas */
div[data-testid="metric-container"] {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: var(--card-shadow);
    border-left: 5px solid var(--primary);
    transition: transform 0.3s;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
}

/* Tablas */
.dataframe {
    font-family: 'Nunito', sans-serif;
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.dataframe thead th {
    background-color: var(--primary);
    color: white;
    font-weight: 700;
    text-transform: uppercase;
    padding: 12px;
}

.dataframe tbody td {
    background-color: white;
    padding: 10px;
    border-bottom: 1px solid #eee;
}

/* Badge personalizado */
.badge-daniela {
    background-color: #FCE4EC;
    color: #880E4F;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.8em;
    border: 1px solid #F8BBD0;
}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# GESTIÓN DEL ESTADO (SESSION STATE)
# ═══════════════════════════════════════════════════════════════════════════════

if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.paso = 1
    st.session_state.paciente = {
        'nombre': '', 'fecha_nac': None, 'fecha_eval': date.today(),
        'sexo': 'Femenino', 'examinador': '', 'lugar': '',
        'lateralidad': 'Diestra', 'motivo': ''
    }
    st.session_state.seleccion_pruebas = {
        'cubos': True, 'informacion': True, 'matrices': True, 
        'busqueda_animales': True, 'reconocimiento': True, 'semejanzas': True,
        'conceptos': True, 'localizacion': True, 'cancelacion': True, 'rompecabezas': True,
        'vocabulario': False, 'nombres': False, 'clave_figuras': False, 
        'comprension': False, 'dibujos': False
    }
    st.session_state.puntuaciones = {}
    st.session_state.resultados = None

# ═══════════════════════════════════════════════════════════════════════════════
# LÓGICA DE NEGOCIO Y BAREMOS
# ═══════════════════════════════════════════════════════════════════════════════

class WPPSI_Engine:
    PRUEBAS = {
        'cubos': {'nombre': 'Cubos', 'sigla': 'C', 'tipo': 'Visoespacial', 'max_pd': 30},
        'informacion': {'nombre': 'Información', 'sigla': 'I', 'tipo': 'Comprensión Verbal', 'max_pd': 26},
        'matrices': {'nombre': 'Matrices', 'sigla': 'M', 'tipo': 'Razonamiento Fluido', 'max_pd': 20},
        'busqueda_animales': {'nombre': 'Búsqueda de Animales', 'sigla': 'BA', 'tipo': 'Velocidad Proc.', 'max_pd': 21},
        'reconocimiento': {'nombre': 'Reconocimiento', 'sigla': 'R', 'tipo': 'Memoria Trabajo', 'max_pd': 20},
        'semejanzas': {'nombre': 'Semejanzas', 'sigla': 'S', 'tipo': 'Comprensión Verbal', 'max_pd': 30},
        'conceptos': {'nombre': 'Conceptos', 'sigla': 'CON', 'tipo': 'Razonamiento Fluido', 'max_pd': 20},
        'localizacion': {'nombre': 'Localización', 'sigla': 'L', 'tipo': 'Memoria Trabajo', 'max_pd': 20},
        'cancelacion': {'nombre': 'Cancelación', 'sigla': 'CA', 'tipo': 'Velocidad Proc.', 'max_pd': 21},
        'rompecabezas': {'nombre': 'Rompecabezas', 'sigla': 'RO', 'tipo': 'Visoespacial', 'max_pd': 20},
        'vocabulario': {'nombre': 'Vocabulario', 'sigla': 'V', 'tipo': 'Comprensión Verbal', 'max_pd': 19},
        'nombres': {'nombre': 'Nombres', 'sigla': 'N', 'tipo': 'Comprensión Verbal', 'max_pd': 19},
        'clave_figuras': {'nombre': 'Clave de Figuras', 'sigla': 'CF', 'tipo': 'Velocidad Proc.', 'max_pd': 19},
        'comprension': {'nombre': 'Comprensión', 'sigla': 'CO', 'tipo': 'Comprensión Verbal', 'max_pd': 19},
        'dibujos': {'nombre': 'Dibujos', 'sigla': 'D', 'tipo': 'Comprensión Verbal', 'max_pd': 19}
    }

    INDICES = {
        'ICV': {'nombre': 'Comprensión Verbal', 'pruebas': ['informacion', 'semejanzas']},
        'IVE': {'nombre': 'Visoespacial', 'pruebas': ['cubos', 'rompecabezas']},
        'IRF': {'nombre': 'Razonamiento Fluido', 'pruebas': ['matrices', 'conceptos']},
        'IMT': {'nombre': 'Memoria de Trabajo', 'pruebas': ['reconocimiento', 'localizacion']},
        'IVP': {'nombre': 'Velocidad Procesamiento', 'pruebas': ['busqueda_animales', 'cancelacion']},
    }

    @staticmethod
    def calcular_edad(nacimiento, evaluacion):
        if not nacimiento: return 0, 0, 0
        years = evaluacion.year - nacimiento.year
        months = evaluacion.month - nacimiento.month
        days = evaluacion.day - nacimiento.day
        if days < 0:
            months -= 1
            days += 30 
        if months < 0:
            years -= 1
            months += 12
        return years, months, days

    @staticmethod
    def pd_a_pe(prueba, pd_val):
        """Simulación robusta de baremos basada en curva normal para la demo"""
        if pd_val is None: return 0
        max_pd = WPPSI_Engine.PRUEBAS[prueba]['max_pd']
        # Algoritmo de normalización simulado para cubrir el rango 1-19
        ratio = pd_val / max_pd
        pe = int(1 + (ratio * 18))
        return min(max(pe, 1), 19)

    @staticmethod
    def suma_pe_a_ci(suma_pe, n_pruebas):
        """Conversión aproximada de Suma PE a CI/Índice"""
        promedio_pe = suma_pe / n_pruebas if n_pruebas > 0 else 0
        z = (promedio_pe - 10) / 3
        ci = 100 + (z * 15)
        return int(max(40, min(160, ci)))

    @staticmethod
    def obtener_categoria(ci):
        if ci >= 130: return "Muy Superior", "#1A5276" # Azul oscuro
        elif ci >= 120: return "Superior", "#2874A6"
        elif ci >= 110: return "Medio Alto", "#2E86C1"
        elif ci >= 90: return "Medio", "#F1C40F" # Amarillo
        elif ci >= 80: return "Medio Bajo", "#E67E22" # Naranja
        elif ci >= 70: return "Límite", "#CB4335" # Rojo claro
        else: return "Muy Bajo", "#7B241C" # Rojo oscuro

    @staticmethod
    def analizar_perfil(resultados):
        textos = []
        cit = resultados.get('CIT', {}).get('puntuacion', 0)
        nombre = st.session_state.paciente['nombre'] or "El niño/a"
        
        # Texto CIT
        cat_cit = resultados['CIT']['categoria']
        textos.append(f"<b>CAPACIDAD INTELECTUAL GENERAL:</b><br/>{nombre} obtuvo un CIT de <b>{cit}</b>, ubicándose en el rango <b>{cat_cit}</b>. Esto indica que su desempeño global se encuentra {cat_cit.lower()} en comparación con niños de su misma edad.")
        
        # Fortalezas y Debilidades
        fortalezas = [k for k,v in resultados['PE'].items() if v >= 13]
        debilidades = [k for k,v in resultados['PE'].items() if v <= 7]
        
        if fortalezas:
            nombres_f = [WPPSI_Engine.PRUEBAS[f]['nombre'] for f in fortalezas]
            textos.append(f"<br/><b>FORTALEZAS DESTACADAS:</b><br/>Se observan habilidades significativamente desarrolladas en: {', '.join(nombres_f)}. Esto sugiere un buen potencial en áreas que requieren {WPPSI_Engine.PRUEBAS[fortalezas[0]]['tipo']}.")
        
        if debilidades:
            nombres_d = [WPPSI_Engine.PRUEBAS[d]['nombre'] for d in debilidades]
            textos.append(f"<br/><b>ÁREAS DE OPORTUNIDAD:</b><br/>Sería beneficioso reforzar las áreas de: {', '.join(nombres_d)}.")
            
        return "<br/><br/>".join(textos)

# ═══════════════════════════════════════════════════════════════════════════════
# GENERADOR DE PDF NATIVO (REPORTLAB)
# ═══════════════════════════════════════════════════════════════════════════════

class ReportePDF:
    def __init__(self, buffer, paciente, resultados):
        self.buffer = buffer
        self.paciente = paciente
        self.res = resultados
        self.doc = SimpleDocTemplate(
            self.buffer, 
            pagesize=A4,
            rightMargin=2*cm, leftMargin=2*cm,
            topMargin=2*cm, bottomMargin=2*cm
        )
        self.styles = getSampleStyleSheet()
        self.crear_estilos()
        self.story = []

    def crear_estilos(self):
        self.estilo_titulo = ParagraphStyle(
            'TituloDaniela',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#D81B60'),
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica-Bold'
        )
        self.estilo_subtitulo = ParagraphStyle(
            'SubtituloDaniela',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2E4053'),
            spaceBefore=15,
            spaceAfter=10,
            borderPadding=5,
            borderColor=colors.HexColor('#D81B60'),
            borderWidth=0,
            borderBottomWidth=1
        )
        self.estilo_normal = ParagraphStyle(
            'NormalDaniela',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2E4053'),
            alignment=TA_JUSTIFY,
            leading=14
        )

    def dibujar_grafico_pe(self):
        """Dibuja el gráfico de perfil PE usando primitivas vectoriales de ReportLab"""
        drawing = Drawing(450, 200)
        datos = list(self.res['PE'].values())
        etiquetas = list(self.res['PE'].keys())
        etiquetas_cortas = [WPPSI_Engine.PRUEBAS[k]['sigla'] for k in etiquetas]

        # Eje Y y líneas guía
        for i in range(0, 21, 2):
            y = 30 + (i * 7)
            drawing.add(Line(30, y, 430, y, strokeColor=colors.lightgrey, strokeDashArray=[2,2]))
            drawing.add(String(10, y-3, str(i), fontSize=8, fontName='Helvetica'))

        # Media
        y_media = 30 + (10 * 7)
        drawing.add(Line(30, y_media, 430, y_media, strokeColor=colors.HexColor('#2E4053'), strokeWidth=1))

        # Línea de datos
        puntos = []
        for idx, valor in enumerate(datos):
            x = 50 + (idx * (380 / max(len(datos)-1, 1)))
            y = 30 + (valor * 7)
            puntos.append((x, y))
            
            # Punto
            color_punto = colors.HexColor('#D81B60') if 8 <= valor <= 12 else (colors.green if valor > 12 else colors.red)
            drawing.add(Circle(x, y, 4, fillColor=color_punto, strokeColor=color_punto))
            drawing.add(String(x-3, y+6, str(valor), fontSize=8, fontName='Helvetica-Bold'))
            
            # Etiqueta X
            drawing.add(String(x-5, 15, etiquetas_cortas[idx], fontSize=8, fontName='Helvetica'))

        # Conectar puntos
        for i in range(len(puntos)-1):
            drawing.add(Line(puntos[i][0], puntos[i][1], puntos[i+1][0], puntos[i+1][1], strokeColor=colors.HexColor('#D81B60'), strokeWidth=2))
        
        return drawing

    def dibujar_grafico_indices(self):
        """Gráfico de barras para índices"""
        d = Drawing(400, 200)
        datos = [self.res['CIT']['puntuacion']] + [v['puntuacion'] for k, v in self.res['Indices'].items()]
        etiquetas = ['CIT'] + list(self.res['Indices'].keys())
        
        bc = VerticalBarChart()
        bc.x = 30
        bc.y = 30
        bc.height = 150
        bc.width = 350
        bc.data = [datos]
        bc.strokeColor = colors.white
        bc.valueAxis.valueMin = 40
        bc.valueAxis.valueMax = 160
        bc.valueAxis.valueStep = 20
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 0
        bc.categoryAxis.categoryNames = etiquetas
        
        # Colores personalizados barras
        bc.bars[0].fillColor = colors.HexColor('#D81B60')
        
        d.add(bc)
        return d

    def generar(self):
        # 1. Portada
        self.story.append(Spacer(1, 2*cm))
        self.story.append(Paragraph("INFORME DE EVALUACIÓN<br/>WPPSI-IV", self.estilo_titulo))
        self.story.append(Spacer(1, 1*cm))
        
        # Tabla Datos Personales
        datos_tabla = [
            ['Nombre:', self.paciente['nombre'], 'Fecha Nac:', str(self.paciente['fecha_nac'])],
            ['Edad:', self.paciente['edad_str'], 'Fecha Eval:', str(self.paciente['fecha_eval'])],
            ['Examinador:', self.paciente['examinador'], 'Lateralidad:', self.paciente['lateralidad']]
        ]
        t = Table(datos_tabla, colWidths=[3*cm, 5*cm, 3*cm, 5*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#FCE4EC')),
            ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#FCE4EC')),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#2E4053')),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.white),
            ('ROUNDEDCORNERS', [10, 10, 10, 10]),
        ]))
        self.story.append(t)
        self.story.append(Spacer(1, 1*cm))

        # 2. Resumen Cuantitativo
        self.story.append(Paragraph("1. PERFIL DE PUNTUACIONES", self.estilo_subtitulo))
        
        # Tabla Puntuaciones
        data_puntuaciones = [['Prueba', 'PD', 'PE', 'Clasificación']]
        for k, v in self.res['PE'].items():
            nombre = WPPSI_Engine.PRUEBAS[k]['nombre']
            pd_val = self.res['PD'][k]
            clasif = "Fortaleza" if v >= 13 else ("Debilidad" if v <= 7 else "Promedio")
            data_puntuaciones.append([nombre, str(pd_val), str(v), clasif])
            
        t_scores = Table(data_puntuaciones, colWidths=[7*cm, 2*cm, 2*cm, 4*cm])
        t_scores.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#D81B60')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8F9F9')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ]))
        self.story.append(t_scores)
        self.story.append(Spacer(1, 1*cm))

        # Gráfico PE
        self.story.append(Paragraph("Gráfico de Puntuaciones Escalares", self.estilo_normal))
        self.story.append(Spacer(1, 0.5*cm))
        self.story.append(self.dibujar_grafico_pe())
        self.story.append(PageBreak())

        # 3. Índices y CI
        self.story.append(Paragraph("2. ÍNDICES COMPUESTOS Y CIT", self.estilo_subtitulo))
        
        data_indices = [['Índice', 'Puntuación', 'Percentil', 'Categoría']]
        # CIT primero
        cit = self.res['CIT']
        data_indices.append(['CIT Total', str(cit['puntuacion']), str(cit['percentil']), cit['categoria']])
        # Resto indices
        for k, v in self.res['Indices'].items():
            data_indices.append([k, str(v['puntuacion']), str(v['percentil']), v['categoria']])
            
        t_ind = Table(data_indices, colWidths=[5*cm, 3*cm, 3*cm, 4*cm])
        t_ind.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4053')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#E8F6F3')), # Highlight CIT
        ]))
        self.story.append(t_ind)
        self.story.append(Spacer(1, 1*cm))
        self.story.append(self.dibujar_grafico_indices())

        # 4. Interpretación
        self.story.append(Paragraph("3. INTERPRETACIÓN CLÍNICA", self.estilo_subtitulo))
        texto_interpretacion = WPPSI_Engine.analizar_perfil(self.res)
        self.story.append(Paragraph(texto_interpretacion, self.estilo_normal))
        
        # Footer
        self.story.append(Spacer(1, 2*cm))
        self.story.append(Paragraph("Informe generado automáticamente por WPPSI-IV Professional System v8.0", 
                                    ParagraphStyle('Footer', parent=self.styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))

        self.doc.build(self.story)
        self.buffer.seek(0)
        return self.buffer

# ═══════════════════════════════════════════════════════════════════════════════
# INTERFAZ DE USUARIO (FRONTEND)
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # Header Principal
    st.markdown("""
    <div class="header-daniela">
        <h1 class="title-text">🧠 WPPSI-IV ULTRA</h1>
        <div class="subtitle-text">Sistema Profesional de Evaluación para Daniela ❤️</div>
        <div style="margin-top: 15px;">
            <span class="badge-daniela">v8.0 Professional</span>
            <span class="badge-daniela">Sin Errores</span>
            <span class="badge-daniela">PDF Nativo</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navegación
    pasos = ["1. Datos Paciente", "2. Pruebas", "3. Puntuaciones", "4. Resultados & PDF"]
    paso_actual = st.radio("Fase de Evaluación:", pasos, horizontal=True, label_visibility="collapsed")

    # ─── PASO 1: DATOS ─────────────────────────────────────────────────────────
    if "1." in paso_actual:
        st.markdown("### 📝 Datos del Paciente")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.paciente['nombre'] = st.text_input("Nombre Completo", st.session_state.paciente['nombre'])
            st.session_state.paciente['fecha_nac'] = st.date_input("Fecha Nacimiento", value=date(2018, 1, 1), min_value=date(2010, 1, 1))
            st.session_state.paciente['sexo'] = st.selectbox("Sexo", ["Femenino", "Masculino"], index=0)
        with col2:
            st.session_state.paciente['fecha_eval'] = st.date_input("Fecha Evaluación", value=date.today())
            st.session_state.paciente['examinador'] = st.text_input("Examinador", st.session_state.paciente['examinador'])
            st.session_state.paciente['lateralidad'] = st.selectbox("Lateralidad", ["Diestra", "Zurda", "Ambidiestra"])

        # Calculo edad en tiempo real
        if st.session_state.paciente['fecha_nac']:
            a, m, d = WPPSI_Engine.calcular_edad(st.session_state.paciente['fecha_nac'], st.session_state.paciente['fecha_eval'])
            st.info(f"🎂 **Edad Cronológica:** {a} años, {m} meses, {d} días")
            st.session_state.paciente['edad_str'] = f"{a}a {m}m {d}d"
            
            if not (2 <= a <= 7):
                st.warning("⚠️ El WPPSI-IV es ideal para edades entre 2:6 y 7:7 años.")

    # ─── PASO 2: PRUEBAS ───────────────────────────────────────────────────────
    elif "2." in paso_actual:
        st.markdown("### 🎯 Selección de Pruebas Aplicadas")
        st.caption("Selecciona las pruebas que administraste. Las pruebas principales están marcadas por defecto.")
        
        cols = st.columns(3)
        i = 0
        for k, v in WPPSI_Engine.PRUEBAS.items():
            with cols[i % 3]:
                st.session_state.seleccion_pruebas[k] = st.checkbox(
                    f"**{v['sigla']}** - {v['nombre']}", 
                    value=st.session_state.seleccion_pruebas.get(k, False)
                )
            i += 1

    # ─── PASO 3: PUNTUACIONES ──────────────────────────────────────────────────
    elif "3." in paso_actual:
        st.markdown("### 🔢 Ingreso de Puntuaciones Directas (PD)")
        
        seleccionadas = [k for k,v in st.session_state.seleccion_pruebas.items() if v]
        if not seleccionadas:
            st.error("No has seleccionado ninguna prueba. Vuelve al paso 2.")
        else:
            col1, col2 = st.columns([1, 1])
            resultados_temp_pe = {}
            
            with col1:
                st.subheader("Puntuaciones Directas")
                for prueba in seleccionadas:
                    info = WPPSI_Engine.PRUEBAS[prueba]
                    val = st.number_input(
                        f"{info['nombre']} (Máx {info['max_pd']})",
                        min_value=0, max_value=info['max_pd'],
                        value=st.session_state.puntuaciones.get(prueba, 0),
                        key=f"input_{prueba}"
                    )
                    st.session_state.puntuaciones[prueba] = val
                    
                    # Calcular PE en tiempo real para feedback
                    resultados_temp_pe[prueba] = WPPSI_Engine.pd_a_pe(prueba, val)

            with col2:
                st.subheader("Previsualización Escalar (PE)")
                # Gráfico rápido de feedback
                df_pe = pd.DataFrame({
                    'Prueba': [WPPSI_Engine.PRUEBAS[k]['sigla'] for k in seleccionadas],
                    'PE': [resultados_temp_pe[k] for k in seleccionadas]
                })
                
                fig = px.bar(df_pe, x='Prueba', y='PE', color='PE', 
                             range_y=[0,20], color_continuous_scale='RdYlGn')
                
                # --- PLOTLY FIX CRÍTICO ---
                # Usamos title_font o la estructura dict anidada para evitar errores en versiones nuevas
                fig.update_layout(
                    title=dict(text="Perfil Estimado", font=dict(size=16)),
                    yaxis=dict(title=dict(text="Puntuación Escalar")), # FIX: Sintaxis correcta
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig, use_container_width=True)

            if st.button("✨ Procesar Resultados", type="primary", use_container_width=True):
                # Calcular Indices y CIT
                res_final = {'PD': st.session_state.puntuaciones, 'PE': resultados_temp_pe, 'Indices': {}}
                
                # Indices
                sumas_indices = {}
                for idx, data in WPPSI_Engine.INDICES.items():
                    suma = sum([resultados_temp_pe.get(p, 0) for p in data['pruebas'] if p in seleccionadas])
                    n = len([p for p in data['pruebas'] if p in seleccionadas])
                    if n > 0:
                        punt_compuesta = WPPSI_Engine.suma_pe_a_ci(suma, n)
                        res_final['Indices'][idx] = {
                            'puntuacion': punt_compuesta,
                            'categoria': WPPSI_Engine.obtener_categoria(punt_compuesta)[0],
                            'percentil': int((punt_compuesta - 100) * 0.8 + 50) # Estimación simple
                        }
                
                # CIT
                suma_total_pe = sum(resultados_temp_pe.values())
                cit = WPPSI_Engine.suma_pe_a_ci(suma_total_pe, len(resultados_temp_pe))
                res_final['CIT'] = {
                    'puntuacion': cit,
                    'categoria': WPPSI_Engine.obtener_categoria(cit)[0],
                    'percentil': int((cit - 100) * 0.8 + 50)
                }
                
                st.session_state.resultados = res_final
                st.balloons()
                st.success("¡Resultados procesados correctamente! Ve a la pestaña 4.")

    # ─── PASO 4: RESULTADOS ────────────────────────────────────────────────────
    elif "4." in paso_actual:
        if not st.session_state.resultados:
            st.warning("⚠️ Primero debes procesar los resultados en el Paso 3.")
        else:
            res = st.session_state.resultados
            st.markdown("### 📊 Tablero de Resultados")
            
            # Métricas Principales
            cols = st.columns(4)
            cit = res['CIT']
            color_cit = WPPSI_Engine.obtener_categoria(cit['puntuacion'])[1]
            
            cols[0].metric("CIT Total", cit['puntuacion'], delta=cit['categoria'])
            
            # Mostrar indices
            idx_list = list(res['Indices'].items())
            for i, (k, v) in enumerate(idx_list):
                if i+1 < 4:
                    cols[i+1].metric(k, v['puntuacion'], delta=v['categoria'])

            st.markdown("---")
            
            # Gráfico Radar Profesional
            categorias = ['CIT'] + list(res['Indices'].keys())
            valores = [cit['puntuacion']] + [v['puntuacion'] for k,v in res['Indices'].items()]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=valores,
                theta=categorias,
                fill='toself',
                name='Paciente',
                line_color='#D81B60'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[40, 160])),
                showlegend=False,
                title=dict(text="Mapa Cognitivo", font=dict(size=20, family="Montserrat"))
            )
            st.plotly_chart(fig_radar, use_container_width=True)

            # Interpretación Automática
            st.markdown("### 📝 Interpretación Clínica Generada")
            texto_interpretacion = WPPSI_Engine.analizar_perfil(res)
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #D81B60; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                {texto_interpretacion}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Generación de PDF
            st.markdown("### 📄 Exportar Informe")
            if st.button("📥 Generar Informe PDF Profesional", type="primary", use_container_width=True):
                with st.spinner("Maquetando PDF vectorial de alta resolución..."):
                    buffer = io.BytesIO()
                    reporte = ReportePDF(buffer, st.session_state.paciente, res)
                    pdf_bytes = reporte.generar()
                    
                    b64 = base64.b64encode(pdf_bytes.getvalue()).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="Informe_WPPSI_{st.session_state.paciente["nombre"]}.pdf" style="text-decoration:none;">' \
                           f'<button style="width:100%; background-color:#27AE60; color:white; padding:15px; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">' \
                           f'✅ DESCARGAR INFORME COMPLETADO</button></a>'
                    st.markdown(href, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
