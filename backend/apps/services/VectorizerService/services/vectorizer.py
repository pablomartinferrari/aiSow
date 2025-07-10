import pytesseract
from PIL import Image


class VectorizerService:
    def ocr_image(self, image_path: str) -> dict:
        """
        Run Tesseract OCR on an image and return word-level results with bounding boxes.
        """
        img = Image.open(image_path)
        ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        words = []
        n_boxes = len(ocr_data["level"])
        for i in range(n_boxes):
            if ocr_data["text"][i].strip() == "":
                continue
            word = {
                "text": ocr_data["text"][i],
                "left": ocr_data["left"][i],
                "top": ocr_data["top"][i],
                "width": ocr_data["width"][i],
                "height": ocr_data["height"][i],
                "conf": ocr_data["conf"][i],
                "line_num": ocr_data["line_num"][i],
                "block_num": ocr_data["block_num"][i],
                "par_num": ocr_data["par_num"][i],
            }
            words.append(word)
        return {"words": words}

    def group_words_by_line(self, words: list) -> list:
        """
        Group OCR words into lines based on their line_num and block_num.
        """
        from collections import defaultdict

        lines = defaultdict(list)
        for word in words:
            key = (word["block_num"], word["par_num"], word["line_num"])
            lines[key].append(word)
        grouped_lines = []
        for key, line_words in lines.items():
            # Sort words left-to-right
            line_words = sorted(line_words, key=lambda w: w["left"])
            line_text = " ".join(w["text"] for w in line_words)
            bbox = [
                min(w["left"] for w in line_words),
                min(w["top"] for w in line_words),
                max(w["left"] + w["width"] for w in line_words),
                max(w["top"] + w["height"] for w in line_words),
            ]
            grouped_lines.append(
                {
                    "text": line_text,
                    "words": line_words,
                    "bbox": bbox,
                    "block_num": key[0],
                    "par_num": key[1],
                    "line_num": key[2],
                }
            )
        # Sort lines top-to-bottom
        grouped_lines = sorted(
            grouped_lines, key=lambda l: (l["bbox"][1], l["bbox"][0])
        )
        return grouped_lines

    def vectorize_images(self, image_paths: list) -> dict:
        """
        For each image path, run Tesseract OCR, group words into lines, and return results as JSON.
        """
        results = []
        for idx, image_path in enumerate(image_paths):
            ocr_result = self.ocr_image(image_path)
            lines = self.group_words_by_line(ocr_result["words"])
            results.append(
                {
                    "image_path": image_path,
                    "page": idx + 1,
                    "lines": lines,
                }
            )
        return {"pages": results}
