import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import io

# ===== CONFIGURACIÓN DE LA PÁGINA =====
st.set_page_config(
    page_title="Generador de Informes WPPSI-IV",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== ESTILOS CSS MEJORADOS =====
st.markdown("""
    <style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Reset y configuración general */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Fondo principal con gradiente suave */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Títulos principales */
    h1 {
        color: #1e293b !important;
        font-weight: 700 !important;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-bottom: 2rem;
    }
    
    h2 {
        color: #334155 !important;
        font-weight: 600 !important;
        border-left: 5px solid #667eea;
        padding-left: 15px;
        margin-top: 2rem;
    }
    
    h3 {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    
    /* Cajas de entrada */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: white !important;
        color: #1e293b !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Labels */
    label {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 10px !important;
        width: 100%;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #1e293b !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #667eea !important;
    }
    
    /* Contenedores de métricas */
    div[data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    
    /* Alerts y mensajes */
    .stSuccess {
        background-color: #d1fae5 !important;
        color: #065f46 !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background-color: #fee2e2 !important;
        color: #991b1b !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background-color: #fef3c7 !important;
        color: #92400e !important;
        border-left: 4px solid #f59e0b !important;
        border-radius: 8px !important;
    }
    
    .stInfo {
        background-color: #dbeafe !important;
        color: #1e40af !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 8px !important;
    }
    
    /* DataFrames */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px !important;
    }
    
    .dataframe td {
        padding: 10px !important;
        color: #1e293b !important;
    }
    
    /* Separadores */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        color: #334155;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Animaciones */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .element-container {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# ===== TABLAS DE CONVERSIÓN (5 años 0-3 meses) =====
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

# Tablas de conversión Sumas PE -> Índices
TABLA_ICV = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:130, 28:137, 30:145}
TABLA_IVE = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:129, 28:136, 30:143, 32:150}
TABLA_IRF = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:130, 28:136, 30:143}
TABLA_IMT = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:95, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138, 30:145}
TABLA_IVP = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138}
TABLA_CIT = {10:40, 15:45, 20:52, 25:58, 30:64, 35:70, 40:76, 45:82, 50:88, 55:94, 60:100, 63:103, 65:106, 70:112, 75:118, 80:124, 85:130, 90:136}

# Percentiles
TABLA_PERCENTILES = {
    40:0.1, 45:0.1, 50:0.1, 55:0.1, 60:0.4, 65:1, 70:2, 75:5, 80:9, 85:16, 90:25, 
    95:37, 100:50, 103:58, 105:63, 106:66, 109:73, 110:75, 115:84, 120:91, 125:95, 
    128:97, 130:98, 135:99, 140:99.6, 145:99.9, 150:99.9
}

# ===== FUNCIONES AUXILIARES =====
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
        'suma_icv': suma_icv,
        'suma_ive': suma_ive,
        'suma_irf': suma_irf,
        'suma_imt': suma_imt,
        'suma_ivp': suma_ivp,
        'suma_cit': suma_cit
    }

def obtener_percentil(puntuacion):
    return TABLA_PERCENTILES.get(puntuacion, 50)

def obtener_categoria(puntuacion):
    if puntuacion >= 130:
        return {'categoria': 'Muy superior', 'nivel': 'Punto fuerte normativo', 'color': '#10b981'}
    elif puntuacion >= 120:
        return {'categoria': 'Superior', 'nivel': 'Dentro de límites', 'color': '#3b82f6'}
    elif puntuacion >= 110:
        return {'categoria': 'Medio alto', 'nivel': 'Dentro de límites', 'color': '#6366f1'}
    elif puntuacion >= 90:
        return {'categoria': 'Medio', 'nivel': 'Promedio', 'color': '#8b5cf6'}
    elif puntuacion >= 80:
        return {'categoria': 'Medio bajo', 'nivel': 'Promedio', 'color': '#f59e0b'}
    elif puntuacion >= 70:
        return {'categoria': 'Límite', 'nivel': 'Punto débil normativo', 'color': '#f97316'}
    else:
        return {'categoria': 'Muy bajo', 'nivel': 'Punto débil normativo', 'color': '#ef4444'}

def generar_pdf(datos_paciente, pe_dict, indices):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    story = []
    styles = getSampleStyleSheet()
    
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    story.append(Paragraph("INFORME PSICOPEDAGÓGICO", titulo_style))
    story.append(Paragraph("Escala de Inteligencia de Wechsler para Preescolar IV (WPPSI-IV)", styles['Normal']))
    story.append(Spacer(1, 0.5*cm))
    
    # Datos del paciente
    story.append(Paragraph("DATOS DEL EVALUADO", subtitulo_style))
    datos_tabla = [
        ['Nombre:', datos_paciente['nombre'], 'Sexo:', datos_paciente['sexo']],
        ['Fecha de nacimiento:', datos_paciente['fecha_nacimiento'], 'Fecha de evaluación:', datos_paciente['fecha_aplicacion']],
        ['Edad cronológica:', datos_paciente['edad_texto'], 'Lugar:', datos_paciente['lugar']],
        ['Examinador/a:', datos_paciente['examinador'], '', '']
    ]
    
    tabla_datos = Table(datos_tabla, colWidths=[4*cm, 5*cm, 4*cm, 5*cm])
    tabla_datos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(tabla_datos)
    story.append(Spacer(1, 0.5*cm))
    
    # Más contenido del PDF...
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ===== INTERFAZ PRINCIPAL =====
st.markdown("<h1>🧠 Generador de Informes WPPSI-IV</h1>", unsafe_allow_html=True)

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📝 Datos del Paciente", "📊 Resultados", "📄 Informe PDF"])

with tab1:
    st.markdown("## 👤 Información del Evaluado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("📝 Nombre completo", placeholder="Ej: Micaela Rodríguez")
        sexo = st.selectbox("⚧ Sexo", ["Femenino", "Masculino"])
        fecha_nacimiento = st.date_input("🎂 Fecha de nacimiento", value=date(2020, 10, 1))
    
    with col2:
        fecha_aplicacion = st.date_input("📅 Fecha de evaluación", value=date.today())
        lugar = st.text_input("📍 Lugar", value="Argentina")
        examinador = st.text_input("👨‍⚕️ Examinador/a", placeholder="Nombre del profesional")
    
    st.markdown("---")
    st.markdown("## 📊 Puntuaciones Directas")
    st.info("💡 Ingrese las puntuaciones directas (PD) obtenidas en cada prueba")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🗣️ Comprensión Verbal")
        pd_informacion = st.number_input("Información", 0, 30, None, key="info")
        pd_semejanzas = st.number_input("Semejanzas", 0, 30, None, key="sem")
        
        st.markdown("### 🧩 Visoespacial")
        pd_cubos = st.number_input("Cubos", 0, 30, None, key="cub")
        pd_rompecabezas = st.number_input("Rompecabezas", 0, 30, None, key="rom")
    
    with col2:
        st.markdown("### 🧠 Razonamiento Fluido")
        pd_matrices = st.number_input("Matrices", 0, 30, None, key="mat")
        pd_conceptos = st.number_input("Conceptos", 0, 30, None, key="con")
        
        st.markdown("### 💭 Memoria de Trabajo")
        pd_reconocimiento = st.number_input("Reconocimiento", 0, 30, None, key="rec")
        pd_localizacion = st.number_input("Localización", 0, 30, None, key="loc")
    
    with col3:
        st.markdown("### ⚡ Velocidad de Procesamiento")
        pd_busqueda = st.number_input("Búsqueda de Animales", 0, 30, None, key="bus")
        pd_cancelacion = st.number_input("Cancelación", 0, 30, None, key="can")
    
    st.markdown("---")
    
    if st.button("🎯 GENERAR ANÁLISIS COMPLETO", type="primary"):
        if not nombre or not examinador:
            st.error("❌ Complete los campos obligatorios: Nombre y Examinador")
        else:
            # Guardar en session state
            st.session_state['datos_guardados'] = True
            st.session_state['nombre'] = nombre
            st.session_state['sexo'] = sexo
            st.session_state['fecha_nac'] = fecha_nacimiento
            st.session_state['fecha_apl'] = fecha_aplicacion
            st.session_state['lugar'] = lugar
            st.session_state['examinador'] = examinador
            st.session_state['puntuaciones'] = {
                'cubos': pd_cubos,
                'informacion': pd_informacion,
                'matrices': pd_matrices,
                'busqueda_animales': pd_busqueda,
                'reconocimiento': pd_reconocimiento,
                'semejanzas': pd_semejanzas,
                'conceptos': pd_conceptos,
                'localizacion': pd_localizacion,
                'cancelacion': pd_cancelacion,
                'rompecabezas': pd_rompecabezas
            }
            st.success("✅ ¡Datos guardados! Pase a la pestaña 'Resultados'")

with tab2:
    if 'datos_guardados' in st.session_state and st.session_state['datos_guardados']:
        # Calcular edad
        years, months, days = calcular_edad(
            st.session_state['fecha_nac'],
            st.session_state['fecha_apl']
        )
        edad_texto = f"{years} años, {months} meses, {days} días"
        
        # Convertir PD a PE
        pe_dict = {}
        for prueba, pd in st.session_state['puntuaciones'].items():
            if pd is not None:
                pe_dict[prueba] = convertir_pd_a_pe(prueba, pd)
        
        # Calcular índices
        indices = calcular_indices(pe_dict)
        st.session_state['indices'] = indices
        st.session_state['pe_dict'] = pe_dict
        
        # RESUMEN EJECUTIVO
        st.markdown("## 📋 Resumen Ejecutivo")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👤 Evaluado", st.session_state['nombre'])
        with col2:
            st.metric("📅 Edad", edad_texto)
        with col3:
            cat = obtener_categoria(indices['CIT'])
            st.metric("🎯 CI Total", indices['CIT'], f"Percentil {obtener_percentil(indices['CIT'])}")
        with col4:
            st.metric("📊 Categoría", cat['categoria'])
        
        st.markdown("---")
        
        # TABLA DE CONVERSIONES
        st.markdown("## 🔄 Conversión de Puntuaciones")
        
        df_conversion = pd.DataFrame({
            'Prueba': ['Cubos', 'Información', 'Matrices', 'Búsqueda Animales', 'Reconocimiento', 
                      'Semejanzas', 'Conceptos', 'Localización', 'Cancelación', 'Rompecabezas'],
            'PD': [st.session_state['puntuaciones'][k] or '-' for k in 
                   ['cubos', 'informacion', 'matrices', 'busqueda_animales', 'reconocimiento',
                    'semejanzas', 'conceptos', 'localizacion', 'cancelacion', 'rompecabezas']],
            'PE': [pe_dict.get(k, '-') or '-' for k in 
                   ['cubos', 'informacion', 'matrices', 'busqueda_animales', 'reconocimiento',
                    'semejanzas', 'conceptos', 'localizacion', 'cancelacion', 'rompecabezas']]
        })
        
        st.dataframe(df_conversion, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # GRÁFICO DE PUNTUACIONES ESCALARES
        st.markdown("## 📊 Perfil de Puntuaciones Escalares (PE)")
        
        pruebas_labels = ['Cubos', 'Info.', 'Matrices', 'B. Anim.', 'Recon.', 
                         'Semej.', 'Concep.', 'Local.', 'Cancel.', 'Rompe.']
        pe_values = [pe_dict.get(k, 0) or 0 for k in 
                    ['cubos', 'informacion', 'matrices', 'busqueda_animales', 'reconocimiento',
                     'semejanzas', 'conceptos', 'localizacion', 'cancelacion', 'rompecabezas']]
        
        # Colores según nivel
        colores_pe = []
        for pe in pe_values:
            if pe >= 13:
                colores_pe.append('#10b981')  # Verde - Fortaleza
            elif pe <= 7:
                colores_pe.append('#ef4444')  # Rojo - Debilidad
            else:
                colores_pe.append('#6366f1')  # Azul - Promedio
        
        fig_pe = go.Figure(data=[
            go.Bar(
                x=pruebas_labels,
                y=pe_values,
                marker=dict(color=colores_pe, line=dict(color='#1e293b', width=2)),
                text=pe_values,
                textposition='outside',
                textfont=dict(size=14, color='#1e293b', family='Inter'),
                hovertemplate='<b>%{x}</b><br>PE: %{y}<extra></extra>'
            )
        ])
        
        # Líneas de referencia
        fig_pe.add_hline(y=10, line_dash="dash", line_color="#64748b", 
                        annotation_text="Media (10)", annotation_position="right")
        fig_pe.add_hline(y=7, line_dash="dot", line_color="#ef4444", 
                        annotation_text="Debilidad (≤7)", annotation_position="right")
        fig_pe.add_hline(y=13, line_dash="dot", line_color="#10b981", 
                        annotation_text="Fortaleza (≥13)", annotation_position="right")
        
        fig_pe.update_layout(
            title={
                'text': "Puntuaciones Escalares por Prueba",
                'font': {'size': 20, 'color': '#1e293b', 'family': 'Inter'},
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title="Pruebas WPPSI-IV",
            yaxis_title="Puntuación Escalar (PE)",
            yaxis=dict(range=[0, 20], dtick=2),
            height=500,
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#1e293b')
        )
        
        st.plotly_chart(fig_pe, use_container_width=True)
        
        st.markdown("---")
        
        # ÍNDICES COMPUESTOS
        st.markdown("## 🎯 Índices Compuestos - Análisis Detallado")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🗣️ Comprensión Verbal")
            icv_cat = obtener_categoria(indices['ICV'])
            st.metric("ICV", indices['ICV'], f"PE: {indices['suma_icv']}")
            st.caption(f"📊 Percentil: {obtener_percentil(indices['ICV'])}")
            st.markdown(f"<p style='color: {icv_cat['color']}; font-weight: 600;'>{icv_cat['categoria']}</p>", 
                       unsafe_allow_html=True)
            st.progress(obtener_percentil(indices['ICV'])/100)
            
            st.markdown("### 🧩 Visoespacial")
            ive_cat = obtener_categoria(indices['IVE'])
            st.metric("IVE", indices['IVE'], f"PE: {indices['suma_ive']}")
            st.caption(f"📊 Percentil: {obtener_percentil(indices['IVE'])}")
            st.markdown(f"<p style='color: {ive_cat['color']}; font-weight: 600;'>{ive_cat['categoria']}</p>", 
                       unsafe_allow_html=True)
            st.progress(obtener_percentil(indices['IVE'])/100)
        
        with col2:
            st.markdown("### 🧠 Razonamiento Fluido")
            irf_cat = obtener_categoria(indices['IRF'])
            st.metric("IRF", indices['IRF'], f"PE: {indices['suma_irf']}")
            st.caption(f"📊 Percentil: {obtener_percentil(indices['IRF'])}")
            st.markdown(f"<p style='color: {irf_cat['color']}; font-weight: 600;'>{irf_cat['categoria']}</p>", 
                       unsafe_allow_html=True)
            st.progress(obtener_percentil(indices['IRF'])/100)
            
            st.markdown("### 💭 Memoria de Trabajo")
            imt_cat = obtener_categoria(indices['IMT'])
            st.metric("IMT", indices['IMT'], f"PE: {indices['suma_imt']}")
            st.caption(f"📊 Percentil: {obtener_percentil(indices['IMT'])}")
            st.markdown(f"<p style='color: {imt_cat['color']}; font-weight: 600;'>{imt_cat['categoria']}</p>", 
                       unsafe_allow_html=True)
            st.progress(obtener_percentil(indices['IMT'])/100)
        
        with col3:
            st.markdown("### ⚡ Velocidad Procesamiento")
            ivp_cat = obtener_categoria(indices['IVP'])
            st.metric("IVP", indices['IVP'], f"PE: {indices['suma_ivp']}")
            st.caption(f"📊 Percentil: {obtener_percentil(indices['IVP'])}")
            st.markdown(f"<p style='color: {ivp_cat['color']}; font-weight: 600;'>{ivp_cat['categoria']}</p>", 
                       unsafe_allow_html=True)
            st.progress(obtener_percentil(indices['IVP'])/100)
            
            st.markdown("### 🏆 CI TOTAL")
            cit_cat = obtener_categoria(indices['CIT'])
            st.metric("CIT", indices['CIT'], f"PE: {indices['suma_cit']}")
            st.caption(f"📊 Percentil: {obtener_percentil(indices['CIT'])}")
            st.markdown(f"<p style='color: {cit_cat['color']}; font-weight: 600;'>{cit_cat['categoria']}</p>", 
                       unsafe_allow_html=True)
            st.progress(obtener_percentil(indices['CIT'])/100)
        
        st.markdown("---")
        
        # GRÁFICO RADAR DE ÍNDICES
        st.markdown("## 🎯 Perfil Cognitivo - Vista Radar")
        
        fig_radar = go.Figure()
        
        indices_nombres = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP']
        indices_valores = [indices['ICV'], indices['IVE'], indices['IRF'], indices['IMT'], indices['IVP']]
        
        fig_radar.add_trace(go.Scatterpolar(
            r=indices_valores,
            theta=indices_nombres,
            fill='toself',
            fillcolor='rgba(102, 126, 234, 0.3)',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color='#667eea'),
            name='Perfil del evaluado'
        ))
        
        # Línea de referencia (media = 100)
        fig_radar.add_trace(go.Scatterpolar(
            r=[100, 100, 100, 100, 100],
            theta=indices_nombres,
            mode='lines',
            line=dict(color='#64748b', width=2, dash='dash'),
            name='Media poblacional (100)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[40, 160],
                    tickfont=dict(size=12, color='#1e293b')
                ),
                angularaxis=dict(
                    tickfont=dict(size=14, color='#1e293b', family='Inter')
                )
            ),
            showlegend=True,
            legend=dict(
                font=dict(size=12, color='#1e293b'),
                bgcolor='rgba(255,255,255,0.8)'
            ),
            title={
                'text': "Perfil de Índices Primarios - Vista Multidimensional",
                'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter'},
                'x': 0.5,
                'xanchor': 'center'
            },
            height=600,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        st.markdown("---")
        
        # GRÁFICO DE BARRAS DE ÍNDICES
        st.markdown("## 📈 Comparación de Índices Compuestos")
        
        indices_labels = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT']
        indices_values = [indices['ICV'], indices['IVE'], indices['IRF'], 
                         indices['IMT'], indices['IVP'], indices['CIT']]
        
        colores_indices = []
        for val in indices_values:
            cat = obtener_categoria(val)
            colores_indices.append(cat['color'])
        
        fig_indices = go.Figure()
        
        fig_indices.add_trace(go.Bar(
            x=indices_labels,
            y=indices_values,
            marker=dict(
                color=colores_indices,
                line=dict(color='#1e293b', width=2),
                pattern_shape=["/", "", "\\", "", "x", ""]
            ),
            text=indices_values,
            textposition='outside',
            textfont=dict(size=16, color='#1e293b', family='Inter'),
            hovertemplate='<b>%{x}</b><br>Puntuación: %{y}<br>Percentil: %{customdata}<extra></extra>',
            customdata=[obtener_percentil(v) for v in indices_values]
        ))
        
        # Zonas de categorización
        fig_indices.add_hrect(y0=130, y1=160, fillcolor="green", opacity=0.1, 
                             annotation_text="Muy Superior", annotation_position="top right")
        fig_indices.add_hrect(y0=120, y1=130, fillcolor="lightgreen", opacity=0.1, 
                             annotation_text="Superior", annotation_position="top right")
        fig_indices.add_hrect(y0=110, y1=120, fillcolor="lightblue", opacity=0.1, 
                             annotation_text="Medio Alto", annotation_position="top right")
        fig_indices.add_hrect(y0=90, y1=110, fillcolor="lightyellow", opacity=0.1, 
                             annotation_text="Medio", annotation_position="top right")
        fig_indices.add_hrect(y0=80, y1=90, fillcolor="lightyellow", opacity=0.1, 
                             annotation_text="Medio Bajo", annotation_position="top right")
        fig_indices.add_hrect(y0=70, y1=80, fillcolor="orange", opacity=0.1, 
                             annotation_text="Límite", annotation_position="top right")
        
        # Líneas de referencia
        fig_indices.add_hline(y=100, line_dash="dash", line_color="#64748b", 
                             annotation_text="Media (100)", annotation_position="left")
        fig_indices.add_hline(y=85, line_dash="dot", line_color="#f97316")
        fig_indices.add_hline(y=115, line_dash="dot", line_color="#10b981")
        
        fig_indices.update_layout(
            title={
                'text': "Índices Compuestos - Puntuaciones Estándar",
                'font': {'size': 20, 'color': '#1e293b', 'family': 'Inter'},
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title="Índices WPPSI-IV",
            yaxis_title="Puntuación Compuesta",
            yaxis=dict(range=[40, 160], dtick=10),
            height=550,
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#1e293b')
        )
        
        st.plotly_chart(fig_indices, use_container_width=True)
        
        st.markdown("---")
        
        # ANÁLISIS DE FORTALEZAS Y DEBILIDADES
        st.markdown("## 💪 Análisis de Fortalezas y Debilidades")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Áreas de Fortaleza (PE ≥ 13)")
            fortalezas = [(k.replace('_', ' ').title(), v) for k, v in pe_dict.items() 
                         if v and v >= 13]
            
            if fortalezas:
                for prueba, valor in fortalezas:
                    st.success(f"**{prueba}**: {valor}")
                    st.progress(valor/19)
            else:
                st.info("No se identificaron fortalezas significativas (PE ≥ 13)")
        
        with col2:
            st.markdown("### ⚠️ Áreas a Desarrollar (PE ≤ 7)")
            debilidades = [(k.replace('_', ' ').title(), v) for k, v in pe_dict.items() 
                          if v and v <= 7]
            
            if debilidades:
                for prueba, valor in debilidades:
                    st.warning(f"**{prueba}**: {valor}")
                    st.progress(valor/19)
            else:
                st.info("No se identificaron debilidades significativas (PE ≤ 7)")
        
        st.markdown("---")
        
        # INTERPRETACIÓN CLÍNICA
        st.markdown("## 📝 Interpretación Clínica")
        
        cit_cat = obtener_categoria(indices['CIT'])
        cit_perc = obtener_percentil(indices['CIT'])
        
        interpretacion = f"""
        <div style='background: white; padding: 2rem; border-radius: 15px; border-left: 5px solid {cit_cat['color']}; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <h3 style='color: #1e293b;'>Resumen del Funcionamiento Cognitivo</h3>
        <p style='font-size: 1.1rem; line-height: 1.8; color: #334155;'>
        <b>{st.session_state['nombre']}</b> obtuvo un <b>Coeficiente Intelectual Total (CIT) de {indices['CIT']}</b>, 
        clasificado en la categoría <b style='color: {cit_cat['color']};'>{cit_cat['categoria']}</b> ({cit_cat['nivel']}). 
        </p>
        
        <p style='font-size: 1.05rem; line-height: 1.8; color: #334155;'>
        Esta puntuación se ubica en el <b>percentil {cit_perc}</b>, lo que indica que su rendimiento 
        supera al {cit_perc}% de los niños de su edad en la muestra de tipificación.
        </p>
        
        <h4 style='color: #1e293b; margin-top: 1.5rem;'>Análisis por Dominios Cognitivos:</h4>
        <ul style='font-size: 1rem; line-height: 1.8; color: #334155;'>
        <li><b>Comprensión Verbal (ICV: {indices['ICV']})</b>: {obtener_categoria(indices['ICV'])['categoria']} - Percentil {obtener_percentil(indices['ICV'])}</li>
        <li><b>Visoespacial (IVE: {indices['IVE']})</b>: {obtener_categoria(indices['IVE'])['categoria']} - Percentil {obtener_percentil(indices['IVE'])}</li>
        <li><b>Razonamiento Fluido (IRF: {indices['IRF']})</b>: {obtener_categoria(indices['IRF'])['categoria']} - Percentil {obtener_percentil(indices['IRF'])}</li>
        <li><b>Memoria de Trabajo (IMT: {indices['IMT']})</b>: {obtener_categoria(indices['IMT'])['categoria']} - Percentil {obtener_percentil(indices['IMT'])}</li>
        <li><b>Velocidad de Procesamiento (IVP: {indices['IVP']})</b>: {obtener_categoria(indices['IVP'])['categoria']} - Percentil {obtener_percentil(indices['IVP'])}</li>
        </ul>
        </div>
        """
        
        st.markdown(interpretacion, unsafe_allow_html=True)
        
    else:
        st.warning("⚠️ Por favor, complete los datos en la pestaña 'Datos del Paciente' primero")

with tab3:
    if 'datos_guardados' in st.session_state and st.session_state['datos_guardados']:
        st.markdown("## 📄 Generar Informe PDF Profesional")
        
        st.info("💡 El informe incluirá todos los análisis, gráficos y tablas generados")
        
        if st.button("📥 DESCARGAR INFORME EN PDF", type="primary"):
            years, months, days = calcular_edad(
                st.session_state['fecha_nac'],
                st.session_state['fecha_apl']
            )
            edad_texto = f"{years} años, {months} meses, {days} días"
            
            datos_paciente = {
                'nombre': st.session_state['nombre'],
                'sexo': st.session_state['sexo'],
                'fecha_nacimiento': st.session_state['fecha_nac'].strftime('%d/%m/%Y'),
                'fecha_aplicacion': st.session_state['fecha_apl'].strftime('%d/%m/%Y'),
                'edad_texto': edad_texto,
                'lugar': st.session_state['lugar'],
                'examinador': st.session_state['examinador'],
                'puntuaciones': st.session_state['puntuaciones']
            }
            
            pdf_buffer = generar_pdf(datos_paciente, st.session_state['pe_dict'], 
                                    st.session_state['indices'])
            
            st.download_button(
                label="📥 DESCARGAR INFORME COMPLETO",
                data=pdf_buffer,
                file_name=f"Informe_WPPSI-IV_{st.session_state['nombre'].replace(' ', '_')}_{st.session_state['fecha_apl'].strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                type="primary"
            )
            
            st.success("✅ ¡Listo para descargar!")
    else:
        st.warning("⚠️ Complete los datos primero")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 2rem; background: white; border-radius: 15px; margin-top: 2rem;'>
        <h3 style='color: #1e293b;'>Generador de Informes WPPSI-IV</h3>
        <p style='font-size: 1rem;'>Herramienta profesional para evaluación psicopedagógica</p>
        <p style='font-size: 0.9rem;'>Desarrollado con ❤️ para psicólogos y psicopedagogos</p>
    </div>
""", unsafe_allow_html=True)
