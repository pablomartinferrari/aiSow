import json

with open("structured_ocr_output.json", "r", encoding="utf-8") as f:
    ocr_data = json.load(f)

# Example: print all detected text
for item in ocr_data:
    print(f"Text: {item['text']} | Score: {item['score']} | Box: {item['box']}")
