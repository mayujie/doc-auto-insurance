from PIL import Image, ImageDraw


def crop_image(
        img,
        left_crop: int,
        top_crop: int,
        right_crop: int,
        bottom_crop: int,
):
    """
    Define the cropping box (left, upper, right, lower)

    Args:
        param img:
        param left_crop:
        param top_crop:
        param right_crop:
        param bottom_crop:

    Returns:
        None
    """
    # Get the dimensions of the image
    width, height = img.size
    print(f'Original image dimensions WxH:{img.size}')

    # Define the cropping box (left, upper, right, lower)
    crop_box = (
        left_crop,
        top_crop,
        width - right_crop,
        height - bottom_crop
    )

    # Crop the image
    cropped_img = img.crop(crop_box)
    print(f'Crop image dimensions WxH:{cropped_img.size}')

    return cropped_img


def convert_white_to_transparent(image, threshold=200):
    """
    Convert white or near-white pixels in an image to transparent.

    Parameters:
        image (PIL.Image.Image): The input image in RGBA mode.
        threshold (int): The RGB value above which a pixel is considered white.
                         Defaults to 200.

    Returns:
        PIL.Image.Image: The image with white pixels made transparent.
    """
    # Ensure the image is in RGBA mode
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Process the image data
    datas = image.getdata()
    new_data = []
    for item in datas:
        # Check if the pixel is white or near-white
        if item[0] >= threshold and item[1] >= threshold and item[2] >= threshold:
            # Replace white pixel with a transparent one
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    # Update image data
    image.putdata(new_data)
    return image


def merge_images_overlay_background_on_transparent(
        transparent_image_path, background_image_path, output_image_path, overlay_flip: bool = False):
    """
    Merge two images by overlaying the background image onto the transparent image.

    This function opens a transparent image and a background image, converts white pixels
    in the background image to transparent, resizes the smaller image to match the larger
    image's dimensions, overlays one image onto the other based on the `overlay_flip` flag,
    and saves the resulting image as a PNG file.

    Parameters:
        transparent_image_path (str): Path to the transparent image file.
        background_image_path (str): Path to the background image file.
        output_image_path (str): Path where the merged image will be saved.
        overlay_flip (bool, optional): If True, overlays the transparent image on top of
                                       the background image. If False (default), overlays
                                       the background image on top of the transparent image.

    Returns:
        None

    Raises:
        FileNotFoundError: If either the transparent or background image file is not found.
        IOError: If there is an error opening or processing the images.

    Example:
        merge_images_overlay_background_on_transparent(
            'transparent_image.png',
            'background_image.png',
            'merged_image.png',
            overlay_flip=False
        )
    """
    # Open the transparent image
    transparent_img = Image.open(transparent_image_path).convert("RGBA")

    # Open the background image
    background_img = Image.open(background_image_path).convert("RGBA")

    # Convert white pixels to transparent
    background_img = convert_white_to_transparent(image=background_img, threshold=200)

    # Determine which image is smaller
    if transparent_img.size[0] * transparent_img.size[1] < background_img.size[0] * background_img.size[1]:
        print("transparent image is smaller than background image")
        smaller_img = transparent_img
        larger_img = background_img
    else:
        print("background image is smaller than transparent image")
        smaller_img = background_img
        larger_img = transparent_img

    # Resize the smaller image to match the larger image's size
    smaller_img = smaller_img.resize(larger_img.size, Image.LANCZOS)

    # Composite the images: overlay the resized smaller image onto the larger image
    if overlay_flip:
        combined_img = Image.alpha_composite(larger_img, smaller_img)
    else:
        combined_img = Image.alpha_composite(smaller_img, larger_img)

    # Save the result
    combined_img.save(output_image_path, format="PNG")


def overlay_rectangle_on_img(
        input_path, output_path=None,
        left_crop=0, right_crop=0, top_crop=0, bottom_crop=0,
        debug: bool = False,
):
    """
    Overlays a rectangle on the input image based on the specified crop values.

    :param input_path: Path to the input PNG image file.
    :param output_path: Path to save the output image. If None, the image will be displayed instead.
    :param left_crop: Pixels to crop from the left.
    :param right_crop: Pixels to crop from the right.
    :param top_crop: Pixels to crop from the top.
    :param bottom_crop: Pixels to crop from the bottom.
    :param debug: display result rectangle with red border.
    """
    # Open the input image
    image = Image.open(input_path)
    print(image.size)
    draw = ImageDraw.Draw(image)

    # Calculate the rectangle coordinates
    width, height = image.size
    left = left_crop
    top = top_crop
    right = width - right_crop
    bottom = height - bottom_crop

    # Draw the rectangle
    if debug:
        draw.rectangle([left, top, right, bottom], outline="red", width=5)
    else:
        draw.rectangle([left, top, right, bottom], fill="white")

    # Save or display the image
    if output_path:
        image.save(output_path)
        print(f"Image saved to {output_path}")
    else:
        image.show()
