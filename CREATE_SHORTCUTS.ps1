$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")

# 1. Acceso Directo al Lanzador Maestro
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\DESPERTAR VIRGILIO.lnk")
$Shortcut.TargetPath = "c:\AG_ALPHA_AGENT\DESPERTAR_VIRGILIO.bat"
$Shortcut.WorkingDirectory = "c:\AG_ALPHA_AGENT"
$Shortcut.IconLocation = "c:\AG_ALPHA_AGENT\AG_ALPHA_CORE\icon.ico"
$Shortcut.Description = "Lanzador Maestro del Agente Virgilio V6.0"
$Shortcut.Save()

Write-Host "✅ Acceso directo creado en el escritorio con el icono oficial." -ForegroundColor Cyan
