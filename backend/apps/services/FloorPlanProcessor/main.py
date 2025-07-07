from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.routes import router

app = FastAPI(
    title="Floor Plan Processor Service",
    version="1.0.0",
    description="Detects rooms, walls, and associates OCR labels with room geometry in floor plans.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
