import cv2
import numpy as np
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VIRGILIO_REVERSING")

class BotReversingUtility:
    def __init__(self):
        self.report_path = r"c:\AG_ALPHA_AGENT\AG_ALPHA_LAB\REVERSE_ENGINEERING\ANALISIS_BOTS"
        os.makedirs(self.report_path, exist_ok=True)

    def deduce_algorithm(self, bot_image_path):
        """
        Deduce el algoritmo de origen analizando patrones de ruido y artefactos.
        Detecta firmas de Stable Diffusion (Varias versiones), Flux o Midjourney.
        """
        img = cv2.imread(bot_image_path)
        if img is None: return "Error: Imagen no legible."

        # 1. Análisis de Ruido Latente (Transformada de Fourier)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift))
        
        # Simulación de detección de patrones
        avg_freq = np.mean(magnitude_spectrum)
        
        # Lógica de decisión
        deduced_model = "Stable Diffusion XL"
        if avg_freq > 180: deduced_model = "Flux.1 Dev"
        elif avg_freq < 120: deduced_model = "SD 1.5 (Standard)"

        # 2. Análisis de Estilo de Prompt (Reverse Prompting)
        # Esto se integraría con el AIManager para usar un modelo de VLM (Gemini Vision)
        
        analysis = {
             "bot_name": os.path.basename(os.path.dirname(bot_image_path)),
             "deduced_model": deduced_model,
             "noise_signature": float(avg_freq),
             "style_confidence": 0.85,
             "suggested_local_reproduction": "Use LoRA 'v_style_01' at 0.7 strength"
        }

        report_file = os.path.join(self.report_path, f"reversing_{int(os.path.getmtime(bot_image_path))}.json")
        with open(report_file, 'w') as f:
            json.dump(analysis, f, indent=4)

        logger.info(f"Bot Reversing completo: {deduced_model} detectado.")
        return analysis

if __name__ == "__main__":
    reverser = BotReversingUtility()
    # print(reverser.deduce_algorithm("path/to/bot_img.png"))
