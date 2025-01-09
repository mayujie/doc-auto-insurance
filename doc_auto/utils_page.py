from typing import Optional, Union

import fitz  # PyMuPDF
import numpy as np
from PyPDF2 import PdfReader

from doc_auto.utils_log import setup_logger

logger = setup_logger(__name__)


def identify_empty_pages(pdf_path: str):
    reader = PdfReader(pdf_path)
    empty_pages = []

    for i, page in enumerate(reader.pages):
        # Extracts the text content of each page.
        text = page.extract_text()
        # Removes any leading or trailing whitespace to detect genuinely empty pages.
        if not text or text.strip() == "":
            # Adds the page number (1-indexed) to the result list.
            empty_pages.append(i + 1)  # Page numbers start from 1

    return empty_pages


def identify_blank_pages(pdf_path: Optional[str] = None, document: Optional[fitz.Document] = None,
                         threshold=0.99) -> Union[int, None, list]:
    """
    Identify blank pages in a PDF by analyzing rendered content.

    Args:
        pdf_path (str): Path to the PDF file.
        threshold (float): Fraction of white pixels to classify as blank. Default is 0.99.

    Returns:
        list: List of 1-based page numbers that are blank.
    """
    blank_pages = []
    if document is None:
        doc = fitz.open(pdf_path)
    else:
        doc = document

    for page_number in range(len(doc)):
        page = doc[page_number]
        pix = page.get_pixmap()  # Render the page as an image
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

        # Convert to grayscale
        if img.shape[2] == 4:  # RGBA
            img = img[:, :, :3]  # Drop alpha channel
        gray_img = np.mean(img, axis=2)

        # Calculate the proportion of near-white pixels
        white_pixels = np.sum(gray_img > 250)  # Threshold for near-white
        total_pixels = gray_img.size
        white_fraction = white_pixels / total_pixels

        if white_fraction > threshold:
            blank_pages.append(page_number + 1)  # Page numbers are 1-based

    if blank_pages:
        logger.info(f"Blank pages found: {blank_pages}")
        if len(blank_pages) == 1:
            return blank_pages[0]
        else:
            return blank_pages
    else:
        logger.warning("No blank pages found.")
        return None
