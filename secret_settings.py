import datetime

from constant_values import *

'''
If you want to use default settings just leave variable with: '' or None
'''

# Set first step of work-cycle
LEVEL_WORK = LW_URLS

# Url with dimensions and other stuff (CAN'T BE NONE!)
BASE_URL = "https://analytics.google.com/analytics/web/?authuser=1#/report/bf-roi-calculator/20190215_u.date01=20190415"

# Set date ranges
FROM_DATE = datetime.datetime(year=2018, month=12, day=1)  # Default: from base-url
TO_DATE = datetime.datetime(year=2019, month=11, day=17)  # Default: now
DATE_TYPE = TYPE_WEEK  # Select from: TYPE_DAY TYPE_WEEK TYPE_MONTH

# Set if you need only total sum from each csv to main csv
AVG_CSV = False

# Set the folder where the csv-files will be downloaded
FOLDER_NAME = ''  # Default: ./out/YYYY.MM.DD_UNIQ_HASH

# Set file with filters, you can add them in runtime mode (and they will be saved)
FILTERS_PATH = 'filters.txt'

# Set the firefox profile for downloading csv via Selenium
# !Please, use only this backslashes: '/'
PROFILE_PATH = "D:/Python/py-sandbox/py-sandbox/typical/Firefox_Profile"
