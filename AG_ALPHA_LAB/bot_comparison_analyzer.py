import cv2
import numpy as np
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VIRGILIO_COMPARISON")

class BotComparisonAnalyzer:
    def __init__(self):
        self.output_dir = r"c:\AG_ALPHA_AGENT\AG_ALPHA_LAB\COMPARISON_ANALYSIS"
        os.makedirs(self.output_dir, exist_ok=True)

    def analyze_transformation(self, before_path, after_path, bot_identifier):
        """
        Analiza el cambio entre dos imágenes para deducir las funciones del bot.
        Especialmente útil para bots de edición o transformación de imagen.
        """
        img_before = cv2.imread(before_path)
        img_after = cv2.imread(after_path)

        if img_before is None or img_after is None:
            return "Error: Imágenes no encontradas."

        # Redimensionar si es necesario
        if img_before.shape != img_after.shape:
            img_after = cv2.resize(img_after, (img_before.shape[1], img_before.shape[0]))

        # Calcular diferencia absoluta y máscaras de cambio
        diff = cv2.absdiff(img_before, img_after)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        
        # Analizar áreas de mayor cambio (máscara de procesamiento)
        _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
        
        # Análisis de frecuencia para detectar "sharpening" o suavizado
        f_before = np.fft.fft2(cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY))
        f_after = np.fft.fft2(cv2.cvtColor(img_after, cv2.COLOR_BGR2GRAY))
        
        freq_diff = np.mean(np.abs(f_after)) / np.mean(np.abs(f_before))

        analysis_report = {
            "bot": bot_identifier,
            "change_magnitude": float(np.mean(gray_diff)),
            "frequency_shift": float(freq_diff),
            "detected_actions": self._deduce_actions(freq_diff, gray_diff),
            "timestamp": os.path.getmtime(after_path)
        }

        report_file = os.path.join(self.output_dir, f"analysis_{bot_identifier}_{int(analysis_report['timestamp'])}.json")
        with open(report_file, 'w') as f:
            json.dump(analysis_report, f, indent=4)

        logger.info(f"Análisis de transformación completado para {bot_identifier}")
        return analysis_report

    def _deduce_actions(self, freq_shift, diff_mask):
        actions = []
        if freq_shift > 1.1: actions.append("High-Freq Enhacing (Sharpening)")
        if freq_shift < 0.9: actions.append("Texture Smoothing (Denoising)")
        if np.mean(diff_mask) > 50: actions.append("Significant Geometry Alteration")
        return actions

if __name__ == "__main__":
    analyzer = BotComparisonAnalyzer()
    print("Analizador de Comparación Bot Activo.")
