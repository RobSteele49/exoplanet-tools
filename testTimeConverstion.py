from datetime import datetime

from timeConverter import convertToUtc  # Import the function from your module
from timeConverter import convertFromUtc

# Example usage
startTimeLocal = datetime(2023, 10, 30, 0, 0, 0)  # Local time, adjust as needed
print (startTimeLocal)
timezone_str = 'America/New_York'  # Example timezone (Eastern Time Zone)

start_time_utc = convertToUtc(startTimeLocal, timezone_str)
print(start_time_utc)

timezone_str = 'America/Los_Angeles'

start_time_utc = convertToUtc(startTimeLocal, timezone_str)
print(start_time_utc)

timeInUtc = convertFromUtc (start_time_utc, timezone_str)
print (timeInUtc)
