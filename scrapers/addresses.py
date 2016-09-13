import json
import geojson
from shapely.geometry import shape
from scraper import FileScraper, WFSScraper
import logging

class AddressFileScraper(FileScraper):

    def write(self, json_string, page):
        writeToDb(self.conn, self.cur, json_string)


class AddressWFSScraper(WFSScraper):

    def writeToDb(self, json_string):
        writeToDb(self.conn, self.cur, json_string)


def writeToDb(connection, cursor, json_string):
    data = json.loads(json_string)
    features = data["features"]
    affectedRows = 0
    for feature in features:
        properties = feature["properties"]

        geometry_dump = json.dumps(feature["geometry"])
        geometry_geojson = geojson.loads(geometry_dump)
        geometry_wkt = shape(geometry_geojson).wkt

        cursor.execute("""
        INSERT INTO postalcodes_to_municipalities (municipality_id, postalcode_id)
        SELECT municipalities.id, postal_codes.id
        FROM municipalities, postal_codes
        WHERE ST_CONTAINS(municipalities.geometry, ST_GeomFromText(%s))
        AND postal_codes.name = %s
        ON CONFLICT DO NOTHING
        """, (geometry_wkt, properties["postcode"][0:4]))
        affectedRows += cursor.rowcount
    connection.commit()
    logging.info("inserted connection count: %d" % (affectedRows,))
