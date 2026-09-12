import numpy as np

from backend.audio.buffer import AudioBuffer
from backend.audio.decoder import decode_pcm16
from backend.audio.preprocessing import pcm16_to_float32


def test_pcm16_decoding_and_buffer_limit():
    decoded = pcm16_to_float32(b"\x00\x00\xff\x7f\x00\x80")
    assert np.allclose(decoded, [0.0, 32767 / 32768, -1.0])

    buffer = AudioBuffer(max_samples=3)
    buffer.add(np.arange(5, dtype=np.float32))
    assert np.array_equal(buffer.get(), [2.0, 3.0, 4.0])


def test_decoder_supports_pcm16_alias():
    decoded = decode_pcm16(b"\x00\x00\xff\x7f")
    assert decoded.dtype == np.float32
    assert decoded.shape == (2,)