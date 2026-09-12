import numpy as np


def decode_pcm16(
    data: bytes,
    channels: int = 1
) -> np.ndarray:
    """
    Decode signed 16-bit PCM audio into float32 samples.

    Input:
        PCM16 little-endian bytes

    Output:
        Mono float32 samples in range approximately [-1, 1]
    """

    if not data:
        return np.array(
            [],
            dtype=np.float32
        )

    samples = np.frombuffer(
        data,
        dtype="<i2"
    ).astype(np.float32)

    if channels > 1:
        usable = (
            len(samples)
            - len(samples) % channels
        )

        samples = samples[:usable]

        if usable > 0:
            samples = samples.reshape(
                -1,
                channels
            ).mean(axis=1)

    samples /= 32768.0

    return np.clip(
        samples,
        -1.0,
        1.0
    ).astype(np.float32)


def decode_audio(
    data: bytes,
    encoding: str = "pcm16",
    channels: int = 1
) -> np.ndarray:
    """
    Decode supported raw audio formats.

    Currently supported:
        pcm16
    """

    encoding = encoding.lower().strip()

    if encoding in {
        "pcm16",
        "pcm_s16le",
        "s16le"
    }:
        return decode_pcm16(
            data,
            channels
        )

    raise ValueError(
        f"Unsupported audio encoding: {encoding}"
    )