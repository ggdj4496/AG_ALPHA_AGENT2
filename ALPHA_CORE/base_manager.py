import abc
import logging
from enum import Enum
from typing import Dict, Any

class ManagerState(Enum):
    """Estados del ciclo de vida del Manager."""
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    ERROR = "ERROR"
    MAINTENANCE = "MAINTENANCE"

class BaseManager(abc.ABC):
    """
    Clase Base Abstracta para todos los Managers de Virgilio V8.0 GOLD.
    Proporciona una interfaz estandarizada de nivel ingeniería para el ciclo de vida y telemetría.
    """
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"VIRGILIO_{name.upper()}")
        self.state = ManagerState.INACTIVE
        self.last_update = 0.0

    @abc.abstractmethod
    def start(self) -> None:
        """Inicialización atómica del módulo."""
        pass

    @abc.abstractmethod
    def stop(self) -> None:
        """Apagado controlado y liberación de recursos."""
        pass

    @abc.abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Devuelve telemetría detallada del módulo."""
        pass

    def log_info(self, message: str) -> None:
        self.logger.info(f"[{self.name}] {message}")

    def log_error(self, message: str) -> None:
        self.logger.error(f"[{self.name}] {message}")

    def log_warning(self, message: str) -> None:
        self.logger.warning(f"[{self.name}] {message}")
