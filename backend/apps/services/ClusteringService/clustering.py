from sklearn.cluster import AgglomerativeClustering
import numpy as np
from typing import List

from models.models import OCRTextItem


def cluster_ocr_items(ocr_items: List[OCRTextItem], distance_threshold=100):
    """
    Cluster OCR items spatially by their bounding box centers.
    distance_threshold: max pixels to consider items in same cluster.
    """
    if not ocr_items:
        return []

    # Compute centers of bounding boxes
    centers = np.array(
        [
            [
                item.bounding_box.x + item.bounding_box.width / 2,
                item.bounding_box.y + item.bounding_box.height / 2,
            ]
            for item in ocr_items
        ]
    )

    clustering = AgglomerativeClustering(
        n_clusters=None, distance_threshold=distance_threshold, linkage="single"
    ).fit(centers)

    clusters = {}
    for label, item in zip(clustering.labels_, ocr_items):
        clusters.setdefault(label, []).append(item)

    return list(clusters.values())


def merge_cluster_text(cluster):
    # Sort by left x
    sorted_items = sorted(cluster, key=lambda item: item.bounding_box.x)
    merged_text = ""
    prev_x_end = None
    for item in sorted_items:
        x_start = item.bounding_box.x
        if prev_x_end is not None:
            gap = x_start - prev_x_end
            if gap > 10:  # threshold for adding space
                merged_text += " "
        merged_text += item.text
        prev_x_end = x_start + item.bounding_box.width
    return merged_text


def cluster_by_line(
    ocr_items: List[OCRTextItem], y_tolerance: int = 10, x_gap_threshold: int = 60
):
    """
    Clusters OCR items that appear on the same horizontal line.

    Args:
        ocr_items: list of OCRTextItem
        y_tolerance: vertical pixel range to consider items in the same line
        x_gap_threshold: max horizontal gap between words to consider them part of the same phrase
    Returns:
        List of clusters, each being a list of OCRTextItem objects
    """
    # Sort top-to-bottom, then left-to-right
    sorted_items = sorted(
        ocr_items, key=lambda item: (item.bounding_box.y, item.bounding_box.x)
    )

    lines = []
    current_line = []

    for item in sorted_items:
        if not current_line:
            current_line.append(item)
            continue

        last = current_line[-1]
        y_diff = abs(item.bounding_box.y - last.bounding_box.y)

        if y_diff <= y_tolerance:
            current_line.append(item)
        else:
            lines.append(current_line)
            current_line = [item]
    if current_line:
        lines.append(current_line)

    # Within each line, split into horizontal word groups if too far apart
    clustered_phrases = []
    for line in lines:
        phrase = [line[0]]
        for i in range(1, len(line)):
            prev = phrase[-1]
            curr = line[i]
            gap = curr.bounding_box.x - (prev.bounding_box.x + prev.bounding_box.width)
            if gap < x_gap_threshold:
                phrase.append(curr)
            else:
                clustered_phrases.append(phrase)
                phrase = [curr]
        if phrase:
            clustered_phrases.append(phrase)

    return clustered_phrases
