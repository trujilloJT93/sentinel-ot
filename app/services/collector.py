import asyncio
import random
from datetime import datetime
from app.api.devices import db_devices
from app.api.alerts import db_alerts
from app.models.alert import Alert, SeverityLevel, AlertStatus
from app.models.device import DeviceStatus

class OTCollectorService:
    def __init__(self):
        self.is_running = False

    async def start_collection_loop(self):
        """Loop asincrono que simula el escaneo periodico de dispositivos OT"""
        self.is_running = True
        print("🟢 [Sentinel OT] Colector de red industrial INICIADO.")
        
        while self.is_running:
            await asyncio.sleep(10)  # Escanear cada 10 segundos
            
            if not db_devices:
                continue

            # Seleccionar un dispositivo al azar para simular lectura/ping
            target_device = random.choice(db_devices)
            
            # Simular posible perdida de conexion o anomalia (20% de probabilidad)
            event_type = random.choices(
                ["NORMAL", "LATENCY_HIGH", "DISCONNECTED"],
                weights=[80, 15, 5]
            )[0]

            if event_type == "NORMAL":
                target_device.status = DeviceStatus.ONLINE
                print(f"📡 [Collector] {target_device.name} ({target_device.ip_address}) -> Respondiendo OK")

            elif event_type == "LATENCY_HIGH":
                target_device.status = DeviceStatus.WARNING
                print(f"⚠️ [Collector] {target_device.name} -> Latencia elevada detectada (>300ms)")

            elif event_type == "DISCONNECTED":
                target_device.status = DeviceStatus.OFFLINE
                print(f"🚨 [Collector] {target_device.name} -> PERDIDA DE CONEXION DETECTADA")
                
                # Generar alerta automatica de ciberseguridad / falla de red
                new_alert = Alert(
                    id=len(db_alerts) + 1,
                    title=f"Perdida de comunicacion con {target_device.name}",
                    description=f"El dispositivo en IP {target_device.ip_address} dejo de responder pings/solicitudes {target_device.protocol}.",
                    severity=SeverityLevel.HIGH,
                    device_id=target_device.id,
                    source_ip=target_device.ip_address,
                    status=AlertStatus.ACTIVE,
                    timestamp=datetime.now()
                )
                db_alerts.append(new_alert)

collector_service = OTCollectorService()
