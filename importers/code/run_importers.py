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
        print "creating %s" % node_data["name"]
        region.create(graph, node_data)
