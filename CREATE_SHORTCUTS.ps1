$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")

# 1. Acceso Directo al Orquestador Maestro (V8.0 GOLD)
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\VIRGILIO V8 GOLD.lnk")
$Shortcut.TargetPath = "c:\AG_ALPHA_AGENT\VIRGILIO_MASTER.PY"
$Shortcut.WorkingDirectory = "c:\AG_ALPHA_AGENT"
$Shortcut.IconLocation = "c:\AG_ALPHA_AGENT\ALPHA_CORE\icon.ico"
$Shortcut.Description = "Orquestador Maestro Virgilio V8.0 GOLD Edition"
$Shortcut.Save()

Write-Host "✅ Acceso directo V8.0 GOLD creado en el escritorio." -ForegroundColor Cyan
