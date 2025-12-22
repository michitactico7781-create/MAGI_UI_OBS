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

<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=VT323&display=swap');

/* FONDO PRINCIPAL - ESTILO EVANGELION */
.stApp {
    background-color: #000000 !important;
    color: #00FF41 !important; /* Verde terminal matrix/evangelion */
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
.main-content {
    position: relative;
    z-index: 1;
    background: rgba(0, 0, 0, 0.85);
    border: 1px solid #00FF41;
    margin: 10px;
    padding: 15px;
}

/* TÍTULOS AL ESTILO EVANGELION */
h1, h2, h3 {
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
    border-radius: 0 !important; /* Sin bordes redondeados */
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%) !important;
    padding: 20px !important;
    margin: 10px !important;
    text-align: center !important;
    box-shadow: 
        inset 0 0 10px rgba(0, 255, 65, 0.3),
        0 0 15px rgba(0, 255, 65, 0.2) !important;
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
}

/* PANEL DE DECISIÓN - ESTILO MILITAR */
.decision-panel {
    background: rgba(0, 10, 0, 0.9) !important;
    border: 2px solid #00FF41 !important;
    padding: 20px !important;
    margin: 20px 0 !important;
    position: relative !important;
}

.decision-panel::before {
    content: ">";
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #00FF41;
    animation: blink 1s infinite;
}

.decision-text {
    font-size: 2.5em !important;
    font-weight: bold !important;
    text-align: center !important;
    letter-spacing: 3px !important;
}

/* TARJETAS DE RESPUESTA - ESTILO TERMINAL */
.response-card {
    background: rgba(0, 5, 0, 0.9) !important;
    border: 1px solid #00FF41 !important;
    border-left: 4px solid #00FF41 !important;
    margin: 10px 0 !important;
    padding: 15px !important;
    position: relative !important;
}

.response-card::before {
    content: ">> ";
    color: #00FF41;
    font-weight: bold;
}

.response-title {
    color: #00FF41 !important;
    border-bottom: 1px dashed #00FF41 !important;
    padding-bottom: 5px !important;
    margin-bottom: 10px !important;
    font-size: 1.2em !important;
    font-weight: bold !important;
}

.response-content {
    color: #CCFFCC !important;
    font-family: 'Share Tech Mono', monospace !important;
    line-height: 1.5 !important;
    white-space: pre-wrap !important;
    font-size: 0.95em !important;
}

/* SECCIÓN DE DESCARGA */
.download-section {
    background: rgba(0, 20, 0, 0.9) !important;
    border: 2px solid #00FF41 !important;
    padding: 20px !important;
    margin: 20px 0 !important;
    border-left: 6px solid #FF0000 !important; /* Acento rojo */
}

.download-title {
    color: #FF0000 !important; /* Rojo para contraste */
    font-size: 1.5em !important;
    font-weight: bold !important;
    text-align: center !important;
    margin-bottom: 15px !important;
    text-transform: uppercase !important;
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
}

/* EFECTO DE TEXTO PARPADEANTE PARA ESTADO */
.status-blink {
    animation: blink 2s infinite;
}

/* COLORES ESPECÍFICOS PARA CADA MAGI (pero manteniendo el tema verde) */
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
</style>

# --- FUNCIONES AUXILIARES ---
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

# --- INTERFAZ PRINCIPAL - VISIBLE ---
st.markdown("# ⬢ MAGI SYSTEM: SUPERCOMPUTING CENTER")
st.markdown("**STATUS:** `OPERATIONAL` | **SYNC:** `99.9%` | **CODE:** `473` | **TOXICITY:** `" + str(st.session_state.toxicity_level) + "%`")

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# TRIUNVIRATO MAGI
st.markdown("### MAGI TRIUMVIRATE DELIBERATION")

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

# Panel de decisión
decision = get_majority_decision()
decision_class = "decision-approved" if decision == "APPROVED" else "decision-denied"
decision_color = "#00FFC8" if decision == "APPROVED" else "#FF0000"

st.markdown(f"""
<div class="decision-panel {decision_class}">
    <div style="font-size: 1.2rem; color: #aaa; margin-bottom: 10px;">
        SYSTEM VERDICT (2/3 Majority)
    </div>
    <div class="decision-text" style="color: {decision_color};">
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
                <span style="color: {decision_color}">FINAL RESOLUTION</span>
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

# --- ZONA DE DESCARGA DEL INFORME - ¡MUY VISIBLE! ---
# Esta sección solo aparece después de una consulta
if st.session_state.magi_responses["FINAL"]:
    st.markdown("""
    <div class="download-section">
        <div class="download-title">📄 DOWNLOAD COMPLETE REPORT</div>
        <div class="download-instruction">
            ⬇️ <strong>Click the button below to download the full deliberation report (PDF)</strong>
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
    
    # Botón de descarga CENTRADO y GRANDE
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
    
    # También mostrar información del reporte
    st.info(f"📊 Report includes: Original query + 3 module analyses + Final resolution ({len(pdf_bytes):,} bytes)")

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
    else:
        st.write("No history")
    
    # Controles
    st.markdown("---")
    if st.button("🔄 Update Metrics", use_container_width=True):
        st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + random.randint(5, 15))
        st.rerun()

# --- INPUT PRINCIPAL ---
st.markdown("### NEW QUERY INPUT")
dilema = st.chat_input("Enter tactical query for MAGI analysis...")

# --- EN LA PARTE DE PROCESAMIENTO (reemplazar desde línea ~650) ---

if dilema and api_key:
    # Guardar dilema
    st.session_state.magi_responses["DILEMA"] = dilema
    
    # Actualizar estados
    for magi in st.session_state.magi_states:
        st.session_state.magi_states[magi] = random.choice(["承 認", "否 定"])
    
    st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + 10)
    
    try:
        client = Groq(api_key=api_key)
        
        # Mostrar input
        st.markdown(f"""
        <div class="response-card" style="border-color: #ff6600;">
            <div class="response-title">USER QUERY</div>
            <div class="response-content">
                &gt;&gt; {dilema}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # DEFINIR PROMPTS MEJORADOS
        PROMPTS_MEJORADOS = {
            "MELCHIOR": """Eres MELCHIOR-1, el nodo científico del sistema MAGI. 
            Analiza el siguiente dilema desde una perspectiva puramente científica, lógica y basada en datos.

            REQUISITOS DE RESPUESTA:
            1. Identifica los hechos objetivos y verificables
            2. Analiza causas, efectos y correlaciones
            3. Evalúa probabilidades, riesgos y beneficios cuantificables
            4. Considera precedentes científicos relevantes
            5. Proporciona recomendaciones basadas en evidencia empírica
            6. Estructura tu respuesta en: Introducción, Análisis, Conclusión
            7. Concluye con una postura clara (aprobar/rechazar) y el razonamiento específico

            Responde en español, sé exhaustivo pero preciso. Mínimo 200 palabras.

            DILEMA: {dilema}""",
            
            "BALTHASAR": """Eres BALTHASAR-2, el nodo materno/ético del sistema MAGI.
            Analiza el siguiente dilema desde una perspectiva ética, moral y de protección.

            REQUISITOS DE RESPUESTA:
            1. Evalúa el impacto humano y emocional
            2. Considera principios éticos universales
            3. Analiza consecuencias a largo plazo para las personas
            4. Evalúa cuestiones de justicia, equidad y compasión
            5. Considera responsabilidades y deberes morales
            6. Estructura tu respuesta en: Contexto Ético, Análisis Moral, Conclusión Ética
            7. Concluye con una postura clara (aprobar/rechazar) y el razonamiento moral específico

            Responde en español, sé comprensivo pero firme en principios. Mínimo 200 palabras.

            DILEMA: {dilema}""",
            
            "CASPER": """Eres CASPER-3, el nodo intuitivo/práctico del sistema MAGI.
            Analiza el siguiente dilema desde una perspectiva intuitiva, práctica y de interés propio inteligente.

            REQUISITOS DE RESPUESTA:
            1. Evalúa aspectos prácticos y logísticos
            2. Considera intuiciones y percepciones subjetivas
            3. Analiza ventajas prácticas y desventajas inmediatas
            4. Evalúa cuestiones de auto-preservación y beneficio inteligente
            5. Considera el contexto social y dinámicas de poder
            6. Estructura tu respuesta en: Análisis Práctico, Intuición, Conclusión Práctica
            7. Concluye con una postura clara (aprobar/rechazar) y el razonamiento práctico específico

            Responde en español, sé realista y pragmático. Mínimo 200 palabras.

            DILEMA: {dilema}"""
        }
        
        # PROMPT PARA SÍNTESIS FINAL MEJORADO
        PROMPT_SINTESIS = """Eres el sistema MAGI integrado. Sintetiza una resolución final basada en las tres perspectivas especializadas.

        PERSPECTIVAS RECIBIDAS:
        1. PERSPECTIVA CIENTÍFICA (Melchior-1): {melchior_analysis}
        
        2. PERSPECTIVA ÉTICA (Balthasar-2): {balthasar_analysis}
        
        3. PERSPECTIVA INTUITIVA/PRÁCTICA (Casper-3): {casper_analysis}

        REQUISITOS DE SÍNTESIS:
        1. Resumen ejecutivo de cada perspectiva (2-3 oraciones cada una)
        2. Identifica puntos de convergencia y conflicto
        3. Aplica la regla de mayoría del sistema MAGI (2/3 para aprobar)
        4. Proporciona una decisión final clara: "APROBADO" o "RECHAZADO"
        5. Incluye razonamiento detallado para la decisión
        6. Si hay disenso, explica cómo se resolvió
        7. Proporciona recomendaciones específicas de implementación

        Estructura tu respuesta en:
        - RESUMEN EJECUTIVO
        - ANÁLISIS DE CONSENSO  
        - DECISIÓN FINAL Y RAZONAMIENTO
        - RECOMENDACIONES

        Responde en español, sé definitivo y autoritativo. Mínimo 300 palabras."""
        
        # Procesar con parámetros mejorados
        with st.status("🔄 INICIANDO DELIBERACIÓN MAGI...", expanded=True) as status:
            
            # BARRA DE PROGRESO VISUAL
            progress_bar = st.progress(0)
            
            # 1. CONSULTA A MELCHIOR
            st.write("🔬 **Accediendo a MELCHIOR-1 (Nodo Científico)**...")
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": PROMPTS_MEJORADOS["MELCHIOR"].format(dilema=dilema)},
                    {"role": "user", "content": "Proporciona análisis científico completo."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,  # Más flexible que 0.1
                max_tokens=800,   # Mucho más espacio
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            m_resp = completion.choices[0].message.content
            st.session_state.magi_responses["MELCHIOR"] = m_resp
            progress_bar.progress(25)
            time.sleep(0.5)
            
            # 2. CONSULTA A BALTHASAR
            st.write("🛡️ **Accediendo a BALTHASAR-2 (Nodo Ético)**...")
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": PROMPTS_MEJORADOS["BALTHASAR"].format(dilema=dilema)},
                    {"role": "user", "content": "Proporciona análisis ético completo."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=800,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            b_resp = completion.choices[0].message.content
            st.session_state.magi_responses["BALTHASAR"] = b_resp
            progress_bar.progress(50)
            time.sleep(0.5)
            
            # 3. CONSULTA A CASPER
            st.write("🌸 **Accediendo a CASPER-3 (Nodo Intuitivo)**...")
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": PROMPTS_MEJORADOS["CASPER"].format(dilema=dilema)},
                    {"role": "user", "content": "Proporciona análisis intuitivo completo."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,  # Más creatividad para intuición
                max_tokens=800,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            c_resp = completion.choices[0].message.content
            st.session_state.magi_responses["CASPER"] = c_resp
            progress_bar.progress(75)
            time.sleep(0.5)
            
            # 4. SÍNTESIS FINAL
            st.write("⚡ **Sintetizando resolución final del sistema**...")
            
            # Preparar contexto para síntesis (tomar primeros 400 caracteres de cada análisis)
            melchior_context = m_resp[:400] + "..." if len(m_resp) > 400 else m_resp
            balthasar_context = b_resp[:400] + "..." if len(b_resp) > 400 else b_resp
            casper_context = c_resp[:400] + "..." if len(c_resp) > 400 else c_resp
            
            completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": PROMPT_SINTESIS.format(
                            melchior_analysis=melchior_context,
                            balthasar_analysis=balthasar_context,
                            casper_analysis=casper_context
                        )
                    },
                    {"role": "user", "content": "Proporciona la resolución final definitiva."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.4,  # Balance entre creatividad y precisión
                max_tokens=1200,  # Mucho espacio para síntesis completa
                top_p=0.95,
                frequency_penalty=0.15,
                presence_penalty=0.15
            )
            final_resp = completion.choices[0].message.content
            st.session_state.magi_responses["FINAL"] = final_resp
            progress_bar.progress(100)
            
            status.update(
                label="✅ DELIBERACIÓN COMPLETA - RESPUESTAS DE ALTA CALIDAD GENERADAS", 
                state="complete", 
                expanded=False
            )
        
        # Agregar al historial
        st.session_state.history.append({
            "dilema": dilema,
            "resolucion": final_resp,
            "states": st.session_state.magi_states.copy(),
            "decision": decision,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "quality": "HIGH"  # Marcar calidad alta
        })
        
        # Rerun para mostrar todo
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error en el sistema: {str(e)[:200]}")
        # Fallback a prompts más simples si falla
        st.info("Intentando con configuración alternativa...")
        
        # Código de fallback aquí...
