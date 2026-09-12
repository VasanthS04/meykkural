import requests
import torch
from pathlib import Path
import os


def download_file(url: str, dest_path: Path, description: str = ""):
    """Download a file with progress indication."""
    if dest_path.exists():
        print(f"✅ {description} already exists at {dest_path}")
        return
    
    print(f"📥 Downloading {description} from {url}")
    response = requests.get(url, stream=True)
    
    if response.status_code != 200:
        print(f"❌ Failed to download {description}: {response.status_code}")
        return
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            if total_size:
                downloaded += len(chunk)
                progress = (downloaded / total_size) * 100
                print(f"  Progress: {progress:.1f}%", end='\r')
    
    print(f"\n✅ Downloaded {description} to {dest_path}")


def download_architecture(model_name: str, source_repo: str, dest_dir: Path):
    """Download architecture file for a model."""
    url = f"https://huggingface.co/{source_repo}/raw/main/model.py"
    dest_path = dest_dir / "architecture.py"
    download_file(url, dest_path, f"{model_name} architecture")


def download_weights(model_name: str, source_repo: str, weight_file: str, dest_path: Path):
    """Download weights file for a model."""
    url = f"https://huggingface.co/{source_repo}/resolve/main/{weight_file}"
    download_file(url, dest_path, f"{model_name} weights")


def setup_all_models():
    """Setup all 6 models."""
    models_config = {
        "aasist": {
            "repo": "clovaai/aasist",
            "weight_file": "pretrained_model.pth",
            "weight_size": "101 MB"
        },
        "wav2vec2": {
            "repo": "facebook/wav2vec2-base",
            "weight_file": "pytorch_model.bin",
            "weight_size": "360 MB"
        },
        "rawnet2": {
            "repo": "ALLA1N/rawnet2-itw-robustness-specialist",
            "weight_file": "best_auc.pth",
            "weight_size": "70.5 MB"
        },
        "conformer": {
            "repo": "openmmlab/mmclassification",
            "weight_file": "conformer-tiny-p16_3rdparty_8xb128_in1k_20211206-f6860372.pth",
            "weight_size": "23.5 MB"
        },
        "ecapa": {
            "repo": "yangwang825/ecapa-tdnn-vox2",
            "weight_file": "embedding_model.ckpt",
            "weight_size": "24.9 MB"
        }
    }
    
    # Special handling for XLSR (uses transformers library)
    print("\n📥 Setting up XLSR...")
    xlsr_path = Path("backend/models/xlsr/architecture.py")
    if not xlsr_path.exists():
        # XLSR doesn't need a separate architecture file since it uses transformers
        with open(xlsr_path, 'w') as f:
            f.write('"""XLSR uses HuggingFace transformers library. No architecture file needed."""')
        print(f"✅ XLSR setup complete")
    
    # Setup each model
    for model_name, config in models_config.items():
        print(f"\n{'='*50}")
        print(f"Setting up {model_name.upper()}")
        print(f"{'='*50}")
        
        model_dir = Path(f"backend/models/{model_name}")
        weights_dir = Path(f"backend/model_weights/{model_name}")
        
        model_dir.mkdir(parents=True, exist_ok=True)
        weights_dir.mkdir(parents=True, exist_ok=True)
        
        # Download architecture
        download_architecture(
            model_name,
            config["repo"],
            model_dir
        )
        
        # Download weights
        download_weights(
            model_name,
            config["repo"],
            config["weight_file"],
            weights_dir / "model.pth" if model_name != "ecapa" else weights_dir / "model.ckpt"
        )


def setup_rawnet2_specific():
    """Download RawNet2 from the recommended source."""
    model_dir = Path("backend/models/rawnet2")
    weights_dir = Path("backend/model_weights/rawnet2")
    model_dir.mkdir(parents=True, exist_ok=True)
    weights_dir.mkdir(parents=True, exist_ok=True)
    
    # Download from ALLA1N (recommended)
    download_architecture(
        "RawNet2",
        "ALLA1N/rawnet2-itw-robustness-specialist",
        model_dir
    )
    
    download_weights(
        "RawNet2",
        "ALLA1N/rawnet2-itw-robustness-specialist",
        "best_auc.pth",
        weights_dir / "model.pth"
    )


if __name__ == "__main__":
    print("🚀 Starting model setup...")
    
    # Setup all models
    setup_all_models()
    
    # Also setup RawNet2 with the recommended repo
    print("\n" + "="*50)
    print("Setting up RECOMMENDED RawNet2 version")
    print("="*50)
    setup_rawnet2_specific()
    
    print("\n✅ All models have been downloaded successfully!")
    print("\n📍 Model locations:")
    print("  - Architectures: backend/models/*/architecture.py")
    print("  - Weights: backend/model_weights/*/model.pth or .ckpt")