# Written by Rob Steele

# The goal of this program is to scan all of the trasiting exoplanets
# and search for ones that are visible during the night times hours
# from my location.

# On Dec. 13, 2022 I moved the logic for updating the xml files out of this
# program and put that logic in the 'updateXmlFiles.py' program.

from astropy import units as u

import astropy.time
from astropy.time import Time
from astropy.time import TimeDelta

from astropy.coordinates import EarthLocation,SkyCoord
from astropy.coordinates import AltAz

# This is a whack, 10/10/22 at removing an error due to being offline
# Need to look into determining how to detect when I"m offline and only use
# this logic under those conditions.

# from astropy.utils.iers import conf
# conf.auto_max_age = None

# Start of the rest of my old code, that worked when online

import cmath
import subprocess

from datetime import timedelta
from datetime import date
from datetime import datetime

import fnmatch

import os

import time

import xml.etree.ElementTree as ET


# As of 2018-08-29 the variable 'fileList' is NOT used in the program.

fileList = (os.listdir('xml_files'))

# Count is the number of objects that have been identifed. The variable is
# initialized to 0 here.

count = 0

# Set up by grabbing the current date and then using the Time object
# from astropy.time

dateTime = datetime.today()
nowPT    = Time (dateTime, scale='utc')

print ('nowPT        : ', nowPT, 'PT')

dateTimeUTC = datetime.utcnow()
nowUTC      = Time (dateTimeUTC, scale='utc')

print ('nowUTC       : ', nowUTC, 'UTC')

# This will search for 4 days (timedelta(4))

startTime = Time(datetime.now(),              scale='utc')
endTime   = Time(datetime.now()+timedelta(4), scale='utc')

# Overwritting the start and end times with hard wired number is done
# below. This logic can be commented out when unnecessary.

startTime = Time(datetime(2022,12,18,0,0,0), scale='utc')
endTime   = Time(datetime(2022,12,23,0,0,0), scale='utc')

print ('startTime    : ', startTime)
print ('endTime      : ', endTime)

observingMorningTime = '04'
observingEveningTime = '16'

print ('Hardwire minMagCutoff, minAltCutoff, and minPlanetStarAreaRatio to 10.0 0.0 0.01')

minMagCutoff           = 10.75
minAltCutoff           = 10.0
minPlanetStarAreaRatio = 0.008

#minMagCutoff           = input ('Enter minimum magnitude  : ')
#minAltCutoff           = input ('Enter minimum altitude   : ')
#minPlanetStarAreaRatio = input ('Enter minimum area ratio : ')

# This reads into 'file' all of the files in the xml_files directory

for file in os.listdir('xml_files'):
    
#    print ("Debugging, file: ", file)
    
# Because of the way I set my the xml_files directory all of the files
# are xml files

# This if statement may not in fact be necessary. Need to confirm this.

    if fnmatch.fnmatch(file, '*.xml'):
        
        tree = ET.parse ('xml_files/'+file)
        root = tree.getroot();

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
            
        for planet in star.findall('.//planet'):
            if planet.findtext ('istransiting') == '1':

# Check for HAT-P-1 as that one is a good one to check the rest of the logic.

# Debugging
#                if root.findtext('name') == 'HAT-P-1':
#                    print ('Did find HAT-P-1')
#                    print ('Period              : ', planet.findtext('period'))
#                    transitTimeBJD = float(planet.findtext('transittime'))
#                    print ('Transit Time BJD    : ', transitTimeBJD)
#                    transitTime = Time(transitTimeBJD,
#                                       format = 'jd',
#                                       scale  = 'utc')
#                    transitTime = transitTime - (1.0/24.0*8.0)
#                    print ('Transit Time        : ',
#                           transitTime.fits)
# Debugging

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
                                            mag = 20.0

                planetPeriod = planet.findtext('period')

                # Look for a valid looking period, one that is not ''
                # nore 'None'.
            
                if planetPeriod != '' and planetPeriod != None:

                    planetPeriod = float(planetPeriod)

                    if planet.findtext('transittime') != None:

# These two times, transitTimeBJD and transitTime are identical times.
# Need to pick out just one for the code.

# Debugging:
#                        if root.findtext('name') == 'HAT-P-1':
#                            print ('planetPeriod        : ', planetPeriod)
# Debugging:

                        transitTimeBJD = float(
                                           planet.findtext('transittime'))
                        transitTime = Time(transitTimeBJD,
                                           format = 'jd',
                                           scale='utc')

# 'now' is the current time. Not sure why I'm using the current time and not
# the range of time specified in the time range.
# It seems like this should be the start of the time range.

                        delta  = nowUTC.jd - transitTimeBJD;

                        revolutionCount = delta / planetPeriod

# Debugging:
#                        if root.findtext('name') == 'HAT-P-1':
#                            print ('revolutionCount     : ', revolutionCount)
# Debugging:
                        
                        intRevolutionCount = int(revolutionCount) + 1

#                        print 'delta              : ', delta
#                        print 'revolutionCount    : ', revolutionCount
#                        print 'intRevolutionCount : ', intRevolutionCount
                        
                        nextTransit = transitTimeBJD + \
                                      (intRevolutionCount * planetPeriod)

                        nextTransitTime = Time (nextTransit,
                                                format ='jd',
                                                scale = 'utc');

                        daysToTransit = nextTransit - nowUTC.jd


#
# Change the time to PT by subtracting 8 hours (7 during DTS) from the UTC time
#

                        nextTransitTimePT = nextTransit - (1.0/24.0*8.0)
                        nTTPT = Time (nextTransitTimePT,
                                       format='jd',
                                       scale='utc')
# Debugging:
#                        if root.findtext('name') == 'HAT-P-1':
#                            print ('nextTransitTime     : ', nextTransitTime)
#                            print ('daysToTransit       : ', daysToTransit)
#                            print ('nTTPT               : ', nTTPT.fits)
# Debugging:

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
                            
                        a = nextTransitTimePT
                        b = nowPT.jd + 1
                        c = a < b

# d start off as false and is det to true if the time is in the specifed
# time range

                        d = False
                        
                        if nTTPT.jd > startTime.jd:
                            if nTTPT.jd < endTime.jd:
                                d = True

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

# Debugging
#                        night = True
#                        minAltCutoff = -90
# Debugging

# Debugging:
#                        if root.findtext('name') == 'HAT-P-1':
#                            print ('d                   : ', d)
#                            print ('planetStarAreaRatio : ', planetStarAreaRatio)
#                            print ('altitude            : ', altAzi.alt.degree)
# Debugging:

                        if (float(mag) < float(minMagCutoff))                     and \
                           d                                                      and \
                           (planetStarAreaRatio >= float(minPlanetStarAreaRatio)) and \
                           (altAzi.alt.degree > float(minAltCutoff))              and \
                           night:
                            count = count + 1

                            print ('------------------')

                            print ('file name                : ', file)

                            print ('System name              : ',  \
                                   root.findtext('name'))

                            print ('Planet name              : ',  \
                                   planet.findtext('name'))

                            print ('Planet period            : ',  \
                                   "{:.1f}".format(float(planet.findtext('period'))))

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
                                   "{:.2f}".format(daysToTransit))
                            
                            print ('Planet/Star area ratio   : ',  \
                                   "{:.3f}".format(planetStarAreaRatio))

                            print ('count                    : ',  \
                                   count)

                            print ('Description              : ',  \
                                   planet.findtext('description'))

