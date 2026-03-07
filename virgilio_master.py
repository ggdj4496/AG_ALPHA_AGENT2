import os
import sys
import subprocess
import time
import logging
import signal

# Sincronización de Rutas Maestras
BASE_DIR = r"c:\AG_ALPHA_AGENT"
CORE_DIR = os.path.join(BASE_DIR, "AG_ALPHA_CORE")
BRIDGE_DIR = os.path.join(BASE_DIR, "AG_ALPHA_BRIDGE")
sys.path.extend([CORE_DIR, BRIDGE_DIR])

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [MASTER] - %(levelname)s - %(message)s')
logger = logging.getLogger("VIRGILIO_MASTER")

class VirgilioMaster:
    """
    Orquestador Central del Software Virgilio V7.0.
    Gestiona el ciclo de vida de los procesos, la sincronización de memoria y la estabilidad global.
    """
    def __init__(self):
        self.processes = {}
        self.is_running = True

    def start_system(self):
        logger.info("🚀 INICIANDO ORQUESTADOR VIRGILIO [ALPHA-MASTER TIERA]...")
        
        # 1. Iniciar Puente (Independiente para máxima estabilidad)
        self.launch_component("PILOT", os.path.join(BRIDGE_DIR, "virgilio_pilot.py"))
        
        # 2. Iniciar Núcleo de Procesamiento (Engine)
        self.launch_component("ENGINE", os.path.join(CORE_DIR, "virgilio_engine.py"))

        # 3. Iniciar Investigador Autónomo (Background Service)
        self.launch_component("AIGEN", os.path.join(CORE_DIR, "autonomous_researcher.py"))

        # 4. Iniciar Núcleo GUI (Interface de Usuario)
        self.launch_component("GUI", os.path.join(CORE_DIR, "virgilio_gui.py"))

        try:
            while self.is_running:
                self.monitor_health()
                time.sleep(10)
        except KeyboardInterrupt:
            self.shutdown()

    def launch_component(self, name, script_path):
        logger.info(f"📦 Arrancando componente: {name} ({script_path})")
        proc = subprocess.Popen([sys.executable, script_path], 
                                creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.processes[name] = proc

    def monitor_health(self):
        for name, proc in list(self.processes.items()):
            if proc.poll() is not None:
                logger.warning(f"⚠️ Componente {name} detectado como CAÍDO. Reiniciando...")
                script_path = proc.args[1]
                self.launch_component(name, script_path)

    def shutdown(self):
        logger.info("🛑 APAGADO CONTROLADO DEL SISTEMA...")
        self.is_running = False
        for name, proc in self.processes.items():
            logger.info(f"Finalizando {name}...")
            proc.terminate()
        sys.exit(0)

if __name__ == "__main__":
    master = VirgilioMaster()
    master.start_system()
