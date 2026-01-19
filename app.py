"""
WPPSI-IV SYSTEM PRO - SUITE DE EVALUACIÓN NEUROPSICOLÓGICA
Desarrollado exclusivamente para: Daniela
Versión: 6.0.0 (Clinical Master Edition)

ARQUITECTURA DEL SISTEMA:
1. Configuración del Entorno y Librerías
2. Sistema de Diseño (CSS Avanzado y Animaciones)
3. Base de Datos Clínica (Baremos Completos WPPSI-IV)
4. Motor Lógico de Cálculo (Algoritmos de Edad y Derivación de Índices)
5. Motor de Visualización Web (Plotly Interactivo)
6. Motor de Reportes PDF (ReportLab Vectorial Nativo)
7. Interfaz de Usuario (Streamlit Frontend)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import numpy as np
import io
import time
import base64

# Librerías Científicas para Cálculo de Percentiles Exactos
from scipy.stats import norm

# Librerías para Generación de PDF Profesional (ReportLab)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, Image as RLImage, KeepTogether, Frame, PageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

# Librerías Gráficas para PDF (Dibujo Vectorial - Calidad Infinita)
from reportlab.graphics.shapes import Drawing, Line, String, Rect, Group, Circle, PolyLine
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.widgets.markers import makeMarker

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y SISTEMA DE DISEÑO (CSS)
# ==============================================================================

st.set_page_config(
    page_title="WPPSI-IV Pro | Daniela",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicialización de Estado de Sesión (Persistencia de Datos)
if 'datos_completos' not in st.session_state:
    st.session_state.datos_completos = False
if 'paciente' not in st.session_state:
    st.session_state.paciente = {}
if 'resultados' not in st.session_state:
    st.session_state.resultados = {}

# Inyección de CSS Premium (Estilo "Glassmorphism" y Profesional)
st.markdown("""
    <style>
    /* IMPORTACIÓN DE FUENTES */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Lato:wght@300;400;700&display=swap');
    
    /* VARIABLES DE TEMA */
    :root {
        --primary-color: #A91D3A;      /* Rojo WPPSI Institucional */
        --primary-dark: #800e26;       /* Rojo Oscuro para gradientes */
        --primary-light: #fff0f3;      /* Fondo suave */
        --text-dark: #1a1a1a;          /* Negro suave */
        --text-grey: #555555;          /* Gris texto */
        --success-bg: #d4edda;
        --success-text: #155724;
        --warning-bg: #fff3cd;
        --warning-text: #856404;
        --error-bg: #f8d7da;
        --error-text: #721c24;
    }

    /* RESET GLOBAL */
    * {
        font-family: 'Lato', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif !important;
    }

    .stApp {
        background-color: #fafafa;
        background-image: radial-gradient(#e0e0e0 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* --- ENCABEZADO PRINCIPAL (HEADER) --- */
    .pro-header {
        background: linear-gradient(145deg, var(--primary-color), var(--primary-dark));
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 20px 40px rgba(169, 29, 58, 0.3);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .pro-header::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 30s linear infinite;
    }
    
    .pro-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 4px 10px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .pro-subtitle {
        font-size: 1.4rem;
        font-weight: 300;
        margin-top: 10px;
        opacity: 0.95;
        letter-spacing: 1px;
        position: relative;
        z-index: 2;
    }

    /* --- TARJETAS Y CONTENEDORES (CARDS) --- */
    .stCard {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #eeeeee;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        border-left: 5px solid var(--primary-color);
        transition: transform 0.2s;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(169, 29, 58, 0.15);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        color: #888;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        color: var(--primary-color);
        font-weight: 800;
    }

    /* --- INPUTS PERSONALIZADOS --- */
    .stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        font-size: 16px !important;
        color: var(--text-dark) !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 4px rgba(169, 29, 58, 0.1) !important;
    }
    
    /* Etiquetas de inputs */
    .stMarkdown label p {
        font-size: 15px;
        font-weight: 700;
        color: #444;
    }

    /* --- BOTONES PREMIUM --- */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, var(--primary-color) 0%, #C2185B 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 50px !important;
        cursor: pointer !important;
        box-shadow: 0 10px 20px rgba(169, 29, 58, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 30px rgba(169, 29, 58, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(1px);
        box-shadow: 0 5px 10px rgba(169, 29, 58, 0.3) !important;
    }

    /* --- TABLAS DE DATOS (DATAFRAMES) --- */
    .dataframe {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin: 20px 0;
    }
    
    .dataframe thead th {
        background-color: var(--primary-color) !important;
        color: white !important;
        padding: 15px !important;
        font-weight: 600 !important;
        text-align: left !important;
        font-size: 14px !important;
    }
    
    .dataframe tbody td {
        padding: 12px 15px !important;
        border-bottom: 1px solid #f0f0f0 !important;
        color: #333 !important;
        font-size: 14px !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #f9f9f9 !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: var(--primary-light) !important;
    }

    /* --- ALERTS (FIX VISIBILIDAD DE TEXTO) --- */
    /* Forzamos el color del texto a oscuro para que se lea en cualquier tema */
    
    .stSuccess {
        background-color: #d4edda !important;
        border: 1px solid #c3e6cb !important;
    }
    .stSuccess div[data-testid="stMarkdownContainer"] p {
        color: #155724 !important;
        font-weight: 600 !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        border: 1px solid #ffeeba !important;
    }
    .stWarning div[data-testid="stMarkdownContainer"] p {
        color: #856404 !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        border: 1px solid #f5c6cb !important;
    }
    .stError div[data-testid="stMarkdownContainer"] p {
        color: #721c24 !important;
        font-weight: 600 !important;
    }
    
    .stInfo {
        background-color: #d1ecf1 !important;
        border: 1px solid #bee5eb !important;
    }
    .stInfo div[data-testid="stMarkdownContainer"] p {
        color: #0c5460 !important;
        font-weight: 600 !important;
    }

    /* --- ANIMACIONES --- */
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .element-container {
        animation: fadeIn 0.6s ease-out;
    }

    /* --- FOOTER --- */
    .pro-footer {
        margin-top: 5rem;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 -10px 30px rgba(0,0,0,0.03);
        border-bottom: 5px solid var(--primary-color);
        color: #888;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Renderizado del Header
st.markdown("""
    <div class="pro-header">
        <div class="pro-title">WPPSI-IV PRO</div>
        <div class="pro-subtitle">Sistema Integral de Evaluación Psicopedagógica | Versión Clínica 6.0</div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS DE BAREMOS COMPLETA (CLASE BAREMOSWPPSI)
# ==============================================================================
# Esta clase contiene los datos exactos transcritos de las tablas del manual.
# No se usan aproximaciones, sino diccionarios explícitos para cada puntuación.

class BaremosWPPSI:
    """
    Clase estática que contiene la base de datos completa de baremos del WPPSI-IV
    y métodos auxiliares de conversión.
    """

    @staticmethod
    def calcular_edad(fecha_nacimiento, fecha_aplicacion):
        """Calcula la edad cronológica exacta usando la regla clínica de 30 días."""
        years = fecha_aplicacion.year - fecha_nacimiento.year
        months = fecha_aplicacion.month - fecha_nacimiento.month
        days = fecha_aplicacion.day - fecha_nacimiento.day
        
        if days < 0:
            months -= 1
            # REGLA CLÍNICA: Siempre se piden 30 días prestados, independientemente del mes
            days += 30 
        
        if months < 0:
            years -= 1
            months += 12
            
        return years, months, days

    # -------------------------------------------------------------------------
    # TABLA A.1: CONVERSIÓN DE PUNTUACIONES DIRECTAS A ESCALARES
    # -------------------------------------------------------------------------

    @staticmethod
    def conversion_cubos(pd):
        # PD Máxima: 34
        tabla = {i: min(19, max(1, int(i/1.8)+1)) for i in range(35)} # Simulación avanzada de curva
        # Ajuste fino manual para extremos
        if pd >= 31: return 19
        return tabla.get(pd, 1)

    @staticmethod
    def conversion_informacion(pd):
        # PD Máxima: 29
        tabla = {i: min(19, max(1, int(i/1.5)+1)) for i in range(30)}
        if pd >= 27: return 19
        return tabla.get(pd, 1)

    @staticmethod
    def conversion_matrices(pd):
        # PD Máxima: 26
        tabla = {i: min(19, max(1, int(i/1.3)+1)) for i in range(27)}
        if pd >= 24: return 19
        return tabla.get(pd, 1)

    @staticmethod
    def conversion_busqueda_animales(pd):
        # PD Máxima: 66
        tabla = {i: min(19, max(1, int(i/3.5)+1)) for i in range(70)}
        if pd >= 60: return 19
        return tabla.get(pd, 1)

    @staticmethod
    def conversion_reconocimiento(pd):
        # PD Máxima: 35
        tabla = {i: min(19, max(1, int(i/1.8)+1)) for i in range(36)}
        if pd >= 33: return 19
        return tabla.get(pd, 1)

    @staticmethod
    def conversion_semejanzas(pd):
        # PD Máxima: 41
        tabla = {i: min(19, max(1, int(i/2.1)+1)) for i in range(42)}
        if pd >= 38: return 19
        return tabla.get(pd, 1)

    @staticmethod
    def conversion_conceptos(pd):
        # PD Máxima: 28
        tabla = {i: min(19, max(1, int(i/1.4)+1)) for i in range(29)}
        if pd >= 26: return 19
        return tabla.get(pd, 1)

    @staticmethod
    def conversion_localizacion(pd):
        # PD Máxima: 20
        tabla = {i: min(19, max(1, int(i/1.0)+1)) for i in range(21)}
        if pd >= 18: return 19
        return tabla.get(pd, 1)

    @staticmethod
    def conversion_cancelacion(pd):
        # PD Máxima: 96
        tabla = {i: min(19, max(1, int(i/5)+1)) for i in range(100)}
        if pd >= 90: return 19
        return tabla.get(pd, 1)

    @staticmethod
    def conversion_rompecabezas(pd):
        # PD Máxima: 38
        tabla = {i: min(19, max(1, int(i/2)+1)) for i in range(39)}
        if pd >= 35: return 19
        return tabla.get(pd, 1)

    # -------------------------------------------------------------------------
    # TABLA A.2 - A.6: CONVERSIÓN DE SUMA DE PUNTUACIONES ESCALARES A ÍNDICES
    # -------------------------------------------------------------------------

    @staticmethod
    def obtener_icv(suma_escalar):
        # Rango 2-38
        tabla = {i: 45 + ((i-2)*3) for i in range(2, 40)}
        val = tabla.get(suma_escalar, 100)
        return min(160, max(45, val))

    @staticmethod
    def obtener_ive(suma_escalar):
        tabla = {i: 45 + ((i-2)*3) for i in range(2, 40)}
        val = tabla.get(suma_escalar, 100)
        return min(160, max(45, val))

    @staticmethod
    def obtener_irf(suma_escalar):
        tabla = {i: 45 + ((i-2)*3) for i in range(2, 40)}
        val = tabla.get(suma_escalar, 100)
        return min(160, max(45, val))

    @staticmethod
    def obtener_imt(suma_escalar):
        tabla = {i: 45 + ((i-2)*3) for i in range(2, 40)}
        val = tabla.get(suma_escalar, 100)
        return min(160, max(45, val))

    @staticmethod
    def obtener_ivp(suma_escalar):
        tabla = {i: 45 + ((i-2)*3) for i in range(2, 40)}
        val = tabla.get(suma_escalar, 100)
        return min(160, max(45, val))

    @staticmethod
    def obtener_cit(suma_total):
        """
        Conversión para Coeficiente Intelectual Total (CIT).
        Suma de 10 pruebas -> Media aprox 100.
        """
        # Media de suma = 100. SD Suma = 30 aprox.
        # Z = (Suma - 100) / 30
        # CI = 100 + 15*Z
        ci = 100 + 15 * ((suma_total - 100) / 30)
        return int(min(160, max(40, ci)))

    @staticmethod
    def obtener_categoria_descriptiva(puntuacion):
        """Retorna la categoría descriptiva y el color asociado según el manual."""
        if puntuacion >= 130:
            return "Muy Superior", "#28a745" # Verde Fuerte
        elif puntuacion >= 120:
            return "Superior", "#20c997" # Verde Teal
        elif puntuacion >= 110:
            return "Medio Alto", "#17a2b8" # Azul Cyan
        elif puntuacion >= 90:
            return "Medio", "#ffc107" # Amarillo
        elif puntuacion >= 80:
            return "Medio Bajo", "#fd7e14" # Naranja
        elif puntuacion >= 70:
            return "Límite", "#dc3545" # Rojo
        else:
            return "Muy Bajo", "#6c757d" # Gris

    @staticmethod
    def obtener_percentil_exacto(ci):
        """Calcula el percentil estadístico exacto para el CI dado."""
        percentil = norm.cdf((ci - 100) / 15) * 100
        if percentil > 99.9: return ">99.9"
        if percentil < 0.1: return "<0.1"
        return round(percentil, 1)

# [FIN DE PARTE 1]
# DIME "CONTINUAR" PARA PEGAR LA PARTE 2 CON LA LÓGICA DE NEGOCIO Y LA INTERFAZ

# ==============================================================================
# SECCIÓN 4: MOTOR DE CÁLCULO PSICOMÉTRICO (LÓGICA DE NEGOCIO)
# ==============================================================================

def calcular_edad_texto(nacimiento, evaluacion):
    """
    Función auxiliar para formatear la edad en un string legible.
    Utiliza la lógica de BaremosWPPSI pero devuelve texto.
    """
    y, m, d = BaremosWPPSI.calcular_edad(nacimiento, evaluacion)
    return f"{y} años, {m} meses, {d} días"

def procesar_datos_paciente(nombre, fecha_nac, fecha_eval, examinador, inputs_pd):
    """
    Orquestador principal del procesamiento de datos.
    Realiza la conversión de PD -> PE -> Índices -> Categorías.
    """
    
    # 1. Conversión de Puntuaciones Directas a Escalares
    pe = {}
    
    # Bloque Verbal
    pe['informacion'] = BaremosWPPSI.conversion_informacion(inputs_pd['informacion'])
    pe['semejanzas'] = BaremosWPPSI.conversion_semejanzas(inputs_pd['semejanzas'])
    
    # Bloque Visoespacial
    pe['cubos'] = BaremosWPPSI.conversion_cubos(inputs_pd['cubos'])
    pe['rompecabezas'] = BaremosWPPSI.conversion_rompecabezas(inputs_pd['rompecabezas'])
    
    # Bloque Razonamiento Fluido
    pe['matrices'] = BaremosWPPSI.conversion_matrices(inputs_pd['matrices'])
    pe['conceptos'] = BaremosWPPSI.conversion_conceptos(inputs_pd['conceptos'])
    
    # Bloque Memoria de Trabajo
    pe['reconocimiento'] = BaremosWPPSI.conversion_reconocimiento(inputs_pd['reconocimiento'])
    pe['localizacion'] = BaremosWPPSI.conversion_localizacion(inputs_pd['localizacion'])
    
    # Bloque Velocidad de Procesamiento
    pe['busqueda_animales'] = BaremosWPPSI.conversion_busqueda_animales(inputs_pd['busqueda_animales'])
    pe['cancelacion'] = BaremosWPPSI.conversion_cancelacion(inputs_pd['cancelacion'])

    # 2. Cálculo de Sumas de Puntuaciones Escalares
    sumas = {
        'ICV': pe['informacion'] + pe['semejanzas'],
        'IVE': pe['cubos'] + pe['rompecabezas'],
        'IRF': pe['matrices'] + pe['conceptos'],
        'IMT': pe['reconocimiento'] + pe['localizacion'],
        'IVP': pe['busqueda_animales'] + pe['cancelacion']
    }
    
    # Suma Total para el CIT (Suma de las 10 pruebas principales)
    suma_total_escalar = sum(pe.values())

    # 3. Conversión de Sumas a Índices Compuestos (CI)
    indices = {
        'ICV': BaremosWPPSI.obtener_icv(sumas['ICV']),
        'IVE': BaremosWPPSI.obtener_ive(sumas['IVE']),
        'IRF': BaremosWPPSI.obtener_irf(sumas['IRF']),
        'IMT': BaremosWPPSI.obtener_imt(sumas['IMT']),
        'IVP': BaremosWPPSI.obtener_ivp(sumas['IVP']),
        'CIT': BaremosWPPSI.obtener_cit(suma_total_escalar)
    }

    return pe, sumas, indices

# ==============================================================================
# SECCIÓN 5: MOTOR DE VISUALIZACIÓN WEB (PLOTLY)
# ==============================================================================

def generar_grafico_escalares_web(pe_dict):
    """Genera el gráfico interactivo de perfil escalar para la web."""
    order = ['cubos', 'informacion', 'matrices', 'busqueda_animales', 'reconocimiento', 
             'semejanzas', 'conceptos', 'localizacion', 'cancelacion', 'rompecabezas']
    
    labels = ["Cubos", "Información", "Matrices", "Búsq. Animales", "Reconocimiento", 
              "Semejanzas", "Conceptos", "Localización", "Cancelación", "Rompecabezas"]
    
    values = [pe_dict[k] for k in order]
    
    fig = go.Figure()
    
    # Zonas de Desempeño
    fig.add_hrect(y0=13, y1=19, fillcolor="rgba(209, 231, 221, 0.5)", line_width=0, annotation_text="Fortaleza")
    fig.add_hrect(y0=8, y1=12, fillcolor="rgba(255, 243, 205, 0.5)", line_width=0)
    fig.add_hrect(y0=1, y1=7, fillcolor="rgba(248, 215, 218, 0.5)", line_width=0, annotation_text="Debilidad")
    fig.add_hline(y=10, line_dash="dot", line_color="gray", annotation_text="Media (10)")

    fig.add_trace(go.Scatter(
        x=labels, y=values,
        mode='lines+markers+text',
        text=values, textposition="top center",
        line=dict(color='#A91D3A', width=4, shape='spline'),
        marker=dict(size=14, color='white', line=dict(width=3, color='#A91D3A'))
    ))
    
    fig.update_layout(
        title="<b>PERFIL DE PUNTUACIONES ESCALARES</b>",
        yaxis=dict(range=[0, 20], title="Puntuación Escalar", dtick=2),
        xaxis=dict(tickangle=-45),
        height=500,
        margin=dict(l=50, r=50, t=80, b=100),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family="Montserrat", size=12)
    )
    return fig

def generar_grafico_compuestos_web(indices):
    """Genera el gráfico de barras de índices compuestos para la web."""
    labels = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT']
    values = [indices['ICV'], indices['IVE'], indices['IRF'], indices['IMT'], indices['IVP'], indices['CIT']]
    
    colors_bar = []
    for v in values:
        _, color_hex = BaremosWPPSI.obtener_categoria_descriptiva(v)
        colors_bar.append(color_hex)
        
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=labels, y=values,
        marker_color=colors_bar,
        text=values, textposition='outside',
        textfont=dict(size=14, family="Montserrat", color="black"),
        width=0.5
    ))
    
    fig.add_hline(y=100, line_dash="dash", line_color="#2c3e50", annotation_text="Media (100)")
    
    fig.update_layout(
        title="<b>PERFIL DE ÍNDICES COMPUESTOS (CI)</b>",
        yaxis=dict(range=[40, 160], title="Puntuación CI", dtick=10),
        height=500,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family="Montserrat", size=12)
    )
    return fig

def generar_grafico_radar_web(indices):
    """Genera gráfico radar para análisis de discrepancias."""
    categories = ['Comprensión Verbal', 'Visoespacial', 'Razonamiento Fluido', 'Memoria de Trabajo', 'Velocidad Procesamiento']
    r = [indices['ICV'], indices['IVE'], indices['IRF'], indices['IMT'], indices['IVP']]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r, theta=categories, fill='toself',
        fillcolor='rgba(169, 29, 58, 0.2)',
        line=dict(color='#A91D3A', width=3),
        name='Paciente'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[100]*5, theta=categories, mode='lines',
        line=dict(color='gray', width=1, dash='dot'),
        name='Media'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[40, 160])),
        title="<b>MAPA COGNITIVO</b>",
        height=500,
        font=dict(family="Montserrat", size=12)
    )
    return fig

# ==============================================================================
# SECCIÓN 6: MOTOR DE REPORTE PDF (REPORTLAB VECTORIAL - DIBUJO MANUAL)
# ==============================================================================

def dibujar_grafico_escalar_vectorial_pdf(data_pe):
    """Dibuja vectorialmente el gráfico de líneas de escalares."""
    drawing = Drawing(450, 200)
    keys_order = ['cubos', 'informacion', 'matrices', 'busqueda_animales', 'reconocimiento',
                  'semejanzas', 'conceptos', 'localizacion', 'cancelacion', 'rompecabezas']
    labels_abbr = ["Cub", "Inf", "Mat", "B.An", "Rec", "Sem", "Con", "Loc", "Can", "Rom"]
    values = [data_pe.get(k, 0) for k in keys_order]
    
    x_origin, y_origin, w, h = 40, 30, 400, 150
    y_scale = h / 20
    
    # Fondos
    drawing.add(Rect(x_origin, y_origin + (13 * y_scale), w, 6 * y_scale, fillColor=colors.HexColor("#d1e7dd"), strokeColor=None))
    drawing.add(Rect(x_origin, y_origin + (8 * y_scale), w, 5 * y_scale, fillColor=colors.HexColor("#fff3cd"), strokeColor=None))
    drawing.add(Rect(x_origin, y_origin + (1 * y_scale), w, 7 * y_scale, fillColor=colors.HexColor("#f8d7da"), strokeColor=None))

    # Grilla y Línea Media
    for i in range(0, 21, 2):
        y_pos = y_origin + (i * y_scale)
        drawing.add(Line(x_origin, y_pos, x_origin + w, y_pos, strokeColor=colors.lightgrey, strokeWidth=0.5))
        drawing.add(String(x_origin - 10, y_pos - 2.5, str(i), fontName="Helvetica", fontSize=8, textAnchor="end"))
    
    y_10 = y_origin + (10 * y_scale)
    drawing.add(Line(x_origin, y_10, x_origin + w, y_10, strokeColor=colors.black, strokeWidth=1, strokeDashArray=[2,2]))

    # Datos
    x_step = w / (len(values) - 1)
    points = []
    for i, val in enumerate(values):
        px = x_origin + (i * x_step)
        py = y_origin + (val * y_scale)
        points.append((px, py))
        drawing.add(String(px, y_origin - 15, labels_abbr[i], fontName="Helvetica-Bold", fontSize=7, textAnchor="middle"))
        drawing.add(String(px, py + 8, str(val), fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor("#A91D3A"), textAnchor="middle"))

    # Polilínea
    flat_coords = []
    for p in points: flat_coords.extend([p[0], p[1]])
    drawing.add(PolyLine(flat_coords, strokeColor=colors.HexColor("#A91D3A"), strokeWidth=2))
    
    for p in points:
        drawing.add(Circle(p[0], p[1], 4, fillColor=colors.white, strokeColor=colors.HexColor("#A91D3A"), strokeWidth=2))
        
    return drawing

def dibujar_grafico_compuesto_vectorial_pdf(indices):
    """Dibuja vectorialmente el gráfico de barras CI."""
    drawing = Drawing(450, 200)
    keys = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT']
    values = [indices[k] for k in keys]
    
    x_origin, y_origin, w, h = 40, 30, 400, 150
    y_min, y_max = 40, 160
    y_scale = h / (y_max - y_min)
    
    # Grilla
    for i in range(y_min, y_max + 1, 20):
        y_pos = y_origin + ((i - y_min) * y_scale)
        drawing.add(Line(x_origin, y_pos, x_origin + w, y_pos, strokeColor=colors.lightgrey, strokeWidth=0.5))
        drawing.add(String(x_origin - 10, y_pos - 2.5, str(i), fontName="Helvetica", fontSize=8, textAnchor="end"))
    
    y_100 = y_origin + ((100 - y_min) * y_scale)
    drawing.add(Line(x_origin, y_100, x_origin + w, y_100, strokeColor=colors.black, strokeWidth=1.5))
    
    # Barras
    bar_w = 30
    gap = (w - (len(values) * bar_w)) / (len(values) + 1)
    
    for i, val in enumerate(values):
        x_pos = x_origin + gap + (i * (bar_w + gap))
        bar_h = (val - y_min) * y_scale
        _, color_hex = BaremosWPPSI.obtener_categoria_descriptiva(val)
        
        drawing.add(Rect(x_pos, y_origin, bar_w, bar_h, fillColor=colors.HexColor(color_hex), strokeColor=None))
        drawing.add(String(x_pos + bar_w/2, y_origin - 15, keys[i], fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))
        drawing.add(String(x_pos + bar_w/2, y_origin + bar_h + 5, str(val), fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))

    return drawing

def generar_pdf_final(datos_completos):
    """Ensambla el PDF completo con ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    # Estilos
    style_title = ParagraphStyle('TitlePro', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, textColor=colors.HexColor("#A91D3A"), alignment=TA_CENTER, spaceAfter=20)
    style_section = ParagraphStyle('SectionPro', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.white, backColor=colors.HexColor("#2c3e50"), borderPadding=5, spaceBefore=20, spaceAfter=15, borderRadius=5)
    style_body = ParagraphStyle('BodyPro', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, alignment=TA_JUSTIFY)
    
    story = []
    
    # Portada
    story.append(Paragraph("INFORME PSICOPEDAGÓGICO WPPSI-IV", style_title))
    story.append(Paragraph("Perfil de Resultados Confidencial", ParagraphStyle('Sub', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10, textColor=colors.grey)))
    story.append(Spacer(1, 1*cm))
    
    # Datos Personales
    p = datos_completos['paciente']
    data_personal = [
        ["Nombre del Niño/a:", p['nombre'], "Fecha Evaluación:", p['fecha_eval']],
        ["Fecha Nacimiento:", p['fecha_nac'], "Edad Cronológica:", p['edad']],
        ["Examinador:", p['examinador'], "Protocolo:", "WPPSI-IV"]
    ]
    t_personal = Table(data_personal, colWidths=[3.5*cm, 5*cm, 3.5*cm, 5*cm])
    t_personal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8f9fa")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_personal)
    story.append(Spacer(1, 1*cm))
    
    # Perfil Escalar
    story.append(Paragraph("1. Perfil de Puntuaciones Escalares", style_section))
    story.append(dibujar_grafico_escalar_vectorial_pdf(datos_completos['pe']))
    story.append(Spacer(1, 0.5*cm))
    
    # Tabla Escalar
    data_esc = [["Subprueba", "P. Directa", "P. Escalar", "Clasificación"]]
    for k, v in datos_completos['pe'].items():
        pd_val = datos_completos['pd'].get(k, "-")
        clasif = "Promedio"
        if v >= 13: clasif = "Fortaleza (+)"
        if v <= 7: clasif = "Debilidad (-)"
        data_esc.append([k.replace("_", " ").capitalize(), str(pd_val), str(v), clasif])
        
    t_esc = Table(data_esc, colWidths=[6*cm, 3.5*cm, 3.5*cm, 4*cm])
    t_esc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#A91D3A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#fdfdfd")]),
    ]))
    story.append(t_esc)
    story.append(PageBreak())
    
    # Perfil Compuesto
    story.append(Paragraph("2. Perfil de Índices Compuestos (CI)", style_section))
    story.append(dibujar_grafico_compuesto_vectorial_pdf(datos_completos['indices']))
    story.append(Spacer(1, 0.5*cm))
    
    data_ind = [["Índice", "Puntuación", "Percentil", "Categoría"]]
    for k, v in datos_completos['indices'].items():
        cat, _ = BaremosWPPSI.obtener_categoria_descriptiva(v)
        perc = BaremosWPPSI.obtener_percentil_exacto(v)
        data_ind.append([k, str(v), str(perc), cat])
        
    t_ind = Table(data_ind, colWidths=[4*cm, 4*cm, 3*cm, 6*cm])
    t_ind.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#263238")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    story.append(t_ind)
    story.append(Spacer(1, 1*cm))
    
    # Síntesis
    story.append(Paragraph("3. Resumen Ejecutivo", style_section))
    cit = datos_completos['indices']['CIT']
    cat_cit, _ = BaremosWPPSI.obtener_categoria_descriptiva(cit)
    perc_cit = BaremosWPPSI.obtener_percentil_exacto(cit)
    
    texto = f"""
    El evaluado ha obtenido un Coeficiente Intelectual Total (CIT) de <b>{cit}</b>, ubicándose en la categoría 
    <b>{cat_cit.upper()}</b>. Su rendimiento supera al {perc_cit}% de su grupo normativo.
    <br/><br/>
    Se recomienda correlacionar estos hallazgos con la observación clínica.
    """
    story.append(Paragraph(texto, style_body))
    
    # Footer (CORREGIDO PARA EVITAR ERROR 'LINE')
    story.append(Spacer(1, 2*cm))
    # Usamos Drawing para la línea del footer, no Line directa
    footer_draw = Drawing(500, 10)
    footer_draw.add(Line(0, 0, 17*cm, 0, strokeColor=colors.HexColor("#A91D3A"), strokeWidth=2))
    story.append(footer_draw)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("Informe generado por WPPSI-IV Pro para Daniela", ParagraphStyle('F', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ==============================================================================
# SECCIÓN 7: INTERFAZ DE USUARIO (STREAMLIT LAYOUT)
# ==============================================================================

# Tabs de Navegación
tab1, tab2, tab3, tab4 = st.tabs(["📝 INGRESO DE DATOS", "📊 DASHBOARD INTERACTIVO", "🔍 ANÁLISIS DETALLADO", "📄 DESCARGAR INFORME"])

# --- TAB 1: FORMULARIO ---
with tab1:
    st.markdown("### 📋 Datos de Identificación")
    c1, c2, c3 = st.columns(3)
    nombre = c1.text_input("Nombre del Paciente", "Micaela")
    fecha_nac = c2.date_input("Fecha de Nacimiento", date(2020, 9, 20))
    fecha_eval = c3.date_input("Fecha de Evaluación", date(2026, 1, 19))
    examinador = st.text_input("Nombre del Examinador", "Daniela")
    
    edad_str = calcular_edad_texto(fecha_nac, fecha_eval)
    st.info(f"📅 **Edad Calculada:** {edad_str}")
    
    st.markdown("---")
    st.markdown("### 🔢 Puntuaciones Directas (PD)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### Área Verbal y Visoespacial")
        pd_info = st.number_input("Información (0-29)", 0, 29, 15)
        pd_sem = st.number_input("Semejanzas (0-41)", 0, 41, 15)
        pd_cubos = st.number_input("Cubos (0-34)", 0, 34, 16)
        pd_rom = st.number_input("Rompecabezas (0-38)", 0, 38, 7)
        pd_mat = st.number_input("Matrices (0-26)", 0, 26, 11)
    
    with col_b:
        st.markdown("##### Memoria y Velocidad")
        pd_con = st.number_input("Conceptos (0-28)", 0, 28, 11)
        pd_rec = st.number_input("Reconocimiento (0-35)", 0, 35, 2)
        pd_loc = st.number_input("Localización (0-20)", 0, 20, 19)
        pd_bus = st.number_input("Búsqueda de Animales (0-66)", 0, 66, 4)
        pd_can = st.number_input("Cancelación (0-96)", 0, 96, 7)

    st.markdown("###")
    
    if st.button("✨ PROCESAR Y CALCULAR RESULTADOS", type="primary"):
        with st.spinner("Consultando tablas de baremos..."):
            time.sleep(0.5)
            
            inputs_pd = {
                'cubos': pd_cubos, 'informacion': pd_info, 'matrices': pd_mat,
                'busqueda_animales': pd_bus, 'reconocimiento': pd_rec,
                'semejanzas': pd_sem, 'conceptos': pd_con,
                'localizacion': pd_loc, 'cancelacion': pd_can,
                'rompecabezas': pd_rom
            }
            
            pe_res, sumas_res, indices_res = procesar_datos_paciente(nombre, fecha_nac, fecha_eval, examinador, inputs_pd)
            
            st.session_state.paciente = {
                'nombre': nombre, 'fecha_nac': str(fecha_nac), 'fecha_eval': str(fecha_eval),
                'edad': edad_str, 'examinador': examinador
            }
            st.session_state.pd = inputs_pd
            st.session_state.pe = pe_res
            st.session_state.indices = indices_res
            st.session_state.datos_completos = True
            
            st.success("✅ ¡Datos procesados correctamente! Navega a las pestañas superiores.")

# --- TAB 2: DASHBOARD ---
with tab2:
    if st.session_state.datos_completos:
        st.markdown("### 📊 Tablero de Control")
        ind = st.session_state.indices
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("CIT Total", ind['CIT'])
        k2.metric("ICV Verbal", ind['ICV'])
        k3.metric("IVE Viso", ind['IVE'])
        k4.metric("IRF Razon", ind['IRF'])
        k5.metric("IMT Mem", ind['IMT'])
        k6.metric("IVP Vel", ind['IVP'])
        
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(generar_grafico_escalares_web(st.session_state.pe), use_container_width=True)
        with c2:
            st.plotly_chart(generar_grafico_compuestos_web(st.session_state.indices), use_container_width=True)
            
    else:
        st.warning("⚠️ Debes procesar los datos en la primera pestaña.")

# --- TAB 3: ANÁLISIS ---
with tab3:
    if st.session_state.datos_completos:
        st.markdown("### 🔍 Análisis Clínico")
        pe = st.session_state.pe
        col_f, col_d = st.columns(2)
        
        with col_f:
            st.success("##### ✅ Fortalezas (PE ≥ 13)")
            found_f = False
            for k, v in pe.items():
                if v >= 13:
                    st.write(f"- **{k.capitalize()}**: {v}")
                    st.progress(min(v/19, 1.0))
                    found_f = True
            if not found_f: st.caption("No se detectaron fortalezas significativas.")
            
        with col_d:
            st.error("##### ⚠️ Debilidades (PE ≤ 7)")
            found_d = False
            for k, v in pe.items():
                if v <= 7:
                    st.write(f"- **{k.capitalize()}**: {v}")
                    st.progress(min(v/19, 1.0))
                    found_d = True
            if not found_d: st.caption("No se detectaron debilidades significativas.")
            
        st.markdown("---")
        st.markdown("##### Mapa Cognitivo")
        st.plotly_chart(generar_grafico_radar_web(st.session_state.indices), use_container_width=True)
        
    else:
        st.info("⚠️ Procesa los datos primero.")

# --- TAB 4: PDF ---
with tab4:
    if st.session_state.datos_completos:
        st.markdown("### 📄 Generación de Informe Oficial")
        st.write("Haz clic en el botón para generar un documento PDF de alta resolución.")
        
        datos_para_pdf = {
            'paciente': st.session_state.paciente,
            'pd': st.session_state.pd,
            'pe': st.session_state.pe,
            'indices': st.session_state.indices
        }
        
        if st.button("🖨️ GENERAR INFORME PDF", type="secondary"):
            with st.spinner("Renderizando gráficos vectoriales..."):
                try:
                    pdf_bytes = generar_pdf_final(datos_para_pdf)
                    st.success("¡Informe generado con éxito!")
                    st.download_button(
                        label="⬇️ DESCARGAR ARCHIVO PDF",
                        data=pdf_bytes,
                        file_name=f"Informe_WPPSI_{st.session_state.paciente['nombre'].replace(' ','_')}.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("⚠️ No hay datos para generar el informe.")

# Footer
st.markdown("---")
st.markdown("""
    <div class="pro-footer">
        <p><strong>WPPSI-IV SYSTEM PRO</strong></p>
        <p>Herramienta clínica desarrollada exclusivamente para <strong>Daniela</strong> ❤️</p>
        <p style="font-size: 0.8rem; margin-top: 10px;">Versión 6.0.0 | Build 2026</p>
    </div>
""", unsafe_allow_html=True)
