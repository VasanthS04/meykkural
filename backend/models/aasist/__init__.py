"""
AASIST anti-spoofing model.
"""

from .model import AASISTModel
from .inference import AASISTInference

__all__ = [
    "AASISTModel",
    "AASISTInference",
]