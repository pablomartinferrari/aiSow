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

from services.VectorizerService.services.vectorizer import VectorizerService


def batch_ocr_images(image_folder, output_json="ocr_batch_output.json", max_images=10):
    # Collect image files (common formats)
    image_files = [
        f
        for f in os.listdir(image_folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"))
    ]
    image_files = sorted(image_files)[:max_images]
    image_paths = [os.path.join(image_folder, f) for f in image_files]
    print(f"Processing {len(image_paths)} images: {image_files}")

    vectorizer = VectorizerService()
    result = vectorizer.vectorize_images(image_paths)

    # Save output
    output_path = os.path.join(image_folder, output_json)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"OCR batch output saved to {output_path}")


if __name__ == "__main__":
    batch_ocr_images(os.path.dirname(__file__))
