import os
import re
from doc_auto.utils_log import setup_logger
from doc_auto.utils_op import insert_signatures

logger = setup_logger(__name__)

def main(dir_paths: list):
    positions = [(400, 220), (230, 300)]  # List of positions
    width, height = 100, 100  # Resize the signature (optional)

    assets_dir = os.listdir("assets")
    for sub_d in DIR_PATHS:

        pattern = r'c\d+_(\w+)'
        c_keyname = re.match(pattern, sub_d).group(1)
        sign_filename = [s_file for s_file in assets_dir if c_keyname in s_file][0]
        sign_filepath = os.path.join('assets', sign_filename)

        sub_d_path = os.path.join(ROOT_DIR, sub_d)
        pdf_paths = [os.path.join(sub_d_path, f_name) for f_name in os.listdir(sub_d_path)]

        for pdf_path in pdf_paths:
            logger.info(f'Processing :{pdf_path}')

            insert_signatures(
                pdf_path=pdf_path,
                image_path=sign_filepath,
                positions=positions,
                width=width,
                height=height,
                page_number=None,
                output_path=None
            )


if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(__file__)
    DIR_PATHS = [d for d in os.listdir(ROOT_DIR) if d.startswith('c')]
    logger.info(f"Main root path: {ROOT_DIR}")
    logger.info(f"{DIR_PATHS}")

    main(dir_paths=DIR_PATHS)
