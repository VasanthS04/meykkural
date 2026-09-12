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
