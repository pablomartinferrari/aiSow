export async function askAgent(projectId, message) {
    const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_id: projectId, message })
    });
    if (!res.ok) throw new Error("Agent service error");
    return await res.json();
}
