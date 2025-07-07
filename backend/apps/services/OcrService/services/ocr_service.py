import easyocr
from models.models import OCRResponse, OCRTextItem, BoundingBox
from typing import List


class OcrService:
    def __init__(self):
        self.reader = easyocr.Reader(["en"])

    def process_image(self, image_bytes: bytes) -> OCRResponse:
        import numpy as np
        import cv2
        import io
        from PIL import Image

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_np = np.array(image)
        results = self.reader.readtext(image_np)

        ocr_items: List[OCRTextItem] = []
        for bbox, text, confidence in results:
            # bbox: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            x_coords = [point[0] for point in bbox]
            y_coords = [point[1] for point in bbox]
            x = int(min(x_coords))
            y = int(min(y_coords))
            width = int(max(x_coords) - x)
            height = int(max(y_coords) - y)
            ocr_items.append(
                OCRTextItem(
                    text=text,
                    bounding_box=BoundingBox(x=x, y=y, width=width, height=height),
                    confidence=float(confidence),
                )
            )
        return OCRResponse(results=ocr_items)
