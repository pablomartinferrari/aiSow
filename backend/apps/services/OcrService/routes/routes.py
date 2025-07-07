from fastapi import APIRouter, File, UploadFile, HTTPException
from services.ocr_service import OcrService
from models.models import OCRResponse

router = APIRouter()
ocr_service = OcrService()


@router.post("/ocr", response_model=OCRResponse)
async def ocr_image(file: UploadFile = File(...)):
    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/jpg",
        "image/bmp",
        "image/tiff",
    ]:
        raise HTTPException(status_code=400, detail="File must be an image.")
    try:
        image_bytes = await file.read()
        result = ocr_service.process_image(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")
