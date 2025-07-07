from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import Optional
import numpy as np
import cv2
from services.processor import FloorPlanProcessor
from models.models import FloorPlanProcessorResponse
import json

router = APIRouter()


@router.post("/process", response_model=FloorPlanProcessorResponse)
async def process_floorplan(
    file: UploadFile = File(...),
    ocr_json: str = Form(...),
    scale: Optional[float] = Form(None),
):
    try:
        image_bytes = await file.read()
        npimg = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        ocr_results = json.loads(ocr_json)
        processor = FloorPlanProcessor(scale=scale)
        result = processor.process(img, ocr_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
