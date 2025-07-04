import React, { useState } from "react";
import { Project } from "./ProjectList";
import { Box, TextField, Button, Typography, Paper } from '@mui/material';

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
        <Paper elevation={2} sx={{ mt: 4, p: 3, maxWidth: 500 }}>
            <form onSubmit={handleSubmit}>
                <Typography variant="h6" gutterBottom>Create New Project</Typography>
                <TextField
                    label="Project name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    fullWidth
                    margin="normal"
                />
                <TextField
                    label="Project description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    fullWidth
                    margin="normal"
                    multiline
                    minRows={3}
                />
                <Box mt={2}>
                    <Button type="submit" variant="contained" color="primary">
                        Create Project
                    </Button>
                </Box>
            </form>
        </Paper>
    );
};

export default NewProjectForm;
