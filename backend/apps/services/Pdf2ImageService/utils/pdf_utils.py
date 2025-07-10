import fitz  # PyMuPDF
import io
from PIL import Image
import numpy as np
from typing import List, Tuple, Optional


def convert_pdf_to_images(
    pdf_stream: bytes, page_numbers: Optional[List[int]] = None
) -> List[np.ndarray]:
    """
    Convert PDF pages to images

    Args:
        pdf_stream: PDF file content as bytes
        page_numbers: List of page numbers to convert (1-based). If None, convert all pages.

    Returns:
        List of images as numpy arrays
    """
    images = []

    # Open PDF
    pdf_document = fitz.open(stream=io.BytesIO(pdf_stream), filetype="pdf")
    total_pages = len(pdf_document)

    # Determine which pages to process
    if page_numbers is None:
        pages_to_process = range(total_pages)
    else:
        pages_to_process = [
            p - 1 for p in page_numbers if 1 <= p <= total_pages
        ]  # Convert to 0-based

    for page_idx in pages_to_process:
        page = pdf_document[page_idx]

        # Convert page to image with high resolution
        mat = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
        img_data = mat.tobytes("png")

        # Convert to PIL Image and then to numpy array
        img = Image.open(io.BytesIO(img_data))
        img_array = np.array(img)

        images.append(img_array)

    pdf_document.close()
    return images


def extract_text_from_pdf(pdf_stream: bytes) -> str:
    """
    Extract text directly from PDF (without OCR)

    Args:
        pdf_stream: PDF file content as bytes

    Returns:
        Extracted text as string
    """
    text = []

    pdf_document = fitz.open(stream=io.BytesIO(pdf_stream), filetype="pdf")

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        page_text = page.get_text()
        text.append(f"--- Page {page_num + 1} ---")
        text.append(page_text)
        text.append("")

    pdf_document.close()
    return "\n".join(text)


def get_pdf_page_count(pdf_stream: bytes) -> int:
    """
    Get the number of pages in a PDF

    Args:
        pdf_stream: PDF file content as bytes

    Returns:
        Number of pages
    """
    pdf_document = fitz.open(stream=io.BytesIO(pdf_stream), filetype="pdf")
    page_count = len(pdf_document)
    pdf_document.close()
    return page_count


def preprocess_image_for_ocr(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image to improve OCR accuracy

    Args:
        image: Input image as numpy array

    Returns:
        Preprocessed image as numpy array
    """
    # Convert to grayscale if it's a color image
    if len(image.shape) == 3:
        # Convert RGB to grayscale
        gray = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
        image = gray.astype(np.uint8)

    # Apply basic preprocessing
    # You can add more preprocessing steps here:
    # - Noise reduction
    # - Contrast enhancement
    # - Deskewing
    # - Binarization

    return image
