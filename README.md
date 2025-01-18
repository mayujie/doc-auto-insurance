# doc-auto-insurance

auto fill insurance

## Structures

1. [run_sign_single.py](run_sign_single.py)
   
   To insert signature for single pdf document and make rectangle cover at certain place with color.
2. [run_sign_multi.py](run_sign_multi.py)
    - Loop through each company folders
    - enable use_ocr then can enable create_blurred_pdf
    - Perform OCR extract information on 1st page,
    - Making rectangle cover at certain place with color.
    - Identifying blank page
    - Finally, insert corresponding company signature to documents under folder.
    - If enabled use_ocr will save each extracted pdf 1st page information to records.txt

4. [run_ocr.py](run_ocr.py)

   Using OCR to extract 1st page information from each pdf under folder `"outputs"`  and save them to `output_ocr/results_ocr.txt`
5. [run_compress_pdf.py](run_compress_pdf.py)
   
   Compress each pdf file under `"outputs"` and save compressed pdf with suffix `_cps`

6. [run_crop_img.py](run_crop_img.py)
   
   Crop the image by specifying crop_box coordinate left, top, right and bottom.

### [poczta polska Wpłata na rachunek bankowy](https://cennik.poczta-polska.pl/druk,Bank.html)

[Python处理PDF的第三方库对比
](https://dothinking.github.io/2021-01-02-Python%E5%A4%84%E7%90%86PDF%E7%9A%84%E7%AC%AC%E4%B8%89%E6%96%B9%E5%BA%93%E5%AF%B9%E6%AF%94/)

## make transparent stamp from canva

Run the following command to make the white background transparent:

```bash
convert stamp_edit.png -transparent white stamp_edit_NoBG.png
```

## Tesseract OCR settings

1. Install Tesseract and pytesseract

```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-pol

# Verify Language Data Installation
tesseract --version
tesseract --list-langs
```

2.Install the Python wrapper for Tesseract:

```bash
pip install pytesseract
```
