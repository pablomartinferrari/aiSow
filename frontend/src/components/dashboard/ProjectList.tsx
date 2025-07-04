import React from "react";
import { Link } from "react-router-dom";
import { Table, TableHead, TableRow, TableCell, TableBody, Typography, Box, Paper } from '@mui/material';

export type Project = {
    id: string;
    name: string;
    description: string;
};

interface ProjectListProps {
    projects: Project[];
    onSelect: (project: Project) => void;
}

const ProjectList: React.FC<ProjectListProps> = ({ projects, onSelect }) => (
    <Box mt={3}>
        <Typography variant="h5" gutterBottom>Your Projects</Typography>
        {projects.length === 0 ? (
            <Typography color="text.secondary">No projects found.</Typography>
        ) : (
            <Paper elevation={2}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell sx={{ fontWeight: 600 }}>Project Name</TableCell>
                            <TableCell sx={{ fontWeight: 600 }}>Description</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {projects.map((project) => (
                            <TableRow key={project.id} hover>
                                <TableCell>
                                    <Link
                                        to={`/projects/${project.id}`}
                                        style={{ color: '#232946', fontWeight: 600, textDecoration: 'underline', cursor: 'pointer' }}
                                        onClick={() => onSelect(project)}
                                    >
                                        {project.name}
                                    </Link>
                                </TableCell>
                                <TableCell>{project.description}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Paper>
        )}
    </Box>
);

export default ProjectList;
