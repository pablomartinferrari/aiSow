from fastapi import FastAPI, Body
from typing import List
import sys, os


# Add backend/apps to sys.path so 'apps.models.models' is importable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

from apps.models.models import TextElement
from services.embedding_service import EmbeddingService

app = FastAPI()
embedding_service = EmbeddingService()


@app.post("/embed/")
def embed_texts(project_id: str = Body(...), texts: List[TextElement] = Body(...)):
    embedding_service.store_texts_and_embeddings(project_id, texts)
    return {"status": "success", "count": len(texts)}


@app.on_event("shutdown")
def shutdown_event():
    embedding_service.close()
