import logging
import threading
from typing import Dict, Any, Optional
from base_manager import BaseManager
from managers.ai_manager import AIManager
from managers.system_auditor import SystemAuditor
from managers.network_optimizer import NetworkOptimizer

class CoreOrchestrator:
    """
    Orquestador Interno de Virgilio V8.0 GOLD.
    Arquitectura Singleton Thread-Safe para gestión de dependencias criticas.
    """
    _instance: Optional['CoreOrchestrator'] = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CoreOrchestrator, cls).__new__(cls)
                cls._instance.initialized = False
            return cls._instance

    def __init__(self):
        if self.initialized:
            return
        
        self.logger = logging.getLogger("VIRGILIO_CORE")
        self.managers: Dict[str, Any] = {
            "ai": AIManager(),
            "auditor": SystemAuditor(),
            "network": NetworkOptimizer(),
            "engine": VirgilioEngine(),
            "lab": LabManager()
        }
        self.version = "V8.0.0-GOLD"
        self.initialized = True

    def boot_all(self) -> None:
        """Secuencia de arranque orquestada de todos los servicios core."""
        self.logger.info(f"--- [CORE ORCHESTRATOR {self.version}] BOOT START ---")
        for name, manager in self.managers.items():
            try:
                manager.start()
                self.logger.info(f"✅ Módulo {name.upper()} operativo.")
            except Exception as e:
                self.logger.error(f"❌ CRITICAL FAILURE en {name.upper()}: {e}", exc_info=True)

    def shutdown_all(self) -> None:
        """Secuencia de apagado seguro con persistencia de estado."""
        self.logger.info(f"--- [CORE ORCHESTRATOR {self.version}] SHUTDOWN ---")
        for name, manager in self.managers.items():
            try:
                manager.stop()
                self.logger.info(f"🛑 {name.upper()} detenido.")
            except Exception as e:
                self.logger.error(f"⚠️ Error al detener {name.upper()}: {e}")

    def get_manager(self, name: str) -> Optional[BaseManager]:
        """Recupera un manager por su identificador único."""
        return self.managers.get(name)

    def get_full_status(self) -> Dict[str, Any]:
        """Agrega telemetría de todo el ecosistema core."""
        return {
            "version": self.version,
            "system_health": "INTEGRITY_OK",
            "managers": {name: m.get_status() for name, m in self.managers.items()}
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
    core = CoreOrchestrator()
    core.boot_all()
    print(core.get_full_status())
