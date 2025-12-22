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
