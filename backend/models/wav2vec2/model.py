from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
from torchaudio.models import wav2vec2_model


class Wav2Vec2Model(nn.Module):
    """Wav2Vec2 feature extractor backed by the project checkpoint."""

    def __init__(
        self,
        checkpoint_path: Optional[str] = None,
        device: Optional[str] = None,
    ):
        super().__init__()

        self.device = device or (
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.checkpoint_loaded = False
        self.network = wav2vec2_model(
            extractor_mode="group_norm",
            extractor_conv_layer_config=[
                (512, 10, 5),
                (512, 3, 2),
                (512, 3, 2),
                (512, 3, 2),
                (512, 3, 2),
                (512, 2, 2),
                (512, 2, 2),
            ],
            extractor_conv_bias=False,
            encoder_embed_dim=768,
            encoder_projection_dropout=0.1,
            encoder_pos_conv_kernel=128,
            encoder_pos_conv_groups=16,
            encoder_num_layers=12,
            encoder_num_heads=12,
            encoder_attention_dropout=0.1,
            encoder_ff_interm_features=3072,
            encoder_ff_interm_dropout=0.0,
            encoder_dropout=0.1,
            encoder_layer_norm_first=False,
            encoder_layer_drop=0.05,
            aux_num_out=32,
        )

        if checkpoint_path:
            self.load_checkpoint(checkpoint_path)

        self.to(self.device)

    def load_checkpoint(self, checkpoint_path: str) -> bool:
        path = Path(checkpoint_path)
        if not path.exists():
            return False

        checkpoint = torch.load(
            path,
            map_location="cpu",
            weights_only=True,
        )
        state_dict = checkpoint.get("state_dict", checkpoint)
        self.network.load_state_dict(state_dict, strict=True)
        self.checkpoint_loaded = True
        self.to(self.device)
        return True

    def forward(self, audio: torch.Tensor) -> torch.Tensor:
        if not self.checkpoint_loaded:
            raise RuntimeError("Wav2Vec2 checkpoint is not loaded.")

        if audio.ndim == 1:
            audio = audio.unsqueeze(0)
        if audio.ndim != 2:
            raise ValueError("Audio must have shape [batch, samples].")

        features = self.network.extract_features(audio)[0][-1]
        return features.mean(dim=1)