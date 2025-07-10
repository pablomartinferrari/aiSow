import os
import sys
import json

# Add backend (for 'apps') and backend/apps (for 'services') to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

from services.OcrService.services.ocr_service import OcrService
from clustering import cluster_by_line, merge_cluster_text


IMAGE_FOLDER = os.path.join(BASE_DIR, "images")  # Folder with your test PNGs
OUTPUT_FILE = os.path.join(BASE_DIR, "output.json")


def main():
    ocr_service = OcrService()
    results = {}

    for filename in sorted(os.listdir(IMAGE_FOLDER)):
        if not filename.lower().endswith(".png"):
            continue

        image_path = os.path.join(IMAGE_FOLDER, filename)
        print(f"Processing {filename}...")
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        try:
            ocr_response = ocr_service.process_image(image_bytes)

            # Cluster OCR results spatially
            clusters = cluster_by_line(
                ocr_response.results, y_tolerance=15, x_gap_threshold=100
            )

            # Merge texts in each cluster
            merged_texts = []
            for cluster in clusters:
                merged = merge_cluster_text(cluster)
                merged_texts.append(
                    {
                        "text": merged,
                        "items_count": len(cluster),
                        # You can add bounding boxes, avg confidence here if needed
                    }
                )

            results[filename] = merged_texts
            print(f"✅ {filename}: {len(merged_texts)} clusters found")

        except Exception as e:
            print(f"❌ Failed on {filename}: {e}")
            results[filename] = {"error": str(e)}

    # Save all results to JSON
    with open(OUTPUT_FILE, "w") as out_file:
        json.dump(results, out_file, indent=2)

    print(f"\n📝 Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
