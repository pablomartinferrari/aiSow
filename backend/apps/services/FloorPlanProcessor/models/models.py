from pydantic import BaseModel
from typing import List, Optional, Dict


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class RoomPolygon(BaseModel):
    points: List[List[int]]  # [[x1, y1], [x2, y2], ...]


class RealSize(BaseModel):
    width_m: Optional[float]
    height_m: Optional[float]


class RoomLabelResult(BaseModel):
    label: str
    bounding_box: BoundingBox
    room_polygon: RoomPolygon
    real_size: Optional[RealSize]
    confidence: Optional[float]


class FloorPlanProcessorResponse(BaseModel):
    rooms: List[RoomLabelResult]
    debug_images: Optional[Dict[str, str]]  # filename or base64
