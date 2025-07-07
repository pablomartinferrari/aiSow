# aiSow

**aiSow** is an AI-powered system that processes architectural plans (PDFs), extracts spatial and measurement data, and generates structured **Scope of Work (SOW)** documents—linked to construction codes and exportable to Bluebeam-compatible formats.

---

## 🚀 Key Features

- 🧱 Upload vector or scanned architectural PDFs
- 📐 Extract room names, dimensions, and scales
- 🧠 Use AI to parse construction elements and functions
- 📋 Generate structured Scope of Work documents
- ⚖️ Link items with local/national code compliance
- 🔍 Visual validation with overlays (PDF/SVG/Bluebeam)
- 🔗 API integration ready for Procore, Autodesk, etc.

---

## 🧰 Tech Stack

- **Backend**: .NET Core (Project Management Service), Python (FastAPI - Pdf2Image Service)
- **AI/ML**: GPT-4 / Claude, EasyOCR, RAG + Embeddings
- **Frontend**: React / TypeScript / Vite
- **Storage**: SQL Server (Entity Framework), AWS S3 or Azure Blob
- **Export**: PDF, Word, SVG

## 🔧 Services

### Project Management Service (.NET Core)
- User authentication and authorization
- Project CRUD operations
- Document management
- RESTful API endpoints

### Pdf2Image Service (Python/FastAPI)
- **Current functionality**: PDF to image conversion using PyMuPDF
- **Planned extensions**: Text extraction with EasyOCR, multi-language support, table extraction
- **API endpoints**: `/api/v1/process-pdf`, `/api/v1/process-image`, `/api/v1/health`
- **Docker support**: Containerized deployment ready

---

## 📌 Status

> 🔧 Early-stage development — core pipeline being implemented.

---

## ⚠️ License / Usage Notice

This project is **not licensed for public or commercial use**.  
All rights are reserved by the author. No permission is granted to use, copy, modify, or distribute any part of this repository or its contents for any purpose without explicit written consent.
