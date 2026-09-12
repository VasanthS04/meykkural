import numpy as np

from backend.privacy.privacy_manager import PrivacyManager


def test_privacy_manager_discards_audio_on_stop():
    manager = PrivacyManager(sample_rate=16000, max_seconds=1)
    manager.start_analysis()
    manager.add_audio(np.ones(100, dtype=np.float32))
    assert manager.privacy_status()["audio_stored"] is False
    manager.stop_analysis()
    assert manager.get_audio().size == 0