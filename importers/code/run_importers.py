import lib.db.setup as db
import lib.model.region as region
import json

graph = db.init_graph()

with open("/data/provincies.geo.json") as raw:
    data = json.load(raw)
    for entry in data:
        node_data = {
            "type": region.PROVINCE,
            "name": entry["properties"]["Provincien"],
            "geometry": entry["geometry"]
        }
        print "creating %s" % node_data["name"].encode("utf-8")
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
