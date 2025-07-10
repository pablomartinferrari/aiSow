from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from neo4j import GraphDatabase
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llava"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "strongpassword123"

app = FastAPI(
    title="Vectorizer Service",
    version="1.0.0",
    description="Extracts vector geometry, text, and scale from floor plan images and performs LLM-based semantic analysis.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# PROMPT TEMPLATE
# ------------------------------------
LLM_PROMPT_TEMPLATE = """
IMPORTANT: Respond ONLY with a valid JSON array. Do NOT include any explanation, commentary, or markdown. If you cannot answer, return [] and nothing else.

You are an expert in architectural plan analysis. Your task is to review OCR-extracted text from a floor plan image. The text is organized as a list of lines, each with a bounding box and words.

Analyze the input lines and identify distinct spaces or rooms described in the plan.

Return a JSON array. Each object must have:
- space_id: unique ID (string)
- name_on_drawing: original label (or "")
- inferred_type: e.g., Bedroom, Lobby, etc.
- is_bathroom: true/false
- is_common_area: true/false
- size: small/medium/large
- description: brief explanation

Again: Respond ONLY with a valid JSON array. Do NOT include any explanation, commentary, or markdown. If you cannot answer, return [] and nothing else.

INPUT LINES:
{lines_payload}
"""


# ------------------------------------
# DATA MODELS
# ------------------------------------
class OCRLine(BaseModel):
    text: str
    words: List[Dict[str, Any]]
    bbox: List[int]
    block_num: int
    par_num: int
    line_num: int


class OCRPage(BaseModel):
    image_path: str
    page: int
    lines: List[OCRLine]


class OCRDocument(BaseModel):
    pages: List[OCRPage]


# ------------------------------------
# OLLAMA LLM CALLER
# ------------------------------------
def call_llm(prompt: str) -> List[Dict[str, Any]]:
    print(
        "[LLM] Sending prompt to Ollama (truncated):\n",
        prompt[:500],
        "...\n---END PROMPT---",
    )
    response = requests.post(
        OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    )
    response.raise_for_status()
    content = response.json()["response"]
    print(
        "[LLM] Ollama response (truncated):\n", content[:500], "...\n---END RESPONSE---"
    )
    import re

    try:
        return json.loads(content)
    except Exception as e:
        print(
            "[LLM] ERROR: Invalid JSON from model. Attempting to extract JSON array..."
        )
        print(content)
        # Try to extract the first JSON array from the response
        match = re.search(r"\[.*?\]", content, re.DOTALL)
        if match:
            try:
                print("[LLM] Extracted JSON array, attempting to parse...")
                return json.loads(match.group(0))
            except Exception as e2:
                print("[LLM] ERROR: Still invalid after extraction.")
                print(match.group(0))
        raise ValueError(f"Invalid JSON from model: {content[:500]}") from e


# ------------------------------------
# NEO4J STORAGE
# ------------------------------------
def store_in_neo4j(spaces: List[Dict[str, Any]], image_path: str, page_number: int):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        for space in spaces:
            session.run(
                """
                MERGE (s:Space {space_id: $space_id})
                SET s.name_on_drawing = $name_on_drawing,
                    s.inferred_type = $inferred_type,
                    s.is_bathroom = $is_bathroom,
                    s.is_common_area = $is_common_area,
                    s.size = $size,
                    s.description = $description,
                    s.image_path = $image_path,
                    s.page_number = $page_number
            """,
                {
                    "space_id": space["space_id"],
                    "name_on_drawing": space.get("name_on_drawing", ""),
                    "inferred_type": space.get("inferred_type", ""),
                    "is_bathroom": space.get("is_bathroom", False),
                    "is_common_area": space.get("is_common_area", False),
                    "size": space.get("size", ""),
                    "description": space.get("description", ""),
                    "image_path": image_path,
                    "page_number": page_number,
                },
            )
    driver.close()


# ------------------------------------
# PROCESS OCR PAGE
# ------------------------------------
def process_page(page: OCRPage) -> List[Dict[str, Any]]:
    lines_payload = json.dumps([line.dict() for line in page.lines], indent=2)
    prompt = LLM_PROMPT_TEMPLATE.replace("{lines_payload}", lines_payload)
    return call_llm(prompt)


# ------------------------------------
# FASTAPI ROUTE
# ------------------------------------
@app.post("/process")
def process_ocr(document: OCRDocument):
    try:
        all_spaces = []
        for page in document.pages:
            spaces = process_page(page)
            store_in_neo4j(spaces, page.image_path, page.page)
            all_spaces.extend(spaces)
        return {
            "status": "success",
            "total_spaces": len(all_spaces),
            "spaces": all_spaces,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
