import streamlit as st
from PIL import Image
import numpy as np

from utils.ocr_utils import preprocess_image, run_ocr
from utils.parser import parse_resume
from utils.sheets_utils import upload_to_sheet

st.set_page_config(page_title="RecruitOCR", page_icon="📄")
st.title("📄 RecruitOCR: Resume Info Extractor")

uploaded_file = st.file_uploader(
    "Upload Resume Image (JPG, PNG, JPEG)",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:
    # Show uploaded image
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    st.image(image, caption="Uploaded Resume Image", use_column_width=True)

    with st.spinner("Running OCR..."):
        processed = preprocess_image(img_array)
        raw_text  = run_ocr(processed)

    st.subheader("Extracted Text")
    st.text_area("", value=raw_text, height=180)

    parsed = parse_resume(raw_text)

    st.subheader("Parsed Resume Information")
    st.json(parsed)

    if st.button("Upload to Google Sheet"):
        with st.spinner("Uploading..."):
            success = upload_to_sheet(parsed)

        if success:
            st.success("✅ Data uploaded to Google Sheet successfully!")
        else:
            st.error("❌ Upload failed. Check your creds.json and sheet name.")
