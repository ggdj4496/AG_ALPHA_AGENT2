import os
import subprocess
import logging

class GitHubManager:
    """Gestiona clones, pulls y análisis de repositorios de GitHub."""
    def __init__(self, workspace_dir):
        self.workspace_dir = workspace_dir
        if not os.path.exists(workspace_dir):
            os.makedirs(workspace_dir)

    def clone_repository(self, repo_url):
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        target_path = os.path.join(self.workspace_dir, repo_name)
        
        if os.path.exists(target_path):
            return f"El repositorio {repo_name} ya existe en {target_path}"
        
        try:
            subprocess.run(["git", "clone", repo_url, target_path], check=True)
            return f"Clonado con éxito en {target_path}"
        except Exception as e:
            return f"Error al clonar: {e}"

    def explore_qlc_codebase(self, repo_path):
        """Analiza específicamente el código de QLC+ para entender la Virtual Console y Fixtures."""
        analysis = {
            "fixture_definitions": [],
            "virtual_console_logic": [],
            "resource_templates": []
        }
        
        # Buscar definiciones de fixture core (.qxf)
        fixture_dir = os.path.join(repo_path, "resources", "fixtures")
        if os.path.exists(fixture_dir):
            analysis["fixture_definitions"] = os.listdir(fixture_dir)[:10]

        # Buscar lógica de la consola virtual (archivos .cpp con 'virtualconsole')
        for root, _, files in os.walk(os.path.join(repo_path, "engine", "src")):
            for f in files:
                if "virtualconsole" in f.lower():
                    analysis["virtual_console_logic"].append(f)

        return analysis

    def analyze_source_code(self, repo_path):
        """Busca archivos críticos como CMakeLists.txt o archivos de Fixtures (.qxf)."""
        files_found = []
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith((".qxf", ".qxw", ".cpp", ".h")):
                    files_found.append(os.path.join(root, file))
        return files_found[:20] # Retorna los primeros 20 para no saturar
