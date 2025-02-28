from doc_auto.utils_img_op import overlay_rectangle_on_img

# Example usage
input_path = "SCRAP title info.png"
# output_path = "SCRAP title.png"
output_path = None

overlay_rectangle_on_img(
    input_path, output_path,
    left_crop=85,
    top_crop=168,
    right_crop=480,
    bottom_crop=0,
    debug=True,
)
