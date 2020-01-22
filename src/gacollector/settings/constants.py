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

# Urls
TEMPORARY_URLS_PATH = "./temp/urls.txt"

# Templates to be replaced by date in BASE_URL
tmpl_date1 = "<!#@!1>"
tmpl_date2 = "<!#@!2>"

# Selenium firefox driver log
GECKO_DRIVER_PATH = './src/bin/chromedriver.exe'
FIREFOX_BINARY_PATH = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
GECKO_DRIVER_LOG_PATH = './temp/ff_driver.log'
GA_COOKE_PATH = './usr/FFP_cookie/ga.pkl'

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
    # '—',
    # '—',
    # 'â€',
    'â€',

]
#7 0 1 3 5
DATE_OUT_FORMAT = "%Y.%m.%d"

csv.register_dialect('ga',
                     quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)

GSHEET_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GSHEET_TOKEN = './usr/connectors/gsheet/user_token.pickle'
GSHEET_CREDS = './usr/connectors/gsheet/app_credentials.json'
