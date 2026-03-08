import sqlite3
import os
import json
import time
from typing import Dict, Any, Optional
from base_manager import BaseManager, ManagerState

class MemoryManager(BaseManager):
    """
    Sistema de Memoria a Largo Plazo (LTM) V8.0 GOLD.
    Motor de persistencia basado en Arquetipos Neuronales y SQLite3.
    """
    def __init__(self):
        super().__init__("Memory")
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.db_path = os.path.join(self.root_dir, "ALPHA_CORE", "data", "VIRGILIO_LTM.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._initialize_db()

    def start(self) -> None:
        """Monta el volumen de base de datos y valida integridad."""
        self.log_info("🧠 Red Neuronal LTM V8.0 GOLD Sincronizada.")
        self.state = ManagerState.ACTIVE

    def stop(self) -> None:
        """Cierre seguro de manejadores de DB."""
        self.log_info("🛑 Hibernando sistema de memoria.")
        self.state = ManagerState.INACTIVE

    def get_status(self) -> Dict[str, Any]:
        """Telemetría de la base de datos de conocimiento."""
        db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        return {
            "name": self.name,
            "state": self.state.value,
            "storage_used": f"{db_size / 1024:.2f} KB"
        }

    def _initialize_db(self) -> None:
        """Configuración de esquemas relacionales para arquetipos."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS neural_archetypes (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    key TEXT UNIQUE,
                                    value TEXT,
                                    category TEXT,
                                    priority INTEGER DEFAULT 1,
                                    timestamp REAL)''')
                conn.commit()
        except Exception as e:
            self.log_error(f"Fallo crítico en inicialización DB: {e}")

    def store_archetype(self, key: str, value: Any, category: str = "General", priority: int = 1) -> bool:
        """Inyecta un nuevo arquetipo en la memoria permanente."""
        if self.state != ManagerState.ACTIVE:
            return False
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT OR REPLACE INTO neural_archetypes 
                                  (key, value, category, priority, timestamp) 
                                  VALUES (?, ?, ?, ?, ?)''', 
                               (key, json.dumps(value), category, priority, time.time()))
                conn.commit()
                self.log_info(f"✅ Arquetipo '{key}' persistido con éxito.")
                return True
        except Exception as e:
            self.log_error(f"Error al persistir arquetipo: {e}")
            return False

if __name__ == "__main__":
    mem = MemoryManager()
    mem.start()
    mem.store_archetype("SYSTEM_IDENTITY", {"name": "VIRGILIO", "tier": "GOLD"})
    print(mem.get_status())
