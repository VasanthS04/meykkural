from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "online",
        "system": "Meykkural",
        "service": "FastAPI",
        "version": "1.0.0"
    }


@router.get("/api/status")
async def system_status():
    return {
        "backend": "online",
        "audio_processing": "ready",
        "websocket": "ready",
        "analysis": "ready",
        "audio_storage": False
    }