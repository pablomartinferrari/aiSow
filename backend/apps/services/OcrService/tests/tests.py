import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # ...\OcrService\tests
OCRSERVICE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # ...\OcrService

if OCRSERVICE_DIR not in sys.path:
    sys.path.insert(0, OCRSERVICE_DIR)

from services.ocr_service import OcrService  # Import from services/ocr_service.py

IMAGE_FOLDER = os.path.join(BASE_DIR, "images")  # or adjust if images/ lives elsewhere
OUTPUT_FILE = os.path.join(BASE_DIR, "output.json")


def main():
    ocr_service = OcrService()
    results = {}

    for filename in sorted(os.listdir(IMAGE_FOLDER)):
        if filename.lower().endswith(".png"):
            image_path = os.path.join(IMAGE_FOLDER, filename)
            print(f"Processing: {image_path}")
            try:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()

                ocr_response = ocr_service.process_image(image_bytes)
                results[filename] = [
                    {
                        "text": item.text,
                        "bounding_box": {
                            "x": item.bounding_box.x,
                            "y": item.bounding_box.y,
                            "width": item.bounding_box.width,
                            "height": item.bounding_box.height,
                        },
                        "confidence": item.confidence,
                    }
                    for item in ocr_response.results
                ]
                print(f"✅ Success: {filename}")
            except Exception as e:
                print(f"❌ Failed: {filename} — {e}")
                results[filename] = {"error": str(e)}

    with open(OUTPUT_FILE, "w") as out_file:
        json.dump(results, out_file, indent=2)

    print(f"\n📝 OCR results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
