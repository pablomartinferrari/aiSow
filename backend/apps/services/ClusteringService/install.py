import os
from paddleocr import PaddleOCR

# === 1. Setup ===
# Path to your image file (update this as needed)
image_path = (
    r"C:\dev\ai-sow\backend\apps\services\ClusteringService\pdfs\test_data-pages-1.pdf"
)

# Output folder
output_dir = "output_regular"
os.makedirs(output_dir, exist_ok=True)

# === 2. Initialize PaddleOCR ===
ocr = PaddleOCR(
    use_textline_orientation=False,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    lang="en",
)

# === 3. Run OCR Prediction ===
print(f"\n--- OCR Predicting  {os.path.basename(image_path)} ---")
results = ocr.predict(input=image_path)


# === 4. Save Results ===
# Visualize the results and save the JSON results
print(f"\n--- OCR Result ---")
for res in results:
    res.print()
    res.save_to_img("output")
    res.save_to_json("output")
# for i, res in enumerate(results):
#     print(f"\n--- OCR Result {i} ---")
#     res.print()

#     # Save visualized image
#     image_save_path = os.path.join(output_dir, f"result_{i}.jpg")
#     res.save_to_img(image_save_path)
#     print(f"Saved annotated image to: {image_save_path}")

#     # Save JSON data
#     json_save_path = os.path.join(output_dir, f"result_{i}.json")
#     res.save_to_json(json_save_path)
#     print(f"Saved JSON data to: {json_save_path}")
