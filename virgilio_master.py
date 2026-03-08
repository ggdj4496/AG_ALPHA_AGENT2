import os
import sys
import subprocess
import time
import logging
from collections import Counter

# Sincronización de Rutas Maestras (V8.0 GOLD)
BASE_DIR = r"c:\AG_ALPHA_AGENT"
CORE_DIR = os.path.join(BASE_DIR, "ALPHA_CORE")
MANAGERS_DIR = os.path.join(CORE_DIR, "managers")
BRIDGE_DIR = os.path.join(BASE_DIR, "ALPHA_BRIDGE")
LAB_DIR = os.path.join(BASE_DIR, "ALPHA_LAB")

# Configuración de Paths para Python
sys.path.extend([BASE_DIR, CORE_DIR, MANAGERS_DIR, BRIDGE_DIR, LAB_DIR])

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [MASTER_V8] - %(levelname)s - %(message)s')
logger = logging.getLogger("VIRGILIO_MASTER")

class VirgilioMaster:
    """
    Orquestador Central V8.0 (Alpha-Master Tier).
    Gestiona procesos con protección contra bucles de reinicio (Boot Loop Protection).
    """
    def __init__(self):
        self.processes = {}
        self.failure_count = Counter()
        self.is_running = True
        self.max_failures = 5 # Límite de reinicios seguidos antes de desistir
        self.retry_delay = 10 

    def start_system(self):
        logger.info("🚀 ACTIVANDO PROTOCOLOS MAESTROS V8.0...")
        
        # Mapa de Componentes Críticos
        components = {
            "PILOT": os.path.join(BRIDGE_DIR, "virgilio_pilot.py"),
            "ENGINE": os.path.join(MANAGERS_DIR, "virgilio_engine.py"),
            "AIGEN": os.path.join(MANAGERS_DIR, "autonomous_researcher.py"),
            "GUI": os.path.join(MANAGERS_DIR, "virgilio_gui.py")
        }

        for name, path in components.items():
            if os.path.exists(path):
                self.launch_component(name, path)
            else:
                logger.error(f"❌ Componente no encontrado: {path}")

        try:
            while self.is_running:
                self.monitor_health(components)
                time.sleep(self.retry_delay)
        except KeyboardInterrupt:
            self.shutdown()

    def launch_component(self, name, script_path):
        if self.failure_count[name] >= self.max_failures:
            logger.error(f"🚫 BLOQUEO DE SEGURIDAD: {name} ha fallado demasiadas veces. Revisa los logs.")
            return

        logger.info(f"📦 Desplegando: {name}...")
        try:
            proc = subprocess.Popen([sys.executable, script_path], 
                                    creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.processes[name] = proc
        except Exception as e:
            logger.error(f"Fallo al lanzar {name}: {e}")

    def monitor_health(self, components):
        for name, proc in list(self.processes.items()):
            if proc.poll() is not None:
                self.failure_count[name] += 1
                logger.warning(f"⚠️ {name} caído (Fallo #{self.failure_count[name]}/{self.max_failures}).")
                
                if self.failure_count[name] < self.max_failures:
                    logger.info(f"Reintentando {name} en {self.retry_delay}s...")
                    self.launch_component(name, components[name])
                else:
                    logger.critical(f"💀 {name} ha colapsado definitivamente.")
                    del self.processes[name]

    def shutdown(self):
        logger.info("🛑 DESACTIVANDO SISTEMA...")
        self.is_running = False
        for name, proc in self.processes.items():
            proc.terminate()
        sys.exit(0)

if __name__ == "__main__":
    master = VirgilioMaster()
    master.start_system()

if __name__ == "__main__":
    master = VirgilioMaster()
    master.start_system()
