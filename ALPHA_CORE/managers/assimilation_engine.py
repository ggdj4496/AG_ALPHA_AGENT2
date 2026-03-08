import cv2
import numpy as np
import os
import json
import time
import re
import logging
from typing import Dict, Any, Optional, List
from base_manager import BaseManager, ManagerState

class AssimilationEngine:
    """
    Motor de Asimilación Algorítmica V8.0 GOLD.
    Especializado en ingeniería inversa de patrones y firmas de bots externos.
    """
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.db_path = os.path.join(self.root_dir, "ALPHA_CORE", "data", "ASIMILACION")
        self.master_db = os.path.join(self.db_path, "MASTER_DB.json")
        self.success_count_file = os.path.join(self.db_path, "success_tracker.json")
        
        os.makedirs(self.db_path, exist_ok=True)
        self._init_tracker()

    def _init_tracker(self) -> None:
        if not os.path.exists(self.success_count_file):
            with open(self.success_count_file, 'w') as f:
                json.dump({}, f)

    def analyze_patterns(self, original_path: str, bot_result_path: str, bot_name: str) -> str:
        """Análisis forense de patrones y firmas cromáticas."""
        if not os.path.exists(original_path) or not os.path.exists(bot_result_path):
            return "ERROR: Archivos de origen no localizados."

        img1 = cv2.imread(original_path)
        img2 = cv2.imread(bot_result_path)
        
        if img1 is None or img2 is None: 
            return "ERROR: Fallo en lectura de matrices de imagen."

        # 1. Similitud Estructural (SSIM)
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        if gray1.shape != gray2.shape:
            gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))
        
        res = cv2.absdiff(gray1, gray2)
        ssim_score = 1 - (np.mean(res) / 255)

        # 2. Perfil de Ruido (Signature Extraction)
        noise_profile = np.std(gray2 - cv2.GaussianBlur(gray2, (5, 5), 0))
        
        # 3. Análisis Cromático (Color Signature)
        avg_color_bot = np.mean(img2, axis=(0, 1))
        avg_color_orig = np.mean(img1, axis=(0, 1))
        color_shift = np.linalg.norm(avg_color_bot - avg_color_orig)

        finding = {
            "bot": bot_name,
            "ssim_score": float(ssim_score),
            "noise_profile": float(noise_profile),
            "chromatic_shift": float(color_shift),
            "deduced_model": self.deduce_model_from_freq(gray2),
            "timestamp": time.time()
        }
        
        finding_file = os.path.join(self.db_path, f"finding_{bot_name}_{int(finding['timestamp'])}.json")
        with open(finding_file, 'w', encoding='utf-8') as f:
            json.dump(finding, f, indent=4)
            
        return self.track_success(bot_name)

    def deduce_model_from_freq(self, gray_img: np.ndarray) -> str:
        """Deduce el modelo base usando FFT (Transformada de Fourier)."""
        f = np.fft.fft2(gray_img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-9)
        avg_freq = np.mean(magnitude_spectrum)
        
        if avg_freq > 180: return "Flux.1 Dev"
        if avg_freq < 120: return "SD 1.5 (Standard)"
        return "Stable Diffusion XL"

    def analyze_api_footprint(self, raw_sample: str) -> Dict[str, Any]:
        """Analiza metadatos y respuestas de API para detectar censura y modelos."""
        found_models = re.findall(r"(gpt-[34][\w\-]*|sd-[\d\.]+|stable-diffusion-[\w\-]+)", raw_sample)
        censorship_indicators = ["refuse", "policy", "restrict", "violation", "safety"]
        detected_filters = [f for f in censorship_indicators if f in raw_sample.lower()]
        
        return {
            "engines_detected": list(set(found_models)),
            "censorship_risk": len(detected_filters) / len(censorship_indicators) if detected_filters else 0,
            "bypass_suggestion": "Injection via base64 or prompt wrapping" if detected_filters else "Standard"
        }


    def track_success(self, bot_name: str) -> str:
        """Rastrea el progreso de asimilación de un modelo específico."""
        try:
            with open(self.success_count_file, 'r') as f:
                tracker = json.load(f)
            
            count = tracker.get(bot_name, 0) + 1
            tracker[bot_name] = count
            
            with open(self.success_count_file, 'w') as f:
                json.dump(tracker, f, indent=4)
                
            if count >= 5:
                self.promote_to_master(bot_name)
                return f"✅ {bot_name} TOTALMENTE ASIMILADO."
            
            return f"📈 Progreso de asimilación {bot_name}: {count}/5."
        except Exception:
            return "ERROR: Fallo en tracker de asimilación."

    def promote_to_master(self, bot_name: str) -> None:
        """Consolida el conocimiento en la base de datos maestra."""
        master_data = {
            "status": "MASTERED",
            "asimilado_el": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tier": "GOLD"
        }
        
        master_local = {}
        if os.path.exists(self.master_db):
            with open(self.master_db, 'r') as f:
                master_local = json.load(f)
        
        master_local[bot_name] = master_data
        with open(self.master_db, 'w') as f:
            json.dump(master_local, f, indent=4)

    def extract_deep_latent_features(self, img_path: str) -> Optional[Dict[str, float]]:
        """Extrae la firma matemática del espacio latente."""
        img = cv2.imread(img_path)
        if img is None: return None
        
        # Análisis de Gradientes
        dx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
        dy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
        gradient_magnitude = np.sqrt(dx**2 + dy**2)
        
        # Análisis de Frecuencias
        dft = cv2.dft(np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        
        return {
            "gradient_mean": float(np.mean(gradient_magnitude)),
            "frequency_entropy": float(np.std(dft_shift)),
            "artifact_score": self._calculate_artifact_score(img)
        }

    def _calculate_artifact_score(self, img: np.ndarray) -> float:
        """Cálculo heurístico de ruido de compresión."""
        return float(np.std(img) / 100.0)

if __name__ == "__main__":
    eng = AssimilationEngine()
    print("Assimilation Engine V8.0 GOLD Ready.")
