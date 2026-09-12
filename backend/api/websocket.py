import asyncio
import json

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect
)

from backend.audio.buffer import AudioBuffer
from backend.audio.preprocessing import pcm16_to_float32
from backend.audio.resampler import resample_audio
from backend.inference.pipeline import process_audio


router = APIRouter()


@router.websocket("/ws/audio")
async def audio_websocket(
    websocket: WebSocket
):
    await websocket.accept()

    audio_buffer = AudioBuffer(
        max_samples=16000 * 10
    )
    input_sample_rate = 16000
    samples_since_analysis = 0
    analysis_samples = 16000
    analysis_in_progress = False

    try:

        while True:

            message = await websocket.receive()

            if message.get("type") == "websocket.disconnect":
                break

            # --------------------------------
            # JSON / TEXT MESSAGE
            # --------------------------------

            if message.get("text") is not None:

                try:
                    data = json.loads(
                        message["text"]
                    )

                    message_type = data.get(
                        "type"
                    )

                    if data.get("sample_rate"):
                        input_sample_rate = int(data["sample_rate"])

                    if message_type == "start_analysis":

                        audio_buffer.clear()
                        samples_since_analysis = 0

                        await websocket.send_json({
                            "type": "connection",
                            "status": "analysis_started",
                            "system": "Meykkural"
                        })

                    elif message_type == "stop_analysis":

                        audio_buffer.clear()
                        samples_since_analysis = 0

                        await websocket.send_json({
                            "type": "connection",
                            "status": "analysis_stopped"
                        })

                except json.JSONDecodeError:

                    await websocket.send_json({
                        "type": "error",
                        "message": "Invalid JSON"
                    })

                continue

            # --------------------------------
            # BINARY AUDIO
            # --------------------------------

            audio_bytes = message.get("bytes")

            if not audio_bytes:
                continue

            audio = pcm16_to_float32(
                audio_bytes
            )

            if input_sample_rate != 16000:
                audio = resample_audio(
                    audio,
                    input_sample_rate,
                    16000
                )

            if len(audio) == 0:
                continue

            audio_buffer.add(
                audio
            )
            samples_since_analysis += len(audio)

            if (
                len(audio_buffer) < analysis_samples or
                samples_since_analysis < analysis_samples or
                analysis_in_progress
            ):
                continue

            samples_since_analysis = 0
            buffered_audio = audio_buffer.get_latest(analysis_samples)

            # Run the complete shared pipeline so every response includes
            # speech, features, model scores, risk, notification, and privacy.
            analysis_in_progress = True
            try:
                result = await asyncio.to_thread(
                    process_audio,
                    buffered_audio,
                    16000,
                )
            finally:
                analysis_in_progress = False
            result["type"] = "analysis"
            result["alert"] = result["notification"]["message"] if result["notification"] else None

            await websocket.send_json(
                result
            )

    except WebSocketDisconnect:
        return

    finally:
        audio_buffer.clear()