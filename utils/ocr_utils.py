"""
ocr_utils.py
------------
Image pre-processing with OpenCV + text extraction with Tesseract.
"""

import cv2
import numpy as np
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(img_array: np.ndarray) -> np.ndarray:
    """
    Clean up a resume image so Tesseract can read it accurately.

    Steps:
      1. Convert to grayscale
      2. Resize to a safe width (improves small-text accuracy)
      3. Apply adaptive thresholding (handles uneven lighting / shadows)
      4. Light dilation to reconnect broken strokes
    """
    # 1. Grayscale
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array.copy()

    # 2. Resize — keep aspect ratio, target width 1800px
    h, w = gray.shape
    target_w = 1800
    if w < target_w:
        scale = target_w / w
        gray = cv2.resize(gray, None, fx=scale, fy=scale,
                          interpolation=cv2.INTER_CUBIC)

    # 3. Adaptive threshold (better than global for photos / scans)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31,
        C=15
    )

    # 4. Light dilation — reconnects letters broken by threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed = cv2.dilate(thresh, kernel, iterations=1)

    return processed


def run_ocr(processed_img: np.ndarray) -> str:
    """
    Run Tesseract OCR on a pre-processed (binary) image.

    psm 6  → assume a single uniform block of text — works well for resumes.
    oem 3  → use the best available engine (LSTM + legacy).
    """
    config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(processed_img, config=config)
    return text.strip()