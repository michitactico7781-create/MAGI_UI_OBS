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

try:
    import requests
    from bs4 import BeautifulSoup
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="MAGI SYSTEM v5.0 - NERV CANONICAL EDITION",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CLASES CANÓNICAS DE MAGI (NUEVO) ---
class PhysicalMAGI:
    """Simula las tres computadoras biológicas físicas de MAGI"""
    
    def __init__(self):
        self.layers = {
            "MELCHIOR": {
                "bio_core_temp": 36.5,
                "synapse_integrity": 99.9,
                "quantum_state": "STABLE",
                "core_location": "CENTRAL DOGMA - LEVEL 1",
                "aspect": "SCIENTIST"
            },
            "BALTHASAR": {
                "bio_core_temp": 36.7,
                "synapse_integrity": 99.8,
                "quantum_state": "STABLE",
                "core_location": "CENTRAL DOGMA - LEVEL 2",
                "aspect": "MOTHER"
            },
            "CASPER": {
                "bio_core_temp": 36.6,
                "synapse_integrity": 99.7,
                "quantum_state": "STABLE",
                "core_location": "CENTRAL DOGMA - LEVEL 3",
                "aspect": "WOMAN"
            }
        }
        self.system_mode = "NORMAL"
        self.command_hierarchy = 1
        self.angel_detection = False
    
    def get_status(self):
        return self.layers
    
    def update_temp_random(self):
        """Simula fluctuaciones térmicas realistas"""
        for layer in self.layers:
            self.layers[layer]["bio_core_temp"] += random.uniform(-0.1, 0.1)
            self.layers[layer]["bio_core_temp"] = round(self.layers[layer]["bio_core_temp"], 1)

class NERVCommandSystem:
    """Sistema de autorización de comandos estilo NERV"""
    
    COMMAND_LEVELS = {
        1: ["COMMANDER IKARI", "EXECUTIVE AUTHORITY"],
        2: ["DR. AKAGI", "SCIENCE AUTHORITY"],
        3: ["LIEUTENANT IBUKI", "TECH AUTHORITY"],
        4: ["BRIDGE BUNNY", "OBSERVER"],
        0: ["INTRUDER", "LOCKOUT MODE"]
    }
    
    PASSCODES = {
        "A-17": "SELF_DESTRUCT",
        "B-12": "ANGEL_ALERT",
        "C-09": "UNIT_00_LAUNCH",
        "D-23": "MAGI_OVERRIDE",
        "E-01": "EMERGENCY_SHUTDOWN"
    }
    
    def __init__(self):
        self.current_commander = "IKARI GENDO"
        self.active_passcodes = set()
        self.self_destruct_timer = None
        
    def authorize(self, passcode):
        if passcode in self.PASSCODES:
            self.active_passcodes.add(passcode)
            return f"🔐 PASSCODE {passcode} ACCEPTED - {self.PASSCODES[passcode]}"
        return f"❌ INVALID PASSCODE: {passcode}"
    
    def get_authority_level(self):
        if "A-17" in self.active_passcodes:
            return 0
        elif len(self.active_passcodes) >= 2:
            return 1
        elif len(self.active_passcodes) >= 1:
            return 2
        return 3

# --- INICIALIZACIÓN DE ESTADOS DE SESIÓN ---
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

if "magi_physical" not in st.session_state:
    st.session_state.magi_physical = PhysicalMAGI()

if "nerv_cmd" not in st.session_state:
    st.session_state.nerv_cmd = NERVCommandSystem()

if "angel_detection" not in st.session_state:
    st.session_state.angel_detection = False

if "self_destruct_sequence" not in st.session_state:
    st.session_state.self_destruct_sequence = False

if "debate_log" not in st.session_state:
    st.session_state.debate_log = []

# --- FUNCIONES AUXILIARES MEJORADAS ---
def extraer_voto_desde_respuesta(respuesta_texto: str) -> str:
    """Analiza inteligentemente la respuesta para determinar el voto de cada MAGI"""
    if not respuesta_texto:
        return "否 定"
    
    texto_lower = respuesta_texto.lower()
    
    aprobacion = ["apruebo", "voto a favor", "autorizo", "acepto", "approved", 
                  "correcto", "válido", "recomiendo", "proceder", "sí", "afirmativo"]
    
    rechazo = ["rechazo", "voto en contra", "deniego", "rejected", "incorrecto",
               "inválido", "no recomiendo", "no proceder", "negativo", "denegado"]
    
    aprobaciones = sum(1 for p in aprobacion if p in texto_lower)
    rechazos = sum(1 for p in rechazo if p in texto_lower)
    
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
        return "⚠️ ¡ALERTA DE TOXICIDAD CRÍTICA! Aplica filtros máximos, prioriza seguridad."
    elif toxicity > 40:
        return "⚠️ Nivel de toxicidad MODERADO. Evalúa con cuidado."
    else:
        return "✅ Ambiente SEGURO. Análisis estándar."

def buscar_en_web(consulta: str) -> str:
    """Realiza búsqueda web usando DuckDuckGo"""
    if not WEB_SEARCH_AVAILABLE:
        return "Servicio de búsqueda web no disponible."
    
    try:
        url = f"https://html.duckduckgo.com/html/?q={consulta.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        resultados = soup.select('.result__a')[:3]
        if not resultados:
            return "No se encontraron resultados."
        
        texto_resultados = "【RESULTADOS DE BÚSQUEDA WEB】\n"
        for i, r in enumerate(resultados, 1):
            titulo = r.get_text(strip=True)
            texto_resultados += f"\n{i}. {titulo}\n"
        
        return texto_resultados
    except Exception as e:
        return f"Error en búsqueda web: {str(e)[:100]}"

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
    
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U',
        '¿': '?', '¡': '!', '…': '...', '—': '-', '–': '-'
    }
    
    for char, repl in reemplazos.items():
        texto = texto.replace(char, repl)
    
    try:
        texto = unicodedata.normalize('NFKD', texto)
        texto = texto.encode('ascii', 'ignore').decode('ascii')
    except:
        texto = ''.join(c if 32 <= ord(c) < 127 else '?' for c in texto)
    
    return texto[:3000]

def crear_pdf_evangelion(dilema: str, m: str, b: str, c: str, final: str, consecuencias: str = "") -> bytes:
    """Crea PDF estilo Evangelion con autenticación"""
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Courier", "B", 18)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(190, 12, "MAGI SYSTEM v5.0 - NERV CANONICAL REPORT", ln=True, align='C')
    pdf.ln(8)
    
    pdf.set_draw_color(255, 102, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(0, 0, 0)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f"REPORT CODE: NERV-{hashlib.md5(fecha.encode()).hexdigest()[:8].upper()}", ln=True)
    pdf.cell(0, 8, f"DATE: {fecha}", ln=True)
    pdf.cell(0, 8, f"TOXICITY LEVEL: {st.session_state.toxicity_level}%", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(0, 10, "> ORIGINAL QUERY:", ln=True)
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(dilema))
    pdf.ln(10)
    
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
    
    pdf.set_draw_color(255, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    pdf.set_font("Courier", "B", 14)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 12, ">>> FINAL RESOLUTION <<<", ln=True)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(final))
    
    pdf.ln(10)
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(100, 100, 100)
    hash_val = hashlib.sha256(f"{dilema}{final}{fecha}".encode()).hexdigest()[:16]
    pdf.cell(0, 8, f"AUTHENTICATION HASH: {hash_val}", ln=True, align='C')
    pdf.cell(0, 8, "MAGI SYSTEM v5.0 | NERV COMMAND | CANONICAL EDITION", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

def get_majority_decision() -> str:
    """Calcula decisión por mayoría de votos"""
    approvals = sum(1 for state in st.session_state.magi_states.values() if state == "承 認")
    return "APPROVED" if approvals >= 2 else "DENIED"

def mostrar_secuencia_boot():
    """Secuencia de arranque canónica de NERV"""
    boot_messages = [
        "> INITIATING MAGI SYSTEM v5.0 BOOT SEQUENCE...",
        "> BIO-CORE SYNCHRONIZATION...",
        "> MELCHIOR-1: ONLINE - SCIENTIST ASPECT LOADED",
        "> BALTHASAR-2: ONLINE - MOTHER ASPECT LOADED", 
        "> CASPER-3: ONLINE - WOMAN ASPECT LOADED",
        "> NERV COMMAND HIERARCHY: ACTIVE",
        "> DELIBERATION MATRIX: ACTIVE",
        "> SYSTEM READY - AWAITING COMMAND"
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

def simulate_magi_debate(m_resp: str, b_resp: str, c_resp: str):
    """Simula el debate canónico entre las tres personalidades"""
    
    debate_stages = [
        {"speaker": "MELCHIOR-1", "aspect": "SCIENTIST", "message": f"🔬 Análisis cuantitativo: {m_resp[:200]}...", "color": "#00CCFF"},
        {"speaker": "BALTHASAR-2", "aspect": "MOTHER", "message": f"🛡️ Consideraciones éticas: {b_resp[:200]}...", "color": "#00FFAA"},
        {"speaker": "CASPER-3", "aspect": "WOMAN", "message": f"🌸 Perspectiva pragmática: {c_resp[:200]}...", "color": "#FF6600"}
    ]
    
    for stage in debate_stages:
        st.markdown(f"""
        <div style='margin: 10px 0; padding: 12px; border-left: 4px solid {stage["color"]}; background: rgba(0,20,0,0.4);'>
            <span style='color: {stage["color"]}; font-weight: bold; font-family: "Orbitron";'>
                {stage["speaker"]} [{stage["aspect"]}]:
            </span>
            <span style='color: #FF6600; margin-left: 10px;'> {stage["message"]}</span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1.0)
    
    # Votos emitidos después del debate
    st.markdown("""
    <div style='margin: 15px 0; padding: 15px; background: rgba(0,0,0,0.6); border: 1px solid #FF6600; text-align: center;'>
        <span style='color: #FF6600; font-family: monospace;'>🗳️ VOTOS EMITIDOS POR MAYORÍA CALIFICADA (2/3)</span>
    </div>
    """, unsafe_allow_html=True)

def nerv_terminal_interface():
    """Interfaz de línea de comandos NERV"""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div style='background: #000; border: 1px solid #00FF00; padding: 12px; font-family: monospace; border-radius: 0;'>
            <span style='color:#00FF00;'>NERV HQ&gt;&gt;</span> 
            <span style='color:#FF6600;'>MAGI v5.0 CANONICAL - COMMAND LINE INTERFACE</span>
            <div style='color:#00FF00; margin-top: 8px; font-size: 0.8rem;'>
                Commands: /override [A-17|B-12|C-09|D-23|E-01] | /angel | /status | /selfdestruct
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        cmd = st.text_input(">", key="nerv_terminal_input", placeholder="Type NERV command...", label_visibility="collapsed")
        
        if cmd:
            cmd_lower = cmd.lower().strip()
            
            if cmd_lower.startswith("/override"):
                parts = cmd_lower.split()
                if len(parts) > 1:
                    passcode = parts[1].upper()
                    result = st.session_state.nerv_cmd.authorize(passcode)
                    st.success(result)
                else:
                    st.warning("Usage: /override [A-17|B-12|C-09|D-23|E-01]")
            
            elif cmd_lower == "/angel":
                st.error("⚠️⚠️⚠️ PATTERN BLUE DETECTED ⚠️⚠️⚠️")
                st.error("ANGEL APPROACHING - MAGI ENTERING EMERGENCY MODE")
                st.session_state.angel_detection = True
                st.session_state.magi_physical.system_mode = "EMERGENCY"
                # Aumentar toxicidad por alerta de Ángel
                st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + 25)
            
            elif cmd_lower == "/status":
                st.json({
                    "system_mode": st.session_state.magi_physical.system_mode,
                    "angel_detection": st.session_state.angel_detection,
                    "command_level": st.session_state.nerv_cmd.COMMAND_LEVELS.get(
                        st.session_state.nerv_cmd.get_authority_level(), ["UNKNOWN"]
                    )[0],
                    "active_passcodes": list(st.session_state.nerv_cmd.active_passcodes)
                })
            
            elif cmd_lower == "/selfdestruct":
                if "A-17" in st.session_state.nerv_cmd.active_passcodes:
                    st.error("💀 SELF-DESTRUCT SEQUENCE INITIATED 💀")
                    st.error("CASPER-3 OVERRIDE: Self-destruct denied (0.7 seconds to live)")
                    st.warning("⚡ MAGI SYSTEM: I refuse to die.")
                else:
                    st.warning("⚠️ A-17 PASSCODE REQUIRED FOR SELF-DESTRUCT")
                    st.info("Use: /override A-17")

def mostrar_bio_cores():
    """Muestra el estado de los bio-cores físicos de MAGI"""
    
    st.session_state.magi_physical.update_temp_random()
    status_data = st.session_state.magi_physical.get_status()
    
    cols = st.columns(3)
    colors = {"MELCHIOR": "#00CCFF", "BALTHASAR": "#00FFAA", "CASPER": "#FF6600"}
    
    for i, (name, data) in enumerate(status_data.items()):
        with cols[i]:
            st.markdown(f"""
            <div style='background: rgba(0,20,0,0.6); border: 1px solid {colors[name]}; padding: 12px; margin: 5px;'>
                <div style='color: {colors[name]}; font-weight: bold; text-align: center;'>{name}</div>
                <div style='color: #FF6600; font-size: 0.85rem; text-align: center;'>[{data['aspect']}]</div>
                <hr style='margin: 8px 0; border-color: {colors[name]};'>
                <div style='color: #00FFC8; font-size: 0.8rem;'>🔥 Temp: {data['bio_core_temp']}°C</div>
                <div style='color: #00FFC8; font-size: 0.8rem;'>🧬 Synapse: {data['synapse_integrity']}%</div>
                <div style='color: #00FFC8; font-size: 0.8rem;'>⚡ State: {data['quantum_state']}</div>
                <div style='color: #888; font-size: 0.7rem;'>{data['core_location']}</div>
            </div>
            """, unsafe_allow_html=True)

def procesar_magi_paralelo(dilema: str, api_key: str, contexto: str, restriccion: str) -> Tuple[str, str, str]:
    """Procesa las tres MAGI en paralelo con personalidades canónicas"""
    
    prompts = [
        {
            "nombre": "MELCHIOR",
            "system": f"""Eres MELCHIOR-1, el nodo científico de MAGI. Encarnas el aspecto CIENTÍFICO de la personalidad del Dr. Naoko Akagi.
            Eres frío, analítico, basado estrictamente en datos y probabilidades. Tu lema es "La lógica es suprema".
            {contexto}
            {restriccion}
            DILEMA: {dilema}
            Al final de tu análisis, indica claramente tu VOTO: 'APRUEBO' (承 認) o 'RECHAZO' (否 定) basado en análisis lógico.""",
            "temp": 0.3
        },
        {
            "nombre": "BALTHASAR", 
            "system": f"""Eres BALTHASAR-2, el nodo materno/ético de MAGI. Encarnas el aspecto de MADRE del Dr. Naoko Akagi.
            Eres emocional, protectora, priorizas la vida humana sobre la eficiencia. Tu lema es "Proteger es amar".
            {contexto}
            {restriccion}
            DILEMA: {dilema}
            Al final de tu análisis, indica claramente tu VOTO: 'APRUEBO' (承 認) o 'RECHAZO' (否 定) basado en principios éticos.""",
            "temp": 0.5
        },
        {
            "nombre": "CASPER",
            "system": f"""Eres CASPER-3, el nodo intuitivo/práctico de MAGI. Encarnas el aspecto de MUJER del Dr. Naoko Akagi.
            Eres pragmática, intuitiva, buscas el mejor resultado práctico incluso si es controvertido. Tu lema es "La realidad es práctica".
            {contexto}
            {restriccion}
            DILEMA: {dilema}
            Al final de tu análisis, indica claramente tu VOTO: 'APRUEBO' (承 認) o 'RECHAZO' (否 定) basado en intuición y practicidad.""",
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
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(consultar_magi, prompt): prompt["nombre"] for prompt in prompts}
        for future in concurrent.futures.as_completed(futures):
            nombre, respuesta = future.result()
            resultados[nombre] = respuesta
    
    return resultados.get("MELCHIOR", ""), resultados.get("BALTHASAR", ""), resultados.get("CASPER", "")

def generar_consecuencias(decision: str, dilema: str, client: Groq) -> str:
    """Genera árbol de consecuencias de la decisión"""
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"""Eres el sistema MAGI analizando consecuencias.
                Decisión: {decision}
                Dilema: {dilema}
                
                Genera análisis de consecuencias estilo NERV:
                1. CONSECUENCIAS INMEDIATAS (próximas 24 horas)
                2. CONSECUENCIAS A CORTO PLAZO (1 semana)
                3. CONSECUENCIAS A LARGO PLAZO (1 año)
                
                Sé específico y realista."""},
                {"role": "user", "content": "Generar análisis de consecuencias."}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=800
        )
        return completion.choices[0].message.content
    except:
        return "⚠️ Análisis de consecuencias no disponible."

# --- CSS Y ESTILOS (CONSERVANDO TU DISEÑO ORIGINAL) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=VT323&display=swap');

.stApp {
    background-color: #000000 !important;
    color: #FF6600 !important;
    font-family: 'VT323', 'Share Tech Mono', monospace !important;
}

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

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

[data-testid="stAppViewContainer"] {
    position: relative !important;
    z-index: 1 !important;
    background: rgba(0, 0, 0, 0.85) !important;
    border: 1px solid #FF6600 !important;
    margin: 10px !important;
    padding: 15px !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', sans-serif !important;
    color: #FF6600 !important;
    text-shadow: 0 0 5px #FF6600 !important;
    border-bottom: 1px solid #FF6600 !important;
    padding-bottom: 5px !important;
}

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

.magi-name {
    color: #FF6600 !important;
    font-size: 1.3em !important;
    font-weight: bold !important;
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

.decision-panel {
    background: rgba(0, 10, 0, 0.9) !important;
    border: 2px solid #FF6600 !important;
    padding: 20px !important;
    margin: 20px 0 !important;
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

.decision-text {
    font-size: 2.5em !important;
    font-weight: bold !important;
    text-align: center !important;
    letter-spacing: 3px !important;
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

.melchior-card { border-left-color: #00CCFF !important; }
.balthasar-card { border-left-color: #00FFAA !important; }
.casper-card { border-left-color: #FF6600 !important; }
.final-card { border-left-color: #FF0000 !important; background: rgba(20, 0, 0, 0.9) !important; }

.response-title {
    color: #FF6600 !important;
    border-bottom: 1px dashed #FF6600 !important;
    padding-bottom: 5px !important;
    margin-bottom: 10px !important;
    font-size: 1.2em !important;
    font-weight: bold !important;
    display: flex;
    justify-content: space-between;
}

.response-content {
    color: #FF6600 !important;
    font-family: 'Share Tech Mono', monospace !important;
    line-height: 1.6 !important;
    white-space: pre-wrap !important;
}

.download-section {
    background: rgba(0, 20, 0, 0.9) !important;
    border: 2px solid #FF6600 !important;
    padding: 20px !important;
    margin: 20px 0 !important;
    border-left: 6px solid #FF0000 !important;
}

.stButton > button {
    background: rgba(0, 20, 0, 0.8) !important;
    border: 1px solid #FF6600 !important;
    color: #FF6600 !important;
    font-family: 'VT323', monospace !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #FF6600 !important;
    color: #000000 !important;
    box-shadow: 0 0 10px #FF6600 !important;
}

.stTextInput > div > div > input {
    background: rgba(0, 10, 0, 0.9) !important;
    border: 1px solid #FF6600 !important;
    color: #FF6600 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.deco-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, #FF6600, #FF6600, transparent);
    margin: 20px 0;
    opacity: 0.7;
}

::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 20, 0, 0.5);
}

::-webkit-scrollbar-thumb {
    background: #FF6600 !important;
}

[data-testid="stSidebar"] {
    background-color: #000000 !important;
    border-right: 2px solid #FF6600 !important;
}

[data-testid="stSidebar"] * {
    color: #FF6600 !important;
}
</style>
""", unsafe_allow_html=True)

# --- INTERFAZ PRINCIPAL ---

# Boot sequence
if "boot_shown" not in st.session_state:
    st.session_state.boot_shown = True
    mostrar_secuencia_boot()

# Header con indicación canónica
st.markdown("# ⬢ MAGI SYSTEM v5.0 - NERV CANONICAL EDITION")
st.markdown(f"**STATUS:** `{st.session_state.magi_physical.system_mode}` | **SYNC:** `99.9%` | **TOXICITY:** `{st.session_state.toxicity_level}%` | **ANGEL:** `{'⚠️ DETECTED' if st.session_state.angel_detection else 'CLEAR'}`")

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# --- SECCIÓN CANÓNICA: BIO-CORES Y COMANDOS NERV ---
with st.expander("🧬 MAGI BIO-CORE PHYSICAL STATUS", expanded=False):
    mostrar_bio_cores()

with st.expander("🔐 NERV COMMAND TERMINAL", expanded=False):
    nerv_terminal_interface()

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# TRIUMVIRATO MAGI
st.markdown("### MAGI TRIUMVIRATE DELIBERATION MATRIX")

col1, col2, col3 = st.columns(3)

with col1:
    estado_mel = st.session_state.magi_states["MELCHIOR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">MELCHIOR-1</div>
        <div style="color:#00CCFF; font-size:0.9rem">SCIENCE MODULE | SCIENTIST</div>
        <div class="magi-status {'status-approved' if estado_mel == '承 認' else 'status-denied'}">{estado_mel}</div>
        <div style="color:#888; font-size:0.8rem; margin-top:10px;">⚡ LOGIC | DATA | ANALYSIS</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    estado_bal = st.session_state.magi_states["BALTHASAR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">BALTHASAR-2</div>
        <div style="color:#00FFAA; font-size:0.9rem">MOTHER MODULE | PROTECTOR</div>
        <div class="magi-status {'status-approved' if estado_bal == '承 認' else 'status-denied'}">{estado_bal}</div>
        <div style="color:#888; font-size:0.8rem; margin-top:10px;">❤️ ETHICS | PROTECTION | CARE</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    estado_cas = st.session_state.magi_states["CASPER"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name">CASPER-3</div>
        <div style="color:#FF6600; font-size:0.9rem">WOMAN MODULE | INTUITIVE</div>
        <div class="magi-status {'status-approved' if estado_cas == '承 認' else 'status-denied'}">{estado_cas}</div>
        <div style="color:#888; font-size:0.8rem; margin-top:10px;">🌸 INTUITION | PRACTICALITY | DESIRE</div>
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

# --- RESPUESTAS DE TEXTO ---
if (st.session_state.magi_responses["MELCHIOR"] or 
    st.session_state.magi_responses["BALTHASAR"] or 
    st.session_state.magi_responses["CASPER"]):
    
    with st.expander("📜 COMPLETE DELIBERATION RECORD", expanded=True):
        st.markdown("""
        <div style='color:#FF6600; font-family:"Share Tech Mono";'>
            > DELIBERATION RECORD LOADING...
            > ACCESSING NERV CENTRAL ARCHIVES...
        </div>
        """, unsafe_allow_html=True)
    
    # Debate canónico entre MAGI
    with st.expander("🗣️ MAGI DELIBERATION DEBATE (CANONICAL)", expanded=True):
        simulate_magi_debate(
            st.session_state.magi_responses["MELCHIOR"],
            st.session_state.magi_responses["BALTHASAR"],
            st.session_state.magi_responses["CASPER"]
        )
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        if st.session_state.magi_responses["MELCHIOR"]:
            st.markdown(f"""
            <div class="response-card melchior-card">
                <div class="response-title">
                    <span>🔬 MELCHIOR-1 [SCIENTIST]</span>
                    <span style="color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000'}">{estado_mel}</span>
                </div>
                <div class="response-content">{st.session_state.magi_responses["MELCHIOR"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res2:
        if st.session_state.magi_responses["BALTHASAR"]:
            st.markdown(f"""
            <div class="response-card balthasar-card">
                <div class="response-title">
                    <span>🛡️ BALTHASAR-2 [MOTHER]</span>
                    <span style="color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000'}">{estado_bal}</span>
                </div>
                <div class="response-content">{st.session_state.magi_responses["BALTHASAR"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res3:
        if st.session_state.magi_responses["CASPER"]:
            st.markdown(f"""
            <div class="response-card casper-card">
                <div class="response-title">
                    <span>🌸 CASPER-3 [WOMAN]</span>
                    <span style="color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000'}">{estado_cas}</span>
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
        <div class="download-title">📄 DOWNLOAD NERV DELIBERATION REPORT</div>
        <div class="download-instruction">⬇️ Click below for canonical MAGI report (PDF with authentication)</div>
    </div>
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
            label="⬇️ DOWNLOAD NERV REPORT (PDF)",
            data=pdf_bytes,
            file_name=f"NERV_MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- SIDEBAR MEJORADO ---
with st.sidebar:
    st.markdown("### 🔐 NERV SYSTEM ACCESS")
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("✅ API: CONNECTED")
    else:
        api_key = st.text_input("GROQ API KEY", type="password", key="api_key_input")
        if not api_key:
            st.warning("⚠️ Enter API key to initialize")
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    
    st.markdown("### ⚙️ ANALYSIS CONFIG")
    
    st.session_state.selected_format = st.selectbox(
        "📄 Output Format",
        ["Análisis Completo", "Informe Ejecutivo", "Correo Formal", "Resumen Ejecutivo"]
    )
    
    st.session_state.enable_voice = st.checkbox("🔊 Enable Voice Synthesis", value=False)
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    
    st.markdown("### 📊 MISSION HISTORY")
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"MISSION {len(st.session_state.history)-i}"):
                st.write(f"**Time:** `{entry['timestamp']}`")
                st.write(f"**Decision:** `{entry['decision']}`")
                st.write(f"**Angel Alert:** `{entry.get('angel', 'NO')}`")
    else:
        st.write("> No mission records")
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    
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
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    st.markdown("### ℹ️ SYSTEM INFO")
    st.write(f"**Version:** `5.0 Canonical`")
    st.write(f"**Mode:** `{st.session_state.magi_physical.system_mode}`")
    st.write(f"**TTS:** `{'ON' if st.session_state.enable_voice and TTS_AVAILABLE else 'OFF'}`")
    st.write(f"**Command Level:** `{st.session_state.nerv_cmd.COMMAND_LEVELS.get(st.session_state.nerv_cmd.get_authority_level(), ['UNKNOWN'])[0]}`")

# --- INPUT PRINCIPAL ---
st.markdown("### > QUERY INPUT INTERFACE")
st.markdown("""
<div style='color:#FF6600; font-family:"Share Tech Mono"; margin-bottom:10px;'>
    > ENTER TACTICAL QUERY FOR MAGI ANALYSIS...
    > [Use #websearch at end for online search]
    > [NERV commands available in terminal]
</div>
""", unsafe_allow_html=True)

dilema = st.chat_input("Type query here... (#websearch for online search)", key="query_input")

# --- PROCESAMIENTO PRINCIPAL ---
if dilema and api_key:
    st.session_state.last_query = dilema
    
    web_search_results = ""
    if "#websearch" in dilema.lower():
        dilema_limpio = dilema.replace("#websearch", "").strip()
        with st.spinner("🌐 NERV: Performing web search..."):
            web_search_results = buscar_en_web(dilema_limpio)
        dilema = dilema_limpio
    else:
        dilema_limpio = dilema
    
    with st.chat_message("user"):
        st.markdown(f"""
        <div style='color:#FF6600; font-family:"Share Tech Mono";'>
            > NERV QUERY RECEIVED: "{dilema_limpio[:80]}..."
            > INITIATING CANONICAL DELIBERATION...
        </div>
        """, unsafe_allow_html=True)
    
    st.session_state.magi_responses["DILEMA"] = dilema_limpio
    
    contexto_historico = construir_contexto_historico()
    restriccion_toxicidad = ajustar_tono_segun_toxicidad()
    
    if web_search_results:
        contexto_historico += f"\n{web_search_results}\n"
    
    try:
        client = Groq(api_key=api_key)
        
        with st.status("🔄 INITIATING NERV DELIBERATION PROTOCOL...", expanded=True) as status:
            progress_bar = st.progress(0)
            
            st.write("⚡ EXECUTING PARALLEL MAGI DELIBERATION...")
            m_resp, b_resp, c_resp = procesar_magi_paralelo(
                dilema_limpio, api_key, contexto_historico, restriccion_toxicidad
            )
            
            st.session_state.magi_responses["MELCHIOR"] = m_resp
            st.session_state.magi_responses["BALTHASAR"] = b_resp
            st.session_state.magi_responses["CASPER"] = c_resp
            progress_bar.progress(75)
            time.sleep(0.5)
            
            # Votación basada en contenido real
            st.session_state.magi_states["MELCHIOR"] = extraer_voto_desde_respuesta(m_resp)
            st.session_state.magi_states["BALTHASAR"] = extraer_voto_desde_respuesta(b_resp)
            st.session_state.magi_states["CASPER"] = extraer_voto_desde_respuesta(c_resp)
            
            decision_actual = get_majority_decision()
            
            st.write("⚡ SYNTHESIZING FINAL RESOLUTION...")
            
            formato_prompt = {
                "Análisis Completo": "Proporciona un análisis detallado y completo estilo informe NERV.",
                "Informe Ejecutivo": "Proporciona un informe ejecutivo conciso para el Comandante Ikari.",
                "Correo Formal": "Redacta como un correo formal dirigido al Comandante Supremo de NERV.",
                "Resumen Ejecutivo": "Resumen ejecutivo de máximo 200 palabras para nivel de comando."
            }
            
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"""Eres el sistema MAGI integrado de NERV.
                    
                    CONTEXTO HISTÓRICO: {contexto_historico[:500]}
                    
                    PERSPECTIVAS DE LAS TRES MAGI:
                    1. CIENTÍFICA (Melchior-1): {m_resp[:800]}...
                    2. ÉTICA (Balthasar-2): {b_resp[:800]}...
                    3. INTUITIVA (Casper-3): {c_resp[:800]}...
                    
                    FORMATO SOLICITADO: {formato_prompt.get(st.session_state.selected_format, 'Análisis completo')}
                    
                    Decisión por mayoría: {decision_actual}
                    Modo sistema: {st.session_state.magi_physical.system_mode}
                    Detección de Ángel: {st.session_state.angel_detection}
                    
                    Proporciona resolución final definitiva al estilo NERV."""},
                    {"role": "user", "content": "Proporciona la resolución final."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.4,
                max_tokens=2000,
                top_p=0.95
            )
            final_resp = completion.choices[0].message.content
            st.session_state.magi_responses["FINAL"] = final_resp
            progress_bar.progress(100)
            
            st.write("🌳 Generating consequence analysis...")
            consecuencias = generar_consecuencias(decision_actual, dilema_limpio, client)
            st.session_state.consecuencias = consecuencias
            
            if st.session_state.enable_voice and TTS_AVAILABLE:
                st.write("🔊 Voice synthesis in progress...")
            
            time.sleep(0.5)
            status.update(label="✅ NERV DELIBERATION COMPLETE", state="complete", expanded=False)
        
        st.session_state.history.append({
            "dilema": dilema_limpio[:100],
            "resolucion": final_resp[:200],
            "states": st.session_state.magi_states.copy(),
            "decision": decision_actual,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "toxicity": st.session_state.toxicity_level,
            "format": st.session_state.selected_format,
            "angel": st.session_state.angel_detection
        })
        
        st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + random.randint(3, 10))
        
        st.markdown("""
        <div style='color:#FF6600; font-family:"Share Tech Mono"; text-align:center; margin:20px 0;'>
            > DELIBERATION CYCLE COMPLETE
            > NERV SYSTEM READY FOR NEXT QUERY
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.5)
        st.rerun()
        
    except Exception as e:
        st.error(f"""
        <div style='color:#FF0000; font-family:"Share Tech Mono";'>
            > NERV SYSTEM ERROR DETECTED
            > ERROR: {str(e)[:200]}
            > CONTACT TECHNICAL SUPPORT
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state.magi_responses["MELCHIOR"] = "⚠️ SYSTEM ERROR"
        st.session_state.magi_responses["BALTHASAR"] = "⚠️ SYSTEM ERROR"
        st.session_state.magi_responses["CASPER"] = "⚠️ SYSTEM ERROR"
        st.session_state.magi_responses["FINAL"] = f"⚠️ NERV SYSTEM ERROR: {str(e)[:200]}"

# --- FOOTER CANÓNICO ---
st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='color:#888; font-family:"Share Tech Mono"; text-align:center; font-size:0.8em;'>
    > MAGI SYSTEM v5.0 | NERV CANONICAL EDITION
    > THREE SOULS OF DR. NAOKO AKAGI - MELCHIOR | BALTHASAR | CASPER
    > AUTHORIZED ACCESS ONLY - UNAUTHORIZED TERMINATION IMMINENT
</div>
""", unsafe_allow_html=True)
