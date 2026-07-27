from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.db_models import AlertDB, UserDB
from app.models.alert import Alert, AlertCreate, AlertStatus
from app.core.security import get_current_user

router = APIRouter(prefix="/api/v1/alerts", tags=["OT Security Alerts"])

@router.get("", response_model=List[Alert])
def get_alerts(db: Session = Depends(get_db)):
    """Obtener historial de alertas de ciberseguridad OT (Publico)"""
    return db.query(AlertDB).order_by(AlertDB.timestamp.desc()).all()

@router.post("", response_model=Alert, status_code=201)
def create_alert(
    alert: AlertCreate, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)  # 👈 Requiere autenticacion JWT
):
    """Registrar una nueva alerta manualmente (Requiere Token JWT)"""
    db_alert = AlertDB(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.patch("/{alert_id}/acknowledge", response_model=Alert)
def acknowledge_alert(
    alert_id: int, 
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)  # 👈 Requiere autenticacion JWT
):
    """Reconocer una alerta de seguridad (Requiere Token JWT)"""
    alert = db.query(AlertDB).filter(AlertDB.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    
    alert.status = AlertStatus.ACKNOWLEDGED
    db.commit()
    db.refresh(alert)
    return alert
