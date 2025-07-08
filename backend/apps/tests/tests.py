import sys, os


# Add backend (for 'apps') and backend/apps (for 'services') to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

import fitz
from apps.models.models import TextElement
from services.VectorizerService.services.vectorizer import VectorizerService
from services.EmbeddingService.services.embedding_service import EmbeddingService


import logging

logging.basicConfig(level=logging.INFO)


def test_vectorize_and_embed_first_25_pages():
    logging.info("[TEST] test_vectorize_and_embed_first_25_pages started.")

    # Ensure the test project does not exist, then create it fresh in Neo4j
    embedding_service = EmbeddingService()
    with embedding_service.driver.session() as session:
        session.run(
            "MATCH (p:Project {id: $project_id}) DETACH DELETE p",
            project_id="test_project",
        )
        session.run("CREATE (p:Project {id: $project_id})", project_id="test_project")
    embedding_service.close()

    # Path to test PDF
    pdf_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "uploads", "test_data.pdf"
    )
    assert os.path.exists(pdf_path), f"Test PDF not found: {pdf_path}"

    # Read only the first 25 pages
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    # Only process the first 25 pages
    new_doc = fitz.open()
    for i in range(min(25, len(doc))):
        new_doc.insert_pdf(doc, from_page=i, to_page=i)
    first_25_bytes = new_doc.write()
    logging.info(f"[DEBUG] Created PDF with {min(25, len(doc))} pages for testing.")

    # Vectorize
    vectorizer = VectorizerService()
    result = vectorizer.vectorize_pdf(first_25_bytes)
    logging.info(f"[DEBUG] Extracted {len(result.texts)} text elements.")
    assert result.texts, "No texts extracted from PDF!"

    # Embed
    embedding_service = EmbeddingService()
    embedding_service.store_texts_and_embeddings("test_project", result.texts)
    embedding_service.close()
    logging.info(
        f"[DEBUG] Embedded {len(result.texts)} text elements from first 25 pages."
    )
    logging.info(
        "[TEST] test_vectorize_and_embed_first_25_pages completed successfully."
    )


if __name__ == "__main__":
    test_vectorize_and_embed_first_25_pages()
