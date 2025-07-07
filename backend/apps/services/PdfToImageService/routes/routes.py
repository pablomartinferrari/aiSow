import time
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional

from models.models import Pdf2ImageResponse
from services.services import PdfToImageService

router = APIRouter()


def get_pdf_to_image_service() -> PdfToImageService:
    """Get PDF to Image service instance - this would typically come from dependency injection"""
    return PdfToImageService()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "Pdf2Image Service is running", "timestamp": time.time()}


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    languages = [
        {"code": "en", "name": "English"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "de", "name": "German"},
        {"code": "it", "name": "Italian"},
        {"code": "pt", "name": "Portuguese"},
        {"code": "ru", "name": "Russian"},
        {"code": "zh", "name": "Chinese"},
        {"code": "ja", "name": "Japanese"},
        {"code": "ko", "name": "Korean"},
    ]
    return languages


@router.post("/process-pdf", response_model=Pdf2ImageResponse)
async def process_pdf(
    file: UploadFile = File(...),
    language: str = Form("en"),
    extract_tables: bool = Form(False),
    extract_images: bool = Form(False),
    page_number: Optional[int] = Form(None),
):
    """Process PDF file and convert to images"""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        file_content = await file.read()
        pdf_to_image_service = get_pdf_to_image_service()

        return await pdf_to_image_service.process_pdf(
            file_content=file_content,
            filename=file.filename,
            page_number=page_number,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@router.post("/process-image", response_model=Pdf2ImageResponse)
async def process_image(file: UploadFile = File(...), language: str = Form("en")):
    """Process image file and extract text using OCR"""
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/tiff", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, detail="File must be an image (JPEG, PNG, TIFF, BMP)"
        )

    try:
        file_content = await file.read()
        pdf_to_image_service = get_pdf_to_image_service()

        return await pdf_to_image_service.process_image(
            file_content=file_content,
            filename=file.filename,
            language=language,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
