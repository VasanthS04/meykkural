import numpy as np
import librosa


def extract_lfcc(
    audio: np.ndarray,
    sample_rate: int = 16000,
    n_lfcc: int = 20
) -> np.ndarray:
    """
    Approximate LFCC extraction using a linear-frequency
    filter-bank followed by DCT.
    """

    if audio is None or len(audio) == 0:
        return np.empty(
            (n_lfcc, 0),
            dtype=np.float32
        )

    stft = np.abs(
        librosa.stft(
            audio.astype(np.float32),
            n_fft=512,
            hop_length=160
        )
    ) ** 2

    frequencies = librosa.fft_frequencies(
        sr=sample_rate,
        n_fft=512
    )

    n_filters = 40

    edges = np.linspace(
        0,
        sample_rate / 2,
        n_filters + 2
    )

    filter_bank = np.zeros(
        (n_filters, len(frequencies)),
        dtype=np.float32
    )

    for i in range(n_filters):
        left = edges[i]
        center = edges[i + 1]
        right = edges[i + 2]

        rising = (
            (frequencies >= left) &
            (frequencies <= center)
        )

        falling = (
            (frequencies > center) &
            (frequencies <= right)
        )

        if center > left:
            filter_bank[i, rising] = (
                frequencies[rising] - left
            ) / (center - left)

        if right > center:
            filter_bank[i, falling] = (
                right - frequencies[falling]
            ) / (right - center)

    energies = np.dot(
        filter_bank,
        stft
    )

    energies = np.maximum(
        energies,
        1e-10
    )

    log_energy = np.log(
        energies
    )

    lfcc = librosa.feature.mfcc(
        S=log_energy,
        n_mfcc=n_lfcc
    )

    return lfcc.astype(np.float32)