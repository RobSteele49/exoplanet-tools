from datetime import datetime
import pytz
from astropy.time import Time

def convert_to_utc(localTime, timezone_str):
    # Define the desired timezone
    desired_timezone = pytz.timezone(timezone_str)

    # Convert the input time (datetime object) to the desired timezone
    start_time_desired_timezone = desired_timezone.localize(localTime)

    # Convert the desired timezone time to UTC
    start_time_utc = start_time_desired_timezone.astimezone(pytz.utc)

    # Create a Time object from the UTC datetime
    start_time_astropy = Time(start_time_utc)

    return start_time_astropy

def convert_from_utc(localTime, timeZoneString):
    # Define the desired timezone
    desired_timezone = pytz.timezone(timeZoneString)

    # Convert the input time (datetime object) to the desired timezone
    localTimeZone = desired_timezone.localize(localTime)

    # Convert the desired timezone time to UTC
    TimeUtc = localTimeZone.astimezone(pytz.utc)

    # Create a Time object from the UTC datetime
    TimeInAstropy = Time(TimeUtc)

    return TimeInAstropy