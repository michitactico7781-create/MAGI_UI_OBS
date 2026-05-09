import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime
import time
import unicodedata
import random
import asyncio
import threading
import concurrent.futures
from typing import Dict, List, Tuple
import hashlib
import json

# --- NUEVAS IMPORTACIONES PARA FUNCIONALIDADES MEJORADAS ---
try:
    import edge_tts
    import pygame
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    st.warning("⚠️ edge-tts o pygame no instalados. La síntesis de voz no estará disponible.")

try:
    import requests
    from bs4 import BeautifulSoup
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False
    st.warning("⚠️ requests o beautifulsoup4 no instalados. La búsqueda web no estará disponible.")

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="MAGI SYSTEM v4.0: ADVANCED DELIBERATION",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INICIALIZACIÓN DE ESTADOS DE SESIÓN MEJORADA ---
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

if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = []

if "selected_format" not in st.session_state:
    st.session_state.selected_format = "Análisis Completo"

if "enable_voice" not in st.session_state:
    st.session_state.enable_voice = False

if "last_voice_text" not in st.session_state:
    st.session_state.last_voice_text = ""

# --- FUNCIONES MEJORADAS ---

def extraer_voto_desde_respuesta(respuesta_texto: str) -> str:
    """Analiza inteligentemente la respuesta para determinar el voto de cada MAGI"""
    if not respuesta_texto:
        return "否 定"
    
    texto_lower = respuesta_texto.lower()
    
    # Palabras clave de aprobación
    aprobacion = ["apruebo", "voto a favor", "autorizo", "acepto", "approved", 
                  "correcto", "válido", "recomiendo", "proceder", "sí", "afirmativo"]
    
    # Palabras clave de rechazo
    rechazo = ["rechazo", "voto en contra", "deniego", "rejected", "incorrecto",
               "inválido", "no recomiendo", "no proceder", "negativo", "denegado"]
    
    # Contar coincidencias
    aprobaciones = sum(1 for p in aprobacion if p in texto_lower)
    rechazos = sum(1 for p in rechazo if p in texto_lower)
    
    # Análisis de sentimiento adicional (positivo vs negativo)
    palabras_positivas = sum(1 for p in ["beneficioso", "ético", "seguro", "eficiente", "vida"] if p in texto_lower)
    palabras_negativas = sum(1 for p in ["peligroso", "inmoral", "riesgo", "dañino", "muerte"] if p in texto_lower)
    
    puntuacion = (aprobaciones + palabras_positivas) - (rechazos + palabras_negativas)
    
    return "承 認" if puntuacion >= 0 else "否 定"

def construir_contexto_historico() -> str:
    """Construye memoria contextual de deliberaciones previas"""
    if not st.session_state.history:
        return ""
    
    ultimos_3 = st.session_state.history[-3:]
    resumen = "【CONTEXTO DE DELIBERACIONES PREVIAS】\n"
    for i, h in enumerate(ultimos_3, 1):
        resumen += f"▸ Misión {i}: {h.get('dilema', 'N/A')[:80]}...\n"
        resumen += f"  ↳ Veredicto: {h.get('decision', 'N/A')} | Toxicidad: {h.get('toxicity', 'N/A')}%\n\n"
    
    return resumen

def ajustar_tono_segun_toxicidad() -> str:
    """Ajusta las restricciones según el nivel de toxicidad"""
    toxicity = st.session_state.toxicity_level
    
    if toxicity > 70:
        return "⚠️ ¡ALERTA DE TOXICIDAD CRÍTICA! Aplica filtros máximos, prioriza seguridad y bienestar humano sobre cualquier análisis. Limita respuestas explícitas."
    elif toxicity > 40:
        return "⚠️ Nivel de toxicidad MODERADO. Evalúa con cuidado pero permite análisis abierto con advertencias apropiadas."
    else:
        return "✅ Ambiente SEGURO. Análisis estándar permitido."

def buscar_en_web(consulta: str) -> str:
    """Realiza búsqueda web usando DuckDuckGo (sin API key)"""
    if not WEB_SEARCH_AVAILABLE:
        return "Servicio de búsqueda web no disponible."
    
    try:
        # Usar DuckDuckGo HTML (no requiere API key)
        url = f"https://html.duckduckgo.com/html/?q={consulta.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer resultados
        resultados = soup.select('.result__a')[:3]
        if not resultados:
            return "No se encontraron resultados."
        
        texto_resultados = "【RESULTADOS DE BÚSQUEDA WEB】\n"
        for i, r in enumerate(resultados, 1):
            titulo = r.get_text(strip=True)
            enlace = r.get('href', '')
            texto_resultados += f"\n{i}. {titulo}\n   ↳ {enlace[:100]}\n"
        
        return texto_resultados
    except Exception as e:
        return f"Error en búsqueda web: {str(e)[:100]}"

async def sintetizar_voz(texto: str, voz: str = "es-ES-ElviraNeural"):
    """Sintetiza voz usando edge-tts y la reproduce"""
    if not TTS_AVAILABLE or not st.session_state.enable_voice:
        return
    
    try:
        # Evitar repetir la misma síntesis
        if texto == st.session_state.last_voice_text:
            return
        
        st.session_state.last_voice_text = texto
        output_file = "temp_magi_speech.mp3"
        
        # Generar audio
        communicate = edge_tts.Communicate(texto, voz)
        await communicate.save(output_file)
        
        # Reproducir
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        # Esperar a que termine (en hilo separado para no bloquear)
        def wait_for_audio():
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        
        threading.Thread(target=wait_for_audio, daemon=True).start()
        
    except Exception as e:
        print(f"Error en síntesis de voz: {e}")

def generar_consecuencias(decision: str, dilema: str, client: Groq) -> str:
    """Genera árbol de consecuencias de la decisión"""
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"""Eres un analista de consecuencias. 
                Decisión tomada: {decision}
                Dilema original: {dilema}
                
                Genera un análisis estructurado de consecuencias:
                1. 3 CONSECUENCIAS A CORTO PLAZO (inmediatas - 1 semana)
                2. 3 CONSECUENCIAS A LARGO PLAZO (1 año o más)
                
                Sé específico, realista y basado en principios lógicos."""},
                {"role": "user", "content": "Generar análisis de consecuencias."}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=800
        )
        return completion.choices[0].message.content
    except:
        return "⚠️ No se pudo generar el análisis de consecuencias."

def stream_data_evangelion(text: str, speed: float = 0.02):
    """Efecto de máquina de escribir con glitch ocasional"""
    glitch_chars = ['�', '▓', '▒', '░', '█', '■', '□', '▢']
    
    for char in text:
        if random.random() < 0.03:
            yield random.choice(glitch_chars)
            time.sleep(0.03)
            yield char
        else:
            yield char
        time.sleep(speed)
        
        if char in ['.', '!', '?', ';', '\n']:
            time.sleep(speed * 2)

def limpiar_texto_para_pdf(texto: str) -> str:
    """Limpia texto para evitar errores en PDF"""
    if not texto:
        return ""
    
    # Reemplazar caracteres problemáticos
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U',
        '¿': '?', '¡': '!', '…': '...', '—': '-', '–': '-'
    }
    
    for char, repl in reemplazos.items():
        texto = texto.replace(char, repl)
    
    # Normalizar Unicode
    try:
        texto = unicodedata.normalize('NFKD', texto)
        texto = texto.encode('ascii', 'ignore').decode('ascii')
    except:
        texto = ''.join(c if 32 <= ord(c) < 127 else '?' for c in texto)
    
    return texto[:3000]

def crear_pdf_evangelion(dilema: str, m: str, b: str, c: str, final: str, consecuencias: str = "") -> bytes:
    """Crea PDF estilo Evangelion con código de autenticación"""
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font("Courier", "B", 18)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(190, 12, "MAGI SYSTEM v4.0 - CLASSIFIED REPORT", ln=True, align='C')
    pdf.ln(8)
    
    # Línea decorativa
    pdf.set_draw_color(255, 102, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Metadatos
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(0, 0, 0)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f"REPORT CODE: NERV-{hashlib.md5(fecha.encode()).hexdigest()[:8].upper()}", ln=True)
    pdf.cell(0, 8, f"DATE: {fecha}", ln=True)
    pdf.cell(0, 8, f"TOXICITY LEVEL: {st.session_state.toxicity_level}%", ln=True)
    pdf.ln(10)
    
    # Consulta
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(0, 10, "> ORIGINAL QUERY:", ln=True)
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(dilema))
    pdf.ln(10)
    
    # Respuestas de los nodos
    nodos = [
        ("MELCHIOR-1 (SCIENCE)", limpiar_texto_para_pdf(m), (0, 204, 255)),
        ("BALTHASAR-2 (MOTHER)", limpiar_texto_para_pdf(b), (0, 255, 170)),
        ("CASPER-3 (WOMAN)", limpiar_texto_para_pdf(c), (255, 102, 0))
    ]
    
    for nombre, contenido, color in nodos:
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(color[0], color[1], color[2])
        pdf.cell(0, 10, f">>> {nombre} <<<", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 5, contenido)
        pdf.ln(8)
    
    # Consecuencias si existen
    if consecuencias:
        pdf.set_draw_color(255, 102, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(255, 102, 0)
        pdf.cell(0, 10, ">>> CONSEQUENCE ANALYSIS <<<", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 5, limpiar_texto_para_pdf(consecuencias))
        pdf.ln(8)
    
    # Resolución final
    pdf.set_draw_color(255, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    pdf.set_font("Courier", "B", 14)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 12, ">>> FINAL RESOLUTION <<<", ln=True)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(final))
    
    # Código QR simulado y hash
    pdf.ln(10)
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(100, 100, 100)
    hash_val = hashlib.sha256(f"{dilema}{final}{fecha}".encode()).hexdigest()[:16]
    pdf.cell(0, 8, f"AUTHENTICATION HASH: {hash_val}", ln=True, align='C')
    pdf.cell(0, 8, "MAGI SYSTEM v4.0 | NERV COMMAND | LEVEL AAA CLASSIFIED", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

def get_majority_decision() -> str:
    """Calcula decisión por mayoría de votos"""
    approvals = sum(1 for state in st.session_state.magi_states.values() if state == "承 認")
    return "APPROVED" if approvals >= 2 else "DENIED"

def mostrar_secuencia_boot():
    """Secuencia de arranque animada"""
    boot_messages = [
        "> INITIATING MAGI SYSTEM v4.0 BOOT SEQUENCE...",
        "> NEURO-LINK ESTABLISHED...",
        "> TRIUMVIRATE SYNCHRONIZATION...",
        "> MEMORY BANKS LOADED...",
        "> TOXICITY MONITOR: ACTIVE",
        "> VOICE SYNTHESIS: STANDBY",
        "> MELCHIOR-1: ONLINE",
        "> BALTHASAR-2: ONLINE", 
        "> CASPER-3: ONLINE",
        "> DELIBERATION MATRIX: ACTIVE",
        "> AWAITING USER INPUT..."
    ]
    
    placeholder = st.empty()
    for i, msg in enumerate(boot_messages):
        placeholder.markdown(f"""
        <div style='color:#FF6600; font-family:"Share Tech Mono"; margin:5px 0;'>
            {msg}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.2)
    
    time.sleep(0.5)
    placeholder.empty()

def procesar_magi_paralelo(dilema: str, api_key: str, contexto: str, restriccion: str) -> Tuple[str, str, str]:
    """Procesa las tres MAGI en paralelo para mayor velocidad"""
    
    prompts = [
        {
            "nombre": "MELCHIOR",
            "system": f"""Eres MELCHIOR-1, nodo científico de MAGI. Eres frío, analítico, basado estrictamente en datos.
            {contexto}
            {restriccion}
            DILEMA: {dilema}
            Al final de tu análisis, indica claramente tu VOTO: 'APRUEBO' o 'RECHAZO'.""",
            "temp": 0.3
        },
        {
            "nombre": "BALTHASAR", 
            "system": f"""Eres BALTHASAR-2, nodo materno/ético de MAGI. Eres emocional, protector, priorizas la vida humana.
            {contexto}
            {restriccion}
            DILEMA: {dilema}
            Al final de tu análisis, indica claramente tu VOTO: 'APRUEBO' o 'RECHAZO'.""",
            "temp": 0.5
        },
        {
            "nombre": "CASPER",
            "system": f"""Eres CASPER-3, nodo intuitivo/práctico de MAGI. Eres pragmático, buscas el mejor resultado práctico.
            {contexto}
            {restriccion}
            DILEMA: {dilema}
            Al final de tu análisis, indica claramente tu VOTO: 'APRUEBO' o 'RECHAZO'.""",
            "temp": 0.7
        }
    ]
    
    resultados = {}
    
    def consultar_magi(prompt_info):
        try:
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": prompt_info["system"]},
                    {"role": "user", "content": f"Analiza el siguiente dilema desde tu perspectiva única: {dilema}"}
                ],
                model="llama-3.3-70b-versatile",
                temperature=prompt_info["temp"],
                max_tokens=1500,
                top_p=0.9
            )
            return prompt_info["nombre"], completion.choices[0].message.content
        except Exception as e:
            return prompt_info["nombre"], f"ERROR: {str(e)}"
    
    # Ejecutar en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(consultar_magi, prompt): prompt["nombre"] for prompt in prompts}
        for future in concurrent.futures.as_completed(futures):
            nombre, respuesta = future.result()
            resultados[nombre] = respuesta
    
    return resultados.get("MELCHIOR", ""), resultados.get("BALTHASAR", ""), resultados.get("CASPER", "")

# --- CSS Y ESTILOS (mantengo los tuyos, añado algunos mejorados) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=VT323&display=swap');

.stApp {
    background-color: #000000 !important;
    color: #FF6600 !important;
    font-family: 'VT323', 'Share Tech Mono', monospace !important;
}

/* Efecto CRT */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        linear-gradient(rgba(255, 102, 0, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 102, 0, 0.03) 1px, transparent 1px);
    background-size: 3px 3px;
    pointer-events: none;
    z-index: 0;
    animation: scan 8s linear infinite;
}

@keyframes scan {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
}

/* Hexágonos y demás estilos (mantengo los tuyos) */
.magi-hexagon {
    background: rgba(0, 20, 0, 0.8) !important;
    border: 2px solid #FF6600 !important;
    border-radius: 0 !important;
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%) !important;
    padding: 20px !important;
    margin: 10px !important;
    text-align: center !important;
    transition: all 0.3s ease;
}

.magi-hexagon:hover {
    box-shadow: 0 0 20px rgba(255, 102, 0, 0.5) !important;
    transform: scale(1.02);
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

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

.decision-panel {
    background: rgba(0, 10, 0, 0.9) !important;
    border: 2px solid #FF6600 !important;
    padding: 20px !important;
    margin: 20px 0 !important;
    transition: all 0.3s ease;
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

.response-card {
    background: rgba(0, 5, 0, 0.9) !important;
    border: 1px solid #FF6600 !important;
    border-left: 4px solid #FF6600 !important;
    margin: 10px 0 !important;
    padding: 15px !important;
    transition: all 0.2s ease;
}

.response-card:hover {
    transform: translateX(5px);
    box-shadow: -5px 0 15px rgba(255, 102, 0, 0.2);
}

/* Selector de formato */
.stSelectbox > div > div {
    background-color: rgba(0, 10, 0, 0.9) !important;
    border: 1px solid #FF6600 !important;
    color: #FF6600 !important;
}

/* Checkbox */
.stCheckbox > label {
    color: #FF6600 !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #FF6600 !important;
}

/* Botones */
.stButton > button {
    background: rgba(0, 20, 0, 0.8) !important;
    border: 1px solid #FF6600 !important;
    color: #FF6600 !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #FF6600 !important;
    color: #000000 !important;
    box-shadow: 0 0 10px #FF6600 !important;
}
</style>
""", unsafe_allow_html=True)

# --- INTERFAZ PRINCIPAL ---

# Boot sequence
if "boot_shown" not in st.session_state:
    st.session_state.boot_shown = True
    mostrar_secuencia_boot()

# Header
st.markdown("# ⬢ MAGI SYSTEM v4.0: ADVANCED DELIBERATION")
st.markdown(f"**STATUS:** `OPERATIONAL` | **SYNC:** `99.9%` | **TOXICITY:** `{st.session_state.toxicity_level}%` | **MEMORY:** `{len(st.session_state.history)} records`")

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# TRIUMVIRATO
st.markdown("### MAGI TRIUMVIRATE DELIBERATION MATRIX")

col1, col2, col3 = st.columns(3)

with col1:
    estado_mel = st.session_state.magi_states["MELCHIOR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">MELCHIOR-1</div>
        <div style="color:#00CCFF; font-size:0.9rem">SCIENCE MODULE</div>
        <div class="magi-status {'status-approved' if estado_mel == '承 認' else 'status-denied'}">{estado_mel}</div>
        <div style="color:#888; font-size:0.8rem; margin-top:10px;">⚡ LOGIC | DATA | ANALYSIS</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    estado_bal = st.session_state.magi_states["BALTHASAR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">BALTHASAR-2</div>
        <div style="color:#00FFAA; font-size:0.9rem">MOTHER MODULE</div>
        <div class="magi-status {'status-approved' if estado_bal == '承 認' else 'status-denied'}">{estado_bal}</div>
        <div style="color:#888; font-size:0.8rem; margin-top:10px;">❤️ ETHICS | PROTECTION | CARE</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    estado_cas = st.session_state.magi_states["CASPER"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">CASPER-3</div>
        <div style="color:#FF6600; font-size:0.9rem">WOMAN MODULE</div>
        <div class="magi-status {'status-approved' if estado_cas == '承 認' else 'status-denied'}">{estado_cas}</div>
        <div style="color:#888; font-size:0.8rem; margin-top:10px;">🌸 INTUITION | PRACTICALITY</div>
    </div>
    """, unsafe_allow_html=True)

# Panel de decisión
decision = get_majority_decision()
decision_class = "decision-approved" if decision == "APPROVED" else "decision-denied"
decision_color = "#00FFC8" if decision == "APPROVED" else "#FF0000"

st.markdown(f"""
<div class="decision-panel {decision_class}">
    <div style="font-size: 1.2rem; color: #aaa; margin-bottom: 10px;">> SYSTEM VERDICT (2/3 Majority Required)</div>
    <div class="decision-text" style="color: {decision_color};">{decision}</div>
    <div style="margin-top: 15px; color: #888; font-size: 0.9rem;">
        Voting Matrix: 
        <span style="color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000'}">MELCHIOR: {estado_mel}</span> | 
        <span style="color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000'}">BALTHASAR: {estado_bal}</span> | 
        <span style="color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000'}">CASPER: {estado_cas}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# --- RESPUESTAS ---
if (st.session_state.magi_responses["MELCHIOR"] or 
    st.session_state.magi_responses["BALTHASAR"] or 
    st.session_state.magi_responses["CASPER"]):
    
    with st.expander("📜 COMPLETE DELIBERATION RECORD", expanded=True):
        st.markdown("""
        <div style='color:#FF6600; font-family:"Share Tech Mono";'>
            > DELIBERATION RECORD LOADING...
            > ACCESSING NEURAL PATTERN ARCHIVES...
        </div>
        """, unsafe_allow_html=True)
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        if st.session_state.magi_responses["MELCHIOR"]:
            st.markdown(f"""
            <div class="response-card melchior-card">
                <div class="response-title">
                    <span>🔬 MELCHIOR-1</span>
                    <span style="color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000}'}">{estado_mel}</span>
                </div>
                <div class="response-content">{st.session_state.magi_responses["MELCHIOR"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res2:
        if st.session_state.magi_responses["BALTHASAR"]:
            st.markdown(f"""
            <div class="response-card balthasar-card">
                <div class="response-title">
                    <span>🛡️ BALTHASAR-2</span>
                    <span style="color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000}'}">{estado_bal}</span>
                </div>
                <div class="response-content">{st.session_state.magi_responses["BALTHASAR"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res3:
        if st.session_state.magi_responses["CASPER"]:
            st.markdown(f"""
            <div class="response-card casper-card">
                <div class="response-title">
                    <span>🌸 CASPER-3</span>
                    <span style="color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000}'}">{estado_cas}</span>
                </div>
                <div class="response-content">{st.session_state.magi_responses["CASPER"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Resolución final
    if st.session_state.magi_responses["FINAL"]:
        st.markdown(f"""
        <div class="response-card final-card">
            <div class="response-title">
                <span style="color: {decision_color}">>>> FINAL RESOLUTION <<<</span>
                <span style="color: {decision_color}; font-size: 1.2rem;">{decision}</span>
            </div>
            <div class="response-content">{st.session_state.magi_responses["FINAL"]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# --- DESCARGA PDF ---
if st.session_state.magi_responses["FINAL"]:
    st.markdown("""
    <div class="download-section">
        <div class="download-title">📄 DOWNLOAD DELIBERATION REPORT</div>
        <div class="download-instruction">⬇️ Click below for full MAGI report (PDF with authentication)</div>
    """, unsafe_allow_html=True)
    
    consecuencias_analysis = st.session_state.get("consecuencias", "")
    
    pdf_bytes = crear_pdf_evangelion(
        st.session_state.magi_responses["DILEMA"],
        st.session_state.magi_responses["MELCHIOR"],
        st.session_state.magi_responses["BALTHASAR"],
        st.session_state.magi_responses["CASPER"],
        st.session_state.magi_responses["FINAL"],
        consecuencias_analysis
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="⬇️ DOWNLOAD FULL REPORT (PDF)",
            data=pdf_bytes,
            file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- SIDEBAR MEJORADO ---
with st.sidebar:
    st.markdown("### 🔐 SYSTEM ACCESS")
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("✅ API: CONNECTED")
    else:
        api_key = st.text_input("GROQ API KEY", type="password", key="api_key_input")
        if not api_key:
            st.warning("⚠️ Enter API key to initialize")
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    
    # Configuración de análisis
    st.markdown("### ⚙️ ANALYSIS CONFIG")
    
    st.session_state.selected_format = st.selectbox(
        "📄 Output Format",
        ["Análisis Completo", "Informe Ejecutivo", "Correo Formal", "Resumen Ejecutivo"],
        help="Elige el formato de la resolución final"
    )
    
    st.session_state.enable_voice = st.checkbox("🔊 Enable Voice Synthesis", value=False)
    
    if st.button("🌐 Test Web Search", use_container_width=True):
        if WEB_SEARCH_AVAILABLE:
            test_query = st.session_state.get("last_query", "inteligencia artificial")
            with st.spinner("Searching..."):
                results = buscar_en_web(test_query)
                st.info(f"Search results:\n{results[:300]}...")
        else:
            st.error("Web search not available. Install requests and beautifulsoup4.")
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    
    # Historial
    st.markdown("### 📊 MISSION HISTORY")
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"MISSION {len(st.session_state.history)-i}"):
                st.write(f"**Time:** `{entry['timestamp']}`")
                st.write(f"**Decision:** `{entry['decision']}`")
                st.write(f"**Toxicity:** `{entry.get('toxicity', 'N/A')}%`")
    else:
        st.write("> No mission records")
    
    # Controles
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
            st.session_state.conversation_memory = []
            st.rerun()
    
    toxicity = st.slider("☣️ Toxicity Level", 0, 100, st.session_state.toxicity_level)
    st.session_state.toxicity_level = toxicity
    
    # Info sistema
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    st.markdown("### ℹ️ SYSTEM INFO")
    st.write(f"**Version:** `4.0`")
    st.write(f"**Memory:** `{len(st.session_state.history)} entries`")
    st.write(f"**TTS:** `{'ON' if st.session_state.enable_voice and TTS_AVAILABLE else 'OFF'}`")
    st.write(f"**Web Search:** `{'ON' if WEB_SEARCH_AVAILABLE else 'OFF'}`")

# --- INPUT PRINCIPAL ---
st.markdown("### > QUERY INPUT INTERFACE")
st.markdown("""
<div style='color:#FF6600; font-family:"Share Tech Mono"; margin-bottom:10px;'>
    > ENTER TACTICAL QUERY FOR MAGI ANALYSIS...
    > [Use #websearch at end to enable web search]
</div>
""", unsafe_allow_html=True)

dilema = st.chat_input("Type query here... (#websearch for online search)", key="query_input")

# --- PROCESAMIENTO PRINCIPAL ---
if dilema and api_key:
    st.session_state.last_query = dilema
    
    # Detectar si se requiere búsqueda web
    web_search_results = ""
    if "#websearch" in dilema.lower():
        dilema_limpio = dilema.replace("#websearch", "").strip()
        with st.spinner("🌐 Performing web search..."):
            web_search_results = buscar_en_web(dilema_limpio)
        dilema = dilema_limpio
    else:
        dilema_limpio = dilema
    
    with st.chat_message("user"):
        st.markdown(f"""
        <div style='color:#FF6600; font-family:"Share Tech Mono";'>
            > QUERY RECEIVED: "{dilema_limpio[:80]}..."
            > INITIATING DELIBERATION...
        </div>
        """, unsafe_allow_html=True)
    
    st.session_state.magi_responses["DILEMA"] = dilema_limpio
    
    # Construir contexto
    contexto_historico = construir_contexto_historico()
    restriccion_toxicidad = ajustar_tono_segun_toxicidad()
    
    # Añadir resultados de búsqueda web si existen
    if web_search_results:
        contexto_historico += f"\n{web_search_results}\n"
    
    try:
        client = Groq(api_key=api_key)
        
        with st.status("🔄 INITIATING MAGI DELIBERATION PROTOCOL...", expanded=True) as status:
            progress_bar = st.progress(0)
            
            progress_messages = [
                ("🔬 Consulting MELCHIOR-1 (Science Node)...", 25),
                ("🛡️ Consulting BALTHASAR-2 (Ethics Node)...", 50),
                ("🌸 Consulting CASPER-3 (Intuition Node)...", 75),
                ("⚡ Synthesizing final resolution...", 100)
            ]
            
            # PROCESAMIENTO EN PARALELO DE LAS 3 MAGI
            st.write("⚡ EXECUTING PARALLEL DELIBERATION...")
            m_resp, b_resp, c_resp = procesar_magi_paralelo(
                dilema_limpio, api_key, contexto_historico, restriccion_toxicidad
            )
            
            st.session_state.magi_responses["MELCHIOR"] = m_resp
            st.session_state.magi_responses["BALTHASAR"] = b_resp
            st.session_state.magi_responses["CASPER"] = c_resp
            progress_bar.progress(75)
            time.sleep(0.5)
            
            # VOTACIÓN BASADA EN CONTENIDO REAL
            st.session_state.magi_states["MELCHIOR"] = extraer_voto_desde_respuesta(m_resp)
            st.session_state.magi_states["BALTHASAR"] = extraer_voto_desde_respuesta(b_resp)
            st.session_state.magi_states["CASPER"] = extraer_voto_desde_respuesta(c_resp)
            
            # Actualizar decisión
            decision_actual = get_majority_decision()
            
            # SÍNTESIS FINAL CON FORMATO SELECCIONADO
            st.write(progress_messages[3][0])
            
            formato_prompt = {
                "Análisis Completo": "Proporciona un análisis detallado y completo.",
                "Informe Ejecutivo": "Proporciona un informe ejecutivo conciso, con puntos clave y recomendaciones.",
                "Correo Formal": "Redacta como un correo formal dirigido al comandante NERV.",
                "Resumen Ejecutivo": "Proporciona un resumen ejecutivo de máximo 200 palabras."
            }
            
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"""Eres el sistema MAGI integrado. Sintetiza resolución final basada en las tres perspectivas.
                    
                    CONTEXTO HISTÓRICO: {contexto_historico[:500]}
                    
                    PERSPECTIVAS:
                    1. CIENTÍFICA (Melchior-1): {m_resp[:800]}...
                    2. ÉTICA (Balthasar-2): {b_resp[:800]}...
                    3. INTUITIVA (Casper-3): {c_resp[:800]}...
                    
                    FORMATO SOLICITADO: {formato_prompt.get(st.session_state.selected_format, 'Análisis completo')}
                    
                    Decisión por mayoría: {decision_actual}
                    Nivel de toxicidad: {st.session_state.toxicity_level}%
                    
                    Proporciona resolución final clara. Responde en español."""},
                    {"role": "user", "content": "Proporciona la resolución final definitiva."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.4,
                max_tokens=2000,
                top_p=0.95
            )
            final_resp = completion.choices[0].message.content
            st.session_state.magi_responses["FINAL"] = final_resp
            progress_bar.progress(100)
            
            # ANÁLISIS DE CONSECUENCIAS (opcional, en segundo plano)
            st.write("🌳 Generating consequence analysis...")
            consecuencias = generar_consecuencias(decision_actual, dilema_limpio, client)
            st.session_state.consecuencias = consecuencias
            
            # SÍNTESIS DE VOZ (si está habilitada)
            if st.session_state.enable_voice and TTS_AVAILABLE:
                st.write("🔊 Synthesizing voice output...")
                asyncio.run(sintetizar_voz(final_resp[:500]))  # Límite para no saturar
            
            time.sleep(0.5)
            status.update(label="✅ DELIBERATION COMPLETE", state="complete", expanded=False)
        
        # Guardar en historial
        st.session_state.history.append({
            "dilema": dilema_limpio[:100],
            "resolucion": final_resp[:200],
            "states": st.session_state.magi_states.copy(),
            "decision": decision_actual,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "toxicity": st.session_state.toxicity_level,
            "format": st.session_state.selected_format
        })
        
        st.session_state.conversation_memory.append({
            "query": dilema_limpio,
            "decision": decision_actual,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # Actualizar toxicidad dinámicamente
        st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + random.randint(3, 10))
        
        st.markdown("""
        <div style='color:#FF6600; font-family:"Share Tech Mono"; text-align:center; margin:20px 0;'>
            > DELIBERATION CYCLE COMPLETE
            > SYSTEM READY FOR NEXT QUERY
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.5)
        st.rerun()
        
    except Exception as e:
        st.error(f"""
        <div style='color:#FF0000; font-family:"Share Tech Mono";'>
            > SYSTEM ERROR DETECTED
            > ERROR: {str(e)[:200]}
            > FALLBACK PROTOCOL INITIATED
        </div>
        """, unsafe_allow_html=True)
        
        # Fallback
        st.session_state.magi_responses["MELCHIOR"] = "⚠️ SYSTEM ERROR - Analysis unavailable"
        st.session_state.magi_responses["BALTHASAR"] = "⚠️ SYSTEM ERROR - Analysis unavailable"
        st.session_state.magi_responses["CASPER"] = "⚠️ SYSTEM ERROR - Analysis unavailable"
        st.session_state.magi_responses["FINAL"] = f"⚠️ SYSTEM ERROR: {str(e)[:200]}\nPlease verify API key and try again."

# --- FOOTER ---
st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='color:#888; font-family:"Share Tech Mono"; text-align:center; font-size:0.8em;'>
    > MAGI SYSTEM v4.0 | NERV COMMAND AUTHORIZED ACCESS ONLY
    > FEATURES: PARALLEL PROCESSING | VOICE SYNTHESIS | WEB SEARCH | CONSEQUENCE ANALYSIS
    > UNAUTHORIZED ACCESS WILL BE MET WITH TERMINAL COUNTERMEASURES
</div>
""", unsafe_allow_html=True)
