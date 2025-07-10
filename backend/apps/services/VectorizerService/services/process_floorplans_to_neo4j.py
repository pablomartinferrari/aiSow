import json
import uuid
from neo4j import GraphDatabase
import requests

# -----------------------------
# CONFIGURATION
# -----------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llava"  # or other local model
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "strongpassword123"

# -----------------------------
# MAIN PROCESSING PROMPT
# -----------------------------
LLM_PROMPT_TEMPLATE = """
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

Only return the final JSON result. No commentary.

INPUT LINES:
{lines_payload}
"""


# -----------------------------
# OLLAMA CALLER
# -----------------------------
def call_llm(prompt: str) -> list:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
    )
    response.raise_for_status()
    content = response.json()["response"]
    try:
        parsed = json.loads(content)
        assert isinstance(parsed, list)
        return parsed
    except Exception as e:
        raise ValueError(f"Invalid JSON from model: {content[:500]}") from e


# -----------------------------
# NEO4J STORER
# -----------------------------
def store_spaces_in_neo4j(spaces: list, page_image: str, page_number: int):
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
                    "image_path": page_image,
                    "page_number": page_number,
                },
            )
    driver.close()


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def process_pages(pages: list):
    for page in pages:
        image_path = page["image_path"]
        lines = page["lines"]
        page_number = page["page"]

        print(f"\nProcessing page {page_number} - {image_path}")
        lines_payload = json.dumps(lines, indent=2)
        prompt = LLM_PROMPT_TEMPLATE.replace("{lines_payload}", lines_payload)

        try:
            rooms = call_llm(prompt)
            print(f"✓ Got {len(rooms)} room(s). Storing in Neo4j...")
            store_spaces_in_neo4j(rooms, image_path, page_number)
        except Exception as e:
            print(f"✗ Error on page {page_number}: {e}")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    input_json_path = "vectorized_output_half.json"  # path to your processed OCR JSON
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    process_pages(data["pages"])
