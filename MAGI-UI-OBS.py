import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime
import time
import unicodedata
from io import BytesIO
import random

# --- CONFIGURACIÓN E HISTORIAL ---
if "history" not in st.session_state:
    st.session_state.history = []

if "toxicity_level" not in st.session_state:
    st.session_state.toxicity_level = 30

if "magi_states" not in st.session_state:
    st.session_state.magi_states = {"MELCHIOR": "承 認", "BALTHASAR": "承 認", "CASPER": "承 認"}

def add_to_history(dilema, final):
    st.session_state.history.append({
        "dilema": dilema, 
        "resolucion": final,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    })

def update_toxicity():
    """Actualiza el nivel de toxicidad mental"""
    st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + random.randint(5, 15))

def get_majority_decision():
    """Determina decisión por mayoría (2 de 3)"""
    approvals = sum(1 for state in st.session_state.magi_states.values() if state == "承 認")
    return "APPROVED" if approvals >= 2 else "DENIED"

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="MAGI SYSTEM: SUPERCOMPUTING CENTER",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS MEJORADO (Fiel a descripción Gemini) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');
    
    /* FONDO Y GENERAL - Mejorado con elementos de referencia */
    .stApp {
        background-color: #050505;
        color: #ff6600;
        font-family: 'Orbitron', 'Share Tech Mono', monospace;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Patrón de hexágonos en fondo (Honeycomb pattern) */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(255, 102, 0, 0.03) 1px, transparent 2px),
            radial-gradient(circle at 75% 75%, rgba(0, 255, 200, 0.02) 1px, transparent 2px);
        background-size: 80px 80px;
        z-index: -1;
        opacity: 0.4;
    }
    
    /* Líneas de escaneo CRT */
    .stApp::after {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            to bottom,
            transparent 50%,
            rgba(0, 255, 200, 0.03) 50%
        );
        background-size: 100% 4px;
        z-index: -1;
        pointer-events: none;
        animation: scanline 10s linear infinite;
    }
    
    @keyframes scanline {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100%); }
    }
    
    /* TEXTOS - Mejor tipografía */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        color: #ff6600 !important;
        text-shadow: 0 0 10px rgba(255, 102, 0, 0.7);
        letter-spacing: 2px;
    }
    
    .kanji-text {
        font-family: 'MS Gothic', 'MS Mincho', monospace;
        font-weight: bold;
        color: #00FFC8;
    }
    
    .warning-text {
        color: #FF0000 !important;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    
    /* HEXAGONOS MAGI - Diseño trapezoidal */
    .magi-hexagon {
        position: relative;
        width: 100%;
        height: 200px;
        background: linear-gradient(135deg, rgba(0, 153, 255, 0.1), rgba(0, 153, 255, 0.3));
        clip-path: polygon(20% 0%, 80% 0%, 100% 50%, 80% 100%, 20% 100%, 0% 50%);
        border: 2px solid #0099FF;
        margin: 20px 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 153, 255, 0.5);
    }
    
    .magi-hexagon:hover {
        box-shadow: 0 0 30px rgba(0, 153, 255, 0.8);
        transform: translateY(-5px);
    }
    
    .magi-hexagon.approved {
        border-color: #00FFC8;
        box-shadow: 0 0 25px rgba(0, 255, 200, 0.6);
    }
    
    .magi-hexagon.denied {
        border-color: #FF0000;
        box-shadow: 0 0 25px rgba(255, 0, 0, 0.6);
    }
    
    .magi-status {
        font-size: 2.5rem;
        font-weight: bold;
        margin-top: 10px;
    }
    
    .status-approved {
        color: #00FFC8;
        text-shadow: 0 0 15px rgba(0, 255, 200, 0.8);
    }
    
    .status-denied {
        color: #FF0000;
        text-shadow: 0 0 15px rgba(255, 0, 0, 0.8);
    }
    
    /* BARRAS DE TOXICIDAD */
    .toxicity-container {
        background: rgba(0, 20, 40, 0.7);
        border: 1px solid #0099FF;
        padding: 20px;
        margin: 20px 0;
        border-radius: 5px;
    }
    
    .toxicity-bar {
        height: 30px;
        background: linear-gradient(90deg, #00FFC8, #0099FF, #7D00FF);
        margin: 5px 0;
        border-radius: 3px;
        transition: width 0.5s ease;
        box-shadow: 0 0 10px rgba(0, 255, 200, 0.3);
    }
    
    /* TARJETAS DE LOS NODOS - Versión mejorada */
    .magi-card {
        border: 2px solid #ff6600;
        background: linear-gradient(145deg, rgba(20, 10, 0, 0.9), rgba(40, 20, 0, 0.7));
        padding: 25px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 25px rgba(255, 102, 0, 0.3);
    }
    
    .magi-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 102, 0, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .node-title {
        font-size: 1.8em;
        border-bottom: 2px solid #ff6600;
        margin-bottom: 15px;
        letter-spacing: 3px;
        text-align: center;
        font-weight: 900;
        text-transform: uppercase;
        padding-bottom: 10px;
    }
    
    /* LÍNEA DECORATIVA MEJORADA */
    .deco-line {
        height: 3px;
        background: linear-gradient(90deg, 
            transparent, 
            #ff6600 20%, 
            #00FFC8 50%, 
            #ff6600 80%, 
            transparent
        );
        margin: 30px 0;
        opacity: 0.8;
    }
    
    /* BOTONES MEJORADOS */
    .stButton > button {
        border: 2px solid #ff6600;
        background: linear-gradient(145deg, rgba(255, 102, 0, 0.1), rgba(255, 102, 0, 0.3));
        color: #ff6600 !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        border-radius: 0;
        transition: all 0.3s;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 12px 24px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(145deg, #ff6600, #ff8533);
        color: black !important;
        box-shadow: 0 0 25px #ff6600;
        transform: translateY(-2px);
    }
    
    /* INPUTS MEJORADOS */
    .stTextInput > div > div > input,
    .stChatInput > div > div > textarea {
        background-color: rgba(10, 10, 10, 0.9) !important;
        color: #ff6600 !important;
        border: 2px solid #ff6600 !important;
        font-family: 'Share Tech Mono', monospace !important;
        border-radius: 0 !important;
        font-size: 1.1rem !important;
        letter-spacing: 1px;
    }
    
    .stChatInput > div > div > textarea::placeholder {
        color: #ff660066 !important;
        font-style: italic;
    }
    
    /* STATUS INDICATORS */
    .status-indicator {
        display: inline-block;
        padding: 5px 15px;
        margin: 0 10px;
        border-radius: 3px;
        font-weight: bold;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
    }
    
    .status-online {
        background: rgba(0, 255, 200, 0.2);
        border: 1px solid #00FFC8;
        color: #00FFC8;
    }
    
    .status-warning {
        background: rgba(255, 0, 0, 0.2);
        border: 1px solid #FF0000;
        color: #FF0000;
        animation: blink 1s infinite;
    }
    
    /* PANEL DE DECISIÓN */
    .decision-panel {
        background: linear-gradient(145deg, rgba(0, 20, 40, 0.9), rgba(0, 40, 60, 0.7));
        border: 2px solid #0099FF;
        padding: 25px;
        margin: 30px 0;
        position: relative;
        overflow: hidden;
    }
    
    .decision-panel::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #ff6600, #00FFC8, #0099FF);
    }
    
    /* Cursor parpadeante */
    .blinking-cursor {
        display: inline-block;
        width: 10px;
        height: 1.2em;
        background-color: #ff6600;
        margin-left: 5px;
        animation: blink 1s infinite;
        vertical-align: middle;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES ---

def stream_data(text, speed=0.02):
    """Efecto de escritura terminal con delay aleatorio"""
    words = text.split(" ")
    for word in words:
        yield word + " "
        time.sleep(speed + random.uniform(0, 0.01))  # Variación aleatoria

def limpiar_texto_para_pdf(texto):
    """Limpia texto para compatibilidad con FPDF"""
    if not texto:
        return ""
    
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N',
        '¿': '?', '¡': '!',
        '—': '-', '–': '-', '…': '...',
        '«': '"', '»': '"', '「': '"', '」': '"',
    }
    
    for char, repl in reemplazos.items():
        texto = texto.replace(char, repl)
    
    try:
        texto = unicodedata.normalize('NFKD', texto)
        texto = texto.encode('ascii', 'ignore').decode('ascii')
    except:
        texto = ''.join(c if 32 <= ord(c) < 127 else '?' for c in texto)
    
    if len(texto) > 1000:
        texto = texto[:1000] + "\n[...CONTINUED...]"
    
    return texto

def crear_pdf_mejorado(dilema, m, b, c, final):
    """Generador de Reportes NERV - Versión mejorada"""
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Encabezado con diseño profesional
        pdf.set_font("Courier", "B", 20)
        pdf.set_text_color(255, 102, 0)  # Naranja principal
        pdf.cell(0, 15, "▌ MAGI SYSTEM - CLASSIFIED REPORT ▌", ln=True, align='C')
        
        # Información del sistema
        pdf.set_font("Courier", "B", 10)
        pdf.set_text_color(0, 153, 255)  # Azul eléctrico
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(0, 8, f"CODE: 473 | PRIORITY: AAA | FILE: MAGI_SYS", ln=True)
        pdf.cell(0, 8, f"TIMESTAMP: {fecha}", ln=True)
        pdf.cell(0, 8, f"SECURITY LEVEL: MAXIMUM", ln=True)
        
        pdf.ln(10)
        
        # Línea divisoria
        pdf.set_draw_color(255, 102, 0)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(15)
        
        # Sección de pregunta
        pdf.set_font("Courier", "B", 12)
        pdf.set_text_color(255, 102, 0)
        pdf.cell(0, 10, "質問 (QUESTION):", ln=True)
        pdf.set_font("Courier", "", 10)
        pdf.set_text_color(200, 200, 200)
        pdf.multi_cell(0, 6, limpiar_texto_para_pdf(dilema)[:400])
        pdf.ln(10)
        
        # Deliberación del Triunvirato
        pdf.set_font("Courier", "B", 14)
        pdf.set_text_color(0, 255, 200)  # Verde neón
        pdf.cell(0, 12, "▌ MAGI TRIUMVIRATE DELIBERATION ▌", ln=True)
        pdf.ln(8)
        
        # Respuestas de cada nodo
        nodos = [
            ("MELCHIOR-1 (SCIENCE)", m, 0, 153, 255),
            ("BALTHASAR-2 (MOTHER)", b, 255, 102, 0),
            ("CASPER-3 (WOMAN)", c, 0, 255, 200)
        ]
        
        for nombre, contenido, r, g, b_color in nodos:
            pdf.set_font("Courier", "B", 11)
            pdf.set_text_color(r, g, b_color)
            pdf.cell(0, 10, f"» {nombre}", ln=True)
            pdf.set_font("Courier", "", 9)
            pdf.set_text_color(180, 180, 180)
            contenido_limpio = limpiar_texto_para_pdf(contenido)
            pdf.multi_cell(0, 5, contenido_limpio[:600])
            pdf.ln(5)
        
        # Línea divisoria final
        pdf.set_draw_color(255, 0, 0)
        pdf.set_line_width(0.8)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(15)
        
        # Decisión final
        pdf.set_font("Courier", "B", 16)
        pdf.set_text_color(255, 0, 0)  # Rojo de alerta
        pdf.cell(0, 12, "解決 (SOLUTION):", ln=True)
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(255, 255, 255)
        final_limpio = limpiar_texto_para_pdf(final)
        pdf.multi_cell(0, 7, final_limpio[:800])
        
        # Estado del sistema
        pdf.ln(15)
        pdf.set_font("Courier", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 8, f"MENTAL TOXICITY LEVEL: {st.session_state.toxicity_level}%", ln=True)
        pdf.cell(0, 8, f"SYNCHRONIZATION: 99.9% | DECISION: {get_majority_decision()}", ln=True)
        
        # Pie de página
        pdf.set_y(-30)
        pdf.set_font("Courier", "I", 8)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 10, "CLASSIFIED - NERV EYES ONLY - UNAUTHORIZED ACCESS: TERMINATION", ln=True, align='C')
        
        return pdf.output(dest='S').encode('latin-1', 'ignore')
        
    except Exception as e:
        st.error(f"PDF Error: {str(e)[:100]}")
        # Fallback simple
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Courier", "B", 16)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "MAGI SYSTEM REPORT", ln=True)
        pdf.set_font("Courier", "", 10)
        pdf.multi_cell(0, 6, f"Input: {dilema[:200]}\n\nFinal: {final[:500]}")
        return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- INTERFAZ PRINCIPAL MEJORADA ---

# Header con elementos de referencia
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.markdown("""
    <div style="text-align: left;">
        <h1 style="margin-bottom: 5px;">⬢ MAGI SYSTEM</h1>
        <div style="display: flex; gap: 15px; align-items: center;">
            <span class="status-indicator status-online">ONLINE</span>
            <span class="status-indicator status-warning">PROTOCOL 473</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="text-align: center;">
        <div style="font-size: 3rem; font-weight: 900; color: #ff6600; text-shadow: 0 0 20px #ff6600;">
            CODE:473
        </div>
        <div style="color: #00FFC8; font-family: 'Orbitron'; font-size: 0.9rem;">
            PRIORITY: AAA
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div style="text-align: right;">
        <div style="font-family: 'Orbitron'; font-size: 1.2rem; color: #0099FF;">
            {datetime.datetime.now().strftime("YY%y-%m-%d")}
        </div>
        <div style="font-family: 'Digital-7', monospace; font-size: 1.5rem; color: #00FFC8;">
            {current_time}
        </div>
        <div style="color: #888; font-size: 0.9rem;">
            SUPERCOMPUTING CENTER
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# --- TRIUNVIRATO MAGI (Elemento central) ---
st.markdown("### <span class='kanji-text'>三賢者の審議</span> - MAGI TRIUMVIRATE", unsafe_allow_html=True)

# Mostrar hexágonos de los nodos MAGI
col_mel, col_bal, col_cas = st.columns(3)

with col_mel:
    estado_mel = st.session_state.magi_states["MELCHIOR"]
    clase_estado = "approved" if estado_mel == "承 認" else "denied"
    st.markdown(f"""
    <div class="magi-hexagon {clase_estado}">
        <div style="font-size: 1.5rem; color: #0099FF; font-weight: bold;">MELCHIOR-1</div>
        <div style="color: #aaa; font-size: 0.9rem;">SCIENCE MODULE</div>
        <div class="magi-status {'status-approved' if estado_mel == '承 認' else 'status-denied'}">
            {estado_mel}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_bal:
    estado_bal = st.session_state.magi_states["BALTHASAR"]
    clase_estado = "approved" if estado_bal == "承 認" else "denied"
    st.markdown(f"""
    <div class="magi-hexagon {clase_estado}">
        <div style="font-size: 1.5rem; color: #0099FF; font-weight: bold;">BALTHASAR-2</div>
        <div style="color: #aaa; font-size: 0.9rem;">MOTHER MODULE</div>
        <div class="magi-status {'status-approved' if estado_bal == '承 認' else 'status-denied'}">
            {estado_bal}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_cas:
    estado_cas = st.session_state.magi_states["CASPER"]
    clase_estado = "approved" if estado_cas == "承 認" else "denied"
    st.markdown(f"""
    <div class="magi-hexagon {clase_estado}">
        <div style="font-size: 1.5rem; color: #0099FF; font-weight: bold;">CASPER-3</div>
        <div style="color: #aaa; font-size: 0.9rem;">WOMAN MODULE</div>
        <div class="magi-status {'status-approved' if estado_cas == '承 認' else 'status-denied'}">
            {estado_cas}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Panel de decisión
decision = get_majority_decision()
color_decision = "#00FFC8" if decision == "APPROVED" else "#FF0000"
st.markdown(f"""
<div class="decision-panel">
    <div style="text-align: center; margin-bottom: 15px;">
        <span style="font-size: 1.1rem; color: #aaa;">DELIBERATION STATUS:</span>
        <span style="font-size: 1.8rem; font-weight: 900; color: {color_decision}; margin-left: 15px;">
            {decision}
        </span>
    </div>
    <div style="text-align: center; color: #888; font-size: 0.9rem;">
        MAJORITY RULE: 2/3 REQUIRED FOR APPROVAL
    </div>
</div>
""", unsafe_allow_html=True)

# --- BARRAS DE TOXICIDAD MENTAL ---
st.markdown("### <span class='warning-text'>⚠</span> MENTAL TOXICITY METRICS", unsafe_allow_html=True)

st.markdown(f"""
<div class="toxicity-container">
    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
        <span style="color: #00FFC8;">SYSTEM LOAD</span>
        <span style="color: #ff6600; font-family: 'Orbitron';">{st.session_state.toxicity_level}%</span>
    </div>
    <div class="toxicity-bar" style="width: {st.session_state.toxicity_level}%;"></div>
    
    <div style="display: grid; grid-template-columns: repeat(10, 1fr); gap: 5px; margin-top: 20px;">
        {"".join([f'<div style="height: {random.randint(10, 40)}px; background: linear-gradient(to top, #00FFC8, #0099FF, #7D00FF); opacity: {random.uniform(0.3, 0.9)}; border-radius: 2px;"></div>' 
          for _ in range(30)])}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# --- SIDEBAR CON INFORMACIÓN DEL SISTEMA ---
with st.sidebar:
    st.markdown("### <span class='kanji-text'>情報</span> SYSTEM INFO", unsafe_allow_html=True)
    
    # API Key
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("🔗 SECURE LINK ESTABLISHED")
    else:
        api_key = st.text_input("CLAVE API (Groq)", type="password", key="api_key_input")
    
    if not api_key:
        st.warning("⚠️ API KEY REQUIRED")
    
    st.markdown("---")
    
    # Estado del sistema
    st.markdown("#### SYSTEM STATUS")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("SYNC RATE", "99.9%", "0.1%")
    with col_stat2:
        st.metric("ERRORS", "0", "0")
    
    st.markdown("---")
    
    # Historial
    st.markdown("#### <span class='kanji-text'>記録</span> RECENT LOGS")
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history[-3:])):
            with st.expander(f"[{entry['timestamp']}] {entry['dilema'][:30]}..."):
                st.write(entry['resolucion'][:150] + "...")
    else:
        st.write("No logs available")
    
    # Botón para actualizar toxicidad
    if st.button("UPDATE METRICS", use_container_width=True):
        update_toxicity()
        st.rerun()

# --- INPUT PRINCIPAL ---
st.markdown("### <span class='kanji-text'>質問</span> TACTICAL INPUT QUERY")
st.markdown('<div class="blinking-cursor"></div>', unsafe_allow_html=True)

dilema = st.chat_input("ENTER TACTICAL PARAMETERS...")

if dilema and api_key:
    # Actualizar estados aleatoriamente para simular deliberación
    for magi in st.session_state.magi_states:
        st.session_state.magi_states[magi] = random.choice(["承 認", "否 定"])
    
    update_toxicity()
    
    try:
        client = Groq(api_key=api_key)
        
        # Mostrar input con estilo
        st.markdown(f"""
        <div class="magi-card">
            <div class="node-title">USER QUERY</div>
            <div style="color: #00FFC8; font-size: 1.1rem; border-left: 3px solid #ff6600; padding-left: 15px;">
                &gt;&gt; {dilema}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        def consultar_magi(prompt_system, temp):
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": dilema}
                ],
                model="llama-3.3-70b-versatile",
                temperature=temp,
                max_tokens=200
            )
            return completion.choices[0].message.content
        
        # Procesamiento con animación
        with st.status("INITIATING NEURAL LINK...", expanded=True) as status:
            time.sleep(0.5)
            st.write("ACCESSING MELCHIOR-1...")
            m_resp = consultar_magi("Eres MELCHIOR. Científico, lógico, frío. Analiza desde perspectiva científica. Máximo 100 palabras.", 0.1)
            time.sleep(0.3)
            
            st.write("ACCESSING BALTHASAR-2...")
            b_resp = consultar_magi("Eres BALTHASAR. Madre, protectora, ética. Analiza desde perspectiva moral y protectora. Máximo 100 palabras.", 0.5)
            time.sleep(0.3)
            
            st.write("ACCESSING CASPER-3...")
            c_resp = consultar_magi("Eres CASPER. Mujer, intuitiva, egoísta. Analiza desde perspectiva intuitiva y práctica. Máximo 100 palabras.", 0.9)
            time.sleep(0.3)
            
            st.write("SYNTHESIZING FINAL RESOLUTION...")
            final_resp = consultar_magi(f"Como sistema MAGI, proporciona una resolución final concisa (máximo 150 palabras) basada en: Ciencia:{m_resp[:100]}, Ética:{b_resp[:100]}, Intuición:{c_resp[:100]}", 0.3)
            
            status.update(label="DELIBERATION COMPLETE", state="complete", expanded=False)
        
        # Mostrar respuestas
        st.markdown("### <span class='kanji-text'>回答</span> MODULE RESPONSES")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.markdown('<div class="magi-card"><div class="node-title">MELCHIOR-1</div><div style="color:#888; text-align:center;">SCIENCE</div></div>', unsafe_allow_html=True)
            st.write_stream(stream_data(m_resp))
        
        with col_res2:
            st.markdown('<div class="magi-card"><div class="node-title">BALTHASAR-2</div><div style="color:#888; text-align:center;">MOTHER</div></div>', unsafe_allow_html=True)
            st.write_stream(stream_data(b_resp))
        
        with col_res3:
            st.markdown('<div class="magi-card"><div class="node-title">CASPER-3</div><div style="color:#888; text-align:center;">WOMAN</div></div>', unsafe_allow_html=True)
            st.write_stream(stream_data(c_resp))
        
        st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
        
        # Resolución final
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, rgba(255, 102, 0, 0.1), rgba(255, 0, 0, 0.05)); 
                    padding: 25px; border-left: 5px solid #ff6600; margin: 30px 0;">
            <h3 style="color: #ff6600; margin-bottom: 15px;">
                <span class='kanji-text'>解決</span> FINAL SYSTEM RESOLUTION
            </h3>
            <div style="color: #fff; line-height: 1.6; font-size: 1.1rem;">
        """, unsafe_allow_html=True)
        
        st.write_stream(stream_data(final_resp, 0.03))
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Agregar al historial
        add_to_history(dilema, final_resp)
        
        # Generar PDF
        st.markdown("### <span class='kanji-text'>報告</span> CLASSIFIED REPORT")
        
        with st.spinner("GENERATING OFFICIAL DOCUMENTATION..."):
            pdf_bytes = crear_pdf_mejorado(dilema, m_resp, b_resp, c_resp, final_resp)
            
            col_pdf1, col_pdf2 = st.columns([3, 1])
            
            with col_pdf1:
                st.download_button(
                    label="📄 DOWNLOAD CLASSIFIED REPORT (PDF)",
                    data=pdf_bytes,
                    file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            with col_pdf2:
                # Vista previa
                with st.expander("PREVIEW"):
                    st.text(f"""
                    MAGI SYSTEM - EXECUTIVE SUMMARY
                    {'='*40}
                    Decision: {decision}
                    Toxicity: {st.session_state.toxicity_level}%
                    
                    Final Resolution:
                    {final_resp[:200]}...
                    """)
        
        # Rerun para actualizar UI
        st.rerun()
        
    except Exception as e:
        st.error(f"SYSTEM ERROR: {str(e)[:150]}")
        st.info("Check API key and connection stability.")

elif dilema and not api_key:
    st.error("""
    <div style="background: rgba(255, 0, 0, 0.1); padding: 20px; border: 2px solid #FF0000;">
        <h3 style="color: #FF0000;">🔴 SYSTEM OFFLINE</h3>
        <p>API KEY REQUIRED FOR NEURAL LINK ACTIVATION</p>
        <p style="color: #aaa; font-size: 0.9rem;">Enter valid Groq API key in sidebar</p>
    </div>
    """, unsafe_allow_html=True)

# Footer del sistema
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem; padding: 20px;">
    <span style="color: #00FFC8;">MAGI SYSTEM v3.14</span> | 
    <span style="color: #0099FF;">SUPERCOMPUTING CENTER</span> | 
    <span style="color: #ff6600;">PROTOCOL: ENIGMA-473</span><br>
    <span style="font-size: 0.8rem; color: #666;">
    FILE: MAGI_SYS | ACCESS: RESTRICTED | SECURITY: MAXIMUM
    </span>
</div>
""", unsafe_allow_html=True)
