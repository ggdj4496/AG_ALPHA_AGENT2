import os
import sys
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

# Sincronización Profesional de Rutas
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ALPHA_CORE.core_orchestrator import CoreOrchestrator

logger = logging.getLogger("VIRGILIO_PILOT_HANDLERS")

class PilotHandlers:
    """
    Gestor de Comandos para el Bridge de Telegram.
    Aísla la lógica de interacción de la infraestructura del bot.
    """
    def __init__(self):
        self.core = CoreOrchestrator()
        self.core.boot_all()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton("/status"), KeyboardButton("/auditoria")],
            [KeyboardButton("/sincro_wifi"), KeyboardButton("/help")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🦾 <b>VIRGILIO PILOT V7.0 ENGINEERED</b>\nPuente de comando activo. Sistemas de ingeniería listos.",
            reply_markup=reply_markup, parse_mode='HTML'
        )

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        statuses = self.core.get_full_status()
        msg = "🩺 <b>ESTADO DEL SISTEMA</b>\n"
        for name, data in statuses.items():
            msg += f"• <b>{name.upper()}</b>: {'✅' if data.get('active', True) else '❌'}\n"
        await update.message.reply_text(msg, parse_mode='HTML')

    async def auditoria(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg_wait = await update.message.reply_text("🔍 Iniciando Auditoría Forense de Hardware...")
        auditor = self.core.get_manager("auditor")
        report = auditor.run_full_audit()
        msg = (f"✅ <b>AUDITORÍA COMPLETADA</b>\n"
               f"• CPU: <code>{report['cpu']['load_percent']}%</code>\n"
               f"• RAM: <code>{report['ram']['used']}</code>\n"
               f"• Admin: <b>{'SI' if report['environment']['is_admin'] else 'NO'}</b>")
        await update.message.edit_text(msg, parse_mode='HTML')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        ai = self.core.get_manager("ai")
        # El agente ahora es capaz de elegir herramientas (lógica interna)
        response = await ai.ask(text)
        await update.message.reply_text(response)
