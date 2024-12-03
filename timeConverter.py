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

def newConvertFromUtc (localTime, timeZoneString):
    
    timezone = pytz.timezone(timezone_string) local_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(timezone) return local_datetime

