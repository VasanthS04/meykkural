"""Generate small labelled WAV fixtures for local pipeline smoke tests.

This is not a training corpus. It creates deterministic speech-like tones and
noise so the audio transport, preprocessing, and manifest tooling can be
verified without downloading or committing third-party audio.
"""

from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import soundfile as sf


SAMPLE_RATE = 16000


def write_fixture(path: Path, spoof: bool, seed: int) -> None:
    rng = np.random.default_rng(seed)
    duration = 1.0
    time = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
    carrier = 210.0 if spoof else 175.0
    signal = 0.18 * np.sin(2 * np.pi * carrier * time)
    signal += 0.04 * np.sin(2 * np.pi * (carrier * 2) * time)
    if spoof:
        signal += 0.015 * rng.standard_normal(signal.shape[0])
    signal = signal.astype(np.float32)
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, signal, SAMPLE_RATE, subtype="PCM_16")


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--count", type=int, default=4)
    args = parser.parse_args()

    if args.count < 1:
        raise ValueError("count must be at least 1")

    for index in range(args.count):
        write_fixture(
            args.output_dir / "bonafide" / f"real_{index:03d}.wav",
            spoof=False,
            seed=index,
        )
        write_fixture(
            args.output_dir / "spoof" / f"synthetic_{index:03d}.wav",
            spoof=True,
            seed=index + args.count,
        )

    print(f"Generated {args.count * 2} WAV fixtures in {args.output_dir}")


if __name__ == "__main__":
    main()
