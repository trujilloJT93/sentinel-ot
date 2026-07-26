import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.devices import router as devices_router
from app.api.alerts import router as alerts_router
from app.services.collector import collector_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Arrancar el colector en segundo plano al iniciar
    asyncio.create_task(collector_service.start_collection_loop())
    yield
    # Apagar el colector al detener la API
    collector_service.is_running = False
    print("🔴 [Sentinel OT] Colector detenido.")

app = FastAPI(
    title="Sentinel OT API",
    description="API para monitoreo, supervision y seguridad en redes de Tecnologia Operativa (OT).",
    version="0.1.0",
    lifespan=lifespan
)

# Incluir los routers
app.include_router(devices_router)
app.include_router(alerts_router)

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "system": "Sentinel OT Core",
        "version": "0.1.0"
    }

@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "ot_collector": "running" if collector_service.is_running else "stopped"
        }
    }
