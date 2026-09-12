from io import BytesIO

import numpy as np
import soundfile as sf
from fastapi import APIRouter, File, UploadFile

from backend.inference.pipeline import process_audio


router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"]
)


@router.get("/status")
async def analysis_status():
    return {
        "status": "ready",
        "system": "Meykkural",
        "analysis_type": "real-time voice analysis"
    }


@router.post("/analyze")
async def analyze_upload(file: UploadFile = File(...)):
    """Analyze an uploaded WAV/FLAC/OGG audio file in memory."""
    audio_bytes = await file.read()
    audio, sample_rate = sf.read(
        BytesIO(audio_bytes),
        dtype="float32",
        always_2d=True,
    )
    mono_audio = np.mean(audio, axis=1)
    return process_audio(mono_audio, sample_rate)


def analyze_audio(audio, sample_rate=16000):
    return process_audio(audio, sample_rate)