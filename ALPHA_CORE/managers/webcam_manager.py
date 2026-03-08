import cv2
import logging

class WebcamManager:
    """Gestiona la cámara para previsualización de posicionamiento CNC/Laser."""
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None

    def start_preview(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            return False, "No se pudo abrir la cámara (Webcam)."
        return True, "Cámara iniciada."

    def get_frame(self, draw_grid=True):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                if draw_grid:
                    # Dibujar retícula de posicionamiento
                    h, w, _ = frame.shape
                    cv2.line(frame, (w//2, 0), (w//2, h), (0, 255, 0), 1)
                    cv2.line(frame, (0, h//2), (w, h//2), (0, 255, 0), 1)
                return frame
        return None

    def stop_preview(self):
        if self.cap:
            self.cap.release()
            self.cap = None
if __name__ == "__main__":
    wm = WebcamManager()
    ok, msg = wm.start_preview()
    print(msg)
    if ok: wm.stop_preview()
