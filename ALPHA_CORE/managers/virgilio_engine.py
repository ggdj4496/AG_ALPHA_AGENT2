import os
import sys
import asyncio
import psutil
import threading
import time
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from base_manager import BaseManager, ManagerState

class VirgilioEngine(BaseManager):
    """
    Núcleo de Procesamiento Virgilio V8.0 GOLD.
    Motor de alto rendimiento para autocuración y gestión de recursos.
    """
    def __init__(self):
        super().__init__("Engine")
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Sincronización de Entorno
        env_path = os.path.join(self.root_dir, "ALPHA_CORE", "config", ".env")
        load_dotenv(dotenv_path=env_path)
        
        self.current_model = "google/gemini-2.0-flash-001"
        self.lock = threading.Lock()

    def start(self) -> None:
        """Activa el motor de monitoreo y purga."""
        self.log_info("🚀 Motor Virgilio V8.0 GOLD activado.")
        self.state = ManagerState.ACTIVE
        threading.Thread(target=self.run_background_monitor, daemon=True).start()

    def stop(self) -> None:
        """Detención orquestada del motor."""
        self.log_info("🛑 Deteniendo Motor V8.0.")
        self.state = ManagerState.INACTIVE

    def get_status(self) -> Dict[str, Any]:
        """Telemetría de carga y estado del motor."""
        return {
            "name": self.name,
            "state": self.state.value,
            "engine_load": f"{psutil.cpu_percent()}%",
            "threads_active": threading.active_count()
        }

    def run_background_monitor(self) -> None:
        """Monitor de autocuración de alta disponibilidad."""
        cleanup_counter = 0
        while self.state == ManagerState.ACTIVE:
            cleanup_counter += 1
            if cleanup_counter >= 60: # Ciclo de purga extendido
                self.purge_temporary_data()
                cleanup_counter = 0
            time.sleep(10)

    def purge_temporary_data(self) -> None:
        """Mantenimiento atómico de directorios de intercambio."""
        self.log_info("🧹 Ejecutando purga de datos temporales...")
        data_dir = os.path.join(self.root_dir, "ALPHA_CORE", "data")
        chimenea = os.path.join(data_dir, "CHIMENEA")
        cajon = os.path.join(data_dir, "CAJON")
        
        os.makedirs(chimenea, exist_ok=True)
        os.makedirs(cajon, exist_ok=True)

        try:
            for f in os.listdir(cajon):
                src = os.path.join(cajon, f)
                dst = os.path.join(chimenea, f)
                if os.path.isfile(src):
                    os.rename(src, dst)
            self.log_info("✅ Purga completada.")
        except Exception as e:
            self.log_error(f"Error en purga: {e}")

    async def start_loop(self) -> None:
        """Bucle asíncrono para integración con orquestadores externos."""
        self.start()
        try:
            while self.state == ManagerState.ACTIVE:
                await asyncio.sleep(1)
        except Exception as e:
            self.log_error(f"Fallo en el bucle principal: {e}")
            self.state = ManagerState.ERROR

if __name__ == "__main__":
    engine = VirgilioEngine()
    asyncio.run(engine.start_loop())
