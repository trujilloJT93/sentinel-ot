from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from app.models.alert import Alert, AlertCreate, SeverityLevel, AlertStatus

router = APIRouter(prefix="/api/v1/alerts", tags=["OT Security Alerts"])

# Base de datos temporal en memoria para alertas
db_alerts: List[Alert] = [
    Alert(
        id=1,
        title="Escaneo de puertos Modbus detectado",
        description="Escaneo intensivo hacia el puerto TCP 502 desde la red corporativa.",
        severity=SeverityLevel.HIGH,
        device_id=2,
        source_ip="10.0.0.45",
        status=AlertStatus.ACTIVE,
        timestamp=datetime.now()
    ),
    Alert(
        id=2,
        title="Cambio de estado inesperado en PLC",
        description="El PLC Siemens S7-1200 cambio a modo STOP sin orden de mantenimiento.",
        severity=SeverityLevel.CRITICAL,
        device_id=1,
        source_ip="192.168.1.10",
        status=AlertStatus.ACKNOWLEDGED,
        timestamp=datetime.now()
    )
]

@router.get("", response_model=List[Alert])
async def get_alerts(severity: Optional[SeverityLevel] = None):
    """Obtener todas las alertas de seguridad OT (filtrables por gravedad)"""
    if severity:
        return [alert for alert in db_alerts if alert.severity == severity]
    return db_alerts

@router.post("", response_model=Alert, status_code=201)
async def create_alert(alert: AlertCreate):
    """Generar una nueva alerta de ciberseguridad OT"""
    new_alert = Alert(
        id=len(db_alerts) + 1,
        **alert.model_dump()
    )
    db_alerts.append(new_alert)
    return new_alert

@router.patch("/{alert_id}/acknowledge", response_model=Alert)
async def acknowledge_alert(alert_id: int):
    """Reconocer/Aceptar una alerta por parte del operador OT"""
    for alert in db_alerts:
        if alert.id == alert_id:
            alert.status = AlertStatus.ACKNOWLEDGED
            return alert
    raise HTTPException(status_code=404, detail="Alerta no encontrada")
