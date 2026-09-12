from typing import Dict

import numpy as np

from backend.inference.model_manager import model_manager


def run_inference(audio: np.ndarray) -> Dict[str, float]:
    """Run the configured model ensemble on one audio segment."""
    return model_manager.analyze(audio)