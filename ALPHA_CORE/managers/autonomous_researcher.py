import os
import psutil
import time
from typing import Dict, Any, Optional
from base_manager import BaseManager, ManagerState

class AutonomousResearcher(BaseManager):
    """
    Investigador Autónomo de Guardia V8.0 GOLD.
    Analiza métricas del sistema y optimiza el conocimiento en periodos de inactividad.
    """
    def __init__(self):
        super().__init__("Researcher")
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.base_dir = os.path.join(self.root_dir, "ALPHA_CORE", "data", "AIGEN")
        os.makedirs(self.base_dir, exist_ok=True)
        self.last_research_topic: Optional[str] = None

    def start(self) -> None:
        """Activa los protocolos de investigación en modo idle."""
        self.log_info("🔍 Investigador Autónomo V8.0 GOLD inicializado.")
        self.state = ManagerState.ACTIVE
        
    def stop(self) -> None:
        """Cesa las operaciones de guardia."""
        self.log_info("🛑 Deteniendo protocolos de investigación.")
        self.state = ManagerState.INACTIVE

    def get_status(self) -> Dict[str, Any]:
        """Telemetría de actividad de guardia."""
        return {
            "name": self.name,
            "state": self.state.value,
            "last_topic": self.last_research_topic or "IDLE",
            "system_ready": self.check_system_availability()
        }

    def check_system_availability(self) -> bool:
        """Verifica si los recursos son suficientes para tareas pesadas."""
        cpu_usage = psutil.cpu_percent(interval=0.5)
        return cpu_usage < 40.0 # Umbral de investigación conservador

    def run_idle_optimization(self, topic: str) -> str:
        """Inicia una tarea de optimización si el sistema lo permite."""
        if self.state != ManagerState.ACTIVE:
            return "ERROR: Manager inactivo."
            
        if not self.check_system_availability():
            return "WAIT: Carga de sistema elevada. Protocolo diferido."
            
        self.last_research_topic = topic
        target_path = os.path.join(self.base_dir, topic.replace(" ", "_").upper())
        os.makedirs(target_path, exist_ok=True)
        
        self.log_info(f"⚡ Optimización de conocimiento iniciada: {topic}")
        return f"OK: Tarea '{topic}' activada en {target_path}."

if __name__ == "__main__":
    res = AutonomousResearcher()
    res.start()
    print(res.get_status())
