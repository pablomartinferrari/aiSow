from pydantic import BaseModel
from typing import List, Dict, Any


class BBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class Pdf2ImageItem(BaseModel):
    text: str
    confidence: float
    bbox: BBox
    status: str


class PageResult(BaseModel):
    page_number: int
    items: List[Pdf2ImageItem]
    tables: List[Dict[str, Any]] = []
    images: List[str] = []


class Pdf2ImageResponse(BaseModel):
    filename: str
    image_paths: List[str]
    processing_time: Dict[str, float]
    status: str
