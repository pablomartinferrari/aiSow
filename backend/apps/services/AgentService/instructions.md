## 🤖 Feature: Build Conversational Agent to Query Embedded Project Data

### Summary

Now that we’ve extracted and embedded the content from vectorized PDFs using Ollama and stored it in Neo4j, we want to create a conversational agent that can interact with this data via a chat window in our React app.

---

### 🎯 Goals

- Allow users to ask natural language questions about uploaded plans/documents (e.g., “What is the ceiling height in the living room?” or “Where is the fire exit located?”).
- Use semantic search on the embedded `TextElement` nodes stored in Neo4j.
- Return relevant context snippets to a local LLM via Ollama.
- Show the result in a chat-like UI in the React front end.

---

### 📦 Backend Tasks

- [ ] Create `AgentService` or `QueryAgent` class.
- [ ] Use cosine similarity or vector search in Neo4j (or integrate with an external vector DB, if needed) to find the most relevant `TextElement` nodes based on query embeddings.
- [ ] Generate an embedding for the user’s query using Ollama (`nomic-embed-text`).
- [ ] Select top-N relevant nodes (based on similarity).
- [ ] Format a prompt with those results and send it to Ollama for response generation.
- [ ] Expose an API endpoint `/chat` that takes a user message and returns the agent's reply.

---

### 🖼️ Frontend Tasks (React)

- [ ] Create a `ChatWindow` component (if not already present).
- [ ] Add message input and display bubbles (user and AI).
- [ ] On user input:
  - Send message to backend `/chat` endpoint.
  - Stream or display agent’s response.
- [ ] Add optional indicators for “thinking”, “source text used”, or “reference PDF position”.

---

### 💡 API Contract Example

```http
POST /chat
{
  "project_id": "abc123",
  "message": "What is the ceiling height?"
}
