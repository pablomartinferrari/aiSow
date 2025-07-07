Great! Since your existing service already returns OCR-labeled text with bounding boxes like:

```json
{
    "text": "Room D",
    "bounding_box": {"x": 3574, "y": 2383, "width": 384, "height": 111}
}
```

We can **update the GitHub issue** to reflect that you want to **enhance your current OCR service** by incorporating **structural analysis of floor plans**, and then correlate the OCR results with detected geometric features.

---

### **📌 Title: Enhance OCR Service to Detect and Measure Floor Plan Geometry**

### **📝 Description:**

The OCR service currently extracts labeled text and bounding boxes from floor plans. We want to **extend this capability** to include:

* Detection of **walls** (via line detection)
* Detection of **room boundaries** (via contour detection)
* Optional **real-world measurement output** if a scale is provided (e.g., pixels per meter)
* **Association of OCR labels** with detected rooms by checking if the label’s center lies inside a room contour

This enhancement will allow the system to not only identify labeled rooms, but also compute room sizes, identify layout structure, and eventually support dimensioned outputs for audit and compliance use cases.

### **🔧 Inputs:**

OCR already provides:

```json
{
  "text": "Room D",
  "bounding_box": { "x": 3574, "y": 2383, "width": 384, "height": 111 }
}
```

This should be extended to associate that bounding box with a specific detected room polygon.

### **✅ Acceptance Criteria:**

* [ ] Use OpenCV `HoughLinesP` to detect straight lines (walls)
* [ ] Use OpenCV `findContours` to detect room boundaries
* [ ] Associate each OCR label with a room shape using geometric containment
* [ ] Optional: compute real-world size from bounding boxes given a scale
* [ ] Return an enriched response that includes:

  * Room label
  * Room bounding box
  * Optional room size (meters)
  * Polygon points of the room contour
* [ ] Save debug overlays (lines, contours, matched labels) for review

### **📁 Example Output:**

```json
{
  "label": "Room D",
  "bounding_box": { "x": 3574, "y": 2383, "width": 384, "height": 111 },
  "room_polygon": [[3500, 2300], [3950, 2300], [3950, 2500], [3500, 2500]],
  "real_size": { "width_m": 4.2, "height_m": 2.0 }
}
```

