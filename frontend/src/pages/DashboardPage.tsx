import React, { useState } from "react";
import ProjectList, { Project } from "../components/dashboard/ProjectList";
import NewProjectForm from "../components/dashboard/NewProjectForm";

const DashboardPage: React.FC = () => {
    const [projects, setProjects] = useState<Project[]>([]);

    const handleCreateProject = (project: Omit<Project, "id">) => {
        const newProject: Project = {
            id: Date.now().toString(),
            ...project,
        };
        setProjects((prev) => [...prev, newProject]);
    };

    const handleSelectProject = (project: Project) => {
        // Here you could navigate to the project details page in the future
    };

    return (
        <div>
            <h1>Dashboard</h1>
            <ProjectList projects={projects} onSelect={handleSelectProject} />
            <NewProjectForm onCreate={handleCreateProject} />
        </div>
    );
};

export default DashboardPage;
