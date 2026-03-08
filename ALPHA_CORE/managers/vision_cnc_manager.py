import cv2
import os
from base_manager import BaseManager, ManagerState

class VisionCNCManager(BaseManager):
    """
    Manager de Visión para CNC Láser V8.0.
    Especializado en detección de bordes y optimización de grabado.
    """
    def __init__(self):
        super().__init__("Vision_CNC")
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.output_path = os.path.join(self.root_dir, "ALPHA_CORE", "data", "CNC_OUTPUT")
        os.makedirs(self.output_path, exist_ok=True)

    def start(self) -> None:
        self.state = ManagerState.ACTIVE
        self.log_info("Procesador Vision CNC Activo.")

    def stop(self) -> None:
        self.state = ManagerState.INACTIVE

    def process_for_laser(self, image_path: str) -> str:
        """Aplica Canny y escala de grises para preparación de láser."""
        if not os.path.exists(image_path): return "ERROR: Path inválido."
        
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Filtro de bordes optimizado
        edges = cv2.Canny(gray, 100, 200)
        
        base_name = os.path.basename(image_path)
        save_path = os.path.join(self.output_path, f"laser_{base_name}")
        cv2.imwrite(save_path, edges)
        
        return save_path
