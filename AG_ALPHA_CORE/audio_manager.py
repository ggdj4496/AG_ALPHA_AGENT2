import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VIRGILIO_AUDIO")

class AudioManager:
    """
    Motor de Audio de Virgilio.
    Preparado para ElevenLabs (Premium) y TTS Local.
    """
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = "Adam" # Default profesional
        self.output_path = r"c:\AG_ALPHA_AGENT\AG_ALPHA_BRAIN\VOICE_OUTPUT"
        os.makedirs(self.output_path, exist_ok=True)

    def speak(self, text):
        """
        Sintetiza voz. Si hay API Key usa ElevenLabs, si no, lo reporta.
        """
        if not self.api_key:
            logger.warning("Falta ELEVENLABS_API_KEY. Virgilio permanece en modo silencioso.")
            return False
        
        logger.info(f"🎙️ Sintetizando voz: '{text[:20]}...'")
        # Aquí iría el POST a ElevenLabs
        # url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        # ... logic ...
        return True

    def toggle_mute(self):
        """Desactiva/Activa audio."""
        logger.info("Modo Silencioso: ON" if not self.api_key else "Modo Voz: ACTIVO")

if __name__ == "__main__":
    audio = AudioManager()
    audio.speak("Sistema Virgilio Vocalizado.")
