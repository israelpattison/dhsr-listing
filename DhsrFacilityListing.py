from requests import get
from csv import DictReader
import re, cStringIO

# The base URI of the NC DHSR website
DHSR_SITE = 'https://www2.ncdhhs.gov/dhsr'

# The URI for the facility listing header file on the DHSR website
DHSR_HAHEADER_FILE_URL = DHSR_SITE + '/data/icfmr-header.txt'

# The URI for the facility listing records on the DHSR website
DHSR_DATA_FILE_URL = DHSR_SITE + '/data/icfmr.txt'

class DhsrFacilityListing:

    def __init__(self):

        # A list of all the record dictionaries
        self._facilities = list()
        self._counties = list()
        self._licensees = list()

        # Retrieve and store the facility listings from the DHSR
        # website when we create a new listing object
        self._retrieveRecords()
        self._getListOfCountiesWithFacilities()
        self._getListOfLicensees()

    # A method to retrieve and return contents from the web for both
    # the header file and the facility listing
    def _retrieve(self, url):

        # Use HTTP GET to retrieve the text contents of the file based
        # on the URI
        file = get(url).text

        # Create a new StringIO object so we can stream the file
        # contents into a variable
        # Necessary to remove Unicode encoding per Python 2.7
        # shortcomings
        output = cStringIO.StringIO()

        # Stream the contents of the file into the StringIO object
        output.write(file)

        # Return the value of the StringIO object and save it in the
        # content variable
        content = output.getvalue()

        # Close the StringIO object
        output.close

        # Return the processed content from the file retrieved from
        # the web
        return content

    # A method to retrieve the header file from the DHSR website
    # and return a the field names as a list
    def _retrieveFieldNames(self, url):

        # Retrieve and store the contents of the facilities listing
        # header file from the DHSR website
        content = self._retrieve(url)

        # Process the file to find the line containing the field names
        lines = content.split('\r\n')
        pattern = re.compile("^(\w+,)+\w+$")
        for line in lines:
            if pattern.match(line):
                fieldNames = line.split(',')

        # Return a list of field names to the caller
        return fieldNames

    def _retrieveRecords(self):

        # Retrieve a list of field names from the DHSR website
        fieldNames = self._retrieveFieldNames(DHSR_HAHEADER_FILE_URL)

        # Retrieve the facility records from the DHSR website
        records = self._retrieve(DHSR_DATA_FILE_URL)
        facilityRecords = records.split('\r\n')

        # Use the csv DictReader to create dictionaries for each row
        # in the csv row inserting the field names as keys in the
        # dictionaries
        reader = DictReader(facilityRecords, fieldnames=fieldNames)

        # append each facility dictionary to the list of facilities
        for row in reader:
            self._facilities.append(row)

    def _getListOfCountiesWithFacilities(self):
        counties = list()
        for facility in self._facilities:
            if facility['FCOUNTY'] not in counties:
                counties.append(facility['FCOUNTY'])
        counties.sort()
        self._counties = counties

    def _getListOfLicensees(self):
        licensees = list()
        for facility in self._facilities:
            if facility['LICENSEE'] not in licensees:
                licensees.append(facility['LICENSEE'])
        licensees.sort()
        self._licensees = licensees

    def _getRecordsByKey(self, key, value):
        records = list()
        for facility in self._facilities:
            if facility[key] == value:
                records.append(facility)
        return records.sort()

    def getRecords(self):
        return self._facilities

    def getCounties(self):
        return self._counties

    def getLicensees(self):
        return self._licensees

    def getRecordsForCounty(self, county):
        return self._getRecordsByKey("FCOUNTY", county)

    def getRecordsForLicensee(self, licensee):
        return self._getRecordsByKey("LICENSEE", licensee)
