import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import DashboardPage from "./pages/DashboardPage";
import UploadPage from "./pages/UploadPage";
import PlanViewerPage from "./pages/PlanViewerPage";
import SOWPage from "./pages/SOWPage";

import ValidationPage from "./pages/ValidationPage";
import IntegrationsPage from "./pages/IntegrationsPage";
import SettingsPage from "./pages/SettingsPage";
import ProjectDetailsPage from "./pages/ProjectDetailsPage";

const App: React.FC = () => (
  <MainLayout>
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/upload" element={<UploadPage />} />
      <Route path="/projects/:projectId" element={<ProjectDetailsPage />} />
      <Route path="/plan-viewer" element={<PlanViewerPage />} />
      <Route path="/sow" element={<SOWPage />} />
      <Route path="/validation" element={<ValidationPage />} />
      <Route path="/integrations" element={<IntegrationsPage />} />
      <Route path="/settings" element={<SettingsPage />} />
    </Routes>
  </MainLayout>
);

export default App;
