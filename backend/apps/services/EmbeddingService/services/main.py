from fastapi import FastAPI, Body
from typing import List
from apps.models.models import TextElement
from .embedding_service import EmbeddingService

app = FastAPI()
embedding_service = EmbeddingService()


@app.post("/embed/")
def embed_texts(project_id: str = Body(...), texts: List[TextElement] = Body(...)):
    embedding_service.store_texts_and_embeddings(project_id, texts)
    return {"status": "success", "count": len(texts)}


@app.on_event("shutdown")
def shutdown_event():
    embedding_service.close()
