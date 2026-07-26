from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(str, Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"

class AlertBase(BaseModel):
    title: str = Field(..., example="Acceso Modbus no autorizado")
    description: str = Field(..., example="Se detecto un intento de escritura en registros de retencion desde una IP desconocida.")
    severity: SeverityLevel
    device_id: Optional[int] = Field(None, example=1)
    source_ip: str = Field(..., example="192.168.1.200")

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    status: AlertStatus = AlertStatus.ACTIVE
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
