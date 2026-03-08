import psutil
import platform
import os

def check_hardware():
    report_path = r"c:\AG_ALPHA_AGENT\AG_ALPHA_BRAIN\System_Audit.txt"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write("=== REPORTE DE SISTEMA VIRGILIO ===\n")
        f.write(f"SO: {platform.system()} {platform.release()}\n")
        f.write(f"Procesador: {platform.processor()}\n")
        f.write(f"Memoria RAM: {psutil.virtual_memory().total / (1024**3):.2f} GB\n")
        f.write("\n--- Procesos en Segundo Plano ---\n")
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.info['cpu_percent'] > 5.0:
                    f.write(f"PID: {proc.info['pid']} | Name: {proc.info['name']} | CPU: {proc.info['cpu_percent']}%\n")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    
    print(f"Escaneo completado. Reporte generado en: {report_path}")

if __name__ == "__main__":
    check_hardware()
