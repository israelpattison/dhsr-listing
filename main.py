from DhsrFacilityListing import *

listing = DhsrFacilityListing()
records = listing.getRecords()

for thisRecord in records:
    print thisRecord.get('FACILITY')
    print thisRecord.get('SADDR')
    print thisRecord.get('SCITY') + ", " + thisRecord.get('SSTATE') + " " + thisRecord.get('SZIP')
    print ""
