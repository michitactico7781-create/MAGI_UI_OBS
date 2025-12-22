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

# Almacenar respuestas completas - ¡ESTAS SON LAS CLAVES QUE PERMANECEN!
if "magi_responses" not in st.session_state:
    st.session_state.magi_responses = {
        "MELCHIOR": "",
        "BALTHASAR": "", 
        "CASPER": "",
        "FINAL": "",
        "DILEMA": ""
    }

# --- ESTILOS CSS CON LÍNEAS DE ESTÁTICA ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

/* FONDO CON LÍNEAS DE ESTÁTICA */
.stApp {
    background-color: #050505;
    color: #ff6600;
    font-family: 'Orbitron', 'Share Tech Mono', monospace;
    position: relative;
    overflow-x: hidden;
}

/* Líneas de estática/escaneo CRT */
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

/* Fondo de interferencia sutil */
.stApp::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 80%, rgba(255, 102, 0, 0.02) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(0, 255, 200, 0.02) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* Asegurar que el contenido esté sobre el fondo */
.main-content {
    position: relative;
    z-index: 1;
}

/* Títulos */
h1, h2, h3, h4 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ff6600 !important;
    text-shadow: 0 0 5px rgba(255, 102, 0, 0.5);
    position: relative;
    z-index: 1;
}

/* TARJETAS DE RESPUESTAS PERMANENTES - SIEMPRE VISIBLES */
.response-permanent {
    border: 2px solid;
    background: rgba(10, 5, 0, 0.95);
    padding: 20px;
    margin: 15px 0;
    min-height: 200px;
    max-height: 400px;
    overflow-y: auto;
    position: relative;
    z-index: 1;
    box-shadow: 0 0 15px rgba(255, 102, 0, 0.2);
}

.response-permanent.melchior {
    border-color: #0099FF;
    border-left: 6px solid #0099FF;
}

.response-permanent.balthasar {
    border-color: #00FFC8;
    border-left: 6px solid #00FFC8;
}

.response-permanent.casper {
    border-color: #FF6600;
    border-left: 6px solid #FF6600;
}

.response-permanent.final {
    border-color: #FF0000;
    border-left: 6px solid #FF0000;
    background: rgba(20, 0, 0, 0.95);
}

.response-title {
    font-size: 1.4em;
    border-bottom: 2px solid;
    margin-bottom: 15px;
    padding-bottom: 8px;
    font-weight: bold;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.response-content {
    color: #e0e0e0;
    font-family: 'Share Tech Mono', monospace;
    line-height: 1.6;
    font-size: 0.95rem;
    white-space: pre-wrap;
    padding: 10px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 3px;
}

/* Hexágonos MAGI */
.magi-hexagon {
    padding: 15px;
    margin: 10px;
    text-align: center;
    background: rgba(0, 153, 255, 0.15);
    border: 2px solid #0099FF;
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
    height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    z-index: 1;
}

.magi-name {
    font-size: 1.2rem;
    color: #0099FF;
    font-weight: bold;
    margin-bottom: 5px;
}

.magi-status {
    font-size: 2rem;
    font-weight: bold;
    margin-top: 10px;
    font-family: 'MS Gothic', 'MS Mincho', monospace;
}

.status-approved {
    color: #00FFC8 !important;
    text-shadow: 0 0 10px rgba(0, 255, 200, 0.7) !important;
}

.status-denied {
    color: #FF0000 !important;
    text-shadow: 0 0 10px rgba(255, 0, 0, 0.7) !important;
}

/* Panel de decisión */
.decision-panel {
    background: rgba(0, 20, 40, 0.9);
    border: 3px solid;
    padding: 25px;
    margin: 25px 0;
    text-align: center;
    position: relative;
    z-index: 1;
}

.decision-approved {
    border-color: #00FFC8;
    background: rgba(0, 255, 200, 0.15);
    box-shadow: 0 0 20px rgba(0, 255, 200, 0.3);
}

.decision-denied {
    border-color: #FF0000;
    background: rgba(255, 0, 0, 0.15);
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
}

.decision-text {
    font-size: 2.2rem;
    font-weight: 900;
    margin: 10px 0;
    letter-spacing: 2px;
}

/* Botones */
.stButton > button {
    border: 2px solid #ff6600;
    background: rgba(255, 102, 0, 0.15);
    color: #ff6600 !important;
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    border-radius: 0;
    padding: 12px 24px;
    transition: all 0.3s;
    position: relative;
    z-index: 1;
}

.stButton > button:hover {
    background: #ff6600;
    color: black !important;
    box-shadow: 0 0 15px #ff6600;
}

/* Inputs */
.stTextInput > div > div > input,
.stChatInput > div > div > textarea {
    background-color: rgba(10, 10, 10, 0.95) !important;
    color: #ff6600 !important;
    border: 2px solid #ff6600 !important;
    font-family: 'Share Tech Mono', monospace !important;
    position: relative;
    z-index: 1;
}

/* Línea decorativa */
.deco-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #ff6600, #00FFC8, #0099FF, transparent);
    margin: 20px 0;
    opacity: 0.7;
    position: relative;
    z-index: 1;
}

/* Contenedor de texto visible */
.visible-text {
    background: rgba(0, 0, 0, 0.7);
    border: 1px solid rgba(255, 102, 0, 0.3);
    padding: 15px;
    margin: 10px 0;
    border-radius: 3px;
    color: #e0e0e0;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
    line-height: 1.5;
    position: relative;
    z-index: 1;
}

/* Kanji styling */
.kanji {
    font-family: 'MS Gothic', 'MS Mincho', monospace;
    font-weight: bold;
    color: #00FFC8;
}

.warning {
    color: #FF0000;
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0.7; }
}

/* Scrollbar personalizado */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.3);
}

::-webkit-scrollbar-thumb {
    background: #ff6600;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #ff8533;
}
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES ---
def stream_data(text, speed=0.02):
    """Efecto de escritura terminal"""
    for word in text.split(" "):
        yield word + " "
        time.sleep(speed)

def limpiar_texto_para_pdf(texto):
    """Limpia texto para compatibilidad con PDF"""
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
    """Genera PDF con todas las respuestas"""
    pdf = FPDF()
    pdf.add_page()
    
    # Título
    pdf.set_font("Courier", "B", 18)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(190, 12, "MAGI SYSTEM - COMPLETE DELIBERATION REPORT", ln=True, align='C')
    pdf.ln(8)
    
    # Información
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(100, 100, 100)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f"CODE: 473 | DATE: {fecha} | TOXICITY: {st.session_state.toxicity_level}%", ln=True)
    pdf.ln(10)
    
    # Input original
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(0, 10, "ORIGINAL QUERY:", ln=True)
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(dilema))
    pdf.ln(10)
    
    # RESPUESTAS COMPLETAS DE CADA NODO (¡ESTAS SON LAS IMPORTANTES!)
    nodos = [
        ("MELCHIOR-1 (SCIENCE MODULE)", 
         limpiar_texto_para_pdf(m), 
         0, 153, 255),  # Azul
        ("BALTHASAR-2 (MOTHER MODULE)", 
         limpiar_texto_para_pdf(b), 
         0, 255, 200),  # Cian
        ("CASPER-3 (WOMAN MODULE)", 
         limpiar_texto_para_pdf(c), 
         255, 102, 0)   # Naranja
    ]
    
    for nombre, contenido, r, g, b in nodos:
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(r, g, b)
        pdf.cell(0, 10, f"--- {nombre} ---", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 5, contenido)
        pdf.ln(8)
    
    # Decisión final
    pdf.set_font("Courier", "B", 14)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 12, "--- FINAL SYSTEM RESOLUTION ---", ln=True)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(final))
    
    # Estado de votación
    pdf.ln(10)
    pdf.set_font("Courier", "I", 9)
    pdf.set_text_color(100, 100, 100)
    votos = list(st.session_state.magi_states.values())
    pdf.cell(0, 8, f"VOTING RECORD: MELCHIOR: {votos[0]} | BALTHASAR: {votos[1]} | CASPER: {votos[2]}", ln=True)
    pdf.cell(0, 8, f"MAJORITY DECISION: {get_majority_decision().upper()}", ln=True)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

def get_majority_decision():
    """Determina decisión por mayoría (2 de 3)"""
    approvals = sum(1 for state in st.session_state.magi_states.values() if state == "承 認")
    return "APPROVED" if approvals >= 2 else "DENIED"

# --- INTERFAZ PRINCIPAL ---
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Header
st.markdown("# ⬢ MAGI SYSTEM: SUPERCOMPUTING CENTER")
st.markdown("**STATUS:** `OPERATIONAL` | **SYNC:** `99.9%` | **CODE:** `473` | **TOXICITY:** `" + str(st.session_state.toxicity_level) + "%`")

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# TRIUNVIRATO MAGI - Hexágonos
st.markdown("### <span class='kanji'>三賢者の審議</span> - MAGI TRIUMVIRATE DELIBERATION", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    estado_mel = st.session_state.magi_states["MELCHIOR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">MELCHIOR-1</div>
        <div style="color:#888; font-size:0.9rem">SCIENCE MODULE</div>
        <div class="magi-status {'status-approved' if estado_mel == '承 認' else 'status-denied'}">
            {estado_mel}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    estado_bal = st.session_state.magi_states["BALTHASAR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">BALTHASAR-2</div>
        <div style="color:#888; font-size:0.9rem">MOTHER MODULE</div>
        <div class="magi-status {'status-approved' if estado_bal == '承 認' else 'status-denied'}">
            {estado_bal}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    estado_cas = st.session_state.magi_states["CASPER"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">CASPER-3</div>
        <div style="color:#888; font-size:0.9rem">WOMAN MODULE</div>
        <div class="magi-status {'status-approved' if estado_cas == '承 認' else 'status-denied'}">
            {estado_cas}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Panel de decisión con votación visible
decision = get_majority_decision()
decision_class = "decision-approved" if decision == "APPROVED" else "decision-denied"
decision_color = "#00FFC8" if decision == "APPROVED" else "#FF0000"

st.markdown(f"""
<div class="decision-panel {decision_class}">
    <div style="font-size: 1.2rem; color: #aaa; margin-bottom: 10px;">
        SYSTEM VERDICT BASED ON MAJORITY RULE (2/3)
    </div>
    <div class="decision-text" style="color: {decision_color};">
        {decision}
    </div>
    <div style="margin-top: 15px; color: #888; font-size: 0.9rem;">
        VOTING RECORD: 
        <span style="color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000'}">MELCHIOR: {estado_mel}</span> | 
        <span style="color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000'}">BALTHASAR: {estado_bal}</span> | 
        <span style="color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000'}">CASPER: {estado_cas}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# --- SECCIÓN CRÍTICA: RESPUESTAS DE TEXTO PERMANENTES ---
# Estas secciones muestran TODAS las respuestas de texto, no solo la decisión

# Solo mostrar si hay respuestas almacenadas
if (st.session_state.magi_responses["MELCHIOR"] or 
    st.session_state.magi_responses["BALTHASAR"] or 
    st.session_state.magi_responses["CASPER"]):
    
    st.markdown("### 📜 <span class='kanji'>完全な記録</span> - COMPLETE DELIBERATION RECORD", unsafe_allow_html=True)
    st.markdown("*All reasoning and analysis preserved for review*", unsafe_allow_html=True)
    
    # Original Query
    if st.session_state.magi_responses["DILEMA"]:
        st.markdown("#### Original Query")
        st.markdown(f'<div class="visible-text">{st.session_state.magi_responses["DILEMA"]}</div>', unsafe_allow_html=True)
    
    # Tres columnas para las respuestas
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        if st.session_state.magi_responses["MELCHIOR"]:
            st.markdown(f"""
            <div class="response-permanent melchior">
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
            <div class="response-permanent balthasar">
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
            <div class="response-permanent casper">
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
    
    # Resolución final (si existe)
    if st.session_state.magi_responses["FINAL"]:
        st.markdown(f"""
        <div class="response-permanent final">
            <div class="response-title">
                <span style="color: {decision_color}">FINAL SYSTEM RESOLUTION</span>
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

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔐 SYSTEM ACCESS")
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("Secure Link Active")
    else:
        api_key = st.text_input("GROQ API KEY", type="password", key="api_key_input")
    
    if not api_key:
        st.warning("API key required for MAGI consultation")
    
    st.markdown("---")
    
    # Historial de consultas
    st.markdown("### 📊 CONSULTATION HISTORY")
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"Query {len(st.session_state.history)-i}: {entry['timestamp']}"):
                st.write(f"**Input:** {entry['dilema'][:80]}...")
                st.write(f"**Result:** {entry['decision']}")
                if st.button(f"View Details {i}", key=f"view_{i}"):
                    st.session_state.magi_responses["DILEMA"] = entry['dilema']
                    st.session_state.magi_responses["FINAL"] = entry['resolucion']
                    st.session_state.magi_states = entry['states']
                    st.rerun()
    else:
        st.write("No consultation history")
    
    # Controles del sistema
    st.markdown("---")
    st.markdown("### ⚙️ SYSTEM CONTROLS")
    
    if st.button("🔄 Update Toxicity Metrics", use_container_width=True):
        st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + random.randint(5, 20))
        st.rerun()
    
    if st.button("🧹 Clear Current Session", use_container_width=True):
        # Mantener historial pero limpiar respuestas actuales
        st.session_state.magi_responses = {k: "" for k in st.session_state.magi_responses}
        st.session_state.magi_states = {"MELCHIOR": "承 認", "BALTHASAR": "承 認", "CASPER": "承 認"}
        st.rerun()

# --- INPUT PRINCIPAL Y PROCESAMIENTO ---
st.markdown("### <span class='kanji'>質問</span> NEW TACTICAL QUERY")
dilema = st.chat_input("Enter parameters for MAGI deliberation...")

if dilema and api_key:
    # Guardar dilema inmediatamente
    st.session_state.magi_responses["DILEMA"] = dilema
    
    # Actualizar estados aleatoriamente (simulación de votación)
    for magi in st.session_state.magi_states:
        st.session_state.magi_states[magi] = random.choice(["承 認", "否 定"])
    
    st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + 15)
    
    try:
        client = Groq(api_key=api_key)
        
        # Mostrar que se está procesando
        with st.status("🔄 INITIATING MAGI DELIBERATION...", expanded=True) as status:
            st.write("Establishing neural link with MELCHIOR-1...")
            
            # CONSULTA A MELCHIOR
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres MELCHIOR. Analista científico, lógico y frío. Proporciona un análisis objetivo basado en datos y hechos. Sé conciso pero completo."},
                    {"role": "user", "content": dilema}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.1,
                max_tokens=300
            )
            m_resp = completion.choices[0].message.content
            st.session_state.magi_responses["MELCHIOR"] = m_resp
            st.write("✓ MELCHIOR analysis complete")
            time.sleep(0.5)
            
            st.write("Establishing neural link with BALTHASAR-2...")
            # CONSULTA A BALTHASAR
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres BALTHASAR. Analista ético, protector y materno. Considera los aspectos morales, humanos y de protección. Sé conciso pero completo."},
                    {"role": "user", "content": dilema}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=300
            )
            b_resp = completion.choices[0].message.content
            st.session_state.magi_responses["BALTHASAR"] = b_resp
            st.write("✓ BALTHASAR analysis complete")
            time.sleep(0.5)
            
            st.write("Establishing neural link with CASPER-3...")
            # CONSULTA A CASPER
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres CASPER. Analista intuitivo, práctico y egoísta. Considera aspectos prácticos, intuitivos y de interés propio. Sé conciso pero completo."},
                    {"role": "user", "content": dilema}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.9,
                max_tokens=300
            )
            c_resp = completion.choices[0].message.content
            st.session_state.magi_responses["CASPER"] = c_resp
            st.write("✓ CASPER analysis complete")
            time.sleep(0.5)
            
            st.write("Synthesizing final system resolution...")
            # RESOLUCIÓN FINAL
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres el sistema MAGI. Sintetiza una resolución final basada en las tres perspectivas. Considera la mayoría (2/3). Proporciona una decisión clara y razonamiento conciso."},
                    {"role": "user", "content": f"Basado en estas tres perspectivas:\n\nCIENCIA (Melchior): {m_resp[:200]}\n\nÉTICA (Balthasar): {b_resp[:200]}\n\nINTUICIÓN (Casper): {c_resp[:200]}\n\nProporciona la resolución final del sistema MAGI."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=400
            )
            final_resp = completion.choices[0].message.content
            st.session_state.magi_responses["FINAL"] = final_resp
            st.write("✓ Final resolution synthesized")
            
            status.update(label="DELIBERATION COMPLETE - ALL DATA PRESERVED", state="complete", expanded=False)
        
        # Agregar al historial
        st.session_state.history.append({
            "dilema": dilema,
            "resolucion": final_resp,
            "states": st.session_state.magi_states.copy(),
            "decision": decision,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })
        
        # Generar PDF con todas las respuestas
        st.markdown("### 📄 GENERATE COMPLETE REPORT")
        
        with st.spinner("Compiling full deliberation record..."):
            pdf_bytes = crear_pdf(dilema, m_resp, b_resp, c_resp, final_resp)
            
            col_dl1, col_dl2 = st.columns([3, 1])
            
            with col_dl1:
                st.download_button(
                    label="⬇️ DOWNLOAD COMPLETE DELIBERATION REPORT (PDF)",
                    data=pdf_bytes,
                    file_name=f"MAGI_FULL_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    help="Includes all reasoning from all three MAGI nodes"
                )
            
            with col_dl2:
                st.info(f"✅ {len(pdf_bytes):,} bytes")
        
        # Forzar rerun para mostrar las nuevas respuestas
        st.rerun()
        
    except Exception as e:
        st.error(f"System error: {str(e)[:150]}")

elif dilema and not api_key:
    st.error("""
    <div style="background: rgba(255, 0, 0, 0.1); padding: 15px; border: 2px solid #FF0000; border-radius: 3px;">
        <strong style="color: #FF0000;">🔴 SYSTEM OFFLINE</strong><br>
        Valid Groq API key required in sidebar
    </div>
    """, unsafe_allow_html=True)

# Cerrar el contenedor principal
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem; padding: 20px; position: relative; z-index: 1;">
    <span style="color: #00FFC8;">MAGI SYSTEM v3.14</span> | 
    <span style="color: #0099FF;">DELIBERATION ARCHIVE ACTIVE</span> | 
    <span style="color: #ff6600;">PROTOCOL: ENIGMA-473</span><br>
    <span style="font-size: 0.8rem; color: #666;">
    All reasoning preserved | Security: MAXIMUM | Access: RESTRICTED
    </span>
</div>
""", unsafe_allow_html=True)
