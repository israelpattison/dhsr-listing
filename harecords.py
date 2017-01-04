import requests
import cStringIO
import re

class HaData:

    def __init__(self, url):
        self.setUrl(url)
        self.retrieveData()

    def setUrl(self, url):
        self.url = url

    def getUrl(self):
        return self.url

    def retrieveData(self):
        output = cStringIO.StringIO()
        dataFile = requests.get(self.url).text
        output.write(dataFile)
        contents = output.getvalue()
        output.close()
        self.records = contents.split('\r\n')

    def getRecords(self):
        return self.records

class HaHeaders:

    def __init__(self, url):
        self.setUrl(url)
        self.retrieveHeaders()

    def setUrl(self, url):
        self.url = url

    def getUrl(self):
        return self.url

    def retrieveHeaders(self):
        output = cStringIO.StringIO()
        headerFile = requests.get(self.url).text
        output.write(headerFile)
        contents = output.getvalue()
        output.close()
        lines = contents.split('\r\n')
        pattern = re.compile("^(\w+,)+\w+$")

        for line in lines:
            if pattern.match(line):
                self.fields = line.split(',')

    def getFieldNames(self):
        return self.fields

    def printFieldNames(self):
        print self.fields