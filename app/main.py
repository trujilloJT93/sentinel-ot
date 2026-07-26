from fastapi import FastAPI

app = FastAPI(
    title="Sentinel OT API",
    description="API para monitoreo, supervisión y seguridad en redes de Tecnología Operativa (OT).",
    version="0.1.0"
)

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
