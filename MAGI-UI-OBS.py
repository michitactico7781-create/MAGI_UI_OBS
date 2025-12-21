import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime
import time
import unicodedata

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="MAGI SYSTEM: SUPERCOMPUTING CENTER",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS FIEL A LAS IMÁGENES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    .stApp {
        background-color: #0a0a0a;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
    }
    
    .stButton > button {
        border: 1px solid #00ff41;
        background-color: rgba(0, 40, 0, 0.8);
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        font-weight: bold;
        border-radius: 0;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: rgba(0, 255, 65, 0.2);
        box-shadow: 0 0 10px #00ff41;
        color: white;
    }
    
    .stTextInput > div > div > input,
    .stChatInput > div > div > textarea {
        background-color: rgba(0, 20, 0, 0.8) !important;
        color: #00ff41 !important;
        border: 1px solid #008f11 !important;
        font-family: 'Share Tech Mono', monospace !important;
        border-radius: 0 !important;
    }
    
    .terminal-box {
        border: 1px solid #008f11;
        background-color: rgba(0, 20, 0, 0.8);
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
    }
    
    .magi-unit-box {
        border: 1px solid #008f11;
        background-color: rgba(0, 30, 0, 0.5);
        padding: 15px;
        margin: 10px 0;
    }
    
    .magi-title {
        color: #00a2ff;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .magi-code {
        color: #ff003c;
        font-size: 1.5rem;
        font-weight: bold;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES CON MANEJO DE UNICODE ---

def stream_data(text, speed=0.02):
    """Efecto de escritura terminal"""
    for word in text.split(" "):
        yield word + " "
        time.sleep(speed)

def limpiar_texto_para_pdf(texto):
    """Convierte texto Unicode a formato compatible con FPDF"""
    if not texto:
        return ""
    
    # Primero normalizar el texto
    texto = unicodedata.normalize('NFKD', texto)
    
    # Reemplazar caracteres problemáticos
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N',
        '¿': '?', '¡': '!',
        '—': '-', '–': '-', '…': '...',
        '«': '"', '»': '"', '“': '"', '”': '"', '‘': "'", '’': "'",
        '€': 'EUR', '£': 'GBP', '¥': 'JPY', '¢': 'cent',
        '°': ' grados', '±': '+/-', '×': 'x', '÷': '/',
        'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta',
        'µ': 'micro', 'Ω': 'Omega', 'π': 'pi', '∞': 'infinity',
    }
    
    for char, replacement in reemplazos.items():
        texto = texto.replace(char, replacement)
    
    # Filtrar solo caracteres ASCII imprimibles y algunos latinos
    texto_limpio = ''
    for char in texto:
        try:
            # Intentar codificar como latin1
            char.encode('latin-1')
            texto_limpio += char
        except UnicodeEncodeError:
            # Si falla, usar caracter de reemplazo
            if ord(char) < 128:
                texto_limpio += char
            else:
                texto_limpio += '?'
    
    # Limitar longitud de líneas para PDF
    lineas = texto_limpio.split('\n')
    lineas_limitadas = []
    for linea in lineas:
        if len(linea) > 120:
            # Dividir líneas muy largas
            for i in range(0, len(linea), 100):
                lineas_limitadas.append(linea[i:i+100])
        else:
            lineas_limitadas.append(linea)
    
    return '\n'.join(lineas_limitadas)

def crear_pdf_compatible(dilema, m_resp, b_resp, c_resp, final_resp):
    """Generador de PDF robusto con manejo de Unicode"""
    pdf = FPDF()
    
    # Añadir fuente con soporte extendido (si tienes archivo .ttf)
    # pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    # pdf.set_font('DejaVu', '', 10)
    
    pdf.add_page()
    
    # Configuración simple con ASCII seguro
    pdf.set_font("Courier", "B", 16)
    pdf.set_text_color(0, 255, 65)  # Verde
    
    # Título seguro
    titulo = "MAGI SYSTEM - CLASSIFIED REPORT"
    pdf.cell(190, 10, titulo, ln=True, align='C')
    pdf.ln(5)
    
    # Fecha y hora
    pdf.set_font("Courier", size=10)
    pdf.set_text_color(170, 170, 170)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f"DATE: {fecha} | CODE: 473", ln=True)
    pdf.ln(10)
    
    # Limpiar todos los textos
    dilema_limpio = limpiar_texto_para_pdf(dilema)
    m_limpio = limpiar_texto_para_pdf(m_resp)
    b_limpio = limpiar_texto_para_pdf(b_resp)
    c_limpio = limpiar_texto_para_pdf(c_resp)
    final_limpio = limpiar_texto_para_pdf(final_resp)
    
    # Input dilema
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(0, 10, "INPUT DILEMA:", ln=True)
    pdf.set_font("Courier", size=10)
    pdf.set_text_color(200, 200, 200)
    pdf.multi_cell(0, 6, f"> {dilema_limpio[:500]}")  # Limitar longitud
    pdf.ln(10)
    
    # Nodos MAGI
    nodos = [
        ("MELCHIOR-1 (SCIENCE)", m_limpio, 0, 255, 65),
        ("BALTHASAR-2 (MOTHER)", b_limpio, 0, 162, 255),
        ("CASPER-3 (WOMAN)", c_limpio, 255, 0, 60)
    ]
    
    for nombre, contenido, r, g, b in nodos:
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(r, g, b)
        pdf.cell(0, 10, f"--- {nombre} ---", ln=True)
        pdf.set_font("Courier", size=9)
        pdf.set_text_color(180, 180, 180)
        
        # Dividir contenido si es muy largo
        if len(contenido) > 800:
            contenido = contenido[:800] + "\n[...CONTENT TRUNCATED FOR PDF COMPATIBILITY...]"
        
        pdf.multi_cell(0, 5, contenido)
        pdf.ln(5)
    
    # Resolución final
    pdf.set_font("Courier", "B", 13)
    pdf.set_text_color(255, 0, 60)
    pdf.cell(0, 12, "FINAL RESOLUTION:", ln=True)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(255, 255, 255)
    
    if len(final_limpio) > 600:
        final_limpio = final_limpio[:600] + "\n[...CONTINUED IN SYSTEM ARCHIVES...]"
    
    pdf.multi_cell(0, 7, final_limpio)
    
    # Pie de página
    pdf.set_y(-30)
    pdf.set_font("Courier", "I", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "NERV CONFIDENTIAL - ACCESS RESTRICTED", ln=True, align='C')
    
    # Guardar a bytes de forma segura
    try:
        return pdf.output(dest='S').encode('latin-1')
    except:
        # Fallback: guardar como string y codificar
        output = pdf.output(dest='S')
        return output.encode('latin-1', 'ignore')

# --- INTERFAZ PRINCIPAL SIMPLIFICADA ---

# Header
col1, col2, col3 = st.columns([3, 1, 3])
with col1:
    st.markdown("### ⬢ MAGI SYSTEM")
with col2:
    st.markdown("## **<span style='color:#ff003c'>CODE:473</span>**", unsafe_allow_html=True)
with col3:
    st.markdown(f"*{datetime.datetime.now().strftime('YY%y-%m-%d %H:%M')}*")

st.markdown("---")

# Panel de nodos MAGI
st.markdown("### 🔻 MAGI UNITS STATUS")
col_m, col_b, col_c = st.columns(3)

with col_m:
    st.markdown("""
    <div class="magi-unit-box">
        <div class="magi-title">MELCHIOR</div>
        <div class="magi-code">*1</div>
        <div style="color:#888; font-size:0.9em">
        Scientific analysis module
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="magi-unit-box">
        <div class="magi-title">BALTHASAR</div>
        <div class="magi-code">*2</div>
        <div style="color:#888; font-size:0.9em">
        Ethical evaluation module
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown("""
    <div class="magi-unit-box">
        <div class="magi-title">CASPER</div>
        <div class="magi-code">*3</div>
        <div style="color:#888; font-size:0.9em">
        Intuitive analysis module
        </div>
    </div>
    """, unsafe_allow_html=True)

# API Key
with st.sidebar:
    st.markdown("### 🔐 NERV ACCESS")
    
    api_key = None
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
            st.success("Secure link established")
    except:
        api_key = st.text_input("API KEY", type="password")
    
    if not api_key:
        st.warning("Enter Groq API key")

# Input principal
st.markdown("### 📡 TACTICAL DATA INPUT")
dilema = st.chat_input("Enter tactical dilemma...")

if dilema and api_key:
    try:
        client = Groq(api_key=api_key)
        
        # Mostrar input
        st.markdown(f"""
        <div class="terminal-box">
        <strong style="color:#00a2ff">USER INPUT:</strong><br>
        {dilema}
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
                max_tokens=300  # Limitar para PDF
            )
            return completion.choices[0].message.content
        
        # Procesar
        with st.spinner("Establishing neural link..."):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**MELCHIOR-1**")
                with st.spinner("Analyzing..."):
                    m_resp = consultar_magi("Eres MELCHIOR. Científico, lógico, frío. Responde breve.", 0.1)
                st.write_stream(stream_data(m_resp[:200] + "..." if len(m_resp) > 200 else m_resp))
            
            with col2:
                st.markdown("**BALTHASAR-2**")
                with st.spinner("Evaluating..."):
                    b_resp = consultar_magi("Eres BALTHASAR. Madre, protectora, ética. Responde breve.", 0.5)
                st.write_stream(stream_data(b_resp[:200] + "..." if len(b_resp) > 200 else b_resp))
            
            with col3:
                st.markdown("**CASPER-3**")
                with st.spinner("Intuiting..."):
                    c_resp = consultar_magi("Eres CASPER. Mujer, intuitiva, egoísta. Responde breve.", 0.9)
                st.write_stream(stream_data(c_resp[:200] + "..." if len(c_resp) > 200 else c_resp))
        
        # Resolución final
        st.markdown("### 🛑 FINAL RESOLUTION")
        with st.spinner("Synthesizing final resolution..."):
            final_resp = consultar_magi(
                f"Resume en 150 palabras maximo la resolucion final basada en: "
                f"MELCHIOR:{m_resp[:100]}, BALTHASAR:{b_resp[:100]}, CASPER:{c_resp[:100]}", 
                0.2
            )
        
        st.markdown(f"""
        <div class="terminal-box" style="border-left: 5px solid #ff003c;">
        {final_resp}
        </div>
        """, unsafe_allow_html=True)
        
        # Generar PDF
        st.markdown("### 📄 CLASSIFIED REPORT")
        
        try:
            pdf_bytes = crear_pdf_compatible(dilema, m_resp, b_resp, c_resp, final_resp)
            
            st.download_button(
                label="⬇️ DOWNLOAD PDF REPORT",
                data=pdf_bytes,
                file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
            
            st.success("PDF generated successfully!")
            
        except Exception as pdf_error:
            st.error(f"PDF Generation Error: {str(pdf_error)[:100]}")
            st.info("""
            **Alternative PDF generation failed. Possible reasons:**
            1. Special characters in the response
            2. Text too long
            3. FPDF encoding issue
            
            **Workaround:** Using text file instead.
            """)
            
            # Fallback: generar archivo de texto
            reporte_texto = f"""
            MAGI SYSTEM REPORT
            ==================
            Date: {datetime.datetime.now()}
            Code: 473
            
            USER INPUT:
            {dilema}
            
            MELCHIOR-1 (SCIENCE):
            {m_resp}
            
            BALTHASAR-2 (MOTHER):
            {b_resp}
            
            CASPER-3 (WOMAN):
            {c_resp}
            
            FINAL RESOLUTION:
            {final_resp}
            """
            
            st.download_button(
                label="⬇️ DOWNLOAD TEXT REPORT",
                data=reporte_texto,
                file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    except Exception as e:
        st.error(f"System Error: {str(e)[:150]}")
        st.info("Check your API key and internet connection.")

elif dilema and not api_key:
    st.error("⚠️ Enter API key in sidebar to activate MAGI system")

# Footer
st.markdown("---")
st.markdown("*MAGI SYSTEM v3.14 | NERV Confidential*")
