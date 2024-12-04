from datetime import datetime
from time_converter import convert_to_utc  # Import the function from your module
from time_converter import convert_from_utc

# Example usage
start_time_local = datetime(2023, 10, 30, 0, 0, 0)  # Local time, adjust as needed
timezone_str = 'America/New_York'  # Example timezone (Eastern Time Zone)

start_time_utc = convert_to_utc(start_time_local, timezone_str)
print(start_time_utc)

timezone_str = 'America/Los_Angeles'  # Example timezone (Eastern Time Zone)

start_time_utc = convert_to_utc(start_time_local, timezone_str)
print(start_time_utc)

from_utc = convert_from_utc(start_time_utc, timezone_str)
print(from_utc)


