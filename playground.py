from harecords import *
import csv

DHSR_HAHEADER_FILE_URL = 'https://www2.ncdhhs.gov/dhsr/data/ha-header.txt'
DHSR_DATA_FILE_URL = 'https://www2.ncdhhs.gov/dhsr/data/ha.txt'

dhsrHaheaderFile = HaHeaders(DHSR_HAHEADER_FILE_URL)
fields = dhsrHaheaderFile.getFieldNames()

dhsrDataFile = HaData(DHSR_DATA_FILE_URL)
records = dhsrDataFile.getRecords()

reader = csv.DictReader(records, fieldnames=fields)

print(reader[76])

# import requests
# import StringIO
# import csv
#
# headerRequest = requests.get('https://www2.ncdhhs.gov/dhsr/data/ha-header.txt')
# dataRequest = requests.get('https://www2.ncdhhs.gov/dhsr/data/ha.txt')
#
# headersString = headerRequest.text.split('\r\n')[6]
# dataString = dataRequest.text
#
# fieldNames = headersString.split(',')
#
#
# ---
# from requests import get
# import cStringIO
# import re
#
# file = get('https://www2.ncdhhs.gov/dhsr/data/ha-header.txt')
# output = cStringIO.StringIO()
# output.write(file.text)
# contents = output.getvalue()
# output.close()
# lines = contents.split('\r\n')
# pattern = re.compile("^(\w+,)+\w+$")
# for line in lines:
#     if pattern.match(line):
#         fields = line.split(,)
#