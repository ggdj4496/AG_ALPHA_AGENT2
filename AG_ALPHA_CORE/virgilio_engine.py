import os
import sys
import asyncio
import time
import psutil
import threading
import logging
from dotenv import load_dotenv

# Log System
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VIRGILIO_ENGINE")

load_dotenv(dotenv_path="../AG_ALPHA_BRAIN/.env")

# Sincronización de Rutas para ejecución como módulo
sys.path.append(os.path.dirname(__file__))

class VirgilioEngine:
    """
    Nucleo de Procesamiento Virgilio V7.0 Gold.
    Gestiona la lógica de autocuración, purga y optimización de recursos.
    """
    def __init__(self):
        self.name = "VIRGILIO"
        from ai_manager import AIManager
        from network_optimizer import NetworkOptimizer
        self.ai = AIManager()
        self.net = NetworkOptimizer()
        self.current_model = "google/gemini-2.0-flash-001"
        self.control_timer = 0
        self.MAX_CONTROL_TIME = 15 * 60
        self.is_running = True
        self.lock = threading.Lock()
        logger.info(f"[{self.name}] Nucleo de Arquitectura Unificada Activado.")

    async def start_engine(self):
        """Inicializa todos los subsistemas del motor y sincroniza nubes."""
        logger.info("🚀 Activando Motor Virgilio V7.0 [Master Edition]")
        
        # Sincronización Inicial de Consciencia (Backup en la nube)
        if self.ai:
            await self.ai.sync_knowledge_to_cloud()
            
        # Lanzar monitor de segundo plano en hilo aparte
        monitor_thread = threading.Thread(target=self.run_background_monitor, daemon=True)
        monitor_thread.start()
        
        logger.info("✅ Motor y Monitor operativos. Arquitectura Unificada Certificada.")

    def set_consciousness(self, model_key):
        """Cambia el modelo de IA dinámicamente."""
        models = {
            "gemini": "google/gemini-2.0-flash-001",
            "gpt": "openai/gpt-4o",
            "deepseek": "deepseek/deepseek-chat"
        }
        self.current_model = models.get(model_key, self.current_model)
        logger.info(f"Consciencia cambiada a: {self.current_model}")
        return f"Modelo cambiado a {model_key}"

    def optimize_system(self):
        """Optimización de recursos de alto nivel."""
        logger.info("Iniciando purga de procesos redundantes...")
        optimized_count = 0
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                critical = ["explorer.exe", "python.exe", "SystemSettings.exe", "Taskmgr.exe", "svchost.exe"]
                if proc.info['name'] not in critical and proc.info['cpu_percent'] > 15.0:
                    logger.info(f"Monitorizando carga alta: {proc.info['name']} (PID: {proc.info['pid']})")
                    optimized_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return f"Escaneo de {optimized_count} procesos completado."

    async def execute_command(self, cmd_text):
        """Enrutador de comandos con manejo de excepciones."""
        logger.info(f"Comando recibido: {cmd_text}")
        try:
            if "optimiza" in cmd_text.lower():
                return self.optimize_system()
            return await self.ai.ask_openrouter(cmd_text)
        except Exception as e:
            logger.error(f"Error ejecutando comando: {e}")
            return f"Error en ejecucion: {str(e)}"

    def take_peripheral_control(self, action_func, *args):
        """Control seguro con bloqueo de hilo."""
        with self.lock:
            self.control_timer = time.time()
            logger.info("Mando periferico activo...")
            action_func(*args)

    def run_background_monitor(self):
        """Monitor de seguridad y limpieza constante."""
        cleanup_counter = 0
        while self.is_running:
            if self.control_timer > 0 and (time.time() - self.control_timer > self.MAX_CONTROL_TIME):
                logger.warning("SAFETY TIMEOUT: Liberando mando.")
                self.control_timer = 0
            
            cleanup_counter += 1
            if cleanup_counter >= 6:
                self.purge_temporary_data()
                cleanup_counter = 0

            time.sleep(10)

    def purge_temporary_data(self):
        """Mantenimiento profesional de archivos."""
        logger.info("VIRGILIO: Mantenimiento de archivos activo.")
        chimenea = r"c:\AG_ALPHA_AGENT\AG_ALPHA_LAB\CHIMENEA"
        cajon = r"c:\AG_ALPHA_AGENT\AG_ALPHA_LAB\CAJON"
        if os.path.exists(cajon):
            for f in os.listdir(cajon):
                try: os.rename(os.path.join(cajon, f), os.path.join(chimenea, f))
                except: pass

        temp_dir = r"c:\AG_ALPHA_AGENT\AG_ALPHA_BRIDGE\temp_downloads"
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                if "tracker" in f: continue
                try: os.remove(os.path.join(temp_dir, f))
                except: pass

    async def start_loop(self):
        """Bucle Infinito de Vida del Motor."""
        await self.start_engine()
        while self.is_running:
            await asyncio.sleep(1)

if __name__ == "__main__":
    engine = VirgilioEngine()
    try:
        asyncio.run(engine.start_loop())
    except Exception as e:
        logger.error(f"COLAPSO DEL MOTOR: {e}")
