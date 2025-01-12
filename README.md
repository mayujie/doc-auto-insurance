# doc-auto-insurance
auto fill insurance

### [poczta polska Wpłata na rachunek bankowy](https://cennik.poczta-polska.pl/druk,Bank.html)

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
