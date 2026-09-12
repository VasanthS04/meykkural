"""
ECAPA-TDNN speaker verification model.
"""

from .model import ECAPAModel
from .inference import ECAPAInference

__all__ = [
    "ECAPAModel",
    "ECAPAInference",
]