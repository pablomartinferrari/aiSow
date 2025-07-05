import React from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from '@tanstack/react-query';
import { fetchProjects } from "../services/projectService";
import {
    Box,
    Typography,
    Grid,
    Card,
    CardContent,
    CardActions,
    Button,
    Paper,
    Container
} from '@mui/material';
import {
    Folder as FolderIcon,
    Settings as SettingsIcon,
    Upload as UploadIcon,
    Assessment as AssessmentIcon
} from '@mui/icons-material';

const DashboardPage: React.FC = () => {
    const navigate = useNavigate();
    const { data: projects, isLoading } = useQuery({
        queryKey: ['projects'],
        queryFn: fetchProjects,
    });

    const recentProjects = projects?.slice(0, 3) || [];

    const dashboardItems = [
        {
            title: 'Projects',
            description: 'Manage your project statements of work',
            icon: <FolderIcon sx={{ fontSize: 40 }} />,
            color: 'primary',
            action: () => navigate('/projects')
        },
        {
            title: 'Upload Files',
            description: 'Upload and process project documents',
            icon: <UploadIcon sx={{ fontSize: 40 }} />,
            color: 'secondary' as const,
            action: () => navigate('/upload')
        },
        {
            title: 'Analysis',
            description: 'View project analytics and insights',
            icon: <AssessmentIcon sx={{ fontSize: 40 }} />,
            color: 'success' as const,
            action: () => navigate('/analysis')
        },
        {
            title: 'Settings',
            description: 'Configure your account and preferences',
            icon: <SettingsIcon sx={{ fontSize: 40 }} />,
            color: 'info' as const,
            action: () => navigate('/settings')
        }
    ];

    if (isLoading) return <div>Loading...</div>;

    return (
        <Container>
            <Box sx={{ mt: 4 }}>
                <Typography variant="h3" gutterBottom>
                    Welcome to AI SOW
                </Typography>
                <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
                    Your AI-powered Statement of Work management platform
                </Typography>

                {/* Quick Actions */}
                <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 2 }}>
                    Quick Actions
                </Typography>
                <Grid container spacing={3} sx={{ mb: 4 }}>
                    {dashboardItems.map((item, index) => (
                        <Grid item xs={12} sm={6} md={3} key={index}>
                            <Card
                                sx={{
                                    height: '100%',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    cursor: 'pointer',
                                    '&:hover': {
                                        transform: 'translateY(-2px)',
                                        transition: 'transform 0.2s ease-in-out'
                                    }
                                }}
                                onClick={item.action}
                            >
                                <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                                    <Box sx={{ color: `${item.color}.main`, mb: 2 }}>
                                        {item.icon}
                                    </Box>
                                    <Typography variant="h6" gutterBottom>
                                        {item.title}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        {item.description}
                                    </Typography>
                                </CardContent>
                                <CardActions>
                                    <Button
                                        size="small"
                                        color={item.color}
                                        fullWidth
                                    >
                                        Open
                                    </Button>
                                </CardActions>
                            </Card>
                        </Grid>
                    ))}
                </Grid>

                {/* Recent Projects */}
                <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 2 }}>
                    Recent Projects
                </Typography>
                {recentProjects.length > 0 ? (
                    <Paper elevation={2} sx={{ p: 3 }}>
                        <Grid container spacing={2}>
                            {recentProjects.map((project) => (
                                <Grid item xs={12} sm={6} md={4} key={project.id}>
                                    <Card
                                        sx={{
                                            cursor: 'pointer',
                                            '&:hover': {
                                                backgroundColor: 'action.hover'
                                            }
                                        }}
                                        onClick={() => navigate(`/projects/${project.id}`)}
                                    >
                                        <CardContent>
                                            <Typography variant="h6" gutterBottom>
                                                {project.name}
                                            </Typography>
                                            <Typography variant="body2" color="text.secondary">
                                                {project.description}
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            ))}
                        </Grid>
                        {projects && projects.length > 3 && (
                            <Box sx={{ mt: 3, textAlign: 'center' }}>
                                <Button
                                    variant="outlined"
                                    onClick={() => navigate('/projects')}
                                >
                                    View All Projects
                                </Button>
                            </Box>
                        )}
                    </Paper>
                ) : (
                    <Paper elevation={2} sx={{ p: 3, textAlign: 'center' }}>
                        <Typography variant="body1" color="text.secondary" gutterBottom>
                            No projects yet
                        </Typography>
                        <Button
                            variant="contained"
                            onClick={() => navigate('/projects')}
                        >
                            Create Your First Project
                        </Button>
                    </Paper>
                )}
            </Box>
        </Container>
    );
};

export default DashboardPage;
