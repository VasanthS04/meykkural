"""
Meykkural audio storage policy.
"""


class StoragePolicy:
    """
    Defines the project's audio privacy policy.
    """

    AUDIO_RECORDING = False
    AUDIO_STORAGE = False
    PERSISTENT_AUDIO_FILES = False
    IN_MEMORY_PROCESSING = True

    @classmethod
    def get_policy(cls) -> dict:
        """Return the current privacy policy."""

        return {
            "audio_recording": cls.AUDIO_RECORDING,
            "audio_storage": cls.AUDIO_STORAGE,
            "persistent_audio_files": (
                cls.PERSISTENT_AUDIO_FILES
            ),
            "in_memory_processing": (
                cls.IN_MEMORY_PROCESSING
            ),
            "raw_audio_retention": False,
        }

    @classmethod
    def allows_storage(cls) -> bool:
        """Return whether persistent audio storage is allowed."""
        return cls.AUDIO_STORAGE

    @classmethod
    def allows_recording(cls) -> bool:
        """Return whether audio recording is allowed."""
        return cls.AUDIO_RECORDING

    @classmethod
    def describe(cls) -> str:
        """Return a human-readable privacy description."""

        return (
            "Meykkural processes audio in memory for real-time "
            "analysis. Raw conversation audio is not persistently "
            "recorded or stored."
        )