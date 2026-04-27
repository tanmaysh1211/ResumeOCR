# 📄 RecruitOCR — Resume Info Extractor

A lightweight resume parsing tool built with Python, OCR, and Streamlit.  
Upload an image-based resume → extract structured data → log it directly to Google Sheets.

---

## 🚀 What It Does

- Accepts resume images (`.jpg`, `.png`, `.jpeg`)
- Extracts: **Name · Email · Phone · Role · Experience · Skills**
- Cleans images with OpenCV before OCR (handles photos, scans, shadows)
- Sends parsed data directly to a connected Google Sheet
- Real-time JSON preview before saving
- Append-only — never overwrites existing rows

---

## 🗂️ Project Structure

```
RecruitOCR/
├── recruitocr_to_sheets.py   ← Main Streamlit app (run this)
├── requirements.txt          ← All Python dependencies
├── creds.json                ← Google API key (DO NOT commit)
├── .gitignore
├── README.md
├── utils/
│   ├── __init__.py
│   ├── ocr_utils.py          ← OpenCV pre-processing + Tesseract OCR
│   ├── parser.py             ← Regex field extraction
│   └── sheets_utils.py       ← Google Sheets auth + append
└── sample_resumes/           ← Test images (optional)
```

---

## ⚙️ Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR (system-level)

**Windows:**  
Download and install from https://github.com/UB-Mannheim/tesseract/wiki  
Default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

**Mac:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install tesseract-ocr
```

### 3. Set up Google Sheets API

1. Go to https://console.cloud.google.com/
2. Create a new project (or use existing)
3. Enable **Google Sheets API** and **Google Drive API**
4. Go to **IAM & Admin → Service Accounts** → Create service account
5. Download the JSON key → rename it to `creds.json` → place in project root
6. Create a Google Sheet named `RecruitmentData`
7. Share the sheet with the **service account email** (found inside `creds.json`)

### 4. Run the app

```bash
streamlit run recruitocr_to_sheets.py
```

Open your browser at `http://localhost:8501`

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| Tesseract OCR | Text extraction from images |
| OpenCV | Image pre-processing |
| Regex | Structured field parsing |
| gspread | Google Sheets API client |
| oauth2client | Google authentication |

---

## 🔒 Security Notes

- `creds.json` is **gitignored** — never commit it
- The service account only has access to sheets you explicitly share with it
- No user data is stored locally — it goes straight to your Google Sheet

---

## 🔮 Future Enhancements

- PDF support via `pdf2image`
- Batch / bulk resume parsing
- NLP-based role classification and skill matching
- CSV export for filtered candidates
- Admin dashboard for screening and review

---

## 📎 GitHub

https://github.com/HEX-CLOUD/Recruit_tool