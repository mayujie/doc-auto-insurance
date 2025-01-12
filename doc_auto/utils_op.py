import os
import re
from typing import Optional

import fitz  # PyMuPDF
import pikepdf

from .utils_page import extract_info_from_page_by_ocr
from .utils_page import identify_blank_pages
from .utils_page import add_white_rectangle_to_page


def identify_insert_page_according_blank_page(blank_page_number: int, num_doc_pages: int):
    target_page_number = None

    if blank_page_number == 3:
        target_page_number = blank_page_number + 1
    if blank_page_number == 4:
        target_page_number = blank_page_number - 1
    if blank_page_number is None:
        target_page_number = num_doc_pages

    if target_page_number is None:
        raise ValueError("target_page_number cannot be None")

    return target_page_number


def insert_signatures(
        pdf_path: str,
        image_path: str,
        positions: list,
        output_path: Optional[str] = None,
        page_number: Optional[int] = None,
        width=None,
        height=None,
        use_ocr: bool = False,
        create_blurred_pdf: bool = True,
) -> list:
    """
    Insert a transparent PNG signature into a PDF at multiple positions on a specified page.

    Args:
        pdf_path (str): Path to the input PDF.
        output_path (str): Path to the output PDF.
        image_path (str): Path to the PNG image file.
        positions (list of tuples): List of (x, y) coordinates for the top-left corner of the image.
        page_number (int): 1-based page number where the image will be added.
        width (float, optional): Desired width of the image. If None, the original image width is used.
        height (float, optional): Desired height of the image. If None, the original image height is used.

    Returns:
        list
    """
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    if use_ocr:
        info_1st_page, info_nr_plate = extract_info_from_page_by_ocr(doc=pdf_document)
        if create_blurred_pdf:
            if not info_nr_plate:
                pattern = r'\d+_(.*?)_NoBG.png'
                match = re.search(pattern, image_path)
                if match:
                    info_nr_plate = [match.group(1)]
                else:
                    raise ValueError(f"No match found in {image_path}")

            add_white_rectangle_to_page(
                pdf_doc=pdf_document,
                info_1st_page=info_1st_page,
                info_nr_plate=info_nr_plate,
                rect_x0=40,  # Top-left X
                rect_y0=454.5,  # Top-left Y
                rect_x1=400,  # Bottom-right X
                rect_y1=580,  # Bottom-right Y
                color=(1, 1, 1),
                page_number=0,
            )
    else:
        info_1st_page = None

    if page_number is None:
        blank_page_number = identify_blank_pages(document=pdf_document)
        num_page_todo = identify_insert_page_according_blank_page(
            blank_page_number=blank_page_number,
            num_doc_pages=len(pdf_document)
        )
    else:
        num_page_todo = page_number

    # Open the specified page
    target_page = pdf_document[num_page_todo - 1]  # Convert to 0-based index

    # Insert the image at each position
    for x, y in positions:
        if width and height:
            rect = fitz.Rect(x, y, x + width, y + height)
        else:
            rect = None  # Use the image's original dimensions
        target_page.insert_image(rect, filename=image_path)

    # Save the updated PDF
    if output_path is None:
        output_path = os.path.splitext(pdf_path)[0] + "_signed" + os.path.splitext(pdf_path)[1]
        output_path = os.path.join('outputs', info_nr_plate[0] + "_" + os.path.basename(output_path))
    if not os.path.exists(output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf_document.save(output_path)
    pdf_document.close()

    return info_1st_page


def compress_pdf(input_path, output_path):
    """
    Compress a PDF file using pikepdf.

    Args:
        input_path (str): Path to the input PDF.
        output_path (str): Path to save the compressed PDF.

    Returns:
        None
    """
    try:
        # Open the original PDF
        pdf = pikepdf.Pdf.open(input_path)

        # Save the optimized version
        pdf.save(output_path)
        print(f"Compressed PDF saved as: {output_path}")
    except Exception as e:
        print(f"Error compressing PDF: {e}")
