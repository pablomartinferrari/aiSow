import requests
from typing import List
from neo4j import GraphDatabase
from apps.models.models import TextElement


class EmbeddingService:
    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "strongpassword123",
        ollama_url: str = "http://localhost:11434/api/embeddings",
    ):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.ollama_url = ollama_url

    def close(self):
        self.driver.close()

    def generate_embedding(self, text: str) -> List[float]:
        response = requests.post(
            self.ollama_url, json={"model": "nomic-embed-text", "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def store_texts_and_embeddings(self, project_id: str, texts: List[TextElement]):
        with self.driver.session() as session:
            for text in texts:
                # Create TextElement node and get its internal Neo4j ID
                result = session.run(
                    """
                    MATCH (p:Project {id: $project_id})
                    CREATE (t:TextElement {text: $text, position: $position, font_size: $font_size, bbox: $bbox})
                    MERGE (p)-[:HAS_TEXT]->(t)
                    RETURN id(t) as text_id
                    """,
                    project_id=project_id,
                    text=text.text,
                    position=text.position,
                    font_size=text.font_size,
                    bbox=text.bbox,
                )
                text_id = result.single()["text_id"]
                # Generate embedding
                embedding = self.generate_embedding(text.text)
                # Store Embedding node and connect
                session.run(
                    """
                    MATCH (t:TextElement) WHERE id(t) = $text_id
                    CREATE (e:Embedding {vector: $vector})
                    MERGE (e)-[:VECTOR_OF]->(t)
                    """,
                    text_id=text_id,
                    vector=embedding,
                )
