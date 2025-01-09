from PIL import Image


def crop_image(input_path, output_path, top_crop=300, bottom_crop=200):
    """
    Crop the top and bottom of the PNG image.

    Args:
        input_path (str): Path to the input PNG image.
        output_path (str): Path to save the cropped image.
        top_crop (int): Number of pixels to crop from the top (default 200).
        bottom_crop (int): Number of pixels to crop from the bottom (default 200).

    Returns:
        None
    """
    # Open the image
    img = Image.open(input_path)

    # Get the dimensions of the image
    width, height = img.size

    # Define the cropping box (left, upper, right, lower)
    crop_box = (0, top_crop, width, height - bottom_crop)

    # Crop the image
    cropped_img = img.crop(crop_box)

    # Save the cropped image
    cropped_img.save(output_path)


# Example usage
input_path = "assets/1_amuatu_NoBG.png"
output_path = "assets/cropped_image.png"
crop_image(input_path, output_path)
