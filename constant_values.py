import csv

# Enum of date-range types
TYPE_DAY = 1
TYPE_WEEK = 7
TYPE_MONTH = 30

# Enum of level-of-work
LW_GENERATE_URLS = 4
LW_DOWNLOAD_GENERATED_URLS = 3
LW_COLLECT_RESULT = 2
LW_SEND_TO_GOOGLE_SHEETS = 1

# Templates to be replaced by date in BASE_URL
tmpl_date1 = "<!#@!1>"
tmpl_date2 = "<!#@!2>"

# Enum of operations with csv-files
CSV_OVERALL = 1
CSV_SUMMARIZE_PERIOD = 2

# Additional headers which included to out_csv
ADDITIONAL_HEADERS = ["Week", "From", "To"]  # WARNING: change CsvHandler._set_additional_headers_ too

# Encodings
ENC_IN = 'windows-1252'
ENC_OUT = 'windows-1251'
CSV_NULL_VALUES = [
    'â€”',
]

DATE_OUT_FORMAT = "%Y.%m.%d"

csv.register_dialect('ga',
                     quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)

GSHEET_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GSHEET_TOKEN = 'token.pickle'
GSHEET_CREDS = 'credentials.json'
