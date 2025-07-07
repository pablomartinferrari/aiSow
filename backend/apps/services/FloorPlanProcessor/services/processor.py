import cv2
import numpy as np
from typing import List, Dict, Optional
from models.models import (
    FloorPlanProcessorResponse,
    RoomLabelResult,
    BoundingBox,
    RoomPolygon,
    RealSize,
)


class FloorPlanProcessor:
    def __init__(self, scale: Optional[float] = None):
        self.scale = scale  # pixels per meter, if provided

    def process(
        self, image: np.ndarray, ocr_results: List[Dict]
    ) -> FloorPlanProcessorResponse:
        debug_images = {}
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

        # Wall detection (lines)
        lines = cv2.HoughLinesP(
            edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10
        )
        line_img = image.copy()
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        debug_images["walls"] = self._save_debug_image(line_img, "walls.png")

        # Room boundary detection (contours)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contour_img = image.copy()
        cv2.drawContours(contour_img, contours, -1, (255, 0, 0), 2)
        debug_images["contours"] = self._save_debug_image(contour_img, "contours.png")

        rooms = []
        for ocr in ocr_results:
            label = ocr["text"]
            bbox = ocr["bounding_box"]
            confidence = ocr.get("confidence", None)
            center = (bbox["x"] + bbox["width"] // 2, bbox["y"] + bbox["height"] // 2)
            matched_polygon = None
            for contour in contours:
                if cv2.pointPolygonTest(contour, center, False) >= 0:
                    matched_polygon = contour.squeeze().tolist()
                    break
            real_size = None
            if matched_polygon and self.scale:
                x_coords = [pt[0] for pt in matched_polygon]
                y_coords = [pt[1] for pt in matched_polygon]
                width_m = (max(x_coords) - min(x_coords)) / self.scale
                height_m = (max(y_coords) - min(y_coords)) / self.scale
                real_size = RealSize(width_m=width_m, height_m=height_m)
            rooms.append(
                RoomLabelResult(
                    label=label,
                    bounding_box=BoundingBox(**bbox),
                    room_polygon=RoomPolygon(
                        points=matched_polygon if matched_polygon else []
                    ),
                    real_size=real_size,
                    confidence=confidence,
                )
            )
        return FloorPlanProcessorResponse(rooms=rooms, debug_images=debug_images)

    def _save_debug_image(self, img, filename):
        cv2.imwrite(filename, img)
        return filename
