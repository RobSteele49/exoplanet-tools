from datetime import datetime

from timeConverter import convertToUtc  # Import the function from your module
from timeConverter import convertFromUtc

# Example usage

timeInLocalZone = datetime(2023, 10, 30, 0, 0, 0)  # Local time, adjust as needed

print (timeInLocalZone)

timeZoneString = 'America/New_York'  # Example timezone (Eastern Time Zone)

timeInUtcZone = convertToUtc(timeInLocalZone, timeZoneString)
print(timeInUtcZone)

timeZoneString = 'America/Los_Angeles'

timeInUtcZone = convertToUtc(timeInLocalZone, timeZoneString)
print(timeInUtcZone)

timeInUtcZone = datetime(2023, 10, 30, 0, 0, 0)
timeInUtc = convertFromUtc (timeInUtcZone, timeZoneString)
print (timeInUtc)
