"""
AI SOW OCR Service

A FastAPI-based OCR service using EasyOCR for text extraction from PDFs and images.
"""

from .models import BBox, OcrItem, PageResult, OcrResponse
from .services import OcrService
from .utils import format_easyocr_result

__version__ = "1.0.0"
__all__ = [
    "BBox",
    "OcrItem",
    "PageResult",
    "OcrResponse",
    "OcrService",
    "format_easyocr_result",
]
