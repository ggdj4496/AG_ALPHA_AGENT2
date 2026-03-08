# Script de Despliegue Maestro - Virgilio V8.0 (GOLD Edition)

$ErrorActionPreference = "Stop"
$ProjectDir = "c:\AG_ALPHA_AGENT"

Write-Host "--- INICIANDO INSTALACIÓN DE INGENIERÍA: VIRGILIO V8.0 GOLD ---" -ForegroundColor Cyan

# 1. Verificación de Directorios
$MandatoryPaths = @("ALPHA_CORE", "ALPHA_BRIDGE", "ALPHA_LAB")
foreach ($path in $MandatoryPaths) {
    if (-not (Test-Path "$ProjectDir\$path")) {
        throw "Error: Falta el directorio crítico $path"
    }
}

# 2. Configuración del Entorno Virtual Profesional
Write-Host "Configurando Python Venv..."
if (-not (Test-Path "$ProjectDir\VENV_MASTER")) {
    python -m venv "$ProjectDir\VENV_MASTER"
}

# 3. Instalación de Dependencias
Write-Host "Sincronizando dependencias..."
& "$ProjectDir\VENV_MASTER\Scripts\pip" install psutil GPUtil firebase-admin python-dotenv telegram python-telegram-bot google-generativeai requests pytest pytest-asyncio customtkinter pillow pystray

# 4. Verificación de Integridad bit-a-bit
Write-Host "Ejecutando suite de pruebas de ingeniería..."
& "$ProjectDir\VENV_MASTER\Scripts\python" -m pytest "$ProjectDir\TESTS\test_core.py"

# 5. Creación de Accesos Directos Maestros
Write-Host "Creando lanzadores en el escritorio..."
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\VIRGILIO MASTER.lnk")
$Shortcut.TargetPath = "$ProjectDir\VIRGILIO_MASTER.PY"
$Shortcut.IconLocation = "$ProjectDir\ALPHA_CORE\icon.ico"
$Shortcut.Save()

Write-Host "--- DESPLIEGUE COMPLETADO AL 100% ---" -ForegroundColor Green
Write-Host "El sistema V8.0 GOLD está certificado y listo para el despertar."
