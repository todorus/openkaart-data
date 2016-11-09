import lib.db.setup as db
import lib.model.region as region
import lib.model.relations as relations
import json
import csv
from py2neo import Relationship

graph = db.init_graph()

municipality_codes = {}
province_codes = {}

CSV_FILE_NAME ="/data/gemeenten-alfabetisch-2016.csv"
with open(CSV_FILE_NAME, 'rb') as f:
    print "checking csv dialect of %s" % CSV_FILE_NAME
    dialect = csv.Sniffer().sniff(f.readline(), delimiters=';,')
    f.seek(0)
    reader = csv.reader(f, dialect)

    print "read %s into memory" % CSV_FILE_NAME
    next(reader, None)  # skip the headers
    data = list(reader)
    # Gemeentecode;Gemeentenaam;Provincienaam;Provinciecode;
    for entry in data:
        municipality_codes[entry[1]] = int(entry[0])
        province_codes[entry[2]] = int(entry[3])

with open("/data/provincies.geo.json") as raw:
    data = json.load(raw)
    for entry in data:
        name = entry["properties"]["Provincien"]
        code = province_codes[name]
        node_data = {
            "type": region.PROVINCE,
            "name": name,
            "code": code,
            "geometry": entry["geometry"]
        }
        print "creating %s" % json.dumps({"name": node_data["name"], "code": node_data["code"]})
        region.create(graph, node_data)

with open("/data/gemeentes.geo.json") as raw:
    data = json.load(raw)
    for entry in data:
        node_data = {
            "type": region.MUNICIPALITY,
            "name": entry["properties"]["gemeentena"],
            "code": int(entry["properties"]["code"]),
            "geometry": entry["geometry"]
        }
        print "creating %s" % node_data["name"].encode("utf-8")
        region.create(graph, node_data)

with open("/data/postcodes.geo.json") as raw:
    data = json.load(raw)
    for entry in data:
        node_data = {
            "type": region.POSTAL_AREA,
            "name": str(entry["properties"]["PC4"]).decode("utf-8"),
            "code": entry["properties"]["PC4"],
            "geometry": entry["geometry"]
        }
        print "creating %s" % node_data["name"].encode("utf-8")
        region.create(graph, node_data)

with open("/data/postalcode-tabel.json") as raw:
    data = json.load(raw)
    last_postal4 = None
    for entry in data:
        postal4 = entry["postal"]
        if postal4 != last_postal4:
            last_postal4 = postal4.encode("utf-8")
            postal_area = region.find(graph, {"type": region.POSTAL_AREA, "name": postal4})
            municipality = region.find(graph, {"type": region.MUNICIPALITY, "code": entry["municipality_code"]})
            province = region.find(graph, {"type": region.PROVINCE, "code": entry["province_code"]})
            print json.dumps(entry)
            if postal_area is not None:
                if municipality is not None:
                    print "%s -BELONGS_TO-> %s" % (postal_area["name"].encode("utf-8"), municipality["name"].encode("utf-8"))
                    rel = Relationship(postal_area, relations.BELONGS_TO, municipality)
                    graph.create(rel)
                    if province is not None:
                        print "%s -BELONGS_TO-> %s" % (municipality["name"].encode("utf-8"), province["name"].encode("utf-8"))
                        rel = Relationship(municipality, relations.BELONGS_TO, province)
                        graph.create(rel)
                elif province is not None:
                    print "%s -BELONGS_TO-> %s" % (postal_area["name"].encode("utf-8"), province["name"].encode("utf-8"))
                    rel = Relationship(postal_area, relations.BELONGS_TO, province)
                    graph.create(rel)
