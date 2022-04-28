from ast import arg
import tokenize, os, sys


class Connection:
    def __init__(self, direction : str, name1: str, name2 : str, offset: int):
        self.direction = direction
        self.name1 = name1
        self.name2 = name2
        self.offset = offset


class MapHeader:
    def __init__(self, name1 : str, name2 : str, tileset : str, connections : list()):
        self.name1 = name1
        self.name2 = name2
        self.tileset = tileset
        self.connections = connections

    def toString(self) -> str:
        out = "\n\tmap_header " + self.name1 + ", " + self.name2 + ", " + self.tileset + ", "
        connectstring = "0"
        if len(self.connections) > 0:
            connectstring = ""
            for con in self.connections:
                connectstring += con.direction.upper()
                if self.connections[-1] == con:
                    continue
                connectstring += " | "
        out += connectstring + "\n"
        for con in self.connections:
            out += "\tconnection " + con.direction.lower() + ", " + con.name1 + ", " + con.name2 + ", " + str(con.offset) + "\n"
        out += "\tend_map_header\n"
        return out

def readMapHeader(file : str) -> MapHeader:
    lines = file.split("\n")
    name1 = ""
    name2 = ""
    tileset = ""
    connections = list()
    for line in lines:
        if "map_header " in line:
            line = line.replace("\tmap_header ", "")
            args = line.split(", ")
            if len(args) != 4:
                sys.exit("error reading file: wrong number of arguments")
            name1 = args[0]
            name2 = args[1]
            tileset = args[2]
        if "connection " in line and " ; unnecessary" not in line:
            line = line.replace("\tconnection ", "")
            line = line.replace(" ; unnecessary", "")
            args = line.split(", ")
            if len(args) != 4:
                sys.exit("error reading file: wrong number of arguments")
            connections.append(Connection(args[0], args[1], args[2], int(args[3])))
    return MapHeader(name1, name2, tileset, connections)

