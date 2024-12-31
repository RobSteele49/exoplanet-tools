
from datetime import datetime
import pytz

def convertToTimezone(utcTime, timezoneStr):
    # Define the desired timezone
    desiredTimezone = pytz.timezone(timezoneStr)

    # Convert the UTC time (datetime object) to the desired timezone
    convertedTime = utcTime.astimezone(desiredTimezone)
    
    return convertedTime

# Example usage
utcTime = datetime(2023, 10, 30, 12, 0, 0, tzinfo=pytz.utc)  # UTC time to be converted

print ('utcTime:', utcTime)

# Convert UTC time to Pacific Time (PT)
convertedPtTime = convertToTimezone(utcTime, 'America/Los_Angeles')
print("Converted to Pacific Time (PT):", convertedPtTime)

# Convert UTC time to Eastern Time (ET)
convertedEtTime = convertToTimezone(utcTime, 'America/New_York')
print("Converted to Eastern Time (ET):", convertedEtTime)
