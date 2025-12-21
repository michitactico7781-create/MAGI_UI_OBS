import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime
import time
import base64
import unicodedata
from io import BytesIO

# --- CONFIGURACIÓN E HISTORIAL ---
if "history" not in st.session_state:
    st.session_state.history = []

def add_to_history(dilema, final):
    st.session_state.history.append({"dilema": dilema, "resolucion": final})

# --- FUNCIÓN DE EFECTO DE SONIDO (HACK DE AUTOPLAY) ---
def play_magi_sound():
    # Sonido de 'data processing' (puedes cambiar el link por un .mp3 de NERV)
    sound_url = "https://www.soundjay.com/communication/beep-07.mp3"
    html_str = f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/mpeg">
        </audio>
    """
    st.markdown(html_str, unsafe_allow_html=True)

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="MAGI SYSTEM: SUPERCOMPUTING CENTER",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS AVANZADOS (FUI - Futuristic User Interface) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* FONDO Y GENERAL */
    .stApp {
        background-color: #050505;
        background-image: linear-gradient(0deg, transparent 24%, rgba(255, 102, 0, .05) 25%, rgba(255, 102, 0, .05) 26%, transparent 27%, transparent 74%, rgba(255, 102, 0, .05) 75%, rgba(255, 102, 0, .05) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(255, 102, 0, .05) 25%, rgba(255, 102, 0, .05) 26%, transparent 27%, transparent 74%, rgba(255, 102, 0, .05) 75%, rgba(255, 102, 0, .05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
        color: #ff6600;
        font-family: 'Share Tech Mono', monospace;
    }

    /* TEXTOS */
    h1, h2, h3, p, div, span, label, .stMarkdown, button {
        font-family: 'Share Tech Mono', monospace !important;
        color: #ff6600 !important;
        text-shadow: 0 0 5px rgba(255, 102, 0, 0.5);
    }
    
    /* INPUTS */
    .stTextInput>div>div>input {
        background-color: #111;
        color: #ff6600;
        border: 1px solid #ff6600;
        font-family: 'Share Tech Mono', monospace;
    }

    /* TARJETAS DE LOS NODOS (MAGI CARDS) */
    .magi-card {
        border: 2px solid #ff6600;
        background-color: rgba(20, 10, 0, 0.8);
        padding: 20px;
        margin-bottom: 15px;
        position: relative;
        clip-path: polygon(
            15px 0, 100% 0, 
            100% calc(100% - 15px), calc(100% - 15px) 100%, 
            0 100%, 0 15px
        );
        box-shadow: inset 0 0 20px rgba(255, 102, 0, 0.2);
    }
    
    .node-title {
        font-size: 1.5em;
        border-bottom: 1px solid #ff6600;
        margin-bottom: 10px;
        letter-spacing: 2px;
        text-align: center;
        font-weight: bold;
    }

    /* LÍNEA DECORATIVA */
    .deco-line {
        height: 2px;
        background: repeating-linear-gradient(to right, #ff6600, #ff6600 10px, transparent 10px, transparent 20px);
        margin: 20px 0;
        opacity: 0.7;
    }
    
    /* BOTONES */
    .stButton>button {
        border: 2px solid #ff6600;
        background-color: transparent;
        border-radius: 0;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff6600;
        color: black !important;
        box-shadow: 0 0 15px #ff6600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES MEJORADAS ---

def stream_data(text, speed=0.01):
    """Efecto de lluvia de texto"""
    for word in text.split(" "):
        yield word + " "
        time.sleep(speed)

def limpiar_texto_para_pdf(texto):
    """Limpia texto para compatibilidad con FPDF"""
    if not texto:
        return ""
    
    # Reemplazar caracteres problemáticos comunes
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N',
        '¿': '?', '¡': '!',
        '—': '-', '–': '-', '…': '...',
        '«': '"', '»': '"', '“': '"', '”': '"', '‘': "'", '’': "'",
        '€': 'EUR', '£': 'GBP', '¥': 'YEN',
        '°': 'deg', '±': '+/-', '×': 'x', '÷': '/',
        'α': 'alpha', 'β': 'beta', 'γ': 'gamma',
        '→': '->', '←': '<-', '↑': 'up', '↓': 'down',
    }
    
    for char, repl in reemplazos.items():
        texto = texto.replace(char, repl)
    
    # Intentar convertir a ASCII (lo más seguro para FPDF)
    try:
        # Primero normalizar
        texto = unicodedata.normalize('NFKD', texto)
        texto = texto.encode('ascii', 'ignore').decode('ascii')
    except:
        # Si falla, mantener solo caracteres imprimibles ASCII
        texto = ''.join(c if 32 <= ord(c) < 127 else '?' for c in texto)
    
    # Limitar longitud para evitar problemas
    if len(texto) > 1000:
        texto = texto[:1000] + "\n[...CONTINUED IN SYSTEM ARCHIVES...]"
    
    return texto

def crear_pdf_corregido(dilema, m, b, c, final):
    """Generador de Reportes NERV - VERSIÓN CORREGIDA (PDF VISIBLE)"""
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # IMPORTANTE: Usar fondo blanco para texto visible
        # pdf.set_fill_color(255, 255, 255)  # Fondo blanco (opcional)
        # pdf.rect(0, 0, 210, 297, 'F')
        
        # Título - NEGRO sobre fondo blanco
        pdf.set_font("Courier", "B", 16)
        pdf.set_text_color(0, 0, 0)  # NEGRO (visible siempre)
        pdf.cell(190, 10, "MAGI SYSTEM - CLASSIFIED REPORT", ln=True, align='C')
        pdf.ln(10)
        
        # Fecha y código
        pdf.set_font("Courier", "", 10)
        pdf.set_text_color(50, 50, 50)  # Gris oscuro
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(0, 8, f"FECHA: {fecha} | CODIGO: 473", ln=True)
        pdf.ln(5)
        
        # Limpiar todos los textos antes de usarlos
        dilema_limpio = limpiar_texto_para_pdf(dilema)
        m_limpio = limpiar_texto_para_pdf(m)
        b_limpio = limpiar_texto_para_pdf(b)
        c_limpio = limpiar_texto_para_pdf(c)
        final_limpio = limpiar_texto_para_pdf(final)
        
        # Input dilema
        pdf.set_font("Courier", "B", 12)
        pdf.set_text_color(0, 0, 0)  # NEGRO
        pdf.cell(0, 10, "INPUT DILEMA:", ln=True)
        pdf.set_font("Courier", "", 10)
        pdf.set_text_color(30, 30, 30)  # Gris muy oscuro
        pdf.multi_cell(0, 6, dilema_limpio[:500])  # Limitar longitud
        pdf.ln(10)
        
        # Línea divisoria
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(10)
        
        # Nodos MAGI
        pdf.set_font("Courier", "B", 14)
        pdf.set_text_color(0, 0, 0)  # NEGRO
        pdf.cell(0, 12, "MAGI SYSTEM ANALYSIS", ln=True)
        pdf.ln(8)
        
        # MELCHIOR-1 (usando naranja para título, texto negro)
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(255, 102, 0)  # Naranja para título
        pdf.cell(0, 10, "--- MELCHIOR-1 (SCIENCE) ---", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(0, 0, 0)  # NEGRO para contenido
        pdf.multi_cell(0, 5, m_limpio[:800])  # Limitar longitud
        pdf.ln(8)
        
        # BALTHASAR-2
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(255, 102, 0)  # Naranja
        pdf.cell(0, 10, "--- BALTHASAR-2 (MOTHER) ---", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(0, 0, 0)  # NEGRO
        pdf.multi_cell(0, 5, b_limpio[:800])
        pdf.ln(8)
        
        # CASPER-3
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(255, 102, 0)  # Naranja
        pdf.cell(0, 10, "--- CASPER-3 (WOMAN) ---", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(0, 0, 0)  # NEGRO
        pdf.multi_cell(0, 5, c_limpio[:800])
        pdf.ln(15)
        
        # Línea divisoria
        pdf.set_draw_color(255, 0, 0)  # Rojo
        pdf.set_line_width(0.8)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(10)
        
        # DECISIÓN FINAL
        pdf.set_font("Courier", "B", 13)
        pdf.set_text_color(255, 0, 0)  # Rojo para título final
        pdf.cell(0, 12, "--- FINAL DECISION ---", ln=True)
        pdf.set_font("Courier", "B", 10)
        pdf.set_text_color(0, 0, 0)  # NEGRO para contenido
        pdf.multi_cell(0, 6, final_limpio[:600])
        
        # Pie de página
        pdf.set_y(-30)
        pdf.set_font("Courier", "I", 8)
        pdf.set_text_color(100, 100, 100)  # Gris
        pdf.cell(0, 10, "NERV CONFIDENTIAL - UNAUTHORIZED ACCESS PROHIBITED", ln=True, align='C')
        
        # Generar PDF de forma segura
        try:
            return pdf.output(dest='S').encode('latin-1', 'ignore')
        except:
            # Fallback alternativo
            output_str = pdf.output(dest='S')
            return output_str.encode('latin-1', 'ignore')
            
    except Exception as e:
        st.error(f"Error en generación de PDF: {str(e)[:100]}")
        # Fallback: crear un PDF simple de emergencia
        return crear_pdf_simple_fallback(dilema, m, b, c, final)

def crear_pdf_simple_fallback(dilema, m, b, c, final):
    """Fallback ultra-simple si todo falla"""
    pdf = FPDF()
    pdf.add_page()
    
    # Solo texto negro básico
    pdf.set_font("Courier", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "MAGI SYSTEM REPORT (EMERGENCY)", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Courier", "", 10)
    
    # Contenido muy simplificado
    contenido = f"""
    Date: {datetime.datetime.now()}
    
    INPUT: {dilema[:200]}
    
    MELCHIOR: {m[:300]}
    
    BALTHASAR: {b[:300]}
    
    CASPER: {c[:300]}
    
    FINAL: {final[:400]}
    """
    
    # Limpiar texto
    contenido_limpio = limpiar_texto_para_pdf(contenido)
    pdf.multi_cell(0, 6, contenido_limpio)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- INTERFAZ PRINCIPAL (IGUAL A LA TUYA) ---

# Cabecera
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.markdown("""
    <div style="border: 2px solid #ff6600; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; transform: rotate(45deg); margin-top: 10px; box-shadow: 0 0 10px #ff6600;">
        <div style="width: 30px; height: 30px; background-color: #ff6600;"></div>
    </div>
    """, unsafe_allow_html=True)
with col_title:
    st.markdown("# ⬢ MAGI SYSTEM: SUPERCOMPUTING CENTER")
    st.markdown("**ESTADO:** `ONLINE` | **SINCRONIZACIÓN:** `99.9%`")

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# Sidebar para API Key
with st.sidebar:
    st.markdown("### 🔒 ACCESO NERV")
    # Intentar leer secretos primero, si no, pedir input manual
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("PROTOCOL: SECURE LINK ESTABLISHED")
    else:
        api_key = st.text_input("CLAVE API (Groq)", type="password")
    
    st.markdown("---")
    st.markdown("### 📜 REGISTROS ANTERIORES")
    if not st.session_state.history:
        st.write("No hay datos en memoria.")
    for i, entry in enumerate(reversed(st.session_state.history[-5:])):  # Mostrar solo últimos 5
        with st.expander(f"Log #{len(st.session_state.history)-i}: {entry['dilema'][:20]}..."):
            st.write(entry['resolucion'][:200] + "..." if len(entry['resolucion']) > 200 else entry['resolucion'])

# Input del Usuario
dilema = st.chat_input("INGRESE DATOS TÁCTICOS...")

if dilema and api_key:
    # Reproducir sonido
    play_magi_sound()
    
    client = Groq(api_key=api_key)
    
    st.markdown(f"""
    <div style="border-left: 3px solid #ff6600; padding-left: 10px; margin-bottom: 20px;">
        <small>COMANDO USUARIO:</small><br>
        <span style="font-size: 1.2em;">>> {dilema}</span>
    </div>
    """, unsafe_allow_html=True)

    def consultar_magi(prompt_system, temp):
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_system}, {"role": "user", "content": dilema}],
            model="llama-3.3-70b-versatile",
            temperature=temp,
            max_tokens=200  # Limitar para evitar textos muy largos
        )
        return completion.choices[0].message.content

    # Procesamiento con Spinner Visual
    with st.status("ESTABLECIENDO ENLACE NEURAL...", expanded=True) as status:
        st.write("Conectando con MELCHIOR-1...")
        m_resp = consultar_magi("Eres MELCHIOR. Científico, lógico, frío. Breve (máximo 100 palabras).", 0.1)
        st.write("Conectando con BALTHASAR-2...")
        b_resp = consultar_magi("Eres BALTHASAR. Madre, protectora, ética. Breve (máximo 100 palabras).", 0.5)
        st.write("Conectando con CASPER-3...")
        c_resp = consultar_magi("Eres CASPER. Mujer, intuitiva, egoísta. Breve (máximo 100 palabras).", 0.9)
        final_resp = consultar_magi(f"Resume resolución final de máximo 150 palabras basada en: M:{m_resp[:100]}, B:{b_resp[:100]}, C:{c_resp[:100]}", 0.2)
        status.update(label="SISTEMA SINCRONIZADO", state="complete", expanded=False)

    # Mostrar Resultados en Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="magi-card"><div class="node-title">MELCHIOR-1</div><small>CIENCIA</small></div>', unsafe_allow_html=True)
        st.write_stream(stream_data(m_resp))
    with col2:
        st.markdown('<div class="magi-card"><div class="node-title">BALTHASAR-2</div><small>MADRE</small></div>', unsafe_allow_html=True)
        st.write_stream(stream_data(b_resp))
    with col3:
        st.markdown('<div class="magi-card"><div class="node-title">CASPER-3</div><small>MUJER</small></div>', unsafe_allow_html=True)
        st.write_stream(stream_data(c_resp))

    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    
    # Resolución y PDF
    st.markdown("""
    <div style="background-color: rgba(255, 102, 0, 0.1); padding: 15px; border-left: 5px solid #ff6600; margin-bottom: 20px;">
        <h3>🛑 RESOLUCIÓN FINAL</h3>
    </div>
    """, unsafe_allow_html=True)
    st.write_stream(stream_data(final_resp))
    
    # Agregar al historial
    add_to_history(dilema, final_resp)
    
    # Generar PDF en memoria - USANDO LA VERSIÓN CORREGIDA
    try:
        with st.spinner("Generando informe clasificado..."):
            pdf_bytes = crear_pdf_corregido(dilema, m_resp, b_resp, c_resp, final_resp)
        
        # Mostrar información del PDF
        st.info(f"📊 **Reporte generado:** {len(pdf_bytes):,} bytes | {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        # Botón de descarga
        col_download, col_preview = st.columns([2, 1])
        with col_download:
            st.download_button(
                label="📄 DESCARGAR INFORME OFICIAL (PDF VISIBLE)",
                data=pdf_bytes,
                file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                help="El PDF ahora tendrá texto negro visible sobre fondo blanco"
            )
        
        with col_preview:
            # Vista previa del contenido
            with st.expander("📋 Vista previa del reporte"):
                st.text(f"""
                MAGI SYSTEM REPORT
                ==================
                Fecha: {datetime.datetime.now()}
                
                INPUT:
                {dilema[:100]}...
                
                MELCHIOR-1:
                {m_resp[:150]}...
                
                BALTHASAR-2:
                {b_resp[:150]}...
                
                CASPER-3:
                {c_resp[:150]}...
                
                RESOLUCIÓN FINAL:
                {final_resp[:200]}...
                """)
        
        # Opción adicional: Archivo de texto como backup
        texto_reporte = f"""MAGI SYSTEM - REPORTE DE CONSULTA
Fecha: {datetime.datetime.now()}
Código: 473

INPUT DEL USUARIO:
{dilema}

RESPUESTA MELCHIOR-1 (CIENCIA):
{m_resp}

RESPUESTA BALTHASAR-2 (MADRE):
{b_resp}

RESPUESTA CASPER-3 (MUJER):
{c_resp}

RESOLUCIÓN FINAL DEL SISTEMA:
{final_resp}

--- FIN DEL REPORTE ---
Sistema MAGI v1.0 | NERV Command"""
        
        st.download_button(
            label="📝 DESCARGAR COMO TEXTO (BACKUP)",
            data=texto_reporte,
            file_name=f"MAGI_BACKUP_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
    except Exception as pdf_error:
        st.error(f"❌ Error crítico al generar PDF: {str(pdf_error)[:100]}")
        st.info("""
        **Solución rápida:**
        1. Los textos pueden contener caracteres especiales
        2. Intenta con una consulta más corta
        3. Usa el botón de descarga como texto como alternativa
        """)

elif dilema and not api_key:
    st.warning("⚠️ MAGI OFFLINE. INGRESE CLAVE DE ACCESO EN EL PANEL LATERAL.")
    
    # Mostrar instrucciones
    with st.expander("ℹ️ ¿Cómo obtener una API key de Groq?"):
        st.markdown("""
        1. Visita [console.groq.com](https://console.groq.com)
        2. Regístrate o inicia sesión
        3. Ve a "API Keys" en el menú
        4. Crea una nueva API key
        5. Cópiala y pégala en el panel lateral de esta aplicación
        6. ¡Listo! El sistema MAGI se activará automáticamente
        """)

# Footer adicional
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #ff6600; opacity: 0.7; font-size: 0.9rem; margin-top: 30px;">
    <i>MAGI SYSTEM v1.0 | NERV Supercomputing Center | Protocol 473 Active</i>
</div>
""", unsafe_allow_html=True)
