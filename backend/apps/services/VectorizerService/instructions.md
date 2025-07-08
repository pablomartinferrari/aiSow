# GitHub Issue: Add Vectorization Support for Floor Plan PDFs



### Title: Implement PDF Vectorization Service for Structured Floor Plan Extraction



### Description:

Currently, the system converts floor plan PDFs into raster images and uses OCR and image processing to extract text and geometry. This approach is effective for image-based plans but lacks precision and structural metadata available in vector-based PDFs.



This issue aims to introduce a new service that detects and processes vector-based PDFs to extract:



Geometric primitives (lines, paths, shapes)
Text labels and positions
Scale and coordinate information




By vectorizing the plan, we enable precise measurement, room detection, and real-world scale awareness.

🎯 

### **Acceptance Criteria**


**Vector PDF Detection**
Determine whether the input PDF is vector-based or image-based.
Route to vector pipeline only if vector content is found.

**Line and Path Extraction**
Extract all straight lines and paths representing walls, boundaries, or architectural features.
Include coordinates and lengths.
Identify closed polygons that could represent rooms.

**Text Extraction**
Extract all vector-based text elements.
Capture:
Text content
Coordinates (x, y)
Font size or bounding box


**Scale Inference**
Extract drawing scale from title blocks, embedded metadata, or known geometry (e.g., labeled measurements).
Store unit information (e.g., 1 unit = 1 ft or 1 cm).

Structured Output Format
Return vector data in a structured JSON format:


``` JSON
{

  "lines": [{ "start": [x, y], "end": [x, y] }],

  "texts": [{ "text": "Room A", "position": [x, y], "font_size": 10 }],

  "paths": [{ "points": [[x1, y1], [x2, y2], ...] }],

  "scale": { "units": "feet", "ratio": 1.0 }

}

```


**Fallback Handling**
If PDF has no vector content, gracefully fall back to existing OCR/image-based processing.

**Integration Test**
Add a test vector PDF file with known geometry and labels.
Assert correct extraction of key text and shapes.
