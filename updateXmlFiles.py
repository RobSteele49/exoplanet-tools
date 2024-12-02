# Written by Rob Steele

# This program updates the xml_files. I've removed this logic from the
# 'predictTransit.py' program since there really isn't a need to update
# the xml files every time I run the predictTransit program.

import subprocess
import os
import platform

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

if platform.system() == 'Linux':
    print("Running on Linux 1")
    subprocess.getstatusoutput ('del xml_files/*')
    subprocess.getstatusoutput ('mkdir xml_files')
    # Do something specific for Linux
elif platform.system() == 'Windows':
    print("Running on Windows 1")
    # Do something specific for Windows
    subprocess.getstatusoutput ('rmdir xml_files')
    subprocess.getstatusoutput ('mkdir xml_files')

if platform.system() == 'Linux':
    print("Running on Linux 2")
elif platform.system() == 'Windows':
    print("Running on Windows 2") 
    copyCommand = 'copy ..\\OpenExoplanetCatalogue\\open_exoplanet_catalogue\\systems\\*.xml xml_files\\ '
    subprocess.getstatusoutput (copyCommand)
    copyCommand = 'copy ..\\OpenExoplanetCatalogue\\open_exoplanet_catalogue\\systems_kepler\\*.xml xml_files\\ '
    subprocess.getstatusoutput (copyCommand)

if platform.system() == 'Linux':
    print("Running on Linux 3")
    subprocess.getstatusoutput ('rm xml_files/EPIC?201637175.xml')
    subprocess.getstatusoutput ('rm xml_files/KIC?12557548.xml')
    subprocess.getstatusoutput ('rm xml_files/SDSS?J1110+0116.xml')
    subprocess.getstatusoutput ('rm xml_files/PSO?J318?5-22.xml')
    subprocess.getstatusoutput ('rm xml_files/SIMP0136+0933.xml')
    subprocess.getstatusoutput ('rm xml_files/CFBDSIR2149.xml')
    subprocess.getstatusoutput ('rm xml_files/WISE?0855-0714.xml')
    subprocess.getstatusoutput ('rm xml_files/EPIC?204129699.xml')
    # Do something specific for Linux
elif platform.system() == 'Windows':
    print("Running on Windows 3")
    subprocess.getstatusoutput ('del xml_files\\CFBDSIR2149.xml')
    subprocess.getstatusoutput ('del xml_files\\EPIC?201637175.xml')
    subprocess.getstatusoutput ('del xml_files\\KIC?12557548.xml')
    subprocess.getstatusoutput ('del xml_files\\SDSS?J1110+0116.xml')
    subprocess.getstatusoutput ('del xml_files\\PSO*J318*5*22.xml')
    subprocess.getstatusoutput ('del xml_files\\SIMP0136+0933.xml')
    subprocess.getstatusoutput ('del xml_files\\CFBDSIR2149.xml')
    subprocess.getstatusoutput ('del xml_files\\WISE?0855-0714.xml')
    subprocess.getstatusoutput ('del xml_files\\EPIC?204129699.xml')
    subprocess.getstatusoutput ('del xml_files\\KOI-2700.xml')





