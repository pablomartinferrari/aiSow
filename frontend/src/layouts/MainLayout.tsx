import React, { ReactNode } from "react";
import { Link } from "react-router-dom";

const navItems = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/upload", label: "Upload" },
    { path: "/plan-viewer", label: "Plan Viewer" },
    { path: "/sow", label: "SOW" },
    { path: "/validation", label: "Validation" },
    { path: "/integrations", label: "Integrations" },
    { path: "/settings", label: "Settings" },
];

type MainLayoutProps = {
    children: ReactNode;
};

const MainLayout = ({ children }: MainLayoutProps) => (
    <div className="app-layout">
        <nav className="sidebar">
            <h2>aiSow</h2>
            <ul>
                {navItems.map((item) => (
                    <li key={item.path}>
                        <Link to={item.path}>{item.label}</Link>
                    </li>
                ))}
            </ul>
        </nav>
        <main className="main-content">{children}</main>
    </div>
);

export default MainLayout;