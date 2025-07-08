import fitz  # PyMuPDF
from typing import List, Dict, Any, Optional
from apps.models.models import (
    VectorizedPDFResponse,
    Line,
    TextElement,
    PathElement,
    ScaleInfo,
)
import re


class VectorizerService:
    def extract_scale_by_reconstructing_lines(self, page) -> Optional[str]:
        """Reconstruct lines from word-level OCR and search for scale patterns."""
        words = page.get_text(
            "words"
        )  # [x0, y0, x1, y1, word, block_no, line_no, word_no]
        lines = {}
        for w in words:
            y0 = round(w[1], 1)
            lines.setdefault(y0, []).append(w)
        scale_pattern = re.compile(
            r'SCALE[:\s]*[\d/]+"?\s*=\s*[\d\'\-"]+', re.IGNORECASE
        )
        for y, line_words in lines.items():
            sorted_words = sorted(line_words, key=lambda w: w[0])
            full_line = " ".join(w[4] for w in sorted_words)
            if scale_pattern.search(full_line):
                print(f"[DEBUG] Found scale on reconstructed line y={y}: {full_line}")
                return full_line
        return None

    # Neo4j logic removed; this service is now stateless and only extracts data.

    def is_vector_pdf(self, doc: fitz.Document) -> bool:
        for page in doc:
            if page.get_drawings() or page.get_text("dict")["blocks"]:
                return True
        return False

    def extract_lines(self, page) -> List[Line]:
        lines = []
        for drawing in page.get_drawings():
            for item in drawing["items"]:
                if item[0] == "l":  # line
                    _, p1, p2 = item
                    lines.append(Line(start=list(p1), end=list(p2)))
        return lines

    def extract_paths(self, page) -> List[PathElement]:
        paths = []
        for drawing in page.get_drawings():
            for item in drawing["items"]:
                if item[0] == "p":  # path
                    _, points = item
                    paths.append(PathElement(points=[list(pt) for pt in points]))
        return paths

    def extract_texts(self, page) -> List[TextElement]:
        texts = []
        for block in page.get_text("dict")["blocks"]:
            if block["type"] == 0:  # text
                for line in block["lines"]:
                    for span in line["spans"]:
                        texts.append(
                            TextElement(
                                text=span["text"],
                                position=[span["bbox"][0], span["bbox"][1]],
                                font_size=span.get("size"),
                                bbox=list(span["bbox"]),
                            )
                        )
        return texts

    def extract_scale(self, page) -> Optional[ScaleInfo]:
        # Scan all text for scale patterns (original method)
        texts = [
            span["text"]
            for block in page.get_text("dict")["blocks"]
            if block["type"] == 0
            for line in block["lines"]
            for span in line["spans"]
        ]
        page_text = " ".join(texts)
        print(f"[DEBUG] Page {page.number + 1} combined text: {page_text}")
        # Try to match patterns like "SCALE: 1/8\" = 1'-0\""
        match = re.search(
            r"scale[:\s]*([\d/\.]+)[\"”']?\s*=\s*([\d'\-\.]+)", page_text, re.IGNORECASE
        )
        if match:
            print(f"[DEBUG] Matched scale pattern: {match.group(0)}")
            # Parse the scale value if possible
            left = match.group(1)
            right = match.group(2)
            # Try to parse architectural scale (e.g., 1/8" = 1'-0")
            arch_match = re.match(r"(\d+)/(\d+)", left)
            if arch_match:
                left_decimal = float(arch_match.group(1)) / float(arch_match.group(2))
            else:
                try:
                    left_decimal = float(left)
                except Exception:
                    left_decimal = None
            # Parse right side (e.g., 1'-0")
            right_feet = 0.0
            right_inches = 0.0
            right_match = re.match(r"(\d+)'[- ]?(\d+)?", right)
            if right_match:
                right_feet = float(right_match.group(1))
                if right_match.group(2):
                    right_inches = float(right_match.group(2))
            else:
                try:
                    right_inches = float(right)
                except Exception:
                    right_inches = 0.0
            right_total_inches = right_feet * 12 + right_inches
            ratio = (
                right_total_inches / left_decimal
                if left_decimal and left_decimal > 0
                else None
            )
            return ScaleInfo(units="feet", ratio=ratio)
        # Fallback to your old patterns
        match = re.search(r"scale\s*1[:=]\s*(\d+)", page_text, re.IGNORECASE)
        if match:
            ratio = float(match.group(1))
            print(f"[DEBUG] Matched scale pattern: {match.group(0)}")
            return ScaleInfo(units=None, ratio=ratio)
        match = re.search(r"1[\"] ?= ?(\d+)[\']", page_text)
        if match:
            ratio = float(match.group(1))
            print(f"[DEBUG] Matched scale pattern: {match.group(0)}")
            return ScaleInfo(units="feet", ratio=ratio)

        # Fallback: Try reconstructing lines from words and searching for scale
        reconstructed_line = self.extract_scale_by_reconstructing_lines(page)
        if reconstructed_line:
            # Try to extract the scale value from the reconstructed line
            match = re.search(
                r'(\d+/\d+|\d+\.?\d*)["\']?\s*=\s*(\d+)[\'\-]?(\d+)?["\']?',
                reconstructed_line,
            )
            if match:
                left = match.group(1)
                right_feet = match.group(2)
                right_inches = match.group(3) if match.group(3) else "0"
                print(
                    f'[DEBUG] Found architectural scale (reconstructed): {left}" = {right_feet}\'-{right_inches}" in: {reconstructed_line}'
                )
                if "/" in left:
                    numerator, denominator = left.split("/")
                    left_decimal = float(numerator) / float(denominator)
                else:
                    left_decimal = float(left)
                right_total_inches = float(right_feet) * 12 + float(right_inches)
                ratio = right_total_inches / left_decimal if left_decimal > 0 else None
                return ScaleInfo(units="feet", ratio=ratio)
        return None

    def find_scale_by_proximity(
        self, project_id: str, page_number: int
    ) -> Optional[ScaleInfo]:
        """Find scale by looking for text elements near 'SCALE:' text"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (p:Project {id: $project_id})-[:HAS_TEXT]->(scale_node:TextElement),
                      (p)-[:HAS_TEXT]->(nearby:TextElement)
                WHERE toLower(scale_node.text) CONTAINS "scale"
                AND scale_node <> nearby
                AND abs(scale_node.position[0] - nearby.position[0]) < 400
                AND abs(scale_node.position[1] - nearby.position[1]) < 100
                RETURN scale_node.text as scale_text, 
                       nearby.text as nearby_text,
                       scale_node.position as scale_pos,
                       nearby.position as nearby_pos,
                       sqrt((scale_node.position[0] - nearby.position[0])^2 + 
                            (scale_node.position[1] - nearby.position[1])^2) as distance
                ORDER BY distance
                LIMIT 10
            """,
                project_id=project_id,
            )

            for record in result:
                nearby_text = record["nearby_text"]
                distance = record["distance"]
                print(
                    f"[DEBUG] Found text near SCALE (distance={distance:.1f}): '{nearby_text}' pos={record['nearby_pos']} scale_pos={record['scale_pos']}"
                )

                # Skip if nearby_text is just 'SCALE:' (case-insensitive, with or without trailing punctuation/whitespace)
                if re.match(r"^\s*scale\s*[:\-]?\s*$", nearby_text, re.IGNORECASE):
                    continue

                # Improved: Find all scale patterns in the string, not just if it's the whole string
                scale_matches = re.findall(
                    r'(\d+/\d+|\d+\.?\d*)["\']?\s*=\s*(\d+)[\'\-]?(\d+)?["\']?',
                    nearby_text,
                )
                if scale_matches:
                    left, right_feet, right_inches = scale_matches[0]
                    if not right_inches:
                        right_inches = "0"
                    print(
                        f'[DEBUG] Found architectural scale: {left}" = {right_feet}\'-{right_inches}" in: {nearby_text}'
                    )
                    # Calculate ratio (convert left fraction to decimal, convert right to inches)
                    if "/" in left:
                        numerator, denominator = left.split("/")
                        left_decimal = float(numerator) / float(denominator)
                    else:
                        left_decimal = float(left)
                    right_total_inches = float(right_feet) * 12 + float(right_inches)
                    ratio = (
                        right_total_inches / left_decimal if left_decimal > 0 else None
                    )
                    return ScaleInfo(units="feet", ratio=ratio)

                # Check for other scale patterns
                match = re.search(r"(\d+)\s*[:=]\s*(\d+)", nearby_text)
                if match:
                    ratio = float(match.group(2))
                    print(f"[DEBUG] Found ratio scale: 1:{ratio}")
                    return ScaleInfo(units=None, ratio=ratio)

        return None

    def vectorize_pdf(self, pdf_bytes: bytes) -> VectorizedPDFResponse:
        from apps.models.models import PageScaleInfo, ScaleInfo

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        if not self.is_vector_pdf(doc):
            return VectorizedPDFResponse(
                lines=[], texts=[], paths=[], scales=[], fallback=True
            )
        lines, texts, paths = [], [], []
        page_scales: list = []
        for i, page in enumerate(doc, start=1):
            lines.extend(self.extract_lines(page))
            texts.extend(self.extract_texts(page))
            paths.extend(self.extract_paths(page))
            scale = self.extract_scale(page)
            if scale:
                page_scales.append(PageScaleInfo(page=i, scale=scale, nts=False))
            else:
                page_scales.append(PageScaleInfo(page=i, scale=None, nts=True))
        # No storage: just return the extracted data
        return VectorizedPDFResponse(
            lines=lines, texts=texts, paths=paths, scales=page_scales, fallback=False
        )
