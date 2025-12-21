import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime
import time
import base64
from io import BytesIO

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="MAGI SYSTEM: SUPERCOMPUTING CENTER",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS FIEL A LAS IMÁGENES (MATRIX/Terminal) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    /* FONDO MATRIX */
    .stApp {
        background-color: #0a0a0a;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
    }
    
    /* HEADER CON CÓDIGO 473 */
    .magi-header {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        padding: 15px 0;
        border-bottom: 1px solid #008f11;
        margin-bottom: 20px;
    }
    
    .system-title {
        font-size: 1.5rem;
        font-weight: bold;
        letter-spacing: 2px;
        color: #00ff41;
        text-shadow: 0 0 10px #00ff41;
    }
    
    .system-code {
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #ff003c;
        letter-spacing: 5px;
    }
    
    .system-time {
        text-align: right;
        font-size: 1.1rem;
        color: #aaaaaa;
    }
    
    /* PANELES TERMINAL */
    .terminal-panel {
        border: 1px solid #008f11;
        background-color: rgba(0, 20, 0, 0.8);
        padding: 20px;
        margin-bottom: 20px;
        position: relative;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
    }
    
    .panel-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 15px;
        padding-bottom: 5px;
        border-bottom: 1px solid #008f11;
        color: #ffcc00;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* MAGI UNITS GRID */
    .magi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .magi-unit {
        border: 1px solid #008f11;
        background-color: rgba(0, 30, 0, 0.5);
        padding: 15px;
        text-align: center;
    }
    
    .magi-name {
        font-size: 1.3rem;
        font-weight: bold;
        color: #00a2ff;
        margin-bottom: 5px;
    }
    
    .magi-code {
        font-size: 1.8rem;
        font-weight: bold;
        color: #ff003c;
        letter-spacing: 3px;
    }
    
    .magi-desc {
        font-size: 0.9rem;
        color: #888;
        margin-top: 10px;
        line-height: 1.3;
    }
    
    /* BOTONES SISTEMA */
    .stButton > button {
        border: 1px solid #00ff41;
        background-color: rgba(0, 40, 0, 0.8);
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        font-weight: bold;
        border-radius: 0;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background-color: rgba(0, 255, 65, 0.2);
        box-shadow: 0 0 10px #00ff41;
        color: white;
    }
    
    /* INPUTS TERMINAL */
    .stTextInput > div > div > input {
        background-color: rgba(0, 20, 0, 0.8);
        color: #00ff41;
        border: 1px solid #008f11;
        font-family: 'Share Tech Mono', monospace;
        border-radius: 0;
    }
    
    /* CHAT INPUT ESPECIAL */
    .stChatInput > div > div > textarea {
        background-color: rgba(0, 20, 0, 0.8) !important;
        color: #00ff41 !important;
        border: 1px solid #008f11 !important;
        font-family: 'Share Tech Mono', monospace !important;
        border-radius: 0 !important;
    }
    
    /* SCROLLBAR */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 20, 0, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: #008f11;
    }
    
    /* DATA DISPLAY (CONSOLA) */
    .data-display {
        background-color: rgba(0, 0, 0, 0.7);
        border-left: 3px solid #00ff41;
        padding: 15px;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        color: #aaa;
        font-size: 0.95rem;
        line-height: 1.5;
        max-height: 300px;
        overflow-y: auto;
    }
    
    /* STATUS INDICATORS */
    .status-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 20px 0;
        padding: 15px;
        background-color: rgba(0, 20, 0, 0.5);
        border: 1px solid #008f11;
    }
    
    .status-item {
        text-align: center;
    }
    
    .status-label {
        font-size: 0.9rem;
        color: #888;
        margin-bottom: 5px;
    }
    
    .status-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #00ff41;
    }
    
    /* NEURAL LINK SECTION */
    .neural-link {
        background-color: rgba(0, 0, 30, 0.7);
        border: 1px solid #00a2ff;
        padding: 15px;
        margin: 15px 0;
    }
    
    .neural-title {
        color: #00a2ff;
        font-size: 1.3rem;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* RESOLUTION SYSTEM */
    .resolution-box {
        background-color: rgba(20, 0, 0, 0.7);
        border: 1px solid #ff003c;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* MATRIX RAIN EFFECT */
    @keyframes matrixRain {
        0% { transform: translateY(-100%); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(1000%); opacity: 0; }
    }
    
    .matrix-char {
        position: fixed;
        color: #00ff41;
        font-size: 14px;
        pointer-events: none;
        z-index: -1;
        opacity: 0.2;
        animation: matrixRain 5s linear infinite;
    }
    </style>
    
    <!-- MATRIX BACKGROUND SCRIPT -->
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Create matrix rain characters
        for(let i = 0; i < 30; i++) {
            const char = document.createElement('div');
            char.className = 'matrix-char';
            char.textContent = Math.random() > 0.5 ? '1' : '0';
            char.style.left = Math.random() * 100 + 'vw';
            char.style.animationDelay = Math.random() * 5 + 's';
            document.body.appendChild(char);
        }
    });
    </script>
    """, unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES MEJORADAS ---

def stream_data(text, speed=0.02):
    """Efecto de escritura terminal con delay configurable"""
    for word in text.split(" "):
        yield word + " "
        time.sleep(speed)

def crear_pdf_avanzado(dilema, m, b, c, final):
    """Generador de Reportes NERV con diseño mejorado"""
    pdf = FPDF()
    pdf.add_page()
    
    # Fondo degradado oscuro
    pdf.set_fill_color(5, 5, 5)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Encabezado con diseño de terminal
    pdf.set_font("Courier", "B", 20)
    pdf.set_text_color(0, 255, 65)  # Verde matriz
    pdf.cell(190, 15, "▌ MAGI SYSTEM - CLASSIFIED REPORT ▌", ln=True, align='C')
    
    # Línea decorativa
    pdf.set_draw_color(0, 255, 65)
    pdf.set_line_width(0.5)
    pdf.line(10, 25, 200, 25)
    
    # Información del sistema
    pdf.set_font("Courier", size=10)
    pdf.set_text_color(170, 170, 170)  # Gris
    pdf.cell(0, 8, f"CODE: 473 | FECHA: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 8, "SECURITY LEVEL: MAXIMUM | ACCESS: RESTRICTED", ln=True)
    pdf.ln(5)
    
    # Input dilema
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(255, 102, 0)  # Naranja
    pdf.cell(0, 10, ">> INPUT DILEMA:", ln=True)
    pdf.set_font("Courier", size=10)
    pdf.set_text_color(200, 200, 200)
    pdf.multi_cell(0, 6, f"> {dilema}")
    pdf.ln(10)
    
    # Respuestas de los nodos MAGI
    nodos = [
        ("MELCHIOR-1 (SCIENCE)", m, 0, 255, 65),
        ("BALTHASAR-2 (MOTHER)", b, 0, 162, 255),
        ("CASPER-3 (WOMAN)", c, 255, 0, 60)
    ]
    
    for nombre, contenido, r, g, b_color in nodos:
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(r, g, b_color)
        pdf.cell(0, 10, f"--- {nombre} ---", ln=True)
        pdf.set_font("Courier", size=9)
        pdf.set_text_color(180, 180, 180)
        pdf.multi_cell(0, 5, contenido)
        pdf.ln(5)
    
    # Resolución final
    pdf.set_font("Courier", "B", 13)
    pdf.set_text_color(255, 0, 60)  # Rojo brillante
    pdf.cell(0, 12, "▌ RESOLUCIÓN FINAL ▌", ln=True)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(0, 7, final)
    
    # Pie de página
    pdf.set_y(-30)
    pdf.set_font("Courier", "I", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "NERV CONFIDENTIAL - UNAUTHORIZED ACCESS PROHIBITED", ln=True, align='C')
    pdf.cell(0, 10, f"Document ID: MAGI_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}", ln=True, align='C')
    
    return bytes(pdf.output())

# --- INTERFAZ PRINCIPAL FIEL A LAS IMÁGENES ---

# Header con código 473 (como en la imagen)
col1, col2, col3 = st.columns([3, 1, 3])
with col1:
    st.markdown("""
    <div class="system-title">
        <i class="fas fa-server"></i> MAGI SYSTEM
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="system-code">
        CODE:473
    </div>
    """, unsafe_allow_html=True)
with col3:
    current_time = datetime.datetime.now().strftime("YY%y-%m-%d-%H H.%M")
    st.markdown(f"""
    <div class="system-time">
        {current_time}
    </div>
    """, unsafe_allow_html=True)

# Línea divisoria
st.markdown('<hr style="border: 1px solid #008f11; margin: 10px 0;">', unsafe_allow_html=True)

# Contenido principal en dos columnas
left_col, right_col = st.columns([1.5, 1])

with left_col:
    # Panel de nodos MAGI
    st.markdown("""
    <div class="terminal-panel">
        <div class="panel-title">
            <i class="fas fa-microchip"></i> MAGI UNITS STATUS
        </div>
    """, unsafe_allow_html=True)
    
    # Grid de nodos MAGI
    col_m1, col_b2, col_c3 = st.columns(3)
    
    with col_m1:
        st.markdown("""
        <div class="magi-unit">
            <div class="magi-name">MELCHIOR</div>
            <div class="magi-code">*1</div>
            <div class="magi-desc">
                "Neriteste nollere de fallemt lo tecempte: dolt, prrrrulant, ne clame nein pedl dolmes, sssath, bitso uud cattftes emtte prolllamist trtlicas dd selltm"
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b2:
        st.markdown("""
        <div class="magi-unit">
            <div class="magi-name">BALTHASAR</div>
            <div class="magi-code">*2</div>
            <div class="magi-desc">
                "Inurtest e nollere de fallemt lo tucempte: dilis prrrrulant, ne rtdame nah ped dalmee, sssath, bitso uud cinttture emtte prolllamist lutlice dd senltm"
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_c3:
        st.markdown("""
        <div class="magi-unit">
            <div class="magi-name">CASPER</div>
            <div class="magi-code">*3</div>
            <div class="magi-desc">
                "haritest e nollere de fallemt lo tecempte dnit, prrrrulant, ne rtdame nein pedl delmes, sssath 3 attita uad senltm"
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Status indicators (con caracteres chinos)
    st.markdown("""
    <div class="status-grid">
        <div class="status-item">
            <div class="status-label">登时</div>
            <div class="status-value">ACTIVE</div>
        </div>
        <div class="status-item">
            <div class="status-label">确定</div>
            <div class="status-value">CONFIRMED</div>
        </div>
        <div class="status-item">
            <div class="status-label">请假</div>
            <div class="status-value">PENDING</div>
        </div>
    </div>
    </div> <!-- Cierre del panel -->
    """, unsafe_allow_html=True)
    
    # Sistema de control
    st.markdown("""
    <div class="terminal-panel">
        <div class="panel-title">
            <i class="fas fa-terminal"></i> SYSTEM CONTROL
        </div>
    """, unsafe_allow_html=True)
    
    # Botones de control
    control_cols = st.columns(4)
    with control_cols[0]:
        if st.button("▶ INIT", use_container_width=True):
            st.session_state.last_command = "INIT"
    with control_cols[1]:
        if st.button("🔍 DIAG", use_container_width=True):
            st.session_state.last_command = "DIAG"
    with control_cols[2]:
        if st.button("🔄 RESET", use_container_width=True):
            st.session_state.last_command = "RESET"
    with control_cols[3]:
        if st.button("⚡ EXECUTE", use_container_width=True):
            st.session_state.last_command = "EXECUTE"
    
    # Output de comandos
    if 'last_command' in st.session_state:
        command_responses = {
            "INIT": "> INITIALIZING MAGI SYSTEM...\n> ALL UNITS ONLINE\n> NEURAL NETWORK: ACTIVE",
            "DIAG": "> RUNNING DIAGNOSTICS...\n> MELCHIOR-1: OK\n> BALTHASAR-2: OK\n> CASPER-3: OK\n> SYSTEM INTEGRITY: 100%",
            "RESET": "> RESETTING SUBSYSTEMS...\n> MEMORY CLEARED\n> READY FOR NEW INPUT",
            "EXECUTE": "> EXECUTING PROTOCOL 473...\n> ACCESSING SUPERCOMPUTING CENTER\n> RESOLUTION SYSTEM ENGAGED"
        }
        
        st.markdown(f"""
        <div class="data-display">
        {command_responses.get(st.session_state.last_command, "> COMMAND NOT RECOGNIZED")}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="data-display">
        > SYSTEM READY
        > MAGI UNITS ONLINE
        > AWAITING COMMANDS...
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    # Neural Link Interface
    st.markdown("""
    <div class="terminal-panel">
        <div class="panel-title">
            <i class="fas fa-project-diagram"></i> MAGI SYSTEM: SUPERCOMPUTING CENTER
        </div>
        
        <div class="neural-link">
            <div class="neural-title">
                <i class="fas fa-link"></i> ENLACE NEURAL
            </div>
            
            <div class="data-display">
    ART SHINE J:
    6 CMIGAIC:
    role: nyir.ret, ssem, contetine prose: [ cleme chitus in aayrieti = 1300],
    FECHA: lloma-3.3-70b versabille, message [ datetime now: (YY31-10-10-22 11H.MO).

    ) .
    (2 )
            </div>
        </div>
        
        <div class="panel-title" style="margin-top: 20px;">
            <i class="fas fa-key"></i> PRIORITY ACCESS KEY
        </div>
        
        <div class="data-display">
    EFCTHA: STANFENAAIAIO5IRA TORA SEITUND...

    ---

    INSRESE DATA: RAS PREPA TOA SEOKNT...
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Resolution System
    st.markdown("""
    <div class="terminal-panel">
        <div class="panel-title">
            <i class="fas fa-cogs"></i> RESOLUTION SYSTEM
        </div>
        
        <div class="data-display">
    ART:
    -- DILEMA
    Promete cout vor mctulte if ansserataste eratloc. [ dilema! final ]
    coulace lame [ dilema!

    ) .
    -- RESOLUSION FINAL
    "role call or asER3 en toira i aosie onyon yes in ehnila de, ssatile y apedale te reun al h3 eson aston" acede ktoina")
    croptee tee: "tsloim 3, ODcatatand")

    -- RESOLUCION FINAL
    role call or counte ilol i ce an nus to conllepre vvrestoy prtlace, encode lathny ergiale inytea's pters: cente")
    terscalatidiceJ.
        </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR PARA API KEY (mantenido de tu código original) ---
with st.sidebar:
    st.markdown("""
    <div class="terminal-panel">
        <div class="panel-title">
            <i class="fas fa-key"></i> NERV ACCESS CONTROL
        </div>
    """, unsafe_allow_html=True)
    
    api_key = None
    
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
            st.success("✅ PROTOCOL: SECURE LINK ESTABLISHED")
    except:
        api_key = st.text_input("CLAVE API (MANUAL ACCESS)", type="password")
        if not api_key:
            st.info("⚠️ INGRESE CLAVE GSK PARA ACTIVAR MAGI")
    
    st.markdown("""
    <div style="margin-top: 20px; padding: 10px; border: 1px solid #ff003c; background-color: rgba(255,0,60,0.1);">
        <small><b>SECURITY NOTICE:</b></small><br>
        <small>UNAUTHORIZED ACCESS IS PROHIBITED</small>
    </div>
    </div>
    """, unsafe_allow_html=True)

# --- INPUT DEL USUARIO MEJORADO ---
st.markdown("""
<div style="margin: 20px 0;">
    <div class="panel-title">
        <i class="fas fa-comment-alt"></i> TACTICAL DATA INPUT
    </div>
</div>
""", unsafe_allow_html=True)

dilema = st.chat_input("INGRESE DATOS TÁCTICOS...", key="chat_input")

if dilema and api_key:
    client = Groq(api_key=api_key)
    
    # Mostrar input del usuario con estilo
    st.markdown(f"""
    <div style="border-left: 3px solid #00a2ff; padding-left: 15px; margin-bottom: 20px; background-color: rgba(0,162,255,0.1); padding: 15px;">
        <small style="color: #888;">USER COMMAND:</small><br>
        <span style="font-size: 1.2em; color: #00a2ff;">&gt;&gt; {dilema}</span>
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
        )
        return completion.choices[0].message.content
    
    # Procesamiento con interfaz mejorada
    with st.status("🔄 ESTABLECIENDO ENLACE NEURAL...", expanded=True) as status:
        status.update(label="CONECTANDO CON MELCHIOR-1...", state="running")
        m_resp = consultar_magi("Eres MELCHIOR. Científico, lógico, frío. Breve.", 0.1)
        
        status.update(label="CONECTANDO CON BALTHASAR-2...", state="running")
        b_resp = consultar_magi("Eres BALTHASAR. Madre, protectora, ética. Breve.", 0.5)
        
        status.update(label="CONECTANDO CON CASPER-3...", state="running")
        c_resp = consultar_magi("Eres CASPER. Mujer, intuitiva, egoísta. Breve.", 0.9)
        
        status.update(label="SINTETIZANDO RESOLUCIÓN FINAL...", state="running")
        final_resp = consultar_magi(f"Resume resolución final de: M:{m_resp}, B:{b_resp}, C:{c_resp}", 0.2)
        
        status.update(label="✅ SISTEMA SINCRONIZADO", state="complete", expanded=False)
    
    # Mostrar resultados en grid
    st.markdown('<div class="panel-title"><i class="fas fa-brain"></i> MAGI CONSULTATION RESULTS</div>', unsafe_allow_html=True)
    
    results_cols = st.columns(3)
    
    with results_cols[0]:
        st.markdown('<div class="magi-unit"><div class="magi-name">MELCHIOR-1</div><div style="color: #888; font-size: 0.8em;">SCIENCE</div></div>', unsafe_allow_html=True)
        st.write_stream(stream_data(m_resp, 0.01))
    
    with results_cols[1]:
        st.markdown('<div class="magi-unit"><div class="magi-name">BALTHASAR-2</div><div style="color: #888; font-size: 0.8em;">MOTHER</div></div>', unsafe_allow_html=True)
        st.write_stream(stream_data(b_resp, 0.01))
    
    with results_cols[2]:
        st.markdown('<div class="magi-unit"><div class="magi-name">CASPER-3</div><div style="color: #888; font-size: 0.8em;">WOMAN</div></div>', unsafe_allow_html=True)
        st.write_stream(stream_data(c_resp, 0.01))
    
    # Resolución final con diseño especial
    st.markdown("""
    <div class="resolution-box">
        <div class="panel-title">
            <i class="fas fa-exclamation-triangle"></i> RESOLUCIÓN FINAL
        </div>
    """, unsafe_allow_html=True)
    
    st.write_stream(stream_data(final_resp, 0.015))
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Generar PDF mejorado
    pdf_bytes = crear_pdf_avanzado(dilema, m_resp, b_resp, c_resp, final_resp)
    
    # Botón de descarga con estilo
    col1, col2 = st.columns([3, 1])
    with col1:
        st.download_button(
            label="📥 DESCARGAR INFORME CLASIFICADO (PDF HD)",
            data=pdf_bytes,
            file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    with col2:
        if st.button("🖨️ IMPRIMIR INFORME", use_container_width=True):
            st.info("Función de impresión disponible en la versión local")

elif dilema and not api_key:
    st.error("""
    🔴 MAGI OFFLINE
    
    Se requiere clave de acceso GSK para activar el sistema.
    Ingrese la clave en el panel lateral.
    """)

# Footer del sistema
st.markdown("""
<div style="margin-top: 40px; padding: 15px; border-top: 1px solid #008f11; text-align: center; color: #888; font-size: 0.9rem;">
    MAGI SYSTEM v3.14 | SUPERCOMPUTING CENTER | NEURAL NETWORK ACTIVE<br>
    <small>SECURITY LEVEL: MAXIMUM | ACCESS: RESTRICTED | PROTOCOL: ENIGMA-473</small>
</div>
""", unsafe_allow_html=True)

# Script para efecto de cursor parpadeante
st.markdown("""
<script>
// Efecto de cursor parpadeante
document.addEventListener('DOMContentLoaded', function() {
    const cursor = document.createElement('span');
    cursor.id = 'blinking-cursor';
    cursor.textContent = '█';
    cursor.style.animation = 'blink 1s infinite';
    cursor.style.color = '#00ff41';
    
    // Agregar estilo de parpadeo
    const style = document.createElement('style');
    style.textContent = '@keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; } }';
    document.head.appendChild(style);
    
    // Intentar agregar cursor a ciertos elementos
    setTimeout(() => {
        const inputs = document.querySelectorAll('.stTextInput input, .stChatInput textarea');
        inputs.forEach(input => {
            if(input.value === '') {
                input.placeholder = '█';
            }
        });
    }, 100);
});
</script>
""", unsafe_allow_html=True)