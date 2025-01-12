from typing import Optional, Union
import os
import cv2
import fitz  # PyMuPDF
import numpy as np
from PIL import Image, ImageOps
from PyPDF2 import PdfReader

from doc_auto.utils_img_op import crop_image
from doc_auto.utils_log import setup_logger
from doc_auto.utils_ocr import extract_important_info_by_ocr
from doc_auto.utils_ocr import extract_nr_rejestracyjny_by_ocr

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


def extract_info_from_page_by_ocr(doc: fitz.Document):
    page_number = 0
    page = doc[page_number]

    zoom_x = 2.0  # Horizontal zoom factor
    zoom_y = 2.0  # Vertical zoom factor
    matrix = fitz.Matrix(zoom_x, zoom_y)  # Scale the resolution
    pix = page.get_pixmap(matrix=matrix)  # Render the page with higher resolution

    # Convert pixmap to PIL Image
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # Crop the image
    cropped_img = crop_image(
        img=image,
        left_crop=50,
        top_crop=580,
        right_crop=50,
        bottom_crop=500
    )
    # image = image.resize((image.width * 2, image.height * 2))  # Resize to improve OCR accuracy
    image = ImageOps.grayscale(cropped_img)  # Convert to grayscale
    image = ImageOps.autocontrast(image)  # Improve contrast
    # image = image.point(lambda x: 0 if x < 210 else 255, '1')  # Binarize (thresholding)

    # Display the image using Pillow
    # image.show()

    ocr_save_dir = 'output_ocr'
    if not os.path.exists(ocr_save_dir):
        os.makedirs(ocr_save_dir, exist_ok=True)
    image.save(os.path.join(ocr_save_dir, 'preprocessed_image.jpg'))
    pdf_ocr_info = extract_important_info_by_ocr(image=image)
    pdf_nr_rejestracyjny_info = extract_nr_rejestracyjny_by_ocr(image=image)
    return pdf_ocr_info, pdf_nr_rejestracyjny_info


def save_single_page(pdf_doc: fitz.Document, page_number, output_path):
    """
    Save a single specified page from a PDF document to a new PDF file.

    Args:
        pdf_doc (fitz.Document): the input PDF document.
        page_number (int): Page number to save (0-based index).
        output_path (str): Path to save the new PDF containing the single page.

    Returns:
        None
    """
    # Create a new empty PDF
    new_pdf = fitz.open()

    # Insert the specified page into the new PDF
    new_pdf.insert_pdf(pdf_doc, from_page=page_number, to_page=page_number)

    # Save the new PDF
    new_pdf.save(output_path)
    new_pdf.close()
    pdf_doc.close()


def validate_coordinates(rect_x0, rect_y0, rect_x1, rect_y1, page_width, page_height):
    if rect_x0 < 0 or rect_x1 > page_width:
        raise ValueError("Rectangle X-coordinates exceed page width")
    if rect_y0 < 0 or rect_y1 > page_height:
        raise ValueError("Rectangle Y-coordinates exceed page height")


def add_white_rectangle_to_page(
        pdf_doc: fitz.Document,
        info_1st_page: list,
        info_nr_plate: str,
        rect_x0, rect_y0, rect_x1, rect_y1,
        color: tuple = (1, 1, 1),
        page_number: int = 0
):
    """
    Adds a white rectangle to a specified location on a PDF document.

    Args:
        pdf_doc (fitz.Document): the input PDF document.
        info_1st_page (list): List of important information extracted from the first page.
        info_nr_plate (str): info_nr_plate from the first page.
        rect_x0 (float): X-coordinate of the top-left corner of the rectangle.
        rect_y0 (float): Y-coordinate of the top-left corner of the rectangle.
        rect_x1 (float): X-coordinate of the bottom-right corner of the rectangle.
        rect_y1 (float): Y-coordinate of the bottom-right corner of the rectangle.
        color (tuple): RGB color of the rectangle (values between 0 and 1).
        page_number (int, optional): Page number to modify (0-based index). Defaults to 0.

    Returns:
        None
    """
    # Open the PDF document
    pdf_document = fitz.open(pdf_doc)

    # Get the specified page
    page = pdf_document[page_number]
    page_width, page_height = page.rect.width, page.rect.height

    # Create a rectangle object
    validate_coordinates(rect_x0, rect_y0, rect_x1, rect_y1, page_width, page_height)
    # Create a rectangle object
    rect = fitz.Rect(rect_x0, rect_y0, rect_x1, rect_y1)

    # Add a filled annotation (rectangle)
    shape = page.new_shape()  # Start drawing a new shape
    shape.draw_rect(rect)  # Draw the rectangle
    shape.finish(fill=color, color=None)  # Fill with color, no border
    shape.commit()  # Commit to the page

    save_out_dir = "outputs_blurred"
    # Save the modified PDF
    if not os.path.exists(save_out_dir):
        os.makedirs(save_out_dir, exist_ok=True)

    save_file_key_info = (info_1st_page[4], info_nr_plate[0], info_1st_page[5])
    output_path = os.path.join(save_out_dir, "_".join(save_file_key_info) + '.pdf')
    save_single_page(pdf_doc=pdf_document, page_number=page_number, output_path=output_path)
    print(f"White rectangle added to page {page_number + 1} and saved to {output_path}.")
