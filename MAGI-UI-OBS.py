import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime
import time
import unicodedata
import random

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="MAGI SYSTEM: SUPERCOMPUTING CENTER",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializar estados de sesión
if "history" not in st.session_state:
    st.session_state.history = []

if "toxicity_level" not in st.session_state:
    st.session_state.toxicity_level = 30

if "magi_states" not in st.session_state:
    st.session_state.magi_states = {"MELCHIOR": "承 認", "BALTHASAR": "承 認", "CASPER": "承 認"}

if "magi_responses" not in st.session_state:
    st.session_state.magi_responses = {
        "MELCHIOR": "",
        "BALTHASAR": "", 
        "CASPER": "",
        "FINAL": "",
        "DILEMA": ""
    }

# --- ESTILOS CSS CON MÓDULOS PARPADEANTES Y BARRA FIJA ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

/* FONDO PRINCIPAL */
.stApp {
    background-color: #050505 !important;
    color: #ff6600 !important;
    font-family: 'Orbitron', 'Share Tech Mono', monospace !important;
    position: relative !important;
}

/* Líneas de estática */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: repeating-linear-gradient(
        0deg,
        rgba(0, 255, 200, 0.03) 0px,
        rgba(0, 255, 200, 0.03) 1px,
        transparent 1px,
        transparent 3px
    );
    pointer-events: none;
    z-index: 0;
    animation: scan 15s linear infinite;
}

@keyframes scan {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
}

/* MÓDULOS PARPADEANTES EN LADO IZQUIERDO */
.magi-modules-sidebar {
    position: fixed;
    left: 20px;
    top: 50%;
    transform: translateY(-50%);
    width: 120px;
    z-index: 999;
    display: flex;
    flex-direction: column;
    gap: 25px;
    align-items: center;
}

.module-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.module-light {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    position: relative;
    box-shadow: 0 0 20px;
}

.module-light::after {
    content: "";
    position: absolute;
    top: -5px;
    left: -5px;
    right: -5px;
    bottom: -5px;
    border-radius: 50%;
    z-index: -1;
    opacity: 0.5;
}

/* Luz de MELCHIOR (Azul) */
.melchior-light {
    background: radial-gradient(circle at 30% 30%, #0099FF, #0055AA);
    box-shadow: 0 0 25px #0099FF;
    animation: pulse-blue 2s infinite alternate;
}

.melchior-light::after {
    background: #0099FF;
    animation: glow-blue 2s infinite alternate;
}

/* Luz de BALTHASAR (Cian) */
.balthasar-light {
    background: radial-gradient(circle at 30% 30%, #00FFC8, #00AA88);
    box-shadow: 0 0 25px #00FFC8;
    animation: pulse-cyan 2.2s infinite alternate;
}

.balthasar-light::after {
    background: #00FFC8;
    animation: glow-cyan 2.2s infinite alternate;
}

/* Luz de CASPER (Naranja) */
.casper-light {
    background: radial-gradient(circle at 30% 30%, #FF6600, #AA4400);
    box-shadow: 0 0 25px #FF6600;
    animation: pulse-orange 1.8s infinite alternate;
}

.casper-light::after {
    background: #FF6600;
    animation: glow-orange 1.8s infinite alternate;
}

/* Luz del SISTEMA (Rojo) */
.system-light {
    background: radial-gradient(circle at 30% 30%, #FF0000, #AA0000);
    box-shadow: 0 0 25px #FF0000;
    animation: pulse-red 1.5s infinite;
}

.system-light::after {
    background: #FF0000;
    animation: glow-red 1.5s infinite;
}

/* Animaciones de parpadeo */
@keyframes pulse-blue {
    0% { opacity: 0.7; transform: scale(0.95); }
    100% { opacity: 1; transform: scale(1.05); }
}

@keyframes glow-blue {
    0% { opacity: 0.3; transform: scale(1); }
    100% { opacity: 0.6; transform: scale(1.1); }
}

@keyframes pulse-cyan {
    0% { opacity: 0.6; transform: scale(0.9); }
    100% { opacity: 1; transform: scale(1.1); }
}

@keyframes glow-cyan {
    0% { opacity: 0.4; transform: scale(1); }
    100% { opacity: 0.7; transform: scale(1.15); }
}

@keyframes pulse-orange {
    0% { opacity: 0.8; transform: scale(1); }
    100% { opacity: 1; transform: scale(1.08); }
}

@keyframes glow-orange {
    0% { opacity: 0.5; transform: scale(1); }
    100% { opacity: 0.8; transform: scale(1.12); }
}

@keyframes pulse-red {
    0%, 100% { opacity: 0.6; transform: scale(0.98); }
    50% { opacity: 1; transform: scale(1.02); }
}

@keyframes glow-red {
    0%, 100% { opacity: 0.4; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.05); }
}

.module-label {
    color: #fff;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.9rem;
    font-weight: bold;
    text-align: center;
    text-shadow: 0 0 10px currentColor;
    margin-top: 5px;
}

.melchior-label { color: #0099FF; }
.balthasar-label { color: #00FFC8; }
.casper-label { color: #FF6600; }
.system-label { color: #FF0000; }

/* BARRA DE TEXTO FIJA */
.fixed-input-container {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    max-width: 800px;
    z-index: 1000;
    background: rgba(5, 5, 5, 0.95);
    border: 3px solid #ff6600;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 0 40px rgba(255, 102, 0, 0.5);
    backdrop-filter: blur(10px);
}

.fixed-input-title {
    color: #00FFC8;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: center;
    text-shadow: 0 0 10px #00FFC8;
}

.fixed-input-area {
    width: 100%;
    background: rgba(10, 10, 10, 0.9) !important;
    color: #ff6600 !important;
    border: 2px solid #0099FF !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem !important;
    padding: 12px !important;
    border-radius: 5px !important;
    resize: none !important;
    min-height: 60px !important;
}

.fixed-input-area:focus {
    outline: none !important;
    border-color: #00FFC8 !important;
    box-shadow: 0 0 15px #00FFC8 !important;
}

.fixed-submit-btn {
    width: 100%;
    background: linear-gradient(145deg, #ff6600, #ff8533) !important;
    color: black !important;
    border: 2px solid #ff6600 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: bold !important;
    padding: 12px !important;
    margin-top: 10px !important;
    border-radius: 5px !important;
    cursor: pointer !important;
    transition: all 0.3s !important;
}

.fixed-submit-btn:hover {
    box-shadow: 0 0 20px #ff6600 !important;
    transform: translateY(-2px) !important;
}

/* Ajustar contenido principal para evitar solapamiento */
.main-content-container {
    margin-left: 160px !important; /* Espacio para módulos izquierdos */
    margin-bottom: 150px !important; /* Espacio para barra fija inferior */
    position: relative;
    z-index: 1;
}

/* Asegurar que el contenido esté sobre el fondo */
[data-testid="stAppViewContainer"] {
    position: relative;
    z-index: 1;
}

/* Contenido scrollable */
.scrollable-content {
    max-height: calc(100vh - 200px);
    overflow-y: auto;
    padding-right: 10px;
}

/* Ocultar scrollbar nativo y usar personalizado */
.scrollable-content::-webkit-scrollbar {
    width: 8px;
}

.scrollable-content::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.3);
}

.scrollable-content::-webkit-scrollbar-thumb {
    background: #ff6600;
    border-radius: 4px;
}

/* Resto de estilos existentes... */
h1, h2, h3, h4 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ff6600 !important;
    text-shadow: 0 0 5px rgba(255, 102, 0, 0.5) !important;
}

.response-card {
    border: 2px solid !important;
    background: rgba(10, 5, 0, 0.95) !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    position: relative !important;
    z-index: 2 !important;
    box-shadow: 0 0 15px rgba(255, 102, 0, 0.3) !important;
}

/* ... (mantener el resto de tus estilos existentes) ... */

</style>
""", unsafe_allow_html=True)

# --- AGREGAR MÓDULOS PARPADEANTES AL LADO IZQUIERDO ---
st.markdown("""
<div class="magi-modules-sidebar">
    <div class="module-container">
        <div class="module-light melchior-light"></div>
        <div class="module-label melchior-label">MELCHIOR-1</div>
        <div class="module-label" style="color: #888; font-size: 0.7rem;">SCIENCE</div>
    </div>
    
    <div class="module-container">
        <div class="module-light balthasar-light"></div>
        <div class="module-label balthasar-label">BALTHASAR-2</div>
        <div class="module-label" style="color: #888; font-size: 0.7rem;">MOTHER</div>
    </div>
    
    <div class="module-container">
        <div class="module-light casper-light"></div>
        <div class="module-label casper-label">CASPER-3</div>
        <div class="module-label" style="color: #888; font-size: 0.7rem;">WOMAN</div>
    </div>
    
    <div class="module-container">
        <div class="module-light system-light"></div>
        <div class="module-label system-label">MAGI SYSTEM</div>
        <div class="module-label" style="color: #888; font-size: 0.7rem;">CODE:473</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES (mantener las existentes) ---
def stream_data(text, speed=0.02):
    for word in text.split(" "):
        yield word + " "
        time.sleep(speed)

def limpiar_texto_para_pdf(texto):
    if not texto:
        return ""
    
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N',
        '¿': '?', '¡': '!',
    }
    
    for char, repl in reemplazos.items():
        texto = texto.replace(char, repl)
    
    try:
        texto = unicodedata.normalize('NFKD', texto)
        texto = texto.encode('ascii', 'ignore').decode('ascii')
    except:
        texto = ''.join(c if 32 <= ord(c) < 127 else '?' for c in texto)
    
    return texto[:1000]

def crear_pdf(dilema, m, b, c, final):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Courier", "B", 18)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(190, 12, "MAGI SYSTEM - DELIBERATION REPORT", ln=True, align='C')
    pdf.ln(8)
    
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(100, 100, 100)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f"CODE: 473 | DATE: {fecha}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(0, 10, "QUERY:", ln=True)
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(dilema))
    pdf.ln(10)
    
    nodos = [
        ("MELCHIOR-1 (SCIENCE)", limpiar_texto_para_pdf(m), 0, 153, 255),
        ("BALTHASAR-2 (MOTHER)", limpiar_texto_para_pdf(b), 0, 255, 200),
        ("CASPER-3 (WOMAN)", limpiar_texto_para_pdf(c), 255, 102, 0)
    ]
    
    for nombre, contenido, r, g, b in nodos:
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(r, g, b)
        pdf.cell(0, 10, f"--- {nombre} ---", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 5, contenido)
        pdf.ln(8)
    
    pdf.set_font("Courier", "B", 14)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 12, "--- FINAL RESOLUTION ---", ln=True)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(final))
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

def get_majority_decision():
    approvals = sum(1 for state in st.session_state.magi_states.values() if state == "承 認")
    return "APPROVED" if approvals >= 2 else "DENIED"

# --- CONTENIDO PRINCIPAL CONTAINER ---
st.markdown('<div class="main-content-container">', unsafe_allow_html=True)
st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)

# Header
st.markdown("# ⬢ MAGI SYSTEM: SUPERCOMPUTING CENTER")
st.markdown("**STATUS:** `OPERATIONAL` | **SYNC:** `99.9%` | **CODE:** `473` | **TOXICITY:** `" + str(st.session_state.toxicity_level) + "%`")

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# TRIUNVIRATO MAGI
st.markdown("### MAGI TRIUMVIRATE DELIBERATION")

col1, col2, col3 = st.columns(3)

with col1:
    estado_mel = st.session_state.magi_states["MELCHIOR"]
    st.markdown(f"""
    <div style="padding: 15px; margin: 10px; text-align: center; background: rgba(0, 153, 255, 0.15); border: 2px solid #0099FF;">
        <div style="font-size: 1.2rem; color: #0099FF; font-weight: bold; margin-bottom: 5px;">MELCHIOR-1</div>
        <div style="color:#888; font-size:0.9rem">SCIENCE MODULE</div>
        <div style="font-size: 2rem; font-weight: bold; margin-top: 10px; color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000'};">
            {estado_mel}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    estado_bal = st.session_state.magi_states["BALTHASAR"]
    st.markdown(f"""
    <div style="padding: 15px; margin: 10px; text-align: center; background: rgba(0, 255, 200, 0.15); border: 2px solid #00FFC8;">
        <div style="font-size: 1.2rem; color: #00FFC8; font-weight: bold; margin-bottom: 5px;">BALTHASAR-2</div>
        <div style="color:#888; font-size:0.9rem">MOTHER MODULE</div>
        <div style="font-size: 2rem; font-weight: bold; margin-top: 10px; color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000'};">
            {estado_bal}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    estado_cas = st.session_state.magi_states["CASPER"]
    st.markdown(f"""
    <div style="padding: 15px; margin: 10px; text-align: center; background: rgba(255, 102, 0, 0.15); border: 2px solid #FF6600;">
        <div style="font-size: 1.2rem; color: #FF6600; font-weight: bold; margin-bottom: 5px;">CASPER-3</div>
        <div style="color:#888; font-size:0.9rem">WOMAN MODULE</div>
        <div style="font-size: 2rem; font-weight: bold; margin-top: 10px; color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000'};">
            {estado_cas}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Panel de decisión
decision = get_majority_decision()
decision_color = "#00FFC8" if decision == "APPROVED" else "#FF0000"

st.markdown(f"""
<div style="background: rgba(0, 20, 40, 0.9); border: 3px solid {decision_color}; padding: 25px; margin: 25px 0; text-align: center;">
    <div style="font-size: 1.2rem; color: #aaa; margin-bottom: 10px;">
        SYSTEM VERDICT (2/3 Majority)
    </div>
    <div style="font-size: 2.2rem; font-weight: 900; margin: 10px 0; letter-spacing: 2px; color: {decision_color};">
        {decision}
    </div>
    <div style="margin-top: 15px; color: #888; font-size: 0.9rem;">
        Voting: 
        <span style="color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000'}">MELCHIOR: {estado_mel}</span> | 
        <span style="color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000'}">BALTHASAR: {estado_bal}</span> | 
        <span style="color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000'}">CASPER: {estado_cas}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# --- RESPUESTAS DE TEXTO (SI EXISTEN) ---
if (st.session_state.magi_responses["MELCHIOR"] or 
    st.session_state.magi_responses["BALTHASAR"] or 
    st.session_state.magi_responses["CASPER"]):
    
    st.markdown("### 📜 COMPLETE DELIBERATION RECORD")
    
    # Tres columnas para respuestas
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        if st.session_state.magi_responses["MELCHIOR"]:
            st.markdown(f"""
            <div class="response-card" style="border-color: #0099FF !important; border-left: 6px solid #0099FF !important;">
                <div style="font-size: 1.4em; border-bottom: 2px solid #0099FF; margin-bottom: 15px; padding-bottom: 8px; font-weight: bold;">
                    <span>MELCHIOR-1</span>
                    <span style="color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000'}; float: right;">
                        {estado_mel}
                    </span>
                </div>
                <div style="color: #e0e0e0; font-family: 'Share Tech Mono', monospace; line-height: 1.6; font-size: 0.95rem; white-space: pre-wrap;">
                    {st.session_state.magi_responses["MELCHIOR"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res2:
        if st.session_state.magi_responses["BALTHASAR"]:
            st.markdown(f"""
            <div class="response-card" style="border-color: #00FFC8 !important; border-left: 6px solid #00FFC8 !important;">
                <div style="font-size: 1.4em; border-bottom: 2px solid #00FFC8; margin-bottom: 15px; padding-bottom: 8px; font-weight: bold;">
                    <span>BALTHASAR-2</span>
                    <span style="color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000'}; float: right;">
                        {estado_bal}
                    </span>
                </div>
                <div style="color: #e0e0e0; font-family: 'Share Tech Mono', monospace; line-height: 1.6; font-size: 0.95rem; white-space: pre-wrap;">
                    {st.session_state.magi_responses["BALTHASAR"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res3:
        if st.session_state.magi_responses["CASPER"]:
            st.markdown(f"""
            <div class="response-card" style="border-color: #FF6600 !important; border-left: 6px solid #FF6600 !important;">
                <div style="font-size: 1.4em; border-bottom: 2px solid #FF6600; margin-bottom: 15px; padding-bottom: 8px; font-weight: bold;">
                    <span>CASPER-3</span>
                    <span style="color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000'}; float: right;">
                        {estado_cas}
                    </span>
                </div>
                <div style="color: #e0e0e0; font-family: 'Share Tech Mono', monospace; line-height: 1.6; font-size: 0.95rem; white-space: pre-wrap;">
                    {st.session_state.magi_responses["CASPER"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Resolución final
    if st.session_state.magi_responses["FINAL"]:
        st.markdown(f"""
        <div class="response-card" style="border-color: #FF0000 !important; border-left: 6px solid #FF0000 !important; background: rgba(20, 0, 0, 0.95) !important;">
            <div style="font-size: 1.4em; border-bottom: 2px solid #FF0000; margin-bottom: 15px; padding-bottom: 8px; font-weight: bold;">
                <span style="color: {decision_color}">FINAL RESOLUTION</span>
                <span style="color: {decision_color}; font-size: 1.2rem; float: right;">
                    {decision}
                </span>
            </div>
            <div style="color: #e0e0e0; font-family: 'Share Tech Mono', monospace; line-height: 1.6; font-size: 0.95rem; white-space: pre-wrap;">
                {st.session_state.magi_responses["FINAL"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    
    # ZONA DE DESCARGA
    if st.session_state.magi_responses["FINAL"]:
        st.markdown("""
        <div style="background: rgba(255, 102, 0, 0.1); border: 3px solid #ff6600; padding: 25px; margin: 30px 0; border-left: 8px solid #00FFC8;">
            <div style="font-size: 1.8rem; color: #00FFC8; font-weight: bold; margin-bottom: 15px; text-align: center;">
                📄 DOWNLOAD COMPLETE REPORT
            </div>
            <div style="color: #ff6600; font-size: 1.1rem; text-align: center; margin-bottom: 20px; padding: 10px; background: rgba(0, 0, 0, 0.3); border-radius: 5px;">
                ⬇️ <strong>Click below to download full deliberation report (PDF)</strong>
            </div>
        """, unsafe_allow_html=True)
        
        # Generar PDF
        pdf_bytes = crear_pdf(
            st.session_state.magi_responses["DILEMA"],
            st.session_state.magi_responses["MELCHIOR"],
            st.session_state.magi_responses["BALTHASAR"],
            st.session_state.magi_responses["CASPER"],
            st.session_state.magi_responses["FINAL"]
        )
        
        # Botón de descarga
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="⬇️ DOWNLOAD FULL DELIBERATION REPORT (PDF)",
                data=pdf_bytes,
                file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Includes all reasoning from all three MAGI nodes"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.info(f"📊 Report includes: Original query + 3 module analyses + Final resolution ({len(pdf_bytes):,} bytes)")

# Cerrar contenedores scrollables
st.markdown('</div>', unsafe_allow_html=True)  # Cerrar scrollable-content
st.markdown('</div>', unsafe_allow_html=True)  # Cerrar main-content-container

# --- BARRA DE TEXTO FIJA EN LA PARTE INFERIOR ---
st.markdown("""
<div class="fixed-input-container">
    <div class="fixed-input-title">🗣️ ENTER MAGI QUERY</div>
""", unsafe_allow_html=True)

# Usar un formulario para capturar el input
with st.form(key="fixed_input_form", clear_on_submit=True):
    dilema_input = st.text_area(
        "Enter tactical dilemma for MAGI analysis...",
        height=100,
        key="fixed_dilema_input",
        label_visibility="collapsed"
    )
    
    col_submit1, col_submit2 = st.columns([3, 1])
    
    with col_submit1:
        submitted = st.form_submit_button(
            "⚡ SUBMIT TO MAGI SYSTEM",
            use_container_width=True,
            type="primary"
        )
    
    with col_submit2:
        if st.form_submit_button("🔄 CLEAR", use_container_width=True):
            st.session_state.fixed_dilema_input = ""

st.markdown("</div>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔐 SYSTEM ACCESS")
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("API: ACTIVE")
    else:
        api_key = st.text_input("GROQ API KEY", type="password", key="api_key_input")
    
    if not api_key:
        st.warning("Enter API key")
    
    st.markdown("---")
    
    # Historial
    st.markdown("### 📊 HISTORY")
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history[-3:])):
            with st.expander(f"Query {len(st.session_state.history)-i}"):
                st.write(f"**Time:** {entry['timestamp']}")
                st.write(f"**Decision:** {entry['decision']}")
                if st.button(f"Load Details", key=f"load_{i}"):
                    st.session_state.magi_responses["DILEMA"] = entry['dilema']
                    st.session_state.magi_responses["FINAL"] = entry['resolucion']
                    st.session_state.magi_states = entry['states']
                    st.rerun()
    else:
        st.write("No history")
    
    # Controles
    st.markdown("---")
    if st.button("🔄 Update Metrics", use_container_width=True):
        st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + random.randint(5, 15))
        st.rerun()

# --- PROCESAR INPUT DE LA BARRA FIJA ---
# Usar session_state para capturar el valor del text_area
if 'fixed_dilema_input' not in st.session_state:
    st.session_state.fixed_dilema_input = ""

# Si se envía el formulario
if submitted and api_key and dilema_input:
    # Guardar dilema
    st.session_state.magi_responses["DILEMA"] = dilema_input
    
    # Actualizar estados
    for magi in st.session_state.magi_states:
        st.session_state.magi_states[magi] = random.choice(["承 認", "否 定"])
    
    st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + 10)
    
    try:
        client = Groq(api_key=api_key)
        
        # Procesar con prompts mejorados (usar los prompts mejorados de antes)
        with st.status("🔄 PROCESSING MAGI DELIBERATION...", expanded=True) as status:
            # ... (usar el código de procesamiento mejorado aquí) ...
            
            # CONSULTA A MELCHIOR
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres MELCHIOR. Analista científico. Proporciona análisis objetivo completo."},
                    {"role": "user", "content": dilema_input}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=500,
                top_p=0.9
            )
            m_resp = completion.choices[0].message.content
            st.session_state.magi_responses["MELCHIOR"] = m_resp
            time.sleep(0.5)
            
            # CONSULTA A BALTHASAR
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres BALTHASAR. Analista ético. Considera aspectos morales completos."},
                    {"role": "user", "content": dilema_input}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=500,
                top_p=0.9
            )
            b_resp = completion.choices[0].message.content
            st.session_state.magi_responses["BALTHASAR"] = b_resp
            time.sleep(0.5)
            
            # CONSULTA A CASPER
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres CASPER. Analista intuitivo. Considera aspectos prácticos completos."},
                    {"role": "user", "content": dilema_input}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=500,
                top_p=0.9
            )
            c_resp = completion.choices[0].message.content
            st.session_state.magi_responses["CASPER"] = c_resp
            time.sleep(0.5)
            
            # SÍNTESIS FINAL
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres el sistema MAGI. Sintetiza resolución final completa basada en las tres perspectivas."},
                    {"role": "user", "content": f"Basado en:\nCiencia: {m_resp[:200]}\nÉtica: {b_resp[:200]}\nIntuición: {c_resp[:200]}"}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.4,
                max_tokens=800,
                top_p=0.95
            )
            final_resp = completion.choices[0].message.content
            st.session_state.magi_responses["FINAL"] = final_resp
            
            status.update(label="✅ DELIBERATION COMPLETE", state="complete", expanded=False)
        
        # Agregar al historial
        st.session_state.history.append({
            "dilema": dilema_input,
            "resolucion": final_resp,
            "states": st.session_state.magi_states.copy(),
            "decision": decision,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })
        
        # Limpiar input
        st.session_state.fixed_dilema_input = ""
        
        # Rerun para mostrar todo
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem; padding: 20px; margin-top: 50px;">
    MAGI SYSTEM v3.14 | PROTOCOL 473 | ACCESS: RESTRICTED
</div>
""", unsafe_allow_html=True)
