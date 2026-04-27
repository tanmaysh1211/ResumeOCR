import gspread
from oauth2client.service_account import ServiceAccountCredentials

CREDS_FILE  = "creds.json"          # path to your service-account key file
SHEET_NAME  = "RecruitmentData"     # exact name of your Google Sheet tab

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

COLUMNS = ["Name", "Email", "Phone", "Role", "Experience (Years)", "Skills"]

def _get_sheet():
    creds  = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPES)
    client = gspread.authorize(creds)
    sheet  = client.open(SHEET_NAME).sheet1
    return sheet


def _ensure_header(sheet):
    try:
        existing = sheet.row_values(1)
    except Exception:
        existing = []

    if existing != COLUMNS:
        sheet.insert_row(COLUMNS, index=1)


def upload_to_sheet(parsed: dict) -> bool:
    try:
        sheet = _get_sheet()
        _ensure_header(sheet)

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
