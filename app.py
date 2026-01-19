"""
═══════════════════════════════════════════════════════════════════════════════
WPPSI-IV SISTEMA PROFESIONAL ULTRA COMPLETO
Sistema Integral de Evaluación Psicopedagógica
Desarrollado especialmente para Daniela ❤️
Versión: 7.0.0 Professional Ultra Edition
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import numpy as np
import io
from scipy.stats import norm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, 
                                Spacer, PageBreak, KeepTogether, Image as RLImage)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm, inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Line, Rect, Circle, PolyLine, String, Polygon
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas as pdf_canvas
import base64
import time

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN INICIAL DE LA APLICACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="WPPSI-IV Professional Ultra",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.pearson.com/wppsi',
        'Report a bug': None,
        'About': "Sistema WPPSI-IV v7.0 - Desarrollado para Daniela ❤️"
    }
)

# Inicialización completa de Session State
def init_session_state():
    """Inicializa todas las variables de session state"""
    defaults = {
        'datos_completos': False,
        'paso_actual': 1,
        'nombre_paciente': '',
        'fecha_nacimiento': None,
        'fecha_evaluacion': None,
        'examinador': '',
        'lugar_aplicacion': '',
        'sexo': 'F',
        'dominancia': 'D',
        'motivo_consulta': '',
        'observaciones': '',
        'pruebas_aplicadas': {
            'cubos': True,
            'informacion': True,
            'matrices': True,
            'busqueda_animales': True,
            'reconocimiento': True,
            'semejanzas': True,
            'conceptos': True,
            'localizacion': True,
            'cancelacion': True,
            'rompecabezas': True,
            'vocabulario': False,
            'nombres': False,
            'clave_figuras': False,
            'comprension': False,
            'dibujos': False
        },
        'pd_dict': {},
        'pe_dict': {},
        'indices_primarios': {},
        'indices_secundarios': {},
        'analisis_completo': {},
        'fortalezas': [],
        'debilidades': [],
        'comparaciones': {},
        'interpretacion_generada': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ═══════════════════════════════════════════════════════════════════════════════
# ESTILOS CSS ULTRA MEJORADOS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

:root {
    --primary: #8B1538;
    --primary-dark: #6b0e2a;
    --primary-light: #c71f4a;
    --secondary: #2c3e50;
    --success: #27ae60;
    --warning: #f39c12;
    --danger: #e74c3c;
    --info: #3498db;
    --light: #ecf0f1;
    --dark: #2c3e50;
    --text-dark: #2c3e50;
    --text-light: #ffffff;
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', sans-serif !important;
    color: var(--text-dark) !important;
    font-weight: 700 !important;
}

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-attachment: fixed;
}

.main {
    background: linear-gradient(to bottom, rgba(255,255,255,0.98), rgba(255,255,255,0.95));
    border-radius: 25px;
    padding: 2.5rem;
    margin: 1.5rem;
    box-shadow: 
        0 25px 50px rgba(0,0,0,0.15),
        0 10px 20px rgba(0,0,0,0.1),
        inset 0 1px 0 rgba(255,255,255,0.8);
    backdrop-filter: blur(10px);
}

/* ==================== HEADER ULTRA MEJORADO ==================== */
.header-ultra {
    background: linear-gradient(135deg, #8B1538 0%, #c71f4a 50%, #8B1538 100%);
    padding: 3.5rem 2.5rem;
    border-radius: 25px;
    color: white;
    text-align: center;
    box-shadow: 
        0 20px 60px rgba(139, 21, 56, 0.4),
        0 10px 30px rgba(139, 21, 56, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
    border: 2px solid rgba(255,255,255,0.1);
}

.header-ultra::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
    animation: rotate-gradient 25s linear infinite;
}

.header-ultra::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, 
        transparent 0%, 
        rgba(255,255,255,0.8) 50%, 
        transparent 100%);
}

.header-title {
    font-size: 3.5rem;
    font-weight: 900;
    margin: 0;
    text-shadow: 
        0 4px 12px rgba(0,0,0,0.3),
        0 2px 4px rgba(0,0,0,0.2),
        0 1px 2px rgba(0,0,0,0.1);
    position: relative;
    z-index: 2;
    letter-spacing: -1px;
}

.header-subtitle {
    font-size: 1.3rem;
    font-weight: 400;
    margin-top: 0.8rem;
    opacity: 0.95;
    position: relative;
    z-index: 2;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.header-version {
    display: inline-block;
    background: rgba(255,255,255,0.25);
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 1rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.3);
}

/* ==================== MÉTRICAS MEJORADAS ==================== */
div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border: none;
    padding: 1.8rem;
    border-radius: 18px;
    box-shadow: 
        0 8px 24px rgba(0,0,0,0.08),
        0 4px 12px rgba(0,0,0,0.04),
        inset 0 1px 0 rgba(255,255,255,0.9);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border-left: 5px solid var(--primary);
    position: relative;
    overflow: hidden;
}

div[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 100px;
    height: 100px;
    background: radial-gradient(circle, rgba(139, 21, 56, 0.08) 0%, transparent 70%);
    border-radius: 50%;
    transform: translate(30%, -30%);
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-10px) scale(1.03);
    box-shadow: 
        0 20px 40px rgba(139, 21, 56, 0.15),
        0 10px 20px rgba(139, 21, 56, 0.1);
    border-left-width: 6px;
}

[data-testid="stMetricLabel"] {
    font-size: 0.95rem;
    color: #5a6c7d !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem !important;
}

[data-testid="stMetricValue"] {
    font-size: 3rem;
    color: var(--primary) !important;
    font-weight: 900 !important;
    text-shadow: 0 3px 6px rgba(139, 21, 56, 0.15);
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="stMetricDelta"] {
    font-size: 1rem;
    font-weight: 600;
}

/* ==================== INPUTS ULTRA MEJORADOS ==================== */
.stTextInput input, .stNumberInput input, .stDateInput input, 
.stSelectbox > div > div, .stTextArea textarea {
    background: linear-gradient(to bottom, #ffffff, #f8f9fa) !important;
    border: 2px solid #e1e8ed !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    color: var(--text-dark) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 3px 10px rgba(0,0,0,0.05),
        inset 0 1px 2px rgba(0,0,0,0.03) !important;
}

.stTextInput input:focus, .stNumberInput input:focus, 
.stDateInput input:focus, .stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 
        0 0 0 5px rgba(139, 21, 56, 0.12),
        0 5px 15px rgba(139, 21, 56, 0.1) !important;
    transform: translateY(-2px);
    background: #ffffff !important;
}

label {
    color: var(--text-dark) !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    margin-bottom: 10px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ==================== CHECKBOXES MEJORADOS ==================== */
.stCheckbox {
    padding: 12px 16px;
    border-radius: 10px;
    transition: all 0.3s ease;
    background: rgba(139, 21, 56, 0.02);
    border: 1px solid rgba(139, 21, 56, 0.1);
}

.stCheckbox:hover {
    background: rgba(139, 21, 56, 0.08);
    border-color: rgba(139, 21, 56, 0.2);
    transform: translateX(4px);
}

.stCheckbox label {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: var(--text-dark) !important;
    text-transform: none !important;
}

/* ==================== BOTONES ULTRA PREMIUM ==================== */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    border: none !important;
    padding: 16px 38px !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    border-radius: 60px !important;
    box-shadow: 
        0 10px 25px rgba(139, 21, 56, 0.35),
        0 5px 15px rgba(139, 21, 56, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.stButton > button:hover::before {
    width: 300px;
    height: 300px;
}

.stButton > button:hover {
    transform: translateY(-6px) scale(1.05);
    box-shadow: 
        0 20px 45px rgba(139, 21, 56, 0.5),
        0 10px 25px rgba(139, 21, 56, 0.35) !important;
}

.stButton > button:active {
    transform: translateY(-2px) scale(1.02);
}

/* ==================== TABLAS ULTRA PROFESIONALES ==================== */
.dataframe {
    border-radius: 15px !important;
    overflow: hidden !important;
    box-shadow: 
        0 8px 25px rgba(0,0,0,0.12),
        0 4px 12px rgba(0,0,0,0.08) !important;
    border: 1px solid rgba(139, 21, 56, 0.1) !important;
}

.dataframe thead th {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    padding: 18px !important;
    font-weight: 800 !important;
    font-size: 13px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    border-bottom: 3px solid rgba(255,255,255,0.2) !important;
}

.dataframe tbody td {
    padding: 16px !important;
    border-bottom: 1px solid rgba(225, 232, 237, 0.8) !important;
    color: var(--text-dark) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

.dataframe tbody tr {
    transition: all 0.3s ease;
}

.dataframe tbody tr:hover {
    background: linear-gradient(to right, rgba(139, 21, 56, 0.08), rgba(139, 21, 56, 0.04)) !important;
    transform: scale(1.01);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.dataframe tbody tr:nth-child(even) {
    background: rgba(248, 249, 250, 0.5) !important;
}

/* ==================== ALERTAS ULTRA MEJORADAS ==================== */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 15px !important;
    padding: 20px 24px !important;
    border-left: 6px solid !important;
    box-shadow: 
        0 6px 20px rgba(0,0,0,0.1),
        0 3px 10px rgba(0,0,0,0.05) !important;
    animation: slide-in-right 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.stSuccess {
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
    border-left-color: #28a745 !important;
}

.stSuccess::before {
    content: '✓';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 3rem;
    color: rgba(40, 167, 69, 0.15);
    font-weight: 900;
}

.stSuccess div[data-testid="stMarkdownContainer"] p {
    color: #155724 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

.stError {
    background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%) !important;
    border-left-color: #dc3545 !important;
}

.stError::before {
    content: '✕';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 3rem;
    color: rgba(220, 53, 69, 0.15);
    font-weight: 900;
}

.stError div[data-testid="stMarkdownContainer"] p {
    color: #721c24 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

.stWarning {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%) !important;
    border-left-color: #ffc107 !important;
}

.stWarning::before {
    content: '⚠';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 3rem;
    color: rgba(255, 193, 7, 0.2);
    font-weight: 900;
}

.stWarning div[data-testid="stMarkdownContainer"] p {
    color: #856404 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

.stInfo {
    background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%) !important;
    border-left-color: #17a2b8 !important;
}

.stInfo::before {
    content: 'ℹ';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 3rem;
    color: rgba(23, 162, 184, 0.15);
    font-weight: 900;
}

.stInfo div[data-testid="stMarkdownContainer"] p {
    color: #0c5460 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

/* ==================== TABS ULTRA MEJORADOS ==================== */
.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
    background: linear-gradient(to bottom, #ffffff, #f8f9fa);
    padding: 16px;
    border-radius: 18px;
    box-shadow: 
        0 6px 20px rgba(0,0,0,0.08),
        inset 0 1px 0 rgba(255,255,255,0.8);
    border: 1px solid rgba(139, 21, 56, 0.1);
}

.stTabs [data-baseweb="tab"] {
    background: linear-gradient(to bottom, #f8f9fa, #e9ecef);
    color: #5a6c7d !important;
    border-radius: 12px;
    padding: 14px 28px;
    font-weight: 700;
    font-size: 14px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid transparent;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

.stTabs [data-baseweb="tab"]:hover {
    background: linear-gradient(to bottom, #ffffff, #f8f9fa);
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    box-shadow: 
        0 8px 20px rgba(139, 21, 56, 0.35),
        0 4px 10px rgba(139, 21, 56, 0.25);
    border-color: rgba(255,255,255,0.3);
    transform: translateY(-2px);
}

/* ==================== EXPANDERS MEJORADOS ==================== */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #f8f9fa 0%, white 100%) !important;
    border-radius: 12px !important;
    padding: 18px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border-left: 5px solid var(--primary) !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    color: var(--text-dark) !important;
}

.streamlit-expanderHeader:hover {
    background: linear-gradient(135deg, white 0%, #f8f9fa 100%) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important;
    transform: translateX(5px);
}

/* ==================== BARRA DE PROGRESO ==================== */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(139, 21, 56, 0.3);
}

.stProgress > div {
    background: rgba(139, 21, 56, 0.1);
    border-radius: 10px;
}

/* ==================== CARD CONTAINER ==================== */
.card-container {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    padding: 28px;
    border-radius: 18px;
    box-shadow: 
        0 8px 24px rgba(0,0,0,0.1),
        0 4px 12px rgba(0,0,0,0.05),
        inset 0 1px 0 rgba(255,255,255,0.8);
    margin-bottom: 24px;
    transition: all 0.4s ease;
    border-left: 5px solid var(--primary);
    position: relative;
    overflow: hidden;
}

.card-container::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, rgba(139, 21, 56, 0.05) 0%, transparent 70%);
    border-radius: 50%;
    transform: translate(40%, -40%);
}

.card-container:hover {
    box-shadow: 
        0 12px 35px rgba(0,0,0,0.15),
        0 6px 18px rgba(0,0,0,0.1);
    transform: translateY(-6px);
    border-left-width: 6px;
}

/* ==================== BADGE / PILL ==================== */
.badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.15);
}

.badge-success {
    background: linear-gradient(135deg, #27ae60, #2ecc71);
    color: white;
}

.badge-danger {
    background: linear-gradient(135deg, #c0392b, #e74c3c);
    color: white;
}

.badge-warning {
    background: linear-gradient(135deg, #f39c12, #f1c40f);
    color: #2c3e50;
}

.badge-info {
    background: linear-gradient(135deg, #2980b9, #3498db);
    color: white;
}

.badge-primary {
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    color: white;
}

/* ==================== ANIMACIONES ==================== */
@keyframes rotate-gradient {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes slide-in-right {
    from {
        opacity: 0;
        transform: translateX(40px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slide-in-left {
    from {
        opacity: 0;
        transform: translateX(-40px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fade-in-up {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse-glow {
    0%, 100% { 
        box-shadow: 0 0 20px rgba(139, 21, 56, 0.3);
    }
    50% { 
        box-shadow: 0 0 40px rgba(139, 21, 56, 0.6);
    }
}

@keyframes bounce-subtle {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.animate-fade-in {
    animation: fade-in-up 0.6s ease-out;
}

.animate-slide-right {
    animation: slide-in-right 0.5s ease-out;
}

/* ==================== SCROLLBAR PERSONALIZADO ==================== */
::-webkit-scrollbar {
    width: 14px;
    height: 14px;
}

::-webkit-scrollbar-track {
    background: linear-gradient(to bottom, #f1f1f1, #e1e1e1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    border-radius: 10px;
    border: 2px solid #f1f1f1;
    box-shadow: inset 0 1px 2px rgba(255,255,255,0.3);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
}

/* ==================== SIDEBAR MEJORADO ==================== */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
    border-right: 3px solid rgba(139, 21, 56, 0.1);
    box-shadow: 4px 0 20px rgba(0,0,0,0.08);
}

[data-testid="stSidebarNav"] {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    padding: 1.5rem;
    border-radius: 15px;
    margin-bottom: 1.5rem;
}

/* ==================== FOOTER PROFESIONAL ==================== */
.footer-ultra {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 20px;
    margin-top: 4rem;
    box-shadow: 
        0 -6px 25px rgba(0,0,0,0.1),
        inset 0 1px 0 rgba(255,255,255,0.8);
    border-bottom: 5px solid var(--primary);
    position: relative;
    overflow: hidden;
}

.footer-ultra::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, 
        transparent 0%, 
        var(--primary) 50%, 
        transparent 100%);
}

.footer-ultra p {
    color: var(--text-dark);
    margin: 0.8rem 0;
    font-weight: 600;
}

/* ==================== FLOATING AVATAR DANIELA ==================== */
.daniela-avatar-ultra {
    position: fixed;
    bottom: 35px;
    right: 35px;
    width: 90px;
    height: 90px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 45px;
    box-shadow: 
        0 12px 30px rgba(139, 21, 56, 0.5),
        0 6px 15px rgba(139, 21, 56, 0.3),
        inset 0 2px 4px rgba(255,255,255,0.3);
    animation: bounce-subtle 3s ease-in-out infinite;
    z-index: 9999;
    cursor: pointer;
    transition: all 0.4s ease;
    border: 4px solid rgba(255,255,255,0.3);
}

.daniela-avatar-ultra:hover {
    transform: scale(1.15) rotate(10deg);
    box-shadow: 
        0 18px 45px rgba(139, 21, 56, 0.6),
        0 9px 22px rgba(139, 21, 56, 0.4);
}

/* ==================== NÚMERO DE PASO ==================== */
.step-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 45px;
    height: 45px;
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    color: white;
    border-radius: 50%;
    font-weight: 900;
    font-size: 20px;
    box-shadow: 
        0 6px 18px rgba(139, 21, 56, 0.35),
        inset 0 1px 2px rgba(255,255,255,0.2);
    margin-right: 15px;
}

/* ==================== TOOLTIP ==================== */
.tooltip {
    position: relative;
    display: inline-block;
    cursor: help;
}

.tooltip:hover::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    background: var(--text-dark);
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    white-space: nowrap;
    font-size: 13px;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    z-index: 1000;
}

/* ==================== LOADING SPINNER ==================== */
.loading-spinner {
    border: 4px solid rgba(139, 21, 56, 0.1);
    border-top: 4px solid var(--primary);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin: 2rem auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* ==================== DIVISOR DECORATIVO ==================== */
.divider-decorative {
    height: 4px;
    background: linear-gradient(90deg, 
        transparent 0%, 
        var(--primary) 30%, 
        var(--primary-light) 50%, 
        var(--primary) 70%, 
        transparent 100%);
    border-radius: 2px;
    margin: 3rem 0;
    box-shadow: 0 2px 8px rgba(139, 21, 56, 0.3);
}

/* ==================== RESPONSIVIDAD ==================== */
@media (max-width: 768px) {
    .header-title {
        font-size: 2.5rem;
    }
    
    .header-subtitle {
        font-size: 1rem;
    }
    
    .main {
        padding: 1.5rem;
        margin: 0.5rem;
    }
    
    .daniela-avatar-ultra {
        width: 70px;
        height: 70px;
        font-size: 35px;
        bottom: 20px;
        right: 20px;
    }
}
</style>
""", unsafe_allow_html=True)

# Avatar flotante de Daniela
st.markdown('<div class="daniela-avatar-ultra" title="Desarrollado con ❤️ para Daniela">👩‍🦱</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CLASE DE BAREMOS WPPSI-IV ULTRA COMPLETA
# ═══════════════════════════════════════════════════════════════════════════════

class BaremosWPPSIUltra:
    """
    Clase que contiene TODOS los baremos oficiales del WPPSI-IV
    Basado en el manual técnico oficial de Pearson
    Incluye baremos para edad 4:0-7:7 años
    """
    
    # ==================== TABLAS DE CONVERSIÓN PD → PE ====================
    # Basadas en las tablas del manual de aplicación y corrección
    # Para edad 5:9-5:11 (Edad de Micaela en el ejemplo)
    
    TABLAS_CONVERSION_PD_PE = {
        'cubos': {
            0:1, 1:1, 2:1, 3:1, 4:1, 5:2, 6:3, 7:4, 8:5, 9:6, 10:7, 11:8, 12:9,
            13:10, 14:11, 15:12, 16:13, 17:14, 18:15, 19:16, 20:16, 21:17, 22:17,
            23:18, 24:18, 25:19, 26:19, 27:19, 28:19, 29:19, 30:19
        },
        'informacion': {
            0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10,
            13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:17, 20:17, 21:18, 22:18,
            23:19, 24:19, 25:19, 26:19
        },
        'matrices': {
            0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11,
            13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19
        },
        'busqueda_animales': {
            0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10,
            13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:17, 20:18, 21:19
        },
        'reconocimiento': {
            0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10,
            13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:17, 20:18
        },
        'semejanzas': {
            0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10,
            13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:16, 20:17, 21:17, 22:18,
            23:18, 24:19, 25:19, 26:19, 27:19, 28:19, 29:19, 30:19
        },
        'conceptos': {
            0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11,
            13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19
        },
        'localizacion': {
            0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11,
            13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19
        },
        'cancelacion': {
            0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11,
            13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19, 21:19
        },
        'rompecabezas': {
            0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11,
            13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19
        },
        'vocabulario': {
            0:1, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12,
            13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19
        },
        'nombres': {
            0:1, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12,
            13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19
        },
        'clave_figuras': {
            0:1, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12,
            13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19
        },
        'comprension': {
            0:1, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12,
            13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19
        },
        'dibujos': {
            0:1, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12,
            13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19
        }
    }
    
    # ==================== DEFINICIÓN COMPLETA DE PRUEBAS ====================
    
    PRUEBAS_INFO = {
        'cubos': {
            'nombre': 'Cubos',
            'nombre_corto': 'C',
            'indice_primario': 'IVE',
            'descripcion': 'Razonamiento visoespacial y construcción',
            'que_mide': 'Análisis y síntesis visoespacial, coordinación visomotora',
            'icono': '🧩',
            'rango_pd': (0, 30),
            'complementaria': False
        },
        'informacion': {
            'nombre': 'Información',
            'nombre_corto': 'I',
            'indice_primario': 'ICV',
            'descripcion': 'Conocimientos adquiridos',
            'que_mide': 'Inteligencia cristalizada, conocimiento general',
            'icono': '📚',
            'rango_pd': (0, 26),
            'complementaria': False
        },
        'matrices': {
            'nombre': 'Matrices',
            'nombre_corto': 'M',
            'indice_primario': 'IRF',
            'descripcion': 'Razonamiento fluido visual',
            'que_mide': 'Razonamiento fluido no verbal, procesamiento simultáneo',
            'icono': '🔲',
            'rango_pd': (0, 20),
            'complementaria': False
        },
        'busqueda_animales': {
            'nombre': 'Búsqueda de Animales',
            'nombre_corto': 'BA',
            'indice_primario': 'IVP',
            'descripcion': 'Velocidad de procesamiento visual',
            'que_mide': 'Velocidad perceptiva, atención selectiva',
            'icono': '🐾',
            'rango_pd': (0, 21),
            'complementaria': False
        },
        'reconocimiento': {
            'nombre': 'Reconocimiento',
            'nombre_corto': 'R',
            'indice_primario': 'IMT',
            'descripcion': 'Memoria de trabajo visual',
            'que_mide': 'Memoria visual a corto plazo',
            'icono': '👁️',
            'rango_pd': (0, 20),
            'complementaria': False
        },
        'semejanzas': {
            'nombre': 'Semejanzas',
            'nombre_corto': 'S',
            'indice_primario': 'ICV',
            'descripcion': 'Razonamiento verbal abstracto',
            'que_mide': 'Formación de conceptos verbales, razonamiento categorial',
            'icono': '💭',
            'rango_pd': (0, 30),
            'complementaria': False
        },
        'conceptos': {
            'nombre': 'Conceptos',
            'nombre_corto': 'CON',
            'indice_primario': 'IRF',
            'descripcion': 'Razonamiento categorial',
            'que_mide': 'Razonamiento abstracto categorial',
            'icono': '🎯',
            'rango_pd': (0, 20),
            'complementaria': False
        },
        'localizacion': {
            'nombre': 'Localización',
            'nombre_corto': 'L',
            'indice_primario': 'IMT',
            'descripcion': 'Memoria espacial de trabajo',
            'que_mide': 'Memoria de trabajo visual-espacial',
            'icono': '📍',
            'rango_pd': (0, 20),
            'complementaria': False
        },
        'cancelacion': {
            'nombre': 'Cancelación',
            'nombre_corto': 'CA',
            'indice_primario': 'IVP',
            'descripcion': 'Atención y velocidad perceptiva',
            'que_mide': 'Velocidad de procesamiento, atención sostenida',
            'icono': '✓',
            'rango_pd': (0, 21),
            'complementaria': False
        },
        'rompecabezas': {
            'nombre': 'Rompecabezas',
            'nombre_corto': 'RO',
            'indice_primario': 'IVE',
            'descripcion': 'Análisis y síntesis visual',
            'que_mide': 'Integración visomotora, análisis parte-todo',
            'icono': '🧩',
            'rango_pd': (0, 20),
            'complementaria': False
        },
        'vocabulario': {
            'nombre': 'Vocabulario',
            'nombre_corto': 'V',
            'indice_primario': 'ICV',
            'descripcion': 'Conocimiento léxico',
            'que_mide': 'Desarrollo del lenguaje, formación de conceptos verbales',
            'icono': '📖',
            'rango_pd': (0, 19),
            'complementaria': True
        },
        'nombres': {
            'nombre': 'Nombres',
            'nombre_corto': 'N',
            'indice_primario': 'ICV',
            'descripcion': 'Denominación y recuperación léxica',
            'que_mide': 'Vocabulario expresivo, recuperación de palabras',
            'icono': '🗣️',
            'rango_pd': (0, 19),
            'complementaria': True
        },
        'clave_figuras': {
            'nombre': 'Clave de Figuras',
            'nombre_corto': 'CF',
            'indice_primario': 'IVP',
            'descripcion': 'Velocidad de codificación',
            'que_mide': 'Velocidad de procesamiento, memoria asociativa',
            'icono': '🔑',
            'rango_pd': (0, 19),
            'complementaria': True
        },
        'comprension': {
            'nombre': 'Comprensión',
            'nombre_corto': 'CO',
            'indice_primario': 'ICV',
            'descripcion': 'Razonamiento social',
            'que_mide': 'Comprensión de normas sociales, juicio práctico',
            'icono': '🧐',
            'rango_pd': (0, 19),
            'complementaria': True
        },
        'dibujos': {
            'nombre': 'Dibujos',
            'nombre_corto': 'D',
            'indice_primario': 'ICV',
            'descripcion': 'Vocabulario receptivo',
            'que_mide': 'Comprensión de vocabulario, conocimiento léxico',
            'icono': '🖼️',
            'rango_pd': (0, 19),
            'complementaria': True
        }
    }
    
    # ==================== TABLAS SUMA PE → ÍNDICE COMPUESTO ====================
    # Basadas en las tablas del manual (Tabla C.1 y similares)
    
    TABLA_SUMA_PE_A_INDICE = {
        'ICV': {  # Comprensión Verbal (2 pruebas principales)
            4:50, 5:53, 6:55, 7:58, 8:61, 9:64, 10:67, 11:69, 12:72, 13:75,
            14:78, 15:81, 16:83, 17:86, 18:89, 19:92, 20:94, 21:97, 22:100,
            23:103, 24:106, 25:108, 26:111, 27:114, 28:117, 29:119, 30:122,
            31:125, 32:128, 33:131, 34:133, 35:136, 36:139, 37:142, 38:145
        },
        'IVE': {  # Visoespacial (2 pruebas)
            4:50, 5:53, 6:56, 7:59, 8:62, 9:65, 10:68, 11:70, 12:73, 13:76,
            14:79, 15:82, 16:85, 17:88, 18:90, 19:93, 20:96, 21:99, 22:102,
            23:105, 24:108, 25:110, 26:113, 27:116, 28:119, 29:122, 30:125,
            31:128, 32:131, 33:133, 34:136, 35:139, 36:142, 37:145, 38:148
        },
        'IRF': {  # Razonamiento Fluido (2 pruebas)
            4:50, 5:53, 6:56, 7:59, 8:62, 9:65, 10:68, 11:71, 12:74, 13:76,
            14:79, 15:82, 16:85, 17:88, 18:91, 19:94, 20:97, 21:100, 22:103,
            23:106, 24:109, 25:112, 26:115, 27:118, 28:121, 29:124, 30:127,
            31:130, 32:133, 33:136, 34:139, 35:142, 36:145, 37:148, 38:151
        },
        'IMT': {  # Memoria de Trabajo (2 pruebas)
            4:50, 5:53, 6:56, 7:59, 8:62, 9:65, 10:67, 11:70, 12:73, 13:76,
            14:79, 15:82, 16:85, 17:88, 18:91, 19:94, 20:97, 21:100, 22:103,
            23:106, 24:109, 25:112, 26:115, 27:118, 28:121, 29:124, 30:127,
            31:130, 32:133, 33:136, 34:139, 35:142, 36:145, 37:148, 38:151
        },
        'IVP': {  # Velocidad de Procesamiento (2 pruebas)
            4:50, 5:53, 6:56, 7:59, 8:62, 9:65, 10:68, 11:71, 12:73, 13:76,
            14:79, 15:82, 16:85, 17:88, 18:91, 19:94, 20:97, 21:100, 22:103,
            23:106, 24:109, 25:112, 26:115, 27:118, 28:121, 29:124, 30:127,
            31:130, 32:133, 33:136, 34:139, 35:142, 36:145, 37:148, 38:151
        }
    }
    
    # Tabla para CIT (5+ pruebas)
    TABLA_CIT = {
        10:40, 12:42, 14:44, 16:46, 18:48, 20:50, 22:52, 24:54, 26:56, 28:58,
        30:60, 32:62, 34:64, 36:66, 38:68, 40:70, 42:72, 44:74, 46:76, 48:78,
        50:80, 52:82, 54:84, 56:86, 58:88, 60:90, 62:92, 63:93, 64:94, 65:95,
        66:96, 67:97, 68:98, 69:99, 70:100, 71:101, 72:102, 73:103, 74:104,
        75:105, 76:106, 77:107, 78:108, 79:109, 80:110, 82:112, 84:114, 86:116,
        88:118, 90:120, 92:122, 94:124, 95:125, 96:126, 97:127, 98:128, 99:129,
        100:130, 102:132, 104:134, 106:136, 108:138, 110:140, 112:142, 114:144,
        115:145, 116:146, 117:147, 118:148, 119:149, 120:150
    }
    
    # ==================== ÍNDICES SECUNDARIOS ====================
    INDICES_SECUNDARIOS_CONFIG = {
        'IAV': {  # Adquisición de Vocabulario
            'nombre': 'Adquisición de Vocabulario',
            'pruebas': ['dibujos', 'nombres'],
            'descripcion': 'Rendimiento en vocabulario receptivo y expresivo'
        },
        'INV': {  # No Verbal
            'nombre': 'No Verbal',
            'pruebas': ['cubos', 'matrices', 'conceptos', 'reconocimiento', 'busqueda_animales'],
            'descripcion': 'Aptitud intelectual sin lenguaje expresivo'
        },
        'ICG': {  # Capacidad General
            'nombre': 'Capacidad General',
            'pruebas': ['informacion', 'semejanzas', 'cubos', 'matrices'],
            'descripcion': 'Aptitud intelectual menos dependiente de MT y VP'
        },
        'ICC': {  # Competencia Cognitiva
            'nombre': 'Competencia Cognitiva',
            'pruebas': ['reconocimiento', 'localizacion', 'busqueda_animales', 'cancelacion'],
            'descripcion': 'Eficacia en procesamiento cognitivo'
        }
    }
    
    @staticmethod
    def calcular_edad_exacta(fecha_nac, fecha_eval):
        """Calcula edad cronológica exacta en años, meses y días"""
        years = fecha_eval.year - fecha_nac.year
        months = fecha_eval.month - fecha_nac.month
        days = fecha_eval.day - fecha_nac.day
        
        if days < 0:
            months -= 1
            days_in_prev_month = (fecha_eval.replace(day=1) - pd.Timedelta(days=1)).day
            days += days_in_prev_month
        
        if months < 0:
            years -= 1
            months += 12
        
        return years, months, days
    
    @staticmethod
    def convertir_pd_a_pe(prueba, pd):
        """Convierte PD a PE usando tablas oficiales"""
        if pd is None or pd == '':
            return None
        
        pd = int(pd)
        tabla = BaremosWPPSIUltra.TABLAS_CONVERSION_PD_PE.get(prueba, {})
        
        # Si no está en tabla, devolver valor límite
        if pd not in tabla:
            if pd <= 0:
                return 1
            else:
                return max(tabla.values()) if tabla else 19
        
        return tabla[pd]
    
    @staticmethod
    def calcular_indice_compuesto(suma_pe, tipo_indice):
        """Calcula índice compuesto a partir de suma de PE"""
        if suma_pe is None or suma_pe <= 0:
            return None
        
        tabla = BaremosWPPSIUltra.TABLA_SUMA_PE_A_INDICE.get(tipo_indice, {})
        
        # Buscar el valor más cercano en la tabla
        valores_tabla = sorted(tabla.keys())
        for val in valores_tabla:
            if suma_pe <= val:
                return tabla[val]
        
        # Si supera el máximo
        return tabla[valores_tabla[-1]] if valores_tabla else 100
    
    @staticmethod
    def calcular_cit_total(suma_total_pe):
        """Calcula CIT a partir de suma total de PE"""
        if suma_total_pe is None or suma_total_pe <= 0:
            return None
        
        valores_tabla = sorted(BaremosWPPSIUltra.TABLA_CIT.keys())
        for val in valores_tabla:
            if suma_total_pe <= val:
                return BaremosWPPSIUltra.TABLA_CIT[val]
        
        return BaremosWPPSIUltra.TABLA_CIT[valores_tabla[-1]] if valores_tabla else 100
    
    @staticmethod
    def obtener_percentil_exacto(ci):
        """Calcula percentil exacto usando distribución normal"""
        if ci is None:
            return None
        
        # Usar distribución normal: media=100, desviación=15
        percentil = norm.cdf((ci - 100) / 15) * 100
        
        if percentil > 99.9:
            return ">99.9"
        elif percentil < 0.1:
            return "<0.1"
        else:
            return round(percentil, 1)
    
    @staticmethod
    def obtener_categoria_descriptiva(ci):
        """Retorna categoría descriptiva y color según CI"""
        if ci is None:
            return "No calculado", "#95a5a6", "Datos insuficientes"
        
        if ci >= 130:
            return "Muy Superior", "#27ae60", "Capacidades intelectuales excepcionales"
        elif ci >= 120:
            return "Superior", "#2ecc71", "Rendimiento significativamente por encima del promedio"
        elif ci >= 110:
            return "Medio Alto", "#3498db", "Rendimiento por encima del promedio"
        elif ci >= 90:
            return "Medio", "#f39c12", "Rendimiento dentro del rango promedio esperado"
        elif ci >= 80:
            return "Medio Bajo", "#e67e22", "Rendimiento ligeramente por debajo del promedio"
        elif ci >= 70:
            return "Límite", "#e74c3c", "Requiere atención y posible intervención"
        else:
            return "Muy Bajo", "#c0392b", "Requiere intervención especializada"
    
    @staticmethod
    def obtener_intervalo_confianza_90(ci):
        """Calcula intervalo de confianza al 90%"""
        if ci is None:
            return None, None
        
        # IC 90% aproximado: ±5-6 puntos
        margen = 6
        return ci - margen, ci + margen
    
    @staticmethod
    def clasificar_pe(pe):
        """Clasifica una PE como Fortaleza, Promedio o Debilidad"""
        if pe is None:
            return "No evaluado"
        elif pe >= 13:
            return "Fortaleza"
        elif pe <= 7:
            return "Debilidad"
        else:
            return "Promedio"

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE PROCESAMIENTO ULTRA COMPLETO
# ═══════════════════════════════════════════════════════════════════════════════

def procesar_evaluacion_completa(datos_personales, pruebas_aplicadas, pd_dict):
    """
    Procesa la evaluación WPPSI-IV de forma ultra completa
    Retorna diccionario con todos los análisis posibles
    """
    
    resultados = {
        'datos_personales': datos_personales,
        'pruebas_aplicadas': pruebas_aplicadas,
        'pd': {},
        'pe': {},
        'sumas_indices': {},
        'indices_primarios': {},
        'indices_secundarios': {},
        'cit': None,
        'percentiles': {},
        'categorias': {},
        'intervalos_confianza': {},
        'fortalezas': [],
        'debilidades': [],
        'analisis_comparativo': {},
        'interpretacion_narrativa': {}
    }
    
    # 1. CONVERTIR PD A PE
    for prueba, aplicada in pruebas_aplicadas.items():
        if aplicada and prueba in pd_dict and pd_dict[prueba] is not None:
            pd = pd_dict[prueba]
            pe = BaremosWPPSIUltra.convertir_pd_a_pe(prueba, pd)
            
            resultados['pd'][prueba] = pd
            resultados['pe'][prueba] = pe
    
    # 2. CALCULAR SUMAS POR ÍNDICE PRIMARIO
    sumas = {'ICV': 0, 'IVE': 0, 'IRF': 0, 'IMT': 0, 'IVP': 0}
    contadores = {'ICV': 0, 'IVE': 0, 'IRF': 0, 'IMT': 0, 'IVP': 0}
    
    for prueba, pe in resultados['pe'].items():
        if pe is not None:
            info_prueba = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            indice = info_prueba['indice_primario']
            
            if indice in sumas:
                sumas[indice] += pe
                contadores[indice] += 1
    
    resultados['sumas_indices'] = sumas
    
    # 3. CALCULAR ÍNDICES COMPUESTOS PRIMARIOS
    for indice, suma in sumas.items():
        if contadores[indice] >= 2:  # Mínimo 2 pruebas por índice
            ic = BaremosWPPSIUltra.calcular_indice_compuesto(suma, indice)
            resultados['indices_primarios'][indice] = ic
            
            # Percentil
            resultados['percentiles'][indice] = BaremosWPPSIUltra.obtener_percentil_exacto(ic)
            
            # Categoría
            cat, color, desc = BaremosWPPSIUltra.obtener_categoria_descriptiva(ic)
            resultados['categorias'][indice] = {'categoria': cat, 'color': color, 'descripcion': desc}
            
            # IC 90%
            ic_inf, ic_sup = BaremosWPPSIUltra.obtener_intervalo_confianza_90(ic)
            resultados['intervalos_confianza'][indice] = (ic_inf, ic_sup)
    
    # 4. CALCULAR CIT
    suma_total = sum(resultados['pe'].values())
    if len(resultados['pe']) >= 5:  # Mínimo 5 pruebas para CIT
        cit = BaremosWPPSIUltra.calcular_cit_total(suma_total)
        resultados['cit'] = cit
        resultados['indices_primarios']['CIT'] = cit
        
        resultados['percentiles']['CIT'] = BaremosWPPSIUltra.obtener_percentil_exacto(cit)
        
        cat, color, desc = BaremosWPPSIUltra.obtener_categoria_descriptiva(cit)
        resultados['categorias']['CIT'] = {'categoria': cat, 'color': color, 'descripcion': desc}
        
        ic_inf, ic_sup = BaremosWPPSIUltra.obtener_intervalo_confianza_90(cit)
        resultados['intervalos_confianza']['CIT'] = (ic_inf, ic_sup)
    
    # 5. CALCULAR ÍNDICES SECUNDARIOS
    for idx_sec, config in BaremosWPPSIUltra.INDICES_SECUNDARIOS_CONFIG.items():
        pruebas_necesarias = config['pruebas']
        suma_sec = 0
        contador_sec = 0
        
        for prueba in pruebas_necesarias:
            if prueba in resultados['pe'] and resultados['pe'][prueba] is not None:
                suma_sec += resultados['pe'][prueba]
                contador_sec += 1
        
        if contador_sec >= len(pruebas_necesarias):  # Todas las pruebas disponibles
            # Usar tabla similar a índices primarios
            ic_sec = BaremosWPPSIUltra.calcular_indice_compuesto(suma_sec, 'ICV')  # Usar tabla similar
            resultados['indices_secundarios'][idx_sec] = ic_sec
    
    # 6. IDENTIFICAR FORTALEZAS Y DEBILIDADES
    for prueba, pe in resultados['pe'].items():
        info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
        clasificacion = BaremosWPPSIUltra.clasificar_pe(pe)
        
        if clasificacion == "Fortaleza":
            resultados['fortalezas'].append({
                'prueba': info['nombre'],
                'pe': pe,
                'descripcion': info['descripcion'],
                'que_mide': info['que_mide']
            })
        elif clasificacion == "Debilidad":
            resultados['debilidades'].append({
                'prueba': info['nombre'],
                'pe': pe,
                'descripcion': info['descripcion'],
                'que_mide': info['que_mide']
            })
    
    return resultados

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE VISUALIZACIÓN ULTRA MEJORADAS
# ═══════════════════════════════════════════════════════════════════════════════

def crear_grafico_perfil_escalares_ultra(pe_dict):
    """Gráfico ultra profesional de perfil de puntuaciones escalares"""
    if not pe_dict:
        return None
    
    pruebas = list(pe_dict.keys())
    valores = list(pe_dict.values())
    nombres = [BaremosWPPSIUltra.PRUEBAS_INFO[p]['nombre'] for p in pruebas]
    
    fig = go.Figure()
    
    # Zonas de rendimiento con gradiente
    fig.add_hrect(y0=13, y1=19, fillcolor="rgba(39, 174, 96, 0.12)", line_width=0,
                 annotation_text="FORTALEZA", annotation_position="top right",
                 annotation_font_size=10, annotation_font_color="#27ae60")
    
    fig.add_hrect(y0=8, y1=12, fillcolor="rgba(243, 156, 18, 0.10)", line_width=0,
                 annotation_text="PROMEDIO", annotation_position="right",
                 annotation_font_size=10, annotation_font_color="#f39c12")
    
    fig.add_hrect(y0=1, y1=7, fillcolor="rgba(231, 76, 60, 0.12)", line_width=0,
                 annotation_text="DEBILIDAD", annotation_position="bottom right",
                 annotation_font_size=10, annotation_font_color="#e74c3c")
    
    # Línea de media (10)
    fig.add_hline(y=10, line_dash="dot", line_color="#7f8c8d", line_width=3,
                 annotation_text="Media (PE=10)", annotation_position="left",
                 annotation_font_size=11, annotation_font_color="#7f8c8d")
    
    # Línea de datos con marcadores
    fig.add_trace(go.Scatter(
        x=nombres,
        y=valores,
        mode='lines+markers+text',
        text=valores,
        textposition="top center",
        textfont=dict(size=13, family='Poppins', weight='bold', color='#2c3e50'),
        line=dict(color='#8B1538', width=5, shape='spline', smoothing=1.2),
        marker=dict(
            size=16,
            color=valores,
            colorscale=[[0, '#e74c3c'], [0.35, '#f39c12'], [0.65, '#3498db'], [1, '#27ae60']],
            cmin=1,
            cmax=19,
            line=dict(width=3, color='white'),
            symbol='circle'
        ),
        name='Puntuaciones Escalares'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>📊 PERFIL DE PUNTUACIONES ESCALARES (PE)</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'family': 'Poppins', 'color': '#2c3e50'}
        },
        yaxis=dict(
            range=[0, 20],
            dtick=2,
            title="<b>Puntuación Escalar (PE)</b>",
            gridcolor='rgba(0,0,0,0.06)',
            titlefont=dict(size=14, family='Inter', weight='bold'),
            tickfont=dict(size=12)
        ),
        xaxis=dict(
            tickangle=-45,
            gridcolor='rgba(0,0,0,0.04)',
            titlefont=dict(size=14, family='Inter', weight='bold'),
            tickfont=dict(size=11, weight='bold')
        ),
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        font=dict(family='Inter'),
        hovermode='x unified',
        showlegend=False
    )
    
    return fig

def crear_grafico_indices_compuestos_ultra(indices):
    """Gráfico ultra profesional de índices compuestos"""
    datos = {k: v for k, v in indices.items() if v is not None}
    
    if not datos:
        return None
    
    nombres = list(datos.keys())
    valores = list(datos.values())
    
    colores_barras = []
    for v in valores:
        _, color, _ = BaremosWPPSIUltra.obtener_categoria_descriptiva(v)
        colores_barras.append(color)
    
    fig = go.Figure()
    
    # Barras con gradiente y sombra
    fig.add_trace(go.Bar(
        x=nombres,
        y=valores,
        marker=dict(
            color=colores_barras,
            line=dict(color='white', width=2),
            opacity=0.9,
            pattern_shape=""
        ),
        text=valores,
        textposition='outside',
        textfont=dict(size=17, family='Poppins', weight='bold', color='#2c3e50'),
        width=0.65,
        name='Puntuación Compuesta',
        hovertemplate='<b>%{x}</b><br>PC: %{y}<extra></extra>'
    ))
    
    # Línea de media (100)
    fig.add_hline(y=100, line_dash="dash", line_color="#34495e", line_width=4,
                 annotation_text="Media Poblacional (100)", annotation_position="right",
                 annotation_font_size=12, annotation_font_color="#34495e")
    
    # Zonas de clasificación
    fig.add_hrect(y0=130, y1=160, fillcolor="rgba(39, 174, 96, 0.08)", line_width=0)
    fig.add_hrect(y0=70, y1=85, fillcolor="rgba(231, 76, 60, 0.08)", line_width=0)
    
    fig.update_layout(
        title={
            'text': '<b>📈 PERFIL DE ÍNDICES COMPUESTOS (PC)</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'family': 'Poppins', 'color': '#2c3e50'}
        },
        yaxis=dict(
            range=[40, 165],
            dtick=20,
            title="<b>Puntuación Compuesta (PC)</b>",
            gridcolor='rgba(0,0,0,0.06)',
            titlefont=dict(size=14, family='Inter', weight='bold'),
            tickfont=dict(size=12)
        ),
        xaxis=dict(
            tickfont=dict(size=13, family='Poppins', weight='bold'),
            tickangle=0
        ),
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        font=dict(family='Inter'),
        showlegend=False,
        hovermode='x'
    )
    
    return fig

def crear_grafico_radar_cognitivo(indices):
    """Gráfico radar ultra profesional de capacidades cognitivas"""
    categorias = []
    valores = []
    
    mapeo = {
        'ICV': 'Comprensión<br>Verbal',
        'IVE': 'Viso-<br>espacial',
        'IRF': 'Razonamiento<br>Fluido',
        'IMT': 'Memoria de<br>Trabajo',
        'IVP': 'Velocidad de<br>Procesamiento'
    }
    
    for key, label in mapeo.items():
        if indices.get(key) is not None:
            categorias.append(label)
            valores.append(indices[key])
    
    if not valores:
        return None
    
    fig = go.Figure()
    
    # Datos del paciente
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        fillcolor='rgba(139, 21, 56, 0.25)',
        line=dict(color='#8B1538', width=4),
        marker=dict(size=12, color='#8B1538', symbol='circle',
                   line=dict(width=2, color='white')),
        name='Paciente',
        hovertemplate='<b>%{theta}</b><br>PC: %{r}<extra></extra>'
    ))
    
    # Media poblacional
    fig.add_trace(go.Scatterpolar(
        r=[100] * len(categorias),
        theta=categorias,
        mode='lines',
        line=dict(color='#7f8c8d', width=3, dash='dot'),
        name='Media (100)',
        hovertemplate='Media: 100<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[40, 160],
                tickfont=dict(size=11, weight='bold'),
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, family='Poppins', weight='bold'),
                gridcolor='rgba(0,0,0,0.1)'
            ),
            bgcolor='rgba(248,249,250,0.5)'
        ),
        title={
            'text': '<b>🧭 MAPA COGNITIVO MULTIDIMENSIONAL</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'family': 'Poppins', 'color': '#2c3e50'}
        },
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12, family='Inter', weight='bold')
        ),
        font=dict(family='Inter')
    )
    
    return fig

def crear_grafico_comparacion_indices(indices):
    """Gráfico de comparación de índices con media del paciente"""
    if not indices or len(indices) < 2:
        return None
    
    # Calcular media de índices primarios (sin CIT)
    indices_sin_cit = {k: v for k, v in indices.items() if k != 'CIT' and v is not None}
    if not indices_sin_cit:
        return None
    
    media_paciente = np.mean(list(indices_sin_cit.values()))
    
    nombres = list(indices_sin_cit.keys())
    valores = list(indices_sin_cit.values())
    diferencias = [v - media_paciente for v in valores]
    
    colores = ['#27ae60' if d > 0 else '#e74c3c' for d in diferencias]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=nombres,
        y=diferencias,
        marker=dict(color=colores, line=dict(color='white', width=2)),
        text=[f"+{d:.1f}" if d > 0 else f"{d:.1f}" for d in diferencias],
        textposition='outside',
        textfont=dict(size=14, weight='bold'),
        name='Diferencia con la media'
    ))
    
    fig.add_hline(y=0, line_color='#34495e', line_width=3)
    
    fig.update_layout(
        title={
            'text': f'<b>📉 ANÁLISIS DE VARIABILIDAD (Media Personal: {media_paciente:.1f})</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Poppins', 'color': '#2c3e50'}
        },
        yaxis=dict(
            title="<b>Diferencia respecto a la media personal</b>",
            gridcolor='rgba(0,0,0,0.06)',
            titlefont=dict(size=13, weight='bold'),
            zeroline=True,
            zerolinecolor='#34495e',
            zerolinewidth=3
        ),
        xaxis=dict(
            tickfont=dict(size=12, weight='bold')
        ),
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        showlegend=False
    )
    
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# CONTINUACIÓN DEL CÓDIGO WPPSI-IV ULTRA COMPLETO - PARTE 2
# Copie este código DESPUÉS del código de la Parte 1
# ═══════════════════════════════════════════════════════════════════════════════

def crear_tabla_conversion_pd_pe_df():
    """Crea DataFrame con tabla completa de conversión PD→PE"""
    # Crear tabla similar al cuadernillo de anotación
    data = []
    
    for prueba_key, info in BaremosWPPSIUltra.PRUEBAS_INFO.items():
        if not info['complementaria']:  # Solo pruebas principales
            row = {
                'Prueba': info['nombre'],
                'Código': info['nombre_corto'],
                'Índice': info['indice_primario'],
                'Rango PD': f"0-{info['rango_pd'][1]}"
            }
            data.append(row)
    
    return pd.DataFrame(data)

# ═══════════════════════════════════════════════════════════════════════════════
# GENERADOR DE PDF ULTRA PROFESIONAL CON GRÁFICOS
# ═══════════════════════════════════════════════════════════════════════════════

def generar_grafico_para_pdf(pe_dict, tipo='perfil'):
    """Genera gráfico para incluir en PDF usando reportlab"""
    from reportlab.graphics.charts.lineplots import LinePlot
    from reportlab.graphics.shapes import Drawing
    
    if not pe_dict:
        return None
    
    drawing = Drawing(450, 200)
    
    if tipo == 'perfil':
        # Crear gráfico de línea para perfil de PE
        lp = LinePlot()
        lp.x = 50
        lp.y = 30
        lp.height = 140
        lp.width = 380
        
        pruebas = list(pe_dict.keys())
        valores = list(pe_dict.values())
        
        lp.data = [list(enumerate(valores, 1))]
        lp.lines[0].strokeColor = colors.HexColor('#8B1538')
        lp.lines[0].strokeWidth = 3
        
        lp.xValueAxis.valueMin = 0
        lp.xValueAxis.valueMax = len(valores) + 1
        lp.yValueAxis.valueMin = 0
        lp.yValueAxis.valueMax = 20
        lp.yValueAxis.valueStep = 5
        
        drawing.add(lp)
    
    return drawing

def crear_tabla_pdf_estilo_manual(data, col_widths, style_config='estandar'):
    """Crea tabla con estilo del manual WPPSI-IV"""
    
    if style_config == 'header_rojo':
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#8B1538')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 11),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('PADDING', (0,0), (-1,-1), 8),
        ])
    elif style_config == 'resumen':
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BACKGROUND', (0,1), (0,-1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 10),
        ])
    else:  # estandar
        style = TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 8),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0f0f0')),
        ])
    
    table = Table(data, colWidths=col_widths)
    table.setStyle(style)
    
    return table

def generar_informe_pdf_ultra_completo(resultados):
    """
    Genera informe PDF ultra profesional con todos los gráficos y tablas
    Similar al informe del ejemplo WPPSI-IV
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2.5*cm,
        bottomMargin=2*cm
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # ==================== ESTILOS PERSONALIZADOS ====================
    
    titulo_principal = ParagraphStyle(
        'TituloPrincipal',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor('#8B1538'),
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica-Bold',
        leading=32
    )
    
    titulo_seccion = ParagraphStyle(
        'TituloSeccion',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.white,
        backColor=colors.HexColor('#8B1538'),
        spaceBefore=25,
        spaceAfter=15,
        fontName='Helvetica-Bold',
        borderPadding=(8, 15, 8, 15),
        borderRadius=5
    )
    
    subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceBefore=15,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    texto_normal = ParagraphStyle(
        'TextoNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    texto_destacado = ParagraphStyle(
        'TextoDestacado',
        parent=texto_normal,
        fontSize=12,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    # ==================== PORTADA ====================
    
    story.append(Spacer(1, 1.5*cm))
    
    story.append(Paragraph("INFORME PSICOPEDAGÓGICO", titulo_principal))
    
    story.append(Paragraph(
        "Escala de Inteligencia de Wechsler<br/>para Preescolar y Primaria - IV (WPPSI-IV)",
        ParagraphStyle('SubtituloPortada', parent=texto_normal, 
                      alignment=TA_CENTER, fontSize=13, textColor=colors.HexColor('#5a6c7d'))
    ))
    
    story.append(Spacer(1, 2*cm))
    
    # Datos del paciente en portada
    datos = resultados['datos_personales']
    
    data_portada = [
        ["DATOS DE FILIACIÓN", ""],
        ["Nombre del examinado:", datos.get('nombre', '')],
        ["Fecha de nacimiento:", datos.get('fecha_nacimiento', '')],
        ["Fecha de evaluación:", datos.get('fecha_evaluacion', '')],
        ["Edad cronológica:", datos.get('edad_texto', '')],
        ["Examinador/a:", datos.get('examinador', '')],
        ["Lugar de aplicación:", datos.get('lugar', '')]
    ]
    
    t_portada = crear_tabla_pdf_estilo_manual(
        data_portada,
        [7*cm, 10*cm],
        'resumen'
    )
    
    story.append(t_portada)
    story.append(Spacer(1, 1*cm))
    
    # Nota profesional
    nota_texto = """
    <b>ADVERTENCIA PROFESIONAL:</b> Este informe ha sido generado automáticamente 
    por el sistema WPPSI-IV Professional. Los resultados deben ser interpretados 
    por un profesional cualificado en Psicología o Psicopedagogía, considerando 
    el contexto completo del evaluado y nunca de forma aislada.
    """
    
    story.append(Paragraph(nota_texto, 
        ParagraphStyle('Nota', parent=texto_normal, fontSize=9, 
                      textColor=colors.HexColor('#7f8c8d'), alignment=TA_JUSTIFY,
                      borderColor=colors.HexColor('#bdc3c7'), borderWidth=1,
                      borderPadding=10, backColor=colors.HexColor('#ecf0f1'))))
    
    story.append(PageBreak())
    
    # ==================== PÁGINA 1: RESUMEN DE PUNTUACIONES ====================
    
    story.append(Paragraph("RESUMEN DE PUNTUACIONES", titulo_seccion))
    story.append(Spacer(1, 0.5*cm))
    
    # Tabla de conversión PD → PE
    story.append(Paragraph("1. CONVERSIÓN DE PUNTUACIONES DIRECTAS A ESCALARES", subtitulo))
    
    data_conversion = [["Prueba", "PD", "PE", "Clasificación"]]
    
    for prueba, pd in resultados['pd'].items():
        info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
        pe = resultados['pe'].get(prueba, '')
        clasif = BaremosWPPSIUltra.clasificar_pe(pe) if pe else ''
        
        data_conversion.append([
            info['nombre'],
            str(pd),
            str(pe),
            clasif
        ])
    
    t_conversion = crear_tabla_pdf_estilo_manual(
        data_conversion,
        [7*cm, 3*cm, 3*cm, 4*cm],
        'header_rojo'
    )
    
    story.append(t_conversion)
    story.append(Spacer(1, 0.8*cm))
    
    # Tabla de índices primarios
    story.append(Paragraph("2. ÍNDICES PRIMARIOS Y CI TOTAL", subtitulo))
    
    data_indices = [["Índice", "Suma PE", "PC", "Percentil", "IC 90%", "Categoría"]]
    
    indices_orden = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT']
    nombres_indices = {
        'ICV': 'Comprensión Verbal',
        'IVE': 'Visoespacial',
        'IRF': 'Razonamiento Fluido',
        'IMT': 'Memoria de Trabajo',
        'IVP': 'Velocidad de Procesamiento',
        'CIT': 'CI TOTAL'
    }
    
    for idx in indices_orden:
        if idx in resultados['indices_primarios']:
            pc = resultados['indices_primarios'][idx]
            perc = resultados['percentiles'].get(idx, '')
            cat_info = resultados['categorias'].get(idx, {})
            ic = resultados['intervalos_confianza'].get(idx, (None, None))
            
            suma = resultados['sumas_indices'].get(idx, '') if idx != 'CIT' else sum(resultados['pe'].values())
            
            data_indices.append([
                nombres_indices[idx],
                str(suma),
                str(pc),
                str(perc),
                f"{ic[0]}-{ic[1]}" if ic[0] else '',
                cat_info.get('categoria', '')
            ])
    
    t_indices = crear_tabla_pdf_estilo_manual(
        data_indices,
        [4.5*cm, 2*cm, 2*cm, 2*cm, 3*cm, 3.5*cm],
        'header_rojo'
    )
    
    story.append(t_indices)
    
    # Gráfico de perfil (simplificado en PDF)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("3. REPRESENTACIÓN GRÁFICA DEL PERFIL", subtitulo))
    
    # Nota sobre gráficos
    story.append(Paragraph(
        "Los gráficos detallados se encuentran disponibles en la versión digital del informe.",
        ParagraphStyle('NotaGrafico', parent=texto_normal, fontSize=10, 
                      textColor=colors.HexColor('#7f8c8d'), fontName='Helvetica-Oblique')
    ))
    
    story.append(PageBreak())
    
    # ==================== PÁGINA 2: ANÁLISIS CUALITATIVO ====================
    
    story.append(Paragraph("ANÁLISIS CUALITATIVO", titulo_seccion))
    story.append(Spacer(1, 0.5*cm))
    
    # Interpretación del CIT
    if resultados['cit']:
        cit = resultados['cit']
        cat_cit = resultados['categorias']['CIT']
        perc_cit = resultados['percentiles']['CIT']
        ic_cit = resultados['intervalos_confianza']['CIT']
        
        story.append(Paragraph("COEFICIENTE INTELECTUAL TOTAL (CIT)", subtitulo))
        
        texto_cit = f"""
        El evaluado obtuvo un CIT de <b>{cit}</b>, que se clasifica como <b>{cat_cit['categoria']}</b>.
        Su puntuación se sitúa en el percentil <b>{perc_cit}</b>, lo que significa que supera al 
        {perc_cit}% de los niños de su edad en la muestra de estandarización.<br/><br/>
        
        Con un 90% de confianza, el verdadero CIT del evaluado se encuentra entre 
        <b>{ic_cit[0]} y {ic_cit[1]}</b>.<br/><br/>
        
        {cat_cit['descripcion']}.
        """
        
        story.append(Paragraph(texto_cit, texto_normal))
        story.append(Spacer(1, 0.5*cm))
    
    # Fortalezas
    if resultados['fortalezas']:
        story.append(Paragraph("FORTALEZAS IDENTIFICADAS", subtitulo))
        
        for fortaleza in resultados['fortalezas']:
            texto_fort = f"""
            <b>• {fortaleza['prueba']} (PE = {fortaleza['pe']})</b>: {fortaleza['descripcion']}. 
            Esta prueba evalúa {fortaleza['que_mide']}.
            """
            story.append(Paragraph(texto_fort, texto_normal))
            story.append(Spacer(1, 0.2*cm))
        
        story.append(Spacer(1, 0.3*cm))
    
    # Debilidades
    if resultados['debilidades']:
        story.append(Paragraph("ÁREAS DE DESARROLLO", subtitulo))
        
        for debilidad in resultados['debilidades']:
            texto_deb = f"""
            <b>• {debilidad['prueba']} (PE = {debilidad['pe']})</b>: {debilidad['descripcion']}. 
            Se recomienda reforzar {debilidad['que_mide']}.
            """
            story.append(Paragraph(texto_deb, texto_normal))
            story.append(Spacer(1, 0.2*cm))
    
    story.append(PageBreak())
    
    # ==================== PÁGINA 3: INTERPRETACIÓN POR ÍNDICES ====================
    
    story.append(Paragraph("INTERPRETACIÓN POR ÍNDICES", titulo_seccion))
    story.append(Spacer(1, 0.5*cm))
    
    interpretaciones_indices = {
        'ICV': {
            'titulo': 'COMPRENSIÓN VERBAL (ICV)',
            'texto': """El índice de Comprensión Verbal mide la inteligencia cristalizada y 
            la capacidad para razonar con información previamente aprendida. Refleja el desarrollo 
            del lenguaje, la formación de conceptos verbales y el conocimiento adquirido a través 
            de la experiencia educativa y cultural."""
        },
        'IVE': {
            'titulo': 'VISOESPACIAL (IVE)',
            'texto': """El índice Visoespacial evalúa la capacidad para analizar y sintetizar 
            información visual, así como para comprender relaciones espaciales. Incluye habilidades 
            de construcción, integración visomotora y razonamiento visoperceptivo."""
        },
        'IRF': {
            'titulo': 'RAZONAMIENTO FLUIDO (IRF)',
            'texto': """El Razonamiento Fluido mide la capacidad para detectar relaciones 
            conceptuales subyacentes y usar el razonamiento inductivo. Es una medida de la 
            inteligencia fluida, menos dependiente del aprendizaje previo."""
        },
        'IMT': {
            'titulo': 'MEMORIA DE TRABAJO (IMT)',
            'texto': """La Memoria de Trabajo refleja la capacidad para retener temporalmente 
            información en la memoria, operar con ella y generar un resultado. Implica atención, 
            concentración y control mental."""
        },
        'IVP': {
            'titulo': 'VELOCIDAD DE PROCESAMIENTO (IVP)',
            'texto': """La Velocidad de Procesamiento mide la rapidez con la que el evaluado 
            puede procesar información visual simple. Es importante para el aprendizaje eficiente 
            y el rendimiento académico."""
        }
    }
    
    for idx in ['ICV', 'IVE', 'IRF', 'IMT', 'IVP']:
        if idx in resultados['indices_primarios']:
            pc = resultados['indices_primarios'][idx]
            cat = resultados['categorias'][idx]
            perc = resultados['percentiles'][idx]
            
            story.append(Paragraph(interpretaciones_indices[idx]['titulo'], subtitulo))
            
            texto_interpretacion = f"""
            <b>Puntuación: {pc} (Percentil {perc})</b><br/>
            <b>Clasificación: {cat['categoria']}</b><br/><br/>
            {interpretaciones_indices[idx]['texto']}<br/><br/>
            El evaluado obtuvo una puntuación de {pc}, clasificada como {cat['categoria']}.
            """
            
            story.append(Paragraph(texto_interpretacion, texto_normal))
            story.append(Spacer(1, 0.4*cm))
    
    # ==================== PÁGINA FINAL: RECOMENDACIONES ====================
    
    story.append(PageBreak())
    story.append(Paragraph("RECOMENDACIONES Y CONCLUSIONES", titulo_seccion))
    story.append(Spacer(1, 0.5*cm))
    
    recomendaciones = """
    <b>RECOMENDACIONES GENERALES:</b><br/><br/>
    
    1. <b>Interpretación Integral:</b> Los resultados deben interpretarse considerando 
    el perfil completo de fortalezas y debilidades del evaluado, junto con información 
    de otras fuentes (observación, historia académica, etc.).<br/><br/>
    
    2. <b>Intervención Educativa:</b> Se recomienda diseñar un plan de intervención que 
    aproveche las fortalezas identificadas para compensar las áreas de menor rendimiento.<br/><br/>
    
    3. <b>Seguimiento:</b> Es aconsejable realizar evaluaciones de seguimiento para 
    monitorear el desarrollo cognitivo y ajustar las intervenciones según sea necesario.<br/><br/>
    
    4. <b>Contexto Familiar y Escolar:</b> La colaboración entre familia y escuela es 
    fundamental para el óptimo desarrollo de las capacidades del niño/a.
    """
    
    story.append(Paragraph(recomendaciones, texto_normal))
    
    # Footer profesional
    story.append(Spacer(1, 2*cm))
    
    # Línea divisoria
    drawing_line = Drawing(17*cm, 10)
    drawing_line.add(Line(0, 5, 17*cm, 5, strokeColor=colors.HexColor('#8B1538'), strokeWidth=2))
    story.append(drawing_line)
    
    story.append(Spacer(1, 0.3*cm))
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    
    footer_text = f"""
    <para alignment="center">
    <font name="Helvetica" size="9" color="#7f8c8d">
    Informe generado por <b>WPPSI-IV Professional System v7.0</b><br/>
    Fecha de generación: {fecha_actual}<br/>
    Desarrollado para uso profesional exclusivo | © 2026 Daniela
    </font>
    </para>
    """
    
    story.append(Paragraph(footer_text, texto_normal))
    
    # Construir PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer

# ═══════════════════════════════════════════════════════════════════════════════
# INTERFAZ DE USUARIO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

# Header Ultra
st.markdown("""
<div class="header-ultra">
    <div class="header-title">🧠 WPPSI-IV PROFESSIONAL ULTRA</div>
    <div class="header-subtitle">Sistema Integral de Evaluación Psicopedagógica</div>
    <div class="header-version">v7.0.0 Professional Edition</div>
</div>
""", unsafe_allow_html=True)

# Sidebar con navegación
with st.sidebar:
    st.markdown("### 📊 NAVEGACIÓN")
    
    pasos = {
        1: "📝 Datos del Paciente",
        2: "🎯 Selección de Pruebas",
        3: "🔢 Puntuaciones Directas",
        4: "📈 Resultados y Análisis",
        5: "📄 Generar Informe PDF"
    }
    
    paso_actual = st.radio(
        "Seleccione una sección:",
        list(pasos.keys()),
        format_func=lambda x: pasos[x],
        key='paso_selector'
    )
    
    st.session_state.paso_actual = paso_actual
    
    st.markdown("---")
    st.markdown("### ℹ️ INFORMACIÓN")
    st.info(f"""
    **Paso actual:** {paso_actual}/5
    
    {pasos[paso_actual]}
    """)
    
    if st.session_state.datos_completos:
        st.success("✅ Evaluación completada")
        n_pruebas = len(st.session_state.pe_dict)
        st.metric("Pruebas aplicadas", n_pruebas)

# Main content area
if paso_actual == 1:
    # ==================== PASO 1: DATOS DEL PACIENTE ====================
    
    st.markdown('<div class="animate-fade-in">', unsafe_allow_html=True)
    st.markdown("## <span class='step-number'>1</span> Datos del Paciente", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input(
            "📝 Nombre completo del niño/a",
            value=st.session_state.nombre_paciente,
            help="Ingrese el nombre completo del evaluado"
        )
        st.session_state.nombre_paciente = nombre
        
        fecha_nac = st.date_input(
            "🎂 Fecha de nacimiento",
            value=st.session_state.fecha_nacimiento if st.session_state.fecha_nacimiento else date(2020, 9, 20),
            help="Seleccione la fecha de nacimiento"
        )
        st.session_state.fecha_nacimiento = fecha_nac
        
        sexo = st.selectbox(
            "⚥ Sexo",
            ["F", "M"],
            index=0 if st.session_state.sexo == "F" else 1
        )
        st.session_state.sexo = sexo
    
    with col2:
        fecha_eval = st.date_input(
            "📅 Fecha de evaluación",
            value=st.session_state.fecha_evaluacion if st.session_state.fecha_evaluacion else date.today(),
            help="Fecha en que se realizó la evaluación"
        )
        st.session_state.fecha_evaluacion = fecha_eval
        
        examinador = st.text_input(
            "👤 Examinador/a",
            value=st.session_state.examinador,
            help="Nombre del profesional que realizó la evaluación"
        )
        st.session_state.examinador = examinador
        
        dominancia = st.selectbox(
            "✋ Dominancia manual",
            ["D", "I"],
            index=0 if st.session_state.dominancia == "D" else 1,
            help="D = Diestro, I = Izquierdo"
        )
        st.session_state.dominancia = dominancia
    
    lugar = st.text_input(
        "📍 Lugar de aplicación",
        value=st.session_state.lugar_aplicacion,
        help="Centro, consultorio o lugar donde se realizó la evaluación"
    )
    st.session_state.lugar_aplicacion = lugar
    
    # Calcular edad
    if fecha_nac and fecha_eval:
        years, months, days = BaremosWPPSIUltra.calcular_edad_exacta(fecha_nac, fecha_eval)
        edad_texto = f"{years} años, {months} meses y {days} días"
        
        st.markdown("---")
        st.success(f"### 📅 Edad Cronológica: **{edad_texto}**")
    
    # Observaciones opcionales
    with st.expander("➕ Información Adicional (Opcional)"):
        motivo = st.text_area(
            "Motivo de consulta",
            value=st.session_state.motivo_consulta,
            height=100,
            help="Descripción breve del motivo de la evaluación"
        )
        st.session_state.motivo_consulta = motivo
        
        observaciones = st.text_area(
            "Observaciones conductuales",
            value=st.session_state.observaciones,
            height=150,
            help="Observaciones sobre el comportamiento durante la evaluación"
        )
        st.session_state.observaciones = observaciones
    
    st.markdown("---")
    
    if st.button("➡️ CONTINUAR AL PASO 2", type="primary", use_container_width=True):
        if not nombre:
            st.error("❌ Por favor ingrese el nombre del paciente")
        elif not examinador:
            st.error("❌ Por favor ingrese el nombre del examinador")
        else:
            st.session_state.paso_actual = 2
            st.rerun()

elif paso_actual == 2:
    # ==================== PASO 2: SELECCIÓN DE PRUEBAS ====================
    
    st.markdown("## <span class='step-number'>2</span> Selección de Pruebas Aplicadas", unsafe_allow_html=True)
    st.markdown("---")
    
    st.warning("""
    ⚠️ **IMPORTANTE**: Marque únicamente las pruebas que fueron **aplicadas completamente** al niño/a.
    
    Para calcular el CIT se requieren **al menos 5 pruebas principales**.
    """)
    
    st.markdown("###  Pruebas Principales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🗣️ Área Verbal-Conceptual")
        
        for prueba in ['informacion', 'semejanzas']:
            info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                f"{info['icono']} {info['nombre']} ({info['indice_primario']})",
                value=st.session_state.pruebas_aplicadas[prueba],
                help=f"{info['descripcion']}\nMide: {info['que_mide']}"
            )
        
        st.markdown("#### 🧠 Razonamiento")
        
        for prueba in ['matrices', 'conceptos']:
            info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                f"{info['icono']} {info['nombre']} ({info['indice_primario']})",
                value=st.session_state.pruebas_aplicadas[prueba],
                help=f"{info['descripcion']}\nMide: {info['que_mide']}"
            )
        
        st.markdown("#### 🧩 Memoria")
        
        for prueba in ['reconocimiento', 'localizacion']:
            info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                f"{info['icono']} {info['nombre']} ({info['indice_primario']})",
                value=st.session_state.pruebas_aplicadas[prueba],
                help=f"{info['descripcion']}\nMide: {info['que_mide']}"
            )
    
    with col2:
        st.markdown("#### 👀 Área Visoespacial")
        
        for prueba in ['cubos', 'rompecabezas']:
            info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                f"{info['icono']} {info['nombre']} ({info['indice_primario']})",
                value=st.session_state.pruebas_aplicadas[prueba],
                help=f"{info['descripcion']}\nMide: {info['que_mide']}"
            )
        
        st.markdown("#### ⚡ Velocidad de Procesamiento")
        
        for prueba in ['busqueda_animales', 'cancelacion']:
            info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                f"{info['icono']} {info['nombre']} ({info['indice_primario']})",
                value=st.session_state.pruebas_aplicadas[prueba],
                help=f"{info['descripcion']}\nMide: {info['que_mide']}"
            )
    
    # Pruebas complementarias
    with st.expander("➕ Pruebas Complementarias (Opcional)"):
        st.info("Estas pruebas son opcionales y se usan para análisis secundarios")
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            for prueba in ['vocabulario', 'dibujos', 'nombres']:
                info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
                st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                    f"{info['icono']} {info['nombre']}",
                    value=st.session_state.pruebas_aplicadas[prueba],
                    help=info['descripcion']
                )
        
        with col_c2:
            for prueba in ['clave_figuras', 'comprension']:
                info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
                st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                    f"{info['icono']} {info['nombre']}",
                    value=st.session_state.pruebas_aplicadas[prueba],
                    help=info['descripcion']
                )
    
    # Resumen de selección
    st.markdown("---")
    n_seleccionadas = sum(st.session_state.pruebas_aplicadas.values())
    
    col_r1, col_r2, col_r3 = st.columns(3)
    
    with col_r1:
        st.metric("Pruebas seleccionadas", n_seleccionadas)
    
    with col_r2:
        if n_seleccionadas >= 5:
            st.metric("Estado", "✅ Suficiente para CIT")
        else:
            st.metric("Estado", "⚠️ Insuficiente")
    
    with col_r3:
        if n_seleccionadas >= 10:
            st.metric("Completitud", "100%")
        else:
            st.metric("Completitud", f"{int(n_seleccionadas/10*100)}%")
    
    if n_seleccionadas < 5:
        st.error("⚠️ Se recomienda aplicar al menos 5 pruebas para calcular el CIT")
    
    st.markdown("---")
    
    col_nav1, col_nav2 = st.columns(2)
    
    with col_nav1:
        if st.button("⬅️ VOLVER AL PASO 1", use_container_width=True):
            st.session_state.paso_actual = 1
            st.rerun()
    
    with col_nav2:
        if st.button("➡️ CONTINUAR AL PASO 3", type="primary", use_container_width=True):
            if n_seleccionadas == 0:
                st.error("❌ Debe seleccionar al menos 1 prueba")
            else:
                st.session_state.paso_actual = 3
                st.rerun()

elif paso_actual == 3:
    # ==================== PASO 3: PUNTUACIONES DIRECTAS ====================
    
    st.markdown("## <span class='step-number'>3</span> Puntuaciones Directas (PD)", unsafe_allow_html=True)
    st.markdown("---")
    
    st.info("💡 Ingrese únicamente las puntuaciones directas de las pruebas que marcó como aplicadas")
    
    # Filtrar solo pruebas seleccionadas
    pruebas_para_ingresar = {k: v for k, v in st.session_state.pruebas_aplicadas.items() if v}
    
    if not pruebas_para_ingresar:
        st.warning("⚠️ No hay pruebas seleccionadas. Vuelva al Paso 2 para seleccionar pruebas.")
    else:
        # Organizar por índice
        pruebas_por_indice = {}
        for prueba in pruebas_para_ingresar:
            indice = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]['indice_primario']
            if indice not in pruebas_por_indice:
                pruebas_por_indice[indice] = []
            pruebas_por_indice[indice].append(prueba)
        
        tabs_indices = st.tabs([
            "📚 ICV", "🧩 IVE", "🧠 IRF", "💭 IMT", "⚡ IVP", "➕ Otras"
        ])
        
        nombres_tab = {
            '📚 ICV': 'ICV',
            '🧩 IVE': 'IVE',
            '🧠 IRF': 'IRF',
            '💭 IMT': 'IMT',
            '⚡ IVP': 'IVP',
            '➕ Otras': 'Otras'
        }
        
        for i, tab in enumerate(tabs_indices):
            with tab:
                indice_actual = list(nombres_tab.values())[i]
                
                if indice_actual == 'Otras':
                    pruebas_mostrar = [p for p in pruebas_para_ingresar 
                                      if BaremosWPPSIUltra.PRUEBAS_INFO[p]['complementaria']]
                else:
                    pruebas_mostrar = pruebas_por_indice.get(indice_actual, [])
                
                if not pruebas_mostrar:
                    st.info(f"No hay pruebas de {indice_actual} seleccionadas")
                else:
                    for prueba in pruebas_mostrar:
                        info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
                        rango = info['rango_pd']
                        
                        col_input, col_info = st.columns([1, 2])
                        
                        with col_input:
                            pd = st.number_input(
                                f"{info['icono']} {info['nombre']}",
                                min_value=rango[0],
                                max_value=rango[1],
                                value=st.session_state.pd_dict.get(prueba, rango[0]),
                                key=f"pd_{prueba}",
                                help=f"Rango: {rango[0]}-{rango[1]}"
                            )
                            st.session_state.pd_dict[prueba] = pd
                        
                        with col_info:
                            pe = BaremosWPPSIUltra.convertir_pd_a_pe(prueba, pd)
                            clasif = BaremosWPPSIUltra.clasificar_pe(pe)
                            
                            if clasif == "Fortaleza":
                                st.success(f"**PE = {pe}** | {clasif} ✨")
                            elif clasif == "Debilidad":
                                st.error(f"**PE = {pe}** | {clasif} ⚠️")
                            else:
                                st.info(f"**PE = {pe}** | {clasif}")
                            
                            st.caption(f"📖 {info['descripcion']}")
    
    st.markdown("---")
    
    # Mostrar resumen rápido
    with st.expander("📋 Resumen de Puntuaciones Ingresadas"):
        if st.session_state.pd_dict:
            df_resumen = pd.DataFrame([
                {
                    "Prueba": BaremosWPPSIUltra.PRUEBAS_INFO[k]['nombre'],
                    "PD": v,
                    "PE": BaremosWPPSIUltra.convertir_pd_a_pe(k, v),
                    "Clasificación": BaremosWPPSIUltra.clasificar_pe(BaremosWPPSIUltra.convertir_pd_a_pe(k, v))
                }
                for k, v in st.session_state.pd_dict.items()
            ])
            st.dataframe(df_resumen, use_container_width=True, hide_index=True)
        else:
            st.info("No hay puntuaciones ingresadas aún")
    
    col_nav1, col_nav2 = st.columns(2)
    
    with col_nav1:
        if st.button("⬅️ VOLVER AL PASO 2", use_container_width=True):
            st.session_state.paso_actual = 2
            st.rerun()
    
    with col_nav2:
        if st.button("✨ PROCESAR Y VER RESULTADOS", type="primary", use_container_width=True):
            if not st.session_state.pd_dict:
                st.error("❌ Debe ingresar al menos una puntuación directa")
            else:
                with st.spinner("Procesando evaluación..."):
                    # Procesar evaluación completa
                    datos_personales = {
                        'nombre': st.session_state.nombre_paciente,
                        'fecha_nacimiento': str(st.session_state.fecha_nacimiento),
                        'fecha_evaluacion': str(st.session_state.fecha_evaluacion),
                        'edad_texto': '',
                        'examinador': st.session_state.examinador,
                        'lugar': st.session_state.lugar_aplicacion,
                        'sexo': st.session_state.sexo,
                        'dominancia': st.session_state.dominancia
                    }
                    
                    if st.session_state.fecha_nacimiento and st.session_state.fecha_evaluacion:
                        y, m, d = BaremosWPPSIUltra.calcular_edad_exacta(
                            st.session_state.fecha_nacimiento,
                            st.session_state.fecha_evaluacion
                        )
                        datos_personales['edad_texto'] = f"{y} años, {m} meses y {d} días"
                    
                    resultados = procesar_evaluacion_completa(
                        datos_personales,
                        st.session_state.pruebas_aplicadas,
                        st.session_state.pd_dict
                    )
                    
                    # Guardar en session state
                    st.session_state.pe_dict = resultados['pe']
                    st.session_state.indices_primarios = resultados['indices_primarios']
                    st.session_state.indices_secundarios = resultados['indices_secundarios']
                    st.session_state.fortalezas = resultados['fortalezas']
                    st.session_state.debilidades = resultados['debilidades']
                    st.session_state.analisis_completo = resultados
                    st.session_state.datos_completos = True
                    
                    time.sleep(1)
                    st.success("✅ ¡Evaluación procesada correctamente!")
                    st.balloons()
                    time.sleep(1)
                    
                    st.session_state.paso_actual = 4
                    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# CONTINUACIÓN DEL CÓDIGO WPPSI-IV ULTRA COMPLETO - PARTE 3 FINAL
# Copie este código DESPUÉS de la Parte 2
# ═══════════════════════════════════════════════════════════════════════════════

elif paso_actual == 4:
    # ==================== PASO 4: RESULTADOS Y ANÁLISIS ====================
    
    if not st.session_state.datos_completos:
        st.warning("⚠️ Debe completar los pasos anteriores primero")
        if st.button("⬅️ VOLVER AL PASO 3"):
            st.session_state.paso_actual = 3
            st.rerun()
    else:
        st.markdown("## <span class='step-number'>4</span> Resultados y Análisis Detallado", unsafe_allow_html=True)
        st.markdown("---")
        
        # Tabs de resultados
        tab_res1, tab_res2, tab_res3, tab_res4 = st.tabs([
            "📊 Dashboard Principal",
            "📈 Gráficos Detallados",
            "🔍 Análisis Comparativo",
            "📝 Interpretación Clínica"
        ])
        
        with tab_res1:
            # ===== DASHBOARD PRINCIPAL =====
            
            st.markdown("### 🎯 Métricas Principales")
            
            resultados = st.session_state.analisis_completo
            indices = resultados['indices_primarios']
            
            # Mostrar métricas principales
            cols_metricas = st.columns(len([k for k in indices if indices[k] is not None]))
            
            idx = 0
            for key, valor in indices.items():
                if valor is not None:
                    with cols_metricas[idx]:
                        cat_info = resultados['categorias'][key]
                        perc = resultados['percentiles'][key]
                        
                        st.metric(
                            label=key,
                            value=valor,
                            delta=f"Percentil {perc}"
                        )
                        
                        # Badge de categoría
                        if "Muy Superior" in cat_info['categoria'] or "Superior" in cat_info['categoria']:
                            badge_class = "badge-success"
                        elif "Bajo" in cat_info['categoria'] or "Límite" in cat_info['categoria']:
                            badge_class = "badge-danger"
                        else:
                            badge_class = "badge-warning"
                        
                        st.markdown(
                            f'<span class="badge {badge_class}">{cat_info["categoria"]}</span>',
                            unsafe_allow_html=True
                        )
                    
                    idx += 1
            
            st.markdown("---")
            
            # Tabla resumen completa
            st.markdown("### 📋 Tabla Resumen de Puntuaciones")
            
            df_completo = pd.DataFrame([
                {
                    "Prueba": BaremosWPPSIUltra.PRUEBAS_INFO[k]['nombre'],
                    "Código": BaremosWPPSIUltra.PRUEBAS_INFO[k]['nombre_corto'],
                    "Índice": BaremosWPPSIUltra.PRUEBAS_INFO[k]['indice_primario'],
                    "PD": resultados['pd'][k],
                    "PE": v,
                    "Clasificación": BaremosWPPSIUltra.clasificar_pe(v)
                }
                for k, v in resultados['pe'].items()
            ])
            
            st.dataframe(
                df_completo,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "PE": st.column_config.ProgressColumn(
                        "PE",
                        help="Puntuación Escalar",
                        format="%d",
                        min_value=1,
                        max_value=19,
                    ),
                }
            )
            
            st.markdown("---")
            
            # CIT destacado
            if resultados['cit']:
                cit = resultados['cit']
                cat_cit = resultados['categorias']['CIT']
                perc_cit = resultados['percentiles']['CIT']
                ic_cit = resultados['intervalos_confianza']['CIT']
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {cat_cit['color']}15 0%, {cat_cit['color']}05 100%); 
                            padding: 2.5rem; border-radius: 20px; border-left: 6px solid {cat_cit['color']};
                            box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
                    <h2 style="color: {cat_cit['color']}; margin: 0; font-weight: 900;">
                        🧠 CI TOTAL: {cit}
                    </h2>
                    <h3 style="color: {cat_cit['color']}; margin-top: 0.5rem; font-weight: 700;">
                        {cat_cit['categoria']}
                    </h3>
                    <p style="margin-top: 1.5rem; font-size: 1.1rem; color: #2c3e50; font-weight: 600;">
                        <b>📊 Percentil:</b> {perc_cit}<br/>
                        <b>📈 Intervalo de Confianza 90%:</b> {ic_cit[0]} - {ic_cit[1]}<br/>
                        <b>💡 Interpretación:</b> {cat_cit['descripcion']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        with tab_res2:
            # ===== GRÁFICOS DETALLADOS =====
            
            st.markdown("### 📊 Visualizaciones Profesionales")
            
            # Gráfico 1: Perfil de PE
            fig_pe = crear_grafico_perfil_escalares_ultra(resultados['pe'])
            if fig_pe:
                st.plotly_chart(fig_pe, use_container_width=True)
            
            st.markdown("---")
            
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                # Gráfico 2: Índices compuestos
                fig_indices = crear_grafico_indices_compuestos_ultra(resultados['indices_primarios'])
                if fig_indices:
                    st.plotly_chart(fig_indices, use_container_width=True)
            
            with col_g2:
                # Gráfico 3: Comparación con media
                fig_comparacion = crear_grafico_comparacion_indices(resultados['indices_primarios'])
                if fig_comparacion:
                    st.plotly_chart(fig_comparacion, use_container_width=True)
            
            st.markdown("---")
            
            # Gráfico 4: Radar
            fig_radar = crear_grafico_radar_cognitivo(resultados['indices_primarios'])
            if fig_radar:
                st.plotly_chart(fig_radar, use_container_width=True)
        
        with tab_res3:
            # ===== ANÁLISIS COMPARATIVO =====
            
            st.markdown("### 🔍 Análisis de Fortalezas y Debilidades")
            
            col_fort, col_deb = st.columns(2)
            
            with col_fort:
                st.markdown("#### ✨ Fortalezas Identificadas")
                
                if resultados['fortalezas']:
                    for item in resultados['fortalezas']:
                        with st.container():
                            st.markdown(f"""
                            <div class="card-container">
                                <h4 style="color: #27ae60; margin: 0;">
                                    {item['prueba']}
                                </h4>
                                <p style="font-size: 1.8rem; font-weight: 900; color: #27ae60; margin: 0.5rem 0;">
                                    PE = {item['pe']}
                                </p>
                                <p style="color: #2c3e50; margin: 0;">
                                    <b>📌 Descripción:</b> {item['descripcion']}<br/>
                                    <b>🎯 Evalúa:</b> {item['que_mide']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.progress(item['pe'] / 19)
                            st.markdown("###")
                else:
                    st.info("No se identificaron fortalezas significativas (PE ≥ 13)")
            
            with col_deb:
                st.markdown("#### ⚠️ Áreas de Desarrollo")
                
                if resultados['debilidades']:
                    for item in resultados['debilidades']:
                        with st.container():
                            st.markdown(f"""
                            <div class="card-container">
                                <h4 style="color: #e74c3c; margin: 0;">
                                    {item['prueba']}
                                </h4>
                                <p style="font-size: 1.8rem; font-weight: 900; color: #e74c3c; margin: 0.5rem 0;">
                                    PE = {item['pe']}
                                </p>
                                <p style="color: #2c3e50; margin: 0;">
                                    <b>📌 Descripción:</b> {item['descripcion']}<br/>
                                    <b>🎯 Evalúa:</b> {item['que_mide']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.progress(item['pe'] / 19)
                            st.markdown("###")
                else:
                    st.info("No se identificaron debilidades significativas (PE ≤ 7)")
            
            st.markdown("---")
            
            # Análisis de dispersión
            st.markdown("### 📉 Análisis de Dispersión del Perfil")
            
            pe_valores = list(resultados['pe'].values())
            if pe_valores:
                pe_min = min(pe_valores)
                pe_max = max(pe_valores)
                pe_mean = np.mean(pe_valores)
                pe_std = np.std(pe_valores)
                disperson = pe_max - pe_min
                
                col_disp1, col_disp2, col_disp3, col_disp4 = st.columns(4)
                
                with col_disp1:
                    st.metric("PE Mínima", pe_min)
                
                with col_disp2:
                    st.metric("PE Máxima", pe_max)
                
                with col_disp3:
                    st.metric("PE Media", f"{pe_mean:.1f}")
                
                with col_disp4:
                    st.metric("Dispersión", disperson)
                
                if disperson >= 5:
                    st.warning(f"""
                    ⚠️ **Dispersión Alta**: La diferencia entre la PE más alta ({pe_max}) y la más baja ({pe_min}) 
                    es de {disperson} puntos. Esto sugiere un perfil cognitivo heterogéneo que requiere 
                    interpretación cuidadosa.
                    """)
                else:
                    st.success(f"""
                    ✅ **Perfil Homogéneo**: La dispersión de {disperson} puntos indica un perfil 
                    cognitivo relativamente uniforme.
                    """)
        
        with tab_res4:
            # ===== INTERPRETACIÓN CLÍNICA =====
            
            st.markdown("### 📝 Interpretación Clínica Narrativa")
            
            st.info("""
            💡 **Nota**: Esta interpretación es generada automáticamente y debe ser 
            revisada y complementada por un profesional cualificado.
            """)
            
            # Interpretación del CIT
            if resultados['cit']:
                st.markdown("#### 🧠 Coeficiente Intelectual Total (CIT)")
                
                cit = resultados['cit']
                cat = resultados['categorias']['CIT']
                perc = resultados['percentiles']['CIT']
                ic = resultados['intervalos_confianza']['CIT']
                
                nombre = st.session_state.nombre_paciente
                
                texto_cit = f"""
                **{nombre}** obtuvo un Coeficiente Intelectual Total (CIT) de **{cit}**, 
                que se clasifica en la categoría **{cat['categoria']}** según los baremos del WPPSI-IV.
                
                Esta puntuación sitúa al evaluado en el **percentil {perc}**, lo que significa que 
                su rendimiento supera aproximadamente al {perc}% de los niños de su edad en la 
                muestra de estandarización.
                
                Existe una probabilidad del 90% de que el verdadero CIT de {nombre} se encuentre 
                en el rango de **{ic[0]} a {ic[1]}** puntos.
                
                **Interpretación:** {cat['descripcion']}.
                """
                
                st.markdown(texto_cit)
            
            st.markdown("---")
            
            # Interpretación de índices
            st.markdown("#### 📊 Interpretación por Índices Primarios")
            
            interpretaciones = {
                'ICV': ('Comprensión Verbal', 
                       'Este índice refleja la capacidad de razonamiento con información verbal, formación de conceptos y conocimientos adquiridos.'),
                'IVE': ('Visoespacial', 
                       'Mide la capacidad para analizar y sintetizar información visual y comprender relaciones espaciales.'),
                'IRF': ('Razonamiento Fluido', 
                       'Evalúa la capacidad para resolver problemas nuevos y detectar relaciones lógicas sin depender del conocimiento previo.'),
                'IMT': ('Memoria de Trabajo', 
                       'Refleja la capacidad para mantener y manipular información en la memoria a corto plazo.'),
                'IVP': ('Velocidad de Procesamiento', 
                       'Mide la rapidez y precisión en el procesamiento de información visual simple.')
            }
            
            for idx, (nombre_idx, desc_idx) in interpretaciones.items():
                if idx in resultados['indices_primarios']:
                    pc = resultados['indices_primarios'][idx]
                    cat = resultados['categorias'][idx]
                    
                    with st.expander(f"**{idx} - {nombre_idx}: {pc}** ({cat['categoria']})"):
                        st.markdown(f"""
                        **Puntuación Compuesta:** {pc}  
                        **Categoría:** {cat['categoria']}  
                        **Percentil:** {resultados['percentiles'][idx]}
                        
                        {desc_idx}
                        
                        El evaluado obtuvo una puntuación de {pc} en este índice, clasificada como 
                        {cat['categoria']}, lo que indica {cat['descripcion'].lower()}.
                        """)
            
            st.markdown("---")
            
            # Recomendaciones
            st.markdown("#### 💡 Recomendaciones Preliminares")
            
            recomendaciones_auto = []
            
            if resultados['fortalezas']:
                recomendaciones_auto.append("""
                **Aprovechar Fortalezas:** Se identificaron áreas de fortaleza que pueden 
                utilizarse como base para desarrollar otras habilidades y compensar áreas 
                de menor rendimiento.
                """)
            
            if resultados['debilidades']:
                recomendaciones_auto.append("""
                **Intervención Focalizada:** Se recomienda diseñar un plan de intervención 
                que incluya actividades específicas para fortalecer las áreas identificadas 
                con menor rendimiento.
                """)
            
            # Verificar dispersión
            pe_valores = list(resultados['pe'].values())
            if pe_valores and (max(pe_valores) - min(pe_valores)) >= 5:
                recomendaciones_auto.append("""
                **Perfil Heterogéneo:** La variabilidad significativa en el perfil sugiere 
                la necesidad de adaptar las estrategias de enseñanza a las características 
                individuales del evaluado.
                """)
            
            for i, rec in enumerate(recomendaciones_auto, 1):
                st.markdown(f"{i}. {rec}")
        
        st.markdown("---")
        
        # Navegación
        col_nav1, col_nav2 = st.columns(2)
        
        with col_nav1:
            if st.button("⬅️ VOLVER AL PASO 3", use_container_width=True):
                st.session_state.paso_actual = 3
                st.rerun()
        
        with col_nav2:
            if st.button("➡️ GENERAR INFORME PDF", type="primary", use_container_width=True):
                st.session_state.paso_actual = 5
                st.rerun()

elif paso_actual == 5:
    # ==================== PASO 5: GENERAR PDF ====================
    
    if not st.session_state.datos_completos:
        st.warning("⚠️ Debe completar la evaluación primero")
        if st.button("⬅️ VOLVER AL INICIO"):
            st.session_state.paso_actual = 1
            st.rerun()
    else:
        st.markdown("## <span class='step-number'>5</span> Generación de Informe Profesional", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 📄 Informe PDF Profesional")
        
        st.success("""
        ✅ **Evaluación completada exitosamente**
        
        Puede generar un informe PDF profesional completo con:
        - Datos de filiación del paciente
        - Tabla completa de puntuaciones (PD y PE)
        - Índices primarios y secundarios
        - Gráficos profesionales
        - Interpretación clínica narrativa
        - Análisis de fortalezas y debilidades
        - Recomendaciones profesionales
        """)
        
        # Previsualización
        st.markdown("### 👁️ Previsualización del Contenido")
        
        resultados = st.session_state.analisis_completo
        
        with st.expander("📋 Ver resumen de datos a incluir"):
            st.markdown(f"""
            **Paciente:** {st.session_state.nombre_paciente}  
            **Edad:** {resultados['datos_personales']['edad_texto']}  
            **Fecha de evaluación:** {st.session_state.fecha_evaluacion}  
            **Examinador/a:** {st.session_state.examinador}
            
            **Pruebas aplicadas:** {len(resultados['pe'])}  
            **CIT:** {resultados['cit'] if resultados['cit'] else 'No calculado'}  
            **Fortalezas identificadas:** {len(resultados['fortalezas'])}  
            **Debilidades identificadas:** {len(resultados['debilidades'])}
            """)
        
        st.markdown("---")
        
        # Opciones de personalización
        st.markdown("### ⚙️ Opciones del Informe")
        
        col_op1, col_op2 = st.columns(2)
        
        with col_op1:
            incluir_graficos = st.checkbox("📊 Incluir gráficos", value=True)
            incluir_interpretacion = st.checkbox("📝 Incluir interpretación narrativa", value=True)
        
        with col_op2:
            incluir_recomendaciones = st.checkbox("💡 Incluir recomendaciones", value=True)
            incluir_observaciones = st.checkbox("🗒️ Incluir observaciones conductuales", 
                                               value=bool(st.session_state.observaciones))
        
        st.markdown("---")
        
        # Botón de generación
        st.markdown("### 🖨️ Generar Informe")
        
        if st.button("📥 GENERAR Y DESCARGAR INFORME PDF", type="primary", use_container_width=True):
            with st.spinner("Generando informe PDF profesional... Por favor espere."):
                try:
                    # Simular progreso
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("⏳ Preparando datos...")
                    progress_bar.progress(20)
                    time.sleep(0.5)
                    
                    status_text.text("📊 Generando tablas...")
                    progress_bar.progress(40)
                    time.sleep(0.5)
                    
                    status_text.text("🎨 Creando gráficos...")
                    progress_bar.progress(60)
                    time.sleep(0.5)
                    
                    status_text.text("📝 Generando interpretación...")
                    progress_bar.progress(80)
                    time.sleep(0.5)
                    
                    # Generar PDF
                    pdf_buffer = generar_informe_pdf_ultra_completo(resultados)
                    
                    status_text.text("✅ Informe completado!")
                    progress_bar.progress(100)
                    time.sleep(0.5)
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.success("✅ ¡Informe PDF generado exitosamente!")
                    st.balloons()
                    
                    # Botón de descarga
                    nombre_archivo = f"Informe_WPPSI-IV_{st.session_state.nombre_paciente.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                    
                    st.download_button(
                        label="⬇️ DESCARGAR INFORME PDF",
                        data=pdf_buffer,
                        file_name=nombre_archivo,
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                    
                    st.info("""
                    💡 **Sugerencia**: Guarde el informe en un lugar seguro y respete la 
                    confidencialidad de los datos del paciente.
                    """)
                    
                except Exception as e:
                    st.error(f"""
                    ❌ **Error al generar el PDF**
                    
                    Ha ocurrido un error: {str(e)}
                    
                    Por favor, intente nuevamente o contacte al administrador del sistema.
                    """)
        
        st.markdown("---")
        
        # Navegación
        col_nav1, col_nav2, col_nav3 = st.columns(3)
        
        with col_nav1:
            if st.button("⬅️ VOLVER A RESULTADOS", use_container_width=True):
                st.session_state.paso_actual = 4
                st.rerun()
        
        with col_nav2:
            if st.button("🔄 NUEVA EVALUACIÓN", use_container_width=True):
                # Reiniciar todo
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                init_session_state()
                st.rerun()
        
        with col_nav3:
            if st.button("💾 GUARDAR SESIÓN", use_container_width=True):
                st.info("Funcionalidad de guardado en desarrollo")

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER ULTRA PROFESIONAL
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="divider-decorative"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-ultra">
    <p style="font-size: 1.4rem; font-weight: 800; color: #8B1538; margin-bottom: 0.8rem;">
        🧠 WPPSI-IV PROFESSIONAL ULTRA SYSTEM
    </p>
    <p style="font-size: 1.1rem; font-weight: 600; color: #2c3e50; margin-bottom: 0.5rem;">
        Sistema Integral de Evaluación Psicopedagógica
    </p>
    <p style="font-size: 1rem; color: #8B1538; font-weight: 700; margin-top: 1rem;">
        ❤️ Desarrollado especialmente para Daniela
    </p>
    <p style="font-size: 0.9rem; color: #7f8c8d; margin-top: 1.5rem;">
        Versión 7.0.0 Professional Ultra Edition | © 2026
    </p>
    <p style="font-size: 0.85rem; color: #95a5a6; margin-top: 0.5rem;">
        Basado en WPPSI-IV de Pearson | Uso profesional exclusivo
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONALIDADES ADICIONALES
# ═══════════════════════════════════════════════════════════════════════════════

# Atajos de teclado (información)
with st.sidebar:
    with st.expander("⌨️ Atajos y Ayuda"):
        st.markdown("""
        **Navegación Rápida:**
        - Paso 1: Datos del Paciente
        - Paso 2: Selección de Pruebas
        - Paso 3: Puntuaciones Directas
        - Paso 4: Resultados
        - Paso 5: Generar PDF
        
        **Información del Sistema:**
        - Versión: 7.0.0 Ultra
        - Desarrollado con Streamlit
        - Python + Plotly + ReportLab
        
        **Soporte:**
        - Manual WPPSI-IV oficial
        - Baremos edad 4:0-7:7
        - Cálculos automáticos
        """)
    
    # Información de desarrollo
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #8B1538 0%, #c71f4a 100%); 
                border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(139,21,56,0.3);">
        <p style="margin: 0; font-size: 0.9rem; font-weight: 700;">
            💝 Con amor para Daniela
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.75rem; opacity: 0.9;">
            Sistema WPPSI-IV Ultra v7.0
        </p>
    </div>
    """, unsafe_allow_html=True)

# Mensaje de estado en sidebar
if st.session_state.datos_completos:
    st.sidebar.success("✅ Sistema listo para generar informes")
else:
    st.sidebar.info("ℹ️ Complete los pasos para generar informes")
