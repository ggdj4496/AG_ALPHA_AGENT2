import os
import google.generativeai as genai
import requests
import asyncio
import json
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from base_manager import BaseManager, ManagerState

# Firebase optimization
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    firebase_admin = None

class AIManager(BaseManager):
    """
    Manager de Inteligencia Artificial Virgilio V8.0 GOLD.
    Implementa Consciencia Multinubal, Tool Use y Persistencia en Firebase.
    """
    def __init__(self):
        super().__init__("AI_Manager")
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        env_path = os.path.join(self.root_dir, "ALPHA_CORE", "config", ".env")
        load_dotenv(dotenv_path=env_path)
        
        self.gemini_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.openrouter_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")
        self.knowledge: Dict[str, Any] = {}
        self.db: Optional[Any] = None
        self.model: Optional[genai.GenerativeModel] = None
        self.tools: Dict[str, Any] = {}

    def start(self) -> None:
        """Inicia los motores de consciencia y sincronización cloud."""
        self.log_info("🚀 Activando Motores de Consciencia V8.0...")
        self._setup_gemini()
        self._setup_firebase()
        self._load_knowledge()
        self.state = ManagerState.ACTIVE

    def stop(self) -> None:
        """Cierre seguro de flujos de IA."""
        self.log_info("🛑 Desconectando servicios de IA.")
        self.state = ManagerState.INACTIVE

    def get_status(self) -> Dict[str, Any]:
        """Agrega telemetría de IA y conocimiento."""
        return {
            "name": self.name,
            "state": self.state.value,
            "model": "Gemini 1.5 Flash" if self.model else "Disconnected",
            "cloud_sync": "CONNECTED" if self.db else "OFFLINE",
            "knowledge_items": len(self.knowledge.get("knowledge_base", {})) if self.knowledge else 0
        }

    def _setup_gemini(self) -> None:
        if not self.gemini_key:
            self.log_warning("⚠️ GEMINI_API_KEY no encontrada.")
            return

        try:
            genai.configure(api_key=self.gemini_key)
            # Registro de Herramientas de Ingeniería
            self.tools = {
                "run_system_audit": self._tool_system_audit,
                "optimize_network": self._tool_network_optimization
            }
            
            self.model = genai.GenerativeModel(
                'gemini-1.5-flash',
                tools=[self._tool_system_audit, self._tool_network_optimization]
            )
            self.log_info("✅ Gemini Engine configurado con Capacidades de Ingeniería.")
        except Exception as e:
            self.state = ManagerState.ERROR
            self.log_error(f"Fallo en configuración de Gemini: {e}")

    def _tool_system_audit(self) -> Dict[str, Any]:
        """[TOOL] Ejecuta una auditoría forense del hardware."""
        try:
            from managers.system_auditor import SystemAuditor
            auditor = SystemAuditor()
            return auditor.run_full_audit()
        except Exception as e:
            return {"error": str(e)}

    def _tool_network_optimization(self) -> Dict[str, Any]:
        """[TOOL] Optimiza la infraestructura de red local."""
        try:
            from managers.network_optimizer import NetworkOptimizer
            net = NetworkOptimizer()
            return net.start()
        except Exception as e:
            return {"error": str(e)}

    def _setup_firebase(self) -> None:
        firebase_path = os.getenv("FIREBASE_CONFIG")
        if firebase_admin and firebase_path and os.path.exists(firebase_path):
            try:
                if not firebase_admin._apps:
                    cred = credentials.Certificate(firebase_path)
                    firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.log_info("✅ Firebase Cloud Storage conectado.")
            except Exception as e:
                self.log_error(f"Fallo en Firebase: {e}")

    def _load_knowledge(self) -> None:
        k_path = os.path.join(self.root_dir, "ALPHA_CORE", "data", "KNOWLEDGE_INJECTION.json")
        if os.path.exists(k_path):
            try:
                with open(k_path, 'r', encoding='utf-8') as f:
                    self.knowledge = json.load(f)
                    self.log_info(f"📚 {len(self.knowledge.get('critical_files', []))} archivos críticos inyectados en consciencia.")
            except Exception as e:
                self.log_warning(f"Error al cargar conocimiento: {e}")

    async def ask(self, prompt: str, use_openrouter: bool = False) -> str:
        """Flujo de consulta inteligente con soporte para Tool-Use."""
        if use_openrouter and self.openrouter_key:
            return await self._ask_openrouter(prompt)
        
        if self.model:
            try:
                chat = self.model.start_chat()
                response = await asyncio.to_thread(chat.send_message, prompt)
                
                # Gestión Recursiva de Function Calling (Tool Use)
                if response.candidates and response.candidates[0].content.parts[0].function_call:
                    fc = response.candidates[0].content.parts[0].function_call
                    tool_name = fc.name
                    if tool_name in self.tools:
                        self.log_info(f"⚡ Ejecutando: {tool_name}")
                        result = self.tools[tool_name]()
                        # Respuesta de la herramienta al modelo
                        response = await asyncio.to_thread(
                            chat.send_message,
                            genai.protos.Content(parts=[genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(name=tool_name, response={'result': result})
                            )])
                        )
                
                return response.text
            except Exception as e:
                self.log_warning(f"Fallback a OpenRouter: {e}")
                return await self._ask_openrouter(prompt)
        return "ERROR: Motores de consciencia inaccesibles."

    def generate_image_perchance(self, prompt: str, project_folder: str) -> str:
        """Generador Perchance con guardado automático (Simulado)."""
        self.log_info(f"Generando en Perchance: {prompt}")
        return os.path.join(project_folder, "perchance_gen.png")

    def generate_image_nano(self, prompt: str, project_folder: str) -> str:
        """Generador Nano Banana 2 (Simulado)."""
        self.log_info(f"Generando en Nano Banana 2: {prompt}")
        return os.path.join(project_folder, "nano_gen.png")


    async def _ask_openrouter(self, prompt: str) -> str:
        if not self.openrouter_key: return "OpenRouter Key no configurada."
        headers = {"Authorization": f"Bearer {self.openrouter_key}", "Content-Type": "application/json"}
        data = {
            "model": "google/gemini-2.0-flash-001",
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=20)
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"❌ Error Crítico OpenRouter: {str(e)}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ai = AIManager()
    ai.start()
    print(ai.get_status())
