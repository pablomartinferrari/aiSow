import React, { useState } from "react";
import { askAgent } from "../../services/agentService";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";

interface ProjectChatbotProps {
    projectId: string;
}

interface AgentMessage {
    sender: "user" | "ai";
    text: string;
    context?: string[];
}

export default function ProjectChatbot({ projectId }: ProjectChatbotProps) {
    const [messages, setMessages] = useState<AgentMessage[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!input.trim()) return;
        setLoading(true);
        setMessages([...messages, { sender: "user", text: input }]);
        try {
            const response = await askAgent(projectId, input);
            setMessages((msgs) => [
                ...msgs,
                { sender: "ai", text: response.reply, context: response.context }
            ]);
        } catch (e) {
            setMessages((msgs) => [
                ...msgs,
                { sender: "ai", text: "Error: Could not get a response from the agent." }
            ]);
        }
        setInput("");
        setLoading(false);
    };

    return (
        <Box>

            <Box sx={{ display: "flex", gap: 1, alignItems: "center", marginTop: 1, marginBottom: 2 }}>
                <TextField
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                    placeholder="Ask a question about this project..."
                    variant="outlined"
                    size="small"
                    fullWidth
                    disabled={loading}
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={sendMessage}
                    disabled={loading || !input.trim()}
                >
                    Send
                </Button>
            </Box>
            <Box sx={{ minHeight: 200, border: "1px solid #ccc", padding: 2 }}>
                {messages.map((msg, idx) => (
                    <div key={idx} style={{ margin: "8px 0" }}>
                        <b>{msg.sender === "user" ? "You" : "Agent"}:</b> {msg.text}
                        {msg.context && (
                            <div style={{ fontSize: "0.8em", color: "#888" }}>
                                <b>Context:</b> {msg.context.join(" | ")}
                            </div>
                        )}
                    </div>
                ))}
                {loading && <div>Thinking...</div>}
            </Box>
        </Box>
    );
}
