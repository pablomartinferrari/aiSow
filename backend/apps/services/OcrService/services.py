import io
import os
import time
from pdf2image import convert_from_bytes
from PIL import Image
import numpy as np
from typing import List, Optional
from fastapi import HTTPException

from models import PageResult, OcrResponse
from utils import format_easyocr_result


class OcrService:
    """Core OCR processing service"""

    def __init__(self, reader):
        self.reader = reader

    async def process_pdf(
        self,
        file_content: bytes,
        filename: str,
        language: str = "en",
        extract_tables: bool = False,
        extract_images: bool = False,
        page_number: Optional[int] = None,
    ) -> OcrResponse:
        """
        Process PDF file and extract text using OCR

        Args:
            file_content: PDF file content as bytes
            filename: Original filename
            language: Language code for OCR
            extract_tables: Whether to extract tables (not implemented)
            extract_images: Whether to extract images (not implemented)
            page_number: Specific page to process (None for all pages)

        Returns:
            OcrResponse with extracted text and metadata
        """
        start_time = time.time()

        try:
            # Convert PDF to images using pdf2image
            pdf_to_image_time = time.time()
            images = convert_from_bytes(
                file_content, dpi=200
            )  # 200 DPI for good quality
            pdf_to_image_time = time.time() - pdf_to_image_time

            # Create output folder for images if it doesn't exist
            images_folder = "images"
            os.makedirs(images_folder, exist_ok=True)

            pages = []
            total_pages = len(images)

            # Determine which pages to process
            if page_number is not None:
                if page_number > total_pages:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Page {page_number} does not exist. PDF has {total_pages} pages.",
                    )
                pages_to_process = [page_number - 1]  # 0-based indexing
            else:
                pages_to_process = range(total_pages)

            ocr_time = 0

            for page_idx in pages_to_process:
                # Get the page image
                img = images[page_idx]

                # Save the image to disk
                image_filename = (
                    f"{os.path.splitext(filename)[0]}_page_{page_idx + 1}.png"
                )
                image_path = os.path.join(images_folder, image_filename)
                img.save(image_path, "PNG")

                img_array = np.array(img)

                # Perform OCR
                ocr_start_time = time.time()
                results = self.reader.readtext(img_array)
                ocr_time += time.time() - ocr_start_time

                # Create page result with saved image path
                page_result = PageResult(
                    page_number=page_idx + 1,
                    items=format_easyocr_result(results),
                    tables=[],  # TODO: Implement table extraction
                    images=[image_path],  # store image file path
                )

                pages.append(page_result)

            total_time = time.time() - start_time

            return OcrResponse(
                filename=filename,
                pages=pages,
                processing_time={
                    "total_seconds": total_time,
                    "pdf_to_image_seconds": pdf_to_image_time,
                    "ocr_seconds": ocr_time,
                },
                status="Completed",
            )

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error processing PDF: {str(e)}"
            )

    async def process_image(
        self,
        file_content: bytes,
        filename: str,
        language: str = "en",
    ) -> OcrResponse:
        """
        Process image file and extract text using OCR

        Args:
            file_content: Image file content as bytes
            filename: Original filename
            language: Language code for OCR

        Returns:
            OcrResponse with extracted text and metadata
        """
        start_time = time.time()

        try:
            # Read image file
            img = Image.open(io.BytesIO(file_content))

            # Save the uploaded image to disk as well
            images_folder = "images"
            os.makedirs(images_folder, exist_ok=True)
            image_path = os.path.join(images_folder, filename)
            img.save(image_path)

            img_array = np.array(img)

            # Perform OCR
            ocr_start_time = time.time()
            results = self.reader.readtext(img_array)
            ocr_time = time.time() - ocr_start_time

            total_time = time.time() - start_time

            return OcrResponse(
                filename=filename,
                pages=[
                    PageResult(
                        page_number=1,
                        items=format_easyocr_result(results),
                        tables=[],
                        images=[image_path],  # store image path here as well
                    )
                ],
                processing_time={
                    "total_seconds": total_time,
                    "pdf_to_image_seconds": 0,
                    "ocr_seconds": ocr_time,
                },
                status="Completed",
            )

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error processing image: {str(e)}"
            )
