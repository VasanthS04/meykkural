# Meykkural

Meykkural is a real-time voice authenticity monitor. The inference path
exposes six model signals (AASIST, Wav2Vec2, RawNet2, Conformer, XLS-R, and
ECAPA-TDNN) and keeps incoming audio in memory.

Wav2Vec2 currently uses its native architecture. The other checked-in
checkpoints are retained and validated as model artifacts, but their original
training architectures are not included in this repository. They therefore
use the shared multi-cue acoustic anti-spoof detector until their exact
architectures and classification heads are integrated. This keeps every model
signal live and bounded instead of returning zeros or failing the request.

## Run locally

Start the backend from the repository root:

```cmd
py -3.13 -m venv .venv
.venv\Scripts\activate
py -m pip install -r backend\requirements.txt
py -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

In a second terminal, start the frontend:

```cmd
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` and `/ws` to the backend.

## Validate

```cmd
py -3.13 -m pytest tests\backend -q
cd frontend
npm run build
```

No `download.zip` is required. The model checkpoint is already in the
repository under `backend\model_weights\wav2vec2`.

To create local audio fixtures and a manifest:

```cmd
py scripts\generate_synthetic_dataset.py datasets\testing\generated
py scripts\prepare_dataset.py datasets\testing\generated datasets\testing\manifest.csv
```

These fixtures validate transport and preprocessing only; they are not a
replacement for a licensed real-world training or validation corpus.

## Download data and models

The lightweight local audio fixtures come from the public Hugging Face dataset
[DynamicSuperb/SpoofDetection_ASVspoof2015](https://huggingface.co/datasets/DynamicSuperb/SpoofDetection_ASVspoof2015).
Install the backend requirements, then download a balanced sample into all
three local dataset targets:

```cmd
py scripts\download_datasets.py --max-per-label 4
```

The script writes `bonafide` and `spoof` WAV files to
`datasets\benchmark\asvspoofing`, `datasets\benchmark\deepvoice`, and
`datasets\samples`. Increase `--max-per-label` for a larger local sample or
pass `--target datasets\my-dataset` to use another output directory. Downloaded
audio is ignored by git.

For larger or task-specific corpora, use the dataset catalog at
[Hugging Face Datasets](https://huggingface.co/datasets). Review each dataset's
license and access requirements before downloading or redistributing audio.

The model downloader references these Hugging Face repositories:

- [clovaai/aasist](https://huggingface.co/clovaai/aasist)
- [facebook/wav2vec2-base](https://huggingface.co/facebook/wav2vec2-base)
- [ALLA1N/rawnet2-itw-robustness-specialist](https://huggingface.co/ALLA1N/rawnet2-itw-robustness-specialist)
- [openmmlab/mmclassification](https://huggingface.co/openmmlab/mmclassification)
- [yangwang825/ecapa-tdnn-vox2](https://huggingface.co/yangwang825/ecapa-tdnn-vox2)

The checked-in model artifacts under `backend\model_weights` are sufficient
for the current local application. Checkpoint downloads may be large and can
have separate licenses.

## Technology stack

- **Frontend:** React 18, Vite, and `lucide-react`
- **Backend:** Python 3.13, FastAPI, Uvicorn, and WebSockets
- **Audio:** librosa, SciPy, SoundFile, torchaudio, and in-memory buffering
- **Machine learning:** PyTorch, Transformers, Hugging Face Datasets,
  safetensors, SpeechBrain, and scikit-learn
- **Models:** AASIST, Wav2Vec2, RawNet2, Conformer, XLS-R, and ECAPA-TDNN
- **Operations:** Docker Compose, environment variables via `python-dotenv`,
  and PyYAML configuration
