"""
XLS-R based anti-deepfake model.
"""

from .model import XLSRModel
from .inference import XLSRInference

__all__ = [
    "XLSRModel",
    "XLSRInference",
]