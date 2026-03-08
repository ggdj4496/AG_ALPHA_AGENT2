import requests
import json
import os
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VIRGILIO_REVERSER")

class MetadataReverser:
    """
    Analiza la 'huella' de las APIs y metadatos de los bots.
    Permite descubrir cómo fragmentan las peticiones y qué modelos reales usan por debajo.
    """
    def __init__(self):
        self.brain_path = r"c:\AG_ALPHA_AGENT\AG_ALPHA_BRAIN\REVERSE_ENGINEERING"
        os.makedirs(self.brain_path, exist_ok=True)

    def analyze_api_footprint(self, raw_response_sample):
        """
        Extrae patrones de cabeceras y JSON para identificar el motor real (Censored/Uncensored).
        """
        logger.info("Analizando huella digital de la API...")
        
        # Buscar indicadores de modelos base (e.g., GPT, Stable Diffusion versions)
        found_models = re.findall(r"(gpt-[34][\w\-]*|sd-[\d\.]+|stable-diffusion-[\w\-]+)", raw_response_sample)
        
        # Buscar indicadores de filtros de censura
        censorship_indicators = ["refuse", "policy", "restrict", "violation", "safety"]
        detected_filters = [f for f in censorship_indicators if f in raw_response_sample.lower()]
        
        report = {
            "engines_detected": list(set(found_models)),
            "censorship_risk": len(detected_filters) / len(censorship_indicators) if detected_filters else 0,
            "bypass_suggestion": "Injection via base64 encoding or prompt wrapping." if detected_filters else "Standard access."
        }
        
        return report

    def extract_hidden_parameters(self, js_sample):
        """
        Analiza código JS (por ejemplo de Perchance) para sacar los pesos de los modelos.
        """
        # Buscar arrays de pesos o configuraciones de 'sampler'
        samplers = re.findall(r"sampler_name:\s*['\"]([\w]+)['\"]", js_sample)
        cfg_scales = re.findall(r"cfg_scale:\s*([\d\.]+)", js_sample)
        
        return {
            "samplers": list(set(samplers)),
            "typical_cfg": cfg_scales if cfg_scales else ["7.5"]
        }

if __name__ == "__main__":
    reverser = MetadataReverser()
    print("Reversor de Metadatos y Huella API Activo.")
