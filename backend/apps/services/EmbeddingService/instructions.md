# 🧠 Copilot Instructions: Add Embedding Support with Ollama (New Service Architecture)

## 🏗️ Goal

Refactor vectorization + embedding logic to follow separation of concerns:

- `VectorizerService` is responsible only for **extracting** vector data from PDFs (lines, text, paths, scale).
- A new `EmbeddingService` will:
  - Create `TextElement` nodes in Neo4j.
  - Call Ollama to generate text embeddings.
  - Store `:Embedding` nodes and connect them to `TextElement` via `:VECTOR_OF`.

---

## 🧱 Service Design

### `VectorizerService`
- Already exists.
- Updates:
  - Remove responsibility for saving to Neo4j.
  - Return `texts`, `lines`, `paths`, and `scales` to caller.

### `EmbeddingService`
New service to be created. Responsibilities:

- `store_texts_and_embeddings(project_id: str, texts: List[TextElement])`
  - For each text:
    - Create `TextElement` node in Neo4j.
    - Get node ID from Cypher return.
    - Call Ollama for embedding.
    - Create `:Embedding` node with vector and connect it using `(:Embedding)-[:VECTOR_OF]->(:TextElement)`.

- `generate_embedding(text: str) -> List[float]`
  - Use HTTP POST to Ollama's local `/api/embeddings` endpoint.
  - Payload:
    ```json
    {
      "model": "nomic-embed-text",
      "prompt": "<text>"
    }
    ```

---

## 📡 Sample Ollama Request (Python)

```python
import requests

def generate_embedding(text: str) -> list:
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    response.raise_for_status()
    return response.json()["embedding"]
