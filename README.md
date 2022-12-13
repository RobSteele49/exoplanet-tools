# exoplanet-tools

Tools for manipulating the open_exoplanet_catalog. The open_exoplanet_catalog
will reside in this repository as a submodule.

To clone this repository and get the populated open_exoplanet_catlog
directory/repository use the command:

git clone --recurse-submodules https://github.com/steelewool/exoplanet-tools.git

2022-12-13

Moved the creation of the XML files from predictTransit.py to updateXmlFiles.py.
This way I only create the XML files after I've updated the Open_Exoplanet
directory.

