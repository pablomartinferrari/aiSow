# Floor Plan OCR Service

This service provides Optical Character Recognition (OCR) for floor plan images. It extracts text labels, their bounding boxes, and confidence scores from uploaded images (PNG, JPG, etc.).

## Features
- Accepts floor plan images via REST API
- Returns detected text, bounding box (x, y, width, height), and confidence for each label
- Easy integration with other microservices

## API Usage

### Start the Service

```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```
Or, if using a virtual environment:
```sh
c:/dev/ai-sow/.venv/Scripts/python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### OCR Endpoint

**POST** `/api/v1/ocr`

- **Request:** Multipart form with an image file (PNG, JPG, JPEG, BMP, TIFF)
- **Response:**
```json
{
  "results": [
    {
      "text": "Room A",
      "bounding_box": {"x": 100, "y": 200, "width": 80, "height": 30},
      "confidence": 0.98
    },
    ...
  ]
}
```

## Testing

Sample test scripts are in the `tests/` folder. To run a test:

```sh
python tests/tests.py
```

## Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- EasyOCR
- Pillow
- numpy
- requests (for tests)

Install dependencies:
```sh
pip install -r requirements.txt
```

## Customization
- Adjust OCR parameters in `services/ocr_service.py` as needed.
- Update test cases in `tests/` to match your floor plan labels.

## License
MIT
