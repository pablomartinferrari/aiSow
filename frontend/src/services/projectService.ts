import api from '../utils/api';

export type Project = {
    id: string;
    name: string;
    description: string;
};

const API_ENDPOINT = '/api/projects';

export async function fetchProjects(): Promise<Project[]> {
    const res = await api.get(API_ENDPOINT);
    return res.data;
}

export async function createProject(project: Omit<Project, 'id'>): Promise<Project> {
    const res = await api.post(API_ENDPOINT, project);
    return res.data;
}

export async function getProject(id: string): Promise<Project> {
    const res = await api.get(`${API_ENDPOINT}/${id}`);
    return res.data;
}

export async function updateProject(project: Project): Promise<Project> {
    const res = await api.put(`${API_ENDPOINT}/${project.id}`, project);
    return res.data;
}

export async function deleteProject(id: string): Promise<void> {
    await api.delete(`${API_ENDPOINT}/${id}`);
}
