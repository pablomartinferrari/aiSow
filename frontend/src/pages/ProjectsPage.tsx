import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import ProjectList, { Project } from "../components/dashboard/ProjectList";
import NewProjectForm from "../components/dashboard/NewProjectForm";
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchProjects, createProject } from "../services/projectService";
import {
    Box,
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Typography,
    Fab
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';

const ProjectsPage: React.FC = () => {
    const navigate = useNavigate();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const { data: projects, isLoading, error } = useQuery<Project[]>({
        queryKey: ['projects'],
        queryFn: fetchProjects,
    });

    const queryClient = useQueryClient();
    const mutation = useMutation({
        mutationFn: createProject,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['projects'] });
            setIsModalOpen(false); // Close modal after successful creation
        },
    });

    const handleCreateProject = (project: Omit<Project, "id">) => {
        mutation.mutate(project);
    };

    const handleSelectProject = (project: Project) => {
        // Navigate to the specific project page
        navigate(`/projects/${project.id}`);
    };

    const handleOpenModal = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error loading projects</div>;

    return (
        <Box sx={{ position: 'relative', minHeight: '100vh' }}>
            <Typography variant="h4" gutterBottom>
                Projects
            </Typography>

            <ProjectList projects={projects || []} onSelect={handleSelectProject} />

            {/* Floating Action Button */}
            <Fab
                color="primary"
                aria-label="add project"
                onClick={handleOpenModal}
                sx={{
                    position: 'fixed',
                    bottom: 24,
                    right: 24,
                }}
            >
                <AddIcon />
            </Fab>

            {/* Create Project Modal */}
            <Dialog
                open={isModalOpen}
                onClose={handleCloseModal}
                maxWidth="sm"
                fullWidth
            >
                <DialogTitle>
                    Create New Project
                </DialogTitle>
                <DialogContent>
                    <NewProjectForm onCreate={handleCreateProject} />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseModal} color="inherit">
                        Cancel
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default ProjectsPage; 