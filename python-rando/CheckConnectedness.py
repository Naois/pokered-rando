import os


def makeGraph() -> dict():

    filedir = os.path.dirname(os.path.realpath(__file__)) + "/connectionlist.txt"

    connections = open(filedir, "r").read().split("\n")

    graph = {
        "Route5" : {"Route6"},
        "Route6" : {"Route5"},
        "Route7" : {"Route8"},
        "Route8" : {"Route7"},
        "Route11" : {"Route2"},
        "Route2" : {"Route11"}
    }

    for connection in connections:
        if "Made north-south connection: " in connection:
            pair = connection.replace("Made north-south connection: ", "").split("-")
            if pair[0] in graph:
                graph[pair[0]].add(pair[1])
            else:
                graph[pair[0]] = set()
                graph[pair[0]].add(pair[1])
            if pair[1] in graph:
                graph[pair[1]].add(pair[0])
            else:
                graph[pair[1]] = set()
                graph[pair[1]].add(pair[0])
        if "Made east-west connection: " in connection:
            pair = connection.replace("Made east-west connection: ", "").split("-")
            if pair[0] in graph:
                graph[pair[0]].add(pair[1])
            else:
                graph[pair[0]] = set()
                graph[pair[0]].add(pair[1])
            if pair[1] in graph:
                graph[pair[1]].add(pair[0])
            else:
                graph[pair[1]] = set()
                graph[pair[1]].add(pair[0])
    return graph


def checkConnection(graph, start):
    oldset = {start}
    newset = graph[start]
    while len(newset) > 0:
        newoldset = oldset.union(newset)
        newnewset = set()
        for a in newset:
            newnewset = newnewset.union(graph[a])
        oldset = newoldset
        newset = newnewset.difference(oldset)

    print("Transitive closure of {} is: \n{}".format(start, oldset))
    print("Full list of map locations: \n{}".format(graph.keys()))
    print("List of inaccessible areas: \n{}".format(set(graph.keys()).difference(oldset)))
    return len(set(graph.keys()).difference(oldset)) == 0