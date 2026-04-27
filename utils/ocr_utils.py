import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(img_array: np.ndarray) -> np.ndarray:

    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array.copy()

    h, w = gray.shape
    target_w = 1800
    if w < target_w:
        scale = target_w / w
        gray = cv2.resize(gray, None, fx=scale, fy=scale,
                          interpolation=cv2.INTER_CUBIC)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31,
        C=15
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed = cv2.dilate(thresh, kernel, iterations=1)

    return processed

def run_ocr(processed_img: np.ndarray) -> str:
    config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(processed_img, config=config)
    return text.strip()
