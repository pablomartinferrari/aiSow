# AI SOW OCR Service

A Python-based OCR service using FastAPI and EasyOCR for processing PDFs and images to extract text.

## Features

- PDF to image conversion using PyMuPDF
- Text extraction using EasyOCR
- Support for multiple languages
- RESTful API endpoints
- Docker support
- Health check endpoint

## Setup

### Prerequisites

- Python 3.11+
- Docker (optional)

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
python main.py
```

The service will be available at `http://localhost:8000`

### Docker

1. Build the image:
```bash
docker build -t ai-sow-ocr-service .
```

2. Run the container:
```bash
docker run -p 8000:8000 ai-sow-ocr-service
```

## API Endpoints

### Health Check
- `GET /health` - Check if the service is running

### Supported Languages
- `GET /languages` - Get list of supported languages

### Process PDF
- `POST /process-pdf` - Process PDF file and extract text
  - Parameters:
    - `file`: PDF file (multipart/form-data)
    - `language`: Language code (default: "en")
    - `extract_tables`: Extract tables (default: false)
    - `extract_images`: Extract images (default: false)
    - `page_number`: Specific page to process (optional)

### Process Image
- `POST /process-image` - Process image file and extract text
  - Parameters:
    - `file`: Image file (multipart/form-data)
    - `language`: Language code (default: "en")

## Example Usage

### Using curl

```bash
# Process a PDF
curl -X POST "http://localhost:8000/process-pdf" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "language=en"

# Process an image
curl -X POST "http://localhost:8000/process-image" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg" \
  -F "language=en"
```

### Using Python requests

```python
import requests

# Process PDF
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    data = {'language': 'en'}
    response = requests.post('http://localhost:8000/process-pdf', files=files, data=data)
    result = response.json()
    print(result)

# Process image
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    data = {'language': 'en'}
    response = requests.post('http://localhost:8000/process-image', files=files, data=data)
    result = response.json()
    print(result)
```

## Response Format

```json
{
  "filename": "document.pdf",
  "pages": [
    {
      "page_number": 1,
      "text": "Extracted text content...",
      "confidence": 0.95,
      "tables": [],
      "images": []
    }
  ],
  "processing_time": {
    "total_seconds": 2.5,
    "pdf_to_image_seconds": 0.8,
    "ocr_seconds": 1.7
  },
  "status": "Completed"
}
```

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)

## Configuration

The service can be configured by modifying the following in `main.py`:

- OCR reader initialization
- Image preprocessing settings
- API endpoints and middleware
- CORS settings

## Dependencies

- FastAPI - Web framework
- Uvicorn - ASGI server
- EasyOCR - OCR engine
- PyMuPDF - PDF processing
- Pillow - Image processing
- NumPy - Numerical computing
- OpenCV - Computer vision
- PyTorch - Deep learning framework 