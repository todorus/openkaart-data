import psycopg2
from shapely.geometry import shape
import os.path
import logging

def municipalities(conn, cur):
    logging.info("(re)creating municipalities")
    cur.execute("DROP TABLE IF EXISTS municipalities")
    cur.execute('CREATE TABLE municipalities (id serial PRIMARY KEY, code integer, name varchar, "geometry" geometry, UNIQUE (code))')
    conn.commit()

def postalcodes(conn, cur):
    logging.info("(re)creating postalcodes")
    cur.execute("DROP TABLE IF EXISTS postal_codes")
    cur.execute("CREATE TABLE postal_codes (id serial PRIMARY KEY, name varchar, UNIQUE (name))")

    logging.info("inserting postal4 codes")
    for number in range(0, 10000):
        name = str(number).zfill(4)
        data = (name,)
        cur.execute("INSERT INTO postal_codes (name) VALUES (%s) ON CONFLICT DO NOTHING", data)
    conn.commit()

def postalcodes_to_municipalities(conn, cur):
    logging.info("(re)creating postalcodes_to_municipalities")
    cur.execute("DROP TABLE IF EXISTS postalcodes_to_municipalities")
    cur.execute('CREATE TABLE postalcodes_to_municipalities (id serial PRIMARY KEY, municipality_id integer, postalcode_id integer, UNIQUE (municipality_id, postalcode_id))')
    conn.commit()
