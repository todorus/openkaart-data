def init_graph(environment="local"):
    from py2neo import Graph
    import config

    graph = Graph(**config.NEO4J)

    return graph
