import os.path

from PIL import Image
from doc_auto.utils_img_op import crop_image


def run_crop_image(
        input_path: str,
        output_path: str = None,
        left_crop: int = 0,
        top_crop: int = 300,
        right_crop: int = 0,
        bottom_crop: int = 200
):
    """
    Crop the left, top, right and bottom of the image.

    Args:
        input_path (str): Path to the input PNG image.
        output_path (str): Path to save the cropped image.
        left_crop (int): Number of pixels to crop from the left (default 0).
        top_crop (int): Number of pixels to crop from the top (default 300).
        right_crop (int): Number of pixels to crop from the right (default 0).
        bottom_crop (int): Number of pixels to crop from the bottom (default 200).

    Returns:
        None
    """
    # Open the image
    img = Image.open(input_path)

    cropped_img = crop_image(
        img=img,
        left_crop=left_crop,
        top_crop=top_crop,
        right_crop=right_crop,
        bottom_crop=bottom_crop
    )

    # Save the cropped image
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '_crop' + os.path.splitext(input_path)[1]
    cropped_img.save(output_path)


# Example usage
input_path = "assets_stamps/sample_amu.png"
output_path = "assets_stamps/cropped_image.png"
# output_path = None
run_crop_image(input_path, output_path,
               left_crop=980,
               right_crop=860,
               top_crop=1720,
               # top_crop=0,
               bottom_crop=1450,
               # bottom_crop=0,
               )
