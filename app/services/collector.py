import asyncio
import random
from datetime import datetime
from app.database import SessionLocal
from app.db_models import DeviceDB, AlertDB
from app.models.alert import SeverityLevel, AlertStatus
from app.models.device import DeviceStatus

class OTCollectorService:
    def __init__(self):
        self.is_running = False

    async def start_collection_loop(self):
        """Loop asincrono que monitorea los dispositivos guardados en BD"""
        self.is_running = True
        print("🟢 [Sentinel OT] Colector conectado a la base de datos e INICIADO.")
        
        while self.is_running:
            await asyncio.sleep(10)
            
            # Crear sesion temporal de BD para la iteracion
            db = SessionLocal()
            try:
                devices = db.query(DeviceDB).all()
                if not devices:
                    continue

                target_device = random.choice(devices)
                event_type = random.choices(
                    ["NORMAL", "LATENCY_HIGH", "DISCONNECTED"],
                    weights=[80, 15, 5]
                )[0]

                if event_type == "NORMAL":
                    target_device.status = DeviceStatus.ONLINE
                    print(f"📡 [Collector] {target_device.name} ({target_device.ip_address}) -> OK")

                elif event_type == "LATENCY_HIGH":
                    target_device.status = DeviceStatus.WARNING
                    print(f"⚠️ [Collector] {target_device.name} -> Latencia elevada")

                elif event_type == "DISCONNECTED":
                    target_device.status = DeviceStatus.OFFLINE
                    print(f"🚨 [Collector] {target_device.name} -> PERDIDA DE CONEXION")
                    
                    new_alert = AlertDB(
                        title=f"Perdida de comunicacion con {target_device.name}",
                        description=f"El dispositivo en IP {target_device.ip_address} dejo de responder pings/solicitudes {target_device.protocol.value}.",
                        severity=SeverityLevel.HIGH,
                        device_id=target_device.id,
                        source_ip=target_device.ip_address,
                        status=AlertStatus.ACTIVE,
                        timestamp=datetime.now()
                    )
                    db.add(new_alert)

                db.commit()
            except Exception as e:
                print(f"❌ Error en Collector: {e}")
                db.rollback()
            finally:
                db.close()

collector_service = OTCollectorService()
