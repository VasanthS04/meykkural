import os


class Settings:
    # Application
    APP_NAME = "Meykkural"
    VERSION = "1.0.0"
    DESCRIPTION = (
        "AI-powered real-time detection and prevention "
        "of voice cloning impersonation attacks."
    )

    # Server
    HOST = os.getenv("MEYKKURAL_HOST", "0.0.0.0")
    PORT = int(os.getenv("MEYKKURAL_PORT", "8000"))

    # Audio
    SAMPLE_RATE = 16000
    CHANNELS = 1
    SAMPLE_WIDTH = 2  # PCM16 = 2 bytes
    AUDIO_FORMAT = "pcm_s16le"

    # Real-time analysis
    ANALYSIS_CHUNK_SECONDS = 2.0
    MIN_AUDIO_SECONDS = 0.5
    MAX_BUFFER_SECONDS = 10.0

    # Privacy
    STORE_AUDIO = False
    RECORD_AUDIO = False
    PERSISTENT_AUDIO_FILES = False
    IN_MEMORY_PROCESSING = True

    # Risk thresholds
    LOW_RISK_MAX = 29.0
    MEDIUM_RISK_MAX = 69.0
    HIGH_RISK_MIN = 70.0

    # WebSocket
    WEBSOCKET_PATH = "/ws/audio"

    # API
    API_PREFIX = "/api"

    # Environment
    DEBUG = os.getenv("MEYKKURAL_DEBUG", "false").lower() == "true"


settings = Settings()