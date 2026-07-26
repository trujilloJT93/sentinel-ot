from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.db_models import DeviceDB
from app.models.device import Device, DeviceCreate

router = APIRouter(prefix="/api/v1/devices", tags=["OT Devices"])

@router.get("", response_model=List[Device])
def get_devices(db: Session = Depends(get_db)):
    """Obtener todos los dispositivos OT registrados en la BD"""
    return db.query(DeviceDB).all()

@router.post("", response_model=Device, status_code=201)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo activo OT en la BD"""
    db_device = DeviceDB(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device
