"""
WPPSI-IV - Generador de Informes Psicopedagógicos (Versión Professional)
Desarrollado especialmente para Daniela
Sistema completo con generación de PDF vectorial y tablas de conversión completas.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import numpy as np
import io

# ==================== LIBRERÍAS DE REPORTE (PDF) ====================
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.graphics.shapes import Drawing, Line, String, Circle, Rect, Group
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.widgets.markers import makeMarker

# ==================== CONFIGURACIÓN DE LA PÁGINA ====================
st.set_page_config(
    page_title="WPPSI-IV Pro - Sistema de Informes",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== INICIALIZACIÓN DE SESSION STATE ====================
if 'datos_completos' not in st.session_state:
    st.session_state.datos_completos = False

# ==================== ESTILOS CSS PREMIUM ====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #A91D3A; 
        --secondary: #2c3e50;
        --bg-light: #f8f9fa;
        --text-dark: #212529;
    }

    * { font-family: 'Montserrat', sans-serif !important; }
    
    .stApp { background-color: var(--bg-light); }

    /* Encabezado */
    .header-container {
        background: linear-gradient(135deg, #A91D3A 0%, #800e26 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(169, 29, 58, 0.3);
        margin-bottom: 2rem;
        animation: slideDown 0.8s ease-out;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    /* Cards y Contenedores */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
        padding: 0.6rem !important;
        font-size: 15px !important;
        background-color: white !important;
        color: var(--text-dark) !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(169, 29, 58, 0.2) !important;
    }

    /* Métricas */
    div[data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid var(--primary);
        animation: fadeIn 0.5s ease-out;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--primary) !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(90deg, #A91D3A 0%, #C7254E 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 15px rgba(169, 29, 58, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(169, 29, 58, 0.5) !important;
    }

    /* Alertas - Corrección de color de texto */
    .stSuccess, .stInfo, .stWarning, .stError {
        padding: 1.2rem !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
    }
    
    .stSuccess { background-color: #d4edda !important; border-left: 6px solid #28a745 !important; }
    .stSuccess div, .stSuccess p { color: #155724 !important; font-weight: 600; }
    
    .stWarning { background-color: #fff3cd !important; border-left: 6px solid #ffc107 !important; }
    .stWarning div, .stWarning p { color: #856404 !important; font-weight: 600; }
    
    .stError { background-color: #f8d7da !important; border-left: 6px solid #dc3545 !important; }
    .stError div, .stError p { color: #721c24 !important; font-weight: 600; }

    /* Footer */
    .footer {
        margin-top: 4rem;
        padding: 2rem;
        text-align: center;
        background: white;
        border-radius: 15px;
        color: #6c757d;
        border-bottom: 4px solid var(--primary);
    }

    /* Animaciones */
    @keyframes slideDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    
    <div class="header-container">
        <div class="header-title">🧠 WPPSI-IV Pro</div>
        <div class="header-subtitle">Sistema Integral de Evaluación Psicopedagógica</div>
    </div>
""", unsafe_allow_html=True)

# ==================== DATOS Y TABLAS COMPLETAS (NO EDITAR) ====================
# Tablas de conversión completas según el código original proporcionado
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

TABLA_ICV = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:130, 28:137, 30:145}
TABLA_IVE = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:129, 28:136, 30:143, 32:150}
TABLA_IRF = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:130, 28:136, 30:143}
TABLA_IMT = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:95, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138, 30:145}
TABLA_IVP = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138}
TABLA_CIT = {10:40, 15:45, 20:52, 25:58, 30:64, 35:70, 40:76, 45:82, 50:88, 55:94, 60:100, 63:103, 65:106, 70:112, 75:118, 80:124, 85:130, 90:136}

TABLA_PERCENTILES = {
    40: 0.1, 45: 0.1, 50: 0.1, 55: 0.1, 60: 0.4, 65: 1, 70: 2, 75: 5,
    80: 9, 85: 16, 90: 25, 95: 37, 100: 50, 103: 58, 105: 63, 106: 66,
    109: 73, 110: 75, 115: 84, 120: 91, 125: 95, 128: 97, 130: 98,
    135: 99, 140: 99.6, 145: 99.9, 150: 99.9
}

# ==================== LÓGICA DE CÁLCULO ====================

def calcular_edad(fecha_nacimiento, fecha_aplicacion):
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

def convertir_pd_a_pe(prueba, pd_valor):
    if pd_valor is None or pd_valor == '': return None
    try:
        pd_int = int(pd_valor)
        return TABLAS_CONVERSION.get(prueba, {}).get(pd_int, None)
    except:
        return None

def buscar_en_tabla(tabla, suma):
    keys = sorted(tabla.keys())
    for key in keys:
        if suma <= key:
            return tabla[key]
    return tabla[keys[-1]]

def calcular_indices(pe_dict):
    def get_pe(key): return pe_dict.get(key, 0) if pe_dict.get(key) is not None else 0
    
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
        'suma_icv': suma_icv, 'suma_ive': suma_ive, 'suma_irf': suma_irf,
        'suma_imt': suma_imt, 'suma_ivp': suma_ivp, 'suma_cit': suma_cit
    }

def obtener_percentil(puntuacion):
    if puntuacion in TABLA_PERCENTILES: return TABLA_PERCENTILES[puntuacion]
    keys = sorted(TABLA_PERCENTILES.keys())
    for i in range(len(keys) - 1):
        if keys[i] <= puntuacion < keys[i + 1]: return TABLA_PERCENTILES[keys[i]]
    return 50

def obtener_categoria(puntuacion):
    if puntuacion >= 130: return {'categoria': 'Muy Superior', 'color': '#28a745', 'desc': 'Punto fuerte normativo'}
    elif puntuacion >= 120: return {'categoria': 'Superior', 'color': '#20c997', 'desc': 'Dentro de límites'}
    elif puntuacion >= 110: return {'categoria': 'Medio Alto', 'color': '#17a2b8', 'desc': 'Promedio alto'}
    elif puntuacion >= 90: return {'categoria': 'Medio', 'color': '#ffc107', 'desc': 'Promedio'}
    elif puntuacion >= 80: return {'categoria': 'Medio Bajo', 'color': '#fd7e14', 'desc': 'Promedio bajo'}
    elif puntuacion >= 70: return {'categoria': 'Límite', 'color': '#dc3545', 'desc': 'Punto débil normativo'}
    else: return {'categoria': 'Muy Bajo', 'color': '#6c757d', 'desc': 'Déficit significativo'}

# ==================== FUNCIONES GRÁFICAS PARA PDF (REPORTLAB PURO) ====================
# Estas funciones dibujan los gráficos directamente en el PDF para evitar dependencias externas.

def pdf_draw_profile_chart(pe_dict):
    """Dibuja el gráfico de líneas de puntuaciones escalares para el PDF"""
    drawing = Drawing(400, 200)
    
    data = []
    labels = []
    pruebas_orden = ['cubos', 'informacion', 'matrices', 'busqueda_animales', 'reconocimiento',
                     'semejanzas', 'conceptos', 'localizacion', 'cancelacion', 'rompecabezas']
    
    for p in pruebas_orden:
        val = pe_dict.get(p, 0)
        data.append(val if val is not None else 0)
        labels.append(p[:3].upper()) # Abreviatura

    # Configuración del gráfico
    lp = LinePlot()
    lp.x = 30
    lp.y = 30
    lp.height = 150
    lp.width = 350
    lp.data = [list(zip(range(len(data)), data))]
    lp.lines[0].strokeColor = colors.HexColor("#A91D3A")
    lp.lines[0].strokeWidth = 2
    lp.lines[0].symbol = makeMarker('Circle')
    lp.lines[0].symbol.size = 4
    lp.lines[0].symbol.fillColor = colors.HexColor("#A91D3A")
    lp.lines[0].symbol.strokeColor = colors.white

    # Ejes
    lp.xValueAxis.valueMin = -0.5
    lp.xValueAxis.valueMax = len(data) - 0.5
    lp.xValueAxis.labels.boxAnchor = 'n'
    lp.xValueAxis.labels.dx = 0
    lp.xValueAxis.labels.dy = -5
    # Asignar etiquetas manualmente (truco para ReportLab simple)
    # En una implementación simple de LinePlot, el eje X es numérico.
    
    lp.yValueAxis.valueMin = 0
    lp.yValueAxis.valueMax = 20
    lp.yValueAxis.valueStep = 2
    
    # Zonas de color (Fondo)
    # Dibujamos rectángulos detrás
    bg_group = Group()
    # Zona media (7-13)
    y_scale = 150 / 20
    bg_group.add(Rect(30, 30 + 7*y_scale, 350, 6*y_scale, fillColor=colors.HexColor("#fff3cd"), strokeColor=None))
    
    drawing.add(bg_group)
    drawing.add(lp)
    
    # Etiquetas X manuales
    for i, label in enumerate(labels):
        x_pos = 30 + (i * (350 / (len(labels)-1))) if len(labels)>1 else 30
        drawing.add(String(x_pos, 15, label, fontSize=8, textAnchor='middle'))

    return drawing

def pdf_draw_composite_chart(indices):
    """Dibuja el gráfico de barras de índices compuestos para el PDF"""
    drawing = Drawing(400, 200)
    
    data = []
    labels = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT']
    
    for l in labels:
        data.append(indices.get(l, 0))
        
    bc = VerticalBarChart()
    bc.x = 30
    bc.y = 30
    bc.height = 150
    bc.width = 350
    bc.data = [data]
    bc.barWidth = 25
    bc.bars[0].fillColor = colors.HexColor("#A91D3A")
    
    bc.valueAxis.valueMin = 40
    bc.valueAxis.valueMax = 160
    bc.valueAxis.valueStep = 20
    
    bc.categoryAxis.labels.boxAnchor = 'n'
    bc.categoryAxis.labels.dx = 0
    bc.categoryAxis.labels.dy = -5
    bc.categoryAxis.categoryNames = labels
    
    # Línea media 100
    y_100 = 30 + (100 - 40) * (150 / 120)
    linea_media = Line(30, y_100, 380, y_100)
    linea_media.strokeColor = colors.grey
    linea_media.strokeDashArray = [2, 2]
    
    drawing.add(bc)
    drawing.add(linea_media)
    
    return drawing

# ==================== GENERACIÓN DE PDF PROFESIONAL ====================

def generar_pdf_completo(meta, pd_dict, pe_dict, indices):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                            rightMargin=2*cm, leftMargin=2*cm, 
                            topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor("#A91D3A"), alignment=1, spaceAfter=20)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#2c3e50"), spaceBefore=15, spaceAfter=10)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, leading=14)
    
    elements = []
    
    # --- PORTADA ---
    elements.append(Paragraph("INFORME PSICOPEDAGÓGICO WPPSI-IV", title_style))
    elements.append(Spacer(1, 1*cm))
    
    # Tabla de Datos Personales
    data_personal = [
        ["Nombre:", meta['nombre'], "Fecha Evaluación:", meta['fecha'].strftime("%d/%m/%Y")],
        ["Edad:", meta['edad'], "Examinador:", meta['ex']]
    ]
    t_personal = Table(data_personal, colWidths=[3*cm, 5*cm, 3.5*cm, 4.5*cm])
    t_personal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8f9fa")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_personal)
    elements.append(Spacer(1, 1*cm))
    
    # --- PÁGINA DE RESUMEN (TABLAS) ---
    elements.append(Paragraph("1. Perfil de Puntuaciones Escalares", h2_style))
    
    # Preparar datos escalares
    data_esc = [["Prueba", "PD", "PE", "Clasificación"]]
    for k, v in pe_dict.items():
        pd_val = pd_dict.get(k, "-")
        clas = "Promedio"
        bg = colors.white
        if v >= 13: 
            clas = "Fortaleza"
            bg = colors.HexColor("#d4edda")
        elif v <= 7: 
            clas = "Debilidad"
            bg = colors.HexColor("#f8d7da")
        data_esc.append([k.upper(), pd_val, v, clas])
        
    t_esc = Table(data_esc, colWidths=[6*cm, 3*cm, 3*cm, 4*cm])
    t_esc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#A91D3A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f9f9f9")])
    ]))
    elements.append(t_esc)
    elements.append(Spacer(1, 1*cm))
    
    # GRÁFICO ESCALAR EN PDF
    elements.append(Paragraph("Gráfico de Perfil Escalar", h2_style))
    chart_esc = pdf_draw_profile_chart(pe_dict)
    elements.append(chart_esc)
    elements.append(Spacer(1, 1*cm))
    
    elements.append(PageBreak())
    
    # --- PUNTUACIONES COMPUESTAS ---
    elements.append(Paragraph("2. Perfil de Índices Compuestos (CI)", h2_style))
    
    data_ind = [["Índice", "Puntuación", "Percentil", "Categoría", "Int. Confianza"]]
    for k, v in indices.items():
        if k.startswith('suma'): continue
        cat_info = obtener_categoria(v)
        perc = obtener_percentil(v)
        # Intervalo confianza simulado para demo
        ic_min = v - 5
        ic_max = v + 5
        data_ind.append([k, v, perc, cat_info['categoria'], f"{ic_min}-{ic_max}"])
        
    t_ind = Table(data_ind, colWidths=[3*cm, 3*cm, 3*cm, 4*cm, 3*cm])
    t_ind.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    elements.append(t_ind)
    elements.append(Spacer(1, 1*cm))
    
    # GRÁFICO COMPUESTO EN PDF
    elements.append(Paragraph("Gráfico de Índices Compuestos", h2_style))
    chart_comp = pdf_draw_composite_chart(indices)
    elements.append(chart_comp)
    elements.append(Spacer(1, 1*cm))
    
    # --- INTERPRETACIÓN ---
    elements.append(Paragraph("3. Síntesis Diagnóstica", h2_style))
    cit = indices['CIT']
    cat = obtener_categoria(cit)
    
    texto = f"""
    El evaluado ha obtenido un Coeficiente Intelectual Total (CIT) de <b>{cit}</b>, situándose en la categoría 
    <b>{cat['categoria']}</b> en comparación con su grupo normativo.
    <br/><br/>
    <b>Análisis de Fortalezas y Debilidades:</b><br/>
    Se observan las siguientes características en el perfil cognitivo:
    """
    elements.append(Paragraph(texto, normal_style))
    
    # Listar fortalezas y debilidades
    fortalezas = [k for k, v in pe_dict.items() if v >= 13]
    debilidades = [k for k, v in pe_dict.items() if v <= 7]
    
    if fortalezas:
        elements.append(Paragraph(f"<b>Fortalezas (PE >= 13):</b> {', '.join(fortalezas).upper()}", normal_style))
    if debilidades:
        elements.append(Paragraph(f"<b>Debilidades (PE <= 7):</b> {', '.join(debilidades).upper()}", normal_style))
        
    elements.append(Spacer(1, 2*cm))
    elements.append(Paragraph("Informe generado automáticamente por WPPSI-IV Pro para Daniela.", normal_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ==================== FUNCIONES VISUALES STREAMLIT (PLOTLY) ====================
def st_chart_escalar(pe_dict):
    labels = [k.upper() for k in pe_dict.keys()]
    values = list(pe_dict.values())
    fig = go.Figure()
    # Zonas
    fig.add_hrect(y0=13, y1=19, fillcolor="rgba(40, 167, 69, 0.1)", line_width=0)
    fig.add_hrect(y0=7, y1=13, fillcolor="rgba(255, 243, 205, 0.5)", line_width=0)
    fig.add_hrect(y0=1, y1=7, fillcolor="rgba(220, 53, 69, 0.1)", line_width=0)
    
    fig.add_trace(go.Scatter(x=labels, y=values, mode='lines+markers+text',
                             text=values, textposition='top center',
                             line=dict(color='#A91D3A', width=4),
                             marker=dict(size=12, color='white', line=dict(width=2, color='#A91D3A'))))
    fig.update_layout(title="<b>Perfil de Puntuaciones Escalares</b>", yaxis=dict(range=[0, 20]), height=400)
    return fig

def st_chart_compuesto(indices):
    keys = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT']
    vals = [indices.get(k, 0) for k in keys]
    colors_map = [obtener_categoria(v)['color'] for v in vals]
    
    fig = go.Figure(data=[go.Bar(x=keys, y=vals, marker_color=colors_map, text=vals, textposition='auto')])
    fig.add_hline(y=100, line_dash="dash", line_color="black", annotation_text="Media")
    fig.update_layout(title="<b>Índices Compuestos (CI)</b>", yaxis=dict(range=[40, 160]), height=400)
    return fig

# ==================== INTERFAZ DE USUARIO ====================
st.markdown("""<div class="header-container"><div class="header-title">🧠 WPPSI-IV Pro</div><p>Sistema Profesional para Daniela</p></div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📝 Ingreso de Datos", "📊 Resultados Gráficos", "🔍 Análisis Clínico", "📄 Informe PDF"])

# --- TAB 1: DATOS ---
with tab1:
    st.markdown("### 👤 Datos del Paciente")
    c1, c2, c3 = st.columns(3)
    nombre = c1.text_input("Nombre Completo", "Micaela")
    fecha_nac = c2.date_input("Fecha Nacimiento", date(2020, 10, 1))
    fecha_app = c3.date_input("Fecha Evaluación", date.today())
    examinador = st.text_input("Examinador/a", "Daniela")
    
    st.markdown("### 🔢 Puntuaciones Directas (PD)")
    st.info("Ingrese los valores directos obtenidos en cada subtest.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Área Verbal y Visoespacial**")
        pd_info = st.number_input("Información", 0, 40, 10)
        pd_sem = st.number_input("Semejanzas", 0, 40, 13)
        pd_cubos = st.number_input("Cubos", 0, 40, 16)
        pd_rom = st.number_input("Rompecabezas", 0, 40, 13)
        pd_rec = st.number_input("Reconocimiento", 0, 40, 11)
        
    with c2:
        st.markdown("**Razonamiento y Velocidad**")
        pd_mat = st.number_input("Matrices", 0, 40, 11)
        pd_con = st.number_input("Conceptos", 0, 40, 11)
        pd_loc = st.number_input("Localización", 0, 40, 8)
        pd_bus = st.number_input("Búsq. Animales", 0, 70, 12)
        pd_can = st.number_input("Cancelación", 0, 70, 8)

    if st.button("PROCESAR DATOS", type="primary"):
        pd_inputs = {
            'cubos': pd_cubos, 'informacion': pd_info, 'matrices': pd_mat,
            'busqueda_animales': pd_bus, 'reconocimiento': pd_rec,
            'semejanzas': pd_sem, 'conceptos': pd_con, 'localizacion': pd_loc,
            'cancelacion': pd_can, 'rompecabezas': pd_rom
        }
        
        pe_res = {}
        for k, v in pd_inputs.items():
            pe = convertir_pd_a_pe(k, v)
            pe_res[k] = pe if pe is not None else 0
            
        indices_res = calcular_indices(pe_res)
        
        st.session_state.datos_completos = True
        st.session_state.pe = pe_res
        st.session_state.indices = indices_res
        st.session_state.pd = pd_inputs
        st.session_state.meta = {'nombre': nombre, 'edad': f"{(fecha_app-fecha_nac).days//365} años", 'ex': examinador, 'fecha': fecha_app}
        st.success("¡Datos procesados correctamente!")

# --- TAB 2: RESULTADOS ---
with tab2:
    if st.session_state.datos_completos:
        st.markdown("### 📊 Tablero de Control")
        ind = st.session_state.indices
        
        # KPIs
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("CIT Total", ind['CIT'])
        k2.metric("ICV Verbal", ind['ICV'])
        k3.metric("IVE Viso", ind['IVE'])
        k4.metric("IRF Razon.", ind['IRF'])
        k5.metric("IMT Memoria", ind['IMT'])
        
        st.markdown("---")
        
        g1, g2 = st.columns(2)
        with g1: st.plotly_chart(st_chart_escalar(st.session_state.pe), use_container_width=True)
        with g2: st.plotly_chart(st_chart_compuesto(st.session_state.indices), use_container_width=True)
        
        # Tabla conversión
        st.markdown("### 📋 Tabla de Conversión")
        rows = []
        for k, v in st.session_state.pe.items():
            rows.append({"Subprueba": k.upper(), "PD": st.session_state.pd[k], "PE": v})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.warning("Por favor ingrese los datos primero.")

# --- TAB 3: ANÁLISIS ---
with tab3:
    if st.session_state.datos_completos:
        pe = st.session_state.pe
        
        c1, c2 = st.columns(2)
        with c1:
            st.success("##### ✅ Puntos Fuertes (PE ≥ 13)")
            for k, v in pe.items():
                if v >= 13: st.write(f"**{k.upper()}**: {v}")
                
        with c2:
            st.error("##### ⚠️ Puntos Débiles (PE ≤ 7)")
            for k, v in pe.items():
                if v <= 7: st.write(f"**{k.upper()}**: {v}")
                
        st.markdown("---")
        st.markdown("### 🧠 Interpretación del CIT")
        cit = st.session_state.indices['CIT']
        cat = obtener_categoria(cit)
        st.info(f"El Coeficiente Intelectual Total de **{cit}** sitúa al evaluado en el rango **{cat['categoria']}** ({cat['desc']}).")

# --- TAB 4: PDF ---
with tab4:
    if st.session_state.datos_completos:
        st.markdown("### 📥 Descarga de Informe Oficial")
        st.write("Genera un PDF con todos los gráficos vectorizados y tablas formateadas.")
        
        pdf_bytes = generar_pdf_completo(
            st.session_state.meta,
            st.session_state.pd,
            st.session_state.pe,
            st.session_state.indices
        )
        
        st.download_button(
            label="📄 DESCARGAR PDF PROFESIONAL",
            data=pdf_bytes,
            file_name=f"Informe_WPPSI_{st.session_state.meta['nombre']}.pdf",
            mime="application/pdf",
            type="primary"
        )
    else:
        st.warning("Complete los datos en la pestaña 1 para habilitar la descarga.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Desarrollado para Daniela ❤️ | Sistema Profesional v3.0</div>", unsafe_allow_html=True)
