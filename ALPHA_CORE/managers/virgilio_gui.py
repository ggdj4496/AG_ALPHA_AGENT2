import customtkinter as ctk
import threading
import pystray
from PIL import Image
from pystray import MenuItem as item
import sys
import os
import time
from typing import Dict, Any, Optional
from base_manager import BaseManager, ManagerState

# Config Estética Lila V8 GOLD
LILA_PRIMARY = "#9B59B6"
LILA_DARK = "#8E44AD"
BG_DARK = "#1A1A1A"

class VirgilioGUI(ctk.CTk, BaseManager):
    """
    Interface de Usuario Maestra V8.0 GOLD.
    Arquitectura de alto rendimiento con Lazy Loading y monitoreo de estado.
    """
    def __init__(self):
        # Inicialización de multi-herencia
        ctk.CTk.__init__(self)
        BaseManager.__init__(self, "GUI")
        
        # Sincronización de Rutas V8.0 GOLD
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Icono y Estilo
        try:
            icon_path = os.path.join(self.root_dir, "ALPHA_CORE", "icon.ico")
            if os.path.exists(icon_path):
                self.after(200, lambda: self.iconbitmap(icon_path))
        except Exception: pass
        
        # Managers con carga lazy
        self.ai: Optional[Any] = None
        self.audio: Optional[Any] = None
        self.alpha_master_active = False
        self.tray_icon = None

        self.setup_ui()

    def start(self) -> None:
        """Punto de entrada para el ciclo de vida de la interface."""
        self.log_info("🚀 Lanzando Interface Gráfica V8.0 GOLD...")
        self.state = ManagerState.ACTIVE
        
        # Iniciar managers en segundo plano para no bloquear el arranque
        threading.Thread(target=self._initialize_core_managers, daemon=True).start()
        self.mainloop()

    def _initialize_core_managers(self) -> None:
        try:
            from managers.ai_manager import AIManager
            from managers.audio_manager import AudioManager
            self.ai = AIManager()
            self.audio = AudioManager()
            self.ai.start()
            self.audio.start()
            self.append_log("✅ Motores Core sincronizados.")
        except Exception as e:
            self.log_error(f"Fallo en inicialización de Managers: {e}")

    def stop(self) -> None:
        """Cierre seguro y liberación de hilos."""
        self.log_info("🛑 Finalizando sesión GUI.")
        self.state = ManagerState.INACTIVE
        self.quit_app()

    def get_status(self) -> Dict[str, Any]:
        """Telemetría de la interface."""
        return {
            "name": self.name,
            "state": self.state.value,
            "mode": "ALPHA_TIER" if self.alpha_master_active else "STANDARD"
        }

    def setup_ui(self) -> None:
        """Construcción de la UI con estética Lila-Dark profesional."""
        self.title("VIRGILIO V8 GOLD - MASTER EDITION")
        self.geometry("1000x700")
        
        # Header
        self.header = ctk.CTkFrame(self, fg_color=LILA_DARK, height=70, corner_radius=0)
        self.header.pack(fill="x")
        self.title_label = ctk.CTkLabel(self.header, text="VIRGILIO MASTER V8.0 GOLD", font=("Orbitron", 24, "bold"), text_color="white")
        self.title_label.pack(pady=15)

        # Layout: Sidebar + Content
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#111")
        self.sidebar.pack(side="left", fill="y")
        
        self.lbl_sidebar = ctk.CTkLabel(self.sidebar, text="CORE INFRASTRUCTURE", font=("Orbitron", 14, "bold"), text_color=LILA_PRIMARY)
        self.lbl_sidebar.pack(pady=20, padx=10)
        
        self.alpha_toggle = ctk.CTkSwitch(self.sidebar, text="ALPHA UNLEASHED", command=self.toggle_alpha_mode, progress_color="#E74C3C")
        self.alpha_toggle.pack(pady=10, padx=10)

        # Tab View
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color=LILA_PRIMARY)
        self.tabview.pack(padx=20, pady=(10, 20), fill="both", expand=True)

        self.tab_main = self.tabview.add("🚀 COMMAND")
        self.tab_chat = self.tabview.add("💬 NEURAL")
        self.tab_logs = self.tabview.add("📄 SYSTEM")

        # Consola de Logs Profesional
        self.console = ctk.CTkTextbox(self.tab_logs, fg_color="#0D0D0D", text_color="#A569BD", font=("Consolas", 12))
        self.console.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones de Acción
        self.scroll_core = ctk.CTkScrollableFrame(self.tab_main, fg_color="transparent")
        self.scroll_core.pack(fill="both", expand=True)
        
        self.create_button("📋 EXECUTE SYSTEM AUDIT", self.run_full_audit, fg_color=LILA_PRIMARY, parent=self.scroll_core).pack(pady=8, padx=20, fill="x")
        self.create_button("📡 SYNC INFRASTRUCTURE", self.sync_wifi, parent=self.scroll_core).pack(pady=8, padx=20, fill="x")
        self.create_button("🧹 ATOMIC PURGE", self.run_purge, parent=self.scroll_core).pack(pady=8, padx=20, fill="x")

    def create_button(self, text: str, command: Any, fg_color: Optional[str] = None, parent: Any = None) -> ctk.CTkButton:
        return ctk.CTkButton(parent or self, text=text, command=command, fg_color=fg_color or "#2C3E50", corner_radius=8, font=("Inter", 12, "bold"), height=45)

    def append_log(self, text: str) -> None:
        timestamp = time.strftime("[%H:%M:%S]")
        self.console.insert("end", f"{timestamp} {text}\n")
        self.console.see("end")

    def toggle_alpha_mode(self) -> None:
        self.alpha_master_active = self.alpha_toggle.get()
        state = "ACTIVO" if self.alpha_master_active else "INACTIVO"
        self.append_log(f"🔥 MODO ALPHA {state}")
        if self.audio: self.audio.speak(f"Modo Alpha {state.lower()}")

    def run_full_audit(self) -> None:
        self.append_log("🔍 Iniciando Auditoría Maestro...")
        threading.Thread(target=self._audit_thread, daemon=True).start()

    def _audit_thread(self) -> None:
        try:
            from managers.system_auditor import SystemAuditor
            auditor = SystemAuditor()
            report = auditor.run_full_audit()
            self.append_log(f"✅ CPU: {report['cpu']['load_percent']}% | RAM: {report['ram']['used']}")
            self.append_log(f"📝 Integridad: {report['system_integrity']}")
        except Exception as e:
            self.append_log(f"❌ Error en auditoría: {e}")

    def sync_wifi(self) -> None:
        self.append_log("📡 Sincronizando Infraestructura de Red...")

    def run_purge(self) -> None:
        self.append_log("🧹 Iniciando Purga de Memoria Atómica...")

    def quit_app(self) -> None:
        if self.tray_icon: self.tray_icon.stop()
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = VirgilioGUI()
    app.start()

if __name__ == "__main__":
    app = VirgilioGUI()
    app.start()
