# Image-to-Text OCR

**Image-to-Text OCR** is a simple and efficient tool that allows you to extract text from images using Optical Character Recognition (OCR). The program uses Tesseract OCR along with OpenCV for preprocessing and text extraction, providing accurate and fast results for document scanning.

## Features

- **Upload Image:** Easily upload an image (JPG, JPEG, PNG) of a document.
- **Edge Detection:** The program applies edge detection to highlight important document features.
- **Perspective Transformation:** Detects the document and applies perspective correction for better OCR accuracy.
- **Document Enhancement:** The program enhances the document for improved OCR performance.
- **Text Extraction:** Uses Tesseract OCR to extract and display text from the processed document.
- **Downloadable Result:** Once the text is extracted, you can download the result as a text file.

## Requirements

- **Python 3.x**
- **Tesseract OCR:** Make sure to install Tesseract OCR on your system and provide its installation path in the code.

## Libraries

This project uses the following Python libraries:

- `opencv-python`
- `numpy`
- `pytesseract`
- `imutils`
- `streamlit`
- `Pillow`

## Installation

To install the required libraries, run the following command:
& 
To run the program 
```bash
pip install -r requirements.txt
streamlit run app2.py


