from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from services.vectorizer import VectorizerService
from models.models import VectorizedPDFResponse

router = APIRouter()
vectorizer_service = VectorizerService()


@router.post("/vectorize")
async def vectorize_pdf(
    file: UploadFile = File(...),
    project_id: str = Form(...),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF.")
    try:
        pdf_bytes = await file.read()
        result = vectorizer_service.vectorize_pdf(pdf_bytes, project_id)
        # Convert to dict, remove any legacy 'scale' key, and return as response model
        result_dict = result.dict() if hasattr(result, "dict") else dict(result)
        if "scale" in result_dict:
            result_dict.pop("scale")
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vectorization failed: {str(e)}")
