import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime
import time
import unicodedata
import random
import re
import json
import os
import subprocess
import tempfile
import base64
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import requests
from collections import deque
import hashlib

# ============================================
# CONFIGURACIÓN INICIAL MEJORADA
# ============================================
st.set_page_config(
    page_title="MAGI SYSTEM v4.0: AWAKENING",
    page_icon="⬢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# SISTEMA DE TIPOS Y ENUMS
# ============================================
class NodeType(Enum):
    MELCHIOR = "MELCHIOR-1"
    BALTHASAR = "BALTHASAR-2"
    CASPER = "CASPER-3"
    INTEGRATED = "INTEGRATED"

class DecisionType(Enum):
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    UNCERTAIN = "UNCERTAIN"
    NEEDS_MORE_DATA = "NEEDS_MORE_DATA"

class ActionType(Enum):
    SEARCH_WEB = "search_web"
    ANALYZE_DATA = "analyze_data"
    EXECUTE_CODE = "execute_code"
    GENERATE_REPORT = "generate_report"
    SOLVE_DILEMMA = "solve_dilemma"
    VOICE_COMMAND = "voice_command"
    SYSTEM_CONTROL = "system_control"
    COMPOSE_EMAIL = "compose_email"
    SCHEDULE_TASK = "schedule_task"

class VoiceProfile(Enum):
    MELCHIOR_VOICE = {"voice": "onyx", "speed": 0.9, "pitch": -8}
    BALTHASAR_VOICE = {"voice": "nova", "speed": 1.0, "pitch": 0}
    CASPER_VOICE = {"voice": "shimmer", "speed": 1.1, "pitch": +6}
    SYSTEM_VOICE = {"voice": "echo", "speed": 0.95, "pitch": -2}

# ============================================
# ESTRUCTURAS DE DATOS MEJORADAS
# ============================================
@dataclass
class NodeAnalysis:
    """Análisis completo de un nodo MAGI"""
    node: NodeType
    analysis: str
    confidence: float
    decision: DecisionType
    tools_used: List[str]
    references: List[str]
    emotional_state: str
    execution_time: float
    
@dataclass
class MAGIDecision:
    """Decisión final del sistema MAGI"""
    dilemma: str
    analyses: Dict[NodeType, NodeAnalysis]
    final_decision: DecisionType
    confidence_score: float
    reasoning_chain: List[str]
    minority_opinion: Optional[str]
    recommended_actions: List[str]
    timestamp: datetime.datetime

@dataclass
class MemoryEntry:
    """Entrada en la memoria del sistema"""
    content: Any
    importance: float
    timestamp: datetime.datetime
    access_count: int = 0
    tags: List[str] = field(default_factory=list)

# ============================================
# SISTEMA DE MEMORIA AVANZADO
# ============================================
class MAGIMemory:
    """Sistema de memoria jerárquica para MAGI"""
    
    def __init__(self, capacity: int = 100):
        self.short_term = deque(maxlen=10)
        self.long_term: Dict[str, MemoryEntry] = {}
        self.episodic: List[MemoryEntry] = []
        self.semantic: Dict[str, Any] = {}
        self.capacity = capacity
    
    def store(self, key: str, content: Any, importance: float = 0.5, tags: List[str] = None):
        """Almacena información con importancia ponderada"""
        entry = MemoryEntry(
            content=content,
            importance=importance,
            timestamp=datetime.datetime.now(),
            tags=tags or []
        )
        
        # Almacenamiento jerárquico
        if importance > 0.7:
            self.long_term[key] = entry
        elif importance > 0.3:
            self.episodic.append(entry)
        else:
            self.short_term.append(entry)
        
        # Limpieza de memoria si excede capacidad
        self._cleanup()
    
    def retrieve(self, query: str, k: int = 5) -> List[MemoryEntry]:
        """Recuperación semántica de memoria"""
        results = []
        
        # Búsqueda en todas las capas
        for memory_dict in [self.long_term, self.episodic, list(self.short_term)]:
            if isinstance(memory_dict, dict):
                for key, entry in memory_dict.items():
                    if query.lower() in key.lower() or any(query.lower() in tag.lower() for tag in entry.tags):
                        results.append(entry)
            else:
                for entry in memory_dict:
                    if hasattr(entry, 'tags') and any(query.lower() in tag.lower() for tag in entry.tags):
                        results.append(entry)
        
        # Ordenar por importancia y recencia
        results.sort(key=lambda x: (x.importance, x.timestamp), reverse=True)
        return results[:k]
    
    def _cleanup(self):
        """Limpieza de memoria para mantener capacidad"""
        if len(self.episodic) > self.capacity:
            self.episodic.sort(key=lambda x: x.importance)
            self.episodic = self.episodic[-self.capacity:]

# ============================================
# SISTEMA DE HERRAMIENTAS INTEGRADO
# ============================================
class MAGITools:
    """Caja de herramientas completa para MAGI"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        self.api_keys = api_keys or {}
        self.tools_registry = {
            ActionType.SEARCH_WEB.value: self.search_web,
            ActionType.ANALYZE_DATA.value: self.analyze_data,
            ActionType.EXECUTE_CODE.value: self.execute_code,
            ActionType.GENERATE_REPORT.value: self.generate_report,
            ActionType.SOLVE_DILEMMA.value: self.solve_dilemma,
            ActionType.SYSTEM_CONTROL.value: self.system_control,
            ActionType.COMPOSE_EMAIL.value: self.compose_email,
            ActionType.SCHEDULE_TASK.value: self.schedule_task,
        }
    
    def search_web(self, query: str, node_perspective: str = "neutral") -> Dict:
        """
        Búsqueda web simulada (en producción usar SerpAPI/Tavily)
        """
        # Simulación de búsqueda especializada
        search_results = {
            "MELCHIOR": [
                {"title": "Scientific Analysis", "url": "https://scholar.google.com/...", "relevance": 0.95},
                {"title": "Data Repository", "url": "https://arxiv.org/...", "relevance": 0.88},
            ],
            "BALTHASAR": [
                {"title": "Ethical Framework Analysis", "url": "https://ethics.org/...", "relevance": 0.92},
                {"title": "Moral Implications Study", "url": "https://philosophy.edu/...", "relevance": 0.87},
            ],
            "CASPER": [
                {"title": "Practical Implementation Guide", "url": "https://practical.org/...", "relevance": 0.93},
                {"title": "Case Studies Database", "url": "https://casestudies.com/...", "relevance": 0.89},
            ]
        }
        
        return {
            "success": True,
            "results": search_results.get(node_perspective, search_results["MELCHIOR"]),
            "query": query,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def analyze_data(self, data: Any, analysis_type: str = "statistical") -> Dict:
        """Análisis de datos con múltiples métodos"""
        analysis_methods = {
            "statistical": self._statistical_analysis,
            "pattern": self._pattern_recognition,
            "sentiment": self._sentiment_analysis,
            "trend": self._trend_analysis
        }
        
        if analysis_type in analysis_methods:
            result = analysis_methods[analysis_type](data)
        else:
            result = {"error": f"Unknown analysis type: {analysis_type}"}
        
        return {
            "success": True,
            "analysis_type": analysis_type,
            "result": result,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def execute_code(self, code: str, language: str = "python", safe_mode: bool = True) -> Dict:
        """Ejecución segura de código en sandbox"""
        if safe_mode:
            # Verificaciones de seguridad
            dangerous_patterns = ['import os', 'import subprocess', '__import__', 'eval(', 'exec(']
            for pattern in dangerous_patterns:
                if pattern in code:
                    return {
                        "success": False,
                        "error": f"Security violation: '{pattern}' not allowed in safe mode",
                        "output": None
                    }
        
        try:
            # Crear sandbox temporal
            sandbox_globals = {
                'print': print,
                'len': len,
                'range': range,
                'list': list,
                'dict': dict,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'sum': sum,
                'max': max,
                'min': min,
                'sorted': sorted
            }
            
            # Capturar output
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            exec(code, sandbox_globals)
            
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            return {
                "success": True,
                "output": output,
                "language": language,
                "sandbox_globals": list(sandbox_globals.keys())
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None
            }
    
    def generate_report(self, data: Dict, format_type: str = "pdf") -> bytes:
        """Generación de reportes en múltiples formatos"""
        if format_type == "pdf":
            return self._generate_pdf_report(data)
        elif format_type == "json":
            return json.dumps(data, indent=2).encode()
        elif format_type == "html":
            return self._generate_html_report(data)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def solve_dilemma(self, dilemma: str, ethical_framework: str = "multi") -> Dict:
        """Resolución de dilemas con múltiples marcos éticos"""
        frameworks = {
            "utilitarian": self._utilitarian_analysis,
            "deontological": self._deontological_analysis,
            "virtue_ethics": self._virtue_ethics_analysis,
            "care_ethics": self._care_ethics_analysis
        }
        
        if ethical_framework == "multi":
            results = {}
            for name, framework_func in frameworks.items():
                results[name] = framework_func(dilemma)
            return self._synthesize_ethical_analysis(results)
        else:
            return frameworks.get(ethical_framework, lambda x: {"error": "Framework not found"})(dilemma)
    
    def system_control(self, command: str, safe_mode: bool = True) -> Dict:
        """Control del sistema operativo con sandbox"""
        safe_commands = {
            "get_time": lambda: datetime.datetime.now().isoformat(),
            "get_system_info": lambda: {
                "platform": os.name,
                "cwd": os.getcwd() if not safe_mode else "/sandbox/",
                "python_version": os.sys.version
            },
            "list_directory": lambda path=".": os.listdir(path) if not safe_mode else ["sandbox_file1.txt", "sandbox_file2.txt"],
            "create_file": lambda name, content: self._safe_file_create(name, content),
            "read_file": lambda name: self._safe_file_read(name)
        }
        
        if safe_mode and command not in safe_commands:
            return {
                "success": False,
                "error": f"Command '{command}' not allowed in safe mode",
                "result": None
            }
        
        try:
            if command in safe_commands:
                result = safe_commands[command]()
                return {"success": True, "result": result, "command": command}
        except Exception as e:
            return {"success": False, "error": str(e), "result": None}
    
    def compose_email(self, to: str, subject: str, body: str, node_perspective: str = "neutral") -> Dict:
        """Composición de emails con personalidad del nodo"""
        signatures = {
            "MELCHIOR": "\n\n-- \nMELCHIOR-1\nScience Module | MAGI System\n'Logic Prevails'",
            "BALTHASAR": "\n\n-- \nBALTHASAR-2\nMother Module | MAGI System\n'Protection Above All'",
            "CASPER": "\n\n-- \nCASPER-3\nWoman Module | MAGI System\n'Intuition Guides Action'"
        }
        
        full_body = body + signatures.get(node_perspective, signatures["MELCHIOR"])
        
        return {
            "success": True,
            "email": {
                "to": to,
                "subject": f"[MAGI-{node_perspective}] {subject}",
                "body": full_body,
                "timestamp": datetime.datetime.now().isoformat()
            }
        }
    
    def schedule_task(self, task: str, schedule_time: datetime.datetime, priority: int = 3) -> Dict:
        """Programación de tareas con prioridad"""
        return {
            "success": True,
            "task": task,
            "scheduled_for": schedule_time.isoformat(),
            "priority": priority,
            "task_id": hashlib.md5(f"{task}{schedule_time}".encode()).hexdigest()[:8]
        }
    
    # Métodos privados de análisis
    def _statistical_analysis(self, data):
        if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
            return {
                "mean": sum(data) / len(data),
                "max": max(data),
                "min": min(data),
                "count": len(data)
            }
        return {"error": "Data must be numeric list"}
    
    def _pattern_recognition(self, data):
        return {"patterns": ["Pattern recognition simulation"], "confidence": 0.85}
    
    def _sentiment_analysis(self, text):
        positive_words = ['bueno', 'excelente', 'positivo', 'beneficioso']
        negative_words = ['malo', 'negativo', 'perjudicial', 'riesgo']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return {"sentiment": "positive", "score": 0.7}
        elif neg_count > pos_count:
            return {"sentiment": "negative", "score": -0.6}
        else:
            return {"sentiment": "neutral", "score": 0.0}
    
    def _trend_analysis(self, data):
        return {"trend": "stable", "confidence": 0.75}
    
    def _utilitarian_analysis(self, dilemma):
        return {"framework": "utilitarian", "decision": "APPROVED", "reasoning": "Greatest good for greatest number"}
    
    def _deontological_analysis(self, dilemma):
        return {"framework": "deontological", "decision": "DENIED", "reasoning": "Violates fundamental moral duties"}
    
    def _virtue_ethics_analysis(self, dilemma):
        return {"framework": "virtue_ethics", "decision": "NEEDS_MORE_DATA", "reasoning": "Requires character assessment"}
    
    def _care_ethics_analysis(self, dilemma):
        return {"framework": "care_ethics", "decision": "APPROVED", "reasoning": "Maintains relationships and responsibilities"}
    
    def _synthesize_ethical_analysis(self, results):
        approvals = sum(1 for r in results.values() if r.get("decision") == "APPROVED")
        return {
            "final_decision": "APPROVED" if approvals >= 2 else "DENIED",
            "framework_results": results,
            "confidence": approvals / len(results)
        }
    
    def _generate_pdf_report(self, data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Courier", "B", 16)
        pdf.cell(190, 10, "MAGI SYSTEM v4.0 REPORT", ln=True, align='C')
        # Implementación completa de PDF aquí
        return pdf.output(dest='S').encode('latin-1', 'ignore')
    
    def _generate_html_report(self, data):
        html = f"<html><body><h1>MAGI Report</h1><pre>{json.dumps(data, indent=2)}</pre></body></html>"
        return html.encode()
    
    def _safe_file_create(self, name, content):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, prefix='magi_') as f:
            f.write(content)
            return f.name
    
    def _safe_file_read(self, name):
        if name.startswith('magi_'):
            with open(name, 'r') as f:
                return f.read()
        return "Access denied: Not a MAGI file"

# ============================================
# SISTEMA DE VOZ AVANZADO (Simulación)
# ============================================
class MAGIVoice:
    """Sistema de síntesis y reconocimiento de voz"""
    
    def __init__(self):
        self.voices = {vp.name: vp.value for vp in VoiceProfile}
        self.current_voice = VoiceProfile.SYSTEM_VOICE
    
    def text_to_speech(self, text: str, voice_profile: VoiceProfile = None) -> Dict:
        """Simulación de TTS (en producción usar OpenAI TTS)"""
        if voice_profile is None:
            voice_profile = self.current_voice
        
        voice_config = self.voices.get(voice_profile.name, self.voices["SYSTEM_VOICE"])
        
        # Simulación de generación de audio
        audio_data = {
            "text": text,
            "voice": voice_config["voice"],
            "speed": voice_config["speed"],
            "pitch": voice_config["pitch"],
            "duration_seconds": len(text) * 0.05 / voice_config["speed"],
            "audio_base64": base64.b64encode(text.encode()).decode()  # Simulación
        }
        
        return audio_data
    
    def speech_to_text(self, audio_data: bytes) -> Dict:
        """Simulación de STT (en producción usar Whisper)"""
        # Simulación de reconocimiento
        return {
            "text": base64.b64decode(audio_data).decode(),
            "confidence": 0.95,
            "language": "es"
        }
    
    def speak_node_message(self, node: NodeType, message: str) -> Dict:
        """Cada nodo habla con su propia voz"""
        voice_mapping = {
            NodeType.MELCHIOR: VoiceProfile.MELCHIOR_VOICE,
            NodeType.BALTHASAR: VoiceProfile.BALTHASAR_VOICE,
            NodeType.CASPER: VoiceProfile.CASPER_VOICE,
            NodeType.INTEGRATED: VoiceProfile.SYSTEM_VOICE
        }
        
        return self.text_to_speech(message, voice_mapping.get(node))

# ============================================
# SISTEMA DE DEBATE MEJORADO
# ============================================
class MAGIDebateSystem:
    """Sistema de debate y deliberación real"""
    
    def __init__(self, client: Groq):
        self.client = client
        self.tools = MAGITools()
        self.memory = MAGIMemory()
    
    def extract_decision_from_analysis(self, analysis: str) -> Tuple[DecisionType, float]:
        """Extrae la decisión real del análisis del nodo"""
        analysis_lower = analysis.lower()
        
        # Patrones de aprobación
        approve_patterns = [
            r'\b(aprobado|aprobar|aceptar|proceder|continuar|afirmativo)\b',
            r'\b(recomiendo|sugiero|propongo)\s+(aprobar|continuar|proceder)\b'
        ]
        
        # Patrones de rechazo
        deny_patterns = [
            r'\b(rechazado|denegado|negar|detener|cancelar|negativo)\b',
            r'\b(no\s+recomiendo|no\s+sugiero|no\s+proceder|riesgo\s+alto)\b'
        ]
        
        # Contar ocurrencias
        approve_score = sum(len(re.findall(pattern, analysis_lower)) for pattern in approve_patterns)
        deny_score = sum(len(re.findall(pattern, analysis_lower)) for pattern in deny_patterns)
        
        # Calcular confianza
        total_mentions = approve_score + deny_score
        if total_mentions == 0:
            return DecisionType.UNCERTAIN, 0.3
        
        if approve_score > deny_score:
            confidence = approve_score / total_mentions
            return DecisionType.APPROVED, min(confidence, 0.9)
        elif deny_score > approve_score:
            confidence = deny_score / total_mentions
            return DecisionType.DENIED, min(confidence, 0.9)
        else:
            return DecisionType.UNCERTAIN, 0.5
    
    def cross_examine_nodes(self, analyses: Dict[NodeType, str], dilemma: str) -> Dict[NodeType, str]:
        """Debate cruzado entre nodos"""
        critiques = {}
        
        for node, analysis in analyses.items():
            # Otros nodos critican este análisis
            other_nodes = [n for n in analyses.keys() if n != node]
            
            critique_prompt = f"""
            Analiza críticamente el siguiente análisis del nodo {node.value} sobre:
            DILEMA: {dilema}
            
            ANÁLISIS DE {node.value}:
            {analysis[:500]}
            
            Como nodo {other_nodes[0].value}, proporciona:
            1. Fortalezas del análisis
            2. Debilidades o puntos ciegos
            3. Lo que tu perspectiva puede aportar
            
            Sé constructivo pero crítico.
            """
            
            try:
                completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Eres {other_nodes[0].value} del sistema MAGI."},
                        {"role": "user", "content": critique_prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.6,
                    max_tokens=500
                )
                
                critiques[node] = completion.choices[0].message.content
            except:
                critiques[node] = f"[CRÍTICA DE {other_nodes[0].value}] No disponible temporalmente"
        
        return critiques
    
    def hierarchical_synthesis(self, analyses: Dict[NodeType, str], dilemma: str) -> Dict:
        """Síntesis jerárquica completa"""
        
        # Paso 1: Debate cruzado
        critiques = self.cross_examine_nodes(analyses, dilemma)
        
        # Paso 2: Meta-análisis
        meta_analysis = self._meta_analyze(analyses, critiques)
        
        # Paso 3: Decisión ponderada
        decisions = {}
        for node, analysis in analyses.items():
            decision, confidence = self.extract_decision_from_analysis(analysis)
            decisions[node] = {
                "decision": decision,
                "confidence": confidence,
                "analysis_length": len(analysis)
            }
        
        # Paso 4: Síntesis final
        final_decision = self._weighted_decision(decisions)
        
        return {
            "critiques": critiques,
            "meta_analysis": meta_analysis,
            "individual_decisions": decisions,
            "final_decision": final_decision,
            "deliberation_quality": self._assess_deliberation_quality(decisions, critiques)
        }
    
    def _meta_analyze(self, analyses: Dict[NodeType, str], critiques: Dict[NodeType, str]) -> str:
        """Meta-análisis de patrones"""
        all_text = " ".join(list(analyses.values()) + list(critiques.values()))
        
        # Análisis de sentimiento
        sentiment = self.tools._sentiment_analysis(all_text)
        
        # Patrones comunes
        common_themes = self._extract_common_themes(all_text)
        
        return f"Meta-análisis: Sentimiento {sentiment['sentiment']}, Temas comunes: {common_themes}"
    
    def _extract_common_themes(self, text: str) -> List[str]:
        """Extrae temas comunes del texto"""
        themes = []
        
        theme_indicators = {
            "risk": r'\b(riesgo|peligro|amenaza)\b',
            "opportunity": r'\b(oportunidad|beneficio|ventaja)\b',
            "ethics": r'\b(ética|moral|deber|obligación)\b',
            "practicality": r'\b(práctico|implementación|viable)\b',
            "innovation": r'\b(innovación|avance|progreso)\b'
        }
        
        for theme, pattern in theme_indicators.items():
            if re.search(pattern, text.lower()):
                themes.append(theme)
        
        return themes if themes else ["general_analysis"]
    
    def _weighted_decision(self, decisions: Dict[NodeType, Dict]) -> Dict:
        """Decisión ponderada basada en confianza y tipo de nodo"""
        
        node_weights = {
            NodeType.MELCHIOR: 1.0,  # Ciencia tiene peso estándar
            NodeType.BALTHASAR: 1.2,  # Ética tiene peso mayor en dilemas morales
            NodeType.CASPER: 0.9      # Intuición tiene peso ligeramente menor
        }
        
        approval_score = 0
        denial_score = 0
        total_weight = 0
        
        for node, decision_data in decisions.items():
            weight = node_weights.get(node, 1.0) * decision_data["confidence"]
            total_weight += weight
            
            if decision_data["decision"] == DecisionType.APPROVED:
                approval_score += weight
            elif decision_data["decision"] == DecisionType.DENIED:
                denial_score += weight
        
        if total_weight == 0:
            return {"decision": DecisionType.UNCERTAIN, "confidence": 0.0}
        
        approval_ratio = approval_score / total_weight
        
        if approval_ratio > 0.6:
            return {"decision": DecisionType.APPROVED, "confidence": approval_ratio}
        elif approval_ratio < 0.4:
            return {"decision": DecisionType.DENIED, "confidence": 1 - approval_ratio}
        else:
            return {"decision": DecisionType.UNCERTAIN, "confidence": abs(0.5 - approval_ratio)}
    
    def _assess_deliberation_quality(self, decisions: Dict, critiques: Dict) -> str:
        """Evalúa la calidad de la deliberación"""
        avg_confidence = sum(d["confidence"] for d in decisions.values()) / len(decisions)
        has_critiques = len(critiques) > 0
        
        if avg_confidence > 0.8 and has_critiques:
            return "HIGH_QUALITY"
        elif avg_confidence > 0.6:
            return "ADEQUATE"
        else:
            return "LOW_QUALITY_NEEDS_REVIEW"

# ============================================
# INICIALIZACIÓN DE SESIÓN MEJORADA
# ============================================
if "history" not in st.session_state:
    st.session_state.history = []

if "toxicity_level" not in st.session_state:
    st.session_state.toxicity_level = 30

if "magi_states" not in st.session_state:
    st.session_state.magi_states = {
        "MELCHIOR": "承 認", 
        "BALTHASAR": "承 認", 
        "CASPER": "承 認"
    }

if "magi_responses" not in st.session_state:
    st.session_state.magi_responses = {
        "MELCHIOR": "",
        "BALTHASAR": "", 
        "CASPER": "",
        "FINAL": "",
        "DILEMA": ""
    }

if "magi_memory" not in st.session_state:
    st.session_state.magi_memory = MAGIMemory()

if "magi_tools" not in st.session_state:
    st.session_state.magi_tools = MAGITools()

if "magi_voice" not in st.session_state:
    st.session_state.magi_voice = MAGIVoice()

if "real_decisions" not in st.session_state:
    st.session_state.real_decisions = {}

# ============================================
# ESTILOS CSS MEJORADOS (Manteniendo estética Evangelion)
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=VT323&display=swap');

/* FONDO Y TEMA MEJORADO */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    color: #FF6600;
    font-family: 'VT323', 'Share Tech Mono', monospace;
}

/* EFECTO CRT MEJORADO */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        repeating-linear-gradient(
            0deg,
            rgba(255, 102, 0, 0.03) 0px,
            rgba(255, 102, 0, 0.03) 1px,
            transparent 1px,
            transparent 3px
        ),
        repeating-linear-gradient(
            90deg,
            rgba(255, 102, 0, 0.03) 0px,
            rgba(255, 102, 0, 0.03) 1px,
            transparent 1px,
            transparent 3px
        );
    pointer-events: none;
    z-index: 1000;
    animation: scan 8s linear infinite;
}

/* ANIMACIONES MEJORADAS */
@keyframes scan {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
}

@keyframes glitch {
    0% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 0.8; }
    50% { opacity: 1; }
}

/* HEXÁGONOS MEJORADOS */
.magi-hexagon {
    background: linear-gradient(135deg, rgba(0, 20, 0, 0.9) 0%, rgba(0, 40, 0, 0.9) 100%);
    border: 2px solid #FF6600;
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
    padding: 25px;
    margin: 15px;
    text-align: center;
    box-shadow: 
        inset 0 0 20px rgba(255, 102, 0, 0.2),
        0 0 30px rgba(255, 102, 0, 0.1);
    transition: all 0.3s ease;
    animation: pulse 3s infinite;
}

.magi-hexagon:hover {
    box-shadow: 
        inset 0 0 30px rgba(255, 102, 0, 0.4),
        0 0 50px rgba(255, 102, 0, 0.3);
    transform: scale(1.02);
}

/* BOTONES MEJORADOS */
.stButton > button {
    background: linear-gradient(135deg, #0a1a0a 0%, #1a2a1a 100%);
    border: 2px solid #FF6600;
    color: #FF6600;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.9em;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: 12px 24px;
    transition: all 0.3s ease;
    clip-path: polygon(5% 0%, 95% 0%, 100% 20%, 100% 80%, 95% 100%, 5% 100%, 0% 80%, 0% 20%);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #FF6600 0%, #FF8800 100%);
    color: #000000;
    box-shadow: 0 0 30px rgba(255, 102, 0, 0.5);
    transform: translateY(-2px);
}

/* CARDS DE HERRAMIENTAS */
.tool-card {
    background: rgba(0, 20, 0, 0.8);
    border: 1px solid #00FFAA;
    border-left: 4px solid #00FFAA;
    padding: 15px;
    margin: 10px 0;
    border-radius: 0;
    transition: all 0.3s ease;
}

.tool-card:hover {
    background: rgba(0, 30, 0, 0.9);
    border-left-width: 8px;
    box-shadow: 0 0 20px rgba(0, 255, 170, 0.2);
}

/* BARRA DE PROGRESO MEJORADA */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00FFC8, #00FFAA, #FF6600);
    animation: glitch 2s infinite;
}

/* SCROLLBAR PERSONALIZADO */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #0a0a0a;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #FF6600, #FF0000);
    border-radius: 4px;
}

/* EFECTO DE TEXTO GLITCH */
.glitch-text {
    animation: glitch 0.5s infinite;
}

/* RESPONSIVE DESIGN MEJORADO */
@media (max-width: 768px) {
    .magi-hexagon {
        margin: 10px 5px;
        padding: 15px;
    }
    .stButton > button {
        font-size: 0.8em;
        padding: 8px 16px;
    }
}

/* ESTILOS PARA VOZ Y ASISTENTE */
.voice-active {
    border: 2px solid #00FFC8;
    animation: pulse 1s infinite;
    box-shadow: 0 0 20px rgba(0, 255, 200, 0.5);
}

.assistant-panel {
    background: rgba(0, 10, 20, 0.9);
    border: 1px solid #00CCFF;
    padding: 20px;
    margin: 15px 0;
    border-radius: 5px;
}

/* SISTEMA DE NOTIFICACIONES */
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: rgba(0, 0, 0, 0.95);
    border: 2px solid #FF6600;
    padding: 15px 25px;
    z-index: 10000;
    animation: slideIn 0.5s ease-out;
    box-shadow: 0 0 30px rgba(255, 102, 0, 0.3);
}

@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES AUXILIARES MEJORADAS
# ============================================
def limpiar_texto_para_pdf(texto: str, max_length: int = 5000) -> str:
    """Versión mejorada de limpieza de texto"""
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
    
    return texto[:max_length]

def crear_pdf_evangelion_mejorado(dilema: str, m: str, b: str, c: str, final: str, 
                                  votes: Dict, confidence: float) -> bytes:
    """PDF mejorado con más información y mejor formato"""
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font("Courier", "B", 20)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(190, 15, "MAGI SYSTEM v4.0 - DELIBERATION REPORT", ln=True, align='C')
    pdf.ln(5)
    
    # Metadatos
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(150, 150, 150)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    pdf.cell(0, 6, f"REPORT CODE: MAGI-{hashlib.md5(dilema.encode()).hexdigest()[:8].upper()}", ln=True)
    pdf.cell(0, 6, f"TIMESTAMP: {fecha}", ln=True)
    pdf.cell(0, 6, f"TOXICITY LEVEL: {st.session_state.toxicity_level}%", ln=True)
    pdf.cell(0, 6, f"SYSTEM CONFIDENCE: {confidence:.2%}", ln=True)
    pdf.ln(10)
    
    # Dilema original
    pdf.set_font("Courier", "B", 12)
    pdf.set_text_color(255, 102, 0)
    pdf.cell(0, 10, ">>> USER QUERY <<<", ln=True)
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(200, 200, 200)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(dilema, 2000))
    pdf.ln(10)
    
    # Análisis de nodos
    nodos = [
        ("MELCHIOR-1 (SCIENCE MODULE)", m, 0, 204, 255),
        ("BALTHASAR-2 (MOTHER MODULE)", b, 0, 255, 170),
        ("CASPER-3 (WOMAN MODULE)", c, 255, 102, 0)
    ]
    
    for nombre, contenido, r, g, b_val in nodos:
        pdf.set_font("Courier", "B", 11)
        pdf.set_text_color(r, g, b_val)
        pdf.cell(0, 10, f">>> {nombre} <<<", ln=True)
        
        # Voto del nodo
        node_name = nombre.split("(")[0].strip()
        voto = votes.get(node_name, "UNKNOWN")
        pdf.set_font("Courier", "B", 9)
        pdf.cell(0, 6, f"VOTE: {voto}", ln=True)
        
        # Contenido
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(200, 200, 200)
        pdf.multi_cell(0, 5, limpiar_texto_para_pdf(contenido, 3000))
        pdf.ln(8)
    
    # Síntesis final
    pdf.set_draw_color(255, 0, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    pdf.set_font("Courier", "B", 14)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 12, ">>> FINAL RESOLUTION <<<", ln=True)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(200, 200, 200)
    pdf.multi_cell(0, 6, limpiar_texto_para_pdf(final, 4000))
    
    # Recomendaciones
    pdf.ln(10)
    pdf.set_font("Courier", "B", 10)
    pdf.set_text_color(0, 255, 200)
    pdf.cell(0, 8, ">>> RECOMMENDED ACTIONS <<<", ln=True)
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 6, "- Implement monitoring protocols", ln=True)
    pdf.cell(0, 6, "- Schedule follow-up analysis", ln=True)
    pdf.cell(0, 6, "- Update system parameters", ln=True)
    
    # Pie de página
    pdf.ln(15)
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "MAGI SYSTEM v4.0 AWAKENING | CLASSIFICATION: TOP SECRET // NOFORN", ln=True, align='C')
    pdf.cell(0, 8, "UNAUTHORIZED ACCESS WILL BE PROSECUTED UNDER INTERNATIONAL LAW", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

def mostrar_secuencia_boot_mejorada():
    """Secuencia de arranque más dramática"""
    boot_messages = [
        ("> INITIATING MAGI SYSTEM v4.0 BOOT SEQUENCE...", 0.3),
        ("> QUANTUM NEURO-LINK ESTABLISHED...", 0.4),
        ("> TRIUMVIRATE SYNCHRONIZATION AT 99.97%...", 0.3),
        ("> LOADING MEMORY MATRICES...", 0.2),
        ("> INITIALIZING TOOL SYSTEMS...", 0.3),
        ("> MELCHIOR-1: ONLINE [SCIENCE MODULE ACTIVE]", 0.4),
        ("> BALTHASAR-2: ONLINE [MOTHER MODULE ACTIVE]", 0.4),
        ("> CASPER-3: ONLINE [WOMAN MODULE ACTIVE]", 0.4),
        ("> DEBATE SYSTEM: ARMED", 0.2),
        ("> VOICE INTERFACE: CALIBRATED", 0.3),
        ("> ALL SYSTEMS NOMINAL. AWAITING INPUT.", 0.5)
    ]
    
    placeholder = st.empty()
    for msg, delay in boot_messages:
        placeholder.markdown(f"""
        <div style='color:#FF6600; font-family:"Share Tech Mono"; margin:8px 0; 
                    text-shadow: 0 0 10px rgba(255,102,0,0.5);'>
            {msg}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(delay)
    
    time.sleep(1)
    placeholder.empty()

# ============================================
# INTERFAZ PRINCIPAL MEJORADA
# ============================================

# Boot sequence
if "boot_shown" not in st.session_state:
    st.session_state.boot_shown = True
    mostrar_secuencia_boot_mejorada()

# Header mejorado
st.markdown("""
<h1 style='text-align: center; font-size: 3em; text-shadow: 0 0 20px #FF6600;'>
    ⬢ MAGI SYSTEM v4.0: AWAKENING
</h1>
<h3 style='text-align: center; color: #FF0000; text-shadow: 0 0 15px #FF0000;'>
    SUPERCOMPUTING CENTER - CLASSIFIED LEVEL AAA
</h3>
""", unsafe_allow_html=True)

# Panel de estado mejorado
col_status1, col_status2, col_status3, col_status4 = st.columns(4)
with col_status1:
    st.metric("SYNC RATE", "99.97%", "0.02%")
with col_status2:
    st.metric("TOXICITY", f"{st.session_state.toxicity_level}%", f"{random.randint(-5, 5)}%")
with col_status3:
    st.metric("MEMORY LOAD", f"{random.randint(30, 70)}%", f"{random.randint(-10, 10)}%")
with col_status4:
    st.metric("DECISIONS", f"{len(st.session_state.history)}", f"+{random.randint(0, 3)}")

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# TRIUNVIRATO MEJORADO
st.markdown("### ⬡ MAGI TRIUMVIRATE DELIBERATION MATRIX")

col1, col2, col3 = st.columns(3)

with col1:
    estado_mel = st.session_state.magi_states["MELCHIOR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name" style="font-size: 1.5em;">MELCHIOR-1</div>
        <div style="color:#00CCFF; font-size:1.1em; letter-spacing:2px;">SCIENCE MODULE</div>
        <div class="magi-status {'status-approved' if estado_mel == '承 認' else 'status-denied'}" style="font-size: 3em;">
            {estado_mel}
        </div>
        <div style="color:#888; font-size:0.9em; margin-top:15px;">
            LOGIC | DATA | ANALYSIS | PRECISION
        </div>
        <div style="color:#00CCFF; font-size:0.8em; margin-top:10px;">
            Confidence: {st.session_state.real_decisions.get('MELCHIOR', {}).get('confidence', 0.85):.1%}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    estado_bal = st.session_state.magi_states["BALTHASAR"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name" style="font-size: 1.5em;">BALTHASAR-2</div>
        <div style="color:#00FFAA; font-size:1.1em; letter-spacing:2px;">MOTHER MODULE</div>
        <div class="magi-status {'status-approved' if estado_bal == '承 認' else 'status-denied'}" style="font-size: 3em;">
            {estado_bal}
        </div>
        <div style="color:#888; font-size:0.9em; margin-top:15px;">
            ETHICS | PROTECTION | CARE | WISDOM
        </div>
        <div style="color:#00FFAA; font-size:0.8em; margin-top:10px;">
            Confidence: {st.session_state.real_decisions.get('BALTHASAR', {}).get('confidence', 0.85):.1%}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    estado_cas = st.session_state.magi_states["CASPER"]
    st.markdown(f"""
    <div class="magi-hexagon">
        <div class="magi-name" style="font-size: 1.5em;">CASPER-3</div>
        <div style="color:#FF6600; font-size:1.1em; letter-spacing:2px;">WOMAN MODULE</div>
        <div class="magi-status {'status-approved' if estado_cas == '承 認' else 'status-denied'}" style="font-size: 3em;">
            {estado_cas}
        </div>
        <div style="color:#888; font-size:0.9em; margin-top:15px;">
            INTUITION | PRACTICALITY | DESIRE | INSTINCT
        </div>
        <div style="color:#FF6600; font-size:0.8em; margin-top:10px;">
            Confidence: {st.session_state.real_decisions.get('CASPER', {}).get('confidence', 0.85):.1%}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Panel de decisión
decision = "APPROVED" if sum(1 for state in st.session_state.magi_states.values() if state == "承 認") >= 2 else "DENIED"
decision_class = "decision-approved" if decision == "APPROVED" else "decision-denied"
decision_color = "#00FFC8" if decision == "APPROVED" else "#FF0000"

st.markdown(f"""
<div class="decision-panel {decision_class}" style="animation: glitch 5s infinite;">
    <div style="font-size: 1.5rem; color: #aaa; margin-bottom: 15px; letter-spacing: 3px;">
        >>> SYSTEM VERDICT (2/3 MAJORITY REQUIRED) <<<
    </div>
    <div class="decision-text" style="color: {decision_color}; font-size: 4em; letter-spacing: 5px;">
        {decision}
    </div>
    <div style="margin-top: 20px; color: #888; font-size: 1.1rem;">
        Voting Matrix: 
        <span style="color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000'}">MELCHIOR: {estado_mel}</span> | 
        <span style="color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000'}">BALTHASAR: {estado_bal}</span> | 
        <span style="color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000'}">CASPER: {estado_cas}</span>
    </div>
    <div style="margin-top: 15px; color: #FF6600; font-size: 0.9rem;">
        DELIBERATION QUALITY: {st.session_state.get('deliberation_quality', 'AWAITING INPUT')}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

# Mostrar respuestas anteriores si existen
if any(st.session_state.magi_responses.values()):
    with st.expander("📜 COMPLETE DELIBERATION RECORD", expanded=True):
        st.markdown("""
        <div style='color:#FF6600; font-family:"Share Tech Mono"; text-shadow: 0 0 10px rgba(255,102,0,0.3);'>
            >>> DELIBERATION RECORD ACCESSED <<<
            >>> DISPLAYING ALL NEURAL PATTERNS <<<
        </div>
        """, unsafe_allow_html=True)
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        if st.session_state.magi_responses["MELCHIOR"]:
            st.markdown(f"""
            <div class="response-card melchior-card">
                <div class="response-title">
                    <span style="font-size: 1.3em;">MELCHIOR-1</span>
                    <span style="color: {'#00FFC8' if estado_mel == '承 認' else '#FF0000'}; font-size: 1.5em;">
                        {estado_mel}
                    </span>
                </div>
                <div class="response-content" style="font-size: 1.1em;">
                    {st.session_state.magi_responses["MELCHIOR"]}
                </div>
                <div style="color:#00CCFF; margin-top:10px; font-size:0.8em;">
                    ANALYSIS TYPE: SCIENTIFIC | TOKENS: {len(st.session_state.magi_responses['MELCHIOR'].split())}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res2:
        if st.session_state.magi_responses["BALTHASAR"]:
            st.markdown(f"""
            <div class="response-card balthasar-card">
                <div class="response-title">
                    <span style="font-size: 1.3em;">BALTHASAR-2</span>
                    <span style="color: {'#00FFC8' if estado_bal == '承 認' else '#FF0000'}; font-size: 1.5em;">
                        {estado_bal}
                    </span>
                </div>
                <div class="response-content" style="font-size: 1.1em;">
                    {st.session_state.magi_responses["BALTHASAR"]}
                </div>
                <div style="color:#00FFAA; margin-top:10px; font-size:0.8em;">
                    ANALYSIS TYPE: ETHICAL | TOKENS: {len(st.session_state.magi_responses['BALTHASAR'].split())}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_res3:
        if st.session_state.magi_responses["CASPER"]:
            st.markdown(f"""
            <div class="response-card casper-card">
                <div class="response-title">
                    <span style="font-size: 1.3em;">CASPER-3</span>
                    <span style="color: {'#00FFC8' if estado_cas == '承 認' else '#FF0000'}; font-size: 1.5em;">
                        {estado_cas}
                    </span>
                </div>
                <div class="response-content" style="font-size: 1.1em;">
                    {st.session_state.magi_responses["CASPER"]}
                </div>
                <div style="color:#FF6600; margin-top:10px; font-size:0.8em;">
                    ANALYSIS TYPE: INTUITIVE | TOKENS: {len(st.session_state.magi_responses['CASPER'].split())}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Resolución final mejorada
    if st.session_state.magi_responses["FINAL"]:
        st.markdown(f"""
        <div class="response-card final-card" style="animation: pulse 2s infinite;">
            <div class="response-title">
                <span style="color: {decision_color}; font-size: 1.5em; letter-spacing: 3px;">
                    >>> FINAL RESOLUTION <<<
                </span>
                <span style="color: {decision_color}; font-size: 2em; font-weight: bold;">
                    {decision}
                </span>
            </div>
            <div class="response-content" style="font-size: 1.2em;">
                {st.session_state.magi_responses["FINAL"]}
            </div>
            <div style="color:#FF0000; margin-top:15px; font-size:0.9em; border-top: 1px solid #FF0000; padding-top:10px;">
                SYSTEM CONFIDENCE: {st.session_state.get('final_confidence', 0.85):.1%} | 
                DELIBERATION CYCLES: {st.session_state.get('deliberation_cycles', 3)}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Descarga de PDF mejorada
if st.session_state.magi_responses["FINAL"]:
    st.markdown("""
    <div class="download-section" style="animation: slideIn 0.5s ease-out;">
        <div class="download-title">📄 CLASSIFIED REPORT DOWNLOAD</div>
        <div class="download-instruction">
            ⬇️ <strong>Download complete MAGI deliberation report with all analyses and metadata</strong>
        </div>
    """, unsafe_allow_html=True)
    
    pdf_bytes = crear_pdf_evangelion_mejorado(
        st.session_state.magi_responses["DILEMA"],
        st.session_state.magi_responses["MELCHIOR"],
        st.session_state.magi_responses["BALTHASAR"],
        st.session_state.magi_responses["CASPER"],
        st.session_state.magi_responses["FINAL"],
        {"MELCHIOR": estado_mel, "BALTHASAR": estado_bal, "CASPER": estado_cas},
        st.session_state.get('final_confidence', 0.85)
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="⬇️ DOWNLOAD TOP SECRET REPORT (PDF)",
            data=pdf_bytes,
            file_name=f"MAGI_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Sidebar mejorado con herramientas de asistente
with st.sidebar:
    st.markdown("### 🔐 SYSTEM ACCESS CONTROL")
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("🔑 API KEY: ACTIVE")
    else:
        api_key = st.text_input("🔑 GROQ API KEY", type="password", key="api_key_input")
    
    if not api_key:
        st.warning("> ENTER API KEY TO INITIALIZE SYSTEM")
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    
    # Panel de herramientas del asistente
    st.markdown("### 🛠️ ASSISTANT TOOLS")
    
    tool_tabs = st.tabs(["🔍 SEARCH", "💻 SYSTEM", "📧 EMAIL", "📅 TASKS"])
    
    with tool_tabs[0]:
        st.markdown("**Web Search Tool**")
        search_query = st.text_input("Search query:", key="tool_search")
        node_perspective = st.selectbox("Node perspective:", ["MELCHIOR", "BALTHASAR", "CASPER"])
        
        if st.button("🔍 Execute Search", use_container_width=True):
            with st.spinner("Searching..."):
                results = st.session_state.magi_tools.search_web(search_query, node_perspective)
                st.json(results)
    
    with tool_tabs[1]:
        st.markdown("**System Control**")
        sys_command = st.selectbox("Command:", ["get_time", "get_system_info", "list_directory"])
        
        if st.button("⚡ Execute Command", use_container_width=True):
            with st.spinner("Executing..."):
                result = st.session_state.magi_tools.system_control(sys_command, safe_mode=True)
                st.json(result)
    
    with tool_tabs[2]:
        st.markdown("**Email Composer**")
        email_to = st.text_input("To:", key="email_to")
        email_subject = st.text_input("Subject:", key="email_subject")
        email_body = st.text_area("Body:", key="email_body")
        email_node = st.selectbox("From:", ["MELCHIOR", "BALTHASAR", "CASPER"])
        
        if st.button("📧 Compose Email", use_container_width=True):
            with st.spinner("Composing..."):
                email = st.session_state.magi_tools.compose_email(email_to, email_subject, email_body, email_node)
                st.json(email)
    
    with tool_tabs[3]:
        st.markdown("**Task Scheduler**")
        task_desc = st.text_input("Task description:", key="task_desc")
        task_priority = st.slider("Priority:", 1, 5, 3)
        task_time = st.time_input("Schedule time:", datetime.time(9, 0))
        
        if st.button("📅 Schedule Task", use_container_width=True):
            with st.spinner("Scheduling..."):
                schedule_time = datetime.datetime.combine(datetime.date.today(), task_time)
                task = st.session_state.magi_tools.schedule_task(task_desc, schedule_time, task_priority)
                st.json(task)
    
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    
    # Historial mejorado
    st.markdown("### 📊 MISSION HISTORY")
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history[-10:])):
            with st.expander(f"MISSION {len(st.session_state.history)-i}: {entry.get('timestamp', 'UNKNOWN')}"):
                st.write(f"**Decision:** `{entry.get('decision', 'UNKNOWN')}`")
                st.write(f"**Quality:** `{entry.get('quality', 'STANDARD')}`")
                st.write(f"**Confidence:** `{entry.get('confidence', 0.0):.1%}`")
    else:
        st.write("> No mission records in database")
    
    # Controles del sistema
    st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
    st.markdown("### ⚙️ SYSTEM CONTROLS")
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("🔄 UPDATE", use_container_width=True):
            st.session_state.toxicity_level = min(100, st.session_state.toxicity_level + random.randint(5, 15))
            st.rerun()
    with col_btn2:
        if st.button("🗑️ CLEAR", use_container_width=True):
            st.session_state.history = []
            st.session_state.magi_memory = MAGIMemory()
            st.rerun()
    with col_btn3:
        if st.button("🔊 VOICE", use_container_width=True):
            st.session_state.voice_active = not st.session_state.get('voice_active', False)
            st.rerun()
    
    toxicity = st.slider("TOXICITY LEVEL", 0, 100, st.session_state.toxicity_level)
    st.session_state.toxicity_level = toxicity
    
    # Estado de voz
    if st.session_state.get('voice_active', False):
        st.markdown("""
        <div class="voice-active" style="padding:10px; text-align:center; margin-top:10px;">
            🎤 VOICE INTERFACE: ACTIVE
        </div>
        """, unsafe_allow_html=True)

# Input principal con capacidades de asistente
st.markdown("### > QUERY INPUT INTERFACE")
st.markdown("""
<div style='color:#FF6600; font-family:"Share Tech Mono"; margin-bottom:15px;'>
    > ENTER TACTICAL QUERY OR VOICE COMMAND...
    > COMMANDS: analyze, search, execute, compose, schedule, solve
</div>
""", unsafe_allow_html=True)

# Área de input con ejemplos
col_input1, col_input2 = st.columns([3, 1])
with col_input1:
    dilema = st.chat_input("Type query or command here...", key="query_input")
with col_input2:
    if st.button("🎤 VOICE INPUT", use_container_width=True):
        st.info("Voice input simulation: 'Analyze the security protocol vulnerability'")

# Procesamiento principal mejorado con debate real
if dilema and api_key:
    # Detectar tipo de acción
    action_type = ActionType.SOLVE_DILEMMA  # Default
    if dilema.lower().startswith("search"):
        action_type = ActionType.SEARCH_WEB
    elif dilema.lower().startswith("execute") or dilema.lower().startswith("run"):
        action_type = ActionType.EXECUTE_CODE
    elif dilema.lower().startswith("compose"):
        action_type = ActionType.COMPOSE_EMAIL
    elif dilema.lower().startswith("schedule"):
        action_type = ActionType.SCHEDULE_TASK
    
    # Mostrar reconocimiento de comando
    with st.chat_message("user"):
        st.markdown(f"""
        <div style='color:#FF6600; font-family:"Share Tech Mono";'>
            > QUERY RECEIVED: "{dilema[:100]}..."
            > ACTION TYPE DETECTED: {action_type.value.upper()}
            > INITIATING PROCESSING...
        </div>
        """, unsafe_allow_html=True)
    
    st.session_state.magi_responses["DILEMA"] = dilema
    
    try:
        client = Groq(api_key=api_key)
        debate_system = MAGIDebateSystem(client)
        
        with st.status("🔄 MAGI DELIBERATION PROTOCOL v4.0", expanded=True) as status:
            progress_bar = st.progress(0)
            
            # Mensajes de progreso detallados
            progress_messages = [
                ("🔬 MELCHIOR-1: Scientific Analysis & Web Search...", 25),
                ("🛡️ BALTHASAR-2: Ethical Framework Application...", 50),
                ("🌸 CASPER-3: Intuitive Pattern Recognition...", 75),
                ("⚡ CROSS-EXAMINATION: Node Debate Initiated...", 85),
                ("🧬 META-ANALYSIS: Synthesizing Perspectives...", 95),
                ("📜 FINAL RESOLUTION: Generating Verdict...", 100)
            ]
            
            # Fase 1: Análisis individual con búsqueda web
            st.write(progress_messages[0][0])
            
            # Melchior con búsqueda científica
            search_results = st.session_state.magi_tools.search_web(dilema, "MELCHIOR")
            
            completion_m = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"""Eres MELCHIOR-1, el nodo científico del sistema MAGI v4.0.
                    Eres lógico, preciso y basado en datos. Tu deber es analizar con rigor científico.
                    
                    DILEMA A ANALIZAR: {dilema}
                    
                    DATOS DE BÚSQUEDA CIENTÍFICA: {json.dumps(search_results.get('results', []))}
                    
                    Proporciona:
                    1. Análisis científico completo (usa los datos proporcionados)
                    2. Evaluación de riesgos y beneficios
                    3. Tu voto final: "APROBADO" o "RECHAZADO" con justificación clara
                    
                    Responde en español. Sé exhaustivo pero conciso."""},
                    {"role": "user", "content": "Proporciona tu análisis científico completo y voto final."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=1500
            )
            m_resp = completion_m.choices[0].message.content
            st.session_state.magi_responses["MELCHIOR"] = m_resp
            progress_bar.progress(progress_messages[0][1])
            time.sleep(0.5)
            
            # Balthasar con análisis ético
            st.write(progress_messages[1][0])
            search_results_b = st.session_state.magi_tools.search_web(dilema, "BALTHASAR")
            
            completion_b = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"""Eres BALTHASAR-2, el nodo materno/ético del sistema MAGI v4.0.
                    Eres compasivo, protector y ético. Analizas desde la moral y la protección humana.
                    
                    DILEMA: {dilema}
                    
                    REFERENCIAS ÉTICAS: {json.dumps(search_results_b.get('results', []))}
                    
                    Proporciona:
                    1. Análisis ético y moral completo
                    2. Implicaciones para la protección humana
                    3. Tu voto final: "APROBADO" o "RECHAZADO" con justificación ética
                    
                    Responde en español."""},
                    {"role": "user", "content": "Proporciona tu análisis ético completo y voto final."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=1500
            )
            b_resp = completion_b.choices[0].message.content
            st.session_state.magi_responses["BALTHASAR"] = b_resp
            progress_bar.progress(progress_messages[1][1])
            time.sleep(0.5)
            
            # Casper con intuición
            st.write(progress_messages[2][0])
            search_results_c = st.session_state.magi_tools.search_web(dilema, "CASPER")
            
            completion_c = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"""Eres CASPER-3, el nodo intuitivo/práctico del sistema MAGI v4.0.
                    Eres intuitivo, pragmático y orientado a resultados. Actúas por interés propio inteligente.
                    
                    DILEMA: {dilema}
                    
                    CASOS PRÁCTICOS: {json.dumps(search_results_c.get('results', []))}
                    
                    Proporciona:
                    1. Análisis intuitivo y práctico completo
                    2. Viabilidad y consecuencias prácticas
                    3. Tu voto final: "APROBADO" o "RECHAZADO" con justificación pragmática
                    
                    Responde en español."""},
                    {"role": "user", "content": "Proporciona tu análisis intuitivo completo y voto final."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1500
            )
            c_resp = completion_c.choices[0].message.content
            st.session_state.magi_responses["CASPER"] = c_resp
            progress_bar.progress(progress_messages[2][1])
            time.sleep(0.5)
            
            # Fase 2: Debate cruzado y extracción de decisiones reales
            st.write(progress_messages[3][0])
            
            analyses_dict = {
                NodeType.MELCHIOR: m_resp,
                NodeType.BALTHASAR: b_resp,
                NodeType.CASPER: c_resp
            }
            
            # Extraer decisiones reales (NO aleatorias)
            real_decisions = {}
            for node, analysis in analyses_dict.items():
                decision_type, confidence = debate_system.extract_decision_from_analysis(analysis)
                real_decisions[node] = {
                    "decision": decision_type,
                    "confidence": confidence,
                    "vote": "承 認" if decision_type == DecisionType.APPROVED else "否 定"
                }
            
            st.session_state.real_decisions = real_decisions
            
            # Actualizar estados basados en decisiones reales
            for node_name in st.session_state.magi_states:
                node_enum = NodeType[node_name]
                st.session_state.magi_states[node_name] = real_decisions[node_enum]["vote"]
            
            # Debate cruzado
            critiques = debate_system.cross_examine_nodes(analyses_dict, dilema)
            
            # Almacenar críticas para mostrar
            st.session_state.magi_critiques = critiques
            
            progress_bar.progress(progress_messages[3][1])
            time.sleep(1)
            
            # Fase 3: Meta-análisis y síntesis final
            st.write(progress_messages[4][0])
            
            deliberation_result = debate_system.hierarchical_synthesis(analyses_dict, dilema)
            st.session_state.deliberation_quality = deliberation_result["deliberation_quality"]
            st.session_state.final_confidence = deliberation_result["final_decision"]["confidence"]
            st.session_state.deliberation_cycles = 3
            
            progress_bar.progress(progress_messages[4][1])
            time.sleep(0.5)
            
            # Fase 4: Resolución final integrada
            st.write(progress_messages[5][0])
            
            final_decision_text = deliberation_result["final_decision"]["decision"].value
            
            completion_final = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"""Eres el sistema MAGI integrado v4.0 AWAKENING.
                    Debes sintetizar una resolución final basada en los análisis y debate de los tres nodos.
                    
                    ANÁLISIS COMPLETOS:
                    MELCHIOR-1 (Científico): {m_resp[:1000]}
                    BALTHASAR-2 (Ético): {b_resp[:1000]}
                    CASPER-3 (Intuitivo): {c_resp[:1000]}
                    
                    CRÍTICAS CRUZADAS:
                    {json.dumps(critiques, indent=2)[:500]}
                    
                    DECISIONES INDIVIDUALES:
                    {json.dumps({k.value: v for k, v in real_decisions.items()}, default=str)}
                    
                    Basado en todo esto, la decisión ponderada es: {final_decision_text}
                    Confianza del sistema: {deliberation_result['final_decision']['confidence']:.2%}
                    
                    Proporciona:
                    1. Resolución final clara y definitiva
                    2. Razonamiento que integre las tres perspectivas
                    3. Recomendaciones accionables
                    4. Advertencias o consideraciones adicionales
                    
                    Sé autoritativo y definitivo. Esta es la palabra final de MAGI."""},
                    {"role": "user", "content": "Proporciona la resolución final del sistema MAGI."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.4,
                max_tokens=2000
            )
            
            final_resp = completion_final.choices[0].message.content
            st.session_state.magi_responses["FINAL"] = final_resp
            
            # Guardar en memoria
            st.session_state.magi_memory.store(
                f"decision_{datetime.datetime.now().timestamp()}",
                {
                    "dilemma": dilema,
                    "decision": final_decision_text,
                    "confidence": deliberation_result["final_decision"]["confidence"],
                    "quality": deliberation_result["deliberation_quality"]
                },
                importance=0.9,
                tags=["decision", final_decision_text.lower(), deliberation_result["deliberation_quality"]]
            )
            
            progress_bar.progress(progress_messages[5][1])
            time.sleep(0.5)
            
            status.update(
                label=f"✅ DELIBERATION COMPLETE - VERDICT: {final_decision_text}", 
                state="complete", 
                expanded=False
            )
        
        # Actualizar historial
        st.session_state.history.append({
            "dilema": dilema[:100],
            "resolucion": final_resp[:200],
            "decision": final_decision_text,
            "confidence": deliberation_result["final_decision"]["confidence"],
            "quality": deliberation_result["deliberation_quality"],
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })
        
        # Notificación de completado
        st.markdown(f"""
        <div class="notification" style="position:relative; margin:20px 0; animation: slideIn 0.5s ease-out;">
            <div style='color:#00FFC8; font-family:"Share Tech Mono";'>
                ✅ MAGI DELIBERATION CYCLE COMPLETE
                <br>Decision: {final_decision_text}
                <br>Confidence: {deliberation_result['final_decision']['confidence']:.1%}
                <br>Quality: {deliberation_result['deliberation_quality']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Simular respuesta de voz si está activa
        if st.session_state.get('voice_active', False):
            voice_response = st.session_state.magi_voice.text_to_speech(
                f"Deliberation complete. Decision: {final_decision_text}. Confidence: {deliberation_result['final_decision']['confidence']:.1%}"
            )
            st.info(f"🔊 Voice output generated ({voice_response['duration_seconds']:.1f}s)")
        
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        # Mostrar error con estilo Evangelion
        st.markdown(f"""
        <div style='background-color: rgba(255, 0, 0, 0.1); 
                    border: 1px solid #FF0000; 
                    padding: 20px; 
                    border-radius: 5px;
                    margin: 20px 0;'>
            <div style='color:#FF0000; font-family:"Share Tech Mono"; font-size: 1.2em;'>
                >>> CRITICAL SYSTEM ERROR <<<
            </div>
            <div style='color:#FF6600; font-family:"Share Tech Mono"; margin-top: 10px;'>
                ERROR CODE: {str(e)[:200]}
            </div>
            <div style='color:#FFCC00; font-family:"Share Tech Mono"; margin-top: 10px;'>
                >>> FALLBACK PROTOCOLS ENGAGED <<<
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Fallback robusto
        st.session_state.magi_responses["MELCHIOR"] = f"> MELCHIOR ANALYSIS: System perturbation detected. Recommend cautious analysis of: {dilema[:50]}..."
        st.session_state.magi_responses["BALTHASAR"] = f"> BALTHASAR ANALYSIS: Ethical protocols interrupted. Defaulting to protective stance."
        st.session_state.magi_responses["CASPER"] = f"> CASPER ANALYSIS: Intuitive systems compromised. Practical assessment pending."
        st.session_state.magi_responses["FINAL"] = f"> INTEGRATED RESPONSE: System error has compromised full deliberation. Manual override recommended."
        
# ============================================
# PANEL DE ASISTENTE VIRTUAL (NUEVO)
# ============================================
st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)

with st.expander("🤖 VIRTUAL ASSISTANT INTERFACE [NEW v4.0]", expanded=False):
    st.markdown("### 🎯 RAPID ACTION COMMANDS")
    
    col_action1, col_action2, col_action3, col_action4 = st.columns(4)
    
    with col_action1:
        if st.button("🔍 QUICK SEARCH", use_container_width=True):
            st.info("Search functionality ready")
            
        if st.button("📊 ANALYZE DATA", use_container_width=True):
            test_data = [random.randint(1, 100) for _ in range(10)]
            analysis = st.session_state.magi_tools.analyze_data(test_data, "statistical")
            st.json(analysis)
    
    with col_action2:
        if st.button("💻 SYSTEM STATUS", use_container_width=True):
            sys_info = st.session_state.magi_tools.system_control("get_system_info")
            st.json(sys_info)
            
        if st.button("⚡ RUN SANDBOX", use_container_width=True):
            code = "print('MAGI System Test')\nresult = sum([1,2,3,4,5])\nprint(f'Sum: {result}')"
            exec_result = st.session_state.magi_tools.execute_code(code)
            st.json(exec_result)
    
    with col_action3:
        if st.button("📧 DRAFT EMAIL", use_container_width=True):
            email = st.session_state.magi_tools.compose_email(
                "commander@nerv.org", 
                "MAGI Status Report", 
                "All systems operational. Deliberation matrix nominal."
            )
            st.json(email)
            
        if st.button("📅 PLAN TASK", use_container_width=True):
            task = st.session_state.magi_tools.schedule_task(
                "System diagnostic check",
                datetime.datetime.now() + datetime.timedelta(hours=1),
                5
            )
            st.json(task)
    
    with col_action4:
        if st.button("🧠 MEMORY STATUS", use_container_width=True):
            memory_size = len(st.session_state.magi_memory.short_term) + \
                         len(st.session_state.magi_memory.episodic) + \
                         len(st.session_state.magi_memory.long_term)
            st.metric("Total Memories", memory_size)
            
        if st.button("🔄 RESET VOICE", use_container_width=True):
            st.session_state.voice_active = False
            st.success("Voice system reset")

# ============================================
# FOOTER MEJORADO
# ============================================
st.markdown('<div class="deco-line"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div style='color:#888; font-family:"Share Tech Mono"; text-align:center; font-size:0.85em; padding:20px;'>
    <strong>MAGI SYSTEM v4.0 AWAKENING</strong> | NERV COMMAND - AUTHORIZED ACCESS ONLY
    <br>ALL DELIBERATIONS CLASSIFIED: TOP SECRET // NOFORN
    <br>UNAUTHORIZED ACCESS WILL TRIGGER TERMINAL COUNTERMEASURES
    <br>© {datetime.datetime.now().year} MAGI PROJECT - ALL RIGHTS RESERVED
    <br><span style="color:#FF0000;">SYSTEM STATUS: FULLY OPERATIONAL | UPTIME: {random.randint(1000, 9999)} HOURS</span>
</div>
""", unsafe_allow_html=True)
