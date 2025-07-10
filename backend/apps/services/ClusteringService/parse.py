import json

# Load the PaddleOCR result JSON
with open("output/result_0.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract relevant parts
boxes = data.get("dt_polys", [])
texts = data.get("rec_texts", [])
scores = data.get("rec_scores", [])

# Combine them into a structured format
structured_output = []
for box, text, score in zip(boxes, texts, scores):
    structured_output.append(
        {
            "text": text,
            "score": float(score),
            "box": [[float(x), float(y)] for x, y in box],
        }
    )

# Save structured output to JSON file
with open("structured_ocr_output.json", "w", encoding="utf-8") as f:
    json.dump(structured_output, f, ensure_ascii=False, indent=2)

print("✅ Parsed and saved structured OCR output to structured_ocr_output.json")
