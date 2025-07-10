import os
import sys
import json

# Add backend and backend/apps to sys.path for module resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "..", ".."))
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

from services.VectorizerService.main import process_page, OCRPage


def test_process_vectorized_output(json_path, num_images=10):
    """
    Processes the first num_images pages from a vectorized_output.json file using the service logic directly.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    pages = data.get("pages", [])[:num_images]
    all_spaces = []
    for idx, page in enumerate(pages):
        ocr_page = OCRPage(**page)
        spaces = process_page(ocr_page)
        all_spaces.extend(spaces)
        print(f"Processed page {idx+1}: {len(spaces)} spaces found.")
    print(f"Total spaces found: {len(all_spaces)}")
    print(json.dumps(all_spaces, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # Example: process first 10 images from ocr_batch_output.json using service logic
    test_process_vectorized_output("ocr_batch_output.json", num_images=10)
