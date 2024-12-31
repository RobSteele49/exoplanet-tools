from astroquery.exoplanet_orbit_database import ExoplanetOrbitDatabase

table = ExoplanetOrbitDatabase.query_planet ('Kepler-107b')

print ("About to print the table")
print (table)
print ("Done printing the table")


