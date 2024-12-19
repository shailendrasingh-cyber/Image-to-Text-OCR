import cv2
import numpy as np
import pytesseract
from imutils.perspective import four_point_transform
from imutils import contours
import streamlit as st
from PIL import Image
import tempfile

# Configure Tesseract OCR path (adjust to your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Function to preprocess the image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    return edged

# Function to detect the document and apply perspective transform
def detect_and_transform(image, edged):
    contours_list = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_list = contours_list[0] if len(contours_list) == 2 else contours_list[1]

    # Sort contours by area and take the largest ones
    contours_list = sorted(contours_list, key=cv2.contourArea, reverse=True)

    for c in contours_list:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)

        # Document detected if the contour has 4 points
        if len(approx) == 4:
            transformed = four_point_transform(image, approx.reshape(4, 2))
            return transformed

    return None

# Function to enhance the document
def enhance_document(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    enhanced = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return enhanced

# Function to extract text using Tesseract OCR
def extract_text(image):
    custom_config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

# Streamlit app
def main():
    st.title("Document Scanner and OCR Tool")

    # Upload image
    uploaded_file = st.file_uploader("Upload a document image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load the image
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        image = cv2.imread(temp_path)
        if image is None:
            st.error("Error: Could not load the image.")
            return

        st.subheader("Original Image")
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Original Image", use_column_width=True)

        # Step 1: Preprocess the image
        edged = preprocess_image(image)
        st.subheader("Edge Detection")
        st.image(edged, caption="Edges Detected", use_column_width=True, channels="GRAY")

        # Step 2: Detect document and apply perspective transformation
        transformed = detect_and_transform(image, edged)
        if transformed is None:
            st.error("Error: Could not detect the document.")
            return

        # Step 3: Enhance the transformed document
        enhanced = enhance_document(transformed)
        st.subheader("Enhanced for OCR")
        st.image(enhanced, caption="Enhanced Document", use_column_width=True, channels="GRAY")

        # Step 4: Extract text using OCR
        text = extract_text(enhanced)
        st.subheader("Extracted Text")
        st.text_area("OCR Result", text, height=200)

        # Additional features for user convenience
        st.subheader("Save or Share Results")
        if st.button("Download OCR Result as Text File"):
            result_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
            with open(result_file.name, "w") as file:
                file.write(text)
            st.download_button(
                label="Download Text File",
                data=open(result_file.name, "rb").read(),
                file_name="ocr_result.txt",
                mime="text/plain",
            )

if __name__ == "__main__":
    main()
