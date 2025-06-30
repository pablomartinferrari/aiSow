export type Project = {
    id: string;
    name: string;
    description: string;
};

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api/projects';

export async function fetchProjects(): Promise<Project[]> {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error('Failed to fetch projects');
    return res.json();
}

export async function createProject(project: Omit<Project, 'id'>): Promise<Project> {
    const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(project),
    });
    if (!res.ok) throw new Error('Failed to create project');
    return res.json();
}

export async function getProject(id: string): Promise<Project> {
    const res = await fetch(`${API_URL}/${id}`);
    if (!res.ok) throw new Error('Failed to fetch project');
    return res.json();
}

export async function updateProject(project: Project): Promise<Project> {
    const res = await fetch(`${API_URL}/${project.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(project),
    });
    if (!res.ok) throw new Error('Failed to update project');
    return res.json();
}

export async function deleteProject(id: string): Promise<void> {
    const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete project');
}
