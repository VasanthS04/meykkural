"""Prepare labelled WAV manifests without copying raw audio into git."""

from argparse import ArgumentParser
from pathlib import Path
import csv


def build_manifest(input_dir: Path, output_file: Path) -> int:
    rows = []
    for audio_path in sorted(input_dir.rglob("*.wav")):
        label = audio_path.parent.name.lower()
        if label not in {"bonafide", "spoof", "real", "fake"}:
            continue
        normalized = "bonafide" if label in {"bonafide", "real"} else "spoof"
        rows.append({"path": str(audio_path.resolve()), "label": normalized})

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8") as manifest:
        writer = csv.DictWriter(manifest, fieldnames=["path", "label"])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()
    print(f"Wrote {build_manifest(args.input_dir, args.output_file)} labelled files")


if __name__ == "__main__":
    main()