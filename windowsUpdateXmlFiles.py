# Written by Rob Steele

# This program updates the xml_files. I've removed this logic from the
# 'predictTransit.py' program since there really isn't a need to update
# the xml files every time I run the predictTransit program.

import subprocess
import os

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

subprocess.getstatusoutput ('rmdir xml_files')
subprocess.getstatusoutput ('mkdir xml_files')

systemFileList = (os.listdir('../open_exoplanet_catalogue/systems'))

for file in systemFileList:
    copyCommand = "cp ../open_exoplanet_catalogue/systems/'" + file + "' xml_files/"
    #print (copyCommand)
    subprocess.getstatusoutput (copyCommand)

systemKeplerFileList = (os.listdir('../open_exoplanet_catalogue/systems_kepler'))

for file in systemKeplerFileList:
    copyCommand = "cp ../open_exoplanet_catalogue/systems_kepler/'" + file + "' xml_files/"
    #print (copyCommand)
    subprocess.getstatusoutput (copyCommand)

subprocess.getstatusoutput ('rm xml_files/EPIC?201637175.xml')
subprocess.getstatusoutput ('rm xml_files/KIC?12557548.xml')
subprocess.getstatusoutput ('rm xml_files/SDSS?J1110+0116.xml')
subprocess.getstatusoutput ('rm xml_files/PSO?J318?5-22.xml')
subprocess.getstatusoutput ('rm xml_files/SIMP0136+0933.xml')
subprocess.getstatusoutput ('rm xml_files/CFBDSIR2149.xml')
subprocess.getstatusoutput ('rm xml_files/WISE?0855-0714.xml')
subprocess.getstatusoutput ('rm xml_files/EPIC?204129699.xml')

