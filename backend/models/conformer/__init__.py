"""
Conformer anti-spoofing model.
"""

from .model import ConformerModel
from .inference import ConformerInference

__all__ = [
    "ConformerModel",
    "ConformerInference",
]