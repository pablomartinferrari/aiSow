# import os
# from paddleocr import PPStructure, save_structure_res
# from PIL import Image

# # === 1. Setup ===
# # Input image (your hotel layout)
# image_path = r"C:\dev\ai-sow\backend\apps\services\ClusteringService\images\test_data_page_9_resized.png"

# # Output folder
# output_dir = "output_structure"
# os.makedirs(output_dir, exist_ok=True)

# # === 2. Initialize PP-StructureV3 ===
# structure_engine = PPStructure(
#     show_log=True,
#     layout=True,  # Enable layout model
#     table=True,  # Enable table recognition (can disable if not needed)
#     ocr=True,  # Use OCR
#     lang="en",  # English language
# )

# # === 3. Load and process the image ===
# image = Image.open(image_path).convert("RGB")
# results = structure_engine(image)

# # === 4. Save structured results (layout, OCR, table, etc.) ===
# save_structure_res(results, output_dir, image_path)

# print(f"\n✅ Layout results saved to: {output_dir}")
# for i, item in enumerate(results):
#     print(f"\n--- Block {i} ---")
#     print("Type:", item.get("type", "unknown"))
#     print("Text:", item.get("text", ""))
#     print("Bounding Box:", item.get("bbox", []))
#     print("Confidence:", item.get("score", "N/A"))


from paddleocr import PPStructureV3

image_path = r"C:\dev\ai-sow\backend\apps\services\ClusteringService\images\test_data-pages-1.pdf"

pipeline = PPStructureV3(
    use_doc_orientation_classify=True,  # Enable document orientation classification
    use_doc_unwarping=True,  # Enable document unwarping
    text_recognition_model_name="en_PP-OCRv4_mobile_rec",
    use_textline_orientation=True,  # Enable textline orientation classification
)
output = pipeline.predict(image_path)
for res in output:
    res.print()  ## Print the structured prediction output
    res.save_to_json(
        save_path="output_pdf.json"
    )  ## Save the current image's structured result in JSON format
    res.save_to_markdown(
        save_path="output_pdf.md"
    )  ## Save the current image's result in Markdown format
