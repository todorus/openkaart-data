import psycopg2

conn = psycopg2.connect("dbname=openkaart_development user=scraper")
conn.set_client_encoding("UTF8")
cur = conn.cursor()

# cur.execute('CREATE TABLE postalcodes_to_municipalities (id serial PRIMARY KEY, municipality_id integer, postalcode_id integer, UNIQUE (municipality_id, postalcode_id))')
relations = []
cur.execute("SELECT * FROM postalcodes_to_municipalities")

for record in cur:
    print record



cur.close()
conn.close()
