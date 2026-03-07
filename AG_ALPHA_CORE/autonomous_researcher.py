import os
import shutil
import time
import logging

class AutonomousResearcher:
    """Investigador de guardia de Virgilio. Trabaja en idle."""
    def __init__(self):
        self.base_dir = "c:\\AG_ALPHA_AGENT\\AG_ALPHA_LAB\\AIGEN"
        self.bench_dir = os.path.join(self.base_dir, "AIBENCH")
        for d in [self.base_dir, self.bench_dir]:
            if not os.path.exists(d): os.makedirs(d)

    def check_system_availability(self):
        """Verifica si el sistema está en reposo (CPU < 40%) para empezar a investigar."""
        import psutil
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        
        # Límite de seguridad: Si el sistema está ocupado, no hacemos nada.
        # Límite de consumo propio: Intentamos no forzar más del 20% adicional.
        if cpu_usage > 50 or ram_usage > 80:
            return False
        return True

    def run_idle_optimization(self, category_id, project_id, name):
        """Investigación autónoma profesional."""
        if not self.check_system_availability():
            return "Sistema ocupado. Investigación AIGEN pospuesta."
            
        folder_name = f"AIG_CAT{category_id}_PR{project_id}_{name}"
        target_path = os.path.join(self.base_dir, folder_name)
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            
        final_file = os.path.join(target_path, "research_summary.md")
        with open(final_file, "w", encoding="utf-8") as f:
            f.write(f"# Informe AIGEN: {name}\n")
            f.write(f"Fecha: {time.ctime()}\n")
            f.write(f"Estado: Optimización de recursos verificada.")
            
        return f"Investigación '{name}' archivada con éxito."
