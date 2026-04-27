"""
sheets_utils.py
---------------
Google Sheets integration via gspread + oauth2client.

Setup:
  1. Create a Google Cloud service account.
  2. Download the JSON key → save as  creds.json  in the project root.
  3. Share your target Google Sheet with the service account email.
  4. Set SHEET_NAME below to match your sheet's name exactly.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ── Config — edit these two values ────────────────────────────────────────────
CREDS_FILE  = "creds.json"          # path to your service-account key file
SHEET_NAME  = "RecruitmentData"     # exact name of your Google Sheet tab

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# Column order must match the header row in your sheet
COLUMNS = ["Name", "Email", "Phone", "Role", "Experience (Years)", "Skills"]


# ── Internal helpers ───────────────────────────────────────────────────────────

def _get_sheet():
    """Authenticate and return the first worksheet of SHEET_NAME."""
    creds  = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPES)
    client = gspread.authorize(creds)
    sheet  = client.open(SHEET_NAME).sheet1
    return sheet


def _ensure_header(sheet):
    """
    Write the header row if the sheet is empty or the first row doesn't match.
    Safe to call on every upload — it won't overwrite existing data.
    """
    try:
        existing = sheet.row_values(1)
    except Exception:
        existing = []

    if existing != COLUMNS:
        sheet.insert_row(COLUMNS, index=1)


# ── Public API ─────────────────────────────────────────────────────────────────

def upload_to_sheet(parsed: dict) -> bool:
    """
    Append a single resume's parsed data as a new row.

    Args:
        parsed: dict returned by parser.parse_resume()

    Returns:
        True on success, False on any error.
    """
    try:
        sheet = _get_sheet()
        _ensure_header(sheet)

        # Build row in the same order as COLUMNS
        row = [parsed.get(col, "") for col in COLUMNS]
        sheet.append_row(row, value_input_option="USER_ENTERED")
        return True

    except FileNotFoundError:
        print(f"[sheets_utils] ERROR: '{CREDS_FILE}' not found. "
              "Download your service-account key and save it as creds.json.")
        return False

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"[sheets_utils] ERROR: Sheet '{SHEET_NAME}' not found. "
              "Check the name and make sure it's shared with the service account.")
        return False

    except Exception as e:
        print(f"[sheets_utils] ERROR: {e}")
        return False