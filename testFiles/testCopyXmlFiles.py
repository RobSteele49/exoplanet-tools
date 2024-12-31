# Written by Rob Steele


import cmath
import subprocess

from datetime import timedelta
from datetime import date
from datetime import datetime

import fnmatch

import os

import time

import xml.etree.ElementTree as ET

# This section of code creates a directory 'xml_files' and then creates
# softlinks to the xml files. in the open_exoplanet_catalogue in the
# The goal of this program is to scan all of the trasiting exoplanets
# and search for ones that are visible during the night times hours
# from my location.

# I was to eventually develop a GUI for this program. But for now the
# funcionality will live in this code.

# astropy.time is not working on my Raspberry Pi.
# This is issue # 3 and more details can be found there.

# This section of code creates a directory 'xml_files' and then creates
# softlinks to the xml files. in the open_exoplanet_catalogue in the
# systems and systems_kepler directories. This was done because I could not
# figure out how to scan though the list of xml files from two directories.
# The other side benefit was that I could remove xml files that were
# causing my program to crash.

subprocess.getstatusoutput ('ls')
subprocess.getstatusoutput ('rm -rf xml_files')
subprocess.getstatusoutput ('mkdir xml_files')

# The creation of software links was not working for me.

# subprocess.getstatusoutput ('cd xml_files; ln -s ../../OpenExoplanetCatalogue/open_exoplanet_catalogue/systems/* .;cd ..')
# subprocess.getstatusoutput ('cd xml_files; ln -s ../../OpenExoplanetCatalogue/open_exoplanet_catalogue/systems_kepler/* .;cd ..')

subprocess.getstatusoutput ('cd xml_files; cp ../../OpenExoplanetCatalogue/open_exoplanet_catalogue/systems/*        .;cd ..')
subprocess.getstatusoutput ('cd xml_files; cp ../../OpenExoplanetCatalogue/open_exoplanet_catalogue/systems_kepler/* .;cd ..')

subprocess.getstatusoutput ('rm xml_files/EPIC?201637175.xml')
subprocess.getstatusoutput ('rm xml_files/KIC?12557548.xml')
subprocess.getstatusoutput ('rm xml_files/SDSS?J1110+0116.xml')
subprocess.getstatusoutput ('rm xml_files/PSO?J318?5-22.xml')
subprocess.getstatusoutput ('rm xml_files/SIMP0136+0933.xml')
subprocess.getstatusoutput ('rm xml_files/CFBDSIR2149.xml')
subprocess.getstatusoutput ('rm xml_files/WISE?0855-0714.xml')
subprocess.getstatusoutput ('rm xml_files/EPIC?204129699.xml')

# This creates a list of all of the files in systems and systems_kepler.
# If I can get this working in the 'for file' I won't need the silly
# softlinks

# As of 2018-08-29 the variable 'fileList' is NOT used in the program.

fileList = (os.listdir('xml_files'))

# Count is the number of objects that have been identifed. The variable is
# initialized to 0 here.

count = 0

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
                    print ('planetPeriod : ', planetPeriod)
                    print ('name         : ', planet.findtext('name'))



