import xml.etree.ElementTree as ET
import os

class QLCMaster:
    """Motor de gestión de Fixtures y Workspaces de QLC+."""
    def __init__(self, qlc_user_path=None):
        # Default Windows path for QLC+ user data
        self.qlc_user_path = qlc_user_path or os.path.join(os.environ['USERPROFILE'], 'QLC+')

    def get_fixtures_by_manufacturer(self):
        """Escanea y organiza fixtures por fabricante."""
        fixture_path = os.path.join(self.qlc_user_path, 'Fixtures')
        if not os.path.exists(fixture_path):
            return {}
        
        fixtures = {}
        for root, dirs, files in os.walk(fixture_path):
            manufacturer = os.path.basename(root)
            if manufacturer == "Fixtures": continue
            fixtures[manufacturer] = [f for f in files if f.endswith(".qxf")]
        return fixtures

    def get_fixture_map_summary(self):
        """Lee el FixturesMap.xml para obtener un índice rápido."""
        map_path = os.path.join(self.qlc_user_path, 'Fixtures', 'FixturesMap.xml')
        if not os.path.exists(map_path):
            return "FixturesMap.xml no encontrado."
        
        tree = ET.parse(map_path)
        return f"Índice de {len(tree.getroot())} fixtures detectado."

    def import_gobo_image(self, source_path):
        """Importa una imagen de Gobo real a la carpeta de recursos de QLC+."""
        gobo_dir = os.path.join(self.qlc_user_path, 'Gobos')
        if not os.path.exists(gobo_dir): os.makedirs(gobo_dir)
        
        import shutil
        dest = os.path.join(gobo_dir, os.path.basename(source_path))
        shutil.copy2(source_path, dest)
        return f"Gobo importado: {dest}"
