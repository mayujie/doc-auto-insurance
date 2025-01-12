import os
import re
import fitz  # PyMuPDF
from doc_auto.utils_op import add_white_rectangle_to_page
from doc_auto.utils_op import identify_insert_page_according_blank_page
from doc_auto.utils_page import identify_blank_pages


def insert_signatures(
        pdf_path,
        output_path,
        image_path,
        page_number,
        positions,
        width=None,
        height=None,
        blur_start_point: tuple = None,
        blur_end_point: tuple = None,
        blur_color: tuple = None,
):
    """
    Insert a transparent PNG signature into a PDF at multiple positions on a specified page.

    Args:
        pdf_path (str): Path to the input PDF.
        output_path (str): Path to the output PDF.
        image_path (str): Path to the PNG image file.
        page_number (int): 1-based page number where the image will be added.
        positions (list of tuples): List of (x, y) coordinates for the top-left corner of the image.
        width (float, optional): Desired width of the image. If None, the original image width is used.
        height (float, optional): Desired height of the image. If None, the original image height is used.

    Returns:
        None
    """
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    if page_number is None:
        blank_page_number = identify_blank_pages(document=pdf_document)
        num_page_todo = identify_insert_page_according_blank_page(
            blank_page_number=blank_page_number,
            num_doc_pages=len(pdf_document)
        )
    else:
        num_page_todo = page_number

    # Open the specified page
    page = pdf_document[num_page_todo - 1]  # Convert to 0-based index

    # Insert the image at each position
    for x, y in positions:
        if width and height:
            rect = fitz.Rect(x, y, x + width, y + height)
        else:
            rect = None  # Use the image's original dimensions
        page.insert_image(rect, filename=image_path)

    if not os.path.exists(output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pattern = r'\d+_(.*?)_NoBG.png'
    match = re.search(pattern, image_path)
    if match:
        info_nr_plate = [match.group(1)]
    else:
        raise ValueError(f"No match found in {image_path}")

    add_white_rectangle_to_page(
        pdf_doc=pdf_document,
        info_1st_page=None,
        info_nr_plate=info_nr_plate,
        rect_x0=blur_start_point[0],  # Top-left X
        rect_y0=blur_start_point[1],  # Top-left Y
        rect_x1=blur_end_point[0],  # Bottom-right X
        rect_y1=blur_end_point[1],  # Bottom-right Y
        color=blur_color,
        page_number=0,
    )

    # Save the updated PDF
    pdf_document.save(output_path)
    pdf_document.close()


if __name__ == "__main__":
    # PDF_PATH = "c1_amuatu/Skan001.pdf"
    # IMG_PATH = "assets/1_amuatu_NoBG.png"

    PDF_PATH = "c2_toyar/Skan001.pdf"
    IMG_PATH = "assets/2_toyar_NoBG.png"

    PDF_PATH = "c3_frano/Skan001.pdf"
    IMG_PATH = "assets/3_frano_NoBG.png"

    # PDF_PATH = "c4_lsy/W2200P31 Polisa do podpisu.pdf"
    # PDF_PATH = "c4_lsy/W2200P34 Polisa do podpisu.pdf"
    # IMG_PATH = "assets/4_lsy_NoBG.png"

    # PDF_PATH = "c5_commercia/Skan001.pdf"
    # IMG_PATH = "assets/5_commercia_NoBG.png"

    OUTPUT_PDF_PATH = "single_output/Skan001_signed.pdf"

    SIGN_PAGE_NUM = None  # Insert which page number
    SIGN_COORDINATES = [(400, 220), (230, 300)]  # List of positions
    # SIGN_COORDINATES = [(400, 190), (230, 250)]  # List of positions
    SIGN_W, SIGN_H = 100, 100  # Resize the signature (optional)

    # BLUR_START_POINT = (40, 454.5)
    # BLUR_START_POINT = (28, 484.5)
    BLUR_START_POINT = (40, 464.5)
    BLUR_END_POINT = (400, 580)

    insert_signatures(
        pdf_path=PDF_PATH,
        output_path=OUTPUT_PDF_PATH,
        image_path=IMG_PATH,
        page_number=SIGN_PAGE_NUM,
        positions=SIGN_COORDINATES,
        width=SIGN_W,
        height=SIGN_H,
        blur_start_point=BLUR_START_POINT,
        blur_end_point=BLUR_END_POINT,
        blur_color=(1, 1, 1),  # White color for blur effect
    )
