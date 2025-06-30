import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getProject, Project } from "../services/projectService";
import UploadPage from "./UploadPage";

const ProjectDetailsPage: React.FC = () => {
    const { projectId } = useParams<{ projectId: string }>();
    const navigate = useNavigate();

    const { data: project, isLoading, error } = useQuery<Project>({
        queryKey: ["project", projectId],
        queryFn: () => getProject(projectId!),
        enabled: !!projectId,
    });

    if (isLoading) return <div>Loading...</div>;
    if (error || !project) {
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