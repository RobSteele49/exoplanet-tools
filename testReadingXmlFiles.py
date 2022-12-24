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

        
tree = ET.parse ('xml_files/HAT-P-1.xml')
root = tree.getroot();

# Look for a star field in the xml - if there isn't raise an exception. This
# exception is not having in the current set of xml files.

star = tree.find('.//star')

namesOfStar = star.findall("name")

for x in range(len(namesOfStar)):
    print ('Star name ', x+1, ' : ', namesOfStar[x].text)

print ('new stuff')

planet = star.findall('.//planet')
namesOfPlanet = planet[0].findall("name")

for x in range(len(namesOfPlanet)):
    print ('Planet name ', x+1, ' : ', namesOfPlanet[x].text)

