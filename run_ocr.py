import os
import fitz  # PyMuPDF

from doc_auto.utils_page import extract_info_from_page_by_ocr

if __name__ == '__main__':
    ROOT_PATH = "res_outputs"
    list_pdf = [os.path.join(ROOT_PATH, file) for file in os.listdir(ROOT_PATH) if file.endswith('.pdf')]

    list_doc_ocr_results = []
    for pdf_path in list_pdf:
        pdf_document = fitz.open(pdf_path)

        start_left_crop_x = 40  # Initial value for left crop X
        while True:
            try:
                # Attempt to extract OCR information
                info_1st_page, info_nr_plate = extract_info_from_page_by_ocr(
                    doc=pdf_document, left_crop_x=start_left_crop_x
                )
                break  # Exit loop if successful
            except Exception as e:
                print(f"Error occurred: {e}, increasing start_left_crop_x to {start_left_crop_x + 1}")
                start_left_crop_x += 1  # Increment and retry

        list_doc_ocr_results.append(info_1st_page)

    # Open the file in write mode (it will overwrite the file if it exists)
    records_file = "res_output_ocr/results_ocr.txt"
    with open(records_file, "w") as file:
        for idx, item in enumerate(list_doc_ocr_results):
            # Join the 7 strings with a space (or any separator you prefer)
            file.write(f"## {idx + 1} ##\n")
            file.write("\n".join(item) + "\n")
            file.write(10 * "-" + "\n\n")

    print(f"Data has been written to {records_file}")
