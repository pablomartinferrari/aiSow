import React, { useState } from "react";
import { Box, TextField, Button, Typography } from '@mui/material';
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
        <Box component="form" onSubmit={handleSubmit} sx={{ pt: 1 }}>
            <TextField
                label="Project name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                fullWidth
                margin="normal"
                autoFocus
            />
            <TextField
                label="Project description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                minRows={3}
                maxRows={6}
            />
            <Box mt={3} display="flex" justifyContent="flex-end">
                <Button type="submit" variant="contained" color="primary">
                    Create Project
                </Button>
            </Box>
        </Box>
    );
};

export default NewProjectForm;
