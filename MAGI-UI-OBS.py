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

# --- ESTILOS CSS EVANGELION MEJORADO ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=VT323&display=swap');

/* FONDO PRINCIPAL - ESTILO EVANGELION */
.stApp {
    background-color: #000000 !important;
    color: #00FF41 !important;
    font-family: 'VT323', 'Share Tech Mono', monospace !important;
    font-size: 1.1em !important;
}

/* EFECTO CRT MÁS PRONUNCIADO */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px);
    background-size: 3px 3px;
    pointer-events: none;
    z-index: 0;
    animation: scan 8s linear infinite;
}

@keyframes scan {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
}

/* EFECTO DE PARPADEO DEL CURSOR */
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

/* GLITCH DIGITAL OCASIONAL */
@keyframes glitch {
    0% { transform: translate(0); }
    20% { transform: translate(-1px, 1px); }
    40% { transform: translate(-1px, -1px); }
    60% { transform: translate(1px, 1px); }
    80% { transform: translate(1px, -1px); }
    100% { transform: translate(0); }
}

/* CONTENIDO PRINCIPAL */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main-content,
.stAppViewContainer {
    position: relative !important;
    z-index: 1 !important;
    background: rgba(0, 0, 0, 0.85) !important;
    border: 1px solid #00FF41 !important;
    margin: 10px !important;
    padding: 15px !important;
}

/* TÍTULOS AL ESTILO EVANGELION */
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00FF41 !important;
    text-shadow: 0 0 5px #00FF41 !important;
    border-bottom: 1px solid #00FF41 !important;
    padding-bottom: 5px !important;
    margin-bottom: 15px !important;
    letter-spacing: 1px !important;
}

/* HEXÁGONOS MAGI - ESTILO EVANGELION */
.magi-hexagon {
    background: rgba(0, 20, 0, 0.8) !important;
    border: 2px solid #00FF41 !important;
    border-radius: 0 !important;
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%) !important;
    padding: 20px !important;
    margin: 10px !important;
    text-align: center !important;
    box-shadow: 
        inset 0 0 10px rgba(0, 255, 65, 0.3),
        0 0 15px rgba(0, 255, 65, 0.2) !important;
    position: relative !important;
    z-index: 2 !important;
}

.magi-name {
    color: #00FF41 !important;
    font-size: 1.3em !important;
    font-weight: bold !important;
    margin-bottom: 5px !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
}

.magi-status {
    font-size: 2.5em !important;
    font-family: 'MS Gothic', 'MS Mincho', monospace !important;
    margin-top: 15px !important;
    font-weight: bold !important;
}

.status-approved {
    color: #00FFC8 !important;
    text-shadow: 0 0 10px rgba(0, 255, 200, 0.7) !important;
    animation: blink 2s infinite;
}

.status-denied {
    color: #FF0000 !important;
    text-shadow: 0 0 10px rgba(255, 0, 0, 0.7) !important;
    animation: blink 1s infinite;
}

/* PANEL DE DECISIÓN - ESTILO MILITAR */
.decision-panel {
    background: rgba(0, 10, 0, 0.9) !important;
    border: 2px solid #00FF41 !important;
    padding: 20px !important;
    margin: 20px 0 !important;
    position: relative !important;
    z-index: 2 !important;
}

.decision-panel::before {
    content: ">";
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #00FF41;
    animation: blink 1s infinite;
    font-size: 1.5em;
}

.decision-text {
    font-size: 2.5em !important;
    font-weight: bold !important;
    text-align: center !important;
    letter-spacing: 3px !important;
    color: inherit !important;
}

.decision-approved {
    border-color: #00FFC8 !important;
    background: rgba(0, 255, 200, 0.15) !important;
    box-shadow: 0 0 20px rgba(0, 255, 200, 0.3) !important;
}

.decision-denied {
    border-color: #FF0000 !important;
    background: rgba(255, 0, 0, 0.15) !important;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.3) !important;
}

/* TARJETAS DE RESPUESTA - ESTILO TERMINAL */
.response-card {
    background: rgba(0, 5, 0, 0.9) !important;
    border: 1px solid #00FF41 !important;
    border-left: 4px solid #00FF41 !important;
    margin: 10px 0 !important;
    padding: 15px !important;
    position: relative !important;
    z-index: 2 !important;
    min-height: 200px !important;
}

.response-card::before {
    content: ">> ";
    color: #00FF41;
    font-weight: bold;
    position: absolute;
    left: 5px;
    top: 15px;
}

.response-title {
    color: #00FF41 !important;
    border-bottom: 1px dashed #00FF41 !important;
    padding-bottom: 5px !important;
    margin-bottom: 10px !important;
    font-size: 1.2em !important;
    font-weight: bold !important;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.response-content {
    color: #CCFFCC !important;
    font-family: 'Share Tech Mono', monospace !important;
    line-height: 1.6 !important;
    white-space: pre-wrap !important;
    font-size: 0.95em !important;
}

/* COLORES ESPECÍFICOS PARA CADA MAGI */
.melchior-card {
    border-left-color: #00CCFF !important;
}

.balthasar-card {
    border-left-color: #00FFAA !important;
}

.casper-card {
    border-left-color: #FF6600 !important;
}

.final-card {
    border-left-color: #FF0000 !important;
    background: rgba(20, 0, 0, 0.9) !important;
}

/* SECCIÓN DE DESCARGA */
.download-section {
    background: rgba(0, 20, 0, 0.9) !important;
    border: 2px solid #00FF41 !important;
    padding: 20px !important;
    margin: 20px 0 !important;
    border-left: 6px solid #FF0000 !important;
    position: relative !important;
    z-index: 2 !important;
}

.download-title {
    color: #FF0000 !important;
    font-size: 1.5em !important;
    font-weight: bold !important;
    text-align: center !important;
    margin-bottom: 15px !important;
    text-transform: uppercase !important;
}

.download-instruction {
    color: #00FF41 !important;
    font-size: 1.1em !important;
    text-align: center !important;
    margin-bottom: 20px !important;
    padding: 10px !important;
    background: rgba(0, 0, 0, 0.3) !important;
}

/* BOTONES - ESTILO INTERFAZ MILITAR */
.stButton > button {
    background: rgba(0, 20, 0, 0.8) !important;
    border: 1px solid #00FF41 !important;
    color: #00FF41 !important;
    font-family: 'VT323', monospace !important;
    font-size: 1.2em !important;
    border-radius: 0 !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
    position: relative !important;
    z-index: 2 !important;
}

.stButton > button:hover {
    background: #00FF41 !important;
    color: #000000 !important;
    box-shadow: 0 0 10px #00FF41 !important;
}

/* INPUTS - ESTILO TERMINAL */
.stTextInput > div > div > input,
.stChatInput > div > div > textarea {
    background: rgba(0, 10, 0, 0.9) !important;
    border: 1px solid #00FF41 !important;
    color: #00FF41 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 0 !important;
    padding: 10px !important;
    position: relative !important;
    z-index: 2 !important;
}

/* LÍNEAS DECORATIVAS */
.deco-line {
    height: 1px;
    background: linear-gradient(90deg, 
        transparent, 
        #00FF41, 
        #00FF41, 
        transparent);
    margin: 20px 0;
    opacity: 0.7;
    position: relative;
    z-index: 2;
}

/* SCROLLBAR ESTILIZADO */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 20, 0, 0.5);
}

::-webkit-scrollbar-thumb {
    background: #00FF41;
}

/* EFECTO DE TEXTO TIPO MÁQUINA DE ESCRIBIR */
.typewriter {
    overflow: hidden;
    border-right: .15em solid #00FF41;
    white-space: nowrap;
    margin: 0 auto;
    letter-spacing: .15em;
    animation: 
        typing 3.5s steps(40, end),
        blink-caret .75s step-end infinite;
}

@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}

@keyframes blink-caret {
    from, to { border-color: transparent }
    50% { border-color: #00FF41; }
}

/* SIDEBAR ESTILO EVANGELION */
[data-testid="stSidebar"] {
    background-color: #000000 !important;
    border-right: 2px solid #00FF41 !important;
}

[data-testid="stSidebar"] * {
    color: #00FF41 !important;
}

/* MENSAJES DE ESTADO */
.stSuccess {
    background-color: rgba(0, 255, 65, 0.1) !important;
    border: 1px solid #00FF41 !important;
    color: #00FF41 !important;
}

.stWarning {
    background-color: rgba(255, 204, 0, 0.1) !important;
    border: 1px solid #FFCC00 !important;
    color: #FFCC00 !important;
}

.stError {
    background-color: rgba(255, 0, 0, 0.1) !important;
    border: 1px solid #FF0000 !important;
    color: #FF0000 !important;
}

.stInfo {
    background-color: rgba(0, 204, 255, 0.1) !important;
    border: 1px solid #00CCFF !important;
    color: #00CCFF !important;
}

/* EFECTO DE ENTRADA DEL SISTEMA */
.system-boot {
    animation: boot-sequence 3s ease-out;
}

@keyframes boot-sequence {
    0% { opacity: 0; transform: translateY(-20px); }
    100% { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES MEJORADAS ---
def stream_data_evangelion(text, speed=0.03):
    """Efecto de máquina de escribir al estilo Evangelion con glitch ocasional"""
    import random
    
    glitch_chars = ['�', '▓', '▒', '░', '█', '■', '□', '▢']
    
    for char in text:
        # Glitch digital ocasional (3% de probabilidad)
        if random.random() < 0.03:
            yield random.choice(glitch_chars)
            time.sleep(0.05)
            yield char
        else:
            yield char
        
        time.sleep(speed)
        
        # Pausa más larga en puntos y comas
        if char in ['.', '!', '?', ';']:
            time.sleep(speed * 3)

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

def crear_pdf_evangelion(dilema, m, b, c, final):
    """Crea un PDF con estilo Evangelion"""
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado estilo Evangelion
    pdf.set_font("Courier", "B", 18)
    pdf.set_text_color(0, 255, 65)  # Verde Evangelion
    pdf.cell(190, 12, "MAGI SYSTEM - DELIBERATION REPORT", ln=True, align='C')
    pdf.ln(8)
    
    # Línea decorativa
    pdf.set_draw_color(0, 255, 65)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(100, 200, 100)  # Verde más claro
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f"CODE: 473 | DATE: {fecha}", ln=True)
    pdf.cell(0, 8, f"TOXICITY LEVEL: {st.session_state.toxicity_level}%", ln=True)
    pdf.ln(10)
    
    # Consulta original
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(0, 255, 65)
    pdf.cell(0, 10, "> USER QUERY:", ln=True)
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(150, 255, 150)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(dilema))
    pdf.ln(10)
    
    # Nodos con colores Evangelion
    nodos = [
        ("MELCHIOR-1 (SCIENCE)", limpiar_texto_para_pdf(m), 0, 204, 255),    # Cian
        ("BALTHASAR-2 (MOTHER)", limpiar_texto_para_pdf(b), 0, 255, 170),    # Verde azulado
        ("CASPER-3 (WOMAN)", limpiar_texto_para_pdf(c), 255, 102, 0)         # Naranja
    ]
    
    for nombre, contenido, r, g, b in nodos:
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(r, g, b)
        pdf.cell(0, 10, f">>> {nombre} <<<", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(150, 255, 150)  # Verde claro para contenido
        pdf.multi_cell(0, 5, contenido)
        pdf.ln(8)
    
    # Línea separadora
    pdf.set_draw_color(255, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # Resolución final en rojo
    pdf.set_font("Courier", "B", 14)
    pdf.set_text_color(255, 0, 0)  # Rojo
    pdf.cell(0, 12, ">>> FINAL RESOLUTION <<<", ln=True)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(200, 100, 100)  # Rojo atenuado
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(final))
    
    # Pie de página
    pdf.ln(10)
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "MAGI SYSTEM v3.0 | CLASSIFIED LEVEL: AAA | FOR AUTHORIZED PERSONNEL ONLY", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

def get_majority_decision():
    approvals = sum(1 for state in st.session_state.magi_states.values() if state == "承 認")
    return "APPROVED" if approvals >= 2 else "DENIED"

def mostrar_secuencia_boot():
    """Muestra una secuencia de arranque al estilo Evangelion"""
    boot_messages = [
        "> INITIATING MAGI SYSTEM BOOT SEQUENCE...",
        "> NEURO-LINK ESTABLISHED...",
        "> TRIUMVIRATE SYNCHRONIZATION...",
        "> MELCHIOR-1: ONLINE",
        "> BALTHASAR-2: ONLINE", 
        "> CASPER-3: ONLINE",
        "> DELIBERATION MATRIX: ACTIVE",
        "> AWAITING USER INPUT..."
    ]
    
    placeholder = st.empty()
    for i, msg in enumerate(boot_messages):
        placeholder.markdown(f"""
        <div style='color:#00FF41; font-family:"Share Tech Mono"; margin:5px 0;'>
            {msg}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.3)
    
    time.sleep(1)
    placeholder.empty()

# --- INTERFAZ PRINCIPAL - ESTILO EVANGELION ---

# Mostrar secuencia de arranque solo la primera vez
if "boot_shown" not in st.session_state:
    st.session_state.boot_shown = True
    mostrar_secuencia_boot()

st.markdown("# ⬢ MAGI SYSTEM: SUPERCOMPUTING CENTER")
st.markdown("**STATUS:** `OPERATIONAL` | **SYNC:** `99.9%` | **CODE:** `473` | **TOXICITY:** `" + str(st.session_state.toxicity_level) + "%`")

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# TRIUNVIRATO MAGI - VERSIÓN EVANGELION
st.markdown("### MAGI TRIUMVIRATE DELIBERATION MATRIX")

col1, col2, col3 = st.columns(3)

with col1:
    estado_mel = st.session_state.magi_states["MELCHIOR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">MELCHIOR-1</div>
        <div style="color:#00CCFF; font-size:0.9rem">SCIENCE MODULE</div>
        <div class="magi-status {'status-approved' if estado_mel == '承 認' else 'status-denied'}">
            {estado_mel}
        </div>
        <div style="color:#888; font-size:0.8rem; margin-top:10px;">LOGIC | DATA | ANALYSIS</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    estado_bal = st.session_state.magi_states["BALTHASAR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">BALTHASAR-2</div>
        <div style="color:#00FFAA; font-size:0.9rem">MOTHER MODULE</div>
        <div class="magi-status {'status-approved' if estado_bal == '承 認' else 'status-denied'}">
            {estado_bal}
        </div>
        <div style="color:#888; font-size:0.8rem; margin-top:10px;">ETHICS | PROTECTION | CARE</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    estado_cas = st.session_state.magi_states["CASPER"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">CASPER-3</div>
        <div style="color:#FF6600; font-size:0.9rem">WOMAN MODULE</div>
        <div class="magi-status {'status-approved' if estado_cas == '承 認' else 'status-denied'}">
            {estado_cas}
        </div>
        <div style="color:#888; font-size:0.8rem; margin-top:10px;">INTUITION | PRACTICALITY | DESIRE</div>
    </div>
    """, unsafe_allow_html=True)

# Panel de decisión estilo Evangelion
decision = get_majority_decision()
decision_class = "decision-approved" if decision == "APPROVED" else "decision-denied"
decision_color = "#00FFC8" if decision == "APPROVED" else "#FF0000"

st.markdown(f"""
<div class="decision-panel {decision_class}">
    <div style="font-size: 1.2rem; color: #aaa; margin-bottom: 10px;">
        > SYSTEM VERDICT (2/3 Majority Required)
    </div>
    <div class="decision-text" style="color: {decision_color};">
        {decision}
    </div>
    <div style="margin-top: 15px; color: #888; font-size: 0.9rem;">
        Voting Matrix: 
        <span style="color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000'}">MELCHIOR: {estado_mel}</span> | 
        <span style="color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000'}">BALTHASAR: {estado_bal}</span> | 
        <span style="color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000'}">CASPER: {estado_cas}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# --- RESPUESTAS DE TEXTO ---
if (st.session_state.magi_responses["MELCHIOR"] or 
    st.session_state.magi_responses["BALTHASAR"] or 
    st.session_state.magi_responses["CASPER"]):
    
    # Mostrar efecto de carga del sistema
    with st.expander("📜 COMPLETE DELIBERATION RECORD", expanded=True):
        st.markdown("""
        <div style='color:#00FF41; font-family:"Share Tech Mono";'>
            > DELIBERATION RECORD LOADING...
            > ACCESSING NEURAL PATTERN ARCHIVES...
            > DISPLAYING ANALYSIS MATRIX...
        </div>
        """, unsafe_allow_html=True)
    
    # Tres columnas para respuestas
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        if st.session_state.magi_responses["MELCHIOR"]:
            st.markdown(f"""
            <div class="response-card melchior-card">
                <div class="response-title">
                    <span>MELCHIOR-1</span>
                    <span style="color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000'}">
                        {estado_mel}
                    </span>
                </div>
                <div class="response-content">
                    {st.session_state.magi_responses["MELCHIOR"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res2:
        if st.session_state.magi_responses["BALTHASAR"]:
            st.markdown(f"""
            <div class="response-card balthasar-card">
                <div class="response-title">
                    <span>BALTHASAR-2</span>
                    <span style="color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000'}">
                        {estado_bal}
                    </span>
                </div>
                <div class="response-content">
                    {st.session_state.magi_responses["BALTHASAR"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res3:
        if st.session_state.magi_responses["CASPER"]:
            st.markdown(f"""
            <div class="response-card casper-card">
                <div class="response-title">
                    <span>CASPER-3</span>
                    <span style="color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000'}">
                        {estado_cas}
                    </span>
                </div>
                <div class="response-content">
                    {st.session_state.magi_responses["CASPER"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Resolución final
    if st.session_state.magi_responses["FINAL"]:
        st.markdown(f"""
        <div class="response-card final-card">
            <div class="response-title">
                <span style="color: {decision_color}">>>> FINAL RESOLUTION <<<</span>
                <span style="color: {decision_color}; font-size: 1.2rem;">
                    {decision}
                </span>
            </div>
            <div class="response-content">
                {st.session_state.magi_responses["FINAL"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# --- ZONA DE DESCARGA DEL INFORME ---
if st.session_state.magi_responses["FINAL"]:
    st.markdown("""
    <div class="download-section">
        <div class="download-title">📄 DOWNLOAD COMPLETE DELIBERATION REPORT</div>
        <div class="download-instruction">
            ⬇️ <strong>Click the button below to download the full MAGI deliberation report (PDF)</strong>
        </div>
    """, unsafe_allow_html=True)
    
    # Generar PDF con estilo Evangelion
    pdf_bytes = crear_pdf_evangelion(
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
    
    # Información del reporte
    st.info(f"📊 Report size: {len(pdf_bytes):,} bytes | Contains: Original query + 3 module analyses + Final resolution")

# --- SIDEBAR ESTILO EVANGELION ---
with st.sidebar:
    st.markdown("### 🔐 SYSTEM ACCESS CONTROL")
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("API: ACTIVE")
    else:
        api_key = st.text_input("GROQ API KEY", type="password", key="api_key_input")
    
    if not api_key:
        st.warning("> Enter API key to initialize system")
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    
    # Historial de consultas
    st.markdown("### 📊 MISSION HISTORY")
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"MISSION {len(st.session_state.history)-i}"):
                st.write(f"**Time:** `{entry['timestamp']}`")
                st.write(f"**Decision:** `{entry['decision']}`")
                st.write(f"**Quality:** `{entry.get('quality', 'STANDARD')}`")
    else:
        st.write("> No mission records found")
    
    # Controles del sistema
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    st.markdown("### ⚙️ SYSTEM CONTROLS")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Update Metrics", use_container_width=True):
            st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + random.randint(5, 15))
            st.rerun()
    
    with col_btn2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    
    # Slider de toxicidad
    toxicity = st.slider("Toxicity Level", 0, 100, st.session_state.toxicity_level)
    st.session_state.toxicity_level = toxicity
    
    # Información del sistema
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    st.markdown("### ℹ️ SYSTEM INFO")
    st.write(f"**Version:** `3.0`")
    st.write(f"**Uptime:** `{random.randint(100, 1000)} hours`")
    st.write(f"**Neural Load:** `{random.randint(30, 90)}%`")

# --- INPUT PRINCIPAL CON EFECTO ---
st.markdown("### > QUERY INPUT INTERFACE")
st.markdown("""
<div style='color:#00FF41; font-family:"Share Tech Mono"; margin-bottom:10px;'>
    > ENTER TACTICAL QUERY FOR MAGI ANALYSIS...
    > [INPUT EXPECTED]
</div>
""", unsafe_allow_html=True)

dilema = st.chat_input("Type query here...", key="query_input")

# --- PROCESAMIENTO CON EFECTOS EVANGELION ---
if dilema and api_key:
    # Efecto de confirmación
    with st.chat_message("user"):
        st.markdown(f"""
        <div style='color:#00FF41; font-family:"Share Tech Mono";'>
            > QUERY RECEIVED: "{dilema[:50]}..."
            > PROCESSING...
        </div>
        """, unsafe_allow_html=True)
    
    # Guardar dilema
    st.session_state.magi_responses["DILEMA"] = dilema
    
    # Actualizar estados con efecto de aleatoriedad controlada
    for magi in st.session_state.magi_states:
        # 70% de probabilidad de aprobación para hacerlo más realista
        st.session_state.magi_states[magi] = "承 認" if random.random() < 0.7 else "否 定"
    
    st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + random.randint(5, 15))
    
    try:
        client = Groq(api_key=api_key)
        
        # Mostrar animación de procesamiento
        with st.status("🔄 INITIATING MAGI DELIBERATION PROTOCOL...", expanded=True) as status:
            
            # Barra de progreso con estilo Evangelion
            progress_bar = st.progress(0)
            
            # Mensajes de progreso
            progress_messages = [
                ("🔬 Accessing MELCHIOR-1 (Science Node)...", 25),
                ("🛡️ Querying BALTHASAR-2 (Ethics Node)...", 50),
                ("🌸 Consulting CASPER-3 (Intuition Node)...", 75),
                ("⚡ Synthesizing final resolution...", 100)
            ]
            
            # 1. CONSULTA A MELCHIOR
            st.write(progress_messages[0][0])
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"""Eres MELCHIOR-1, el nodo científico del sistema MAGI. 
                    Analiza desde perspectiva puramente científica, lógica y basada en datos.
                    DILEMA: {dilema}
                    Responde en español, sé exhaustivo pero preciso."""},
                    {"role": "user", "content": "Proporciona análisis científico completo."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=800,
                top_p=0.9
            )
            m_resp = completion.choices[0].message.content
            st.session_state.magi_responses["MELCHIOR"] = m_resp
            progress_bar.progress(progress_messages[0][1])
            time.sleep(0.8)
            
            # 2. CONSULTA A BALTHASAR
            st.write(progress_messages[1][0])
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"""Eres BALTHASAR-2, el nodo materno/ético del sistema MAGI.
                    Analiza desde perspectiva ética, moral y de protección humana.
                    DILEMA: {dilema}
                    Responde en español, sé comprensivo pero firme en principios."""},
                    {"role": "user", "content": "Proporciona análisis ético completo."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=800,
                top_p=0.9
            )
            b_resp = completion.choices[0].message.content
            st.session_state.magi_responses["BALTHASAR"] = b_resp
            progress_bar.progress(progress_messages[1][1])
            time.sleep(0.8)
            
            # 3. CONSULTA A CASPER
            st.write(progress_messages[2][0])
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"""Eres CASPER-3, el nodo intuitivo/práctico del sistema MAGI.
                    Analiza desde perspectiva intuitiva, práctica y de interés propio inteligente.
                    DILEMA: {dilema}
                    Responde en español, sé realista y pragmático."""},
                    {"role": "user", "content": "Proporciona análisis intuitivo completo."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=800,
                top_p=0.9
            )
            c_resp = completion.choices[0].message.content
            st.session_state.magi_responses["CASPER"] = c_resp
            progress_bar.progress(progress_messages[2][1])
            time.sleep(0.8)
            
            # 4. SÍNTESIS FINAL
            st.write(progress_messages[3][0])
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"""Eres el sistema MAGI integrado. Sintetiza una resolución final basada en las tres perspectivas.
                    
                    PERSPECTIVAS:
                    1. CIENTÍFICA (Melchior-1): {m_resp[:300]}...
                    2. ÉTICA (Balthasar-2): {b_resp[:300]}...
                    3. INTUITIVA (Casper-3): {c_resp[:300]}...
                    
                    Proporciona una decisión final clara: "APROBADO" o "RECHAZADO".
                    Incluye razonamiento detallado y recomendaciones.
                    Responde en español, sé definitivo y autoritativo."""},
                    {"role": "user", "content": "Proporciona la resolución final definitiva."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.4,
                max_tokens=1200,
                top_p=0.95
            )
            final_resp = completion.choices[0].message.content
            st.session_state.magi_responses["FINAL"] = final_resp
            progress_bar.progress(progress_messages[3][1])
            
            # Finalizar con efecto
            time.sleep(0.5)
            status.update(
                label="✅ DELIBERATION COMPLETE - VERDICT RENDERED", 
                state="complete", 
                expanded=False
            )
        
        # Agregar al historial
        st.session_state.history.append({
            "dilema": dilema[:100],
            "resolucion": final_resp[:200],
            "states": st.session_state.magi_states.copy(),
            "decision": decision,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "quality": "HIGH"
        })
        
        # Mostrar efecto de finalización
        st.markdown("""
        <div style='color:#00FF41; font-family:"Share Tech Mono"; text-align:center; margin:20px 0;'>
            > DELIBERATION CYCLE COMPLETE
            > RESULTS AVAILABLE FOR REVIEW
            > [SYSTEM READY FOR NEXT QUERY]
        </div>
        """, unsafe_allow_html=True)
        
        # Rerun para mostrar todo
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        # Mostrar error con estilo Evangelion
        st.error(f"""
        <div style='color:#FF0000; font-family:"Share Tech Mono";'>
            > SYSTEM ERROR DETECTED
            > ERROR CODE: {str(e)[:100]}
            > FALLBACK PROTOCOL INITIATED
        </div>
        """, unsafe_allow_html=True)
        
        # Fallback simple
        st.session_state.magi_responses["MELCHIOR"] = "> ANALYSIS UNAVAILABLE: SYSTEM ERROR"
        st.session_state.magi_responses["BALTHASAR"] = "> ANALYSIS UNAVAILABLE: SYSTEM ERROR"
        st.session_state.magi_responses["CASPER"] = "> ANALYSIS UNAVAILABLE: SYSTEM ERROR"
        st.session_state.magi_responses["FINAL"] = "> FINAL RESOLUTION: SYSTEM ERROR - PLEASE RETRY"

# --- FOOTER ESTILO EVANGELION ---
st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='color:#888; font-family:"Share Tech Mono"; text-align:center; font-size:0.8em;'>
    > MAGI SYSTEM v3.0 | NERV COMMAND AUTHORIZED ACCESS ONLY
    > ALL DELIBERATIONS ARE CLASSIFIED LEVEL AAA
    > UNAUTHORIZED ACCESS WILL BE MET WITH TERMINAL COUNTERMEASURES
</div>
""", unsafe_allow_html=True)
