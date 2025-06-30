import React, { useState } from "react";
import { Project } from "./ProjectList";

interface NewProjectFormProps {
    onCreate: (project: Omit<Project, 'id'>) => void;
}

const NewProjectForm: React.FC<NewProjectFormProps> = ({ onCreate }) => {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!name.trim()) return;
        onCreate({ name, description });
        setName("");
        setDescription("");
    };

    return (
        <form onSubmit={handleSubmit} style={{ marginTop: "2rem" }}>
            <h3>Create New Project</h3>
            <div>
                <input
                    type="text"
                    placeholder="Project name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    style={{ padding: "0.5rem", width: "100%", marginBottom: "0.5rem" }}
                />
            </div>
            <div>
                <textarea
                    placeholder="Project description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    style={{ padding: "0.5rem", width: "100%", minHeight: "60px" }}
                />
            </div>
            <button type="submit" style={{ marginTop: "0.5rem" }}>Create Project</button>
        </form>
    );
};

export default NewProjectForm;
