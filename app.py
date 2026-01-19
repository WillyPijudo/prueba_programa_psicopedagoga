import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas
import io
import base64

# Configuración de la página
st.set_page_config(
    page_title="Generador de Informes WPPSI-IV",
    page_icon="📊",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(to bottom right, #e0e7ff, #e0f2fe);
    }
    h1 {
        color: #4f46e5;
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 30px;
        border-radius: 8px;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1>📊 Generador de Informes WPPSI-IV</h1>", unsafe_allow_html=True)
st.markdown("---")

# Tablas de conversión PD -> PE (basadas en edad 5 años 0-3 meses)
TABLAS_CONVERSION = {
    'cubos': {0:1, 1:1, 2:1, 3:1, 4:1, 5:2, 6:3, 7:4, 8:5, 9:6, 10:7, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:16, 19:17, 20:17, 21:18, 22:18, 23:19, 24:19, 25:19, 26:19, 27:19, 28:19, 29:19, 30:19},
    'informacion': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:15, 17:16, 18:17, 19:18, 20:18, 21:19, 22:19, 23:19, 24:19, 25:19, 26:19},
    'matrices': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:9, 10:10, 11:11, 12:12, 13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19},
    'busqueda_animales': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:17, 20:18, 21:19},
    'reconocimiento': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:8, 9:10, 10:11, 11:13, 12:14, 13:16, 14:17, 15:18, 16:19},
    'semejanzas': {0:1, 1:1, 2:1, 3:1, 4:2, 5:3, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:14, 17:15, 18:16, 19:16, 20:17, 21:17, 22:18, 23:18, 24:19, 25:19, 26:19, 27:19, 28:19, 29:19},
    'conceptos': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:17, 18:18, 19:19},
    'dibujos': {0:1, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12, 13:13, 14:14, 15:15, 16:16, 17:17, 18:18, 19:19},
    'localizacion': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:7, 8:8, 9:9, 10:11, 11:12, 12:13, 13:14, 14:15, 15:16, 16:17, 17:18, 18:19, 19:19, 20:19},
    'cancelacion': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19, 21:19},
    'rompecabezas': {0:1, 1:1, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 12:11, 13:12, 14:13, 15:14, 16:15, 17:16, 18:17, 19:18, 20:19}
}

# Tablas de conversión Sumas PE -> Índices Compuestos
TABLA_ICV = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:130, 28:137, 30:145}
TABLA_IVE = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:129, 28:136, 30:143, 32:150}
TABLA_IRF = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:109, 22:116, 24:123, 26:130, 28:136, 30:143}
TABLA_IMT = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:95, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138, 30:145}
TABLA_IVP = {2:50, 4:55, 6:62, 8:69, 10:76, 12:83, 14:90, 16:97, 18:103, 20:110, 22:117, 24:124, 26:131, 28:138}
TABLA_CIT = {10:40, 15:45, 20:52, 25:58, 30:64, 35:70, 40:76, 45:82, 50:88, 55:94, 60:100, 63:103, 65:106, 70:112, 75:118, 80:124, 85:130, 90:136}

# Tabla de percentiles
TABLA_PERCENTILES = {
    40: 0.1, 45: 0.1, 50: 0.1, 55: 0.1, 60: 0.4, 65: 1, 70: 2, 75: 5,
    80: 9, 85: 16, 90: 25, 95: 37, 100: 50, 103: 58, 105: 63, 106: 66,
    109: 73, 110: 75, 115: 84, 120: 91, 125: 95, 128: 97, 130: 98,
    135: 99, 140: 99.6, 145: 99.9, 150: 99.9
}

def calcular_edad(fecha_nac, fecha_apl):
    """Calcula la edad cronológica"""
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
    """Convierte puntuación directa a escalar"""
    if pd is None or pd == '':
        return None
    return TABLAS_CONVERSION.get(prueba, {}).get(int(pd), None)

def buscar_en_tabla(tabla, suma):
    """Busca en tabla de conversión"""
    keys = sorted(tabla.keys())
    for key in keys:
        if suma <= key:
            return tabla[key]
    return tabla[keys[-1]]

def calcular_indices(pe_dict):
    """Calcula los índices compuestos"""
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
    """Obtiene el percentil de una puntuación compuesta"""
    return TABLA_PERCENTILES.get(puntuacion, 50)

def obtener_categoria(puntuacion):
    """Determina la categoría descriptiva"""
    if puntuacion >= 130:
        return {'categoria': 'Muy superior', 'nivel': 'Punto fuerte normativo'}
    elif puntuacion >= 120:
        return {'categoria': 'Superior', 'nivel': 'Dentro de límites'}
    elif puntuacion >= 110:
        return {'categoria': 'Medio alto', 'nivel': 'Dentro de límites'}
    elif puntuacion >= 90:
        return {'categoria': 'Medio', 'nivel': 'Promedio'}
    elif puntuacion >= 80:
        return {'categoria': 'Medio bajo', 'nivel': 'Promedio'}
    elif puntuacion >= 70:
        return {'categoria': 'Límite', 'nivel': 'Punto débil normativo'}
    else:
        return {'categoria': 'Muy bajo', 'nivel': 'Punto débil normativo'}

def generar_pdf(datos_paciente, pe_dict, indices):
    """Genera el PDF del informe completo"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#4f46e5'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Título del informe
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
    
    # Conversión de puntuaciones
    story.append(Paragraph("CONVERSIÓN DE PUNTUACIONES DIRECTAS A ESCALARES", subtitulo_style))
    
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
    
    conversion_data = [['Prueba', 'PD', 'PE']]
    for key, nombre in pruebas_nombres.items():
        pd = datos_paciente['puntuaciones'].get(key, '-')
        pe = pe_dict.get(key, '-')
        conversion_data.append([nombre, str(pd) if pd else '-', str(pe) if pe else '-'])
    
    tabla_conversion = Table(conversion_data, colWidths=[8*cm, 4*cm, 4*cm])
    tabla_conversion.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
    ]))
    story.append(tabla_conversion)
    story.append(Spacer(1, 0.5*cm))
    
    # Puntuaciones compuestas
    story.append(Paragraph("PUNTUACIONES COMPUESTAS E ÍNDICES PRIMARIOS", subtitulo_style))
    
    indices_data = [['Índice', 'Suma PE', 'Puntuación', 'Percentil', 'Categoría']]
    indices_lista = [
        ('Comprensión Verbal (ICV)', indices['suma_icv'], indices['ICV']),
        ('Visoespacial (IVE)', indices['suma_ive'], indices['IVE']),
        ('Razonamiento Fluido (IRF)', indices['suma_irf'], indices['IRF']),
        ('Memoria de Trabajo (IMT)', indices['suma_imt'], indices['IMT']),
        ('Velocidad de Procesamiento (IVP)', indices['suma_ivp'], indices['IVP']),
        ('CI TOTAL (CIT)', indices['suma_cit'], indices['CIT'])
    ]
    
    for nombre, suma, valor in indices_lista:
        percentil = obtener_percentil(valor)
        categoria = obtener_categoria(valor)['categoria']
        indices_data.append([nombre, str(suma), str(valor), str(percentil), categoria])
    
    tabla_indices = Table(indices_data, colWidths=[6*cm, 2*cm, 3*cm, 2.5*cm, 3.5*cm])
    tabla_indices.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ddd6fe')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    story.append(tabla_indices)
    story.append(Spacer(1, 0.5*cm))
    
    # Interpretación
    story.append(PageBreak())
    story.append(Paragraph("INTERPRETACIÓN CLÍNICA", titulo_style))
    story.append(Spacer(1, 0.3*cm))
    
    cit_cat = obtener_categoria(indices['CIT'])
    cit_percentil = obtener_percentil(indices['CIT'])
    
    interpretacion_texto = f"""
    <b>{datos_paciente['nombre']}</b> obtuvo un Coeficiente Intelectual Total (CIT) de <b>{indices['CIT']}</b>, 
    lo cual se clasifica en la categoría <b>{cit_cat['categoria']}</b>. Esta puntuación se ubica en el 
    percentil <b>{cit_percentil}</b>, indicando que su rendimiento supera al {cit_percentil}% de los niños 
    de su edad en la muestra de tipificación.<br/><br/>
    
    El CIT representa una medida global de la capacidad intelectual del niño, evaluada a través de cinco 
    índices primarios que miden diferentes aspectos del funcionamiento cognitivo.
    """
    
    story.append(Paragraph(interpretacion_texto, styles['Normal']))
    story.append(Spacer(1, 0.5*cm))
    
    # Análisis por índices
    story.append(Paragraph("ANÁLISIS DE ÍNDICES PRIMARIOS", subtitulo_style))
    
    for nombre_completo, nombre_corto in [
        ('Comprensión Verbal', 'ICV'),
        ('Visoespacial', 'IVE'),
        ('Razonamiento Fluido', 'IRF'),
        ('Memoria de Trabajo', 'IMT'),
        ('Velocidad de Procesamiento', 'IVP')
    ]:
        valor = indices[nombre_corto]
        cat = obtener_categoria(valor)
        perc = obtener_percentil(valor)
        
        texto_indice = f"""
        <b>{nombre_completo} ({nombre_corto}): {valor}</b><br/>
        Categoría: {cat['categoria']} | Percentil: {perc}<br/>
        {cat['nivel']}<br/><br/>
        """
        story.append(Paragraph(texto_indice, styles['Normal']))
    
    # Fortalezas y debilidades
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("ANÁLISIS DE FORTALEZAS Y DEBILIDADES", subtitulo_style))
    
    fortalezas = [f"{k.replace('_', ' ').title()}: {v}" for k, v in pe_dict.items() if v and v >= 13]
    debilidades = [f"{k.replace('_', ' ').title()}: {v}" for k, v in pe_dict.items() if v and v <= 7]
    
    if fortalezas:
        story.append(Paragraph("<b>Áreas de Fortaleza (PE ≥ 13):</b>", styles['Normal']))
        for fort in fortalezas:
            story.append(Paragraph(f"• {fort}", styles['Normal']))
        story.append(Spacer(1, 0.3*cm))
    
    if debilidades:
        story.append(Paragraph("<b>Áreas a Desarrollar (PE ≤ 7):</b>", styles['Normal']))
        for deb in debilidades:
            story.append(Paragraph(f"• {deb}", styles['Normal']))
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# INTERFAZ DE USUARIO
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 👤 Datos del Paciente")

# Datos básicos
col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("📝 Nombre del niño/a", placeholder="Ej: Micaela")
    sexo = st.selectbox("⚧ Sexo", ["F", "M"])
    fecha_nacimiento = st.date_input("🎂 Fecha de nacimiento", value=date(2020, 10, 1))

with col2:
    fecha_aplicacion = st.date_input("📅 Fecha de aplicación", value=date.today())
    lugar = st.text_input("📍 Lugar de aplicación", value="Argentina")
    examinador = st.text_input("👨‍⚕️ Examinador/a", placeholder="Nombre del profesional")

st.markdown("---")
st.markdown("### 📊 Puntuaciones Directas (PD)")
st.info("💡 Ingresa las puntuaciones directas obtenidas en cada prueba (0-30)")

# Organizar pruebas por índice
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🗣️ Comprensión Verbal**")
    pd_informacion = st.number_input("Información", min_value=0, max_value=30, value=None, key="info")
    pd_semejanzas = st.number_input("Semejanzas", min_value=0, max_value=30, value=None, key="sem")
    
    st.markdown("**🧩 Visoespacial**")
    pd_cubos = st.number_input("Cubos", min_value=0, max_value=30, value=None, key="cub")
    pd_rompecabezas = st.number_input("Rompecabezas", min_value=0, max_value=30, value=None, key="rom")

with col2:
    st.markdown("**🧠 Razonamiento Fluido**")
    pd_matrices = st.number_input("Matrices", min_value=0, max_value=30, value=None, key="mat")
    pd_conceptos = st.number_input("Conceptos", min_value=0, max_value=30, value=None, key="con")
    
    st.markdown("**💭 Memoria de Trabajo**")
    pd_reconocimiento = st.number_input("Reconocimiento", min_value=0, max_value=30, value=None, key="rec")
    pd_localizacion = st.number_input("Localización", min_value=0, max_value=30, value=None, key="loc")

with col3:
    st.markdown("**⚡ Velocidad de Procesamiento**")
    pd_busqueda = st.number_input("Búsqueda de Animales", min_value=0, max_value=30, value=None, key="bus")
    pd_cancelacion = st.number_input("Cancelación", min_value=0, max_value=30, value=None, key="can")
    
    st.markdown("**📝 Pruebas Adicionales (Opcional)**")
    pd_dibujos = st.number_input("Dibujos", min_value=0, max_value=30, value=None, key="dib")

st.markdown("---")

# Botón para generar informe
if st.button("🎯 GENERAR INFORME COMPLETO", type="primary"):
    if not nombre:
        st.error("❌ Por favor ingresa el nombre del niño/a")
    elif not examinador:
        st.error("❌ Por favor ingresa el nombre del examinador/a")
    else:
        # Calcular edad
        years, months, days = calcular_edad(fecha_nacimiento, fecha_aplicacion)
        edad_texto = f"{years} años, {months} meses, {days} días"
        
        # Recopilar puntuaciones
        puntuaciones = {
            'cubos': pd_cubos,
            'informacion': pd_informacion,
            'matrices': pd_matrices,
            'busqueda_animales': pd_busqueda,
            'reconocimiento': pd_reconocimiento,
            'semejanzas': pd_semejanzas,
            'conceptos': pd_conceptos,
            'localizacion': pd_localizacion,
            'cancelacion': pd_cancelacion,
            'rompecabezas': pd_rompecabezas,
            'dibujos': pd_dibujos
        }
        
        # Convertir PD a PE
        pe_dict = {}
        for prueba, pd in puntuaciones.items():
            if pd is not None:
                pe_dict[prueba] = convertir_pd_a_pe(prueba, pd)
        
        # Calcular índices
        indices = calcular_indices(pe_dict)
        
        # Mostrar resultados
        st.success("✅ ¡Informe generado exitosamente!")
        st.markdown("---")
        
        # Resumen ejecutivo
        st.markdown("## 📋 RESUMEN EJECUTIVO")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Edad Cronológica", edad_texto)
        with col2:
            st.metric("CI Total (CIT)", indices['CIT'], 
                     delta=f"Percentil {obtener_percentil(indices['CIT'])}")
        with col3:
            cat = obtener_categoria(indices['CIT'])
            st.metric("Categoría", cat['categoria'])
        
        st.markdown("---")
        
        # Tabla de conversión
        st.markdown("### 🔄 Conversión de Puntuaciones")
        
        tabla_conversion = pd.DataFrame({
            'Prueba': ['Cubos', 'Información', 'Matrices', 'Búsqueda Animales', 
                      'Reconocimiento', 'Semejanzas', 'Conceptos', 'Localización',
                      'Cancelación', 'Rompecabezas'],
            'PD': [puntuaciones.get(k, '-') for k in ['cubos', 'informacion', 'matrices', 
                   'busqueda_animales', 'reconocimiento', 'semejanzas', 'conceptos',
                   'localizacion', 'cancelacion', 'rompecabezas']],
            'PE': [pe_dict.get(k, '-') for k in ['cubos', 'informacion', 'matrices',
                   'busqueda_animales', 'reconocimiento', 'semejanzas', 'conceptos',
                   'localizacion', 'cancelacion', 'rompecabezas']]
        })
        
        st.dataframe(tabla_conversion, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Gráfico de puntuaciones escalares
        st.markdown("### 📊 Perfil de Puntuaciones Escalares")
        
        pruebas_labels = ['Cubos', 'Info', 'Matrices', 'B.A.', 'Recon.', 
                         'Semej.', 'Concep.', 'Local.', 'Cancel.', 'Rompe.']
        pe_values = [pe_dict.get(k, 0) for k in ['cubos', 'informacion', 'matrices',
                     'busqueda_animales', 'reconocimiento', 'semejanzas', 'conceptos',
                     'localizacion', 'cancelacion', 'rompecabezas']]
        
        fig_pe = go.Figure(data=[
            go.Bar(
                x=pruebas_labels,
                y=pe_values,
                marker=dict(
                    color=pe_values,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="PE")
                ),
                text=pe_values,
                textposition='outside'
            )
        ])
        
        fig_pe.update_layout(
            title="Puntuaciones Escalares por Prueba",
            xaxis_title="Pruebas",
            yaxis_title="Puntuación Escalar (PE)",
            yaxis=dict(range=[0, 20]),
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_pe, use_container_width=True)
        
        st.markdown("---")
        
        # Índices compuestos
        st.markdown("### 🎯 Índices Compuestos")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🗣️ Comprensión Verbal**")
            st.metric("ICV", indices['ICV'], delta=f"PE: {indices['suma_icv']}")
            st.caption(f"Percentil: {obtener_percentil(indices['ICV'])}")
            st.caption(obtener_categoria(indices['ICV'])['categoria'])
            
            st.markdown("**🧩 Visoespacial**")
            st.metric("IVE", indices['IVE'], delta=f"PE: {indices['suma_ive']}")
            st.caption(f"Percentil: {obtener_percentil(indices['IVE'])}")
            st.caption(obtener_categoria(indices['IVE'])['categoria'])
        
        with col2:
            st.markdown("**🧠 Razonamiento Fluido**")
            st.metric("IRF", indices['IRF'], delta=f"PE: {indices['suma_irf']}")
            st.caption(f"Percentil: {obtener_percentil(indices['IRF'])}")
            st.caption(obtener_categoria(indices['IRF'])['categoria'])
            
            st.markdown("**💭 Memoria de Trabajo**")
            st.metric("IMT", indices['IMT'], delta=f"PE: {indices['suma_imt']}")
            st.caption(f"Percentil: {obtener_percentil(indices['IMT'])}")
            st.caption(obtener_categoria(indices['IMT'])['categoria'])
        
        with col3:
            st.markdown("**⚡ Velocidad Procesamiento**")
            st.metric("IVP", indices['IVP'], delta=f"PE: {indices['suma_ivp']}")
            st.caption(f"Percentil: {obtener_percentil(indices['IVP'])}")
            st.caption(obtener_categoria(indices['IVP'])['categoria'])
            
            st.markdown("**🏆 CI TOTAL**")
            st.metric("CIT", indices['CIT'], delta=f"PE: {indices['suma_cit']}")
            st.caption(f"Percentil: {obtener_percentil(indices['CIT'])}")
            st.caption(obtener_categoria(indices['CIT'])['categoria'])
        
        st.markdown("---")
        
        # Gráfico de índices compuestos
        st.markdown("### 📈 Perfil de Índices Primarios")
        
        indices_labels = ['ICV', 'IVE', 'IRF', 'IMT', 'IVP', 'CIT']
        indices_values = [indices['ICV'], indices['IVE'], indices['IRF'], 
                         indices['IMT'], indices['IVP'], indices['CIT']]
        
        # Asignar colores según rango
        colores = []
        for val in indices_values:
            if val >= 115:
                colores.append('green')
            elif val >= 85:
                colores.append('blue')
            else:
                colores.append('orange')
        
        fig_indices = go.Figure(data=[
            go.Bar(
                x=indices_labels,
                y=indices_values,
                marker=dict(color=colores),
                text=indices_values,
                textposition='outside'
            )
        ])
        
        fig_indices.add_hline(y=100, line_dash="dash", line_color="gray", 
                             annotation_text="Media (100)")
        fig_indices.add_hline(y=85, line_dash="dot", line_color="orange", 
                             annotation_text="Límite inferior")
        fig_indices.add_hline(y=115, line_dash="dot", line_color="green", 
                             annotation_text="Límite superior")
        
        fig_indices.update_layout(
            title="Índices Compuestos",
            xaxis_title="Índices",
            yaxis_title="Puntuación Compuesta",
            yaxis=dict(range=[40, 160]),
            height=450,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_indices, use_container_width=True)
        
        st.markdown("---")
        
        # Fortalezas y debilidades
        st.markdown("### 💪 Análisis de Fortalezas y Debilidades")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Áreas Fuertes (PE ≥ 13)")
            fortalezas = [(k.replace('_', ' ').title(), v) for k, v in pe_dict.items() if v and v >= 13]
            if fortalezas:
                for prueba, valor in fortalezas:
                    st.success(f"**{prueba}**: {valor}")
            else:
                st.info("No se identificaron fortalezas significativas")
        
        with col2:
            st.markdown("#### ⚠️ Áreas a Desarrollar (PE ≤ 7)")
            debilidades = [(k.replace('_', ' ').title(), v) for k, v in pe_dict.items() if v and v <= 7]
            if debilidades:
                for prueba, valor in debilidades:
                    st.warning(f"**{prueba}**: {valor}")
            else:
                st.info("No se identificaron debilidades significativas")
        
        st.markdown("---")
        
        # Interpretación clínica
        st.markdown("### 📝 Interpretación Clínica")
        
        cit_cat = obtener_categoria(indices['CIT'])
        cit_perc = obtener_percentil(indices['CIT'])
        
        interpretacion = f"""
        **{nombre}** obtuvo un **Coeficiente Intelectual Total (CIT) de {indices['CIT']}**, 
        clasificado en la categoría **{cit_cat['categoria']}** ({cit_cat['nivel']}). 
        
        Esta puntuación se ubica en el **percentil {cit_perc}**, lo que indica que su rendimiento 
        supera al {cit_perc}% de los niños de su edad en la muestra de tipificación.
        
        El CIT representa una medida global de la capacidad intelectual, evaluada a través de 
        cinco índices primarios que miden diferentes aspectos del funcionamiento cognitivo:
        
        - **Comprensión Verbal (ICV: {indices['ICV']})**: {obtener_categoria(indices['ICV'])['categoria']}
        - **Visoespacial (IVE: {indices['IVE']})**: {obtener_categoria(indices['IVE'])['categoria']}
        - **Razonamiento Fluido (IRF: {indices['IRF']})**: {obtener_categoria(indices['IRF'])['categoria']}
        - **Memoria de Trabajo (IMT: {indices['IMT']})**: {obtener_categoria(indices['IMT'])['categoria']}
        - **Velocidad de Procesamiento (IVP: {indices['IVP']})**: {obtener_categoria(indices['IVP'])['categoria']}
        """
        
        st.info(interpretacion)
        
        st.markdown("---")
        
        # Generar PDF
        st.markdown("### 📄 Descargar Informe Completo")
        
        datos_paciente = {
            'nombre': nombre,
            'sexo': sexo,
            'fecha_nacimiento': fecha_nacimiento.strftime('%d/%m/%Y'),
            'fecha_aplicacion': fecha_aplicacion.strftime('%d/%m/%Y'),
            'edad_texto': edad_texto,
            'lugar': lugar,
            'examinador': examinador,
            'puntuaciones': puntuaciones
        }
        
        pdf_buffer = generar_pdf(datos_paciente, pe_dict, indices)
        
        st.download_button(
            label="📥 DESCARGAR INFORME EN PDF",
            data=pdf_buffer,
            file_name=f"Informe_WPPSI-IV_{nombre.replace(' ', '_')}_{fecha_aplicacion.strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
        
        st.success("✅ ¡Informe completo! Puedes descargarlo en PDF para imprimirlo o enviarlo.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 20px;'>
        <p><b>Generador de Informes WPPSI-IV</b></p>
        <p>Herramienta profesional para psicopedagogos y psicólogos</p>
        <p style='font-size: 0.8em;'>Desarrollado con ❤️ para facilitar la evaluación psicopedagógica</p>
    </div>
""", unsafe_allow_html=True)