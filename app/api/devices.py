from fastapi import APIRouter, HTTPException
from typing import List
from app.models.device import Device, DeviceCreate, DeviceStatus

router = APIRouter(prefix="/api/v1/devices", tags=["OT Devices"])

# Base de datos temporal en memoria
db_devices: List[Device] = [
    Device(
        id=1,
        name="PLC Siemens S7-1200",
        ip_address="192.168.1.10",
        protocol="Profinet",
        vendor="Siemens",
        location="Proceso Principal",
        status=DeviceStatus.ONLINE
    ),
    Device(
        id=2,
        name="Modbus Gateway",
        ip_address="192.168.1.50",
        protocol="Modbus-TCP",
        vendor="Moxa",
        location="Subestación B",
        status=DeviceStatus.WARNING
    )
]

@router.get("", response_model=List[Device])
async def get_devices():
    """Obtener todos los dispositivos OT registrados"""
    return db_devices

@router.post("", response_model=Device, status_code=201)
async def create_device(device: DeviceCreate):
    """Registrar un nuevo activo OT"""
    new_device = Device(
        id=len(db_devices) + 1,
        **device.model_dump()
    )
    db_devices.append(new_device)
    return new_device
