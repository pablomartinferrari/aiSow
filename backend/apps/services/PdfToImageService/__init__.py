"""
AII SOW Pdf2Image Service

A FastAPI-based Pdf2Image service for converting PDFs to images (and optionally extracting text).
"""

from .models.models import BBox, Pdf2ImageItem, PageResult, Pdf2ImageResponse
from .services.services import PdfToImageService
from .utils.utils import format_easyocr_result

__version__ = "1.0.0"
__all__ = [
    "BBox",
    "Pdf2ImageItem",
    "PageResult",
    "Pdf2ImageResponse",
    "PdfToImageService",
    "format_easyocr_result",
]
