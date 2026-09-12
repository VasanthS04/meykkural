from typing import List, Dict
import numpy as np

from backend.inference.model_manager import model_manager


def run_batch_inference(
    audio_segments: List[np.ndarray]
) -> List[Dict[str, float]]:
    """
    Run inference on multiple audio segments.

    Audio is processed in memory and is not stored.
    """

    if not audio_segments:
        return []

    results = []

    for audio in audio_segments:

        if audio is None or len(audio) == 0:
            results.append({
                "aasist": 0.0,
                "wav2vec2": 0.0,
                "rawnet2": 0.0,
                "conformer": 0.0,
                "xlsr": 0.0,
                "ecapa": 0.0,
            })
            continue

        result = model_manager.analyze(audio)
        results.append(result)

    return results


def average_batch_scores(
    results: List[Dict[str, float]]
) -> Dict[str, float]:
    """
    Calculate the average score for every model
    across a batch of inference results.
    """

    if not results:
        return {}

    model_names = [
        "aasist",
        "wav2vec2",
        "rawnet2",
        "conformer",
        "xlsr",
        "ecapa",
    ]

    averaged = {}

    for model_name in model_names:

        values = [
            float(result.get(model_name, 0.0))
            for result in results
        ]

        if values:
            averaged[model_name] = round(
                float(np.mean(values)),
                2
            )
        else:
            averaged[model_name] = 0.0

    return averaged


def process_audio_batch(
    audio_segments: List[np.ndarray]
) -> Dict[str, object]:
    """
    Process a complete batch and return both
    individual and averaged model results.
    """

    results = run_batch_inference(
        audio_segments
    )

    average_scores = average_batch_scores(
        results
    )

    return {
        "segments": results,
        "average": average_scores,
        "segment_count": len(audio_segments),
    }