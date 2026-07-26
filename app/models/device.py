from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ProtocolType(str, Enum):
    MODBUS_TCP = "Modbus-TCP"
    OPC_UA = "OPC-UA"
    PROFINET = "Profinet"
    DNP3 = "DNP3"
    ETHERNET_IP = "EtherNet/IP"

class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    WARNING = "warning"

class DeviceBase(BaseModel):
    name: str = Field(..., example="PLC Siemens S7-1500")
    ip_address: str = Field(..., example="192.168.1.100")
    protocol: ProtocolType
    vendor: Optional[str] = Field(None, example="Siemens")
    location: Optional[str] = Field(None, example="Planta 1 - Línea de Embalaje")

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    status: DeviceStatus = DeviceStatus.ONLINE

    class Config:
        from_attributes = True
