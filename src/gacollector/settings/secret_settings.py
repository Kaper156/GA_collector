import datetime

from gacollector.settings.enums import LevelWorkEnum, PeriodEnum, CsvOutOpEnum

'''
If you want to use default settings just leave variable with: '' or None
'''

# Set first step of work-cycle
# Or select from this LW_GENERATE_URLS LW_DOWNLOAD_GENERATED_URLS LW_COLLECT_RESULT LW_SEND_TO_GOOGLE_SHEETS
LEVEL_WORK = LevelWorkEnum.COLLECT_RESULT

# Url with dimensions and other stuff (CAN'T BE NONE!)
BASE_URL = "https://analytics.google.com/analytics/web/?authuser=1#/report/bf-roi-calculator/"

# Set date ranges
FROM_DATE = datetime.datetime(year=2018, month=12, day=31)  # Default: from base-url
TO_DATE = datetime.datetime(year=2019, month=11, day=24)  # Default: now
DATE_TYPE = PeriodEnum.WEEK  # Select from: TYPE_DAY TYPE_WEEK TYPE_MONTH

# Set if you need only total sum from each csv to result csv
# Select from: CSV_OVERALL CSV_SUMMARIZE_PERIOD
OUT_OPERATION = CsvOutOpEnum.SUMMARIZE_PERIOD  # Default: add all rows

# Google-sheets
# Uniq ID of google spreadsheet
GSHEET_SPREADSHEET = ''  # MUST BE SET (!!!), else not load csv to google-sheet
# Range where out csv data will be append (You can set list like other links. Ex: 'WeeklyData'!A10
GSHEET_RANGE = ""  # By default app will append data to A1 of first list of spreadsheet

# Set the folder where the csv-files will be downloaded
FOLDER_NAME = '../../out/test'  # Default: ./out/YYYY.MM.DD_UNIQ_HASH

# Set the path for file which will be contain results
OUT_CSV_PATH = ''

# Set the firefox profile for downloading csv via Selenium
# !Please, use only this backslashes: '/'
PROFILE_PATH = "./usr/FFP"
