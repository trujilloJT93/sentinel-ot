from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.db_models import AlertDB
from app.models.alert import Alert, AlertCreate, SeverityLevel, AlertStatus

router = APIRouter(prefix="/api/v1/alerts", tags=["OT Security Alerts"])

@router.get("", response_model=List[Alert])
def get_alerts(severity: Optional[SeverityLevel] = None, db: Session = Depends(get_db)):
    """Obtener todas las alertas de seguridad OT registradas"""
    query = db.query(AlertDB)
    if severity:
        query = query.filter(AlertDB.severity == severity)
    return query.all()

@router.post("", response_model=Alert, status_code=201)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """Generar una nueva alerta de ciberseguridad OT"""
    db_alert = AlertDB(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.patch("/{alert_id}/acknowledge", response_model=Alert)
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """Reconocer/Aceptar una alerta por parte del operador OT"""
    alert = db.query(AlertDB).filter(AlertDB.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    alert.status = AlertStatus.ACKNOWLEDGED
    db.commit()
    db.refresh(alert)
    return alert
