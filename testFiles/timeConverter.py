import pytz
from astropy.time import Time

def convertToUtc (localTime, timezoneString):
    # Define the desired timezone
    desiredTimezone = pytz.timezone(timezoneString)

    # Convert the input time (datetime object) to the desired timezone
    localTimeDesiredTimezone = desiredTimezone.localize(localTime)

    # Convert the desired timezone time to UTC
    start_time_utc = localTimeDesiredTimezone.astimezone(pytz.utc)

    # Create a Time object from the UTC datetime
    localTimeAstropy = Time(start_time_utc)

    return localTimeAstropy

def convertFromUtc(localTime, timeZoneString):
    # Define the desired timezone
    desiredTimeZone = pytz.timezone(timeZoneString)

    # Convert the input time (datetime object) to the desired timezone
    localTimeZone = desiredTimeZone.localize(localTime)

    # Convert the desired timezone time to UTC
    TimeUtc = localTimeZone.astimezone(pytz.utc)

    # Create a Time object from the UTC datetime
    TimeInAstropy = Time(TimeUtc)

    return TimeInAstropy

if __name__ == '__main__':

    from datetime import datetime

    print ('inside of __main__')

    # Example usage
    timeInLocalZone = datetime(2023, 10, 30, 0, 0, 0)  # Local time, adjust as needed
    print (timeInLocalZone)
    timeZoneString = 'America/New_York'  # Example timezone (Eastern Time Zone)

    timeInUtcZone = convertToUtc(timeInLocalZone, timeZoneString)
    print(timeInUtcZone)

    timeZoneString = 'America/Los_Angeles'

    timeInUtcZone = convertToUtc(timeInLocalZone, timeZoneString)
    print(timeInUtcZone)

    timeInUtcZone = datetime(2023,10, 30, 0, 0, 0)
    timeInLocalZone = convertFromUtc (timeInUtcZone, timeZoneString)
    print ('time in local Zone')
    print (timeInLocalZone)
    
