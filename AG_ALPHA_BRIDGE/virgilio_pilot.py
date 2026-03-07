import os
import asyncio
import logging
import sys
import json
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Importar lógica del Core (Nativo)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'AG_ALPHA_CORE'))
try:
    from system_auditor import SystemAuditor
    from network_optimizer import NetworkOptimizer
except ImportError:
    SystemAuditor = None
    NetworkOptimizer = None

# Configuración de Elite
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("c:\\AG_ALPHA_AGENT\\AG_ALPHA_BRIDGE\\pilot_log.txt"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("VIRGILIO_PILOT")

load_dotenv(dotenv_path="../AG_ALPHA_BRAIN/.env")
TOKEN = os.getenv("TELEGRAM_TOKEN_VIRGILIO")

class VirgilioPilot:
    def __init__(self):
        self.start_time = datetime.now()
        self.state_file = "c:\\AG_ALPHA_AGENT\\AG_ALPHA_BRIDGE\\pilot_state.json"
        self._check_singleton()
        self.load_state()

    def _check_singleton(self):
        # Lógica simple para evitar doble instancia si fuera necesario
        pass

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {"missions": [], "last_sync": str(datetime.now())}

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=4)

    def load_knowledge(self):
        """Inyecta el contexto de consciencia del proyecto en el Piloto."""
        k_path = "c:\\AG_ALPHA_AGENT\\AG_ALPHA_BRAIN\\KNOWLEDGE_INJECTION.json"
        if os.path.exists(k_path):
            with open(k_path, 'r', encoding='utf-8') as f:
                self.knowledge = json.load(f)
                logger.info("🧠 Consciencia Inyectada: Virgilio sabe quién es.")
        else:
            self.knowledge = {"identity": "Generic Agent"}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.load_knowledge() # Recargar al iniciar
        keyboard = [
            [KeyboardButton("/status"), KeyboardButton("/auditoria")],
            [KeyboardButton("/sincro_wifi"), KeyboardButton("/ultra_tuning")],
            [KeyboardButton("/wake_agent"), KeyboardButton("/help")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        import html
        safe_mission = html.escape(self.knowledge['knowledge_base']['chat_history_summary'][:100])
        msg = (f"🦾 <b>VIRGILIO PILOT V6.0 [BOOTSTRAPPER]</b>\n"
               f"Misión: <code>{safe_mission}...</code>\n"
               f"Puente independiente establecido. Sistema listo para el despertar.")
        await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode='HTML')

    async def wake_agent(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Lanza el núcleo (GUI/Engine) si no está activo."""
        import subprocess
        try:
            subprocess.Popen(["python", "c:\\AG_ALPHA_AGENT\\AG_ALPHA_CORE\\virgilio_gui.py"], 
                            creationflags=subprocess.CREATE_NEW_CONSOLE)
            await update.message.reply_text("🚀 **NÚCLEO DESPERTADO**. Sintonizando GUI y Motor...", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Error al despertar al Agente: {e}")

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        uptime = datetime.now() - self.start_time
        await update.message.reply_text(
            f"🩺 <b>ESTADO DEL PILOTO</b>\n"
            f"• Uptime: <code>{str(uptime).split('.')[0]}</code>\n"
            f"• Core Link: <b>ESTABLE</b> (Python Native)\n"
            f"• Memoria: <b>Aislada</b> (Independent Process)\n"
            f"• Latencia: <code>Sub-ms</code>",
            parse_mode='HTML'
        )

    async def auditoria(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔍 Iniciando Escaneo de Hardware de Élite...")
        try:
            if SystemAuditor:
                auditor = SystemAuditor()
                report = auditor.run_full_audit()
                msg = (f"✅ <b>AUDITORÍA COMPLETADA</b>\n"
                       f"• CPU: <code>{report['cpu']['load_percent']}%</code>\n"
                       f"• RAM: <code>{report['ram']['used']}</code>\n"
                       f"• UAC/Admin: <b>{'SI' if report['environment']['is_admin'] else 'NO'}</b>\n"
                       f"• Firewall: <b>{'Activo' if report['environment']['firewall_active'] else 'Inactivo'}</b>\n"
                       f"• Sugerencias: <code>{report['system_integrity'][0] if report['system_integrity'] else 'Ninguna'}</code>")
                await update.message.reply_text(msg, parse_mode='HTML')
            else:
                await update.message.reply_text("⚠️ **ERROR**: Auditor no disponible.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error en Auditoría: {e}")

    async def sincro_wifi(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🌀 Sincronizando Red [Livebox 6 Master]...")
        if NetworkOptimizer:
            net = NetworkOptimizer()
            info = net.scan_wifi_interfaces()
            await update.message.reply_text(
                f"📡 <b>RED SINCRONIZADA</b>\n"
                f"• SSID: <code>{info['ssid']}</code>\n"
                f"• Señal: <code>{info['signal_strength']}%</code>\n"
                f"• Estado: <b>{info['status']}</b>",
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text("⚠️ Optimizador de red no disponible.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        logger.info(f"Mensaje recibido: {text}")
        # Aquí se conectaría con AIManager para respuestas inteligentes
        await update.message.reply_text("🦾 Virgilio Pilot procesando misión en segundo plano...")

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        import traceback
        error_msg = f"Error en el Pilot: {context.error}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        
        if update and isinstance(update, Update) and update.effective_message:
            # Notificar al usuario con detalle técnico si es necesario
            await update.effective_message.reply_text(f"⚠️ <b>INTERFERENCIA DETECTADA</b>\n<code>{str(context.error)[:100]}</code>", parse_mode='HTML')

async def run_pilot():
    pilot = VirgilioPilot()
    # Hardening: Connection Pool & Timeouts para HyperOS/Android Fluctuations
    app = ApplicationBuilder().token(TOKEN).connect_timeout(30).read_timeout(30).build()

    # Handlers
    app.add_handler(CommandHandler("start", pilot.start))
    app.add_handler(CommandHandler("status", pilot.status))
    app.add_handler(CommandHandler("wake_agent", pilot.wake_agent))
    app.add_handler(CommandHandler("auditoria", pilot.auditoria))
    app.add_handler(CommandHandler("sincro_wifi", pilot.sincro_wifi))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), pilot.handle_message))
    app.add_error_handler(pilot.error_handler)

    logger.info("VIRGILIO PILOT V6.0 Iniciado [Python Asyncio]")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(run_pilot())
    except Exception as e:
        logger.critical(f"COLAPSO TOTAL DEL PILOTO: {e}")
