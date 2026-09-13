"""Download small labelled audio fixtures from Hugging Face.

The default source is intentionally small enough for local smoke tests. Audio
is written into the repository's existing bonafide/spoof directory layout.
"""

from argparse import ArgumentParser
from io import BytesIO
from pathlib import Path
import re

import soundfile as sf
from datasets import Audio, load_dataset


DEFAULT_DATASET = "DynamicSuperb/SpoofDetection_ASVspoof2015"
DEFAULT_TARGETS = (
    Path("datasets/benchmark/asvspoofing"),
    Path("datasets/benchmark/deepvoice"),
    Path("datasets/samples"),
)


def normalize_label(value: object) -> str | None:
    label = str(value).strip().lower()
    if label in {"authentic", "bonafide", "bonafied", "real", "genuine"}:
        return "bonafide"
    if label in {"spoofed", "spoof", "fake", "synthetic"}:
        return "spoof"
    return None


def find_column(columns: list[str], candidates: tuple[str, ...]) -> str:
    for candidate in candidates:
        if candidate in columns:
            return candidate
    raise ValueError(f"Could not find one of {candidates} in dataset columns {columns}")


def safe_name(value: object, index: int) -> str:
    if not value:
        return f"sample_{index:04d}"
    name = Path(str(value)).stem
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("._")
    return name or f"sample_{index:04d}"


def download_dataset(
    dataset_id: str,
    targets: tuple[Path, ...],
    max_per_label: int,
    split: str,
) -> int:
    dataset = load_dataset(dataset_id, split=split)
    audio_column = find_column(dataset.column_names, ("audio", "audio_path"))
    label_column = find_column(dataset.column_names, ("label", "labels", "category", "target"))
    if audio_column == "audio":
        dataset = dataset.cast_column(audio_column, Audio(decode=False))
    counts = {"bonafide": 0, "spoof": 0}
    written = 0

    for index, row in enumerate(dataset):
        label = normalize_label(row[label_column])
        if label is None or counts[label] >= max_per_label:
            continue

        audio = row[audio_column]
        if not isinstance(audio, dict):
            raise ValueError(f"Dataset row {index} has no audio metadata")
        audio_source = audio.get("bytes") or audio.get("path")
        if audio_source is None:
            raise ValueError(f"Dataset row {index} has no audio path or bytes")
        signal, sample_rate = sf.read(BytesIO(audio_source) if isinstance(audio_source, bytes) else audio_source)
        filename = f"{counts[label]:04d}_{safe_name(audio.get('path'), index)}.wav"
        for target in targets:
            output = target / label / filename
            output.parent.mkdir(parents=True, exist_ok=True)
            if not output.exists():
                sf.write(output, signal, sample_rate, subtype="PCM_16")
        counts[label] += 1
        written += 1

        if all(count >= max_per_label for count in counts.values()):
            break

    print(f"Downloaded {written} files from {dataset_id}: {counts}")
    return written


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--split", default="test")
    parser.add_argument("--max-per-label", type=int, default=8)
    parser.add_argument("--target", action="append", type=Path, dest="targets")
    args = parser.parse_args()

    if args.max_per_label < 1:
        raise ValueError("--max-per-label must be at least 1")
    targets = tuple(args.targets) if args.targets else DEFAULT_TARGETS
    download_dataset(args.dataset, targets, args.max_per_label, args.split)


if __name__ == "__main__":
    main()