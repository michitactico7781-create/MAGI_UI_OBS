import streamlit as st
from groq import Groq
import datetime
import time
import unicodedata
from io import BytesIO
import base64

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
    
    /* CHAT INPUT */
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
    
    /* NEURAL LINK */
    .neural-link {
        background-color: rgba(0, 0, 30, 0.7);
        border: 1px solid #00a2ff;
        padding: 15px;
        margin: 15px 0;
    }
    
    /* MATRIX RAIN */
    @keyframes matrixRain {
        0% { transform: translateY(-100px); opacity: 0; }
        10% { opacity: 0.8; }
        90% { opacity: 0.8; }
        100% { transform: translateY(100vh); opacity: 0; }
    }
    
    .matrix-char {
        position: fixed;
        color: #00ff41;
        font-size: 14px;
        pointer-events: none;
        z-index: -1;
        opacity: 0.3;
        animation: matrixRain 3s linear infinite;
    }
    </style>
    
    <script>
    // Efecto Matrix simple
    document.addEventListener('DOMContentLoaded', function() {
        const chars = '01';
        const container = document.createElement('div');
        container.style.position = 'fixed';
        container.style.top = '0';
        container.style.left = '0';
        container.style.width = '100%';
        container.style.height = '100%';
        container.style.pointerEvents = 'none';
        container.style.zIndex = '-1';
        document.body.appendChild(container);
        
        for(let i = 0; i < 50; i++) {
            const char = document.createElement('div');
            char.className = 'matrix-char';
            char.textContent = chars[Math.floor(Math.random() * chars.length)];
            char.style.left = Math.random() * 100 + 'vw';
            char.style.animationDelay = Math.random() * 3 + 's';
            container.appendChild(char);
        }
    });
    </script>
    """, unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES ---

def stream_data(text, speed=0.02):
    """Efecto de escritura terminal"""
    for word in text.split(" "):
        yield word + " "
        time.sleep(speed)

def limpiar_texto_para_pdf(texto):
    """Limpia texto para compatibilidad"""
    if not texto:
        return ""
    
    # Reemplazar caracteres problemáticos
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N',
        '¿': '?', '¡': '!',
        '—': '-', '–': '-', '…': '...',
        '«': '"', '»': '"', '“': '"', '”': '"', '‘': "'", '’': "'",
    }
    
    for char, repl in reemplazos.items():
        texto = texto.replace(char, repl)
    
    # Limitar longitud
    if len(texto) > 1000:
        texto = texto[:1000] + "\n[...CONTINUED IN SYSTEM ARCHIVES...]"
    
    return texto

# --- GENERACIÓN DE PDF CON FPDF (VERSIÓN SIMPLE Y VISIBLE) ---

def crear_pdf_fpdf(dilema, m_resp, b_resp, c_resp, final_resp):
    """Genera PDF simple y visible con FPDF"""
    try:
        from fpdf import FPDF
        
        pdf = FPDF()
        pdf.add_page()
        
        # TÍTULO (NEGRO SOBRE BLANCO)
        pdf.set_font("Courier", "B", 20)
        pdf.set_text_color(0, 0, 0)  # NEGRO
        pdf.cell(0, 15, "MAGI SYSTEM - CLASSIFIED REPORT", ln=True, align='C')
        pdf.ln(10)
        
        # INFORMACIÓN
        pdf.set_font("Courier", "", 10)
        pdf.set_text_color(0, 0, 0)  # NEGRO
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(0, 8, f"Report Code: 473 | Date: {fecha}", ln=True)
        pdf.cell(0, 8, "Security Level: MAXIMUM | Access: RESTRICTED", ln=True)
        pdf.ln(15)
        
        # LÍNEA DIVISORIA
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(10)
        
        # INPUT DEL USUARIO
        pdf.set_font("Courier", "B", 12)
        pdf.set_text_color(0, 0, 0)  # NEGRO
        pdf.cell(0, 10, "TACTICAL INPUT:", ln=True)
        pdf.set_font("Courier", "", 10)
        pdf.set_text_color(50, 50, 50)  # Gris oscuro
        pdf.multi_cell(0, 6, f"> {limpiar_texto_para_pdf(dilema)}")
        pdf.ln(10)
        
        # RESPUESTAS DE LOS NODOS MAGI
        pdf.set_font("Courier", "B", 14)
        pdf.set_text_color(0, 0, 0)  # NEGRO
        pdf.cell(0, 12, "MAGI SYSTEM ANALYSIS", ln=True)
        pdf.ln(8)
        
        # Lista de respuestas
        respuestas = [
            ("MELCHIOR-1 (SCIENCE)", limpiar_texto_para_pdf(m_resp)),
            ("BALTHASAR-2 (MOTHER)", limpiar_texto_para_pdf(b_resp)),
            ("CASPER-3 (WOMAN)", limpiar_texto_para_pdf(c_resp))
        ]
        
        for nombre, contenido in respuestas:
            pdf.set_font("Courier", "B", 11)
            pdf.set_text_color(0, 0, 0)  # NEGRO
            pdf.cell(0, 10, f"{nombre}:", ln=True)
            pdf.set_font("Courier", "", 9)
            pdf.set_text_color(30, 30, 30)  # Gris muy oscuro
            pdf.multi_cell(0, 5, contenido)
            pdf.ln(8)
        
        # RESOLUCIÓN FINAL
        pdf.ln(10)
        pdf.set_font("Courier", "B", 14)
        pdf.set_text_color(0, 0, 0)  # NEGRO
        pdf.cell(0, 12, "FINAL RESOLUTION:", ln=True)
        pdf.set_font("Courier", "B", 10)
        pdf.set_text_color(0, 0, 0)  # NEGRO
        pdf.multi_cell(0, 6, limpiar_texto_para_pdf(final_resp))
        
        # PIE DE PÁGINA
        pdf.ln(20)
        pdf.set_font("Courier", "I", 9)
        pdf.set_text_color(100, 100, 100)  # Gris
        pdf.cell(0, 8, "--- SYSTEM AUTO-GENERATED REPORT ---", ln=True)
        pdf.cell(0, 8, "MAGI v3.14 | NERV Command System", ln=True)
        
        return pdf.output(dest='S').encode('latin-1', 'ignore')
        
    except Exception as e:
        st.error(f"FPDF Error: {str(e)}")
        return None

# --- GENERACIÓN DE PDF CON REPORTLAB (RECOMENDADO) ---

def crear_pdf_reportlab(dilema, m_resp, b_resp, c_resp, final_resp):
    """Genera PDF profesional con ReportLab"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.colors import black, Color
        from io import BytesIO
        
        # Crear buffer
        buffer = BytesIO()
        
        # Crear canvas
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Configurar fuente Courier (built-in)
        c.setFont("Courier-Bold", 16)
        
        # TÍTULO
        c.setFillColor(black)
        c.drawCentredString(width/2, height - 50, "MAGI SYSTEM - CLASSIFIED REPORT")
        
        # INFORMACIÓN
        c.setFont("Courier", 10)
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.drawString(50, height - 80, f"Report Code: 473")
        c.drawString(50, height - 95, f"Date: {fecha}")
        c.drawString(50, height - 110, "Security Level: MAXIMUM")
        
        # LÍNEA DIVISORIA
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.line(50, height - 120, width - 50, height - 120)
        
        y_position = height - 140
        
        # INPUT DEL USUARIO
        c.setFont("Courier-Bold", 12)
        c.drawString(50, y_position, "TACTICAL INPUT:")
        y_position -= 20
        
        c.setFont("Courier", 10)
        input_lines = dilema[:300].split('\n')
        for line in input_lines[:5]:  # Máximo 5 líneas
            c.drawString(60, y_position, f"> {line[:80]}")
            y_position -= 15
            if y_position < 100:
                c.showPage()
                c.setFont("Courier", 10)
                y_position = height - 50
        
        y_position -= 10
        
        # MAGI SYSTEM ANALYSIS
        c.setFont("Courier-Bold", 14)
        c.drawString(50, y_position, "MAGI SYSTEM ANALYSIS")
        y_position -= 25
        
        # Respuestas de los nodos
        respuestas = [
            ("MELCHIOR-1 (SCIENCE)", m_resp),
            ("BALTHASAR-2 (MOTHER)", b_resp),
            ("CASPER-3 (WOMAN)", c_resp)
        ]
        
        for nombre, contenido in respuestas:
            c.setFont("Courier-Bold", 11)
            c.drawString(50, y_position, f"{nombre}:")
            y_position -= 15
            
            c.setFont("Courier", 9)
            # Limitar y dividir contenido
            texto = contenido[:400] + ("..." if len(contenido) > 400 else "")
            lines = texto.split('\n')
            for line in lines[:10]:  # Máximo 10 líneas por nodo
                if y_position < 100:
                    c.showPage()
                    c.setFont("Courier", 9)
                    y_position = height - 50
                
                c.drawString(60, y_position, line[:90])
                y_position -= 12
            
            y_position -= 10
        
        # RESOLUCIÓN FINAL
        y_position -= 10
        c.setFont("Courier-Bold", 14)
        c.drawString(50, y_position, "FINAL RESOLUTION:")
        y_position -= 20
        
        c.setFont("Courier-Bold", 10)
        final_lines = final_resp[:500].split('\n')
        for line in final_lines[:10]:
            if y_position < 100:
                c.showPage()
                c.setFont("Courier-Bold", 10)
                y_position = height - 50
            
            c.drawString(60, y_position, line[:90])
            y_position -= 14
        
        # PIE DE PÁGINA
        c.setFont("Courier-Oblique", 8)
        c.setFillColor(Color(0.4, 0.4, 0.4))  # Gris
        c.drawCentredString(width/2, 40, "--- SYSTEM AUTO-GENERATED REPORT ---")
        c.drawCentredString(width/2, 30, "MAGI v3.14 | NERV Command System | UNAUTHORIZED ACCESS PROHIBITED")
        
        # Guardar PDF
        c.save()
        
        # Obtener bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
        
    except ImportError:
        st.warning("ReportLab no está instalado. Usando FPDF...")
        return crear_pdf_fpdf(dilema, m_resp, b_resp, c_resp, final_resp)
    except Exception as e:
        st.error(f"ReportLab Error: {str(e)}")
        return None

# --- GENERACIÓN DE PDF (FUNCIÓN PRINCIPAL) ---

def generar_pdf(dilema, m_resp, b_resp, c_resp, final_resp):
    """Función principal para generar PDF - usa ReportLab si está disponible"""
    # Primero intentar con ReportLab
    pdf_bytes = crear_pdf_reportlab(dilema, m_resp, b_resp, c_resp, final_resp)
    
    # Si ReportLab falla, usar FPDF
    if pdf_bytes is None:
        pdf_bytes = crear_pdf_fpdf(dilema, m_resp, b_resp, c_resp, final_resp)
    
    return pdf_bytes

# --- INTERFAZ PRINCIPAL ---

# Header
col1, col2, col3 = st.columns([3, 1, 3])
with col1:
    st.markdown("""
    <div class="system-title">
        ⬢ MAGI SYSTEM
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="system-code">
        CODE:473
    </div>
    """, unsafe_allow_html=True)
with col3:
    current_time = datetime.datetime.now().strftime("YY%y-%m-%d %H:%M")
    st.markdown(f"""
    <div class="system-time">
        {current_time}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Panel de nodos MAGI
st.markdown("### 🔻 MAGI UNITS STATUS")
col_m, col_b, col_c = st.columns(3)

with col_m:
    st.markdown("""
    <div class="magi-unit">
        <div class="magi-name">MELCHIOR</div>
        <div class="magi-code">*1</div>
        <div style="color:#888; font-size:0.9em; margin-top:10px">
        "Neriteste nollere de fallemt lo tecempte: dolt, prrrrulant..."
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="magi-unit">
        <div class="magi-name">BALTHASAR</div>
        <div class="magi-code">*2</div>
        <div style="color:#888; font-size:0.9em; margin-top:10px">
        "Inurtest e nollere de fallemt lo tucempte: dilis prrrrulant..."
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown("""
    <div class="magi-unit">
        <div class="magi-name">CASPER</div>
        <div class="magi-code">*3</div>
        <div style="color:#888; font-size:0.9em; margin-top:10px">
        "haritest e nollere de fallemt lo tecempte dnit, prrrrulant..."
        </div>
    </div>
    """, unsafe_allow_html=True)

# Status indicators
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
""", unsafe_allow_html=True)

# Neural Link Section
st.markdown("""
<div class="neural-link">
    <div style="color:#00a2ff; font-size:1.2rem; margin-bottom:10px;">
        <i class="fas fa-link"></i> ENLACE NEURAL
    </div>
    <div style="color:#aaa; font-family:'Courier New'; white-space:pre; font-size:0.9rem;">
ART SHINE J:
6 CMIGAIC:
role: nyir.ret, ssem, contetine prose: [ cleme chitus in aayrieti = 1300],
FECHA: lloma-3.3-70b versabille, message [ datetime now: (YY31-10-10-22 11H.MO).

) .
(2 )
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar para API Key
with st.sidebar:
    st.markdown("### 🔐 NERV ACCESS CONTROL")
    
    api_key = None
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
            st.success("✅ Secure link established")
    except:
        api_key = st.text_input("API KEY (GROQ)", type="password", key="api_key_input")
    
    if not api_key:
        st.warning("⚠️ Enter Groq API key to activate system")
    
    st.markdown("---")
    st.markdown("**Instalar ReportLab para mejor PDF:**")
    st.code("pip install reportlab", language="bash")

# Input principal
st.markdown("### 📡 TACTICAL DATA INPUT")
dilema = st.chat_input("INGRESE DATOS TÁCTICOS...", key="main_input")

if dilema and api_key:
    try:
        client = Groq(api_key=api_key)
        
        # Mostrar input del usuario
        st.markdown(f"""
        <div class="terminal-panel">
            <div class="panel-title">
                <i class="fas fa-comment-alt"></i> USER INPUT
            </div>
            <div style="color:#00a2ff; font-size:1.1em;">
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
                max_tokens=250  # Limitar para PDF
            )
            return completion.choices[0].message.content
        
        # Procesar con los 3 nodos
        with st.spinner("🔄 ESTABLECIENDO ENLACE NEURAL..."):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("##### 🧪 MELCHIOR-1")
                with st.spinner("Analyzing..."):
                    m_resp = consultar_magi("Eres MELCHIOR. Científico, lógico, frío. Responde breve en 100 palabras max.", 0.1)
                st.write_stream(stream_data(m_resp))
            
            with col2:
                st.markdown("##### 🛡️ BALTHASAR-2")
                with st.spinner("Evaluating..."):
                    b_resp = consultar_magi("Eres BALTHASAR. Madre, protectora, ética. Responde breve en 100 palabras max.", 0.5)
                st.write_stream(stream_data(b_resp))
            
            with col3:
                st.markdown("##### 🌸 CASPER-3")
                with st.spinner("Intuiting..."):
                    c_resp = consultar_magi("Eres CASPER. Mujer, intuitiva, egoísta. Responde breve en 100 palabras max.", 0.9)
                st.write_stream(stream_data(c_resp))
        
        # Resolución final
        st.markdown("### 🛑 FINAL RESOLUTION")
        with st.spinner("Synthesizing final resolution..."):
            final_resp = consultar_magi(
                f"Resume en 150 palabras máximo la resolución final basada en las tres perspectivas. "
                f"Sé conciso y directo. No repitas lo que ya dijeron.", 
                0.3
            )
        
        st.markdown(f"""
        <div class="terminal-panel" style="border-left: 5px solid #ff003c;">
            <div style="color:#ff003c; font-weight:bold; margin-bottom:10px;">
                ⚡ RESOLUCIÓN DEL SISTEMA:
            </div>
            <div style="color:#fff; line-height:1.6;">
                {final_resp}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # --- GENERAR PDF ---
        st.markdown("### 📄 CLASSIFIED REPORT GENERATION")
        
        # Opciones de PDF
        col_pdf1, col_pdf2 = st.columns(2)
        
        with col_pdf1:
            if st.button("🖨️ GENERAR PDF CON REPORTLAB", use_container_width=True):
                with st.spinner("Generando PDF profesional..."):
                    pdf_bytes = crear_pdf_reportlab(dilema, m_resp, b_resp, c_resp, final_resp)
                    
                    if pdf_bytes:
                        st.download_button(
                            label="⬇️ DESCARGAR PDF (ReportLab)",
                            data=pdf_bytes,
                            file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("✅ PDF generado con ReportLab (calidad profesional)")
                    else:
                        st.error("❌ Error al generar PDF con ReportLab")
        
        with col_pdf2:
            if st.button("📄 GENERAR PDF CON FPDF", use_container_width=True):
                with st.spinner("Generando PDF simple..."):
                    pdf_bytes = crear_pdf_fpdf(dilema, m_resp, b_resp, c_resp, final_resp)
                    
                    if pdf_bytes:
                        st.download_button(
                            label="⬇️ DESCARGAR PDF (FPDF)",
                            data=pdf_bytes,
                            file_name=f"MAGI_SIMPLE_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("✅ PDF generado con FPDF (formato simple)")
                    else:
                        st.error("❌ Error al generar PDF con FPDF")
        
        # Previsualización del reporte
        with st.expander("📋 PREVIEW REPORT CONTENT"):
            st.text(f"""
            ===== MAGI SYSTEM REPORT =====
            Date: {datetime.datetime.now()}
            Code: 473
            
            INPUT:
            {dilema[:200]}
            
            MELCHIOR-1:
            {m_resp[:150]}
            
            BALTHASAR-2:
            {b_resp[:150]}
            
            CASPER-3:
            {c_resp[:150]}
            
            FINAL RESOLUTION:
            {final_resp}
            """)
            
            # Opción de descarga como texto
            texto_completo = f"""MAGI SYSTEM REPORT
================================
Date: {datetime.datetime.now()}
Report Code: 473
Security Level: MAXIMUM

TACTICAL INPUT:
{dilema}

MELCHIOR-1 (SCIENCE):
{m_resp}

BALTHASAR-2 (MOTHER):
{b_resp}

CASPER-3 (WOMAN):
{c_resp}

FINAL SYSTEM RESOLUTION:
{final_resp}

--- END OF REPORT ---
MAGI v3.14 | NERV Command System"""
            
            st.download_button(
                label="📝 DESCARGAR COMO TEXTO",
                data=texto_completo,
                file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    except Exception as e:
        st.error(f"❌ SYSTEM ERROR: {str(e)[:200]}")
        st.info("""
        **Posibles soluciones:**
        1. Verifica tu API key de Groq
        2. Revisa tu conexión a internet
        3. Intenta con un input más corto
        4. Espera unos minutos e inténtalo de nuevo
        """)

elif dilema and not api_key:
    st.error("""
    🔴 MAGI SYSTEM OFFLINE
    
    Se requiere clave de acceso Groq API para activar el sistema.
    Ingresa la clave en el panel lateral.
    
    **Cómo obtener una API key:**
    1. Ve a https://console.groq.com
    2. Regístrate o inicia sesión
    3. Crea una nueva API key
    4. Cópiala y pégala en el panel lateral
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem; padding: 20px;">
    MAGI SYSTEM v3.14 | SUPERCOMPUTING CENTER | NEURAL NETWORK ACTIVE<br>
    <small>SECURITY LEVEL: MAXIMUM | ACCESS: RESTRICTED | PROTOCOL: ENIGMA-473</small>
</div>
""", unsafe_allow_html=True)

# Instrucciones de instalación
st.sidebar.markdown("---")
st.sidebar.markdown("### 📦 INSTALACIÓN")
st.sidebar.code("""
pip install streamlit
pip install groq
pip install reportlab  # Para PDF profesional
""", language="bash")
