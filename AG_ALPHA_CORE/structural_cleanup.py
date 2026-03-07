import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VIRGILIO_PURGE")

class StructuralCleanup:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def purge_empty_folders(self):
        """Borra carpetas vacías de forma recursiva."""
        purged_count = 0
        for root, dirs, files in os.walk(self.root_dir, topdown=False):
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                try:
                    if not os.listdir(folder_path):
                        os.rmdir(folder_path)
                        purged_count += 1
                        logger.info(f"Purga: {folder_path} eliminada (Vacía)")
                except Exception as e:
                    logger.error(f"Error purgando {folder_path}: {e}")
        return purged_count

    def clean_obsolete_files(self):
        """Elimina archivos temporales conocidos o inútiles."""
        obsolete_patterns = [".tmp", "desktop.ini", "Thumbs.db"]
        removed_count = 0
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                if any(file.endswith(p) or file.lower() == p.lower() for p in obsolete_patterns):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    removed_count += 1
                    logger.info(f"Purga: {file_path} eliminado")
        return removed_count

    def auto_clean(self):
        """Ejecución automatizada para el orquestador."""
        f = self.purge_empty_folders()
        a = self.clean_obsolete_files()
        logger.info(f"Sincronización de limpieza: {f} carpetas, {a} archivos.")
