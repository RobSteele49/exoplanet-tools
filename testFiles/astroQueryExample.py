from astroquery.simbad import Simbad

from astroquery.exoplanet_orbit_database import ExoplanetOrbitDatabase

table = Simbad.query_object ('M *', wildcard=True, verbose=False, get_query_payload=False)

table.pprint()

print (table[49])

table = ExoplanetOrbitDatabase.query_planet ('Kepler-107b')

print (table)

from astroquery import open_exoplanet_catalogue as oec
from astroquery.open_exoplanet_catalogue import findvalue

cata = oec.get_catalogue()

# tree was not defined in this code:
# star = tree.find(".//star")

# As of 2024 Dec 19 the findvalue function was not working

for planet in oec.findvalue(".//planet"):
    print (findvalue (planet, 'name'))
           
