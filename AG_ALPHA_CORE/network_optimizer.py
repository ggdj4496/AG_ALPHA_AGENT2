import subprocess
import re
import os
import logging
import socket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VIRGILIO_NET")

class NetworkOptimizer:
    def __init__(self):
        self.log_file = r"c:\AG_ALPHA_AGENT\AG_ALPHA_BRAIN\NETWORK_DIAGNOSTICS.txt"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def scan_wifi_interfaces(self):
        """Escanea interfaces WiFi y determina calidad de señal."""
        try:
            output = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], encoding="latin-1")
            signal = re.search(r"Señal\s+:\s+(\d+)%", output)
            ssid = re.search(r"SSID\s+:\s+(.+)", output)
            state = re.search(r"Estado\s+:\s+(.+)", output)
            
            report = {
                "ssid": ssid.group(1).strip() if ssid else "N/A",
                "signal_strength": int(signal.group(1)) if signal else 0,
                "status": state.group(1).strip() if state else "Desconocido"
            }
            logger.info(f"Escaneo WiFi: {report}")
            return report
        except Exception as e:
            logger.error(f"Error escaneando WiFi: {e}")
            return None

    def get_wifi_channel_analysis(self):
        """Analiza canales WiFi cercanos para encontrar el menos congestionado."""
        try:
            # Escaneo de BSSIDs y canales
            output = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"], encoding="latin-1")
            channels = re.findall(r"Canal\s+:\s+(\d+)", output)
            
            # Contar frecuencias por canal
            from collections import Counter
            counts = Counter(channels)
            
            # Sugerencias (2.4GHz: 1, 6, 11 son los mejores)
            suggestions = []
            if counts.get('1', 0) > counts.get('6', 0) and counts.get('11', 0) > counts.get('6', 0):
                suggestions.append("Cambia el canal 2.4GHz al 6 (Parece menos saturado).")
            elif int(counts.get('6', 0)) > 5:
                suggestions.append("Canal 6 saturado. Prueba el 1 o el 11.")

            return {
                "detected_channels": dict(counts),
                "suggestions": suggestions
            }
        except Exception as e:
            logger.error(f"Error analizando canales: {e}")
            return {"error": str(e)}

    def optimize_network_stack(self):
        """Aplica optimizaciones de GRADO MILITAR para sincronizar red."""
        commands = [
            ["ipconfig", "/flushdns"],
            ["netsh", "int", "ip", "reset"],
            ["netsh", "winsock", "reset"],
            ["netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"],
            ["netsh", "int", "tcp", "set", "global", "rss=enabled"],
            ["netsh", "interface", "tcp", "set", "heuristics", "disabled"],
            ["netsh", "wlan", "set", "autoconfig", "enabled=no", "interface=Wi-Fi"] # Evita lag de escaneo
        ]
        results = []
        for cmd in commands:
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=5)
                results.append(f"SUCCESS: {' '.join(cmd)}")
            except:
                results.append(f"FAILED: {' '.join(cmd)}")
        
        return results

    def restore_wifi_autoconfig(self):
        """Restaura el escaneo automático de WiFi."""
        subprocess.run(["netsh", "wlan", "set", "autoconfig", "enabled=yes", "interface=Wi-Fi"], capture_output=True)

    def optimize_ports_for_virgilio(self):
        """Sugiere y verifica puertos para Virgilio, Telegram y JDownloader."""
        # Puertos Críticos
        ports = {
            "Telegram (Bridge)": "443, 80, 5222",
            "JDownloader": "9666 (Local), 10101 (Remote)",
            "Virgilio Core": "Custom 8080 (opcional)"
        }
        advice = [
            "Para tu Livebox 6:",
            "1. Accede a http://192.168.1.1",
            "2. Configurar > Red > NAT/PAT",
            f"3. Asegura que los puertos {ports['JDownloader']} están abiertos para este PC."
        ]
        return advice

    def diagnose_orange_hardware(self):
        """Diagnóstico específico para Orange Livebox 6 y Repetidor."""
        gateway = self._get_gateway()
        is_orange = gateway == "192.168.1.1"
        
        report = [
            f"Gateway detectado: {gateway}",
            f"Hardware Orange probable: {'SI' if is_orange else 'NO'}",
            "--- TIPS ORANGE ---",
            "URL Panel: http://192.168.1.1 o http://livebox/",
            "Pass por defecto: Primeros 8 caracteres de tu clave WiFi.",
            "Sync Repetidor: Pulsa WPS en Livebox y luego '+' en el repetidor."
        ]
        return "\n".join(report)

    def suggest_roaming_tuning(self):
        """Sugiere ajustes de agresividad de itinerancia para mejorar el cambio entre Router y Repetidor."""
        return (
            "Sugerencia: Para mejor sincronía con el repetidor, ajusta 'Agresividad de Itinerancia' a 'Media-Alta' "
            "en las propiedades avanzadas de tu adaptador WiFi en el Administrador de Dispositivos."
        )

    def _get_gateway(self):
        try:
            ip_config = subprocess.check_output(["ipconfig"], encoding="latin-1")
            gateway = re.search(r"Puerta de enlace predeterminada . . . . . : ([\d\.]+)", ip_config)
            return gateway.group(1) if gateway else "No detectado"
        except:
            return "Error detectando IP"

    def trace_latency_to_gateway(self):
        """Mide la latencia real hacia el router para detectar micro-cortes."""
        gateway = self._get_gateway()
        if gateway == "No detectado": return "Error: No se puede trazar latencia sin gateway."
        
        try:
            output = subprocess.check_output(["ping", "-n", "4", gateway], encoding="latin-1")
            latencies = re.findall(r"tiempo[=<](\d+)ms", output)
            if latencies:
                avg = sum(map(int, latencies)) / len(latencies)
                return f"Latencia media al Router: {avg}ms (Estado: {'ÓPTIMO' if avg < 5 else 'MEJORABLE'})"
            return "No se ha podido obtener respuesta del Gateway."
        except Exception as e:
            return f"Error en ping: {e}"

    async def run_diagnostics(self):
        """Ejecuta un diagnóstico completo de red para el Orquestador."""
        logger.info("📡 Iniciando Diagnóstico de Red Alpha-Master...")
        return {
            "wifi": self.scan_wifi_interfaces(),
            "latency": self.trace_latency_to_gateway(),
            "orange_hardware": self.diagnose_orange_hardware()
        }
