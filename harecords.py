from requests import get
from csv import DictReader
import re, cStringIO

# The base URI of the NC DHSR website
DHSR_SITE = 'https://www2.ncdhhs.gov/dhsr'

# The URI for the facility listing header file on the DHSR website
DHSR_HAHEADER_FILE_URL = DHSR_SITE + '/data/ha-header.txt'

# The URI for the facility listing records on the DHSR website
DHSR_DATA_FILE_URL = DHSR_SITE + '/data/ha.txt'

class DhsrFacilityListing:

    def __init__(self):

        # Retrieve and store the facility listings from the DHSR
        # website when we create a new listing object
        self.retrieveRecords()

    # A method to retrieve and return contents from the web for both
    # the header file and the facility listing
    def retrieve(self, url):

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
    def retrieveFieldNames(self, url):

        # Retrieve and store the contents of the facilities listing
        # header file from the DHSR website
        content = self.retrieve(url)

        # Process the file to find the line containing the field names
        lines = content.split('\r\n')
        pattern = re.compile("^(\w+,)+\w+$")
        for line in lines:
            if pattern.match(line):
                fieldNames = line.split(',')

        # Return a list of field names to the caller
        return fieldNames

    def retrieveRecords(self):

        # Retrieve a list of field names from the DHSR website
        self.fieldNames = self.retrieveFieldNames(DHSR_HAHEADER_FILE_URL)

        # Retrieve the facility records from the DHSR website
        self.facilityRecords = self.retrieve(DHSR_DATA_FILE_URL)

        # Save a list of dictionaries containing the facility records
        #TODO: figure out how to return a dictionary instead of a DictReader object
        self.records = DictReader(self.facilityRecords, fieldnames=self.fieldNames)

    def getRecords(self):
        return self.records