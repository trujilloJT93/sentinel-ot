from fastapi import FastAPI
from app.api.devices import router as devices_router
from app.api.alerts import router as alerts_router

app = FastAPI(
    title="Sentinel OT API",
    description="API para monitoreo, supervision y seguridad en redes de Tecnologia Operativa (OT).",
    version="0.1.0"
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
            "ot_collector": "running"
        }
    }
