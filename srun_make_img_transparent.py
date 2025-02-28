from PIL import Image
from doc_auto.utils_img_op import convert_white_to_transparent

# Example usage
if __name__ == "__main__":
    # Load the image
    img_path = 'assets_stamps/insurance_example.png'
    output_img_path = 'assets_stamps/insurance_example_trans.png'

    img = Image.open(img_path)
    # Convert white pixels to transparent
    img_with_transparency = convert_white_to_transparent(img)
    # Save the result
    img_with_transparency.save(output_img_path, 'PNG')
