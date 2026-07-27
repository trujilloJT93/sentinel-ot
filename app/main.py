import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.database import engine, Base, SessionLocal
from app.db_models import DeviceDB, UserDB
from app.models.device import ProtocolType, DeviceStatus
from app.core.security import get_password_hash
from app.api.devices import router as devices_router
from app.api.alerts import router as alerts_router
from app.api.auth import router as auth_router
from app.services.collector import collector_service

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates")

def seed_data():
    db = SessionLocal()
    if db.query(UserDB).count() == 0:
        admin_user = UserDB(
            username="admin",
            email="admin@sentinel.ot",
            hashed_password=get_password_hash("admin123")
        )
        db.add(admin_user)
        db.commit()
        print("👤 [Database] Usuario 'admin' (password: admin123) creado por defecto.")

    if db.query(DeviceDB).count() == 0:
        initial_devices = [
            DeviceDB(
                name="PLC Siemens S7-1200",
                ip_address="192.168.1.10",
                protocol=ProtocolType.PROFINET,
                vendor="Siemens",
                location="Proceso Principal",
                status=DeviceStatus.ONLINE
            ),
            DeviceDB(
                name="Modbus Gateway",
                ip_address="192.168.1.50",
                protocol=ProtocolType.MODBUS_TCP,
                vendor="Moxa",
                location="Subestacion B",
                status=DeviceStatus.WARNING
            )
        ]
        db.add_all(initial_devices)
        db.commit()
        print("🌱 [Database] Datos semilla creados.")
    db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_data()
    asyncio.create_task(collector_service.start_collection_loop())
    yield
    collector_service.is_running = False
    print("🔴 [Sentinel OT] Colector detenido.")

app = FastAPI(
    title="Sentinel OT API",
    description="API para monitoreo, supervision y seguridad en redes de Tecnologia Operativa (OT).",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(devices_router)
app.include_router(alerts_router)

@app.get("/", tags=["Dashboard"])
async def render_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "sqlite_connected",
            "ot_collector": "running" if collector_service.is_running else "stopped"
        }
    }
