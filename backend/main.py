from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.api.routes import router
from backend.api.websocket import router as websocket_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# API Routes
# --------------------------------------------------

app.include_router(router)

# WebSocket
app.include_router(websocket_router)


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
async def root():
    return {
        "system": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "online",
        "service": "FastAPI",
        "message": "Meykkural backend is running.",
    }


# --------------------------------------------------
# Application Events
# --------------------------------------------------

@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("Meykkural Backend Starting")
    print("=" * 60)
    print(f"Host        : {settings.HOST}")
    print(f"Port        : {settings.PORT}")
    print(f"Sample Rate : {settings.SAMPLE_RATE} Hz")
    print(f"Audio Store : {settings.STORE_AUDIO}")
    print(f"WebSocket   : {settings.WEBSOCKET_PATH}")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    print("Meykkural Backend stopped.")