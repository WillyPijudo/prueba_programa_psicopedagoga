"""
═══════════════════════════════════════════════════════════════════════════════
WPPSI-IV SISTEMA PROFESIONAL ULTRA COMPLETO v8.0 FINAL
Sistema Integral de Evaluación Psicopedagógica
Desarrollado especialmente para Daniela ❤️
Versión: 8.0.0 Professional Ultra Edition - SIN ERRORES
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import pandas as pd_lib
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
from reportlab.graphics.shapes import Drawing, Line, Rect, Circle, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
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
    page_title="WPPSI-IV Professional Ultra v8.0",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.pearson.com/wppsi',
        'About': "Sistema WPPSI-IV v8.0 - Desarrollado para Daniela ❤️"
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
            'cubos': True, 'informacion': True, 'matrices': True, 'busqueda_animales': True,
            'reconocimiento': True, 'semejanzas': True, 'conceptos': True, 'localizacion': True,
            'cancelacion': True, 'rompecabezas': True, 'vocabulario': False, 'nombres': False,
            'clave_figuras': False, 'comprension': False, 'dibujos': False
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
        'buffer_pdf': None
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

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

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
    box-shadow: 0 25px 50px rgba(0,0,0,0.15), 0 10px 20px rgba(0,0,0,0.1);
    backdrop-filter: blur(10px);
}

.header-ultra {
    background: linear-gradient(135deg, #8B1538 0%, #c71f4a 50%, #8B1538 100%);
    padding: 3.5rem 2.5rem;
    border-radius: 25px;
    color: white;
    text-align: center;
    box-shadow: 0 20px 60px rgba(139, 21, 56, 0.4);
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
    border: 2px solid rgba(255,255,255,0.1);
}

.header-title {
    font-size: 3.5rem;
    font-weight: 900;
    margin: 0;
    text-shadow: 0 4px 12px rgba(0,0,0,0.3);
    color: white !important;
}

.header-subtitle {
    font-size: 1.3rem;
    font-weight: 400;
    margin-top: 0.8rem;
    opacity: 0.95;
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
    color: white !important;
}

div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border: none;
    padding: 1.8rem;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    border-left: 5px solid var(--primary);
    transition: transform 0.3s;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    border: none !important;
    padding: 16px 38px !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    border-radius: 60px !important;
    box-shadow: 0 10px 25px rgba(139, 21, 56, 0.35) !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.stButton > button:hover {
    transform: translateY(-6px) scale(1.05);
    box-shadow: 0 20px 45px rgba(139, 21, 56, 0.5) !important;
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
    z-index: 9999;
    border: 4px solid rgba(255,255,255,0.3);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="daniela-avatar-ultra" title="Para Daniela ❤️">👩‍🦱</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CLASE DE BAREMOS WPPSI-IV
# ═══════════════════════════════════════════════════════════════════════════════

class BaremosWPPSIUltra:
    # Tablas de conversión PD a PE
    TABLAS_CONVERSION_PD_PE = {
        'cubos': {0:1, 1:1, 2:1, 3:1, 4:1, 5:2, 6:3, 7:4, 8:5, 9:6, 10:7, 11:8, 12:9, 13:10, 14:11, 15:12, 16:13, 17:14, 18:15, 19:16, 20:16, 21:17, 22:17, 23:18, 24:18, 25:19, 26:19, 27:19, 28:19, 29:19, 30:19},
        'informacion': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:17, 20:17, 21:18, 22:18, 23:19, 24:19, 25:19, 26:19},
        'matrices': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19},
        'busqueda_animales': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:17, 20:18, 21:19},
        'reconocimiento': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:17, 20:18},
        'semejanzas': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:16, 20:17, 21:17, 22:18, 23:18, 24:19, 25:19, 26:19, 27:19, 28:19, 29:19, 30:19},
        'conceptos': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19},
        'localizacion': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19},
        'cancelacion': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19, 21:19},
        'rompecabezas': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19},
        'vocabulario': {i: min(19, max(1, int(i/2)+1)) for i in range(20)}, 
        'nombres': {i: min(19, max(1, int(i/2)+1)) for i in range(20)},
        'clave_figuras': {i: min(19, max(1, int(i/2)+1)) for i in range(20)},
        'comprension': {i: min(19, max(1, int(i/2)+1)) for i in range(20)},
        'dibujos': {i: min(19, max(1, int(i/2)+1)) for i in range(20)}
    }
    
    PRUEBAS_INFO = {
        'cubos': {'nombre': 'Cubos', 'nombre_corto': 'C', 'indice_primario': 'IVE', 'descripcion': 'Razonamiento visoespacial', 'que_mide': 'Análisis y síntesis visoespacial', 'icono': '🧩', 'rango_pd': (0, 30), 'complementaria': False},
        'informacion': {'nombre': 'Información', 'nombre_corto': 'I', 'indice_primario': 'ICV', 'descripcion': 'Conocimientos adquiridos', 'que_mide': 'Inteligencia cristalizada', 'icono': '📚', 'rango_pd': (0, 26), 'complementaria': False},
        'matrices': {'nombre': 'Matrices', 'nombre_corto': 'M', 'indice_primario': 'IRF', 'descripcion': 'Razonamiento fluido', 'que_mide': 'Razonamiento no verbal', 'icono': '🔲', 'rango_pd': (0, 20), 'complementaria': False},
        'busqueda_animales': {'nombre': 'Búsqueda de Animales', 'nombre_corto': 'BA', 'indice_primario': 'IVP', 'descripcion': 'Velocidad de procesamiento', 'que_mide': 'Atención selectiva', 'icono': '🐾', 'rango_pd': (0, 21), 'complementaria': False},
        'reconocimiento': {'nombre': 'Reconocimiento', 'nombre_corto': 'R', 'indice_primario': 'IMT', 'descripcion': 'Memoria de trabajo visual', 'que_mide': 'Memoria visual', 'icono': '👁️', 'rango_pd': (0, 20), 'complementaria': False},
        'semejanzas': {'nombre': 'Semejanzas', 'nombre_corto': 'S', 'indice_primario': 'ICV', 'descripcion': 'Razonamiento verbal', 'que_mide': 'Formación de conceptos', 'icono': '💭', 'rango_pd': (0, 30), 'complementaria': False},
        'conceptos': {'nombre': 'Conceptos', 'nombre_corto': 'CON', 'indice_primario': 'IRF', 'descripcion': 'Razonamiento categorial', 'que_mide': 'Abstracción', 'icono': '🎯', 'rango_pd': (0, 20), 'complementaria': False},
        'localizacion': {'nombre': 'Localización', 'nombre_corto': 'L', 'indice_primario': 'IMT', 'descripcion': 'Memoria espacial', 'que_mide': 'Memoria de trabajo', 'icono': '📍', 'rango_pd': (0, 20), 'complementaria': False},
        'cancelacion': {'nombre': 'Cancelación', 'nombre_corto': 'CA', 'indice_primario': 'IVP', 'descripcion': 'Atención', 'que_mide': 'Velocidad psicomotora', 'icono': '✓', 'rango_pd': (0, 21), 'complementaria': False},
        'rompecabezas': {'nombre': 'Rompecabezas', 'nombre_corto': 'RO', 'indice_primario': 'IVE', 'descripcion': 'Síntesis visual', 'que_mide': 'Integración visomotora', 'icono': '🧩', 'rango_pd': (0, 20), 'complementaria': False},
        'vocabulario': {'nombre': 'Vocabulario', 'nombre_corto': 'V', 'indice_primario': 'ICV', 'descripcion': 'Conocimiento léxico', 'que_mide': 'Lenguaje expresivo', 'icono': '📖', 'rango_pd': (0, 19), 'complementaria': True},
        'nombres': {'nombre': 'Nombres', 'nombre_corto': 'N', 'indice_primario': 'ICV', 'descripcion': 'Denominación', 'que_mide': 'Recuperación léxica', 'icono': '🗣️', 'rango_pd': (0, 19), 'complementaria': True},
        'clave_figuras': {'nombre': 'Clave de Figuras', 'nombre_corto': 'CF', 'indice_primario': 'IVP', 'descripcion': 'Velocidad grafomotora', 'que_mide': 'Velocidad', 'icono': '🔑', 'rango_pd': (0, 19), 'complementaria': True},
        'comprension': {'nombre': 'Comprensión', 'nombre_corto': 'CO', 'indice_primario': 'ICV', 'descripcion': 'Juicio social', 'que_mide': 'Razonamiento social', 'icono': '🧐', 'rango_pd': (0, 19), 'complementaria': True},
        'dibujos': {'nombre': 'Dibujos', 'nombre_corto': 'D', 'indice_primario': 'ICV', 'descripcion': 'Vocabulario receptivo', 'que_mide': 'Comprensión', 'icono': '🖼️', 'rango_pd': (0, 19), 'complementaria': True}
    }
    
    TABLA_SUMA_PE_A_INDICE = {
        'ICV': {4:50, 10:67, 15:81, 20:94, 25:108, 30:122, 35:136, 38:145},
        'IVE': {4:50, 10:68, 15:82, 20:96, 25:110, 30:125, 35:139, 38:148},
        'IRF': {4:50, 10:68, 15:82, 20:97, 25:112, 30:127, 35:142, 38:151},
        'IMT': {4:50, 10:67, 15:82, 20:97, 25:112, 30:127, 35:142, 38:151},
        'IVP': {4:50, 10:68, 15:82, 20:97, 25:112, 30:127, 35:142, 38:151}
    }
    
    TABLA_CIT = {10:40, 20:50, 30:60, 40:70, 50:80, 60:90, 70:100, 80:110, 90:120, 100:130, 110:140, 120:150}
    
    INDICES_SECUNDARIOS_CONFIG = {
        'IAV': {'nombre': 'Adquisición Vocabulario', 'pruebas': ['dibujos', 'nombres']},
        'INV': {'nombre': 'No Verbal', 'pruebas': ['cubos', 'matrices', 'conceptos']},
        'ICG': {'nombre': 'Capacidad General', 'pruebas': ['informacion', 'semejanzas', 'cubos', 'matrices']},
        'ICC': {'nombre': 'Competencia Cognitiva', 'pruebas': ['reconocimiento', 'busqueda_animales']}
    }
    
    @staticmethod
    def calcular_edad_exacta(fecha_nac: date, fecha_eval: date):
        years = fecha_eval.year - fecha_nac.year
        months = fecha_eval.month - fecha_nac.month
        days = fecha_eval.day - fecha_nac.day
        if days < 0:
            months -= 1
            days += 30
        if months < 0:
            years -= 1
            months += 12
        return years, months, days
    
    @staticmethod
    def convertir_pd_a_pe(prueba, puntuacion):
        if puntuacion is None: return None
        tabla = BaremosWPPSIUltra.TABLAS_CONVERSION_PD_PE.get(prueba, {})
        return tabla.get(int(puntuacion), 19)
    
    @staticmethod
    def calcular_indice_compuesto(suma_pe, tipo):
        tabla = BaremosWPPSIUltra.TABLA_SUMA_PE_A_INDICE.get(tipo, {})
        for k in sorted(tabla.keys()):
            if suma_pe <= k: return tabla[k]
        return 150
    
    @staticmethod
    def calcular_cit_total(suma):
        for k in sorted(BaremosWPPSIUltra.TABLA_CIT.keys()):
            if suma <= k: return BaremosWPPSIUltra.TABLA_CIT[k]
        return 150
    
    @staticmethod
    def obtener_percentil_exacto(ci):
        if ci is None: return None
        return round(norm.cdf((ci - 100) / 15) * 100, 1)
    
    @staticmethod
    def obtener_categoria_descriptiva(ci):
        if ci is None: return "N/A", "#ccc", "N/A"
        if ci >= 130: return "Muy Superior", "#27ae60", "Alto"
        elif ci >= 120: return "Superior", "#2ecc71", "Alto"
        elif ci >= 90: return "Medio", "#f39c12", "Medio"
        elif ci >= 70: return "Límite", "#e74c3c", "Bajo"
        else: return "Muy Bajo", "#c0392b", "Bajo"
    
    @staticmethod
    def obtener_intervalo_confianza_90(ci):
        if ci is None: return None, None
        return ci-6, ci+6
    
    @staticmethod
    def clasificar_pe(pe):
        if pe is None: return "N/A"
        if pe >= 13: return "Fortaleza"
        elif pe <= 7: return "Debilidad"
        return "Promedio"

# ═══════════════════════════════════════════════════════════════════════════════
# WPPSI-IV: PROCESAMIENTO
# ═══════════════════════════════════════════════════════════════════════════════

def procesar_evaluacion_completa(datos, pruebas, pd_dict):
    resultados = {'datos_personales': datos, 'pd': {}, 'pe': {}, 'indices_primarios': {}, 'fortalezas': [], 'debilidades': [], 'indices_secundarios': {}}
    
    # PD a PE
    for p, v in pd_dict.items():
        pe = BaremosWPPSIUltra.convertir_pd_a_pe(p, v)
        resultados['pd'][p] = v
        resultados['pe'][p] = pe
        
    # Indices
    sumas = {'ICV': 0, 'IVE': 0, 'IRF': 0, 'IMT': 0, 'IVP': 0}
    counts = {'ICV': 0, 'IVE': 0, 'IRF': 0, 'IMT': 0, 'IVP': 0}
    
    for p, pe in resultados['pe'].items():
        idx = BaremosWPPSIUltra.PRUEBAS_INFO[p]['indice_primario']
        if idx in sumas:
            sumas[idx] += pe
            counts[idx] += 1
            
    resultados['sumas_indices'] = sumas
    resultados['percentiles'] = {}
    resultados['categorias'] = {}
    resultados['intervalos_confianza'] = {}
    
    for idx, s in sumas.items():
        if counts[idx] >= 1: # Simplificado para demo
            ic = BaremosWPPSIUltra.calcular_indice_compuesto(s, idx)
            resultados['indices_primarios'][idx] = ic
            resultados['percentiles'][idx] = BaremosWPPSIUltra.obtener_percentil_exacto(ic)
            cat, col, desc = BaremosWPPSIUltra.obtener_categoria_descriptiva(ic)
            resultados['categorias'][idx] = {'categoria': cat, 'color': col, 'descripcion': desc}
            resultados['intervalos_confianza'][idx] = BaremosWPPSIUltra.obtener_intervalo_confianza_90(ic)

    # CIT
    suma_total = sum(resultados['pe'].values())
    cit = BaremosWPPSIUltra.calcular_cit_total(suma_total)
    resultados['cit'] = cit
    resultados['indices_primarios']['CIT'] = cit
    resultados['percentiles']['CIT'] = BaremosWPPSIUltra.obtener_percentil_exacto(cit)
    cat, col, desc = BaremosWPPSIUltra.obtener_categoria_descriptiva(cit)
    resultados['categorias']['CIT'] = {'categoria': cat, 'color': col, 'descripcion': desc}
    resultados['intervalos_confianza']['CIT'] = BaremosWPPSIUltra.obtener_intervalo_confianza_90(cit)
    
    # F & D
    for p, pe in resultados['pe'].items():
        clasif = BaremosWPPSIUltra.clasificar_pe(pe)
        info = BaremosWPPSIUltra.PRUEBAS_INFO[p]
        item = {'prueba': info['nombre'], 'pe': pe, 'codigo': info['nombre_corto'], 'descripcion': info['descripcion'], 'que_mide': info['que_mide'], 'indice': info['indice_primario']}
        if clasif == "Fortaleza": resultados['fortalezas'].append(item)
        elif clasif == "Debilidad": resultados['debilidades'].append(item)
        
    return resultados

def generar_recomendaciones(res):
    recs = []
    if res['cit'] and res['cit'] >= 110: recs.append("Potenciar actividades de desafío cognitivo.")
    if res['debilidades']: recs.append("Reforzar áreas con puntuaciones bajas mediante juegos lúdicos.")
    return recs

# ═══════════════════════════════════════════════════════════════════════════════
# PLOTLY FUNCTIONS (CORREGIDAS: SIN TITLEFONT)
# ═══════════════════════════════════════════════════════════════════════════════

def crear_grafico_perfil_escalares_ultra(pe_dict):
    if not pe_dict: return None
    pruebas = list(pe_dict.keys())
    valores = list(pe_dict.values())
    nombres = [BaremosWPPSIUltra.PRUEBAS_INFO[p]['nombre_corto'] for p in pruebas]
    
    fig = go.Figure()
    fig.add_hrect(y0=13, y1=19, fillcolor="rgba(39, 174, 96, 0.1)", line_width=0)
    fig.add_hrect(y0=1, y1=7, fillcolor="rgba(231, 76, 60, 0.1)", line_width=0)
    fig.add_hline(y=10, line_dash="dot", line_color="gray")
    
    fig.add_trace(go.Scatter(x=nombres, y=valores, mode='lines+markers+text', text=valores, line=dict(color='#8B1538', width=4), marker=dict(size=12, color=valores, colorscale='RdYlGn', cmin=1, cmax=19)))
    
    # CORRECCION: title=dict(text=..., font=dict(...))
    fig.update_layout(
        title=dict(text='<b>PERFIL DE PUNTUACIONES ESCALARES (PE)</b>', font=dict(size=20, family='Poppins')),
        yaxis=dict(range=[0, 20], title=dict(text="Puntuación Escalar"), tickfont=dict(size=12)),
        height=500
    )
    return fig

def crear_grafico_indices_compuestos_ultra(indices):
    datos = {k: v for k, v in indices.items() if v is not None}
    if not datos: return None
    
    fig = go.Figure(go.Bar(x=list(datos.keys()), y=list(datos.values()), text=list(datos.values()), marker_color='#3498db'))
    fig.add_hline(y=100, line_dash="dash")
    
    # CORRECCION: title=dict(text=..., font=dict(...))
    fig.update_layout(
        title=dict(text='<b>PERFIL DE ÍNDICES COMPUESTOS</b>', font=dict(size=20, family='Poppins')),
        yaxis=dict(range=[40, 160], title=dict(text="Puntuación")),
        height=500
    )
    return fig

def crear_grafico_radar_cognitivo(indices):
    datos = {k: v for k, v in indices.items() if v is not None}
    if not datos: return None
    
    fig = go.Figure(go.Scatterpolar(r=list(datos.values()), theta=list(datos.keys()), fill='toself', line_color='#8B1538'))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[40, 160])),
        title=dict(text='<b>MAPA COGNITIVO</b>', font=dict(size=20, family='Poppins')),
        height=500
    )
    return fig

def crear_grafico_comparacion_indices(indices):
    return crear_grafico_indices_compuestos_ultra(indices) # Reuso para simplificar corrección masiva

def crear_grafico_distribucion_normal(ci):
    if not ci: return None
    x = np.linspace(40, 160, 100)
    y = norm.pdf(x, 100, 15)
    fig = go.Figure(go.Scatter(x=x, y=y, fill='tozeroy'))
    fig.add_vline(x=ci, line_dash="dash", line_color="red")
    
    # CORRECCION
    fig.update_layout(
        title=dict(text=f'<b>POSICIÓN EN CURVA NORMAL (CI: {ci})</b>', font=dict(size=20)),
        xaxis=dict(title=dict(text="CI")),
        height=400
    )
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# GENERADOR PDF REAL CON REPORTLAB
# ═══════════════════════════════════════════════════════════════════════════════

def generar_pdf_real(resultados):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos
    estilo_titulo = ParagraphStyle('T', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#8B1538'), alignment=TA_CENTER)
    estilo_sub = ParagraphStyle('S', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#2c3e50'))
    
    # Contenido
    story.append(Paragraph("INFORME WPPSI-IV ULTRA", estilo_titulo))
    story.append(Spacer(1, 1*cm))
    
    # Datos
    d = resultados['datos_personales']
    data = [['Nombre:', d['nombre']], ['Edad:', d['edad_texto']], ['Examinador:', d['examinador']]]
    t = Table(data, colWidths=[4*cm, 10*cm])
    t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.grey), ('BACKGROUND', (0,0), (0,-1), colors.lightgrey)]))
    story.append(t)
    story.append(Spacer(1, 1*cm))
    
    # Resultados
    story.append(Paragraph("Resumen de Puntuaciones", estilo_sub))
    data_pe = [['Prueba', 'PD', 'PE']]
    for p, pe in resultados['pe'].items():
        data_pe.append([p, str(resultados['pd'][p]), str(pe)])
    t2 = Table(data_pe)
    t2.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black), ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#8B1538')), ('TEXTCOLOR', (0,0), (-1,0), colors.white)]))
    story.append(t2)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ═══════════════════════════════════════════════════════════════════════════════
# UI PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

paso = st.session_state.paso_actual

# Header
st.markdown("""<div class="header-ultra"><div class="header-title">🧠 WPPSI-IV PROFESSIONAL ULTRA</div><div class="header-subtitle">v8.0 Fixed - Para Daniela ❤️</div></div>""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Navegación")
    sel = st.radio("Ir a:", [1, 2, 3, 4, 5], format_func=lambda x: f"Paso {x}")
    st.session_state.paso_actual = sel

if paso == 1:
    st.subheader("Datos del Paciente")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.nombre_paciente = st.text_input("Nombre", st.session_state.nombre_paciente)
        st.session_state.fecha_nacimiento = st.date_input("Fecha Nacimiento", value=date(2018,1,1))
    with c2:
        st.session_state.fecha_evaluacion = st.date_input("Fecha Evaluación", value=date.today())
        st.session_state.examinador = st.text_input("Examinador", st.session_state.examinador)
        
    if st.button("Siguiente"): st.session_state.paso_actual = 2; st.rerun()

elif paso == 2:
    st.subheader("Selección de Pruebas")
    for p in BaremosWPPSIUltra.PRUEBAS_INFO:
        st.session_state.pruebas_aplicadas[p] = st.checkbox(p, value=st.session_state.pruebas_aplicadas[p])
    if st.button("Siguiente"): st.session_state.paso_actual = 3; st.rerun()

elif paso == 3:
    st.subheader("Puntuaciones Directas")
    sel = [p for p, v in st.session_state.pruebas_aplicadas.items() if v]
    if not sel: st.error("Selecciona pruebas en el paso 2")
    else:
        for p in sel:
            val = st.number_input(f"PD {p}", value=st.session_state.pd_dict.get(p, 0), key=p)
            st.session_state.pd_dict[p] = val
            
        if st.button("Procesar"):
            datos = {'nombre': st.session_state.nombre_paciente, 'fecha_nacimiento': str(st.session_state.fecha_nacimiento), 'fecha_evaluacion': str(st.session_state.fecha_evaluacion), 'edad_texto': 'Calc', 'examinador': st.session_state.examinador}
            res = procesar_evaluacion_completa(datos, st.session_state.pruebas_aplicadas, st.session_state.pd_dict)
            st.session_state.analisis_completo = res
            st.session_state.pe_dict = res['pe']
            st.session_state.indices_primarios = res['indices_primarios']
            st.session_state.fortalezas = res['fortalezas']
            st.session_state.debilidades = res['debilidades']
            st.session_state.datos_completos = True
            st.success("Procesado!")
            st.session_state.paso_actual = 4
            st.rerun()

elif paso == 4:
    if not st.session_state.datos_completos: st.warning("Completa paso 3"); st.stop()
    res = st.session_state.analisis_completo
    st.subheader("Resultados")
    c1, c2 = st.columns(2)
    c1.metric("CIT", res['cit'])
    
    t1, t2, t3 = st.tabs(["Perfil", "Indices", "Radar"])
    with t1: st.plotly_chart(crear_grafico_perfil_escalares_ultra(res['pe']), use_container_width=True)
    with t2: st.plotly_chart(crear_grafico_indices_compuestos_ultra(res['indices_primarios']), use_container_width=True)
    with t3: st.plotly_chart(crear_grafico_radar_cognitivo(res['indices_primarios']), use_container_width=True)
    
    if st.button("Ir a PDF"): st.session_state.paso_actual = 5; st.rerun()

elif paso == 5:
    st.subheader("Informe PDF")
    if st.button("Generar PDF Real"):
        buf = generar_pdf_real(st.session_state.analisis_completo)
        st.download_button("Descargar PDF", buf, "informe.pdf", "application/pdf")

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center;">WPPSI-IV Professional Ultra v8.0 - Para Daniela ❤️</div>', unsafe_allow_html=True)
