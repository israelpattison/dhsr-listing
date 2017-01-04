import requests
import StringIO
import cvs

headerRequest = requests.get('https://www2.ncdhhs.gov/dhsr/data/ha-header.txt')
dataRequest = requests.get('https://www2.ncdhhs.gov/dhsr/data/ha.txt')

headersString = headerRequest.text.split('\r\n')[6]
dataString = dataRequest.text

fieldNames = headersString.split(',')


