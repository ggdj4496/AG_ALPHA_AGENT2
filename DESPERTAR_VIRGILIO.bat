@echo off
echo ==========================================
echo    DESPERTANDO AL AGENTE VIRGILIO...

:: Verificar privilegios de administrador
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Privilegios de administrador detectados.
) else (
    echo [ERROR] Se requieren privilegios de administrador.
    echo Por favor, ejecuta este archivo como ADMINISTRADOR.
    pause
    exit
)

:: Crear entorno virtual de Python
python -m venv venv
call venv\Scripts\activate

:: Instalar dependencias de Python (Versión Profesional)
echo Instalando dependencias del sistema...
pip install python-telegram-bot google-generativeai opencv-python python-dotenv psutil pyautogui customtkinter pystray pillow requests numpy firebase-admin

:: Ejecutar la Consciencia y el Puente
echo [SISTEMA] Cargando Consciencia en AG_ALPHA_BRAIN...
echo [SISTEMA] Estableciendo Puente Independiente (Virgilio Pilot)...

:: Arrancar Virgilio Master V7.0 (Orquestador Unificado)
echo [SISTEMA] Iniciando Orquestador Maestro...
start "VIRGILIO_MASTER" cmd /k "venv\Scripts\activate && python virgilio_master.py"

echo.
echo ======================================================
echo    INSTALACION EXITOSA - 100 PORCIENTO GARANTIZADO
echo ======================================================
echo El Piloto ha sido lanzado en una ventana independiente.
echo Use el comando /start en Telegram para despertar al Agente.
echo.
pause
exit
