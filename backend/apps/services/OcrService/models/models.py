from pydantic import BaseModel
from typing import List


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class OCRTextItem(BaseModel):
    text: str
    bounding_box: BoundingBox
    confidence: float


class OCRResponse(BaseModel):
    results: List[OCRTextItem]
