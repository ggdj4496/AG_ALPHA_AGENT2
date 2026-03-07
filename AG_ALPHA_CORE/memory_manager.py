import sqlite3
import os
import logging
import json
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VIRGILIO_MEMORY")

class MemoryManager:
    """
    Sistema de Memoria a Largo Plazo (LTM) de Virgilio.
    Implementa Arquetipos Neuronales basados en Z-BRAIN para almacenamiento estructurado.
    """
    def __init__(self):
        self.db_path = r"c:\AG_ALPHA_AGENT\AG_ALPHA_BRAIN\VIRGILIO_LTM.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._initialize_db()

    def _initialize_db(self):
        """Crea las tablas maestras si no existen."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Tabla de Hechos (Arquetipos)
            cursor.execute('''CREATE TABLE IF NOT EXISTS neural_archetypes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                key TEXT UNIQUE,
                                value TEXT,
                                category TEXT,
                                priority INTEGER DEFAULT 1,
                                timestamp REAL)''')
            # Tabla de Historial (Experiencias)
            cursor.execute('''CREATE TABLE IF NOT EXISTS experience_log (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                session_id TEXT,
                                content TEXT,
                                importance REAL,
                                timestamp REAL)''')
            conn.commit()

    def store_archetype(self, key, value, category="General", priority=1):
        """Almacena un fragmento de conocimiento estructurado."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT OR REPLACE INTO neural_archetypes 
                                  (key, value, category, priority, timestamp) 
                                  VALUES (?, ?, ?, ?, ?)''', 
                               (key, json.dumps(value), category, priority, time.time()))
                conn.commit()
                logger.info(f"🧠 Arquetipo '{key}' inyectado en LTM.")
        except Exception as e:
            logger.error(f"Error en LTM (Archetype): {e}")

    def query_memory(self, query):
        """Busca en el historial y arquetipos por palabras clave."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT key, value FROM neural_archetypes WHERE key LIKE ?", (f"%{query}%",))
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error en LTM (Query): {e}")
            return []

if __name__ == "__main__":
    memory = MemoryManager()
    memory.store_archetype("Identidad", {"name": "Virgilio", "mode": "Alpha-Master"}, "Identity")
    print("Memory Manager [ALPHA-TIER] Operativo.")
