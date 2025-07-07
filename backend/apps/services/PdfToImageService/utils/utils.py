from typing import List
from models.models import Pdf2ImageItem, BBox


def format_easyocr_result(results, confidence_threshold=0.80) -> List[Pdf2ImageItem]:
    """
    Convert EasyOCR results to structured OcrItem objects

    Args:
        results: EasyOCR detection results
        confidence_threshold: Minimum confidence score for 'ok' status

    Returns:
        List of OcrItem objects with structured data
    """
    formatted = []
    for bbox, text, confidence in results:
        x_coords = [point[0] for point in bbox]
        y_coords = [point[1] for point in bbox]
        x = min(x_coords)
        y = min(y_coords)
        width = max(x_coords) - x
        height = max(y_coords) - y

        formatted.append(
            Pdf2ImageItem(
                text=text,
                confidence=round(confidence, 4),
                bbox=BBox(
                    x=int(x),
                    y=int(y),
                    width=int(width),
                    height=int(height),
                ),
                status="low_confidence" if confidence < confidence_threshold else "ok",
            )
        )
    return formatted
