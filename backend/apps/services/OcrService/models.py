from pydantic import BaseModel
from typing import List, Dict, Any


class BBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class OcrItem(BaseModel):
    text: str
    confidence: float
    bbox: BBox
    status: str


class PageResult(BaseModel):
    page_number: int
    items: List[OcrItem]
    tables: List[Dict[str, Any]] = []
    images: List[str] = []


class OcrResponse(BaseModel):
    filename: str
    pages: List[PageResult]
    processing_time: Dict[str, float]
    status: str
