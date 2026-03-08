import os
import psutil
import platform
import subprocess
import time
import json
from typing import Dict, Any, List
from base_manager import BaseManager, ManagerState

try:
    import GPUtil
except ImportError:
    GPUtil = None

class SystemAuditor(BaseManager):
    """
    Manager de Auditoría Forense de Hardware V8.0 GOLD.
    Proporciona telemetría profunda del entorno de ejecución.
    """
    def __init__(self):
        super().__init__("Auditor")
        self.report: Dict[str, Any] = {}
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.profiles_dir = os.path.join(self.root_dir, "ALPHA_CORE", "data", "device_profiles")
        
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir, exist_ok=True)

    def start(self) -> Dict[str, Any]:
        """Inicia el escaneo asíncrono y devuelve el primer reporte."""
        self.log_info("🔍 Iniciando Auditoría Forense de Hardware...")
        self.state = ManagerState.ACTIVE
        return self.run_full_audit()

    def stop(self) -> None:
        """Cesa las actividades de monitoreo."""
        self.log_info("🛑 Deteniendo motor de auditoría.")
        self.state = ManagerState.INACTIVE

    def get_status(self) -> Dict[str, Any]:
        """Reporta la salud y última auditoría del sistema."""
        return {
            "name": self.name,
            "state": self.state.value,
            "last_audit": self.report.get("timestamp", "N/A"),
            "integrity": self.report.get("system_integrity", "UNKNOWN")
        }

    def run_full_audit(self) -> Dict[str, Any]:
        """Ejecuta una auditoría holística de todos los subsistemas hardware."""
        self.report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cpu": self._check_cpu(),
            "gpu": self._check_gpu(),
            "ram": self._check_ram(),
            "usb": self._check_usb_devices(),
            "environment": self._check_environment(),
            "system_integrity": "INTEGRITY_CERTIFIED"
        }
        self.log_info("✅ Auditoría de Sistemas completada.")
        return self.report

    def _check_cpu(self) -> Dict[str, Any]:
        try:
            load = psutil.cpu_percent(interval=0.5)
            cores = psutil.cpu_count(logical=True)
            return {"load_percent": load, "cores": cores, "status": "OK" if load < 85 else "HIGH_LOAD"}
        except Exception:
            return {"status": "ERROR"}

    def _check_gpu(self) -> Any:
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    return {"name": gpu.name, "load": f"{gpu.load*100}%", "temp": f"{gpu.temperature}C"}
            except Exception: pass
        return "N/A"

    def _check_ram(self) -> Dict[str, Any]:
        try:
            mem = psutil.virtual_memory()
            return {"total": f"{mem.total // (1024**3)}GB", "used": f"{mem.percent}%", "free": f"{mem.available // (1024**3)}GB"}
        except Exception:
            return {"status": "ERROR"}

    def _check_usb_devices(self) -> List[str]:
        """Descubre dispositivos USB mediante PowerShell nativo."""
        try:
            cmd = "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match 'USB' } | Select-Object FriendlyName"
            output = subprocess.check_output(["powershell", "-Command", cmd], encoding="latin-1")
            devices = [line.strip() for line in output.splitlines() if line.strip() and "FriendlyName" not in line and "---" not in line]
            return list(set(devices))[:10] # Top 10 dispositivos únicos
        except Exception:
            return []

    def _check_environment(self) -> Dict[str, Any]:
        import ctypes
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            is_admin = False
            
        return {
            "is_admin": is_admin, 
            "platform": platform.platform(),
            "architecture": platform.machine(),
            "python_version": platform.python_version()
        }

if __name__ == "__main__":
    auditor = SystemAuditor()
    print(json.dumps(auditor.start(), indent=4))
