from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum, DateTime, ForeignKey
from datetime import datetime
from app.database import Base
from app.models.device import ProtocolType, DeviceStatus
from app.models.alert import SeverityLevel, AlertStatus

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class DeviceDB(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    protocol = Column(SQLEnum(ProtocolType), nullable=False)
    vendor = Column(String, nullable=True)
    location = Column(String, nullable=True)
    status = Column(SQLEnum(DeviceStatus), default=DeviceStatus.ONLINE)

class AlertDB(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    severity = Column(SQLEnum(SeverityLevel), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    source_ip = Column(String, nullable=False)
    status = Column(SQLEnum(AlertStatus), default=AlertStatus.ACTIVE)
    timestamp = Column(DateTime, default=datetime.now)
