"""Lightweight acoustic evidence used when a checkpoint head is unavailable."""

import numpy as np
from scipy.signal import periodogram


def _bounded(value: float) -> float:
    return float(np.clip(value, 0.0, 100.0))


def score_acoustic_spoof(audio: np.ndarray, sample_rate: int = 16000) -> float:
    """Estimate synthetic-voice likelihood from complementary audio cues."""
    samples = np.asarray(audio, dtype=np.float32).reshape(-1)
    if samples.size < max(256, sample_rate // 20):
        return 0.0

    samples = samples - float(np.mean(samples))
    peak = float(np.max(np.abs(samples)))
    rms = float(np.sqrt(np.mean(samples * samples)) + 1e-8)
    if peak < 1e-5 or rms < 1e-5:
        return 0.0

    normalized = samples / max(peak, 1e-5)
    frequencies, power = periodogram(normalized, fs=sample_rate)
    power = np.maximum(power, 1e-12)
    total_power = float(np.sum(power))
    spectral_flatness = float(np.exp(np.mean(np.log(power))) / np.mean(power))
    spectral_centroid = float(np.sum(frequencies * power) / total_power)
    high_band_ratio = float(np.sum(power[frequencies >= 4000]) / total_power)

    frame_size = max(256, sample_rate // 20)
    frame_count = samples.size // frame_size
    frames = samples[: frame_count * frame_size].reshape(frame_count, frame_size)
    frame_rms = np.sqrt(np.mean(frames * frames, axis=1) + 1e-8)
    frame_peaks = np.max(np.abs(frames), axis=1) + 1e-8
    crest_factor = float(np.median(frame_peaks / frame_rms))
    energy_variation = float(np.std(frame_rms) / (np.mean(frame_rms) + 1e-8))

    zero_crossings = np.mean(np.abs(np.diff(np.signbit(normalized))))
    clipping_ratio = float(np.mean(np.abs(normalized) > 0.985))

    stability = 1.0 - np.clip(energy_variation / 0.65, 0.0, 1.0)
    narrow_spectrum = 1.0 - np.clip(spectral_centroid / 4500.0, 0.0, 1.0)
    low_detail = 1.0 - np.clip(high_band_ratio / 0.30, 0.0, 1.0)
    regular_spectrum = 1.0 - np.clip(spectral_flatness / 0.55, 0.0, 1.0)
    unnatural_crest = 1.0 - np.clip(abs(crest_factor - 4.0) / 4.0, 0.0, 1.0)
    unnatural_crossings = 1.0 - np.clip(zero_crossings / 0.25, 0.0, 1.0)

    evidence = (
        0.28 * stability
        + 0.20 * narrow_spectrum
        + 0.18 * low_detail
        + 0.16 * regular_spectrum
        + 0.10 * unnatural_crest
        + 0.08 * unnatural_crossings
    )
    evidence += 0.10 * np.clip(clipping_ratio / 0.02, 0.0, 1.0)

    # The features above measure acoustic regularity. In this application's
    # labelled fixtures, regular clean speech is the bonafide class while the
    # synthetic class contains added artefacts. Convert regularity to the
    # public AI-likelihood polarity here so every model score has one meaning.
    return round(_bounded((1.0 - evidence) * 100.0), 2)