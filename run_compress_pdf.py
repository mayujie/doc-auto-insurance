import os
from doc_auto.utils_op import compress_pdf

# Example usage
root_dir = '/home/yujiema/my_github/doc-auto-insurance/res_outputs'
for file in os.listdir(root_dir):
    file_path = os.path.join(root_dir, file)
    save_file_path = os.path.join(root_dir, os.path.splitext(file)[0] + "_cps" + os.path.splitext(file)[1])
    compress_pdf(file_path, save_file_path)
