import os
import re
from doc_auto.utils_log import setup_logger
from doc_auto.utils_op import insert_signatures

logger = setup_logger(__name__)


def main(
        dir_paths: list,
        use_ocr: bool = False,
        create_blurred_pdf: bool = True,
):
    positions = [
        # (400, 220),
        # (230, 300)

        (400, 170),
        (230, 250)
    ]  # List of positions
    # width, height = 100, 100  # Resize the signature (optional)
    width, height = 120, 120  # Resize the signature (optional)

    assets_dir = os.listdir("assets_stamps")
    all_pdf_extracted_info = []

    for sub_d in DIR_PATHS:

        pattern = r'c\d+_(\w+)'
        c_keyname = re.match(pattern, sub_d).group(1)
        sign_filename = [s_file for s_file in assets_dir if c_keyname in s_file][0]
        sign_filepath = os.path.join("assets_stamps", sign_filename)

        sub_d_path = os.path.join(ROOT_DIR, sub_d)
        pdf_paths = [os.path.join(sub_d_path, f_name) for f_name in os.listdir(sub_d_path)]

        for pdf_path in pdf_paths:
            logger.info(f'Processing :{pdf_path}')

            extract_info = insert_signatures(
                pdf_path=pdf_path,
                image_path=sign_filepath,
                positions=positions,
                width=width,
                height=height,
                page_number=None,
                output_path=None,
                use_ocr=use_ocr,
                create_blurred_pdf=create_blurred_pdf,
            )
            all_pdf_extracted_info.append(extract_info)

    if use_ocr:
        # Open the file in write mode (it will overwrite the file if it exists)
        with open("res_outputs/records.txt", "w") as file:
            for idx, item in enumerate(all_pdf_extracted_info):
                # Join the 7 strings with a space (or any separator you prefer)
                file.write(f"## {idx + 1} ##\n")
                file.write("\n".join(item) + "\n")
                file.write(10 * "-" + "\n\n")

        print("Data has been written to records.txt.")


if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(__file__)

    DIR_PATHS = [d for d in os.listdir(ROOT_DIR) if d.startswith('c')]
    # DIR_PATHS = [d for d in os.listdir(ROOT_DIR) if d.startswith('c4')]

    logger.info(f"Main root path: {ROOT_DIR}")
    logger.info(f"{DIR_PATHS}")

    main(dir_paths=DIR_PATHS, use_ocr=True, create_blurred_pdf=True)
