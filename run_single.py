import fitz  # PyMuPDF


def insert_signatures(pdf_path, output_path, image_path, page_number, positions, width=None, height=None):
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

    # Open the specified page
    page = pdf_document[page_number - 1]  # Convert to 0-based index

    # Insert the image at each position
    for x, y in positions:
        if width and height:
            rect = fitz.Rect(x, y, x + width, y + height)
        else:
            rect = None  # Use the image's original dimensions
        page.insert_image(rect, filename=image_path)

    # Save the updated PDF
    pdf_document.save(output_path)
    pdf_document.close()


# Example usage
pdf_path = "c1_amuatu/1 Skan001.pdf"
output_path = "output_single/Skan001_signed.pdf"

image_path = "assets/1_amuatu_NoBG.png"
# image_path = "assets/2_toyar_NoBG.png"
# image_path = "assets/3_frano_NoBG.png"
# image_path = "assets/4_lsy_NoBG.png"
# image_path = "assets/5_commercia_NoBG.png"

page_number = 3  # Insert which page number
positions = [(400, 220), (230, 300)]  # List of positions
width, height = 100, 80  # Resize the signature (optional)

insert_signatures(pdf_path, output_path, image_path, page_number, positions, width, height)
