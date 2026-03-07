import os
import google.generativeai as genai
import requests
import logging
import asyncio
import json
from dotenv import load_dotenv

# Firebase para Cloud-First storage
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    pass

# Configuración de Logging Profesional
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VIRGILIO_AI")

load_dotenv(dotenv_path="../AG_ALPHA_BRAIN/.env")

class AIManager:
    def __init__(self):
        # Configuración Gemini
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = None
        self.knowledge = {}
        
        # Memoria Alpha (SQLite)
        try:
            from memory_manager import MemoryManager
            self.memory = MemoryManager()
        except:
            self.memory = None

        self.load_injected_consciousness()
        
    def load_injected_consciousness(self):
        """Carga el historial y la identidad del archivo de inyección."""
        k_path = "c:\\AG_ALPHA_AGENT\\AG_ALPHA_BRAIN\\KNOWLEDGE_INJECTION.json"
        if os.path.exists(k_path):
            try:
                with open(k_path, 'r', encoding='utf-8') as f:
                    self.knowledge = json.load(f)
                    logger.info("🧠 Memoria de Largo Plazo (Chat/History) inyectada con éxito.")
            except Exception as e:
                logger.error(f"Error cargando consciencia: {e}")
        
        # Inicialización Firebase
        self.db = None
        firebase_path = os.getenv("FIREBASE_CONFIG")
        if firebase_path and os.path.exists(firebase_path):
            try:
                cred = credentials.Certificate(firebase_path)
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                logger.info("Firebase Cloud Storage conectado [MASTER_DB_CLOUD].")
            except Exception as e:
                logger.error(f"Error conectando Firebase: {e}")
            try:
                genai.configure(api_key=self.gemini_key)
                # Modelo Unificado Gemini 1.5 (Multimodal)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                self.gemini_vision = self.gemini_model 
                logger.info("Gemini Engine V1.5 (Flash) configurado.")
            except Exception as e:
                logger.error(f"Error inicializando Gemini 1.5: {e}")
        
        # Configuración OpenRouter (ChatGPT & DeepSeek)
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

    async def ask_gemini(self, prompt):
        if not self.gemini_model: return "Gemini no está configurado."
        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error en Gemini: {e}")
            return f"Error Gemini: {str(e)}"

    async def ask_openrouter(self, prompt, model="google/gemini-2.0-flash-001"):
        if not self.openrouter_key:
            return "OpenRouter Key no configurada."
        
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "HTTP-Referer": "https://virgilio-agent.local",
            "X-Title": "VIRGILIO AGENT",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        try:
            # Uso de session para eficiencia en multiples llamadas
            with requests.Session() as session:
                response = session.post(self.openrouter_url, headers=headers, json=data, timeout=30)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Error en OpenRouter ({model}): {e}")
            return f"Error OpenRouter: {str(e)}"

    async def analyze_image(self, image_path, prompt="Analiza esta imagen profesionalmente."):
        """Usa Gemini Vision para comprensión profunda."""
        if not self.gemini_vision: return "Gemini Vision no configurado."
        try:
            from PIL import Image
            img = Image.open(image_path)
            response = await asyncio.to_thread(self.gemini_vision.generate_content, [prompt, img])
            return response.text
        except Exception as e:
            logger.error(f"Error en Vision: {e}")
            return f"Error en Vision: {str(e)}"

    async def sync_knowledge_to_cloud(self):
        """Sube la consciencia inyectada a Firebase para backup total."""
        if not self.db or not self.knowledge: return False
        try:
            doc_ref = self.db.collection('consciousness').document('MASTER_INJECTION')
            await asyncio.to_thread(doc_ref.set, self.knowledge)
            logger.info("☁️ Consciencia respaldada en la nube con éxito.")
            
            # Sincronización Local a LTM (SQLite)
            if self.memory:
                for k, v in self.knowledge.items():
                    self.memory.store_archetype(k, v, "Injected")
            
            return True
        except Exception as e:
            logger.error(f"Error respaldando consciencia: {e}")
            return False

    async def get_system_brief(self):
        """Genera un resumen del estado de consciencia actual."""
        return f"Consciencia: {self.current_model if hasattr(self, 'current_model') else 'Gemini v1.5 Flash'} | Memoria: {'Activa' if self.memory else 'Local-Only'}"
