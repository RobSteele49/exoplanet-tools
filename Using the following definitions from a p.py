Using the following definitions from a python program

from datetime import datetime
from astropy.time import Time, TimezoneInfo
from astropy import units as u

and using the following definition for startTime in PDT how do I convert,
using a function, to CUT in the same Time definition

startTime = Time(datetime(2023,10,30,0,0,0), scale='utc')

