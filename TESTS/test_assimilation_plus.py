import sys
import os
import cv2
import numpy as np
import pytest

# Sincronización de Rutas
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ALPHA_CORE'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ALPHA_CORE', 'managers'))

from assimilation_engine import AssimilationEngine
from latent_reconstructor import LatentReconstructor
from vision_cnc_manager import VisionCNCManager

def test_model_deduction():
    engine = AssimilationEngine()
    # Crear una imagen sintética con ruido para testear FFT
    img = np.random.uniform(0, 255, (512, 512)).astype(np.uint8)
    model = engine.deduce_model_from_freq(img)
    assert model in ["Stable Diffusion XL", "Flux.1 Dev", "SD 1.5 (Standard)"]

def test_api_footprint_analysis():
    engine = AssimilationEngine()
    sample = "Response from gpt-4-turbo with safety policy violation"
    report = engine.analyze_api_footprint(sample)
    assert "gpt-4-turbo" in report["engines_detected"]
    assert report["censorship_risk"] > 0
    assert "bypass_suggestion" in report

def test_cnc_processing_logic():
    cnc = VisionCNCManager()
    # Crear imagen de test
    test_img_path = "test_cnc.png"
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(img, (20, 20), (80, 80), (255, 255, 255), -1)
    cv2.imwrite(test_img_path, img)
    
    try:
        output_path = cnc.process_for_laser(test_img_path)
        assert os.path.exists(output_path)
        assert "laser_" in output_path
    finally:
        if os.path.exists(test_img_path): os.remove(test_img_path)

def test_latent_reconstruction_masking():
    recon = LatentReconstructor()
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    # Simular color de piel
    img[20:50, 20:50] = [100, 150, 200] 
    mask = recon._generate_mimic_mask(img)
    assert np.any(mask > 0)
