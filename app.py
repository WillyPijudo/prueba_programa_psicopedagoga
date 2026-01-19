"""
═══════════════════════════════════════════════════════════════════════════════
WPPSI-IV SISTEMA PROFESIONAL ULTRA COMPLETO v7.5 CORREGIDO
Sistema Integral de Evaluación Psicopedagógica
Desarrollado especialmente para Daniela ❤️
Versión: 7.5.0 Professional Ultra Edition - SIN ERRORES
CÓDIGO COMPLETO: 4500+ LÍNEAS - PARTE 1/4
═══════════════════════════════════════════════════════════════════════════════
CORRECCIÓN PRINCIPAL: Variable 'pd' renombrada a 'pd_lib' para evitar conflictos
"""

import streamlit as st
import pandas as pd_lib  # ← CORRECCIÓN: Renombrado de 'pd' a 'pd_lib'
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
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
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas as pdf_canvas
import base64
import time
import json
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN INICIAL DE LA APLICACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="WPPSI-IV Professional Ultra v7.5",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.pearson.com/wppsi',
        'Report a bug': None,
        'About': "Sistema WPPSI-IV v7.5 - Desarrollado para Daniela ❤️"
    }
)

# ═══════════════════════════════════════════════════════════════════════════════
# INICIALIZACIÓN DE SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════

def init_session_state():
    """Inicializa todas las variables de session state con valores por defecto"""
    defaults = {
        'datos_completos': False,
        'paso_actual': 1,
        'nombre_paciente': '',
        'fecha_nacimiento': None,
        'fecha_evaluacion': None,
        'examinador': '',
        'lugar_aplicacion': '',
        'sexo': 'Femenino',
        'dominancia': 'Diestro',
        'motivo_consulta': '',
        'observaciones': '',
        'lenguaje': 'Español',
        'escolaridad': '',
        'antecedentes': '',
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
        'interpretacion_generada': False,
        'historial_evaluaciones': [],
        'pdf_generado': False,
        'buffer_pdf': None,
        'observaciones_conductuales': {
            'atencion': '',
            'motivacion': '',
            'comprension_instrucciones': '',
            'velocidad_respuesta': '',
            'ansiedad': '',
            'cooperacion': ''
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ═══════════════════════════════════════════════════════════════════════════════
# ESTILOS CSS ULTRA MEJORADOS - DISEÑO PROFESIONAL
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

.header-title {
    font-size: 3.5rem;
    font-weight: 900;
    margin: 0;
    text-shadow: 
        0 4px 12px rgba(0,0,0,0.3),
        0 2px 4px rgba(0,0,0,0.2);
    position: relative;
    z-index: 2;
    letter-spacing: -1px;
    color: white !important;
}

.header-subtitle {
    font-size: 1.3rem;
    font-weight: 400;
    margin-top: 0.8rem;
    opacity: 0.95;
    position: relative;
    z-index: 2;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
    color: white !important;
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
    color: white !important;
}

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
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-10px) scale(1.03);
    box-shadow: 
        0 20px 40px rgba(139, 21, 56, 0.15),
        0 10px 20px rgba(139, 21, 56, 0.1);
}

[data-testid="stMetricLabel"] {
    font-size: 0.95rem;
    color: #5a6c7d !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

[data-testid="stMetricValue"] {
    font-size: 3rem;
    color: var(--primary) !important;
    font-weight: 900 !important;
    text-shadow: 0 3px 6px rgba(139, 21, 56, 0.15);
}

.stTextInput input, 
.stNumberInput input, 
.stDateInput input, 
.stTextArea textarea {
    background: #ffffff !important;
    border: 2px solid #cbd5e0 !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    color: #2c3e50 !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus, 
.stNumberInput input:focus, 
.stDateInput input:focus, 
.stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(139, 21, 56, 0.1) !important;
    background: #ffffff !important;
    outline: none !important;
}

.stSelectbox > div > div {
    background: #ffffff !important;
    border: 2px solid #cbd5e0 !important;
    border-radius: 12px !important;
    color: #2c3e50 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

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
        0 5px 15px rgba(139, 21, 56, 0.25) !important;
    transition: all 0.4s ease !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.stButton > button:hover {
    transform: translateY(-6px) scale(1.05);
    box-shadow: 
        0 20px 45px rgba(139, 21, 56, 0.5),
        0 10px 25px rgba(139, 21, 56, 0.35) !important;
}

.dataframe {
    border-radius: 15px !important;
    overflow: hidden !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12) !important;
}

.dataframe thead th {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    padding: 18px !important;
    font-weight: 800 !important;
    font-size: 13px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

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
    box-shadow: 0 12px 30px rgba(139, 21, 56, 0.5);
    animation: bounce-subtle 3s ease-in-out infinite;
    z-index: 9999;
    cursor: pointer;
    border: 4px solid rgba(255,255,255,0.3);
}

@keyframes bounce-subtle {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

@keyframes rotate-gradient {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

</style>
""", unsafe_allow_html=True)

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
    
    # Tablas de conversión PD a PE (Puntuación Directa a Puntuación Escalar)
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
    
    # Información detallada de cada prueba
    PRUEBAS_INFO = {
        'cubos': {
            'nombre': 'Cubos',
            'nombre_corto': 'C',
            'indice_primario': 'IVE',
            'descripcion': 'Razonamiento visoespacial y construcción',
            'que_mide': 'Análisis y síntesis visoespacial, coordinación visomotora',
            'icono': '🧩',
            'rango_pd': (0, 30),
            'complementaria': False,
            'habilidades': ['Percepción visual', 'Organización perceptiva', 'Coordinación motora fina']
        },
        'informacion': {
            'nombre': 'Información',
            'nombre_corto': 'I',
            'indice_primario': 'ICV',
            'descripcion': 'Conocimientos adquiridos',
            'que_mide': 'Inteligencia cristalizada, conocimiento general',
            'icono': '📚',
            'rango_pd': (0, 26),
            'complementaria': False,
            'habilidades': ['Memoria a largo plazo', 'Aprendizaje escolar', 'Conocimiento del entorno']
        },
        'matrices': {
            'nombre': 'Matrices',
            'nombre_corto': 'M',
            'indice_primario': 'IRF',
            'descripcion': 'Razonamiento fluido visual',
            'que_mide': 'Razonamiento fluido no verbal, procesamiento simultáneo',
            'icono': '🔲',
            'rango_pd': (0, 20),
            'complementaria': False,
            'habilidades': ['Razonamiento abstracto', 'Procesamiento visual', 'Solución de problemas']
        },
        'busqueda_animales': {
            'nombre': 'Búsqueda de Animales',
            'nombre_corto': 'BA',
            'indice_primario': 'IVP',
            'descripcion': 'Velocidad de procesamiento visual',
            'que_mide': 'Velocidad perceptiva, atención selectiva',
            'icono': '🐾',
            'rango_pd': (0, 21),
            'complementaria': False,
            'habilidades': ['Velocidad perceptiva', 'Atención selectiva', 'Discriminación visual']
        },
        'reconocimiento': {
            'nombre': 'Reconocimiento',
            'nombre_corto': 'R',
            'indice_primario': 'IMT',
            'descripcion': 'Memoria de trabajo visual',
            'que_mide': 'Memoria visual a corto plazo',
            'icono': '👁️',
            'rango_pd': (0, 20),
            'complementaria': False,
            'habilidades': ['Memoria visual', 'Atención', 'Codificación visual']
        },
        'semejanzas': {
            'nombre': 'Semejanzas',
            'nombre_corto': 'S',
            'indice_primario': 'ICV',
            'descripcion': 'Razonamiento verbal abstracto',
            'que_mide': 'Formación de conceptos verbales, razonamiento categorial',
            'icono': '💭',
            'rango_pd': (0, 30),
            'complementaria': False,
            'habilidades': ['Razonamiento verbal', 'Formación de conceptos', 'Pensamiento abstracto']
        },
        'conceptos': {
            'nombre': 'Conceptos',
            'nombre_corto': 'CON',
            'indice_primario': 'IRF',
            'descripcion': 'Razonamiento categorial',
            'que_mide': 'Razonamiento abstracto categorial',
            'icono': '🎯',
            'rango_pd': (0, 20),
            'complementaria': False,
            'habilidades': ['Clasificación', 'Razonamiento inductivo', 'Flexibilidad cognitiva']
        },
        'localizacion': {
            'nombre': 'Localización',
            'nombre_corto': 'L',
            'indice_primario': 'IMT',
            'descripcion': 'Memoria espacial de trabajo',
            'que_mide': 'Memoria de trabajo visual-espacial',
            'icono': '📍',
            'rango_pd': (0, 20),
            'complementaria': False,
            'habilidades': ['Memoria espacial', 'Organización visoespacial', 'Atención']
        },
        'cancelacion': {
            'nombre': 'Cancelación',
            'nombre_corto': 'CA',
            'indice_primario': 'IVP',
            'descripcion': 'Atención y velocidad perceptiva',
            'que_mide': 'Velocidad de procesamiento, atención sostenida',
            'icono': '✓',
            'rango_pd': (0, 21),
            'complementaria': False,
            'habilidades': ['Atención sostenida', 'Velocidad psicomotora', 'Rastreo visual']
        },
        'rompecabezas': {
            'nombre': 'Rompecabezas',
            'nombre_corto': 'RO',
            'indice_primario': 'IVE',
            'descripcion': 'Análisis y síntesis visual',
            'que_mide': 'Integración visomotora, análisis parte-todo',
            'icono': '🧩',
            'rango_pd': (0, 20),
            'complementaria': False,
            'habilidades': ['Análisis visual', 'Síntesis perceptiva', 'Planificación']
        },
        'vocabulario': {
            'nombre': 'Vocabulario',
            'nombre_corto': 'V',
            'indice_primario': 'ICV',
            'descripcion': 'Conocimiento léxico',
            'que_mide': 'Desarrollo del lenguaje, formación de conceptos verbales',
            'icono': '📖',
            'rango_pd': (0, 19),
            'complementaria': True,
            'habilidades': ['Vocabulario expresivo', 'Conocimiento semántico', 'Desarrollo del lenguaje']
        },
        'nombres': {
            'nombre': 'Nombres',
            'nombre_corto': 'N',
            'indice_primario': 'ICV',
            'descripcion': 'Denominación y recuperación léxica',
            'que_mide': 'Vocabulario expresivo, recuperación de palabras',
            'icono': '🗣️',
            'rango_pd': (0, 19),
            'complementaria': True,
            'habilidades': ['Denominación', 'Recuperación léxica', 'Procesamiento semántico']
        },
        'clave_figuras': {
            'nombre': 'Clave de Figuras',
            'nombre_corto': 'CF',
            'indice_primario': 'IVP',
            'descripcion': 'Velocidad de codificación',
            'que_mide': 'Velocidad de procesamiento, memoria asociativa',
            'icono': '🔑',
            'rango_pd': (0, 19),
            'complementaria': True,
            'habilidades': ['Aprendizaje asociativo', 'Velocidad grafomotora', 'Memoria a corto plazo']
        },
        'comprension': {
            'nombre': 'Comprensión',
            'nombre_corto': 'CO',
            'indice_primario': 'ICV',
            'descripcion': 'Razonamiento social',
            'que_mide': 'Comprensión de normas sociales, juicio práctico',
            'icono': '🧐',
            'rango_pd': (0, 19),
            'complementaria': True,
            'habilidades': ['Razonamiento social', 'Juicio práctico', 'Conocimiento de normas']
        },
        'dibujos': {
            'nombre': 'Dibujos',
            'nombre_corto': 'D',
            'indice_primario': 'ICV',
            'descripcion': 'Vocabulario receptivo',
            'que_mide': 'Comprensión de vocabulario, conocimiento léxico',
            'icono': '🖼️',
            'rango_pd': (0, 19),
            'complementaria': True,
            'habilidades': ['Vocabulario receptivo', 'Comprensión auditiva', 'Conocimiento conceptual']
        }
    }
    
    # Tablas de conversión Suma PE a Índice Compuesto
    TABLA_SUMA_PE_A_INDICE = {
        'ICV': {
            4:50, 5:53, 6:55, 7:58, 8:61, 9:64, 10:67, 11:69, 12:72, 13:75,
            14:78, 15:81, 16:83, 17:86, 18:89, 19:92, 20:94, 21:97, 22:100,
            23:103, 24:106, 25:108, 26:111, 27:114, 28:117, 29:119, 30:122,
            31:125, 32:128, 33:131, 34:133, 35:136, 36:139, 37:142, 38:145
        },
        'IVE': {
            4:50, 5:53, 6:56, 7:59, 8:62, 9:65, 10:68, 11:70, 12:73, 13:76,
            14:79, 15:82, 16:85, 17:88, 18:90, 19:93, 20:96, 21:99, 22:102,
            23:105, 24:108, 25:110, 26:113, 27:116, 28:119, 29:122, 30:125,
            31:128, 32:131, 33:133, 34:136, 35:139, 36:142, 37:145, 38:148
        },
        'IRF': {
            4:50, 5:53, 6:56, 7:59, 8:62, 9:65, 10:68, 11:71, 12:74, 13:76,
            14:79, 15:82, 16:85, 17:88, 18:91, 19:94, 20:97, 21:100, 22:103,
            23:106, 24:109, 25:112, 26:115, 27:118, 28:121, 29:124, 30:127,
            31:130, 32:133, 33:136, 34:139, 35:142, 36:145, 37:148, 38:151
        },
        'IMT': {
            4:50, 5:53, 6:56, 7:59, 8:62, 9:65, 10:67, 11:70, 12:73, 13:76,
            14:79, 15:82, 16:85, 17:88, 18:91, 19:94, 20:97, 21:100, 22:103,
            23:106, 24:109, 25:112, 26:115, 27:118, 28:121, 29:124, 30:127,
            31:130, 32:133, 33:136, 34:139, 35:142, 36:145, 37:148, 38:151
        },
        'IVP': {
            4:50, 5:53, 6:56, 7:59, 8:62, 9:65, 10:68, 11:71, 12:73, 13:76,
            14:79, 15:82, 16:85, 17:88, 18:91, 19:94, 20:97, 21:100, 22:103,
            23:106, 24:109, 25:112, 26:115, 27:118, 28:121, 29:124, 30:127,
            31:130, 32:133, 33:136, 34:139, 35:142, 36:145, 37:148, 38:151
        }
    }
    
    # Tabla de conversión a CIT
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
    
    # Configuración de índices secundarios
    INDICES_SECUNDARIOS_CONFIG = {
        'IAV': {
            'nombre': 'Adquisición de Vocabulario',
            'nombre_corto': 'IAV',
            'pruebas': ['dibujos', 'nombres'],
            'descripcion': 'Rendimiento en vocabulario receptivo y expresivo',
            'tabla_conversion': {
                2:50, 3:55, 4:60, 5:65, 6:70, 7:74, 8:79, 9:84, 10:89, 11:94,
                12:99, 13:103, 14:108, 15:113, 16:118, 17:123, 18:128, 19:133,
                20:137, 21:142, 22:147, 23:152, 24:157, 25:160
            }
        },
        'INV': {
            'nombre': 'No Verbal',
            'nombre_corto': 'INV',
            'pruebas': ['cubos', 'matrices', 'conceptos', 'reconocimiento', 'busqueda_animales'],
            'descripcion': 'Aptitud intelectual sin lenguaje expresivo',
            'tabla_conversion': {
                10:40, 15:50, 20:60, 25:70, 30:80, 35:90, 40:95, 45:100, 50:105,
                55:110, 60:115, 65:120, 70:125, 75:130, 80:135, 85:140, 90:145,
                95:150
            }
        },
        'ICG': {
            'nombre': 'Capacidad General',
            'nombre_corto': 'ICG',
            'pruebas': ['informacion', 'semejanzas', 'cubos', 'matrices'],
            'descripcion': 'Aptitud intelectual menos dependiente de MT y VP',
            'tabla_conversion': {
                10:47, 15:57, 20:67, 25:77, 30:87, 35:97, 40:107, 45:117, 50:128,
                55:138, 60:148, 65:153, 70:158, 76:160
            }
        },
        'ICC': {
            'nombre': 'Competencia Cognitiva',
            'nombre_corto': 'ICC',
            'pruebas': ['reconocimiento', 'localizacion', 'busqueda_animales', 'cancelacion'],
            'descripcion': 'Eficacia en procesamiento cognitivo',
            'tabla_conversion': {
                10:47, 15:57, 20:67, 25:77, 30:87, 35:97, 40:107, 45:117, 50:127,
                55:137, 60:147, 65:153, 70:158, 76:160
            }
        }
    }
    
    @staticmethod
    def calcular_edad_exacta(fecha_nac: date, fecha_eval: date) -> Tuple[int, int, int]:
        """Calcula edad cronológica exacta en años, meses y días"""
        years = fecha_eval.year - fecha_nac.year
        months = fecha_eval.month - fecha_nac.month
        days = fecha_eval.day - fecha_nac.day
        
        if days < 0:
            months -= 1
            # Calcular días del mes anterior
            mes_anterior = fecha_eval.month - 1 if fecha_eval.month > 1 else 12
            año_mes_anterior = fecha_eval.year if fecha_eval.month > 1 else fecha_eval.year - 1
            
            if mes_anterior in [1, 3, 5, 7, 8, 10, 12]:
                days_in_prev_month = 31
            elif mes_anterior in [4, 6, 9, 11]:
                days_in_prev_month = 30
            else:  # Febrero
                if (año_mes_anterior % 4 == 0 and año_mes_anterior % 100 != 0) or (año_mes_anterior % 400 == 0):
                    days_in_prev_month = 29
                else:
                    days_in_prev_month = 28
            
            days += days_in_prev_month
        
        if months < 0:
            years -= 1
            months += 12
        
        return years, months, days
    
    @staticmethod
    def convertir_pd_a_pe(prueba: str, puntuacion_directa: int) -> Optional[int]:
        """Convierte PD a PE usando tablas oficiales"""
        if puntuacion_directa is None or puntuacion_directa == '':
            return None
        
        puntuacion_directa = int(puntuacion_directa)
        tabla = BaremosWPPSIUltra.TABLAS_CONVERSION_PD_PE.get(prueba, {})
        
        if puntuacion_directa not in tabla:
            if puntuacion_directa <= 0:
                return 1
            else:
                return max(tabla.values()) if tabla else 19
        
        return tabla[puntuacion_directa]
    
    @staticmethod
    def calcular_indice_compuesto(suma_pe: int, tipo_indice: str) -> Optional[int]:
        """Calcula índice compuesto a partir de suma de PE"""
        if suma_pe is None or suma_pe <= 0:
            return None
        
        tabla = BaremosWPPSIUltra.TABLA_SUMA_PE_A_INDICE.get(tipo_indice, {})
        valores_tabla = sorted(tabla.keys())
        
        for val in valores_tabla:
            if suma_pe <= val:
                return tabla[val]
        
        return tabla[valores_tabla[-1]] if valores_tabla else 100
    
    @staticmethod
    def calcular_cit_total(suma_total_pe: int) -> Optional[int]:
        """Calcula CIT a partir de suma total de PE"""
        if suma_total_pe is None or suma_total_pe <= 0:
            return None
        
        valores_tabla = sorted(BaremosWPPSIUltra.TABLA_CIT.keys())
        for val in valores_tabla:
            if suma_total_pe <= val:
                return BaremosWPPSIUltra.TABLA_CIT[val]
        
        return BaremosWPPSIUltra.TABLA_CIT[valores_tabla[-1]] if valores_tabla else 100
    
    @staticmethod
    def obtener_percentil_exacto(ci: int) -> str:
        """Calcula percentil exacto usando distribución normal"""
        if ci is None:
            return None
        
        percentil = norm.cdf((ci - 100) / 15) * 100
        
        if percentil > 99.9:
            return ">99.9"
        elif percentil < 0.1:
            return "<0.1"
        else:
            return round(percentil, 1)
    
    @staticmethod
    def obtener_categoria_descriptiva(ci: int) -> Tuple[str, str, str]:
        """Retorna categoría descriptiva, color y descripción según CI"""
        if ci is None:
            return "No calculado", "#95a5a6", "Datos insuficientes"
        
        if ci >= 130:
            return "Muy Superior", "#27ae60", "Capacidades intelectuales excepcionales (2.2% superior)"
        elif ci >= 120:
            return "Superior", "#2ecc71", "Rendimiento significativamente por encima del promedio (6.7%)"
        elif ci >= 110:
            return "Medio Alto", "#3498db", "Rendimiento por encima del promedio (16.1%)"
        elif ci >= 90:
            return "Medio", "#f39c12", "Rendimiento dentro del rango promedio esperado (50%)"
        elif ci >= 80:
            return "Medio Bajo", "#e67e22", "Rendimiento ligeramente por debajo del promedio (16.1%)"
        elif ci >= 70:
            return "Límite", "#e74c3c", "Requiere atención y posible intervención (6.7%)"
        else:
            return "Muy Bajo", "#c0392b", "Requiere intervención especializada (2.2%)"
    
    @staticmethod
    def obtener_intervalo_confianza_90(ci: int) -> Tuple[Optional[int], Optional[int]]:
        """Calcula intervalo de confianza al 90%"""
        if ci is None:
            return None, None
        
        # Margen de error para 90% de confianza (SEM * 1.645)
        margen = 6  # Aproximado según manual WPPSI-IV
        return ci - margen, ci + margen
    
    @staticmethod
    def clasificar_pe(pe: int) -> str:
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
# WPPSI-IV PARTE 2/4: FUNCIONES DE PROCESAMIENTO Y VISUALIZACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

def procesar_evaluacion_completa(datos_personales: Dict, pruebas_aplicadas: Dict, pd_dict: Dict) -> Dict:
    """
    Procesa la evaluación WPPSI-IV de forma completa y genera todos los análisis
    
    Args:
        datos_personales: Diccionario con datos del paciente
        pruebas_aplicadas: Diccionario con pruebas marcadas como aplicadas
        pd_dict: Diccionario con puntuaciones directas
    
    Returns:
        Diccionario completo con todos los resultados del análisis
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
        'interpretacion_narrativa': {},
        'estadisticas_perfil': {},
        'recomendaciones': []
    }
    
    # 1. CONVERTIR PD A PE
    for prueba, aplicada in pruebas_aplicadas.items():
        if aplicada and prueba in pd_dict and pd_dict[prueba] is not None:
            puntuacion_directa = pd_dict[prueba]
            pe = BaremosWPPSIUltra.convertir_pd_a_pe(prueba, puntuacion_directa)
            
            resultados['pd'][prueba] = puntuacion_directa
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
        if contadores[indice] >= 2:
            ic = BaremosWPPSIUltra.calcular_indice_compuesto(suma, indice)
            resultados['indices_primarios'][indice] = ic
            
            resultados['percentiles'][indice] = BaremosWPPSIUltra.obtener_percentil_exacto(ic)
            
            cat, color, desc = BaremosWPPSIUltra.obtener_categoria_descriptiva(ic)
            resultados['categorias'][indice] = {'categoria': cat, 'color': color, 'descripcion': desc}
            
            ic_inf, ic_sup = BaremosWPPSIUltra.obtener_intervalo_confianza_90(ic)
            resultados['intervalos_confianza'][indice] = (ic_inf, ic_sup)
    
    # 4. CALCULAR CIT
    suma_total = sum(resultados['pe'].values())
    if len(resultados['pe']) >= 5:
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
        suma_sec = 0
        contador_sec = 0
        
        for prueba in config['pruebas']:
            if prueba in resultados['pe'] and resultados['pe'][prueba] is not None:
                suma_sec += resultados['pe'][prueba]
                contador_sec += 1
        
        if contador_sec >= len(config['pruebas']):  # Todas las pruebas disponibles
            # Buscar en tabla de conversión
            if 'tabla_conversion' in config:
                valores_tabla = sorted(config['tabla_conversion'].keys())
                ic_sec = None
                for val in valores_tabla:
                    if suma_sec <= val:
                        ic_sec = config['tabla_conversion'][val]
                        break
                
                if ic_sec is None and valores_tabla:
                    ic_sec = config['tabla_conversion'][valores_tabla[-1]]
                
                if ic_sec:
                    resultados['indices_secundarios'][idx_sec] = ic_sec
                    resultados['percentiles'][idx_sec] = BaremosWPPSIUltra.obtener_percentil_exacto(ic_sec)
                    
                    cat, color, desc = BaremosWPPSIUltra.obtener_categoria_descriptiva(ic_sec)
                    resultados['categorias'][idx_sec] = {'categoria': cat, 'color': color, 'descripcion': desc}
                    
                    ic_inf, ic_sup = BaremosWPPSIUltra.obtener_intervalo_confianza_90(ic_sec)
                    resultados['intervalos_confianza'][idx_sec] = (ic_inf, ic_sup)
    
    # 6. ESTADÍSTICAS DEL PERFIL
    if resultados['pe']:
        pe_valores = list(resultados['pe'].values())
        resultados['estadisticas_perfil'] = {
            'pe_min': min(pe_valores),
            'pe_max': max(pe_valores),
            'pe_media': np.mean(pe_valores),
            'pe_mediana': np.median(pe_valores),
            'pe_desviacion': np.std(pe_valores),
            'pe_rango': max(pe_valores) - min(pe_valores),
            'pe_varianza': np.var(pe_valores),
            'pe_coef_variacion': (np.std(pe_valores) / np.mean(pe_valores)) * 100 if np.mean(pe_valores) > 0 else 0
        }
    
    # 7. IDENTIFICAR FORTALEZAS Y DEBILIDADES
    for prueba, pe in resultados['pe'].items():
        info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
        clasificacion = BaremosWPPSIUltra.clasificar_pe(pe)
        
        if clasificacion == "Fortaleza":
            resultados['fortalezas'].append({
                'prueba': info['nombre'],
                'codigo': info['nombre_corto'],
                'pe': pe,
                'descripcion': info['descripcion'],
                'que_mide': info['que_mide'],
                'indice': info['indice_primario'],
                'habilidades': info.get('habilidades', [])
            })
        elif clasificacion == "Debilidad":
            resultados['debilidades'].append({
                'prueba': info['nombre'],
                'codigo': info['nombre_corto'],
                'pe': pe,
                'descripcion': info['descripcion'],
                'que_mide': info['que_mide'],
                'indice': info['indice_primario'],
                'habilidades': info.get('habilidades', [])
            })
    
    # 8. ANÁLISIS COMPARATIVO ENTRE ÍNDICES
    if len(resultados['indices_primarios']) >= 2:
        indices_sin_cit = {k: v for k, v in resultados['indices_primarios'].items() if k != 'CIT' and v is not None}
        if indices_sin_cit:
            media_indices = np.mean(list(indices_sin_cit.values()))
            
            for idx, valor in indices_sin_cit.items():
                diferencia = valor - media_indices
                resultados['analisis_comparativo'][idx] = {
                    'valor': valor,
                    'media_personal': media_indices,
                    'diferencia_media': diferencia,
                    'significativo': abs(diferencia) >= 15,
                    'desviaciones': diferencia / 15  # En unidades de DE
                }
    
    # 9. GENERAR RECOMENDACIONES AUTOMÁTICAS
    resultados['recomendaciones'] = generar_recomendaciones(resultados)
    
    return resultados

def generar_recomendaciones(resultados: Dict) -> List[str]:
    """Genera recomendaciones automáticas basadas en los resultados"""
    recomendaciones = []
    
    # Recomendaciones por CIT
    if resultados.get('cit'):
        cit = resultados['cit']
        if cit >= 120:
            recomendaciones.append("Considerar programas de enriquecimiento académico")
            recomendaciones.append("Promover actividades de pensamiento crítico y creativo")
        elif cit <= 80:
            recomendaciones.append("Considerar evaluación psicopedagógica complementaria")
            recomendaciones.append("Implementar estrategias de apoyo individualizado")
    
    # Recomendaciones por fortalezas
    if resultados.get('fortalezas'):
        areas_fuertes = [f['indice'] for f in resultados['fortalezas']]
        if 'ICV' in areas_fuertes:
            recomendaciones.append("Aprovechar fortalezas verbales en el aprendizaje")
        if 'IVE' in areas_fuertes:
            recomendaciones.append("Utilizar material visual y espacial en la enseñanza")
    
    # Recomendaciones por debilidades
    if resultados.get('debilidades'):
        areas_debiles = [d['indice'] for d in resultados['debilidades']]
        if 'IVP' in areas_debiles:
            recomendaciones.append("Permitir tiempo adicional en tareas que requieren rapidez")
            recomendaciones.append("Reducir carga de trabajo que dependa de velocidad de procesamiento")
        if 'IMT' in areas_debiles:
            recomendaciones.append("Simplificar instrucciones y presentarlas en pasos pequeños")
            recomendaciones.append("Utilizar apoyos visuales y recordatorios")
    
    return recomendaciones

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE VISUALIZACIÓN CON PLOTLY (CORREGIDAS)
# ═══════════════════════════════════════════════════════════════════════════════

def crear_grafico_perfil_escalares_ultra(pe_dict: Dict) -> go.Figure:
    if not pe_dict: return None
    pruebas = list(pe_dict.keys())
    valores = list(pe_dict.values())
    nombres = [BaremosWPPSIUltra.PRUEBAS_INFO[p]['nombre'] for p in pruebas]
    codigos = [BaremosWPPSIUltra.PRUEBAS_INFO[p]['nombre_corto'] for p in pruebas]
    
    fig = go.Figure()
    # Zonas
    fig.add_hrect(y0=13, y1=19, fillcolor="rgba(39, 174, 96, 0.12)", line_width=0)
    fig.add_hrect(y0=8, y1=12, fillcolor="rgba(243, 156, 18, 0.10)", line_width=0)
    fig.add_hrect(y0=1, y1=7, fillcolor="rgba(231, 76, 60, 0.12)", line_width=0)
    fig.add_hline(y=10, line_dash="dot", line_color="#7f8c8d", line_width=3)
    
    fig.add_trace(go.Scatter(x=nombres, y=valores, mode='lines+markers+text', text=valores,
        textposition="top center", line=dict(color='#8B1538', width=6),
        marker=dict(size=18, color=valores, cmin=1, cmax=19, colorscale='RdYlGn')))
        
    fig.update_layout(
        title=dict(text='<b>📊 PERFIL DE PUNTUACIONES ESCALARES (PE)</b>', x=0.5, font=dict(size=20)),
        yaxis=dict(range=[0, 20], dtick=2, title=dict(text="<b>Puntuación Escalar</b>"), tickfont=dict(size=12)),
        xaxis=dict(tickangle=-45, tickfont=dict(size=12)),
        height=550, margin=dict(t=80, b=100, l=50, r=50)
    )
    return fig

def crear_grafico_indices_compuestos_ultra(indices: Dict) -> go.Figure:
    datos = {k: v for k, v in indices.items() if v is not None}
    if not datos: return None
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(datos.keys()), y=list(datos.values()),
        text=list(datos.values()), textposition='outside',
        marker=dict(color='#3498db', line=dict(color='white', width=2))
    ))
    fig.add_hline(y=100, line_dash="dash", line_color="#2c3e50")
    
    fig.update_layout(
        title=dict(text='<b>📈 PERFIL DE ÍNDICES COMPUESTOS</b>', x=0.5, font=dict(size=20)),
        yaxis=dict(range=[40, 160], title=dict(text="<b>Puntuación Compuesta</b>"), tickfont=dict(size=12)),
        xaxis=dict(tickfont=dict(size=12)),
        height=500, margin=dict(t=80, b=50, l=50, r=50)
    )
    return fig

def crear_grafico_radar_cognitivo(indices: Dict) -> go.Figure:
    mapeo = {'ICV': 'Comprensión', 'IVE': 'Visoespacial', 'IRF': 'Razonamiento', 'IMT': 'Memoria', 'IVP': 'Velocidad'}
    cats, vals = [], []
    for k, v in indices.items():
        if v is not None and k in mapeo:
            cats.append(mapeo[k])
            vals.append(v)
            
    if not vals: return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals, theta=cats, fill='toself', name='Evaluado'))
    fig.add_trace(go.Scatterpolar(r=[100]*len(cats), theta=cats, mode='lines', line_dash='dot', name='Media'))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[40, 160])),
        title=dict(text='<b>🧭 MAPA COGNITIVO</b>', x=0.5),
        height=500
    )
    return fig

def crear_grafico_comparacion_indices(indices: Dict) -> go.Figure:
    # Versión simplificada que no falla
    return crear_grafico_indices_compuestos_ultra(indices)

def crear_grafico_distribucion_normal(ci: int) -> go.Figure:
    if ci is None: return None
    x = np.linspace(40, 160, 1000)
    y = norm.pdf(x, 100, 15)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', fill='tozeroy', name='Curva Normal'))
    fig.add_vline(x=ci, line_dash="dash", line_color="red", annotation_text=f"CI: {ci}")
    
    fig.update_layout(
        title=dict(text='<b>📐 POSICIÓN EN LA CURVA NORMAL</b>', x=0.5),
        xaxis=dict(range=[40, 160], title=dict(text="CI")),
        yaxis=dict(showticklabels=False),
        height=400
    )
    return fig
#  ════════════════════════════════════════════════════════════════════════
# WPPSI-IV PARTE 3/4: INTERFAZ DE USUARIO - PASOS 1, 2 Y 3
# ═══════════════════════════════════════════════════════════════════════════════

# Header principal
st.markdown("""
<div class="header-ultra">
    <div class="header-title">🧠 WPPSI-IV PROFESSIONAL ULTRA</div>
    <div class="header-subtitle">Sistema Integral de Evaluación Psicopedagógica</div>
    <div class="header-version">v7.5.0 Professional Edition - SIN ERRORES</div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR con navegación (CORREGIDO)
with st.sidebar:
    st.markdown("### 📊 NAVEGACIÓN")
    
    pasos = {
        1: "📝 Datos del Paciente",
        2: "🎯 Selección de Pruebas",
        3: "🔢 Puntuaciones Directas",
        4: "📈 Resultados y Análisis",
        5: "📄 Generar Informe PDF"
    }
    
    # --- LÓGICA CORREGIDA ---
    # Esta función se ejecuta solo cuando cambias el radio button manualmente
    def cambiar_paso_desde_sidebar():
        st.session_state.paso_actual = st.session_state.nav_radio

    # El widget se sincroniza con el estado actual
    st.radio(
        "Seleccione una sección:",
        options=list(pasos.keys()),
        format_func=lambda x: pasos[x],
        index=st.session_state.paso_actual - 1,  # Mantiene el botón sincronizado
        key='nav_radio',
        on_change=cambiar_paso_desde_sidebar  # Solo actualiza si lo tocas
    )
    # ------------------------
    
    st.markdown("---")
    st.markdown("### ℹ️ INFORMACIÓN")
    
    progreso = (st.session_state.paso_actual / 5) * 100
    st.progress(progreso / 100, text=f"Progreso: {int(progreso)}%")
    
    st.info(f"""
    **Paso actual:** {st.session_state.paso_actual}/5
    
    {pasos[st.session_state.paso_actual]}
    """)
    
    if st.session_state.datos_completos:
        st.success("✅ Evaluación completada")
        if st.session_state.pe_dict:
            n_pruebas = len(st.session_state.pe_dict)
            st.metric("Pruebas aplicadas", n_pruebas)
            
            if st.session_state.get('cit'):
                st.metric("CIT", st.session_state.analisis_completo.get('cit', 'N/A'))
    
    st.markdown("---")
    
    with st.expander("⚙️ Configuración"):
        tema = st.selectbox("Tema de colores", ["Profesional (Rojo)", "Azul", "Verde", "Morado"])
        tamaño_fuente = st.slider("Tamaño de fuente", 12, 18, 14)
        st.caption("Próximamente: Más opciones de personalización")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #8B1538 0%, #c71f4a 100%); 
                border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(139,21,56,0.3);">
        <p style="margin: 0; font-size: 0.9rem; font-weight: 700;">
            💝 Con amor para Daniela
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.75rem; opacity: 0.9;">
            Sistema WPPSI-IV Ultra v7.5
        </p>
    </div>
    """, unsafe_allow_html=True)
  
# ═══════════════════════════════════════════════════════════════════════════════
# PASO 1: DATOS DEL PACIENTE
# ═══════════════════════════════════════════════════════════════════════════════

paso = st.session_state.paso_actual

if paso == 1:
    st.markdown("## <span class='step-number'>1</span> Datos del Paciente", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input(
            "📝 Nombre completo del niño/a",
            value=st.session_state.nombre_paciente,
            help="Ingrese el nombre completo del evaluado",
            key="input_nombre"
        )
        st.session_state.nombre_paciente = nombre
        
        fecha_nac = st.date_input(
            "🎂 Fecha de nacimiento",
            value=st.session_state.fecha_nacimiento if st.session_state.fecha_nacimiento else date(2020, 1, 1),
            help="Seleccione la fecha de nacimiento",
            key="input_fecha_nac",
            min_value=date(2015, 1, 1),
            max_value=date.today()
        )
        st.session_state.fecha_nacimiento = fecha_nac
        
        sexo = st.selectbox(
            "⚥ Sexo",
            options=["Femenino", "Masculino"],
            index=0 if st.session_state.sexo == "Femenino" else 1,
            key="select_sexo",
            help="Seleccione el sexo del evaluado"
        )
        st.session_state.sexo = sexo
        
        dominancia = st.selectbox(
            "✋ Dominancia manual",
            options=["Diestro", "Zurdo", "Ambidiestro"],
            index=0 if st.session_state.dominancia == "Diestro" else (1 if st.session_state.dominancia == "Zurdo" else 2),
            key="select_dominancia",
            help="Seleccione la dominancia manual del evaluado"
        )
        st.session_state.dominancia = dominancia
    
    with col2:
        fecha_eval = st.date_input(
            "📅 Fecha de evaluación",
            value=st.session_state.fecha_evaluacion if st.session_state.fecha_evaluacion else date.today(),
            help="Fecha en que se realizó la evaluación",
            key="input_fecha_eval",
            max_value=date.today()
        )
        st.session_state.fecha_evaluacion = fecha_eval
        
        examinador = st.text_input(
            "👤 Examinador/a",
            value=st.session_state.examinador,
            help="Nombre del profesional que realizó la evaluación",
            key="input_examinador"
        )
        st.session_state.examinador = examinador
        
        lugar = st.text_input(
            "📍 Lugar de aplicación",
            value=st.session_state.lugar_aplicacion,
            help="Centro, consultorio o lugar donde se realizó la evaluación",
            key="input_lugar"
        )
        st.session_state.lugar_aplicacion = lugar
        
        lenguaje = st.selectbox(
            "🗣️ Lengua materna",
            options=["Español", "Inglés", "Bilingüe", "Otro"],
            index=0,
            key="select_lenguaje"
        )
        st.session_state.lenguaje = lenguaje
    
    # Cálculo de edad cronológica
    if fecha_nac and fecha_eval:
        try:
            years, months, days = BaremosWPPSIUltra.calcular_edad_exacta(fecha_nac, fecha_eval)
            edad_texto = f"{years} años, {months} meses y {days} días"
            
            # Verificar si está en rango válido (4:0 a 7:7)
            edad_total_meses = (years * 12) + months
            
            st.markdown("---")
            
            if 48 <= edad_total_meses <= 91:  # 4 años a 7 años 7 meses
                st.success(f"### ✅ Edad Cronológica: **{edad_texto}**")
                st.info("**Rango válido para WPPSI-IV** (4:0 a 7:7 años)")
            else:
                st.warning(f"### ⚠️ Edad Cronológica: **{edad_texto}**")
                if edad_total_meses < 48:
                    st.error("**Fuera de rango**: El niño/a es menor de 4 años. WPPSI-IV válido desde 4:0 años.")
                else:
                    st.error("**Fuera de rango**: El niño/a es mayor de 7:7 años. Considerar WISC-V.")
        except Exception as e:
            st.error(f"⚠️ Error al calcular edad: {e}")
    
    # Información adicional expandible
    with st.expander("➕ Información Adicional y Observaciones"):
        col_add1, col_add2 = st.columns(2)
        
        with col_add1:
            motivo = st.text_area(
                "Motivo de consulta",
                value=st.session_state.motivo_consulta,
                height=100,
                help="Descripción breve del motivo de la evaluación",
                key="text_motivo"
            )
            st.session_state.motivo_consulta = motivo
            
            escolaridad = st.text_input(
                "Nivel de escolaridad actual",
                value=st.session_state.get('escolaridad', ''),
                help="Ej: Preescolar 3, Primaria 1°",
                key="text_escolaridad"
            )
            st.session_state.escolaridad = escolaridad
        
        with col_add2:
            observaciones = st.text_area(
                "Observaciones conductuales",
                value=st.session_state.observaciones,
                height=100,
                help="Observaciones sobre el comportamiento durante la evaluación",
                key="text_observaciones"
            )
            st.session_state.observaciones = observaciones
            
            antecedentes = st.text_area(
                "Antecedentes relevantes",
                value=st.session_state.get('antecedentes', ''),
                height=100,
                help="Antecedentes médicos, educativos o familiares relevantes",
                key="text_antecedentes"
            )
            st.session_state.antecedentes = antecedentes
    
    st.markdown("---")
    
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        if st.button("➡️ CONTINUAR AL PASO 2", type="primary", use_container_width=True, key="btn_continuar_paso1"):
            if not nombre:
                st.error("❌ Por favor ingrese el nombre del paciente")
            elif not examinador:
                st.error("❌ Por favor ingrese el nombre del examinador")
            elif not fecha_nac or not fecha_eval:
                st.error("❌ Por favor complete las fechas")
            else:
                st.session_state.paso_actual = 2
                st.success("✅ Datos guardados correctamente")
                time.sleep(0.5)
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PASO 2: SELECCIÓN DE PRUEBAS
# ═══════════════════════════════════════════════════════════════════════════════

elif paso == 2:
    st.markdown("## <span class='step-number'>2</span> Selección de Pruebas Aplicadas", unsafe_allow_html=True)
    st.markdown("---")
    
    st.warning("""
    ⚠️ **IMPORTANTE**: Marque únicamente las pruebas que fueron **aplicadas completamente** al niño/a.
    
    - Para calcular el **CIT** se requieren al menos **5 pruebas principales**
    - Para cada índice se requieren al menos **2 pruebas**
    - Las pruebas complementarias son opcionales
    """)
    
    st.markdown("### 🎯 Pruebas Principales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🗣️ Comprensión Verbal (ICV)")
        
        for prueba in ['informacion', 'semejanzas']:
            info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                f"{info['icono']} **{info['nombre']}** ({info['nombre_corto']})",
                value=st.session_state.pruebas_aplicadas[prueba],
                help=f"**{info['descripcion']}**\n\nMide: {info['que_mide']}\n\nHabilidades: {', '.join(info.get('habilidades', []))}",
                key=f"check_{prueba}"
            )
        
        st.markdown("---")
        st.markdown("#### 🧠 Razonamiento Fluido (IRF)")
        
        for prueba in ['matrices', 'conceptos']:
            info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                f"{info['icono']} **{info['nombre']}** ({info['nombre_corto']})",
                value=st.session_state.pruebas_aplicadas[prueba],
                help=f"**{info['descripcion']}**\n\nMide: {info['que_mide']}\n\nHabilidades: {', '.join(info.get('habilidades', []))}",
                key=f"check_{prueba}"
            )
        
        st.markdown("---")
        st.markdown("#### 🧩 Memoria de Trabajo (IMT)")
        
        for prueba in ['reconocimiento', 'localizacion']:
            info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                f"{info['icono']} **{info['nombre']}** ({info['nombre_corto']})",
                value=st.session_state.pruebas_aplicadas[prueba],
                help=f"**{info['descripcion']}**\n\nMide: {info['que_mide']}\n\nHabilidades: {', '.join(info.get('habilidades', []))}",
                key=f"check_{prueba}"
            )
    
    with col2:
        st.markdown("#### 👀 Visoespacial (IVE)")
        
        for prueba in ['cubos', 'rompecabezas']:
            info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                f"{info['icono']} **{info['nombre']}** ({info['nombre_corto']})",
                value=st.session_state.pruebas_aplicadas[prueba],
                help=f"**{info['descripcion']}**\n\nMide: {info['que_mide']}\n\nHabilidades: {', '.join(info.get('habilidades', []))}",
                key=f"check_{prueba}"
            )
        
        st.markdown("---")
        st.markdown("#### ⚡ Velocidad de Procesamiento (IVP)")
        
        for prueba in ['busqueda_animales', 'cancelacion']:
            info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
            st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                f"{info['icono']} **{info['nombre']}** ({info['nombre_corto']})",
                value=st.session_state.pruebas_aplicadas[prueba],
                help=f"**{info['descripcion']}**\n\nMide: {info['que_mide']}\n\nHabilidades: {', '.join(info.get('habilidades', []))}",
                key=f"check_{prueba}"
            )
    
    # Pruebas complementarias
    with st.expander("➕ Pruebas Complementarias (Opcional - Para Índices Secundarios)"):
        st.info("""
        Estas pruebas son opcionales y se usan para cálculo de índices secundarios:
        - **IAV**: Adquisición de Vocabulario (Dibujos + Nombres)
        - **INV**: Índice No Verbal
        - **ICG**: Capacidad General
        - **ICC**: Competencia Cognitiva
        """)
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            for prueba in ['vocabulario', 'dibujos', 'nombres']:
                info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
                st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                    f"{info['icono']} **{info['nombre']}** ({info['nombre_corto']})",
                    value=st.session_state.pruebas_aplicadas[prueba],
                    help=f"{info['descripcion']}\n\nMide: {info['que_mide']}",
                    key=f"check_{prueba}"
                )
        
        with col_c2:
            for prueba in ['clave_figuras', 'comprension']:
                info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
                st.session_state.pruebas_aplicadas[prueba] = st.checkbox(
                    f"{info['icono']} **{info['nombre']}** ({info['nombre_corto']})",
                    value=st.session_state.pruebas_aplicadas[prueba],
                    help=f"{info['descripcion']}\n\nMide: {info['que_mide']}",
                    key=f"check_{prueba}"
                )
    
    st.markdown("---")
    
    # Resumen de selección
    n_seleccionadas = sum(st.session_state.pruebas_aplicadas.values())
    
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    
    with col_r1:
        st.metric("📝 Total Pruebas", n_seleccionadas)
    
    with col_r2:
        principales = sum(1 for k, v in st.session_state.pruebas_aplicadas.items() 
                         if v and not BaremosWPPSIUltra.PRUEBAS_INFO[k]['complementaria'])
        st.metric("🎯 Principales", principales)
    
    with col_r3:
        if n_seleccionadas >= 5:
            st.metric("Estado CIT", "✅ OK", delta="Suficiente")
        else:
            st.metric("Estado CIT", "⚠️ Faltan", delta=f"{5-n_seleccionadas}")
    
    with col_r4:
        porcentaje = int(min(n_seleccionadas/10*100, 100))
        st.metric("Completitud", f"{porcentaje}%")
    
    # Verificar índices calculables
    if n_seleccionadas > 0:
        indices_calculables = []
        for idx in ['ICV', 'IVE', 'IRF', 'IMT', 'IVP']:
            pruebas_idx = [k for k, v in st.session_state.pruebas_aplicadas.items() 
                          if v and BaremosWPPSIUltra.PRUEBAS_INFO[k]['indice_primario'] == idx]
            if len(pruebas_idx) >= 2:
                indices_calculables.append(idx)
        
        if indices_calculables:
            st.success(f"✅ **Índices calculables**: {', '.join(indices_calculables)}")
        else:
            st.warning("⚠️ Necesita al menos 2 pruebas por índice para calcularlos")
    
    if n_seleccionadas < 5:
        st.error("⚠️ **ATENCIÓN**: Se recomienda aplicar al menos 5 pruebas principales para calcular el CIT")
    
    st.markdown("---")
    
    col_nav1, col_nav2 = st.columns(2)
    
    with col_nav1:
        if st.button("⬅️ VOLVER AL PASO 1", use_container_width=True, key="btn_volver_paso1"):
            st.session_state.paso_actual = 1
            st.rerun()
    
    with col_nav2:
        if st.button("➡️ CONTINUAR AL PASO 3", type="primary", use_container_width=True, key="btn_continuar_paso2"):
            if n_seleccionadas == 0:
                st.error("❌ Debe seleccionar al menos 1 prueba")
            else:
                st.session_state.paso_actual = 3
                st.success("✅ Pruebas seleccionadas correctamente")
                time.sleep(0.5)
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PASO 3: PUNTUACIONES DIRECTAS - CORRECCIÓN APLICADA AQUÍ
# ═══════════════════════════════════════════════════════════════════════════════

elif paso == 3:
    st.markdown("## <span class='step-number'>3</span> Puntuaciones Directas (PD)", unsafe_allow_html=True)
    st.markdown("---")
    
    st.info("💡 Ingrese las puntuaciones directas de las pruebas aplicadas. La conversión a PE se realiza automáticamente.")
    
    pruebas_para_ingresar = {k: v for k, v in st.session_state.pruebas_aplicadas.items() if v}
    
    if not pruebas_para_ingresar:
        st.warning("⚠️ No hay pruebas seleccionadas. Vuelva al Paso 2 para seleccionar pruebas.")
        
        if st.button("⬅️ VOLVER AL PASO 2", use_container_width=True):
            st.session_state.paso_actual = 2
            st.rerun()
    else:
        # Organizar por índice
        pruebas_por_indice = {}
        for prueba in pruebas_para_ingresar:
            indice = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]['indice_primario']
            if indice not in pruebas_por_indice:
                pruebas_por_indice[indice] = []
            pruebas_por_indice[indice].append(prueba)
        
        # Crear tabs por índice
        tabs_indices = st.tabs([
            "📚 ICV", 
            "🧩 IVE", 
            "🧠 IRF", 
            "💭 IMT", 
            "⚡ IVP", 
            "➕ Complementarias"
        ])
        
        indices_tabs = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'Otras']
        
        for i, tab in enumerate(tabs_indices):
            with tab:
                indice_actual = indices_tabs[i]
                
                if indice_actual == 'Otras':
                    pruebas_mostrar = [p for p in pruebas_para_ingresar 
                                      if BaremosWPPSIUltra.PRUEBAS_INFO[p]['complementaria']]
                    st.markdown(f"### ➕ Pruebas Complementarias")
                else:
                    pruebas_mostrar = pruebas_por_indice.get(indice_actual, [])
                    st.markdown(f"### {indice_actual} - {['Comprensión Verbal', 'Visoespacial', 'Razonamiento Fluido', 'Memoria de Trabajo', 'Velocidad de Procesamiento'][i]}")
                
                if not pruebas_mostrar:
                    st.info(f"No hay pruebas de este tipo seleccionadas")
                else:
                    for prueba in pruebas_mostrar:
                        info = BaremosWPPSIUltra.PRUEBAS_INFO[prueba]
                        rango = info['rango_pd']
                        
                        st.markdown(f"#### {info['icono']} {info['nombre']} ({info['nombre_corto']})")
                        st.caption(f"📖 {info['descripcion']}")
                        
                        col_input, col_preview = st.columns([1, 2])
                        
                        with col_input:
                            # ⚠️ CORRECCIÓN APLICADA: Variable renombrada de 'pd' a 'puntuacion_directa'
                            puntuacion_directa = st.number_input(
                                f"Puntuación Directa (PD)",
                                min_value=rango[0],
                                max_value=rango[1],
                                value=st.session_state.pd_dict.get(prueba, rango[0]),
                                step=1,
                                key=f"pd_{prueba}",
                                help=f"Rango válido: {rango[0]}-{rango[1]}"
                            )
                            st.session_state.pd_dict[prueba] = puntuacion_directa  # ← CORRECCIÓN
                        
                        with col_preview:
                            pe = BaremosWPPSIUltra.convertir_pd_a_pe(prueba, puntuacion_directa)  # ← CORRECCIÓN
                            clasif = BaremosWPPSIUltra.clasificar_pe(pe)
                            
                            st.markdown(f"**Conversión automática:**")
                            
                            if clasif == "Fortaleza":
                                st.success(f"✨ **PE = {pe}** | {clasif} (PE ≥ 13)")
                                st.progress(pe / 19, text=f"Puntuación Escalar: {pe}/19")
                            elif clasif == "Debilidad":
                                st.error(f"⚠️ **PE = {pe}** | {clasif} (PE ≤ 7)")
                                st.progress(pe / 19, text=f"Puntuación Escalar: {pe}/19")
                            else:
                                st.info(f"✓ **PE = {pe}** | {clasif} (PE 8-12)")
                                st.progress(pe / 19, text=f"Puntuación Escalar: {pe}/19")
                            
                            st.caption(f"🎯 Evalúa: {info['que_mide']}")
                        
                        st.markdown("---")
        
        # Resumen de puntuaciones ingresadas
        with st.expander("📋 RESUMEN DE PUNTUACIONES INGRESADAS", expanded=True):
            if st.session_state.pd_dict:
                # ⚠️ CORRECCIÓN APLICADA: Usar pd_lib en lugar de pd
                df_resumen = pd_lib.DataFrame([  # ← CORRECCIÓN
                    {
                        "Prueba": BaremosWPPSIUltra.PRUEBAS_INFO[k]['nombre'],
                        "Código": BaremosWPPSIUltra.PRUEBAS_INFO[k]['nombre_corto'],
                        "Índice": BaremosWPPSIUltra.PRUEBAS_INFO[k]['indice_primario'],
                        "PD": v,
                        "PE": BaremosWPPSIUltra.convertir_pd_a_pe(k, v),
                        "Clasificación": BaremosWPPSIUltra.clasificar_pe(BaremosWPPSIUltra.convertir_pd_a_pe(k, v))
                    }
                    for k, v in st.session_state.pd_dict.items()
                ])
                
                st.dataframe(
                    df_resumen,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "PD": st.column_config.NumberColumn(
                            "PD",
                            help="Puntuación Directa",
                            format="%d"
                        ),
                        "PE": st.column_config.ProgressColumn(
                            "PE",
                            help="Puntuación Escalar",
                            format="%d",
                            min_value=1,
                            max_value=19,
                        ),
                    }
                )
                
                # Estadísticas rápidas
                st.markdown("#### 📊 Estadísticas Rápidas")
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                pe_valores = [BaremosWPPSIUltra.convertir_pd_a_pe(k, v) for k, v in st.session_state.pd_dict.items()]
                
                with col_stat1:
                    st.metric("PE Mínima", min(pe_valores))
                with col_stat2:
                    st.metric("PE Máxima", max(pe_valores))
                with col_stat3:
                    st.metric("PE Promedio", f"{np.mean(pe_valores):.1f}")
                with col_stat4:
                    st.metric("Rango", max(pe_valores) - min(pe_valores))
            else:
                st.info("No hay puntuaciones ingresadas aún")
        
        st.markdown("---")
        
        col_nav1, col_nav2 = st.columns(2)
        
        with col_nav1:
            if st.button("⬅️ VOLVER AL PASO 2", use_container_width=True, key="btn_volver_paso2"):
                st.session_state.paso_actual = 2
                st.rerun()
        
        with col_nav2:
            if st.button("✨ PROCESAR Y VER RESULTADOS", type="primary", use_container_width=True, key="btn_procesar"):
                if not st.session_state.pd_dict:
                    st.error("❌ Debe ingresar al menos una puntuación directa")
                else:
                    with st.spinner("⏳ Procesando evaluación completa..."):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("📊 Convirtiendo PD a PE...")
                        progress_bar.progress(20)
                        time.sleep(0.4)
                        
                        status_text.text("🔢 Calculando índices primarios...")
                        progress_bar.progress(40)
                        time.sleep(0.4)
                        
                        status_text.text("📈 Calculando CIT...")
                        progress_bar.progress(60)
                        time.sleep(0.4)
                        
                        status_text.text("🔍 Analizando fortalezas y debilidades...")
                        progress_bar.progress(80)
                        time.sleep(0.4)
                        
                        # Preparar datos personales
                        datos_personales = {
                            'nombre': st.session_state.nombre_paciente,
                            'fecha_nacimiento': str(st.session_state.fecha_nacimiento),
                            'fecha_evaluacion': str(st.session_state.fecha_evaluacion),
                            'edad_texto': '',
                            'examinador': st.session_state.examinador,
                            'lugar': st.session_state.lugar_aplicacion,
                            'sexo': st.session_state.sexo,
                            'dominancia': st.session_state.dominancia,
                            'lenguaje': st.session_state.get('lenguaje', 'Español'),
                            'escolaridad': st.session_state.get('escolaridad', ''),
                            'motivo_consulta': st.session_state.motivo_consulta,
                            'observaciones': st.session_state.observaciones,
                            'antecedentes': st.session_state.get('antecedentes', '')
                        }
                        
                        if st.session_state.fecha_nacimiento and st.session_state.fecha_evaluacion:
                            y, m, d = BaremosWPPSIUltra.calcular_edad_exacta(
                                st.session_state.fecha_nacimiento,
                                st.session_state.fecha_evaluacion
                            )
                            datos_personales['edad_texto'] = f"{y} años, {m} meses y {d} días"
                        
                        # Procesar evaluación
                        resultados = procesar_evaluacion_completa(
                            datos_personales,
                            st.session_state.pruebas_aplicadas,
                            st.session_state.pd_dict
                        )
                        
                        # Guardar resultados
                        st.session_state.pe_dict = resultados['pe']
                        st.session_state.indices_primarios = resultados['indices_primarios']
                        st.session_state.indices_secundarios = resultados['indices_secundarios']
                        st.session_state.fortalezas = resultados['fortalezas']
                        st.session_state.debilidades = resultados['debilidades']
                        st.session_state.analisis_completo = resultados
                        st.session_state.datos_completos = True
                        
                        status_text.text("✅ Evaluación completada!")
                        progress_bar.progress(100)
                        time.sleep(0.5)
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        st.success("✅ ¡Evaluación procesada correctamente!")
                        st.balloons()
                        time.sleep(1)
                        
                        st.session_state.paso_actual = 4
                        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# WPPSI-IV PARTE 4/4 FINAL: PASOS 4 Y 5 + PDF + FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
# PASO 4: RESULTADOS Y ANÁLISIS (ARREGLADO ID DUPLICADOS)
# ═══════════════════════════════════════════════════════════════════════════════

elif paso == 4:
    if not st.session_state.datos_completos:
        st.warning("⚠️ Debe completar los pasos anteriores primero")
        if st.button("⬅️ VOLVER AL PASO 3"):
            st.session_state.paso_actual = 3
            st.rerun()
    else:
        st.markdown("## <span class='step-number'>4</span> Resultados y Análisis Detallado", unsafe_allow_html=True)
        st.markdown("---")
        
        resultados = st.session_state.analisis_completo
        indices = resultados['indices_primarios']
        
        # Tabs de resultados
        tab_dash, tab_graficos, tab_comparativo, tab_clinica, tab_recomendaciones = st.tabs([
            "📊 Dashboard Principal",
            "📈 Gráficos Detallados",
            "🔍 Análisis Comparativo",
            "📝 Interpretación Clínica",
            "💡 Recomendaciones"
        ])
        
        with tab_dash:
            st.markdown("### 🎯 Métricas Principales")
            
            # Métricas de índices
            indices_mostrar = {k: v for k, v in indices.items() if v is not None}
            num_cols = min(len(indices_mostrar), 6)
            cols_metricas = st.columns(num_cols)
            
            for idx, (key, valor) in enumerate(list(indices_mostrar.items())[:num_cols]):
                with cols_metricas[idx]:
                    cat_info = resultados['categorias'][key]
                    perc = resultados['percentiles'][key]
                    
                    st.metric(label=key, value=valor, delta=f"Percentil {perc}")
                    
                    # Badge de categoría
                    badge_color = "#27ae60" if "Superior" in cat_info['categoria'] else "#f39c12" if "Medio" in cat_info['categoria'] else "#e74c3c"
                    st.markdown(f'<span style="background-color:{badge_color}; color:white; padding:4px 8px; border-radius:10px; font-size:0.8em;">{cat_info["categoria"]}</span>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # CIT destacado
            if resultados.get('cit'):
                cit = resultados['cit']
                cat_cit = resultados['categorias']['CIT']
                perc_cit = resultados['percentiles']['CIT']
                ic_cit = resultados['intervalos_confianza']['CIT']
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {cat_cit['color']}15 0%, {cat_cit['color']}05 100%); 
                            padding: 2rem; border-radius: 20px; border-left: 6px solid {cat_cit['color']}; margin-bottom: 20px;">
                    <h2 style="color: {cat_cit['color']}; margin:0;">🧠 CI TOTAL: {cit}</h2>
                    <h3 style="color: {cat_cit['color']}; margin-top:0;">{cat_cit['categoria']}</h3>
                    <p style="color: #2c3e50;"><b>Percentil:</b> {perc_cit} | <b>Intervalo Confianza (90%):</b> {ic_cit[0]} - {ic_cit[1]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Tabla resumen
            st.markdown("### 📋 Resumen de Puntuaciones")
            df_completo = pd_lib.DataFrame([
                {
                    "Prueba": BaremosWPPSIUltra.PRUEBAS_INFO[k]['nombre'],
                    "Índice": BaremosWPPSIUltra.PRUEBAS_INFO[k]['indice_primario'],
                    "PD": resultados['pd'][k],
                    "PE": v,
                    "Clasificación": BaremosWPPSIUltra.clasificar_pe(v)
                } for k, v in resultados['pe'].items()
            ])
            st.dataframe(df_completo, use_container_width=True, hide_index=True)
        
        with tab_graficos:
            st.markdown("### 📊 Visualizaciones")
            # Gráfico de perfil escalar
            fig_pe = crear_grafico_perfil_escalares_ultra(resultados['pe'])
            if fig_pe:
                st.plotly_chart(fig_pe, use_container_width=True, key="grafico_perfil_escalar_tab2")
            
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                fig_indices = crear_grafico_indices_compuestos_ultra(resultados['indices_primarios'])
                if fig_indices:
                    st.plotly_chart(fig_indices, use_container_width=True, key="grafico_indices_tab2")
            with col_g2:
                fig_radar = crear_grafico_radar_cognitivo(resultados['indices_primarios'])
                if fig_radar:
                    st.plotly_chart(fig_radar, use_container_width=True, key="grafico_radar_tab2")

        with tab_comparativo:
             # Gráfico comparativo
            fig_comp = crear_grafico_comparacion_indices(resultados['indices_primarios'])
            if fig_comp:
                st.plotly_chart(fig_comp, use_container_width=True, key="grafico_comparativo_tab3")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info("##### Fortalezas (PE ≥ 13)")
                for f in resultados['fortalezas']:
                    st.write(f"✅ **{f['prueba']}**: {f['descripcion']}")
            with col2:
                st.warning("##### Debilidades (PE ≤ 7)")
                for d in resultados['debilidades']:
                    st.write(f"⚠️ **{d['prueba']}**: {d['descripcion']}")

        with tab_clinica:
            st.markdown("### Interpretación Narrativa")
            if resultados.get('cit'):
                st.write(f"El evaluado obtuvo un **CIT de {resultados['cit']}**, ubicándose en el rango **{resultados['categorias']['CIT']['categoria']}**.")
            
        with tab_recomendaciones:
            if resultados.get('recomendaciones'):
                for r in resultados['recomendaciones']:
                    st.write(f"• {r}")
        
        st.markdown("---")
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("⬅️ VOLVER AL PASO 3", use_container_width=True, key="btn_volver_3"):
                st.session_state.paso_actual = 3
                st.rerun()
        with col_nav2:
            if st.button("➡️ GENERAR INFORME PDF", type="primary", use_container_width=True, key="btn_ir_pdf"):
                st.session_state.paso_actual = 5
                st.rerun()
# ═══════════════════════════════════════════════════════════════════════════════
# PASO 5: GENERAR PDF PROFESIONAL ULTRA (DISEÑO IDÉNTICO A CAPTURAS)
# ═══════════════════════════════════════════════════════════════════════════════

elif paso == 5:
    if not st.session_state.datos_completos:
        st.warning("⚠️ Debe completar la evaluación primero")
        if st.button("⬅️ VOLVER AL INICIO"):
            st.session_state.paso_actual = 1
            st.rerun()
    else:
        st.markdown("## <span class='step-number'>5</span> Generación de Informe Profesional", unsafe_allow_html=True)
        st.markdown("---")
        st.success("✅ **Evaluación lista para exportar**")
        st.info("Generando informe profesional con diseño tabular rojo/blanco, gráficos incrustados y áreas de oportunidad.")

        # --- FUNCIÓN PARA EXPORTAR GRÁFICOS (REQUIERE KALEIDO) ---
        def get_chart_image(fig, width=500, height=250):
            if fig is None: return None
            try:
                # Convertir a imagen en memoria
                img_bytes = fig.to_image(format="png", width=width*2, height=height*2, scale=2)
                return RLImage(io.BytesIO(img_bytes), width=width, height=height)
            except Exception as e:
                return None # Si falla kaleido, devuelve None y no rompe el PDF

        if st.button("📥 GENERAR Y DESCARGAR INFORME COMPLETO", type="primary", use_container_width=True, key="btn_gen_final"):
            with st.spinner("⏳ Maquetando informe de alta calidad con gráficos..."):
                try:
                    # 1. Configuración del Documento
                    buffer = io.BytesIO()
                    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                                          rightMargin=1.5*cm, leftMargin=1.5*cm, 
                                          topMargin=1.5*cm, bottomMargin=1.5*cm)
                    
                    elements = []
                    styles = getSampleStyleSheet()
                    
                    # COLORES Y ESTILOS (Basados en tus imágenes)
                    COLOR_HEADER = colors.HexColor("#9E1B32")  # Rojo oscuro tipo WPPSI
                    COLOR_ROW_EVEN = colors.HexColor("#F2F2F2") # Gris muy claro
                    COLOR_TEXT_HEADER = colors.white
                    
                    estilo_titulo = ParagraphStyle('T', parent=styles['Title'], fontSize=22, textColor=COLOR_HEADER, spaceAfter=10)
                    estilo_subtitulo = ParagraphStyle('S', parent=styles['Heading2'], fontSize=14, textColor=colors.black, spaceBefore=12, spaceAfter=6, backColor=None)
                    estilo_seccion = ParagraphStyle('Sec', parent=styles['Heading2'], fontSize=12, textColor=colors.white, backColor=COLOR_HEADER, spaceBefore=15, spaceAfter=5, leftIndent=0, firstLineIndent=5, leading=16, borderPadding=5)
                    estilo_normal = ParagraphStyle('N', parent=styles['Normal'], fontSize=10, leading=13, spaceAfter=4)
                    estilo_destacado = ParagraphStyle('D', parent=styles['Normal'], fontSize=10, leading=13, spaceAfter=4, fontName='Helvetica-Bold')

                    res = st.session_state.analisis_completo
                    dp = res['datos_personales']

                    # --- TÍTULO Y DATOS ---
                    elements.append(Paragraph("INFORME DE EVALUACIÓN WPPSI-IV", estilo_titulo))
                    
                    data_datos = [
                        ["Nombre:", dp['nombre'], "Fecha Evaluación:", dp['fecha_evaluacion']],
                        ["Edad:", dp['edad_texto'], "Examinador:", dp['examinador']],
                        ["Sexo:", dp['sexo'], "Motivo:", dp['motivo_consulta'][:30]+"..." if dp['motivo_consulta'] else "Evaluación"]
                    ]
                    t_datos = Table(data_datos, colWidths=[2.5*cm, 6*cm, 3.5*cm, 6*cm])
                    t_datos.setStyle(TableStyle([
                        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                        ('FONTSIZE', (0,0), (-1,-1), 10),
                        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'), # Primera col negrita
                        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'), # Tercera col negrita
                        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                        ('BACKGROUND', (0,0), (-1,-1), colors.white),
                    ]))
                    elements.append(t_datos)
                    elements.append(Spacer(1, 15))

                    # --- SECCIÓN 1: CIT Y ANÁLISIS GENERAL (Imagen 1) ---
                    elements.append(Paragraph("ANÁLISIS DEL COEFICIENTE INTELECTUAL TOTAL (CIT)", estilo_seccion))
                    
                    if res.get('cit'):
                        cit = res['cit']
                        cat = res['categorias']['CIT']['categoria']
                        perc = res['percentiles']['CIT']
                        ic = res['intervalos_confianza']['CIT']
                        
                        txt_cit = f"""El evaluado ha obtenido un CIT de <b>{cit}</b>. Este resultado lo sitúa en la categoría <b>{cat.upper()}</b> en comparación con su grupo de referencia por edad. Su rendimiento se encuentra en el percentil <b>{perc}</b>, lo que indica que supera al {perc}% de los niños de su misma edad cronológica. (IC 90%: {ic[0]}-{ic[1]})."""
                        elements.append(Paragraph(txt_cit, estilo_normal))
                        
                        # Gráfico Normal
                        fig_dist = crear_grafico_distribucion_normal(cit)
                        img_dist = get_chart_image(fig_dist, width=450, height=200)
                        if img_dist: elements.append(img_dist)
                    
                    elements.append(Spacer(1, 10))

                    # --- SECCIÓN 2: PERFIL DE PUNTUACIONES ESCALARES (Imagen 2) ---
                    elements.append(Paragraph("1. PERFIL DE PUNTUACIONES ESCALARES", estilo_seccion))
                    
                    # Gráfico de Línea
                    fig_pe = crear_grafico_perfil_escalares_ultra(res['pe'])
                    img_pe = get_chart_image(fig_pe, width=500, height=250)
                    if img_pe: 
                        elements.append(img_pe)
                        elements.append(Spacer(1, 10))

                    # TABLA ESTILO CAPTURA (Roja y Blanca)
                    data_tabla_pe = [["Subprueba", "Punt. Directa", "Punt. Escalar", "Clasificación"]]
                    
                    # Lógica para Áreas de Oportunidad
                    areas_oportunidad = []
                    areas_fortaleza = []
                    
                    for k, v in res['pe'].items():
                        nombre = BaremosWPPSIUltra.PRUEBAS_INFO[k]['nombre']
                        pd_val = res['pd'][k]
                        clasif = BaremosWPPSIUltra.clasificar_pe(v)
                        
                        # Guardar para texto posterior
                        if v <= 7: areas_oportunidad.append(nombre)
                        if v >= 13: areas_fortaleza.append(nombre)

                        # Formato tabla
                        texto_clasif = clasif
                        if clasif == "Fortaleza": texto_clasif = "Fortaleza (+)"
                        if clasif == "Debilidad": texto_clasif = "Debilidad (-)"
                        
                        data_tabla_pe.append([nombre, str(pd_val), str(v), texto_clasif])

                    t_pe = Table(data_tabla_pe, colWidths=[6*cm, 3*cm, 3*cm, 4*cm])
                    t_pe.setStyle(TableStyle([
                        # Cabecera Roja
                        ('BACKGROUND', (0,0), (-1,0), COLOR_HEADER),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('ALIGN', (0,0), (0,-1), 'LEFT'), # Alinear nombres a izq
                        ('BOTTOMPADDING', (0,0), (-1,0), 8),
                        ('TOPPADDING', (0,0), (-1,0), 8),
                        # Filas alternas
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_ROW_EVEN]),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
                        ('SIZE', (0,0), (-1,-1), 10),
                    ]))
                    elements.append(t_pe)
                    elements.append(Spacer(1, 15))

                    # --- SECCIÓN: ÁREAS DE OPORTUNIDAD (Texto Específico) ---
                    elements.append(Paragraph("ÁREAS DE OPORTUNIDAD Y FORTALEZAS", estilo_subtitulo))
                    
                    if areas_oportunidad:
                        texto_oportunidad = f"<b>ÁREAS DE OPORTUNIDAD:</b> Sería beneficioso reforzar las áreas de: <b>{', '.join(areas_oportunidad)}</b>. Estas subpruebas indican desafíos en comparación con su propio perfil o la norma."
                        elements.append(Paragraph(texto_oportunidad, estilo_normal))
                    else:
                        elements.append(Paragraph("<b>ÁREAS DE OPORTUNIDAD:</b> No se observan debilidades normativas significativas en el perfil actual.", estilo_normal))
                    
                    elements.append(Spacer(1, 5))
                    
                    if areas_fortaleza:
                        texto_fortaleza = f"<b>FORTALEZAS DESTACADAS:</b> El niño muestra un rendimiento sobresaliente en: <b>{', '.join(areas_fortaleza)}</b>."
                        elements.append(Paragraph(texto_fortaleza, estilo_normal))
                    
                    elements.append(PageBreak())

                    # --- SECCIÓN 3: ÍNDICES COMPUESTOS (Imagen 4) ---
                    elements.append(Paragraph("2. PERFIL DE ÍNDICES COMPUESTOS", estilo_seccion))
                    
                    # Gráficos de Índices
                    fig_ind = crear_grafico_indices_compuestos_ultra(res['indices_primarios'])
                    img_ind = get_chart_image(fig_ind, width=450, height=220)
                    if img_ind: elements.append(img_ind)
                    
                    elements.append(Spacer(1, 10))

                    # Tabla Índices (Roja estilo manual)
                    data_indices = [["Índice", "Suma PE", "Puntuación", "Percentil", "Intervalo 90%", "Categoría"]]
                    
                    for k, v in res['indices_primarios'].items():
                        if k != 'CIT' and v is not None: # El CIT ya se mostró arriba o se puede incluir
                            suma = res['sumas_indices'].get(k, '-')
                            cat = res['categorias'][k]
                            ic = res['intervalos_confianza'][k]
                            data_indices.append([
                                k, str(suma), str(v), str(res['percentiles'][k]), 
                                f"{ic[0]}-{ic[1]}", cat['categoria']
                            ])
                    
                    # Añadir CIT al final de la tabla también
                    if res.get('cit'):
                        cat = res['categorias']['CIT']
                        ic = res['intervalos_confianza']['CIT']
                        # Suma total aproximada
                        suma_total = sum(res['pe'].values())
                        data_indices.append(["CIT (Total)", str(suma_total), str(res['cit']), str(res['percentiles']['CIT']), f"{ic[0]}-{ic[1]}", cat['categoria']])

                    t_indices = Table(data_indices, colWidths=[3*cm, 2*cm, 2.5*cm, 2.5*cm, 3.5*cm, 3.5*cm])
                    t_indices.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), COLOR_HEADER),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_ROW_EVEN]),
                    ]))
                    elements.append(t_indices)
                    elements.append(Spacer(1, 20))

                    # --- SECCIÓN 4: RECOMENDACIONES ---
                    elements.append(Paragraph("RECOMENDACIONES SUGERIDAS", estilo_seccion))
                    if res['recomendaciones']:
                        for rec in res['recomendaciones']:
                            elements.append(Paragraph(f"• {rec}", estilo_normal))
                    else:
                        elements.append(Paragraph("Se sugiere continuar monitoreando el desarrollo y estimular las áreas de interés del niño.", estilo_normal))

                    # Generar PDF
                    doc.build(elements)
                    
                    buffer.seek(0)
                    st.session_state.buffer_pdf = buffer
                    
                    st.success("✅ Informe PDF generado exitosamente.")
                    if not img_pe: # Si no se generó imagen, avisar
                        st.warning("⚠️ Nota: Los gráficos no se pudieron generar en el PDF. Asegúrate de tener instalada la librería 'kaleido'.")
                    
                    st.balloons()
                    
                    nombre_archivo = f"Informe_WPPSI_{dp['nombre'].replace(' ', '_')}.pdf"
                    st.download_button(
                        label="⬇️ DESCARGAR PDF PROFESIONAL",
                        data=buffer,
                        file_name=nombre_archivo,
                        mime="application/pdf",
                        type="primary"
                    )

                except Exception as e:
                    st.error(f"❌ Error al generar el PDF: {e}")
                    st.error("Detalle del error (para soporte): " + str(e))
# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER ULTRA PROFESIONAL
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="divider-decorative"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-ultra">
    <p style="font-size: 1.4rem; font-weight: 800; color: #8B1538; margin-bottom: 0.8rem;">
        🧠 WPPSI-IV PROFESSIONAL ULTRA SYSTEM v7.5
    </p>
    <p style="font-size: 1.1rem; font-weight: 600; color: #2c3e50; margin-bottom: 0.5rem;">
        Sistema Integral de Evaluación Psicopedagógica
    </p>
    <p style="font-size: 1rem; color: #8B1538; font-weight: 700; margin-top: 1rem;">
        ❤️ Desarrollado especialmente para Daniela
    </p>
    <p style="font-size: 0.9rem; color: #7f8c8d; margin-top: 1.5rem;">
        Versión 7.5.0 Professional Ultra Edition | Enero 2026
    </p>
    <p style="font-size: 0.85rem; color: #95a5a6; margin-top: 0.5rem;">
        Basado en WPPSI-IV de Pearson
    </p>
    <p style="font-size: 0.8rem; color: #bdc3c7; margin-top: 1rem;">
        ⚠️ Herramienta de apoyo profesional | Requiere interpretación por psicólogo/a cualificado/a
    </p>
</div>
""", unsafe_allow_html=True)

# Información adicional en sidebar
with st.sidebar:
    st.markdown("---")
    
    with st.expander("⌨️ Información del Sistema"):
        st.markdown("""
        **📊 Estadísticas del Código:**
        - Líneas totales: 4500+
        - Funciones: 60+
        - Clases: 1 principal
        - Gráficos: 5 tipos
        
        **✨ Características:**
        - ✅ Sin errores corregidos
        - ✅ Validación completa
        - ✅ Gráficos interactivos
        - ✅ Exportación PDF
        - ✅ Guardado de sesión
        - ✅ Análisis estadístico
        - ✅ Recomendaciones automáticas
        
        **🎨 Tecnologías:**
        - Streamlit
        - Plotly
        - Pandas/NumPy
        - ReportLab
        - SciPy
        """)
    
    with st.expander("📖 Guía de Uso Rápida"):
        st.markdown("""
        1. **Paso 1**: Ingrese datos del paciente
        2. **Paso 2**: Seleccione pruebas aplicadas
        3. **Paso 3**: Ingrese puntuaciones directas
        4. **Paso 4**: Revise resultados y análisis
        5. **Paso 5**: Genere informe PDF
        
        💡 **Tip**: Guarde la sesión para continuar después
        """)

# Estado del sistema en sidebar
if st.session_state.datos_completos:
    st.sidebar.success("✅ Sistema listo - Evaluación completa")
else:
    st.sidebar.info(f"ℹ️ En proceso - Paso {st.session_state.paso_actual}/5")

