import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Project } from "../components/dashboard/ProjectList";
import UploadPage from "./UploadPage";

// For now, we'll mock the project data. In a real app, you'd fetch this from state or an API.
const mockProjects: Project[] = [];

const ProjectDetailsPage: React.FC = () => {
    const { projectId } = useParams<{ projectId: string }>();
    const navigate = useNavigate();
    const project = mockProjects.find((p) => p.id === projectId);

    if (!project) {
        return (
            <div>
                <h2>Project not found</h2>
                <button onClick={() => navigate(-1)}>Back</button>
            </div>
        );
    }

    return (
        <div>
            <h1>{project.name}</h1>
            <p>{project.description}</p>
            <h3>Upload Files</h3>
            <UploadPage />
        </div>
    );
};

export default ProjectDetailsPage;
