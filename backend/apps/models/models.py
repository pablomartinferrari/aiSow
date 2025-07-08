from pydantic import BaseModel
from typing import List, Optional


class Line(BaseModel):
    start: List[float]  # [x, y]
    end: List[float]  # [x, y]
    length: Optional[float] = None


class TextElement(BaseModel):
    text: str
    position: List[float]  # [x, y]
    font_size: Optional[float] = None
    bbox: Optional[List[float]] = None  # [x, y, width, height]


class PathElement(BaseModel):
    points: List[List[float]]  # [[x1, y1], [x2, y2], ...]


class ScaleInfo(BaseModel):
    units: Optional[str] = None
    ratio: Optional[float] = None


class PageScaleInfo(BaseModel):
    page: int
    scale: Optional[ScaleInfo] = None  # None if NTS
    nts: Optional[bool] = False


class VectorizedPDFResponse(BaseModel):
    lines: List[Line]
    texts: List[TextElement]
    paths: List[PathElement]
    scales: List[PageScaleInfo]
    fallback: Optional[bool] = False
