from fastapi import APIRouter, UploadFile, File, HTTPException
from services.vectorizer import VectorizerService
import os
import tempfile

router = APIRouter()
vectorizer_service = VectorizerService()


@router.post("/vectorize-images")
async def vectorize_images(files: list[UploadFile] = File(...)):
    """
    Accepts multiple image files, runs OCR and layout grouping, and returns JSON results.
    """
    temp_paths = []
    try:
        for file in files:
            suffix = os.path.splitext(file.filename)[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                temp_paths.append(tmp.name)
        result = vectorizer_service.vectorize_images(temp_paths)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Image vectorization failed: {str(e)}"
        )
    finally:
        for path in temp_paths:
            try:
                os.remove(path)
            except Exception:
                pass
