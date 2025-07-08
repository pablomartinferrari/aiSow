import requests
from typing import List, Dict, Any
from neo4j import GraphDatabase
import numpy as np


class AgentService:
    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "strongpassword123",
        ollama_url: str = "http://localhost:11434/api/embeddings",
        ollama_chat_url: str = "http://localhost:11434/api/chat",  # fixed endpoint
    ):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.ollama_url = ollama_url
        self.ollama_chat_url = ollama_chat_url

    def close(self):
        self.driver.close()

    def get_query_embedding(self, query: str) -> List[float]:
        response = requests.post(
            self.ollama_url, json={"model": "nomic-embed-text", "prompt": query}
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def find_relevant_texts(
        self, project_id: str, query_embedding: List[float], top_n: int = 5
    ) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (p:Project {id: $project_id})-[:HAS_TEXT]->(t:TextElement)<-[:VECTOR_OF]-(e:Embedding)
                RETURN t, e.vector AS embedding
                """,
                project_id=project_id,
            )
            texts = []
            for record in result:
                text = record["t"]
                embedding = record["embedding"]
                if embedding:
                    texts.append(
                        {"text": text["text"], "embedding": embedding, "meta": text}
                    )

        def cosine_similarity(a, b):
            a = np.array(a)
            b = np.array(b)
            return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

        for t in texts:
            t["similarity"] = cosine_similarity(query_embedding, t["embedding"])

        texts.sort(key=lambda x: x["similarity"], reverse=True)
        return texts[:top_n]

    def generate_agent_response(
        self, user_message: str, context_snippets: List[str]
    ) -> str:
        prompt = (
            "You are an expert assistant for architectural plans. Use the following context to answer the user's question.\n"
            f"Context:\n{chr(10).join(context_snippets)}\n"
        )

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message},
        ]

        response = requests.post(
            self.ollama_chat_url,
            json={
                "model": "mistral:7b",
                "prompt": prompt,
                "stream": False,
            },
        )
        if not response.ok:
            print(f"Error from Ollama API: {response.status_code} - {response.text}")
            response.raise_for_status()
        return response.json().get("message", {}).get("content", "")

    def chat(self, project_id: str, message: str, top_n: int = 5) -> Dict[str, Any]:
        query_embedding = self.get_query_embedding(message)
        relevant_texts = self.find_relevant_texts(
            project_id, query_embedding, top_n=top_n
        )
        context_snippets = [t["text"] for t in relevant_texts]
        agent_reply = self.generate_agent_response(message, context_snippets)
        return {
            "reply": agent_reply,
            "context": context_snippets,
            "meta": [t["meta"] for t in relevant_texts],
        }
