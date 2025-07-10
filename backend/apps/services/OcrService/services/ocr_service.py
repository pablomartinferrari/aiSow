import pytesseract
from PIL import Image
import io
import cv2
import numpy as np
from typing import List, Optional

from models.models import OCRResponse, OCRTextItem, BoundingBox


class OcrService:
    def __init__(self):
        pass  # No initialization needed for pytesseract

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Convert the image to grayscale and apply adaptive thresholding to improve OCR accuracy.
        """
        img = np.array(image)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 8
        )
        blur = cv2.medianBlur(thresh, 3)
        return Image.fromarray(blur)

    def process_image(
        self, image_bytes: bytes, min_confidence: float = 60.0
    ) -> OCRResponse:
        """
        Perform OCR on a given image byte stream, returning bounding boxes and text with confidence filtering.
        """
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        preprocessed_image = self.preprocess_image(image)

        custom_config = r"--oem 3 --psm 6"
        ocr_data = pytesseract.image_to_data(
            preprocessed_image,
            output_type=pytesseract.Output.DICT,
            config=custom_config,
        )

        ocr_items: List[OCRTextItem] = []
        n_boxes = len(ocr_data["level"])
        for i in range(n_boxes):
            text = ocr_data["text"][i].strip()
            conf = float(ocr_data["conf"][i])

            if not text or conf < min_confidence:
                continue

            x = int(ocr_data["left"][i])
            y = int(ocr_data["top"][i])
            width = int(ocr_data["width"][i])
            height = int(ocr_data["height"][i])

            ocr_items.append(
                OCRTextItem(
                    text=text,
                    bounding_box=BoundingBox(x=x, y=y, width=width, height=height),
                    confidence=conf,
                )
            )

        return OCRResponse(results=ocr_items)

    def draw_ocr_boxes(
        self,
        image_bytes: bytes,
        ocr_items: List[OCRTextItem],
        output_path: Optional[str] = None,
    ) -> Image.Image:
        """
        Draw OCR bounding boxes on the image for debugging.
        """
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = np.array(image)

        for item in ocr_items:
            bb = item.bounding_box
            cv2.rectangle(
                img, (bb.x, bb.y), (bb.x + bb.width, bb.y + bb.height), (0, 255, 0), 1
            )
            cv2.putText(
                img,
                item.text,
                (bb.x, bb.y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 0, 0),
                1,
            )

        debug_image = Image.fromarray(img)
        if output_path:
            debug_image.save(output_path)
        return debug_image
