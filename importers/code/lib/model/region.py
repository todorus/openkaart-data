from enum import Enum
from py2neo import Graph, Node, Relationship, NodeSelector
import json


ZIP = u"Zip"
POSTAL_AREA = u"PostalArea"
PLACE = u"Place"
MUNICIPALITY = u"Municipality"
PROVINCE = u"Province"
CARE = u"Care"


def new(graph, definition):
    # py2neo does not support dictionary properties, so convert it to json
    if 'geometry' in definition:
        definition["geometry"] = json.dumps(definition["geometry"])
    node = Node("Region", **definition)
    return node


def create(graph, definition):
    # py2neo does not support dictionary properties, so convert it to json
    if 'geometry' in definition:
        definition["geometry"] = json.dumps(definition["geometry"])
    node = new(graph, definition)
    return graph.create(node)


def createAll(graph, node_definitions):
    transaction = graph.begin()
    for definition in node_definitions:
        node = new(graph, definition)
        transaction.create(node)

    transaction.commit()


def exists(graph, definition):
    return len(match(graph, definition)) > 0


def match(graph, definition):
    selector = NodeSelector(graph)
    result = list(selector.select("Region", **definition))
    return result


def find(graph, definition):
    results = match(graph, definition)
    if len(results) == 0:
        return None
    else:
        return results[0]


def search(graph, query=None, limit=10, page=1):
    skip = (page - 1) * limit

    result = None
    count = None
    if query is not None:
        query = '(?i)%s.*' % (query)

        result = graph.run(
            '''
            MATCH (n:Region)
            WHERE n.name =~ {query}
            RETURN n
            ORDER BY LOWER(n.name), length(n.name) ASC
            SKIP {skip}
            LIMIT {limit}
            ''',
            query=query, skip=skip, limit=limit
        )
        count = graph.run(
            '''
            MATCH (n:Region)
            WHERE n.name =~ {query}
            RETURN count(n) as count
            ''',
            query=query
        )
    else:
        result = graph.run(
            '''
            MATCH (n:Region)
            RETURN n
            ORDER BY LOWER(n.name), length(n.name) ASC
            SKIP {skip}
            LIMIT {limit}
            ''',
            skip=skip, limit=limit
        )
        count = graph.run(
            '''
            MATCH (n:Region)
            RETURN count(n) as count
            '''
        )

    count = count.evaluate()
    return result, count


def readCursor(cursor):
    data = []

    while cursor.forward():
        values = dict(cursor.current().values()[0])
        if 'geometry' in values:
            values["geometry"] = json.loads(values["geometry"])
        data.append(values)

    return data
