from PIL import Image


def crop_image(
        img,
        left_crop: int,
        top_crop: int,
        right_crop: int,
        bottom_crop: int,
):
    # Get the dimensions of the image
    width, height = img.size

    # Define the cropping box (left, upper, right, lower)
    crop_box = (
        left_crop,
        top_crop,
        width - right_crop,
        height - bottom_crop
    )

    # Crop the image
    cropped_img = img.crop(crop_box)

    return cropped_img
