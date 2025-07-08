import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getProject, Project } from "../services/projectService";
import UploadPage from "./UploadPage";
import {
    Box,
    Typography,
    Button,
    Paper,
    Container
} from '@mui/material';
import { ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import ProjectChatbot from "../components/project/ProjectChatbot";

const ProjectDetailsPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const { data: project, isLoading, error } = useQuery<Project>({
        queryKey: ["project", id],
        queryFn: () => getProject(id!),
        enabled: !!id,
    });

    if (isLoading) return <div>Loading...</div>;
    if (error || !project) {
        return (
            <Container>
                <Box sx={{ mt: 4, textAlign: 'center' }}>
                    <Typography variant="h4" gutterBottom>
                        Project not found
                    </Typography>
                    <Button
                        variant="outlined"
                        startIcon={<ArrowBackIcon />}
                        onClick={() => navigate(-1)}
                        sx={{ mt: 2 }}
                    >
                        Go Back
                    </Button>
                </Box>
            </Container>
        );
    }

    return (
        <Container>
            <Box sx={{ mt: 4 }}>
                <Button
                    variant="outlined"
                    startIcon={<ArrowBackIcon />}
                    onClick={() => navigate('/projects')}
                    sx={{ mb: 3 }}
                >
                    Back to Projects
                </Button>

                <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
                    <Typography variant="h3" gutterBottom>
                        {project.name}
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                        {project.description}
                    </Typography>
                </Paper>

                <Typography variant="h5" gutterBottom>
                    Upload Files
                </Typography>
                <UploadPage />
                <Typography variant="h5" gutterBottom>
                    Ask about this project
                </Typography>
                <ProjectChatbot projectId={project.id} />
            </Box>
        </Container>
    );
};

export default ProjectDetailsPage;