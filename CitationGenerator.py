import pandas as pd
from dateutil import parser
import datetime
import re



# Given single date, parse into IEEE format (Month Year)
def convert_date(date):
    parsed_date = parser.parse(date, default=datetime.datetime(1,1,1))
    if parsed_date.month ==  1 and len(date) == 4:
        return parsed_date.strftime("%Y")
    else:
        return parsed_date.strftime("%B %Y")
        
# Given list of dates, convert all dates into IEEE format
def convert_dates(dates):
    for date in dates:
        print(date)
        print(convert_date(date))


