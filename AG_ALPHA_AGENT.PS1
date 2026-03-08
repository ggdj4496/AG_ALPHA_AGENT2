# SCRIPT DE INYECCIÓN DE MODELOS GRATUITOS - PROTOCOLO VIRGILIO
# Ejecutar como Administrador para asegurar permisos ROOT

Write-Host "Iniciando asimilación de modelos de código gratuitos..." -ForegroundColor Cyan

# 1. Instalar dependencias para modelos Open Source
Write-Host "Instalando librerías de conexión..."
pip install openai huggingface_hub requests --quiet

# 2. Configurar asociación de archivos .py con Python
Write-Host "Reparando asociación de archivos .py..."
assoc .py=Python.File
ftype Python.File="C:\Windows\py.exe" "%1" %*

# 3. Inyectar modelos en el archivo .env
$envPath = "C:\AG_ALPHA_AGENT\AG_ALPHA_BRAIN\.env"
$models = @"
# MODELOS DE CÓDIGO GRATUITOS (OPENROUTER/HF)
FREE_MODEL_CODER=deepseek/deepseek-chat
FREE_MODEL_FAST=qwen/qwen-2.5-72b-instruct
FREE_MODEL_REVERSE=meta-llama/llama-3.1-70b-instruct
"@

if (Test-Path $envPath) {
    Add-Content -Path $envPath -Value $models
    Write-Host "Modelos inyectados con éxito en .env." -ForegroundColor Green
}
else {
    Write-Host "ERROR: No se encontró el archivo .env en $envPath" -ForegroundColor Red
}

# 4. Crear carpeta de Dossier de Mejoras
$dossierPath = "C:\CALABOZO\PROYECTOS\CAT11_SISTEMAYHARDW"
if (!(Test-Path $dossierPath)) {
    New-Item -ItemType Directory -Path $dossierPath
    Write-Host "Carpeta de hardware creada en $dossierPath"
}

Write-Host "PROCESO COMPLETADO. Reinicia Antigravity y selecciona GPT-OSS 120B." -ForegroundColor Yellow