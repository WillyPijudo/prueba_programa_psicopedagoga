import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io

# ===== CONFIGURACIÓN =====
st.set_page_config(
    page_title="WPPSI-IV - Cuadernillo de Anotación",
    page_icon="🧠",
    layout="wide"
)

# ===== ESTILOS CSS =====
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { 
        background: #f8f9fa;
        color: #212529;
    }
    
    h1, h2, h3, h4 { color: #212529 !important; }
    
    /* Inputs con buen contraste */
    input, select, .stNumberInput input, .stTextInput input, .stDateInput input, .stSelectbox select {
        background-color: white !important;
        color: #212529 !important;
        border: 2px solid #dee2e6 !important;
        font-size: 16px !important;
    }
    
    label { 
        color: #212529 !important; 
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Botones */
    .stButton > button {
        background: #8B1538 !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border: none !important;
        font-size: 16px !important;
    }
    
    .stButton > button:hover {
        background: #6d1029 !important;
    }
    
    /* Tablas */
    .dataframe { font-size: 14px !important; }
    .dataframe th {
        background: #8B1538 !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px !important;
    }
    .dataframe td {
        padding: 8px !important;
        color: #212529 !important;
        background: white !important;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] { color: #212529 !important; }
    [data-testid="stMetricLabel"] { color: #495057 !important; }
    
    /* Mensajes */
    .stSuccess, .stError, .stWarning, .stInfo {
        color: #212529 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ===== TABLAS DE CONVERSIÓN =====
TABLAS_CONVERSION = {
    'cubos': {0:1, 1:1, 2:1, 3:1, 4:1, 5:2, 6:3, 7:4, 8:5, 9:6, 10:7, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:16, 19:17, 20:17, 21:18, 22:18, 23:19, 24:19, 25:19, 26:19, 27:19, 28:19, 29:19, 30:19},
    'informacion': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:15, 17:16, 18:17, 19:18, 20:18, 21:19, 22:19, 23:19, 24:19, 25:19, 26:19},
    'matrices': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:9, 10:10, 11:11, 12:12, 13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19},
    'busqueda_animales': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:17, 20:18, 21:19},
    'reconocimiento': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:8, 9:10, 10:11, 11:13, 12:14, 13:16, 14:17, 15:18, 16:19},
    'semejanzas': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:16, 20:17, 21:17, 22:18, 23:18, 24:19, 25:19, 26:19, 27:19, 28:19, 29:19},
    'conceptos': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:17, 18:18, 19:19},
    'localizacion': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:7, 8:8, 9:9, 10:11, 11:12, 12:13, 13:14, 14:15, 15:16, 16:17, 17:18, 18:19, 19:19, 20:19},
    'cancelacion': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19, 21:19},
    'rompecabezas': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19}
}

TABLA_ICV = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:130, 28:137, 30:145}
TABLA_IVE = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:129, 28:136, 30:143, 32:150}
TABLA_IRF = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:130, 28:136, 30:143}
TABLA_IMT = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:95, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138, 30:145}
TABLA_IVP = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138}
TABLA_CIT = {10:40, 15:45, 20:52, 25:58, 30:64, 35:70, 40:76, 45:82, 50:88, 55:94, 60:100, 63:103, 65:106, 70:112, 75:118, 80:124, 85:130, 90:136}

TABLA_PERCENTILES = {
    40:0.1, 45:0.1, 50:0.1, 55:0.1, 60:0.4, 65:1, 70:2, 75:5, 80:9, 85:16, 90:25, 
    95:37, 100:50, 103:58, 105:63, 106:66, 109:73, 110:75, 115:84, 120:91, 125:95, 
    128:97, 130:98, 135:99, 140:99.6, 145:99.9, 150:99.9
}

# ===== FUNCIONES =====
def calcular_edad(fecha_nac, fecha_apl):
    years = fecha_apl.year - fecha_nac.year
    months = fecha_apl.month - fecha_nac.month
    days = fecha_apl.day - fecha_nac.day
    if days < 0:
        months -= 1
        days += 30
    if months < 0:
        years -= 1
        months += 12
    return years, months, days

def convertir_pd_a_pe(prueba, pd):
    if pd is None or pd == '':
        return None
    return TABLAS_CONVERSION.get(prueba, {}).get(int(pd), None)

def buscar_en_tabla(tabla, suma):
    keys = sorted(tabla.keys())
    for key in keys:
        if suma <= key:
            return tabla[key]
    return tabla[keys[-1]]

def calcular_indices(pe_dict):
    suma_icv = (pe_dict.get('informacion', 0) or 0) + (pe_dict.get('semejanzas', 0) or 0)
    suma_ive = (pe_dict.get('cubos', 0) or 0) + (pe_dict.get('rompecabezas', 0) or 0)
    suma_irf = (pe_dict.get('matrices', 0) or 0) + (pe_dict.get('conceptos', 0) or 0)
    suma_imt = (pe_dict.get('reconocimiento', 0) or 0) + (pe_dict.get('localizacion', 0) or 0)
    suma_ivp = (pe_dict.get('busqueda_animales', 0) or 0) + (pe_dict.get('cancelacion', 0) or 0)
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
    return TABLA_PERCENTILES.get(puntuacion, 50)

def obtener_categoria(puntuacion):
    if puntuacion >= 130: return 'Muy superior'
    elif puntuacion >= 120: return 'Superior'
    elif puntuacion >= 110: return 'Medio alto'
    elif puntuacion >= 90: return 'Medio'
    elif puntuacion >= 80: return 'Medio bajo'
    elif puntuacion >= 70: return 'Límite'
    else: return 'Muy bajo'

def crear_grafico_perfil_escalares(pe_dict):
    """Gráfico estilo WPPSI-IV: líneas conectadas con puntos"""
    pruebas = ['Cubos', 'Información', 'Matrices', 'B.Animales', 'Reconoc.', 
               'Semejanzas', 'Conceptos', 'Localiz.', 'Cancelac.', 'Rompecab.']
    keys = ['cubos', 'informacion', 'matrices', 'busqueda_animales', 'reconocimiento',
            'semejanzas', 'conceptos', 'localizacion', 'cancelacion', 'rompecabezas']
    
    valores = [pe_dict.get(k, 10) or 10 for k in keys]
    
    fig = go.Figure()
    
    # Línea conectando puntos
    fig.add_trace(go.Scatter(
        x=list(range(len(pruebas))),
        y=valores,
        mode='lines+markers',
        line=dict(color='#8B1538', width=3),
        marker=dict(size=12, color='#8B1538', symbol='circle',
                   line=dict(color='white', width=2)),
        name='Puntuaciones Escalares',
        hovertemplate='<b>%{text}</b><br>PE: %{y}<extra></extra>',
        text=pruebas
    ))
    
    # Líneas de referencia
    fig.add_hline(y=10, line_dash="dash", line_color="gray", 
                 annotation_text="Media", annotation_position="right")
    fig.add_hline(y=7, line_dash="dot", line_color="red", opacity=0.5)
    fig.add_hline(y=13, line_dash="dot", line_color="green", opacity=0.5)
    
    # Zonas sombreadas
    fig.add_hrect(y0=7, y1=13, fillcolor="lightyellow", opacity=0.2, line_width=0)
    fig.add_hrect(y0=13, y1=19, fillcolor="lightgreen", opacity=0.1, line_width=0)
    fig.add_hrect(y0=1, y1=7, fillcolor="lightcoral", opacity=0.1, line_width=0)
    
    fig.update_layout(
        title='Perfil de Puntuaciones Escalares',
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(pruebas))),
            ticktext=pruebas,
            tickangle=-45
        ),
        yaxis=dict(range=[0, 20], dtick=1, title='Puntuación Escalar'),
        height=500,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

def crear_grafico_perfil_compuestas(indices):
    """Gráfico estilo WPPSI-IV: barras con intervalos"""
    nombres = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT']
    valores = [indices['ICV'], indices['IVE'], indices['IRF'], 
              indices['IMT'], indices['IVP'], indices['CIT']]
    
    # Colores según categoría
    colores = []
    for v in valores:
        if v >= 130: colores.append('#2E7D32')
        elif v >= 120: colores.append('#66BB6A')
        elif v >= 110: colores.append('#81C784')
        elif v >= 90: colores.append('#FDD835')
        elif v >= 80: colores.append('#FFB74D')
        elif v >= 70: colores.append('#FF8A65')
        else: colores.append('#E53935')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=nombres,
        y=valores,
        marker=dict(color=colores, line=dict(color='#212529', width=2)),
        text=valores,
        textposition='outside',
        textfont=dict(size=14, color='#212529'),
        hovertemplate='<b>%{x}</b><br>Puntuación: %{y}<br>Percentil: %{customdata}<extra></extra>',
        customdata=[obtener_percentil(v) for v in valores]
    ))
    
    # Línea de la media
    fig.add_hline(y=100, line_dash="dash", line_color="#212529", 
                 annotation_text="Media (100)", annotation_position="left")
    
    # Zonas de clasificación
    fig.add_hrect(y0=130, y1=160, fillcolor="green", opacity=0.1, line_width=0)
    fig.add_hrect(y0=120, y1=130, fillcolor="lightgreen", opacity=0.1, line_width=0)
    fig.add_hrect(y0=110, y1=120, fillcolor="lightblue", opacity=0.1, line_width=0)
    fig.add_hrect(y0=90, y1=110, fillcolor="lightyellow", opacity=0.1, line_width=0)
    fig.add_hrect(y0=80, y1=90, fillcolor="orange", opacity=0.1, line_width=0)
    fig.add_hrect(y0=70, y1=80, fillcolor="lightcoral", opacity=0.1, line_width=0)
    
    fig.update_layout(
        title='Perfil de Puntuaciones Compuestas',
        xaxis_title='Índices',
        yaxis=dict(range=[40, 160], dtick=10, title='Puntuación Compuesta'),
        height=500,
        template='plotly_white'
    )
    
    return fig

def crear_curva_normal(cit_value):
    """Curva normal de clasificación"""
    import numpy as np
    x = np.linspace(40, 160, 200)
    y = np.exp(-0.5 * ((x - 100) / 15) ** 2)
    
    fig = go.Figure()
    
    # Curva
    fig.add_trace(go.Scatter(
        x=x, y=y,
        fill='tozeroy',
        fillcolor='rgba(139, 21, 56, 0.2)',
        line=dict(color='#8B1538', width=2),
        name='Distribución Normal'
    ))
    
    # Marcador de posición
    fig.add_vline(x=cit_value, line_dash="dash", line_color="red", line_width=3,
                 annotation_text=f"CIT: {cit_value}", annotation_position="top")
    
    # Etiquetas de clasificación
    clasificaciones = [
        (70, "Límite"), (85, "Medio bajo"), (100, "Medio"), 
        (115, "Medio alto"), (130, "Superior")
    ]
    
    for pos, texto in clasificaciones:
        fig.add_vline(x=pos, line_dash="dot", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title='Curva Normal de Clasificación',
        xaxis=dict(range=[40, 160], title='Puntuación Compuesta'),
        yaxis=dict(showticklabels=False, title='Densidad'),
        height=400,
        template='plotly_white',
        showlegend=False
    )
    
    return fig

# ===== INTERFAZ =====
st.title("🧠 WPPSI-IV - Escala de Inteligencia de Wechsler para Preescolar")
st.markdown("### Cuadernillo de Anotación Digital")

st.divider()

# Datos del paciente
col1, col2, col3, col4 = st.columns(4)
with col1:
    nombre = st.text_input("👤 Nombre del niño/a", "Micaela")
with col2:
    sexo = st.selectbox("Sexo", ["F", "M"])
with col3:
    fecha_nac = st.date_input("📅 Fecha de nacimiento", date(2020, 10, 1))
with col4:
    fecha_apl = st.date_input("📅 Fecha de aplicación", date.today())

col5, col6 = st.columns(2)
with col5:
    examinador = st.text_input("👨‍⚕️ Examinador/a", "Daniela")
with col6:
    lugar = st.text_input("📍 Lugar", "Argentina")

st.divider()

# Puntuaciones Directas
st.markdown("## 📊 Conversión de Puntuaciones Directas a Escalares")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Comprensión Verbal**")
    pd_info = st.number_input("Información", 0, 30, 10, key="info")
    pd_sem = st.number_input("Semejanzas", 0, 30, 13, key="sem")
    
    st.markdown("**Visoespacial**")
    pd_cub = st.number_input("Cubos", 0, 30, 15, key="cub")
    pd_rom = st.number_input("Rompecabezas", 0, 30, 13, key="rom")

with col2:
    st.markdown("**Razonamiento Fluido**")
    pd_mat = st.number_input("Matrices", 0, 30, 11, key="mat")
    pd_con = st.number_input("Conceptos", 0, 30, 11, key="con")
    
    st.markdown("**Memoria de Trabajo**")
    pd_rec = st.number_input("Reconocimiento", 0, 30, 8, key="rec")
    pd_loc = st.number_input("Localización", 0, 30, 12, key="loc")

with col3:
    st.markdown("**Velocidad de Procesamiento**")
    pd_bus = st.number_input("Búsqueda de Animales", 0, 30, 12, key="bus")
    pd_can = st.number_input("Cancelación", 0, 30, 8, key="can")

st.divider()

if st.button("🎯 GENERAR INFORME COMPLETO", type="primary"):
    # Calcular edad
    years, months, days = calcular_edad(fecha_nac, fecha_apl)
    
    # Convertir PD a PE
    puntuaciones = {
        'cubos': pd_cub, 'informacion': pd_info, 'matrices': pd_mat,
        'busqueda_animales': pd_bus, 'reconocimiento': pd_rec,
        'semejanzas': pd_sem, 'conceptos': pd_con,
        'localizacion': pd_loc, 'cancelacion': pd_can, 'rompecabezas': pd_rom
    }
    
    pe_dict = {k: convertir_pd_a_pe(k, v) for k, v in puntuaciones.items() if v is not None}
    indices = calcular_indices(pe_dict)
    
    st.success("✅ ¡Informe generado exitosamente!")
    
    st.divider()
    
    # RESUMEN
    st.markdown("## 📋 Página de Resumen")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Edad", f"{years} años, {months} meses")
    col2.metric("CI Total (CIT)", indices['CIT'])
    col3.metric("Percentil", obtener_percentil(indices['CIT']))
    col4.metric("Clasificación", obtener_categoria(indices['CIT']))
    
    st.divider()
    
    # TABLA DE CONVERSIÓN
    st.markdown("### 🔄 Conversión de Puntuaciones")
    
    df_conv = pd.DataFrame({
        'Prueba': ['Cubos', 'Información', 'Matrices', 'Búsqueda Animales', 
                  'Reconocimiento', 'Semejanzas', 'Conceptos', 'Localización',
                  'Cancelación', 'Rompecabezas'],
        'PD': [puntuaciones[k] for k in ['cubos', 'informacion', 'matrices', 
               'busqueda_animales', 'reconocimiento', 'semejanzas', 'conceptos',
               'localizacion', 'cancelacion', 'rompecabezas']],
        'PE': [pe_dict[k] for k in ['cubos', 'informacion', 'matrices',
               'busqueda_animales', 'reconocimiento', 'semejanzas', 'conceptos',
               'localizacion', 'cancelacion', 'rompecabezas']]
    })
    
    st.dataframe(df_conv, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # GRÁFICOS
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(crear_grafico_perfil_escalares(pe_dict), use_container_width=True)
    
    with col2:
        st.plotly_chart(crear_grafico_perfil_compuestas(indices), use_container_width=True)
    
    st.divider()
    
    # CURVA NORMAL
    st.plotly_chart(crear_curva_normal(indices['CIT']), use_container_width=True)
    
    st.divider()
    
    # ÍNDICES COMPUESTOS
    st.markdown("### 📊 Índices Compuestos")
    
    df_indices = pd.DataFrame({
        'Índice': ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT'],
        'Suma PE': [indices['suma_icv'], indices['suma_ive'], indices['suma_irf'],
                   indices['suma_imt'], indices['suma_ivp'], indices['suma_cit']],
        'Puntuación': [indices['ICV'], indices['IVE'], indices['IRF'],
                      indices['IMT'], indices['IVP'], indices['CIT']],
        'Percentil': [obtener_percentil(indices['ICV']), obtener_percentil(indices['IVE']),
                     obtener_percentil(indices['IRF']), obtener_percentil(indices['IMT']),
                     obtener_percentil(indices['IVP']), obtener_percentil(indices['CIT'])],
        'Clasificación': [obtener_categoria(indices['ICV']), obtener_categoria(indices['IVE']),
                         obtener_categoria(indices['IRF']), obtener_categoria(indices['IMT']),
                         obtener_categoria(indices['IVP']), obtener_categoria(indices['CIT'])]
    })
    
    st.dataframe(df_indices, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # FORTALEZAS Y DEBILIDADES
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Fortalezas (PE ≥ 13)")
        fortalezas = [(k.replace('_', ' ').title(), v) for k, v in pe_dict.items() if v >= 13]
        if fortalezas:
            for prueba, valor in fortalezas:
                st.success(f"**{prueba}**: {valor}")
        else:
            st.info("No hay fortalezas significativas")
    
    with col2:
        st.markdown("### ⚠️ Debilidades (PE ≤ 7)")
        debilidades = [(k.replace('_', ' ').title(), v) for k, v in pe_dict.items() if v <= 7]
        if debilidades:
            for prueba, valor in debilidades:
                st.warning(f"**{prueba}**: {valor}")
        else:
            st.info("No hay debilidades significativas")

st.divider()
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6c757d;'>WPPSI-IV - Escala de Inteligencia de Wechsler para Preescolar y Primaria-IV</p>", unsafe_allow_html=True)
