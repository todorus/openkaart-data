import tables
import psycopg2

conn = psycopg2.connect("dbname=openkaart_development user=scraper")
cur = conn.cursor()

tables.municipalities(conn, cur)
tables.postalcodes(conn, cur)
tables.postalcodes_to_municipalities(conn, cur)

cur.close()
conn.close()
