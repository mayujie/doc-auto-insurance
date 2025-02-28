from doc_auto.utils_img_op import merge_images_overlay_background_on_transparent

if __name__ == '__main__':
    trans_img_path = "assets_stamps/chen_sign_only_trans.png"
    merged_img_path = "assets_stamps/merged_img.png"

    background_img_path = "assets_stamps/sample_peony.eur_crop.png"
    # merged_img_path = "assets_stamps/6_peony.eur_NoBG.png"

    # background_img_path = "assets_stamps/sample_NIO_crop.png"
    # merged_img_path = "assets_stamps/7_NIO_NoBG.png"

    merge_images_overlay_background_on_transparent(
        transparent_image_path=trans_img_path,
        background_image_path=background_img_path,
        output_image_path=merged_img_path,
        overlay_flip=False,
    )
