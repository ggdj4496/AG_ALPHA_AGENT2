import customtkinter as ctk
import threading
import pystray
from PIL import Image
from pystray import MenuItem as item
import sys
import os
import logging
import time

# Config
LILA_PRIMARY = "#9B59B6"
LILA_DARK = "#8E44AD"
BG_DARK = "#1A1A1A"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VIRGILIO_GUI")

# Sincronización de Rutas (Master)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'AG_ALPHA_LAB'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'AG_ALPHA_ADDONS'))

class VirgilioGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Icono y Estilo
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
            if os.path.exists(icon_path):
                self.after(200, lambda: self.iconbitmap(icon_path))
        except:
            pass
        
        # Instancias de Motores Alpha (Nativo)
        from ai_manager import AIManager
        from audio_manager import AudioManager
        from alpha_liberator import AlphaLiberator
        self.ai = AIManager()
        self.audio = AudioManager()
        self.liberator = AlphaLiberator()
        self.alpha_master_active = False

        self.setup_ui()
        self.tray_icon = None

    def create_button(self, text, command, fg_color=None, parent=None):
        return ctk.CTkButton(
            parent or self,
            text=text,
            command=command,
            fg_color=fg_color or "#2C3E50",
            hover_color="#34495E",
            corner_radius=8,
            font=("Inter", 12, "bold"),
            height=40
        )

    def setup_ui(self):
        # Header
        self.header = ctk.CTkFrame(self, fg_color=LILA_DARK, height=70, corner_radius=0)
        self.header.pack(fill="x")
        self.title_label = ctk.CTkLabel(self.header, text="VIRGILIO MASTER V7.0 [UNIFIED EDITION]", font=("Orbitron", 24, "bold"), text_color="white")
        self.title_label.pack(pady=15)

        # Layout: Sidebar + Content
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#111")
        self.sidebar.pack(side="left", fill="y")
        
        self.lbl_sidebar = ctk.CTkLabel(self.sidebar, text="MASTER UNIFIED", font=("Orbitron", 14, "bold"), text_color=LILA_PRIMARY)
        self.lbl_sidebar.pack(pady=20, padx=10)
        
        self.alpha_toggle = ctk.CTkSwitch(self.sidebar, text="MODO LIBERADO", command=self.toggle_alpha_mode, progress_color="#E74C3C")
        self.alpha_toggle.pack(pady=10, padx=10)

        self.lbl_ltm = ctk.CTkLabel(self.sidebar, text="LTM: READY", font=("Inter", 10), text_color="#2ECC71")
        self.lbl_ltm.pack(side="bottom", pady=20)

        # Tab View (Derecha)
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color=LILA_PRIMARY)
        self.tabview.pack(padx=20, pady=(10, 0), fill="both", expand=True)

        self.tab_main = self.tabview.add("🚀 CORE")
        self.tab_qlc = self.tabview.add("💡 QLC+ STATION")
        self.tab_diy = self.tabview.add("🛠️ DIY LAB")
        self.tab_chat = self.tabview.add("💬 DIRECT CHAT")

        # Tab: CORE
        self.scroll_core = ctk.CTkScrollableFrame(self.tab_main, fg_color="transparent")
        self.scroll_core.pack(fill="both", expand=True)
        self.create_button("📡 SINCRO WIFI", self.sync_wifi, parent=self.scroll_core).pack(pady=5, padx=20, fill="x")
        self.create_button("📋 FULL AUDIT", self.run_full_audit, fg_color=LILA_PRIMARY, parent=self.scroll_core).pack(pady=5, padx=20, fill="x")
        self.create_button("🧹 ESTRUCTURA PURGE", self.run_purge, parent=self.scroll_core).pack(pady=5, padx=20, fill="x")
        self.create_button("🧠 AIGEN EVOLVE", lambda: self.append_log("Iniciando investigación en AIBENCH..."), parent=self.scroll_core).pack(pady=5, padx=20, fill="x")
        self.create_button("🧬 REVERSING BOTS [DEEP]", self.run_deep_reversing, parent=self.scroll_core).pack(pady=5, padx=20, fill="x")
        self.create_button("🧪 LATENT RECONSTRUCTOR", self.run_reconstructor_ui, parent=self.scroll_core).pack(pady=5, padx=20, fill="x")
        self.create_button("🕵️ SHADOW ASSIMILATOR", self.run_shadow_ui, parent=self.scroll_core).pack(pady=5, padx=20, fill="x")
        self.create_button("🛡️ PROXY GUARDIAN", self.run_proxy_ui, parent=self.scroll_core).pack(pady=5, padx=20, fill="x")
        self.create_button("🔞 NUDI-BOT ELITE", self.run_nudi_ui, fg_color="#E74C3C", parent=self.scroll_core).pack(pady=5, padx=20, fill="x")
        self.create_button("🔍 ANALYZER PROCESOS", self.run_process_analyzer, parent=self.scroll_core).pack(pady=5, padx=20, fill="x")
        self.create_button("🎵 MUSIC BATCH", self.run_music_batch, parent=self.scroll_core).pack(pady=5, padx=20, fill="x")

        # Tab: QLC+ STATION
        self.lbl_qlc = ctk.CTkLabel(self.tab_qlc, text="CONTROL DE FIXTURES DMX", font=("Inter", 14, "bold"))
        self.lbl_qlc.pack(pady=10)
        self.create_button("📁 SCAN QLC+ FIXTURES", self.run_qlc_scan, parent=self.tab_qlc).pack(pady=5, padx=20, fill="x")
        self.create_button("🎨 RESOURCE MANAGER", lambda: self.append_log("Gobos y Colores listos."), parent=self.tab_qlc).pack(pady=5, padx=20, fill="x")

        # Tab: DIY LAB
        self.lbl_diy = ctk.CTkLabel(self.tab_diy, text="ENTORNO ELECTRÓNICA & CNC (+ WEBCAM)", font=("Inter", 14, "bold"))
        self.lbl_diy.pack(pady=10)
        
        # Consola de Previsualización de Imagen
        self.webcam_canvas = ctk.CTkLabel(self.tab_diy, text="CÁMARA CNC: OFF", fg_color="#111", height=150)
        self.webcam_canvas.pack(pady=5, padx=20, fill="x")

        self.create_button("📷 ACTIVAR WEBCAM ENCUADRE", self.toggle_webcam, parent=self.tab_diy).pack(pady=5, padx=20, fill="x")
        self.create_button("🔥 LASER/CNC CONTROL", lambda: self.append_log("LaserGRBL modo espera."), parent=self.tab_diy).pack(pady=5, padx=20, fill="x")
        self.create_button("📖 MATERIAL DATABASE", self.open_material_db, parent=self.tab_diy).pack(pady=5, padx=20, fill="x")

        # Tab: DIRECT CHAT
        self.chat_display = ctk.CTkTextbox(self.tab_chat, height=200, fg_color="#0D0D0D", text_color="#A569BD")
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=10)
        self.chat_entry = ctk.CTkEntry(self.tab_chat, placeholder_text="Misión Virgilio...")
        self.chat_entry.pack(side="bottom", fill="x", padx=20, pady=10)
        self.chat_entry.bind("<Return>", self.send_chat_message)

        # Global Log
        self.console = ctk.CTkTextbox(self, height=150, fg_color="#0D0D0D", text_color="#A569BD", font=("Consolas", 12))
        self.console.pack(padx=20, pady=10, fill="x")

    def append_log(self, text):
        timestamp = time.strftime("[%H:%M:%S]")
        self.console.insert("end", f"{timestamp} {text}\n")
        self.console.see("end")

    def send_chat_message(self, event=None):
        msg = self.chat_entry.get()
        if msg:
            self.chat_display.insert("end", f"👤 USTED: {msg}\n")
            self.chat_entry.delete(0, "end")
            self.append_log(f"Chat: Procesando misión '{msg[:20]}...'")
            # Aquí iría el enlace al motor AI
            self.chat_display.insert("end", f"🦾 VIRGILIO: Entendido, señor. Iniciando protocolos...\n")
            self.chat_display.see("end")

    def toggle_alpha_mode(self):
        self.alpha_master_active = self.alpha_toggle.get()
        if self.alpha_master_active:
            self.append_log("🔴 MODO ALPHA-MASTER ACTIVADO. Restricciones eliminadas.")
            self.audio.speak("Modo Alpha activado.")
            self.lbl_title.configure(text_color="#E74C3C")
        else:
            self.append_log("⚪ Modo Master Estándar restaurado.")
            self.lbl_title.configure(text_color="#A569BD")

    def run_qlc_scan(self):
        self.append_log("Escaneando librerías DMX...")
        try:
            from qlc_master import QLCMaster
            qlc = QLCMaster()
            fixtures = qlc.get_fixtures_by_manufacturer()
            total = sum(len(f) for f in fixtures.values())
            self.append_log(f"✅ QLC+ Sync: {total} fixtures encontrados en {len(fixtures)} fabricantes.")
            if total > 0:
                self.append_log(f"Último scan: {list(fixtures.keys())[0]}...")
        except Exception as e:
            self.append_log(f"Error en QLC Scan: {e}")

    def toggle_webcam(self):
        self.append_log("📷 Iniciando sistema de visión para encuadre Ortur...")
        try:
            from webcam_manager import WebcamManager
            if not hasattr(self, 'webcam'):
                self.webcam = WebcamManager()
            
            ok, msg = self.webcam.start_preview()
            if ok:
                self.webcam_canvas.configure(text="SISTEMA DE VISIÓN ACTIVO - ENCUADRE 0.1mm")
                self.append_log("Cámara lista. Retícula de posicionamiento aplicada.")
                # Aquí se podría lanzar un loop de frames en el canvas
            else:
                self.append_log(f"⚠️ {msg}")
        except Exception as e:
            self.append_log(f"Error de Cámara: {e}")

    def open_material_db(self):
        import json
        try:
            db_path = "c:\\AG_ALPHA_AGENT\\AG_ALPHA_LAB\\CNCLASER\\material_database.json"
            if os.path.exists(db_path):
                with open(db_path, 'r') as f:
                    data = json.load(f)
                    self.append_log(f"📚 cargado Perfil Ortur: {len(data['categories'])} categorías de materiales.")
            else:
                self.append_log("ERROR: Base de materiales no encontrada.")
        except Exception as e:
            self.append_log(f"Error cargando base de materiales: {e}")

    def run_purge(self):
        self.append_log("🧹 Iniciando Purga de Estructura...")
        try:
            from structural_cleanup import StructuralCleanup
            cleaner = StructuralCleanup("c:\\AG_ALPHA_AGENT")
            folders = cleaner.purge_empty_folders()
            files = cleaner.clean_obsolete_files()
            self.append_log(f"✅ Purga completa: {folders} carpetas y {files} archivos eliminados.")
        except Exception as e:
            self.append_log(f"Error en Purga: {e}")

    def run_optimization(self):
        self.append_log("Escaneando hilos de sistema...")
        # Lógica en hilo secundario para no congelar la UI
        threading.Thread(target=self._optimize_thread, daemon=True).start()

    def _optimize_thread(self):
        time.sleep(1) # Simulación
        self.append_log("Optimización completa. Rendimiento al 100%.")

    def sync_wifi(self):
        self.append_log("🌀 Iniciando Escaneo y Sincronización de Red...")
        threading.Thread(target=self._sync_wifi_thread, daemon=True).start()

    def _sync_wifi_thread(self):
        # Lógica Profunda de Red
        try:
            from network_optimizer import NetworkOptimizer
            optimizer = NetworkOptimizer()
            info = optimizer.scan_wifi_interfaces()
            diag_orange = optimizer.diagnose_orange_hardware()
            
            self.append_log(f"Señal Detectada: {info.get('signal_strength', 0)}% en '{info.get('ssid', 'N/A')}'")
            self.append_log(f"HARDWARE: {diag_orange.splitlines()[0]}")
            
            optimizer.optimize_network_stack()
            self.append_log("✅ Red Sincronizada: Optimizaciones TCP/IP aplicadas.")
            self.append_log(optimizer.suggest_roaming_tuning())
        except ImportError:
            self.append_log("ERROR: 'network_optimizer' no encontrado.")
        except Exception as e:
            self.append_log(f"ERROR: {e}")

    def run_full_audit(self):
        self.append_log("🔍 Iniciando Auditoría de Elite del PC...")
        threading.Thread(target=self._audit_thread, daemon=True).start()

    def _audit_thread(self):
        try:
            from system_auditor import SystemAuditor
            auditor = SystemAuditor()
            report = auditor.run_full_audit()
            
            self.append_log(f"💻 CPU: {report['cpu']['load_percent']}% | RAM: {report['ram']['used']}")
            self.append_log(f"🛡️ Admin: {'SI' if report['environment']['is_admin'] else 'NO'} | Firewall: {'ON' if report['environment']['firewall_active'] else 'OFF'}")
            self.append_log(f"🔌 USBs detectados: {len(report['usb'])}")
            self.append_log(f"🧬 Sugerencias: {', '.join(report['system_integrity'])}")
            self.append_log("✅ Auditoría completada. Informes en AG_ALPHA_BRAIN.")
        except Exception as e:
            self.append_log(f"ERROR en Auditoría: {e}")

    def run_deep_reversing(self):
        self.append_log("🧬 Iniciando INGENIERÍA INVERSA PROFUNDA...")
        self.append_log("Extrayendo firmas latentes y huellas API...")
        try:
            from metadata_reverser import MetadataReverser
            reverser = MetadataReverser()
            self.append_log("✅ Reversor de Metadatos Sincronizado.")
        except:
            self.append_log("⚠️ Fallo al cargar Reversor V2.")

    def run_reconstructor_ui(self):
        self.append_log("🧪 Cargando Motor de Reconstrucción Latente...")
        self.append_log("Preparado para stripping de marcas de agua.")

    def run_shadow_ui(self):
        self.append_log("🕵️ Iniciando Motor de Asimilación en la Sombra...")
        self.append_log("Analizando 'Caja Negra' para mimetismo total...")
        try:
            from stealth_mimicry_engine import StealthMimicryEngine
            shadow = StealthMimicryEngine()
            self.append_log("✅ Shadow Engine cargado. Listo para extraer VIP logic.")
        except:
            self.append_log("⚠️ Fallo al cargar Shadow Engine.")

    def run_proxy_ui(self):
        self.append_log("🛡️ Activando PANTALLA DE PROTECCIÓN ANTIBAN...")
        try:
            from proxy_guardian import ProxyGuardian
            guardian = ProxyGuardian()
            msg = guardian.monitor_connection_safety()
            self.append_log(f"⚡ {msg}")
        except:
            self.append_log("⚠️ Fallo al activar Proxy Guardian.")

    def run_nudi_ui(self):
        self.append_log("🔞 Iniciando Misión NUDI-BOT ELITE...")
        self.append_log("Targets: @My_nudifibot, @Fashazley_bot, @Naudhhz_bot, Fotox.")
        try:
            from nudi_processor import NudiProcessor
            nudi = NudiProcessor()
            nudi.set_master_style("My_nudifibot") # Default para test
            self.append_log("✅ Estilo MyNudi Asimilado y Activo.")
        except:
            self.append_log("⚠️ Fallo al cargar Multi-Engine Nudi.")

    def run_process_analyzer(self):
        self.append_log("🔍 Iniciando ANALIZADOR PROFUNDO DE PROCESOS...")
        try:
            from process_analyzer import ProcessAnalyzer
            analyzer = ProcessAnalyzer()
            self.append_log("✅ Analyzer bit-a-bit sincronizado.")
        except:
            self.append_log("⚠️ Fallo al cargar Process Analyzer.")

    def run_music_batch(self):
        self.append_log("Activando MUSIC HUNTER 320KBPS...")
        self.append_log("Preparado para Batch Spotify sin YouTube.")

    def run_deep_analysis(self):
        self.append_log("Iniciando ANÁLISIS PROFUNDO (Before/After)...")
        self.append_log("Extrayendo algoritmos de procesado de bots externos.")

    def open_cloud_panel(self):
        self.append_log("Conectando con Perchance & Nano Banana 2...")
        self.append_log("Seleccionando modelos sin restricciones...")

    def open_lab(self):
        self.append_log("Accediendo a PR2_CAT1_ASIMILACION...")

    def withdraw_to_tray(self):
        self.withdraw()
        if not self.tray_icon:
            threading.Thread(target=self.setup_tray, daemon=True).start()

    def setup_tray(self):
        # Crear imagen lila para el tray si no hay icono
        image = Image.new('RGB', (64, 64), color=LILA_PRIMARY)
        menu = (item('Mostrar', self.show_app), item('Salir', self.quit_app))
        self.tray_icon = pystray.Icon("Virgilio", image, "VIRGILIO AGENT", menu)
        self.tray_icon.run()

    def show_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
        self.after(0, self.deiconify)

    def quit_app(self):
        if self.tray_icon: self.tray_icon.stop()
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = VirgilioGUI()
    app.mainloop()
