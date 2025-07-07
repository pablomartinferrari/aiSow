import io
import os
import time
from pdf2image import convert_from_bytes
from PIL import Image
import numpy as np
from typing import List, Optional
from fastapi import HTTPException

from models.models import Pdf2ImageResponse


class PdfToImageService:
    """Service for converting PDF files to images"""

    async def process_pdf(
        self,
        file_content: bytes,
        filename: str,
        page_number: Optional[int] = None,
    ) -> Pdf2ImageResponse:
        """
        Convert PDF file to images and save them to disk.

        Args:
            file_content: PDF file content as bytes
            filename: Original filename
            page_number: Specific page to process (None for all pages)

        Returns:
            dict with image file paths and metadata
        """
        start_time = time.time()

        try:
            from PyPDF2 import PdfReader
            from io import BytesIO

            # Get total pages using PyPDF2 (lightweight)
            pdf = PdfReader(BytesIO(file_content))
            total_pages = len(pdf.pages)

            # Create output folder for images if it doesn't exist
            images_folder = "images"
            os.makedirs(images_folder, exist_ok=True)

            image_paths = []
            pdf_to_image_time = 0

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

            for page_idx in pages_to_process:
                # Convert single page to image
                page_to_image_start = time.time()
                images = convert_from_bytes(
                    file_content,
                    dpi=600,
                    first_page=page_idx + 1,
                    last_page=page_idx + 1,
                )
                img = images[0]  # We only converted one page
                pdf_to_image_time += time.time() - page_to_image_start

                # Save the image to disk
                image_filename = (
                    f"{os.path.splitext(filename)[0]}_page_{page_idx + 1}.png"
                )
                image_path = os.path.join(images_folder, image_filename)
                img.save(image_path, "PNG")
                image_paths.append(image_path)

            total_time = time.time() - start_time

            return Pdf2ImageResponse(
                filename=filename,
                image_paths=image_paths,
                processing_time={
                    "total_seconds": total_time,
                    "pdf_to_image_seconds": pdf_to_image_time,
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
    ) -> Pdf2ImageResponse:
        """
        Process image file and extract text using OCR

        Args:
            file_content: Image file content as bytes
            filename: Original filename
            language: Language code for OCR

        Returns:
            Pdf2ImageResponse with extracted text and metadata
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

            return Pdf2ImageResponse(
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
