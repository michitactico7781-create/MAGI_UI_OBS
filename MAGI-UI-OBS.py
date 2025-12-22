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

# Almacenar respuestas completas
if "magi_responses" not in st.session_state:
    st.session_state.magi_responses = {
        "MELCHIOR": "",
        "BALTHASAR": "",
        "CASPER": "",
        "FINAL": ""
    }

# --- ESTILOS CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

.stApp {
    background-color: #050505;
    color: #ff6600;
    font-family: 'Orbitron', 'Share Tech Mono', monospace;
}

/* Títulos */
h1, h2, h3, h4 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ff6600 !important;
    text-shadow: 0 0 5px rgba(255, 102, 0, 0.5);
}

/* Tarjetas de respuestas permanentes */
.response-card {
    border: 2px solid;
    background: rgba(20, 10, 0, 0.9);
    padding: 20px;
    margin: 15px 0;
    min-height: 200px;
    overflow-y: auto;
}

.melchior-card { border-color: #0099FF; }
.balthasar-card { border-color: #00FFC8; }
.casper-card { border-color: #FF6600; }
.final-card { border-color: #FF0000; }

.response-title {
    font-size: 1.3em;
    border-bottom: 2px solid;
    margin-bottom: 15px;
    padding-bottom: 8px;
    font-weight: bold;
}

/* Hexágonos MAGI */
.magi-hexagon {
    padding: 15px;
    margin: 10px;
    text-align: center;
    background: rgba(0, 153, 255, 0.1);
    border: 2px solid #0099FF;
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
    height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.magi-name {
    font-size: 1.1rem;
    color: #0099FF;
    font-weight: bold;
    margin-bottom: 5px;
}

.magi-status {
    font-size: 1.8rem;
    font-weight: bold;
    margin-top: 10px;
    font-family: 'MS Gothic', monospace;
}

.status-approved {
    color: #00FFC8;
    text-shadow: 0 0 8px rgba(0, 255, 200, 0.5);
}

.status-denied {
    color: #FF0000;
    text-shadow: 0 0 8px rgba(255, 0, 0, 0.5);
}

/* Panel de decisión */
.decision-panel {
    background: rgba(0, 20, 40, 0.8);
    border: 3px solid;
    padding: 25px;
    margin: 25px 0;
    text-align: center;
}

.decision-approved {
    border-color: #00FFC8;
    background: rgba(0, 255, 200, 0.1);
}

.decision-denied {
    border-color: #FF0000;
    background: rgba(255, 0, 0, 0.1);
}

.decision-text {
    font-size: 2rem;
    font-weight: 900;
    margin: 10px 0;
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
    box-shadow: 0 0 15px #ff6600;
}

/* Inputs */
.stTextInput > div > div > input,
.stChatInput > div > div > textarea {
    background-color: rgba(10, 10, 10, 0.9) !important;
    color: #ff6600 !important;
    border: 2px solid #ff6600 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Línea decorativa */
.deco-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #ff6600, transparent);
    margin: 20px 0;
}

/* Contenedor de texto */
.text-container {
    background: rgba(0, 0,
