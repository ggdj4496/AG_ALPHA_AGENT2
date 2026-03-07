import cv2
import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="../AG_ALPHA_BRAIN/.env")

class ImageProcessor:
    def __init__(self):
        self.output_path = r"c:\AG_ALPHA_AGENT\AG_ALPHA_LAB\CNCLASER"
        os.makedirs(self.output_path, exist_ok=True)
        print("Procesador Vision CNC Activo.")

    def generate_image_perchance(self, prompt, project_folder):
        """Generador Perchance con guardado automatico en proyecto."""
        print(f"Generando en Perchance: {prompt}")
        # Simulacion de conexion a Perchance
        return os.path.join(project_folder, "perchance_gen.png")

    def generate_image_nano(self, prompt, project_folder):
        """Generador Nano Banana 2."""
        print(f"Generando en Nano Banana 2: {prompt}")
        return os.path.join(project_folder, "nano_gen.png")

    def analyze_for_cnc(self, image_path):
        """Escala de grises y deteccion de bordes para Laser CNC."""
        if not os.path.exists(image_path): return "Path invalido."
        
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        base_name = os.path.basename(image_path)
        save_path = os.path.join(self.output_path, f"cnc_{base_name}")
        cv2.imwrite(save_path, edges)
        
        return f"Archivo para CNC generado: {save_path}"

if __name__ == "__main__":
    processor = ImageProcessor()
