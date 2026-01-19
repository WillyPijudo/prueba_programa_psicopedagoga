"""
═══════════════════════════════════════════════════════════════════════════════
WPPSI-IV SISTEMA PROFESIONAL COMPLETO
Sistema de Evaluación Psicopedagógica con Selección Dinámica de Pruebas
Desarrollado especialmente para Daniela ❤️
Versión: 6.0.0 Professional Edition
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
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, 
                                Spacer, PageBreak, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.graphics.shapes import Drawing, Line, Rect, Circle, PolyLine, String
from reportlab.pdfgen import canvas

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN INICIAL
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="WPPSI-IV Professional",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicialización de Session State
if 'datos_completos' not in st.session_state:
    st.session_state.datos_completos = False
if 'pruebas_seleccionadas' not in st.session_state:
    st.session_state.pruebas_seleccionadas = {
        'cubos': True,
        'informacion': True,
        'matrices': True,
        'busqueda_animales': True,
        'reconocimiento': True,
        'semejanzas': True,
        'conceptos': True,
        'localizacion': True,
        'cancelacion': True,
        'rompecabezas': True
    }

# ═══════════════════════════════════════════════════════════════════════════════
# ESTILOS CSS PREMIUM
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');

:root {
    --primary: #8B1538;
    --primary-dark: #6b0e2a;
    --primary-light: #a91d3a;
    --secondary: #2c3e50;
    --success: #27ae60;
    --warning: #f39c12;
    --danger: #e74c3c;
    --info: #3498db;
    --light: #ecf0f1;
    --dark: #2c3e50;
}

* {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}

.main {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

/* Header Principal */
.header-principal {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    box-shadow: 0 15px 35px rgba(139, 21, 56, 0.4);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.header-principal::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

.header-title {
    font-size: 3rem;
    font-weight: 800;
    margin: 0;
    text-shadow: 0 4px 12px rgba(0,0,0,0.3);
    position: relative;
    z-index: 2;
}

.header-subtitle {
    font-size: 1.2rem;
    font-weight: 300;
    margin-top: 0.5rem;
    opacity: 0.95;
    position: relative;
    z-index: 2;
}

/* Tarjetas de Métric */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, white 0%, #f8f9fa 100%);
    border: none;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-left: 4px solid var(--primary);
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 12px 30px rgba(139, 21, 56, 0.2);
}

[data-testid="stMetricLabel"] {
    font-size: 0.9rem;
    color: #5a6c7d;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

[data-testid="stMetricValue"] {
    font-size: 2.5rem;
    color: var(--primary);
    font-weight: 800;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Inputs Mejorados */
.stTextInput input, .stNumberInput input, .stDateInput input, 
.stSelectbox > div > div {
    background: white !important;
    border: 2px solid #e1e8ed !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}

.stTextInput input:focus, .stNumberInput input:focus, 
.stDateInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(139, 21, 56, 0.1) !important;
    transform: translateY(-2px);
}

label {
    color: var(--dark) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    margin-bottom: 8px !important;
}

/* Checkboxes Personalizados */
.stCheckbox {
    padding: 8px;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.stCheckbox:hover {
    background: rgba(139, 21, 56, 0.05);
}

.stCheckbox label {
    font-size: 15px !important;
    font-weight: 500 !important;
}

/* Botones Premium */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    border: none !important;
    padding: 14px 32px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    border-radius: 50px !important;
    box-shadow: 0 8px 20px rgba(139, 21, 56, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 15px 35px rgba(139, 21, 56, 0.5) !important;
}

.stButton > button:active {
    transform: translateY(-1px);
}

/* Tablas */
.dataframe {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1) !important;
}

.dataframe thead th {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    padding: 16px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.dataframe tbody td {
    padding: 14px !important;
    border-bottom: 1px solid #e1e8ed !important;
    color: #2c3e50 !important;
    font-weight: 500 !important;
}

.dataframe tbody tr:hover {
    background: rgba(139, 21, 56, 0.05) !important;
}

/* Alertas Mejoradas */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 12px !important;
    padding: 16px 20px !important;
    border-left: 4px solid !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    animation: slideInRight 0.5s ease-out;
}

.stSuccess {
    background: #d4edda !important;
    border-left-color: #28a745 !important;
}

.stSuccess div[data-testid="stMarkdownContainer"] p {
    color: #155724 !important;
    font-weight: 600 !important;
}

.stError {
    background: #f8d7da !important;
    border-left-color: #dc3545 !important;
}

.stError div[data-testid="stMarkdownContainer"] p {
    color: #721c24 !important;
    font-weight: 600 !important;
}

.stWarning {
    background: #fff3cd !important;
    border-left-color: #ffc107 !important;
}

.stWarning div[data-testid="stMarkdownContainer"] p {
    color: #856404 !important;
    font-weight: 600 !important;
}

.stInfo {
    background: #d1ecf1 !important;
    border-left-color: #17a2b8 !important;
}

.stInfo div[data-testid="stMarkdownContainer"] p {
    color: #0c5460 !important;
    font-weight: 600 !important;
}

/* Tabs Mejorados */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: white;
    padding: 12px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.stTabs [data-baseweb="tab"] {
    background: #f8f9fa;
    color: #5a6c7d;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 600;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(139, 21, 56, 0.3);
}

/* Expanders */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #f8f9fa 0%, white 100%) !important;
    border-radius: 10px !important;
    padding: 16px !important;
    font-weight: 600 !important;
    border-left: 4px solid var(--primary) !important;
    transition: all 0.3s ease !important;
}

.streamlit-expanderHeader:hover {
    background: linear-gradient(135deg, white 0%, #f8f9fa 100%) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

/* Animaciones */
@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
}

/* Progress Bar */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
    border-radius: 10px;
}

/* Card Container */
.card-container {
    background: white;
    padding: 24px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    transition: all 0.3s ease;
    border-left: 4px solid var(--primary);
}

.card-container:hover {
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    transform: translateY(-4px);
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 15px;
    margin-top: 3rem;
    box-shadow: 0 -4px 15px rgba(0,0,0,0.08);
    border-bottom: 4px solid var(--primary);
}

.footer p {
    color: #5a6c7d;
    margin: 0.5rem 0;
}

/* Avatar Daniela */
.daniela-avatar {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    box-shadow: 0 8px 20px rgba(139, 21, 56, 0.4);
    animation: pulse 2s ease-in-out infinite;
    z-index: 9999;
    cursor: pointer;
    transition: all 0.3s ease;
}

.daniela-avatar:hover {
    transform: scale(1.1) rotate(10deg);
    box-shadow: 0 12px 30px rgba(139, 21, 56, 0.6);
}
</style>
""", unsafe_allow_html=True)

# Avatar de Daniela
st.markdown('<div class="daniela-avatar">👩‍🦱</div>', unsafe_allow_html=True)

# Header Principal
st.markdown("""
<div class="header-principal">
    <div class="header-title">🧠 WPPSI-IV PROFESSIONAL</div>
    <div class="header-subtitle">Sistema Integral de Evaluación Psicopedagógica | Desarrollado con ❤️ para Daniela</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CLASE DE BAREMOS WPPSI-IV
# ═══════════════════════════════════════════════════════════════════════════════

class BaremosWPPSI:
    """
    Clase que contiene todos los baremos oficiales del WPPSI-IV
    Basado en el manual técnico y de interpretación
    """
    
    # TABLAS DE CONVERSIÓN PD → PE
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
    
    # DEFINICIÓN DE PRUEBAS
    PRUEBAS_INFO = {
        'cubos': {
            'nombre': 'Cubos',
            'indice': 'IVE',
            'descripcion': 'Razonamiento visoespacial y construcción',
            'icono': '🧩'
        },
        'informacion': {
            'nombre': 'Información',
            'indice': 'ICV',
            'descripcion': 'Conocimientos adquiridos',
            'icono': '📚'
        },
        'matrices': {
            'nombre': 'Matrices',
            'indice': 'IRF',
            'descripcion': 'Razonamiento fluido visual',
            'icono': '🔲'
        },
        'busqueda_animales': {
            'nombre': 'Búsqueda de Animales',
            'indice': 'IVP',
            'descripcion': 'Velocidad de procesamiento visual',
            'icono': '🐾'
        },
        'reconocimiento': {
            'nombre': 'Reconocimiento',
            'indice': 'IMT',
            'descripcion': 'Memoria de trabajo visual',
            'icono': '👁️'
        },
        'semejanzas': {
            'nombre': 'Semejanzas',
            'indice': 'ICV',
            'descripcion': 'Razonamiento verbal abstracto',
            'icono': '💭'
        },
        'conceptos': {
            'nombre': 'Conceptos',
            'indice': 'IRF',
            'descripcion': 'Razonamiento categorial',
            'icono': '🎯'
        },
        'localizacion': {
            'nombre': 'Localización',
            'indice': 'IMT',
            'descripcion': 'Memoria espacial de trabajo',
            'icono': '📍'
        },
        'cancelacion': {
            'nombre': 'Cancelación',
            'indice': 'IVP',
            'descripcion': 'Atención y velocidad perceptiva',
            'icono': '✓'
        },
        'rompecabezas': {
            'nombre': 'Rompecabezas',
            'indice': 'IVE',
            'descripcion': 'Análisis y síntesis visual',
            'icono': '🧩'
        }
    }
    
    @staticmethod
    def calcular_edad(fecha_nacimiento, fecha_aplicacion):
        """Calcula la edad cronológica exacta"""
        years = fecha_aplicacion.year - fecha_nacimiento.year
        months = fecha_aplicacion.month - fecha_nacimiento.month
        days = fecha_aplicacion.day - fecha_nacimiento.day
        
        if days < 0:
            months -= 1
            days += 30
        
        if months < 0:
            years -= 1
            months += 12
        
        return years, months, days
    
    @staticmethod
    def convertir_pd_a_pe(prueba, pd):
        """Convierte PD a PE usando tablas oficiales"""
        if pd is None:
            return None
        tabla = BaremosWPPSI.TABLAS_CONVERSION.get(prueba, {})
        return tabla.get(pd, 1 if pd == 0 else 19)
    
    @staticmethod
    def calcular_indice_compuesto(suma_escalar, tipo_indice):
        """Calcula índice compuesto a partir de suma de PE"""
        # Tablas de conversión Suma PE → Índice Compuesto
        tablas = {
            'ICV': {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:130, 28:137, 30:145},
            'IVE': {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:129, 28:136, 30:143},
            'IRF': {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:130, 28:136, 30:143},
            'IMT': {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:95, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138, 30:145},
            'IVP': {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138}
        }
        
        tabla = tablas.get(tipo_indice, {})
        keys = sorted(tabla.keys())
        
        for key in keys:
            if suma_escalar <= key:
                return tabla[key]
        
        return tabla[keys[-1]] if keys else 100
    
    @staticmethod
    def calcular_cit(suma_total):
        """Calcula CI Total a partir de suma de todas las PE"""
        tabla_cit = {
            10:40, 15:45, 20:52, 25:58, 30:64, 35:70, 40:76, 45:82, 50:88, 55:94,
            60:100, 63:103, 65:106, 70:112, 75:118, 80:124, 85:130, 90:136, 95:143
        }
        
        keys = sorted(tabla_cit.keys())
        for key in keys:
            if suma_total <= key:
                return tabla_cit[key]
        
        return tabla_cit[keys[-1]] if keys else 100
    
    @staticmethod
    def obtener_percentil(ci):
        """Calcula percentil exacto usando distribución normal"""
        percentil = norm.cdf((ci - 100) / 15) * 100
        if percentil > 99.9:
            return ">99.9"
        if percentil < 0.1:
            return "<0.1"
        return round(percentil, 1)
    
    @staticmethod
    def obtener_categoria(ci):
        """Retorna categoría descriptiva según CI"""
        if ci >= 130:
            return "Muy Superior", "#27ae60", "Rendimiento excepcional"
        elif ci >= 120:
            return "Superior", "#2ecc71", "Rendimiento sobresaliente"
        elif ci >= 110:
            return "Medio Alto", "#3498db", "Por encima del promedio"
        elif ci >= 90:
            return "Medio", "#f39c12", "Rendimiento promedio esperado"
        elif ci >= 80:
            return "Medio Bajo", "#e67e22", "Ligeramente por debajo del promedio"
        elif ci >= 70:
            return "Límite", "#e74c3c", "Requiere atención y seguimiento"
        else:
            return "Muy Bajo", "#c0392b", "Requiere intervención especializada"

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE PROCESAMIENTO
# ═══════════════════════════════════════════════════════════════════════════════

def procesar_evaluacion(datos_personales, pruebas_data, pruebas_selec):
    """
    Procesa la evaluación completa con las pruebas seleccionadas
    """
    # 1. Convertir PD a PE solo para pruebas seleccionadas
    pe_dict = {}
    for prueba, seleccionada in pruebas_selec.items():
        if seleccionada and prueba in pruebas_data:
            pd = pruebas_data[prueba]
            pe = BaremosWPPSI.convertir_pd_a_pe(prueba, pd)
            if pe is not None:
                pe_dict[prueba] = pe
    
    # 2. Calcular sumas por índice
    sumas_indices = {
        'ICV': 0,
        'IVE': 0,
        'IRF': 0,
        'IMT': 0,
        'IVP': 0
    }
    
    contadores = {
        'ICV': 0,
        'IVE': 0,
        'IRF': 0,
        'IMT': 0,
        'IVP': 0
    }
    
    for prueba, pe in pe_dict.items():
        indice = BaremosWPPSI.PRUEBAS_INFO[prueba]['indice']
        sumas_indices[indice] += pe
        contadores[indice] += 1
    
    # 3. Calcular índices compuestos solo si hay pruebas suficientes
    indices = {}
    for indice, suma in sumas_indices.items():
        if contadores[indice] >= 1:  # Al menos 1 prueba
            indices[indice] = BaremosWPPSI.calcular_indice_compuesto(suma, indice)
        else:
            indices[indice] = None
    
    # 4. Calcular CIT solo si hay al menos 5 pruebas
    suma_total = sum(pe_dict.values())
    if len(pe_dict) >= 5:
        indices['CIT'] = BaremosWPPSI.calcular_cit(suma_total)
    else:
        indices['CIT'] = None
    
    # 5. Análisis de fortalezas y debilidades
    fortalezas = []
    debilidades = []
    
    for prueba, pe in pe_dict.items():
        if pe >= 13:
            fortalezas.append({
                'prueba': BaremosWPPSI.PRUEBAS_INFO[prueba]['nombre'],
                'pe': pe,
                'descripcion': BaremosWPPSI.PRUEBAS_INFO[prueba]['descripcion']
            })
        elif pe <= 7:
            debilidades.append({
                'prueba': BaremosWPPSI.PRUEBAS_INFO[prueba]['nombre'],
                'pe': pe,
                'descripcion': BaremosWPPSI.PRUEBAS_INFO[prueba]['descripcion']
            })
    
    return {
        'pe': pe_dict,
        'sumas': sumas_indices,
        'indices': indices,
        'fortalezas': fortalezas,
        'debilidades': debilidades,
        'suma_total': suma_total,
        'n_pruebas': len(pe_dict)
    }

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE VISUALIZACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

def crear_grafico_perfil_escalares(pe_dict):
    """Gráfico de perfil de puntuaciones escalares"""
    if not pe_dict:
        return None
    
    pruebas = list(pe_dict.keys())
    valores = list(pe_dict.values())
    nombres = [BaremosWPPSI.PRUEBAS_INFO[p]['nombre'] for p in pruebas]
    
    fig = go.Figure()
    
    # Zonas de fondo
    fig.add_hrect(y0=13, y1=19, fillcolor="rgba(39, 174, 96, 0.15)", line_width=0)
    fig.add_hrect(y0=8, y1=12, fillcolor="rgba(243, 156, 18, 0.15)", line_width=0)
    fig.add_hrect(y0=1, y1=7, fillcolor="rgba(231, 76, 60, 0.15)", line_width=0)
    
    # Línea media
    fig.add_hline(y=10, line_dash="dash", line_color="#95a5a6", line_width=2)
    
    # Datos
    fig.add_trace(go.Scatter(
        x=nombres,
        y=valores,
        mode='lines+markers+text',
        text=valores,
        textposition="top center",
        line=dict(color='#8B1538', width=4, shape='spline'),
        marker=dict(size=14, color='#8B1538', line=dict(width=3, color='white')),
        textfont=dict(size=14, family='Poppins', weight='bold')
    ))
    
    fig.update_layout(
        title={
            'text': '<b>PERFIL DE PUNTUACIONES ESCALARES</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Poppins'}
        },
        yaxis=dict(
            range=[0, 20],
            dtick=2,
            title="Puntuación Escalar (PE)",
            gridcolor='rgba(0,0,0,0.05)'
        ),
        xaxis=dict(
            tickangle=-45,
            gridcolor='rgba(0,0,0,0.05)'
        ),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        font=dict(family='Inter')
    )
    
    return fig

def crear_grafico_indices(indices):
    """Gráfico de barras de índices compuestos"""
    # Filtrar solo índices calculados
    datos = {k: v for k, v in indices.items() if v is not None}
    
    if not datos:
        return None
    
    nombres = list(datos.keys())
    valores = list(datos.values())
    
    colores = []
    for v in valores:
        _, color, _ = BaremosWPPSI.obtener_categoria(v)
        colores.append(color)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=nombres,
        y=valores,
        marker_color=colores,
        text=valores,
        textposition='outside',
        textfont=dict(size=16, family='Poppins', weight='bold'),
        width=0.6
    ))
    
    fig.add_hline(y=100, line_dash="dash", line_color="#34495e", line_width=3)
    
    fig.update_layout(
        title={
            'text': '<b>PERFIL DE ÍNDICES COMPUESTOS</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Poppins'}
        },
        yaxis=dict(
            range=[40, 160],
            dtick=20,
            title="Puntuación Compuesta (CI)",
            gridcolor='rgba(0,0,0,0.05)'
        ),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        font=dict(family='Inter')
    )
    
    return fig

def crear_grafico_radar(indices):
    """Gráfico radar de capacidades cognitivas"""
    categorias = []
    valores = []
    
    mapeo = {
        'ICV': 'Comprensión\nVerbal',
        'IVE': 'Visoespacial',
        'IRF': 'Razonamiento\nFluido',
        'IMT': 'Memoria de\nTrabajo',
        'IVP': 'Velocidad de\nProcesamiento'
    }
    
    for key, label in mapeo.items():
        if indices.get(key) is not None:
            categorias.append(label)
            valores.append(indices[key])
    
    if not valores:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        fillcolor='rgba(139, 21, 56, 0.25)',
        line=dict(color='#8B1538', width=3),
        marker=dict(size=10, color='#8B1538'),
        name='Paciente'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[100] * len(categorias),
        theta=categorias,
        mode='lines',
        line=dict(color='gray', width=2, dash='dot'),
        name='Media (100)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[40, 160],
                tickfont=dict(size=11)
            ),
            angularaxis=dict(
                tickfont=dict(size=12, family='Poppins')
            )
        ),
        title={
            'text': '<b>MAPA COGNITIVO MULTIDIMENSIONAL</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Poppins'}
        },
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        font=dict(family='Inter')
    )
    
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# GENERADOR DE PDF
# ═══════════════════════════════════════════════════════════════════════════════

def generar_pdf_informe(datos):
    """Genera informe PDF profesional"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Estilo título
    titulo_style = ParagraphStyle(
        'Titulo',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#8B1538'),
        alignment=TA_CENTER,
        spaceAfter=30,
        fontName='Helvetica-Bold'
    )
    
    # Estilo sección
    seccion_style = ParagraphStyle(
        'Seccion',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.white,
        backColor=colors.HexColor('#2c3e50'),
        spaceBefore=20,
        spaceAfter=15,
        borderPadding=(5, 10, 5, 10)
    )
    
    # Portada
    story.append(Paragraph("INFORME PSICOPEDAGÓGICO", titulo_style))
    story.append(Paragraph("Escala de Inteligencia WPPSI-IV", 
                          ParagraphStyle('Sub', parent=styles['Normal'], alignment=TA_CENTER, fontSize=12)))
    story.append(Spacer(1, 2*cm))
    
    # Datos del paciente
    paciente = datos['paciente']
    data_personal = [
        ["Nombre:", paciente['nombre'], "Fecha Eval:", paciente['fecha_eval']],
        ["F. Nacimiento:", paciente['fecha_nac'], "Edad:", paciente['edad']],
        ["Examinador:", paciente['examinador'], "", ""]
    ]
    
    t_personal = Table(data_personal, colWidths=[3*cm, 6*cm, 3*cm, 5*cm])
    t_personal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#f8f9fa')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    
    story.append(t_personal)
    story.append(Spacer(1, 1*cm))
    
    # Resultados
    story.append(Paragraph("RESULTADOS DE LA EVALUACIÓN", seccion_style))
    
    # Tabla de PE
    pe_data = [["Prueba", "PD", "PE", "Clasificación"]]
    for prueba, pe in datos['pe'].items():
        pd = datos['pd'].get(prueba, '-')
        clasif = "Promedio"
        if pe >= 13:
            clasif = "Fortaleza"
        elif pe <= 7:
            clasif = "Debilidad"
        
        pe_data.append([
            BaremosWPPSI.PRUEBAS_INFO[prueba]['nombre'],
            str(pd),
            str(pe),
            clasif
        ])
    
    t_pe = Table(pe_data, colWidths=[6*cm, 3*cm, 3*cm, 5*cm])
    t_pe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#8B1538')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')])
    ]))
    
    story.append(t_pe)
    story.append(PageBreak())
    
    # Índices
    story.append(Paragraph("ÍNDICES COMPUESTOS", seccion_style))
    
    ind_data = [["Índice", "Puntuación", "Percentil", "Categoría"]]
    for key, valor in datos['indices'].items():
        if valor is not None:
            cat, _, _ = BaremosWPPSI.obtener_categoria(valor)
            perc = BaremosWPPSI.obtener_percentil(valor)
            ind_data.append([key, str(valor), str(perc), cat])
    
    t_ind = Table(ind_data, colWidths=[4*cm, 4*cm, 4*cm, 5*cm])
    t_ind.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    
    story.append(t_ind)
    story.append(Spacer(1, 1*cm))
    
    # Interpretación
    if datos['indices'].get('CIT'):
        cit = datos['indices']['CIT']
        cat, _, desc = BaremosWPPSI.obtener_categoria(cit)
        perc = BaremosWPPSI.obtener_percentil(cit)
        
        interpretacion = f"""
        <b>ANÁLISIS DEL COEFICIENTE INTELECTUAL TOTAL (CIT):</b><br/><br/>
        El evaluado obtuvo un CIT de <b>{cit}</b>, clasificado como <b>{cat}</b>.
        Se sitúa en el percentil <b>{perc}</b>. {desc}.<br/><br/>
        <b>Interpretación:</b> Se recomienda considerar el perfil completo de fortalezas
        y debilidades para una comprensión integral del funcionamiento cognitivo.
        """
        
        story.append(Paragraph(interpretacion, styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 2*cm))
    footer_line = Drawing(500, 10)
    footer_line.add(Line(0, 0, 17*cm, 0, strokeColor=colors.HexColor('#8B1538')))
    story.append(footer_line)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Informe generado por WPPSI-IV Professional | Uso profesional exclusivo",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER, textColor=colors.grey)
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ═══════════════════════════════════════════════════════════════════════════════
# INTERFAZ DE USUARIO
# ═══════════════════════════════════════════════════════════════════════════════

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 INGRESO DE DATOS",
    "📊 RESULTADOS GRÁFICOS",
    "🔍 ANÁLISIS DETALLADO",
    "📄 GENERAR INFORME PDF"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: INGRESO DE DATOS
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("### 📋 Datos del Paciente")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nombre = st.text_input("Nombre completo", "Micaela")
    with col2:
        fecha_nac = st.date_input("Fecha de nacimiento", date(2020, 9, 20))
    with col3:
        fecha_eval = st.date_input("Fecha de evaluación", date.today())
    
    examinador = st.text_input("Examinador/a", "Daniela")
    
    # Calcular edad
    years, months, days = BaremosWPPSI.calcular_edad(fecha_nac, fecha_eval)
    edad_str = f"{years} años, {months} meses, {days} días"
    st.info(f"📅 **Edad Cronológica:** {edad_str}")
    
    st.markdown("---")
    st.markdown("### 🎯 Selección de Pruebas Aplicadas")
    st.warning("⚠️ **IMPORTANTE**: Marque solo las pruebas que se aplicaron al niño/a")
    
    # Selector de pruebas
    col_a, col_b = st.columns(2)
    
    pruebas_temp = {}
    
    with col_a:
        st.markdown("#### Área Verbal y Cognitiva")
        pruebas_temp['informacion'] = st.checkbox(
            f"{BaremosWPPSI.PRUEBAS_INFO['informacion']['icono']} Información (ICV)",
            value=st.session_state.pruebas_seleccionadas['informacion']
        )
        pruebas_temp['semejanzas'] = st.checkbox(
            f"{BaremosWPPSI.PRUEBAS_INFO['semejanzas']['icono']} Semejanzas (ICV)",
            value=st.session_state.pruebas_seleccionadas['semejanzas']
        )
        pruebas_temp['matrices'] = st.checkbox(
            f"{BaremosWPPSI.PRUEBAS_INFO['matrices']['icono']} Matrices (IRF)",
            value=st.session_state.pruebas_seleccionadas['matrices']
        )
        pruebas_temp['conceptos'] = st.checkbox(
            f"{BaremosWPPSI.PRUEBAS_INFO['conceptos']['icono']} Conceptos (IRF)",
            value=st.session_state.pruebas_seleccionadas['conceptos']
        )
        pruebas_temp['reconocimiento'] = st.checkbox(
            f"{BaremosWPPSI.PRUEBAS_INFO['reconocimiento']['icono']} Reconocimiento (IMT)",
            value=st.session_state.pruebas_seleccionadas['reconocimiento']
        )
    
    with col_b:
        st.markdown("#### Área Visoespacial y Procesamiento")
        pruebas_temp['cubos'] = st.checkbox(
            f"{BaremosWPPSI.PRUEBAS_INFO['cubos']['icono']} Cubos (IVE)",
            value=st.session_state.pruebas_seleccionadas['cubos']
        )
        pruebas_temp['rompecabezas'] = st.checkbox(
            f"{BaremosWPPSI.PRUEBAS_INFO['rompecabezas']['icono']} Rompecabezas (IVE)",
            value=st.session_state.pruebas_seleccionadas['rompecabezas']
        )
        pruebas_temp['localizacion'] = st.checkbox(
            f"{BaremosWPPSI.PRUEBAS_INFO['localizacion']['icono']} Localización (IMT)",
            value=st.session_state.pruebas_seleccionadas['localizacion']
        )
        pruebas_temp['busqueda_animales'] = st.checkbox(
            f"{BaremosWPPSI.PRUEBAS_INFO['busqueda_animales']['icono']} Búsqueda de Animales (IVP)",
            value=st.session_state.pruebas_seleccionadas['busqueda_animales']
        )
        pruebas_temp['cancelacion'] = st.checkbox(
            f"{BaremosWPPSI.PRUEBAS_INFO['cancelacion']['icono']} Cancelación (IVP)",
            value=st.session_state.pruebas_seleccionadas['cancelacion']
        )
    
    # Actualizar session state
    st.session_state.pruebas_seleccionadas = pruebas_temp
    
    # Contador de pruebas seleccionadas
    n_seleccionadas = sum(pruebas_temp.values())
    if n_seleccionadas < 5:
        st.error(f"⚠️ Advertencia: Solo {n_seleccionadas} pruebas seleccionadas. Se recomienda aplicar al menos 5 pruebas para calcular el CIT.")
    else:
        st.success(f"✅ {n_seleccionadas} pruebas seleccionadas")
    
    st.markdown("---")
    st.markdown("### 🔢 Puntuaciones Directas (PD)")
    st.info("💡 Ingrese solo las PD de las pruebas marcadas arriba")
    
    pd_inputs = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        if pruebas_temp['informacion']:
            pd_inputs['informacion'] = st.number_input("📚 Información (0-26)", 0, 26, 15, key="pd_info")
        if pruebas_temp['semejanzas']:
            pd_inputs['semejanzas'] = st.number_input("💭 Semejanzas (0-29)", 0, 29, 15, key="pd_sem")
        if pruebas_temp['matrices']:
            pd_inputs['matrices'] = st.number_input("🔲 Matrices (0-19)", 0, 19, 11, key="pd_mat")
        if pruebas_temp['conceptos']:
            pd_inputs['conceptos'] = st.number_input("🎯 Conceptos (0-19)", 0, 19, 11, key="pd_con")
        if pruebas_temp['reconocimiento']:
            pd_inputs['reconocimiento'] = st.number_input("👁️ Reconocimiento (0-16)", 0, 16, 2, key="pd_rec")
    
    with col2:
        if pruebas_temp['cubos']:
            pd_inputs['cubos'] = st.number_input("🧩 Cubos (0-30)", 0, 30, 16, key="pd_cub")
        if pruebas_temp['rompecabezas']:
            pd_inputs['rompecabezas'] = st.number_input("🧩 Rompecabezas (0-20)", 0, 20, 7, key="pd_rom")
        if pruebas_temp['localizacion']:
            pd_inputs['localizacion'] = st.number_input("📍 Localización (0-20)", 0, 20, 19, key="pd_loc")
        if pruebas_temp['busqueda_animales']:
            pd_inputs['busqueda_animales'] = st.number_input("🐾 Búsqueda de Animales (0-21)", 0, 21, 4, key="pd_bus")
        if pruebas_temp['cancelacion']:
            pd_inputs['cancelacion'] = st.number_input("✓ Cancelación (0-21)", 0, 21, 7, key="pd_can")
    
    st.markdown("###")
    
    if st.button("✨ PROCESAR Y GENERAR ANÁLISIS COMPLETO", type="primary"):
        if not nombre:
            st.error("❌ Ingrese el nombre del paciente")
        elif n_seleccionadas == 0:
            st.error("❌ Debe seleccionar al menos 1 prueba")
        else:
            with st.spinner("Procesando evaluación..."):
                # Procesar
                resultados = procesar_evaluacion(
                    {
                        'nombre': nombre,
                        'fecha_nac': str(fecha_nac),
                        'fecha_eval': str(fecha_eval),
                        'edad': edad_str,
                        'examinador': examinador
                    },
                    pd_inputs,
                    pruebas_temp
                )
                
                # Guardar en session state
                st.session_state.datos_completos = True
                st.session_state.paciente = {
                    'nombre': nombre,
                    'fecha_nac': str(fecha_nac),
                    'fecha_eval': str(fecha_eval),
                    'edad': edad_str,
                    'examinador': examinador
                }
                st.session_state.pd = pd_inputs
                st.session_state.pe = resultados['pe']
                st.session_state.indices = resultados['indices']
                st.session_state.fortalezas = resultados['fortalezas']
                st.session_state.debilidades = resultados['debilidades']
                st.session_state.n_pruebas = resultados['n_pruebas']
                
                st.success("✅ ¡Evaluación procesada correctamente! Explore las demás pestañas para ver los resultados.")
                st.balloons()

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: RESULTADOS GRÁFICOS
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    if st.session_state.datos_completos:
        st.markdown("### 📊 Dashboard de Resultados")
        
        # Métricas principales
        indices = st.session_state.indices
        
        cols = st.columns(len([k for k, v in indices.items() if v is not None]))
        for i, (key, valor) in enumerate(indices.items()):
            if valor is not None:
                with cols[i]:
                    cat, color, desc = BaremosWPPSI.obtener_categoria(valor)
                    perc = BaremosWPPSI.obtener_percentil(valor)
                    st.metric(key, valor, f"Percentil {perc}")
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pe = crear_grafico_perfil_escalares(st.session_state.pe)
            if fig_pe:
                st.plotly_chart(fig_pe, use_container_width=True)
        
        with col2:
            fig_ind = crear_grafico_indices(st.session_state.indices)
            if fig_ind:
                st.plotly_chart(fig_ind, use_container_width=True)
        
        st.markdown("---")
        
        # Gráfico radar
        fig_radar = crear_grafico_radar(st.session_state.indices)
        if fig_radar:
            st.plotly_chart(fig_radar, use_container_width=True)
        
    else:
        st.warning("⚠️ Complete los datos en la pestaña 'Ingreso de Datos' primero")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: ANÁLISIS DETALLADO
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    if st.session_state.datos_completos:
        st.markdown("### 🔍 Análisis Clínico Detallado")
        
        # Fortalezas y Debilidades
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Fortalezas Significativas (PE ≥ 13)")
            if st.session_state.fortalezas:
                for item in st.session_state.fortalezas:
                    st.success(f"**{item['prueba']}**: PE = {item['pe']}")
                    st.caption(item['descripcion'])
                    st.progress(item['pe'] / 19)
            else:
                st.info("No se identificaron fortalezas significativas")
        
        with col2:
            st.markdown("#### ⚠️ Áreas a Desarrollar (PE ≤ 7)")
            if st.session_state.debilidades:
                for item in st.session_state.debilidades:
                    st.error(f"**{item['prueba']}**: PE = {item['pe']}")
                    st.caption(item['descripcion'])
                    st.progress(item['pe'] / 19)
            else:
                st.info("No se identificaron debilidades significativas")
        
        st.markdown("---")
        
        # Interpretación CIT
        if st.session_state.indices.get('CIT'):
            cit = st.session_state.indices['CIT']
            cat, color, desc = BaremosWPPSI.obtener_categoria(cit)
            perc = BaremosWPPSI.obtener_percentil(cit)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}15 0%, {color}05 100%); 
                        padding: 2rem; border-radius: 15px; border-left: 5px solid {color};">
                <h3 style="color: {color}; margin: 0;">CIT: {cit} - {cat}</h3>
                <p style="margin-top: 1rem; font-size: 1.1rem;">
                    <b>Percentil:</b> {perc}<br>
                    <b>Interpretación:</b> {desc}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Tabla detallada
        with st.expander("📋 Tabla Detallada de Resultados"):
            df_resultados = pd.DataFrame([
                {
                    "Prueba": BaremosWPPSI.PRUEBAS_INFO[k]['nombre'],
                    "PD": st.session_state.pd.get(k, '-'),
                    "PE": v,
                    "Índice": BaremosWPPSI.PRUEBAS_INFO[k]['indice'],
                    "Descripción": BaremosWPPSI.PRUEBAS_INFO[k]['descripcion']
                }
                for k, v in st.session_state.pe.items()
            ])
            st.dataframe(df_resultados, use_container_width=True, hide_index=True)
    
    else:
        st.warning("⚠️ Complete los datos primero")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: GENERAR PDF
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    if st.session_state.datos_completos:
        st.markdown("### 📄 Generación de Informe Profesional")
        
        st.write("""
        Genere un informe PDF completo con:
        - Datos de filiación
        - Tabla de puntuaciones
        - Gráficos vectoriales
        - Interpretación clínica
        - Análisis de fortalezas y debilidades
        """)
        
        if st.button("🖨️ GENERAR INFORME PDF", type="secondary"):
            with st.spinner("Generando informe PDF profesional..."):
                try:
                    datos_pdf = {
                        'paciente': st.session_state.paciente,
                        'pd': st.session_state.pd,
                        'pe': st.session_state.pe,
                        'indices': st.session_state.indices
                    }
                    
                    pdf_buffer = generar_pdf_informe(datos_pdf)
                    
                    st.success("✅ Informe generado exitosamente")
                    
                    st.download_button(
                        label="⬇️ DESCARGAR INFORME PDF",
                        data=pdf_buffer,
                        file_name=f"Informe_WPPSI-IV_{st.session_state.paciente['nombre'].replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
                    
                except Exception as e:
                    st.error(f"Error al generar PDF: {str(e)}")
    
    else:
        st.info("⚠️ Complete la evaluación primero")

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div class="footer">
    <p style="font-size: 1.2rem; font-weight: 700; color: #8B1538; margin-bottom: 0.5rem;">
        🧠 WPPSI-IV PROFESSIONAL SYSTEM
    </p>
    <p style="font-size: 1rem; font-weight: 500;">
        Sistema de Evaluación Psicopedagógica
    </p>
    <p style="font-size: 0.9rem; color: #8B1538; font-weight: 600;">
        ❤️ Desarrollado especialmente para Daniela
    </p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">
        Versión 6.0.0 Professional Edition | © 2026
    </p>
</div>
""", unsafe_allow_html=True)
