import os
import asyncio
import logging
import sys
from typing import Optional
from dotenv import load_dotenv

# Sincronización de Ecosistema V8.0 GOLD
root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)
sys.path.append(os.path.join(root_path, "ALPHA_CORE"))

env_path = os.path.join(root_path, "ALPHA_CORE", "config", ".env")
load_dotenv(dotenv_path=env_path)

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from pilot_handlers import PilotHandlers

# Configuración Profesional de Tráfico
logging.basicConfig(
    format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("VIRGILIO_BRIDGE_GOLD")

class VirgilioPilotMain:
    """
    Orquestador del Bridge de Comunicación V8.0 GOLD.
    Implementa resiliencia y conexión directa con el CORE.
    """
    def __init__(self):
        self.token: Optional[str] = os.getenv("TELEGRAM_TOKEN_VIRGILIO")
        self.handlers = PilotHandlers()
        self.version = "V8.0 GOLD"

    async def run(self) -> None:
        """Ciclo de vida del Bridge con gestión de reconexión."""
        if not self.token:
            logger.error("❌ TELEGRAM_TOKEN_VIRGILIO no configurado en ALPHA_CORE/.env")
            return

        logger.info(f"🚀 Iniciando VIRGILIO BRIDGE {self.version}...")
        
        while True:
            try:
                app = ApplicationBuilder().token(self.token).build()

                # Registro de Handlers de Misión
                app.add_handler(CommandHandler("start", self.handlers.start))
                app.add_handler(CommandHandler("status", self.handlers.status))
                app.add_handler(CommandHandler("auditoria", self.handlers.auditoria))
                app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handlers.handle_message))

                logger.info("✅ Bridge Pilot operativo en la red de Telegram.")
                await app.run_polling(drop_pending_updates=True)
                
            except Exception as e:
                logger.error(f"⚠️ Caída del Bridge Detectada: {e}. Reintentando en 10s...")
                await asyncio.sleep(10)

if __name__ == "__main__":
    pilot = VirgilioPilotMain()
    try:
        asyncio.run(pilot.run())
    except KeyboardInterrupt:
        logger.info("🛑 Apagado controlado por el usuario.")
    except Exception as e:
        logger.critical(f"🔥 COLAPSO CRÍTICO DEL BRIDGE: {e}")
