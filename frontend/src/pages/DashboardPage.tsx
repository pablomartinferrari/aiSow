import React, { useState } from "react";
import ProjectList, { Project } from "../components/dashboard/ProjectList";
import NewProjectForm from "../components/dashboard/NewProjectForm";
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchProjects, createProject } from "../services/projectService";

const DashboardPage: React.FC = () => {
    const { data: projects, isLoading, error } = useQuery<Project[]>({
        queryKey: ['projects'],
        queryFn: fetchProjects,
    });

    const queryClient = useQueryClient();
    const mutation = useMutation({
        mutationFn: createProject,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['projects'] });
        },
    });

    const handleCreateProject = (project: Omit<Project, "id">) => {
        mutation.mutate(project);
    };

    const handleSelectProject = (project: Project) => {
        // Here you could navigate to the project details page in the future
    };

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error loading projects</div>;
    return (
        <div>
            <h1>Dashboard</h1>
            <ProjectList projects={projects || []} onSelect={handleSelectProject} />
            <NewProjectForm onCreate={handleCreateProject} />
        </div>
    );
};

export default DashboardPage;
