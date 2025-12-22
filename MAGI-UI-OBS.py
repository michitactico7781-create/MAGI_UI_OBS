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

# --- ESTILOS CSS SIMPLIFICADOS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

.stApp {
    background-color: #050505;
    color: #ff6600;
    font-family: 'Orbitron', 'Share Tech Mono', monospace;
}

/* Títulos */
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900 !important;
    color: #ff6600 !important;
    text-shadow: 0 0 10px rgba(255, 102, 0, 0.7);
    letter-spacing: 1px;
}

/* Tarjetas MAGI */
.magi-card {
    border: 2px solid #ff6600;
    background: rgba(20, 10, 0, 0.9);
    padding: 20px;
    margin: 15px 0;
    position: relative;
}

.node-title {
    font-size: 1.5em;
    border-bottom: 2px solid #ff6600;
    margin-bottom: 15px;
    padding-bottom: 10px;
    text-align: center;
    font-weight: 900;
}

/* Hexágonos MAGI */
.magi-hexagon {
    padding: 20px;
    margin: 10px;
    text-align: center;
    background: rgba(0, 153, 255, 0.1);
    border: 2px solid #0099FF;
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
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
}

.status-approved {
    color: #00FFC8;
    text-shadow: 0 0 10px rgba(0, 255, 200, 0.5);
}

.status-denied {
    color: #FF0000;
    text-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
}

/* Botones */
.stButton > button {
    border: 2px solid #ff6600;
    background: rgba(255, 102, 0, 0.1);
    color: #ff6600 !important;
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    border-radius: 0;
    padding: 12px 24px;
    transition: all 0.3s;
}

.stButton > button:hover {
    background: #ff6600;
    color: black !important;
    box-shadow: 0 0 20px #ff6600;
}

/* Inputs */
.stTextInput > div > div > input,
.stChatInput > div > div > textarea {
    background-color: rgba(10, 10, 10, 0.9) !important;
    color: #ff6600 !important;
    border: 2px solid #ff6600 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem !important;
}

/* Línea decorativa */
.deco-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #ff6600, transparent);
    margin: 20px 0;
}

/* Panel de decisión */
.decision-panel {
    background: rgba(0, 20, 40, 0.8);
    border: 2px solid #0099FF;
    padding: 20px;
    margin: 20px 0;
    text-align: center;
}

/* Indicadores */
.kanji-text {
    font-family: 'MS Gothic', monospace;
    color: #00FFC8;
    font-weight: bold;
}

.warning-text {
    color: #FF0000;
}
</style>
""", unsafe_allow_html=True)

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
    
    # Título
    pdf.set_font("Courier", "B", 16)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(190, 10, "MAGI SYSTEM - CLASSIFIED REPORT", ln=True, align='C')
    pdf.ln(10)
    
    # Información
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(100, 100, 100)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f"CODE: 473 | DATE: {fecha}", ln=True)
    pdf.ln(10)
    
    # Limpiar textos
    dilema_limpio = limpiar_texto_para_pdf(dilema)
    m_limpio = limpiar_texto_para_pdf(m)
    b_limpio = limpiar_texto_para_pdf(b)
    c_limpio = limpiar_texto_para_pdf(c)
    final_limpio = limpiar_texto_para_pdf(final)
    
    # Input
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(0, 10, "TACTICAL INPUT:", ln=True)
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, dilema_limpio)
    pdf.ln(10)
    
    # Respuestas MAGI
    nodos = [
        ("MELCHIOR-1 (SCIENCE)", m_limpio),
        ("BALTHASAR-2 (MOTHER)", b_limpio),
        ("CASPER-3 (WOMAN)", c_limpio)
    ]
    
    for nombre, contenido in nodos:
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(255, 102, 0)
        pdf.cell(0, 10, f"--- {nombre} ---", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 5, contenido)
        pdf.ln(5)
    
    # Decisión final
    pdf.set_font("Courier", "B", 13)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 12, "--- FINAL DECISION ---", ln=True)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, final_limpio)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

def get_majority_decision():
    approvals = sum(1 for state in st.session_state.magi_states.values() if state == "承 認")
    return "APPROVED" if approvals >= 2 else "DENIED"

# --- INTERFAZ PRINCIPAL ---

# Header
st.markdown("# ⬢ MAGI SYSTEM: SUPERCOMPUTING CENTER")
st.markdown("**STATUS:** `ONLINE` | **SYNC:** `99.9%` | **CODE:** `473`")

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# TRIUNVIRATO MAGI
st.markdown("### <span class='kanji-text'>三賢者の審議</span> - MAGI TRIUMVIRATE", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    estado = st.session_state.magi_states["MELCHIOR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">MELCHIOR-1</div>
        <div style="color:#888; font-size:0.9rem">SCIENCE MODULE</div>
        <div class="magi-status {'status-approved' if estado == '承 認' else 'status-denied'}">
            {estado}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    estado = st.session_state.magi_states["BALTHASAR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">BALTHASAR-2</div>
        <div style="color:#888; font-size:0.9rem">MOTHER MODULE</div>
        <div class="magi-status {'status-approved' if estado == '承 認' else 'status-denied'}">
            {estado}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    estado = st.session_state.magi_states["CASPER"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">CASPER-3</div>
        <div style="color:#888; font-size:0.9rem">WOMAN MODULE</div>
        <div class="magi-status {'status-approved' if estado == '承 認' else 'status-denied'}">
            {estado}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Panel de decisión
decision = get_majority_decision()
color = "#00FFC8" if decision == "APPROVED" else "#FF0000"
st.markdown(f"""
<div class="decision-panel">
    <div style="font-size: 1.5rem; font-weight: bold; color: {color}; margin-bottom: 10px;">
        SYSTEM DECISION: {decision}
    </div>
    <div style="color: #888; font-size: 0.9rem;">
        Majority Rule: 2/3 Required | Current Toxicity: {st.session_state.toxicity_level}%
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### 🔐 SYSTEM ACCESS")
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("Secure Link Active")
    else:
        api_key = st.text_input("GROQ API KEY", type="password")
    
    st.markdown("---")
    
    # Historial
    st.markdown("### 📜 RECENT LOGS")
    if st.session_state.history:
        for entry in reversed(st.session_state.history[-3:]):
            with st.expander(f"{entry['timestamp']}"):
                st.write(entry['dilema'][:50])
                st.write("→ " + entry['resolucion'][:100] + "...")
    else:
        st.write("No logs available")
    
    # Controles
    if st.button("UPDATE METRICS", use_container_width=True):
        st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + random.randint(5, 15))
        for magi in st.session_state.magi_states:
            st.session_state.magi_states[magi] = random.choice(["承 認", "否 定"])
        st.rerun()

# INPUT PRINCIPAL
st.markdown("### <span class='kanji-text'>質問</span> TACTICAL QUERY INPUT")
dilema = st.chat_input("Enter tactical parameters for analysis...")

if dilema and api_key:
    # Actualizar estados
    for magi in st.session_state.magi_states:
        st.session_state.magi_states[magi] = random.choice(["承 認", "否 定"])
    
    st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + 10)
    
    try:
        client = Groq(api_key=api_key)
        
        # Mostrar input
        st.markdown(f"""
        <div class="magi-card">
            <div class="node-title">USER QUERY</div>
            <div style="color: #00FFC8; font-size: 1.1rem; padding: 10px; border-left: 3px solid #ff6600;">
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
                max_tokens=150
            )
            return completion.choices[0].message.content
        
        # Procesar
        with st.status("INITIATING NEURAL LINK...", expanded=True) as status:
            st.write("Accessing MELCHIOR-1...")
            m_resp = consultar_magi("Eres MELCHIOR. Científico, lógico, frío. Breve análisis científico.", 0.1)
            time.sleep(0.5)
            
            st.write("Accessing BALTHASAR-2...")
            b_resp = consultar_magi("Eres BALTHASAR. Madre, protectora, ética. Breve análisis ético.", 0.5)
            time.sleep(0.5)
            
            st.write("Accessing CASPER-3...")
            c_resp = consultar_magi("Eres CASPER. Mujer, intuitiva, egoísta. Breve análisis intuitivo.", 0.9)
            time.sleep(0.5)
            
            st.write("Synthesizing final resolution...")
            final_resp = consultar_magi(f"Como sistema MAGI, resume resolución final concisa basada en: Ciencia:{m_resp[:50]}, Ética:{b_resp[:50]}, Intuición:{c_resp[:50]}", 0.3)
            
            status.update(label="DELIBERATION COMPLETE", state="complete", expanded=False)
        
        # Mostrar respuestas
        st.markdown("### <span class='kanji-text'>回答</span> MODULE RESPONSES")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.markdown('<div class="magi-card"><div class="node-title">MELCHIOR-1</div></div>', unsafe_allow_html=True)
            st.write_stream(stream_data(m_resp))
        
        with col_res2:
            st.markdown('<div class="magi-card"><div class="node-title">BALTHASAR-2</div></div>', unsafe_allow_html=True)
            st.write_stream(stream_data(b_resp))
        
        with col_res3:
            st.markdown('<div class="magi-card"><div class="node-title">CASPER-3</div></div>', unsafe_allow_html=True)
            st.write_stream(stream_data(c_resp))
        
        st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
        
        # Resolución final
        st.markdown("### <span class='kanji-text'>解決</span> FINAL RESOLUTION")
        st.markdown(f"""
        <div class="magi-card" style="border-left: 5px solid #ff6600;">
            <div style="color: #fff; line-height: 1.6; font-size: 1.1rem;">
        """, unsafe_allow_html=True)
        
        st.write_stream(stream_data(final_resp))
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Agregar al historial
        st.session_state.history.append({
            "dilema": dilema,
            "resolucion": final_resp,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })
        
        # Generar PDF
        with st.spinner("Generating official report..."):
            pdf_bytes = crear_pdf(dilema, m_resp, b_resp, c_resp, final_resp)
            
            st.download_button(
                label="📄 DOWNLOAD CLASSIFIED REPORT",
                data=pdf_bytes,
                file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        # Rerun para actualizar
        st.rerun()
        
    except Exception as e:
        st.error(f"System error: {str(e)}")

elif dilema and not api_key:
    st.error("Please enter API key in sidebar to activate system")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem; padding: 20px;">
    MAGI SYSTEM v3.14 | SUPERCOMPUTING CENTER | PROTOCOL 473<br>
    <span style="font-size: 0.8rem; color: #666;">
    Access Restricted | Security Maximum | File: MAGI_SYS
    </span>
</div>
""", unsafe_allow_html=True)
