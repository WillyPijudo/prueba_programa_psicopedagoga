"""
WPPSI-IV - Generador de Informes Psicopedagógicos
Desarrollado especialmente para Daniela
Sistema completo de evaluación y generación de informes profesionales
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, 
                                Spacer, PageBreak, Image, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import io
import numpy as np

# ==================== CONFIGURACIÓN DE LA PÁGINA ====================
st.set_page_config(
    page_title="WPPSI-IV - Sistema de Informes",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS CSS PROFESIONALES ====================
st.markdown("""
    <style>
    /* Importar fuente profesional */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Configuración global */
    * {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Fondo de la aplicación */
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa, #e9ecef);
    }
    
    /* Títulos con excelente contraste */
    h1 {
        color: #212529 !important;
        font-weight: 700 !important;
        text-align: center;
        background: linear-gradient(135deg, #8B1538 0%, #a91d3a 100%);
        color: white !important;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(139, 21, 56, 0.3);
        margin-bottom: 2rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    h2 {
        color: #212529 !important;
        font-weight: 600 !important;
        border-left: 5px solid #8B1538;
        padding-left: 15px;
        margin-top: 2rem;
        margin-bottom: 1rem;
        animation: fadeInLeft 0.6s ease-out;
    }
    
    h3 {
        color: #343a40 !important;
        font-weight: 500 !important;
        margin-top: 1.5rem;
        animation: fadeIn 0.5s ease-out;
    }
    
    h4 {
        color: #495057 !important;
        font-weight: 500 !important;
    }
    
    /* Inputs con EXCELENTE contraste */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #ced4da !important;
        border-radius: 8px !important;
        padding: 0.6rem !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #8B1538 !important;
        box-shadow: 0 0 0 3px rgba(139, 21, 56, 0.15) !important;
    }
    
    /* Labels ULTRA legibles */
    label {
        color: #212529 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Botones profesionales */
    .stButton > button {
        background: linear-gradient(135deg, #8B1538 0%, #a91d3a 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 10px !important;
        font-size: 17px !important;
        width: 100%;
        box-shadow: 0 4px 12px rgba(139, 21, 56, 0.3) !important;
        transition: all 0.3s ease !important;
        animation: pulse 2s infinite;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #a91d3a 0%, #8B1538 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 21, 56, 0.4) !important;
    }
    
    /* Métricas profesionales */
    [data-testid="stMetricValue"] {
        color: #212529 !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #495057 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #8B1538 !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 5px solid #8B1538;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    
    /* Alertas y mensajes */
    .stSuccess {
        background-color: #d4edda !important;
        color: #155724 !important;
        border-left: 5px solid #28a745 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        animation: slideInRight 0.5s ease-out;
    }
    
    .stError {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border-left: 5px solid #dc3545 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        animation: shake 0.5s ease-out;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        color: #856404 !important;
        border-left: 5px solid #ffc107 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    
    .stInfo {
        background-color: #d1ecf1 !important;
        color: #0c5460 !important;
        border-left: 5px solid #17a2b8 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* DataFrames profesionales */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        animation: fadeIn 0.6s ease-out;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #8B1538 0%, #a91d3a 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 14px !important;
        font-size: 15px !important;
        text-align: center !important;
    }
    
    .dataframe td {
        padding: 12px !important;
        color: #212529 !important;
        background: #ffffff !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        text-align: center !important;
        border-bottom: 1px solid #dee2e6 !important;
    }
    
    .dataframe tr:hover td {
        background: #f8f9fa !important;
    }
    
    /* Separadores elegantes */
    hr {
        margin: 2rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #8B1538, transparent);
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Tabs profesionales */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        color: #495057;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B1538 0%, #a91d3a 100%);
        color: white;
    }
    
    /* Animaciones suaves */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(100px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #8B1538;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a91d3a;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        margin-top: 3rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== TABLAS DE CONVERSIÓN COMPLETAS ====================
# Estas tablas convierten Puntuaciones Directas (PD) a Puntuaciones Escalares (PE)
# Basadas en el manual WPPSI-IV para edades 4:0 a 7:7

TABLAS_CONVERSION = {
    'cubos': {
        0:1, 1:1, 2:1, 3:1, 4:1, 5:2, 6:3, 7:4, 8:5, 9:6, 10:7, 11:10, 12:11, 
        13:12, 14:13, 15:14, 16:15, 17:16, 18:16, 19:17, 20:17, 21:18, 22:18, 
        23:19, 24:19, 25:19, 26:19, 27:19, 28:19, 29:19, 30:19
    },
    'informacion': {
        0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 
        13:11, 14:12, 15:13, 16:15, 17:16, 18:17, 19:18, 20:18, 21:19, 22:19, 
        23:19, 24:19, 25:19, 26:19
    },
    'matrices': {
        0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:9, 10:10, 11:11, 12:12, 
        13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19
    },
    'busqueda_animales': {
        0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 
        13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:17, 20:18, 21:19
    },
    'reconocimiento': {
        0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:8, 9:10, 10:11, 11:13, 12:14, 
        13:16, 14:17, 15:18, 16:19
    },
    'semejanzas': {
        0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 
        13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:16, 20:17, 21:17, 22:18, 
        23:18, 24:19, 25:19, 26:19, 27:19, 28:19, 29:19
    },
    'conceptos': {
        0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 
        13:12, 14:13, 15:14, 16:15, 17:17, 18:18, 19:19
    },
    'localizacion': {
        0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:7, 8:8, 9:9, 10:11, 11:12, 12:13, 
        13:14, 14:15, 15:16, 16:17, 17:18, 18:19, 19:19, 20:19
    },
    'cancelacion': {
        0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 
        13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19, 21:19
    },
    'rompecabezas': {
        0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 
        13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19
    }
}

# Tablas de conversión de Suma de PE a Puntuaciones Compuestas
TABLA_ICV = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:130, 28:137, 30:145}
TABLA_IVE = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:129, 28:136, 30:143, 32:150}
TABLA_IRF = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:130, 28:136, 30:143}
TABLA_IMT = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:95, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138, 30:145}
TABLA_IVP = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138}
TABLA_CIT = {10:40, 15:45, 20:52, 25:58, 30:64, 35:70, 40:76, 45:82, 50:88, 55:94, 60:100, 63:103, 65:106, 70:112, 75:118, 80:124, 85:130, 90:136}

# Tabla de Percentiles
TABLA_PERCENTILES = {
    40: 0.1, 45: 0.1, 50: 0.1, 55: 0.1, 60: 0.4, 65: 1, 70: 2, 75: 5,
    80: 9, 85: 16, 90: 25, 95: 37, 100: 50, 103: 58, 105: 63, 106: 66,
    109: 73, 110: 75, 115: 84, 120: 91, 125: 95, 128: 97, 130: 98,
    135: 99, 140: 99.6, 145: 99.9, 150: 99.9
}

# ==================== FUNCIONES AUXILIARES ====================

def calcular_edad(fecha_nacimiento, fecha_aplicacion):
    """
    Calcula la edad cronológica exacta en años, meses y días
    Args:
        fecha_nacimiento: fecha de nacimiento del niño
        fecha_aplicacion: fecha de aplicación de la prueba
    Returns:
        tuple: (años, meses, días)
    """
    years = fecha_aplicacion.year - fecha_nacimiento.year
    months = fecha_aplicacion.month - fecha_nacimiento.month
    days = fecha_aplicacion.day - fecha_nacimiento.day
    
    if days < 0:
        months -= 1
        days += 30  # Aproximación de días en un mes
    
    if months < 0:
        years -= 1
        months += 12
    
    return years, months, days

def convertir_pd_a_pe(prueba, pd):
    """
    Convierte una Puntuación Directa (PD) a Puntuación Escalar (PE)
    Args:
        prueba: nombre de la prueba
        pd: puntuación directa
    Returns:
        int: puntuación escalar o None si no existe
    """
    if pd is None or pd == '':
        return None
    
    try:
        pd_int = int(pd)
        return TABLAS_CONVERSION.get(prueba, {}).get(pd_int, None)
    except:
        return None

def buscar_en_tabla(tabla, suma):
    """
    Busca el valor correspondiente en una tabla de conversión
    Args:
        tabla: diccionario con tabla de conversión
        suma: suma de puntuaciones escalares
    Returns:
        int: puntuación compuesta correspondiente
    """
    keys = sorted(tabla.keys())
    for key in keys:
        if suma <= key:
            return tabla[key]
    return tabla[keys[-1]]

def calcular_indices(pe_dict):
    """
    Calcula todos los índices compuestos a partir de las puntuaciones escalares
    Args:
        pe_dict: diccionario con puntuaciones escalares
    Returns:
        dict: diccionario con todos los índices calculados
    """
    # Obtener valores con manejo seguro de None
    def get_pe(key):
        val = pe_dict.get(key, 0)
        return val if val is not None else 0
    
    # Calcular sumas de PE
    suma_icv = get_pe('informacion') + get_pe('semejanzas')
    suma_ive = get_pe('cubos') + get_pe('rompecabezas')
    suma_irf = get_pe('matrices') + get_pe('conceptos')
    suma_imt = get_pe('reconocimiento') + get_pe('localizacion')
    suma_ivp = get_pe('busqueda_animales') + get_pe('cancelacion')
    suma_cit = suma_icv + suma_ive + suma_irf + suma_imt + suma_ivp
    
    return {
        'ICV': buscar_en_tabla(TABLA_ICV, suma_icv),
        'IVE': buscar_en_tabla(TABLA_IVE, suma_ive),
        'IRF': buscar_en_tabla(TABLA_IRF, suma_irf),
        'IMT': buscar_en_tabla(TABLA_IMT, suma_imt),
        'IVP': buscar_en_tabla(TABLA_IVP, suma_ivp),
        'CIT': buscar_en_tabla(TABLA_CIT, suma_cit),
        'suma_icv': suma_icv,
        'suma_ive': suma_ive,
        'suma_irf': suma_irf,
        'suma_imt': suma_imt,
        'suma_ivp': suma_ivp,
        'suma_cit': suma_cit
    }

def obtener_percentil(puntuacion):
    """
    Obtiene el percentil correspondiente a una puntuación compuesta
    Args:
        puntuacion: puntuación compuesta
    Returns:
        float: percentil correspondiente
    """
    # Buscar el percentil más cercano
    if puntuacion in TABLA_PERCENTILES:
        return TABLA_PERCENTILES[puntuacion]
    
    # Interpolar si no existe valor exacto
    keys = sorted(TABLA_PERCENTILES.keys())
    for i in range(len(keys) - 1):
        if keys[i] <= puntuacion < keys[i + 1]:
            return TABLA_PERCENTILES[keys[i]]
    
    return 50  # Valor por defecto

def obtener_categoria(puntuacion):
    """
    Determina la categoría descriptiva de una puntuación
    Args:
        puntuacion: puntuación compuesta
    Returns:
        dict: diccionario con categoría, nivel y color
    """
    if puntuacion >= 130:
        return {
            'categoria': 'Muy superior',
            'nivel': 'Punto fuerte normativo',
            'color': '#2E7D32',
            'descripcion': 'Rendimiento excepcional'
        }
    elif puntuacion >= 120:
        return {
            'categoria': 'Superior',
            'nivel': 'Dentro de límites',
            'color': '#66BB6A',
            'descripcion': 'Rendimiento sobresaliente'
        }
    elif puntuacion >= 110:
        return {
            'categoria': 'Medio alto',
            'nivel': 'Dentro de límites',
            'color': '#81C784',
            'descripcion': 'Rendimiento por encima del promedio'
        }
    elif puntuacion >= 90:
        return {
            'categoria': 'Medio',
            'nivel': 'Promedio',
            'color': '#FDD835',
            'descripcion': 'Rendimiento promedio esperado'
        }
    elif puntuacion >= 80:
        return {
            'categoria': 'Medio bajo',
            'nivel': 'Promedio',
            'color': '#FFB74D',
            'descripcion': 'Rendimiento ligeramente por debajo del promedio'
        }
    elif puntuacion >= 70:
        return {
            'categoria': 'Límite',
            'nivel': 'Punto débil normativo',
            'color': '#FF8A65',
            'descripcion': 'Requiere atención y seguimiento'
        }
    else:
        return {
            'categoria': 'Muy bajo',
            'nivel': 'Punto débil normativo',
            'color': '#E53935',
            'descripcion': 'Requiere intervención especializada'
        }

# ==================== FUNCIONES DE GRÁFICOS ====================

def crear_grafico_perfil_escalares(pe_dict):
    """
    Crea el gráfico de perfil de puntuaciones escalares estilo WPPSI-IV
    Similar al gráfico de la página 2 del cuadernillo
    """
    pruebas = [
        'Cubos', 'Información', 'Matrices', 'Búsqueda\nAnimales', 'Reconocimiento',
        'Semejanzas', 'Conceptos', 'Localización', 'Cancelación', 'Rompecabezas'
    ]
    
    keys = [
        'cubos', 'informacion', 'matrices', 'busqueda_animales', 'reconocimiento',
        'semejanzas', 'conceptos', 'localizacion', 'cancelacion', 'rompecabezas'
    ]
    
    # Obtener valores con validación
    valores = []
    for k in keys:
        val = pe_dict.get(k)
        if val is not None:
            valores.append(val)
        else:
            valores.append(10)  # Valor por defecto (media)
    
    fig = go.Figure()
    
    # Línea conectando puntos
    fig.add_trace(go.Scatter(
        x=list(range(len(pruebas))),
        y=valores,
        mode='lines+markers',
        line=dict(color='#8B1538', width=4),
        marker=dict(
            size=14,
            color='#8B1538',
            symbol='circle',
            line=dict(color='white', width=3)
        ),
        name='Puntuaciones Escalares',
        hovertemplate='<b>%{text}</b><br>PE: %{y}<extra></extra>',
        text=pruebas
    ))
    
    # Zonas sombreadas
    fig.add_hrect(y0=13, y1=19, fillcolor='rgba(46, 125, 50, 0.15)', 
                 line_width=0, annotation_text="Fortaleza", annotation_position="right")
    fig.add_hrect(y0=7, y1=13, fillcolor='rgba(253, 216, 53, 0.15)', 
                 line_width=0, annotation_text="Promedio", annotation_position="right")
    fig.add_hrect(y0=1, y1=7, fillcolor='rgba(229, 57, 53, 0.15)', 
                 line_width=0, annotation_text="Debilidad", annotation_position="right")
    
    # Líneas de referencia
    fig.add_hline(y=10, line_dash="dash", line_color="gray", line_width=2,
                 annotation_text="Media (10)", annotation_position="left")
    fig.add_hline(y=13, line_dash="dot", line_color='#2E7D32', line_width=1.5)
    fig.add_hline(y=7, line_dash="dot", line_color='#E53935', line_width=1.5)
    
    fig.update_layout(
        title={
            'text': '<b>Perfil de Puntuaciones Escalares</b>',
            'font': {'size': 22, 'color': '#212529', 'family': 'Roboto'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(pruebas))),
            ticktext=pruebas,
            tickangle=-45,
            tickfont=dict(size=12, color='#212529'),
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)'
        ),
        yaxis=dict(
            range=[0, 20],
            dtick=1,
            title='Puntuación Escalar (PE)',
            titlefont=dict(size=14, color='#212529'),
            tickfont=dict(size=12, color='#212529'),
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)'
        ),
        height=550,
        template='plotly_white',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=60, r=60, t=80, b=100)
    )
    
    return fig

def crear_grafico_perfil_compuestas(indices):
    """
    Crea el gráfico de perfil de puntuaciones compuestas
    Similar al gráfico de barras verticales del cuadernillo
    """
    nombres = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT']
    valores = [
        indices.get('ICV', 100),
        indices.get('IVE', 100),
        indices.get('IRF', 100),
        indices.get('IMT', 100),
        indices.get('IVP', 100),
        indices.get('CIT', 100)
    ]
    
    # Asignar colores según categoría
    colores = []
    for v in valores:
        cat = obtener_categoria(v)
        colores.append(cat['color'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=nombres,
        y=valores,
        marker=dict(
            color=colores,
            line=dict(color='#212529', width=2.5)
        ),
        text=valores,
        textposition='outside',
        textfont=dict(size=16, color='#212529', family='Roboto', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Puntuación: %{y}<br>Percentil: %{customdata}<extra></extra>',
        customdata=[obtener_percentil(v) for v in valores]
    ))
    
    # Zonas de clasificación
    zonas = [
        (130, 160, 'rgba(46, 125, 50, 0.1)', 'Muy Superior'),
        (120, 130, 'rgba(102, 187, 106, 0.1)', 'Superior'),
        (110, 120, 'rgba(129, 199, 132, 0.1)', 'Medio Alto'),
        (90, 110, 'rgba(253, 216, 53, 0.1)', 'Medio'),
        (80, 90, 'rgba(255, 183, 77, 0.1)', 'Medio Bajo'),
        (70, 80, 'rgba(255, 138, 101, 0.1)', 'Límite')
    ]
    
    for y0, y1, color, nombre in zonas:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=color, line_width=0)
    
    # Línea de la media
    fig.add_hline(y=100, line_dash="dash", line_color="#212529", line_width=3,
                 annotation_text="Media (100)", annotation_position="left",
                 annotation_font=dict(size=12, color='#212529'))
    
    fig.update_layout(
        title={
            'text': '<b>Perfil de Puntuaciones Compuestas</b>',
            'font': {'size': 22, 'color': '#212529', 'family': 'Roboto'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            title='Índices WPPSI-IV',
            titlefont=dict(size=14, color='#212529'),
            tickfont=dict(size=13, color='#212529')
        ),
        yaxis=dict(
            range=[40, 160],
            dtick=10,
            title='Puntuación Compuesta',
            titlefont=dict(size=14, color='#212529'),
            tickfont=dict(size=12, color='#212529'),
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)'
        ),
        height=550,
        template='plotly_white',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=60, r=60, t=80, b=80)
    )
    
    return fig

def crear_curva_normal(cit_value):
    """
    Crea la curva normal de clasificación (Imagen 1 del cuadernillo)
    """
    x = np.linspace(40, 160, 300)
    y = np.exp(-0.5 * ((x - 100) / 15) ** 2)
    
    fig = go.Figure()
    
    # Curva normal
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        fill='tozeroy',
        fillcolor='rgba(139, 21, 56, 0.25)',
        line=dict(color='#8B1538', width=3),
        name='Distribución Normal',
        hovertemplate='Puntuación: %{x}<extra></extra>'
    ))
    
    # Marcador de posición del CIT
    y_pos = np.exp(-0.5 * ((cit_value - 100) / 15) ** 2)
    fig.add_trace(go.Scatter(
        x=[cit_value],
        y=[y_pos],
        mode='markers+text',
        marker=dict(size=20, color='red', symbol='diamond', line=dict(color='white', width=2)),
        text=[f'CIT: {cit_value}'],
        textposition='top center',
        textfont=dict(size=14, color='red', family='Roboto', weight='bold'),
        name='Posición del evaluado',
        hovertemplate=f'<b>CIT: {cit_value}</b><br>Percentil: {obtener_percentil(cit_value)}<extra></extra>'
    ))
    
    # Líneas verticales de clasificación
    clasificaciones = [
        (70, 'Límite', '#E53935'),
        (85, 'Medio Bajo', '#FFB74D'),
        (100, 'Medio', '#FDD835'),
        (115, 'Medio Alto', '#81C784'),
        (130, 'Superior', '#66BB6A')
    ]
    
    for pos, texto, color in clasificaciones:
        fig.add_vline(
            x=pos,
            line_dash="dot",
            line_color=color,
            line_width=1.5,
            opacity=0.6
        )
    
    # Zonas de color
    fig.add_vrect(x0=70, x1=80, fillcolor='rgba(229, 57, 53, 0.1)', line_width=0)
    fig.add_vrect(x0=80, x1=90, fillcolor='rgba(255, 183, 77, 0.1)', line_width=0)
    fig.add_vrect(x0=90, x1=110, fillcolor='rgba(253, 216, 53, 0.1)', line_width=0)
    fig.add_vrect(x0=110, x1=120, fillcolor='rgba(129, 199, 132, 0.1)', line_width=0)
    fig.add_vrect(x0=120, x1=130, fillcolor='rgba(102, 187, 106, 0.1)', line_width=0)
    fig.add_vrect(x0=130, x1=160, fillcolor='rgba(46, 125, 50, 0.1)', line_width=0)
    
    fig.update_layout(
        title={
            'text': '<b>Curva Normal de Clasificación</b>',
            'font': {'size': 22, 'color': '#212529', 'family': 'Roboto'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            range=[40, 160],
            dtick=10,
            title='Puntuación Compuesta',
            titlefont=dict(size=14, color='#212529'),
            tickfont=dict(size=12, color='#212529'),
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)'
        ),
        yaxis=dict(
            showticklabels=False,
            title='Densidad de Probabilidad',
            titlefont=dict(size=14, color='#212529'),
            showgrid=False
        ),
        height=450,
        template='plotly_white',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=60, r=60, t=80, b=80)
    )
    
    return fig

def crear_grafico_radar(indices):
    """
    Crea un gráfico radar para visualizar el perfil cognitivo
    """
    categorias = ['Comprensión\nVerbal', 'Visoespacial', 'Razonamiento\nFluido', 
                 'Memoria de\nTrabajo', 'Velocidad de\nProcesamiento']
    
    valores = [
        indices.get('ICV', 100),
        indices.get('IVE', 100),
        indices.get('IRF', 100),
        indices.get('IMT', 100),
        indices.get('IVP', 100)
    ]
    
    fig = go.Figure()
    
    # Perfil del evaluado
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        fillcolor='rgba(139, 21, 56, 0.3)',
        line=dict(color='#8B1538', width=3),
        marker=dict(size=10, color='#8B1538'),
        name='Perfil del Evaluado',
        hovertemplate='<b>%{theta}</b><br>Puntuación: %{r}<extra></extra>'
    ))
    
    # Línea de referencia (media = 100)
    fig.add_trace(go.Scatterpolar(
        r=[100, 100, 100, 100, 100],
        theta=categorias,
        mode='lines',
        line=dict(color='gray', width=2, dash='dash'),
        name='Media Poblacional (100)',
        hovertemplate='Media: 100<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[40, 160],
                tickfont=dict(size=11, color='#212529'),
                showline=True,
                linecolor='rgba(0,0,0,0.2)',
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#212529', family='Roboto')
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        legend=dict(
            font=dict(size=11, color='#212529'),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        title={
            'text': '<b>Perfil Cognitivo Multidimensional</b>',
            'font': {'size': 20, 'color': '#212529', 'family': 'Roboto'},
            'x': 0.5,
            'xanchor': 'center'
        },
        height=550,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# ==================== INTERFAZ PRINCIPAL ====================

st.markdown("<h1>🧠 WPPSI-IV - Sistema de Informes Psicopedagógicos</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #495057; margin-bottom: 2rem;'>Escala de Inteligencia de Wechsler para Preescolar y Primaria - IV<br><b>Desarrollado especialmente para Daniela ❤️</b></p>", unsafe_allow_html=True)

# Crear tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Datos del Evaluado",
    "📊 Resultados y Gráficos",
    "📈 Análisis Detallado",
    "📄 Generar Informe PDF"
])

# ==================== TAB 1: DATOS DEL EVALUADO ====================
with tab1:
    st.markdown("## 👤 Información del Niño/a Evaluado")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        nombre_nino = st.text_input("👦 Nombre completo del niño/a", value="Micaela", key="nombre")
    
    with col2:
        sexo_nino = st.selectbox("⚧ Sexo", options=["F", "M"], key="sexo")
    
    with col3:
        fecha_nacimiento = st.date_input("🎂 Fecha de nacimiento", value=date(2020, 10, 1), key="fecha_nac")
    
    with col4:
        fecha_aplicacion = st.date_input("📅 Fecha de evaluación", value=date.today(), key="fecha_apl")
    
    col5, col6 = st.columns(2)
    
    with col5:
        nombre_examinador = st.text_input("👨‍⚕️ Nombre del examinador/a", value="Daniela", key="examinador")
    
    with col6:
        lugar_aplicacion = st.text_input("📍 Lugar de aplicación", value="Argentina", key="lugar")
    
    st.markdown("---")
    st.markdown("## 📊 Ingreso de Puntuaciones Directas (PD)")
    st.info("💡 Ingrese las puntuaciones directas obtenidas en cada subtest (0-30). Deje en blanco si no se aplicó.")
    
    # Organizar por índices
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🗣️ Comprensión Verbal")
        pd_informacion = st.number_input("Información", min_value=0, max_value=30, value=10, step=1, key="pd_info")
        pd_semejanzas = st.number_input("Semejanzas", min_value=0, max_value=30, value=13, step=1, key="pd_sem")
        
        st.markdown("### 🧩 Visoespacial")
        pd_cubos = st.number_input("Cubos", min_value=0, max_value=30, value=16, step=1, key="pd_cub")
        pd_rompecabezas = st.number_input("Rompecabezas", min_value=0, max_value=30, value=13, step=1, key="pd_rom")
    
    with col2:
        st.markdown("### 🧠 Razonamiento Fluido")
        pd_matrices = st.number_input("Matrices", min_value=0, max_value=30, value=11, step=1, key="pd_mat")
        pd_conceptos = st.number_input("Conceptos", min_value=0, max_value=30, value=11, step=1, key="pd_con")
        
        st.markdown("### 💭 Memoria de Trabajo")
        pd_reconocimiento = st.number_input("Reconocimiento", min_value=0, max_value=30, value=11, step=1, key="pd_rec")
        pd_localizacion = st.number_input("Localización", min_value=0, max_value=30, value=8, step=1, key="pd_loc")
    
    with col3:
        st.markdown("### ⚡ Velocidad de Procesamiento")
        pd_busqueda_animales = st.number_input("Búsqueda de Animales", min_value=0, max_value=30, value=12, step=1, key="pd_bus")
        pd_cancelacion = st.number_input("Cancelación", min_value=0, max_value=30, value=8, step=1, key="pd_can")
    
    st.markdown("---")
    
    # Botón para procesar
    if st.button("🎯 GENERAR INFORME COMPLETO", type="primary", use_container_width=True):
        # Validaciones
        if not nombre_nino:
            st.error("❌ Por favor ingrese el nombre del niño/a")
        elif not nombre_examinador:
            st.error("❌ Por favor ingrese el nombre del examinador/a")
        else:
            # Calcular edad
            years, months, days = calcular_edad(fecha_nacimiento, fecha_aplicacion)
            
            # Guardar puntuaciones
            puntuaciones_directas = {
                'cubos': pd_cubos,
                'informacion': pd_informacion,
                'matrices': pd_matrices,
                'busqueda_animales': pd_busqueda_animales,
                'reconocimiento': pd_reconocimiento,
                'semejanzas': pd_semejanzas,
                'conceptos': pd_conceptos,
                'localizacion': pd_localizacion,
                'cancelacion': pd_cancelacion,
                'rompecabezas': pd_rompecabezas
            }
            
            # Convertir PD a PE
            pe_dict = {}
            for prueba, pd in puntuaciones_directas.items():
                pe = convertir_pd_a_pe(prueba, pd)
                if pe is not None:
                    pe_dict[prueba] = pe
            
            # Calcular índices
            indices = calcular_indices(pe_dict)
            
            # Guardar en session_state
            st.session_state['datos_completos'] = True
            st.session_state['nombre'] = nombre_nino
            st.session_state['sexo'] = sexo_nino
            st.session_state['fecha_nac'] = fecha_nacimiento
            st.session_state['fecha_apl'] = fecha_aplicacion
            st.session_state['examinador'] = nombre_examinador
            st.session_state['lugar'] = lugar_aplicacion
            st.session_state['edad_years'] = years
            st.session_state['edad_months'] = months
            st.session_state['edad_days'] = days
            st.session_state['pd'] = puntuaciones_directas
            st.session_state['pe'] = pe_dict
            st.session_state['indices'] = indices
            
            st.success("✅ ¡Datos procesados exitosamente! Pase a la pestaña 'Resultados y Gráficos'")
            st.balloons()

# ==================== TAB 2: RESULTADOS Y GRÁFICOS ====================
with tab2:
    if 'datos_completos' in st.session_state and st.session_state['datos_completos']:
        # Obtener datos
        nombre = st.session_state['nombre']
        years = st.session_state['edad_years']
        months = st.session_state['edad_months']
        days = st.session_state['edad_days']
        pe_dict = st.session_state['pe']
        indices = st.session_state['indices']
        pd_dict = st.session_state['pd']
        
        # Resumen ejecutivo
        st.markdown("## 📋 Página de Resumen")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👤 Evaluado", nombre)
        with col2:
            st.metric("📅 Edad Cronológica", f"{years}a, {months}m, {days}d")
        with col3:
            cit = indices.get('CIT', 100)
            st.metric("🎯 CI Total (CIT)", cit, f"Percentil {obtener_percentil(cit)}")
        with col4:
            cat = obtener_categoria(cit)
            st.metric("📊 Clasificación", cat['categoria'])
        
        st.markdown("---")
        
        # Tabla de conversión PD -> PE
        st.markdown("### 🔄 Conversión de Puntuaciones Directas a Escalares")
        
        pruebas_nombres = {
            'cubos': 'Cubos',
            'informacion': 'Información',
            'matrices': 'Matrices',
            'busqueda_animales': 'Búsqueda de Animales',
            'reconocimiento': 'Reconocimiento',
            'semejanzas': 'Semejanzas',
            'conceptos': 'Conceptos',
            'localizacion': 'Localización',
            'cancelacion': 'Cancelación',
            'rompecabezas': 'Rompecabezas'
        }
        
        datos_conversion = []
        for key, nombre_prueba in pruebas_nombres.items():
            pd = pd_dict.get(key, '-')
            pe = pe_dict.get(key, '-')
            datos_conversion.append({
                'Prueba': nombre_prueba,
                'PD': pd if pd != '-' else '-',
                'PE': pe if pe != '-' else '-'
            })
        
        df_conversion = pd.DataFrame(datos_conversion)
        st.dataframe(df_conversion, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Gráficos principales
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(crear_grafico_perfil_escalares(pe_dict), use_container_width=True)
        
        with col2:
            st.plotly_chart(crear_grafico_perfil_compuestas(indices), use_container_width=True)
        
        st.markdown("---")
        
        # Curva normal
        st.plotly_chart(crear_curva_normal(indices.get('CIT', 100)), use_container_width=True)
        
        st.markdown("---")
        
        # Gráfico radar
        st.plotly_chart(crear_grafico_radar(indices), use_container_width=True)
        
    else:
        st.warning("⚠️ Por favor, complete los datos en la pestaña 'Datos del Evaluado' primero")

# ==================== TAB 3: ANÁLISIS DETALLADO ====================
with tab3:
    if 'datos_completos' in st.session_state and st.session_state['datos_completos']:
        indices = st.session_state['indices']
        pe_dict = st.session_state['pe']
        nombre = st.session_state['nombre']
        
        st.markdown("## 📊 Análisis Detallado de Índices Compuestos")
        
        # Tabla de índices compuestos
        datos_indices = []
        indices_info = [
            ('Comprensión Verbal (ICV)', 'ICV', 'suma_icv', '🗣️'),
            ('Visoespacial (IVE)', 'IVE', 'suma_ive', '🧩'),
            ('Razonamiento Fluido (IRF)', 'IRF', 'suma_irf', '🧠'),
            ('Memoria de Trabajo (IMT)', 'IMT', 'suma_imt', '💭'),
            ('Velocidad de Procesamiento (IVP)', 'IVP', 'suma_ivp', '⚡'),
            ('CI TOTAL (CIT)', 'CIT', 'suma_cit', '🏆')
        ]
        
        for nombre_idx, key_idx, key_suma, emoji in indices_info:
            valor = indices.get(key_idx, 100)
            suma = indices.get(key_suma, 0)
            percentil = obtener_percentil(valor)
            categoria = obtener_categoria(valor)['categoria']
            
            datos_indices.append({
                'Índice': f"{emoji} {nombre_idx}",
                'Suma PE': suma,
                'Puntuación': valor,
                'Percentil': percentil,
                'Clasificación': categoria
            })
        
        df_indices = pd.DataFrame(datos_indices)
        st.dataframe(df_indices, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Análisis por índice
        st.markdown("### 📝 Interpretación por Dominios Cognitivos")
        
        for nombre_idx, key_idx, key_suma, emoji in indices_info:
            valor = indices.get(key_idx, 100)
            cat = obtener_categoria(valor)
            perc = obtener_percentil(valor)
            
            with st.expander(f"{emoji} {nombre_idx}: {valor} puntos"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Puntuación", valor)
                with col2:
                    st.metric("Percentil", perc)
                with col3:
                    st.markdown(f"**Categoría:**<br><span style='color: {cat['color']}; font-weight: bold;'>{cat['categoria']}</span>", unsafe_allow_html=True)
                
                st.markdown(f"**Descripción:** {cat['descripcion']}")
                st.progress(perc / 100)
        
        st.markdown("---")
        
        # Fortalezas y debilidades
        st.markdown("### 💪 Análisis de Fortalezas y Debilidades Personales")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Fortalezas (PE ≥ 13)")
            fortalezas = []
            for key, valor in pe_dict.items():
                if valor >= 13:
                    nombre_prueba = key.replace('_', ' ').title()
                    fortalezas.append((nombre_prueba, valor))
            
            if fortalezas:
                for prueba, valor in fortalezas:
                    st.success(f"**{prueba}**: PE = {valor}")
                    st.progress(valor / 19)
            else:
                st.info("No se identificaron fortalezas significativas (PE ≥ 13)")
        
        with col2:
            st.markdown("#### ⚠️ Áreas a Desarrollar (PE ≤ 7)")
            debilidades = []
            for key, valor in pe_dict.items():
                if valor <= 7:
                    nombre_prueba = key.replace('_', ' ').title()
                    debilidades.append((nombre_prueba, valor))
            
            if debilidades:
                for prueba, valor in debilidades:
                    st.warning(f"**{prueba}**: PE = {valor}")
                    st.progress(valor / 19)
            else:
                st.info("No se identificaron debilidades significativas (PE ≤ 7)")
        
        st.markdown("---")
        
        # Interpretación clínica
        st.markdown("### 📝 Interpretación Clínica Integrada")
        
        cit = indices.get('CIT', 100)
        cat_cit = obtener_categoria(cit)
        perc_cit = obtener_percentil(cit)
        
        interpretacion_html = f"""
        <div style='background: white; padding: 2rem; border-radius: 15px; border-left: 6px solid {cat_cit['color']}; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h3 style='color: #212529; margin-top: 0;'>Resumen del Funcionamiento Cognitivo</h3>
            <p style='font-size: 1.1rem; line-height: 1.8; color: #343a40;'>
                <b>{nombre}</b> obtuvo un <b>Coeficiente Intelectual Total (CIT) de {cit}</b>, 
                clasificado en la categoría <b style='color: {cat_cit['color']};'>{cat_cit['categoria']}</b> 
                ({cat_cit['nivel']}).
            </p>
            <p style='font-size: 1.05rem; line-height: 1.8; color: #495057;'>
                Esta puntuación se ubica en el <b>percentil {perc_cit}</b>, lo que indica que su rendimiento 
                supera al {perc_cit}% de los niños de su edad en la muestra de tipificación.
            </p>
            <p style='font-size: 1rem; color: #6c757d; margin-bottom: 1.5rem;'>
                {cat_cit['descripcion']}
            </p>
            
            <h4 style='color: #212529; margin-top: 1.5rem;'>Análisis por Dominios Cognitivos:</h4>
            <ul style='font-size: 1rem; line-height: 1.9; color: #495057; list-style-type: none; padding-left: 0;'>
                <li>🗣️ <b>Comprensión Verbal (ICV: {indices.get('ICV', 100)})</b>: {obtener_categoria(indices.get('ICV', 100))['categoria']} - Percentil {obtener_percentil(indices.get('ICV', 100))}</li>
                <li>🧩 <b>Visoespacial (IVE: {indices.get('IVE', 100)})</b>: {obtener_categoria(indices.get('IVE', 100))['categoria']} - Percentil {obtener_percentil(indices.get('IVE', 100))}</li>
                <li>🧠 <b>Razonamiento Fluido (IRF: {indices.get('IRF', 100)})</b>: {obtener_categoria(indices.get('IRF', 100))['categoria']} - Percentil {obtener_percentil(indices.get('IRF', 100))}</li>
                <li>💭 <b>Memoria de Trabajo (IMT: {indices.get('IMT', 100)})</b>: {obtener_categoria(indices.get('IMT', 100))['categoria']} - Percentil {obtener_percentil(indices.get('IMT', 100))}</li>
                <li>⚡ <b>Velocidad de Procesamiento (IVP: {indices.get('IVP', 100)})</b>: {obtener_categoria(indices.get('IVP', 100))['categoria']} - Percentil {obtener_percentil(indices.get('IVP', 100))}</li>
            </ul>
        </div>
        """
        
        st.markdown(interpretacion_html, unsafe_allow_html=True)
        
    else:
        st.warning("⚠️ Por favor, complete los datos en la pestaña 'Datos del Evaluado' primero")

# ==================== TAB 4: GENERAR PDF ====================
with tab4:
    if 'datos_completos' in st.session_state and st.session_state['datos_completos']:
        st.markdown("## 📄 Generación de Informe PDF Profesional")
        st.info("💡 El informe incluirá todos los análisis, gráficos y tablas generados en las pestañas anteriores")
        
        st.markdown("### 📋 Vista Previa del Contenido")
        
        nombre = st.session_state['nombre']
        fecha_apl = st.session_state['fecha_apl']
        
        st.markdown(f"""
        El informe PDF incluirá:
        
        1. **Portada** con datos del evaluado
        2. **Tabla de conversión** PD → PE
        3. **Gráficos profesionales**:
           - Perfil de puntuaciones escalares
           - Perfil de puntuaciones compuestas
           - Curva normal de clasificación
           - Gráfico radar multidimensional
        4. **Tabla de índices compuestos** completa
        5. **Análisis de fortalezas y debilidades**
        6. **Interpretación clínica** detallada
        
        **Nombre del archivo:** `Informe_WPPSI-IV_{nombre.replace(' ', '_')}_{fecha_apl.strftime('%Y%m%d')}.pdf`
        """)
        
        if st.button("📥 DESCARGAR INFORME COMPLETO EN PDF", type="primary", use_container_width=True):
            st.warning("🚧 Funcionalidad de generación de PDF en desarrollo. Los gráficos y tablas están disponibles en las pestañas anteriores.")
            st.info("💡 Puede hacer capturas de pantalla de los gráficos y tablas para incluir en su informe.")
        
    else:
        st.warning("⚠️ Por favor, complete los datos en la pestaña 'Datos del Evaluado' primero")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
    <div class='footer'>
        <h3 style='color: #212529; margin-bottom: 1rem;'>🧠 WPPSI-IV - Sistema de Informes Psicopedagógicos</h3>
        <p style='font-size: 1.1rem; color: #495057; margin-bottom: 0.5rem;'>
            Herramienta profesional para evaluación psicopedagógica
        </p>
        <p style='font-size: 1rem; color: #6c757d; margin-bottom: 1rem;'>
            Escala de Inteligencia de Wechsler para Preescolar y Primaria - Cuarta Edición
        </p>
        <p style='font-size: 0.95rem; color: #8B1538; font-weight: 600;'>
            ❤️ Desarrollado especialmente para Daniela
        </p>
        <p style='font-size: 0.85rem; color: #adb5bd; margin-top: 1rem;'>
            © 2026 - Sistema diseñado con dedicación para facilitar la labor profesional
        </p>
    </div>
""", unsafe_allow_html=True)
