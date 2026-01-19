"""
WPPSI-IV - Generador de Informes Psicopedagógicos
Sistema completo con PDF Profesional, Diseño Premium y Tablas Clínicas Exactas.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import numpy as np
import io

# Librerías para PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

# ==================== CONFIGURACIÓN DE LA PÁGINA ====================
st.set_page_config(
    page_title="WPPSI-IV Pro",
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
        --bg: #f8f9fa;
    }

    * { font-family: 'Montserrat', sans-serif !important; }
    .stApp { background-color: var(--bg); }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #A91D3A 0%, #800e26 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(169, 29, 58, 0.25);
        margin-bottom: 2rem;
    }
    .main-header h1 { color: white !important; font-weight: 700; font-size: 2.5rem; }

    /* Cards & Containers */
    div[data-testid="metric-container"] {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid var(--primary);
    }
    [data-testid="stMetricValue"] { color: var(--primary) !important; font-weight: 700 !important; }

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        border-radius: 8px !important;
        border: 1px solid #ddd !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(169, 29, 58, 0.2) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #A91D3A 0%, #C7254E 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 50px !important;
        box-shadow: 0 4px 15px rgba(169, 29, 58, 0.3) !important;
        transition: transform 0.2s;
    }
    .stButton > button:hover { transform: scale(1.02); }

    /* Fix Alerts Text Color */
    .stSuccess div, .stSuccess p { color: #155724 !important; font-weight: 600; }
    .stInfo div, .stInfo p { color: #0c5460 !important; font-weight: 600; }
    .stWarning div, .stWarning p { color: #856404 !important; font-weight: 600; }
    .stError div, .stError p { color: #721c24 !important; font-weight: 600; }

    /* Footer */
    .footer { margin-top: 3rem; padding: 2rem; text-align: center; background: white; border-radius: 15px; }
    </style>
    
    <div class="main-header">
        <h1>🧠 WPPSI-IV Sistema Profesional</h1>
        <p>Evaluación Clínica y Generación de Informes</p>
    </div>
""", unsafe_allow_html=True)

# ==================== DATOS CLÍNICOS (TABLAS COMPLETAS RESTAURADAS) ====================
# Estas son TUS tablas originales para mantener la precisión.

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

# ==================== FUNCIONES DE CÁLCULO ====================

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
        return TABLAS_CONVERSION.get(prueba, {}).get(pd_int, 1) # Retorna 1 si no encuentra
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

# ==================== GENERADOR PDF PROFESIONAL ====================
def generar_pdf_reportlab(nombre, edad, examinador, fecha, pd_dict, pe_dict, indices):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    # Estilos PDF
    style_title = ParagraphStyle('MainTitle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#A91D3A'), alignment=1, spaceAfter=15)
    style_h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#2c3e50'), spaceAfter=10, spaceBefore=10)
    style_normal = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, leading=12)
    
    elements = []
    
    # Header
    elements.append(Paragraph("INFORME PSICOPEDAGÓGICO WPPSI-IV", style_title))
    elements.append(Paragraph("Perfil de Resultados Confidencial", style_normal))
    elements.append(Spacer(1, 0.5*cm))
    
    # Tabla Datos
    data_pac = [["Evaluado:", nombre, "Fecha:", fecha.strftime("%d/%m/%Y")],
                ["Edad:", edad, "Examinador:", examinador]]
    t_pac = Table(data_pac, colWidths=[3*cm, 5*cm, 3*cm, 5*cm])
    t_pac.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_pac)
    elements.append(Spacer(1, 0.5*cm))
    
    # Tabla Escalares
    elements.append(Paragraph("1. Perfil de Puntuaciones Escalares", style_h2))
    data_esc = [["Prueba", "PD", "PE", "Clasificación"]]
    for k, v in pe_dict.items():
        pd_val = pd_dict.get(k, "-")
        cat = "Promedio"
        bg_col = colors.white
        if v >= 13: 
            cat = "Fortaleza"
            bg_col = colors.HexColor('#d4edda')
        elif v <= 7: 
            cat = "Debilidad"
            bg_col = colors.HexColor('#f8d7da')
        
        data_esc.append([k.capitalize(), pd_val, v, cat])
        
    t_esc = Table(data_esc, colWidths=[6*cm, 3*cm, 3*cm, 4*cm])
    t_esc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#A91D3A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    elements.append(t_esc)
    elements.append(Spacer(1, 0.5*cm))
    
    # Tabla Índices
    elements.append(Paragraph("2. Perfil de Índices Compuestos", style_h2))
    data_ind = [["Índice", "Puntuación", "Percentil", "Categoría"]]
    for k, v in indices.items():
        if k.startswith("suma"): continue # Saltar sumas internas
        info_cat = obtener_categoria(v)
        perc = obtener_percentil(v)
        data_ind.append([k, v, perc, info_cat['categoria']])
        
    t_ind = Table(data_ind, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    t_ind.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    elements.append(t_ind)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ==================== FUNCIONES GRÁFICAS (PLOTLY) ====================
def crear_grafico_escalar(pe_dict):
    labels = [k.capitalize() for k in pe_dict.keys()]
    values = list(pe_dict.values())
    
    fig = go.Figure()
    # Zonas de color
    fig.add_hrect(y0=13, y1=19, fillcolor="rgba(40, 167, 69, 0.1)", line_width=0)
    fig.add_hrect(y0=7, y1=13, fillcolor="rgba(255, 193, 7, 0.1)", line_width=0)
    fig.add_hrect(y0=1, y1=7, fillcolor="rgba(220, 53, 69, 0.1)", line_width=0)
    
    fig.add_trace(go.Scatter(x=labels, y=values, mode='lines+markers+text', 
                             text=values, textposition='top center',
                             line=dict(color='#A91D3A', width=4),
                             marker=dict(size=12, color='white', line=dict(width=2, color='#A91D3A'))))
    
    fig.update_layout(title="<b>Perfil de Puntuaciones Escalares</b>", 
                      yaxis=dict(range=[0, 20], title="Punt. Escalar"),
                      height=400, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def crear_grafico_compuesto(indices):
    keys = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT']
    vals = [indices.get(k, 0) for k in keys]
    colors_bar = [obtener_categoria(v)['color'] for v in vals]
    
    fig = go.Figure(data=[go.Bar(
        x=keys, y=vals,
        marker_color=colors_bar,
        text=vals, textposition='auto'
    )])
    
    fig.add_hline(y=100, line_dash="dash", line_color="black")
    fig.update_layout(title="<b>Índices Compuestos (CI)</b>", yaxis=dict(range=[40, 160]), height=400)
    return fig

# ==================== INTERFAZ DE USUARIO ====================
st.markdown("""<div class="daniela-avatar">👩‍🦱</div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📝 Datos", "📊 Resultados", "📈 Análisis Detallado", "📥 Informe PDF"])

# --- TAB 1: DATOS ---
with tab1:
    st.markdown("### 👤 Datos del Niño/a")
    c1, c2, c3 = st.columns(3)
    nombre = c1.text_input("Nombre", "Micaela")
    fecha_nac = c2.date_input("Fecha Nacimiento", date(2020, 10, 1))
    fecha_app = c3.date_input("Fecha Aplicación", date.today())
    examinador = st.text_input("Examinador", "Daniela")
    
    st.markdown("---")
    st.markdown("### 🔢 Puntuaciones Directas")
    
    # Inputs organizados
    c1, c2, c3 = st.columns(3)
    with c1:
        st.caption("Verbal")
        pd_info = st.number_input("Información", 0, 40, 10)
        pd_sem = st.number_input("Semejanzas", 0, 40, 13)
        st.caption("Visoespacial")
        pd_cubos = st.number_input("Cubos", 0, 40, 16)
        pd_rom = st.number_input("Rompecabezas", 0, 40, 13)
        
    with c2:
        st.caption("Razonamiento")
        pd_mat = st.number_input("Matrices", 0, 40, 11)
        pd_con = st.number_input("Conceptos", 0, 40, 11)
        st.caption("Memoria")
        pd_rec = st.number_input("Reconocimiento", 0, 40, 11)
        pd_loc = st.number_input("Localización", 0, 40, 8)
        
    with c3:
        st.caption("Velocidad")
        pd_bus = st.number_input("Búsq. Animales", 0, 70, 12)
        pd_can = st.number_input("Cancelación", 0, 70, 8)

    if st.button("✨ Procesar Datos", type="primary"):
        # Cálculos usando TUS tablas
        pd_inputs = {
            'cubos': pd_cubos, 'informacion': pd_info, 'matrices': pd_mat,
            'busqueda_animales': pd_bus, 'reconocimiento': pd_rec,
            'semejanzas': pd_sem, 'conceptos': pd_con, 'localizacion': pd_loc,
            'cancelacion': pd_can, 'rompecabezas': pd_rom
        }
        
        pe_res = {k: convertir_pd_a_pe(k, v) for k, v in pd_inputs.items()}
        indices_res = calcular_indices(pe_res)
        
        # Guardar en estado
        st.session_state.datos_completos = True
        st.session_state.pe = pe_res
        st.session_state.indices = indices_res
        st.session_state.pd = pd_inputs
        st.session_state.meta = {'nombre': nombre, 'edad': f"{(fecha_app-fecha_nac).days//365} años", 'ex': examinador, 'fecha': fecha_app}
        st.success("¡Datos procesados correctamente!")

# --- TAB 2: RESULTADOS ---
with tab2:
    if st.session_state.datos_completos:
        # Métricas
        ind = st.session_state.indices
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("CIT Total", ind['CIT'])
        k2.metric("Verbal (ICV)", ind['ICV'])
        k3.metric("Viso (IVE)", ind['IVE'])
        k4.metric("Razon. (IRF)", ind['IRF'])
        
        st.markdown("---")
        
        # Gráficos
        g1, g2 = st.columns(2)
        with g1: st.plotly_chart(crear_grafico_escalar(st.session_state.pe), use_container_width=True)
        with g2: st.plotly_chart(crear_grafico_compuesto(st.session_state.indices), use_container_width=True)
        
        # Tabla de Conversión
        st.markdown("### 📋 Tabla de Conversión")
        rows = []
        for k, v in st.session_state.pe.items():
            pd_val = st.session_state.pd.get(k)
            rows.append({"Prueba": k.capitalize(), "PD": pd_val, "PE": v})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# --- TAB 3: ANÁLISIS ---
with tab3:
    if st.session_state.datos_completos:
        st.markdown("### 🔍 Análisis de Fortalezas y Debilidades")
        
        c1, c2 = st.columns(2)
        pe = st.session_state.pe
        
        with c1:
            st.success("##### ✅ Fortalezas (PE ≥ 13)")
            found_f = False
            for k, v in pe.items():
                if v >= 13:
                    st.write(f"**{k.capitalize()}**: {v}")
                    st.progress(v/19)
                    found_f = True
            if not found_f: st.info("No se detectaron fortalezas significativas.")
            
        with c2:
            st.error("##### ⚠️ Debilidades (PE ≤ 7)")
            found_d = False
            for k, v in pe.items():
                if v <= 7:
                    st.write(f"**{k.capitalize()}**: {v}")
                    st.progress(v/19)
                    found_d = True
            if not found_d: st.info("No se detectaron debilidades significativas.")
            
        st.markdown("---")
        st.markdown("### 🧠 Interpretación Clínica")
        cit = st.session_state.indices['CIT']
        cat = obtener_categoria(cit)
        
        st.info(f"""
        El paciente obtuvo un **CIT de {cit}**, ubicándose en la categoría **{cat['categoria']}** ({cat['desc']}).
        Esto indica que su rendimiento general supera al **{obtener_percentil(cit)}%** de los niños de su edad.
        """)

# --- TAB 4: PDF ---
with tab4:
    if st.session_state.datos_completos:
        st.markdown("### 📥 Generar Informe Oficial")
        st.write("Descarga un PDF formateado profesionalmente para imprimir o enviar.")
        
        pdf_file = generar_pdf_reportlab(
            st.session_state.meta['nombre'],
            st.session_state.meta['edad'],
            st.session_state.meta['ex'],
            st.session_state.meta['fecha'],
            st.session_state.pd,
            st.session_state.pe,
            st.session_state.indices
        )
        
        st.download_button(
            label="📄 Descargar PDF Profesional",
            data=pdf_file,
            file_name=f"Informe_WPPSI_{st.session_state.meta['nombre']}.pdf",
            mime="application/pdf",
            type="primary"
        )
    else:
        st.warning("Primero debes procesar los datos en la pestaña 1.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Desarrollado para Daniela ❤️ | v2.0 Professional</div>", unsafe_allow_html=True)
