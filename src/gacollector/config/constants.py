import csv
import re

# Urls
TEMPORARY_URLS_PATH = "./temp/urls.txt"

# Regex
reURL = re.compile(r"(2\d{3}[0-1]\d[0-3]\d)(?:&|&amp;)_u\.date01=(2\d{3}[0-1]\d[0-3]\d)")
reFILE = re.compile(r"(2\d{3}[0-1]\d[0-3]\d)-(2\d{3}[0-1]\d[0-3]\d)")
reFILE_DUPLICATE = re.compile(r"\(\d+\)")  # Ex. file(1).txt, ... , file(25).txt

# Templates to be replaced by date in BASE_URL
tmpl_date1 = "<!#@!1>"
tmpl_date2 = "<!#@!2>"

# Selenium firefox driver log
GECKO_DRIVER_PATH = './src/bin/geckodriver.exe'
FIREFOX_BINARY_PATH = "C:/Program Files/Mozilla Firefox/firefox.exe"
GECKO_DRIVER_LOG_PATH = './temp/ff_driver.log'
GA_COOKE_PATH = './usr/FFP_cookie/ga.pkl'

# Set the firefox profile for downloading csv via Selenium
# !Please, use only this backslashes: '/'
PROFILE_PATH = "./usr/FFP"

# Additional headers which included to out_csv
ADDITIONAL_HEADERS = ["Week", "From", "To"]  # WARNING: change CsvHandler._set_additional_headers_ too

# Encodings
ENC_IN = 'windows-1252'
# ENC_OUT = 'windows-1251'
ENC_OUT = 'windows-1252'
CSV_NULL_VALUES = (
    'â€”',
    '—',
    '—',
    'â€',
    'â€',
    '-',
)
# 7 0 1 3 5
DATE_OUT_FORMAT = "%Y.%m.%d"

csv.register_dialect('ga',
                     quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)

GSHEET_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GSHEET_TOKEN = './usr/connectors/gsheet/user_token.pickle'
GSHEET_CREDS = './usr/connectors/gsheet/app_credentials.json'
