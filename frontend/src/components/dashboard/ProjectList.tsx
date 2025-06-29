import React from "react";
import { Link } from "react-router-dom";

export type Project = {
    id: string;
    name: string;
    description: string;
};

interface ProjectListProps {
    projects: Project[];
    onSelect: (project: Project) => void;
}



const tableStyle: React.CSSProperties = {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '1.5rem',
};

const thStyle: React.CSSProperties = {
    textAlign: 'left',
    padding: '0.75rem 0.5rem',
    borderBottom: '2px solid #eee',
    fontWeight: 600,
    fontSize: '1.05em',
};

const tdStyle: React.CSSProperties = {
    padding: '0.75rem 0.5rem',
    borderBottom: '1px solid #f0f0f0',
    verticalAlign: 'top',
};

const ProjectList: React.FC<ProjectListProps> = ({ projects, onSelect }) => (
    <div>
        <h2>Your Projects</h2>
        {projects.length === 0 ? (
            <p>No projects found.</p>
        ) : (
            <table style={tableStyle}>
                <thead>
                    <tr>
                        <th style={thStyle}>Project Name</th>
                        <th style={thStyle}>Description</th>
                    </tr>
                </thead>
                <tbody>
                    {projects.map((project) => (
                        <tr key={project.id}>
                            <td style={tdStyle}>
                                <Link
                                    to={`/projects/${project.id}`}
                                    style={{ color: '#232946', fontWeight: 600, textDecoration: 'underline', cursor: 'pointer' }}
                                    onClick={() => onSelect(project)}
                                >
                                    {project.name}
                                </Link>
                            </td>
                            <td style={tdStyle}>{project.description}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        )}
    </div>
);

export default ProjectList;
