# predictTransit.py

# Written by Rob Steele

# The goal of this program is to scan all of the trasiting exoplanets
# and search for ones that are visible during the night times hours
# from my location.

# On Dec. 13, 2022 I moved the logic for updating the xml files out of this
# program and put that logic in the 'updateXmlFiles.py' program.

from astropy import units as u
from astropy.time import Time

from astropy.coordinates import EarthLocation,SkyCoord
from astropy.coordinates import AltAz

# This is a whack, 10/10/22 at removing an error due to being offline
# Need to look into determining how to detect when I"m offline and only use
# this logic under those conditions.

from astropy.utils.iers import conf
conf.auto_max_age = None

# Start of the rest of my old code, that worked when online

import cmath
from datetime import datetime
import fnmatch
import os
import xml.etree.ElementTree as ET

# 11/2/23 Added the function covertToUtc which lives in the file timeConverter.py
# This code was written by chatGPT.

from timeConverter import convertToUtc  # Import the function from your module

# As of 2018-08-29 the variable 'fileList' is NOT used in the program.

fileList = (os.listdir('xml_files'))

# Count is the number of objects that have been identifed. The variable is
# initialized to 0 here.

count = 0

dateTime = datetime.today()
nowPT    = Time (dateTime, scale='utc')

print ('nowPT        : ', nowPT, 'PT')
print ('nowPT.jd     : ', nowPT.jd )
dateTimeUTC = datetime.utcnow()

# This will search for 4 days (timedelta(4))

# Set start and end time. Doing this from the command line would be
# a good idea. For now, I just modify the file.

startTimePDT = datetime(2024, 12, 19, 0, 0, 0)  # Local time, adjust as needed
timezone_str = 'America/Los_Angeles'  # Example timezone (Eastern Time Zone)

startTimeUTC = convertToUtc(startTimePDT, timezone_str)

endTimePDT = datetime(2024, 12, 25, 0, 0, 0)  # Local time, adjust as needed
endTimeUTC = convertToUtc(endTimePDT, timezone_str)

# Debug print statements

print ('startTimeUTC    : ', startTimeUTC)
print ('endTimeUTC      : ', endTimeUTC)
print ('startTimeUTC.jd : ', startTimeUTC.jd)
print ('endTimeUTC.jd   : ', endTimeUTC.jd)

# Setting the morning and evening times - assuming local time but they may in fact be in UT
# These times do need to be adjusted to UTC as that is how everthing is calculated

observingMorningTime = '06'
observingEveningTime = '16'

print ('Hardwire minMagCutoff, minAltCutoff, and minPlanetStarAreaRatio to 10.0 0.0 0.01')

minMagCutoff           = 10.75
minAltCutoff           = 10.0
minPlanetStarAreaRatio = 0.01

# minMagCutoff           = input ('Enter minimum magnitude  : ')
# minAltCutoff           = input ('Enter minimum altitude   : ')
# minPlanetStarAreaRatio = input ('Enter minimum area ratio : ')

# This reads into 'file' all of the files in the xml_files directory

# Start of the for loop looping over all of the xml files.

for file in os.listdir('xml_files'):

# Because of the way I set my the xml_files directory all of the files
# are xml files

# This if statement may not in fact be necessary. Need to confirm this.
# Since all of the files in the directory xml_files are guarenteed to have
# the extension .xml this check below is unnecessary and if I move sufficient code
# into functions I will try and optimize this a little.

    if fnmatch.fnmatch(file, '*.xml'):
        
        tree = ET.parse ('xml_files/'+file)
        root = tree.getroot()

# Look for a star field in the xml - if there isn't raise an exception. This
# exception is not having in the current set of xml files.

        try: 
            star = tree.find('.//star')
        except:
            print ('tree.find raised an exception')
            print ('file name: ', file)

# Look through all of the possible planets in a system.

        try:
            tmpX = star.findall('.//planet')
        except:
            print ('star.findall raised an exception.')
            print ('file name: ', file)
            
# Start of for loop, looping over all of the planets within the system
            
        for planet in star.findall('.//planet'):

# Only look at planets that are transitting

            if planet.findtext ('istransiting') == '1':

# Get the magntiude of the star. Use the visual magnitude if it is available.
# If not, use the 'B' magnitude and if that isn't available use the
# 'J' magnitude. If none of these are avaiable use 20.0 as the magnitude.

                if star.findtext('magV') != None:
                    mag = star.findtext('magV')
                else:
                    if star.findtext('magB') != None:
                        mag = star.findtext('magB')
                    else:
                        if star.findtext('magJ') != None:
                            mag = star.findtext('magJ')
                        else:
                            if star.findtext('magR') != None:
                                mag = star.findtext('magR')
                            else:
                                if star.findtext('magI') != None:
                                    mag = star.findtext('magI')
                                else:
                                    if star.findtext('magH') != None:
                                        mag = star.findtext('magH')
                                    else:
                                        if star.findtext('magK') != None:
                                            mag = star.findtext('magK')
                                        else:
#                                            print ('Did not find a magnitude in the xml file')
#                                            print ('Is transiting ?: ', planet.findtext('istransiting'))
#                                            print ('xml file: ', file)
                                            mag = 20.0

# End of magnitude check, use a magnitude of 20 if there isn't anything in
# the xml file.

                planetPeriod = planet.findtext('period')

                # Look for a valid looking period, one that is not ''
                # nore 'None'.
            
                if planetPeriod != '' and planetPeriod != None:

                    planetPeriod = float(planetPeriod)

                    if planet.findtext('transittime') != None:

                        firstTimeInCountTransit = True;

# why is the maxCountTransit set to 801?

                        maxCountTransit = 801
                        for countTransit in range(maxCountTransit):
                            
# These two times, transitTimeBJD and transitTime are identical times.
# Need to pick out just one for the code.

# The transit time in the .xml file has the units of BJD. I'm not sure how to
# check this field to make sure I'm getting the time correct.

                            transitTime = float(
                                planet.findtext('transittime'))
                            transitTimeBJD = Time(transitTime,
                                               format = 'jd',
                                               scale='utc')

# 'now' is the current time. Not sure why I'm using the current time and not
# the range of time specified in the time range.
# It seems like this should be the start of the time range.

# Trying to eliminate the use of transitTime and replacing with transitTimeBJD.jd

                            deltaDays  = startTimeUTC.jd - transitTimeBJD.jd;

#                           print ('type of startTimeUTC.jd : ', type(startTimeUTC.jd))
                            revolutionCount = deltaDays / planetPeriod

# Add the number of countTransit to the intRevolutionCount. This starts at 0
# and keeps incrementing until timeLessThanEnd becomes false. Until I come up
# with something better when this event is detected I'll set countTransit
# to 100.

                            intRevolutionCount = int(revolutionCount) + 1 + countTransit
                            
                            nextTransit = transitTimeBJD + \
                                (intRevolutionCount * planetPeriod)

                            x = Time.__add__(transitTimeBJD,\
                                (intRevolutionCount * planetPeriod))

                            nextTransitTime = Time (nextTransit,
                                                    format ='jd',
                                                    scale = 'utc');

                            daysToTransit = nextTransit - startTimeUTC.jd

#
# Change the time to PT by subtracting 8 hours (7 during DTS) from the UTC time
# nextTransit time 'should' be in UTC and this is converted to PT via a subtraction.
# Look into doing this via a function.

                            nextTransitTimePT = nextTransit - (1.0/24.0*8.0)
                            nTTPT = Time (nextTransitTimePT,
                                          format='jd',
                                          scale='utc')

                            starRadius   = star.findtext('radius')
                            if (starRadius == None):
                                starRadius = float(0.0)
                            else:
                                starRadius    = float(starRadius) * \
                                    1.3914      * \
                                    1000000

                            try:
                                planetRadius   = planet.findtext('radius')
                            except:
                                print ('planet.findtext(radius) failed')
                                print ('file name: ', file)
                            
                            if (planetRadius == None):
                                planetRadius = 0.0
                            else:
                                try:
                                    planetRadius = float(planetRadius) * 139822
                                except:
                                    print ('float(planetRadius) failed')
                                    print ('file name: ', file)
                                
                            if (starRadius != 0) and (planetRadius != 0):
                                starArea            = cmath.pi   * \
                                    starRadius * \
                                    starRadius
                                planetArea          = cmath.pi     * \
                                    planetRadius * \
                                    planetRadius
                                planetStarAreaRatio = planetArea / starArea
                            else:
                                planetStarAreaRatio = 0
                            
                            a = nextTransitTimePT.jd
                            b = nowPT.jd + 1
                            c = a < b

# Look at the start and end times of the transitting period.

                            if nTTPT.jd > startTimeUTC.jd:
                                timeGreaterThanstartTimeUTC = True
                            else:
                                timeGreaterThanstartTimeUTC = False

# Look for the end time to be exceeded. If it has break out of the loop.

                            if nTTPT.jd < endTimeUTC.jd:
                                timeLessThanendTimeUTC = True
                            else:
                                timeLessThanendTimeUTC = False
                                break

# This 'if' statement is looking for the condition where the maxCount was not set
# high enough for the time interval and the short period of a planet. If this
# is reported then the maxCount should be set higher.

                            if countTransit == maxCountTransit-1:
                                print ('Count transit = (maxCountTransit-1)')
                                print ('countTransit : ', countTransit)
                                
                            if timeGreaterThanstartTimeUTC & timeLessThanendTimeUTC:
                                withinTimeRange = True
                            else:
                                withinTimeRange = False

# e = sideral_time('apparent',longitude=None,model=None)

                            observingPosition = EarthLocation(lat   = (34+(49/60)+(32/3600))  * u.deg,
                                                              lon   =-(119+(1/60)+(27/3600))  * u.deg,
                                                              height=1621*u.m)  

                            observingNextTransitTime = Time(nextTransitTime.fits)


# Eliminate objects based on
# a) magnitude of the star must be great the 11th magnitude,
# b) planetStarRatio at least 0.01,
# c) variable 'd' (poorly named) is not true, that is the object will be
#    eliminated if the transit is
#    not within the specified time range
# d) altitude of the object is not at least 10 degrees above the horizon
# e) transit happens during daylight hours, between 4 & 18 time.
# Still need to only output if the transit happens at night.

                            aa = AltAz(location=observingPosition,
                                       obstime=observingNextTransitTime)

                            ra = root.findtext('rightascension')
                            dec = root.findtext('declination')
                            
                            raHrMinSec   = ra[0:2]   + 'h' + ra[3:5]  + 'm' + \
                                           ra[6:8]   + 's'
                            decDegMinSec = dec[0:3]  + 'd' + dec[4:6] + 'm' + \
                                           dec[8:10] + 's'
                            
                            skyCoord = SkyCoord (raHrMinSec + ' ' + \
                                                 decDegMinSec,
                                                 frame='icrs')

                            altAzi = skyCoord.transform_to(
                                AltAz(obstime=observingNextTransitTime,
                                      location=observingPosition))

# Looking for hour of transit (PT). For now day time is between
# 06 and 17 hours. Night would be defined as true if we are not in
# this range:

                            hour = nTTPT.fits[11:13];

                            if (hour > observingMorningTime and
                                hour < observingEveningTime):
                                night = False
                            else:
                                night = True

# Debugging:
#                            if root.findtext('name') == 'HD 56414':
#                                print ('******* DEBUGGING *******')
#                                print ('countTransit                : ', countTransit)
#                                print ('revolutionCount             : ', revolutionCount)
#                                print ('intRevolutionCount          : ', intRevolutionCount)
#                                print ('deltaDays                   : ', deltaDays)
#                                print ('startTimeUTC                : ', startTimeUTC)
#                                print ('startTimeUTC.jd             : ', startTimeUTC.jd)
#                                print ('startTimeUTC.fits           : ', startTimeUTC.fits)
#                                print ('transitTimeBJD              : ', transitTimeBJD)
#                                print ('nextTransitTime             : ', nextTransitTime)
#                                print ('daysToTransit               : ', daysToTransit)
#                                print ('nTTPT                       : ', nTTPT.fits)
#                                print ('Period                      : ', planet.findtext('period'))
#                                print ('Is transiting?              : ',
#                                       planet.findtext('istransiting'))
#                                print ('timeGreaterThanstartTimeUTC : ', timeGreaterThanstartTimeUTC)
#                                print ('timeLessThanendTimeUTC      : ', timeLessThanendTimeUTC)
#                                print ('withinTimeRange             : ', withinTimeRange)
#                                print ('planetStarAreaRatio         : ', planetStarAreaRatio)
#                                print ('altitude                    : ', altAzi.alt.degree)
#                                print ('******* DEBUGGING *******')
# Debugging

# Debugging
#                            night                  =  True
#                            minPlanetStarAreaRatio =   0.0003
#                            minAltCutoff           = -30
# Debugging

                            if (float(mag) < float(minMagCutoff))                     and \
                               withinTimeRange                                        and \
                               (planetStarAreaRatio >= float(minPlanetStarAreaRatio)) and \
                               (altAzi.alt.degree > float(minAltCutoff))              and \
                               night:
                                count = count + 1

                                print ('------------------')

                                print ('file name                : ', file)

# Debugging:
                                print ('countTransit             : ', countTransit)
                                print ('intRevolutionCount       : ', intRevolutionCount)
# End of debugging print statements

                                namesOfStar = star.findall("name")
                                for x in range(len(namesOfStar)):
                                    print ('Star name ', x+1, '            : ', namesOfStar[x].text)

                                namesOfPlanet = planet.findall("name")

                                for x in range(len(namesOfPlanet)):
                                    print ('Planet name ', x+1, '          : ', namesOfPlanet[x].text)

                                print ('Planet period            : ',  \
                                       "{:.4f}".format(float(planet.findtext('period'))))
                                
                                print ('transitTimeBJD           : ', transitTimeBJD)
                                print ('transitTimeBJD.datetime  : ', transitTimeBJD.to_datetime())

                                print ('System Right Ascension   :  ', \
                                       root.findtext('rightascension'))

                                print ('System Declination       : ',  \
                                       root.findtext('declination'))

                                print ('System Magnitude         : ',  \
                                       "{:.1f}".format(float(mag)))

                                print ('observingNextTransitTime : ',  \
                                       nTTPT.fits, 'PT')

                                print ('Azimuth                  : ',  \
                                       "{:.2f}".format(altAzi.az.degree))

                                print ('Altitude                 : ',  \
                                       "{:.2f}".format(altAzi.alt.degree))

                                print ('Days until transit       : ',  \
                                       "{:.2f}".format(daysToTransit.jd))
                            
                                print ('Planet/Star area ratio   : ',  \
                                       "{:.3f}".format(planetStarAreaRatio))

                                print ('count                    : ',  \
                                       count)

                                print ('Description              : ',  \
                                       planet.findtext('description'))


