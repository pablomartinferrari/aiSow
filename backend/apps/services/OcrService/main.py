from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.routes import router

app = FastAPI(
    title="Floor Plan OCR Service",
    version="1.0.0",
    description="Extracts text from floor plan images and returns recognized text, bounding box, and confidence.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
