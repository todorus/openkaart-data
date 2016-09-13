import json
import geojson
import psycopg2
from shapely.geometry import shape

conn = psycopg2.connect("dbname=openkaart_development user=scraper")
cur = conn.cursor()

print "postalcodes that are not matched:"
cur.execute("SELECT * FROM postal_codes WHERE id NOT IN (SELECT postalcode_id FROM postalcodes_to_municipalities)")
for record in cur:
    print record

cur.close()
conn.close()
