
from unicodedata import name
import MapHeader, os, shutil

from xmlrpc.client import Boolean

filedir = os.path.dirname(os.path.realpath(__file__))

os.chdir(filedir + "/../data/maps/")

cwd = os.getcwd()

print("Maps folder located at: \"" + cwd + "\"")

def isSouth(header: MapHeader.MapHeader) -> Boolean:
    return getSouth(header) != None

def isNorth(header: MapHeader.MapHeader) -> Boolean:
    return getNorth(header) != None

def isEast(header: MapHeader.MapHeader) -> Boolean:
    return getEast(header) != None

def isWest(header: MapHeader.MapHeader) -> Boolean:
    return getWest(header) != None

def getSouth(header: MapHeader.MapHeader) -> MapHeader.Connection:
    for con in header.connections:
        if con.direction == "south":
            return con
    return None

def getNorth(header: MapHeader.MapHeader) -> MapHeader.Connection:
    for con in header.connections:
        if con.direction == "north":
            return con
    return None

def getEast(header: MapHeader.MapHeader) -> MapHeader.Connection:
    for con in header.connections:
        if con.direction == "east":
            return con
    return None

def getWest(header: MapHeader.MapHeader) -> MapHeader.Connection:
    for con in header.connections:
        if con.direction == "west":
            return con
    return None

def isOverworld(header: MapHeader.MapHeader) -> Boolean:
    return "OVERWORLD" == header.tileset

headerfiles = os.listdir("headers")
headerlist = list()
southlist = list()
northlist = list()
eastlist = list()
westlist = list()
for file in headerfiles:
    current = open("headers/" + file, "r")
    newheader = MapHeader.readMapHeader(current.read())
    headerlist.append(newheader)
    if not isOverworld(newheader):
        continue
    if isNorth(newheader):
        northlist.append(newheader)
    if isSouth(newheader):
        southlist.append(newheader)
    if isEast(newheader):
        eastlist.append(newheader)
    if isWest(newheader):
        westlist.append(newheader)

for north in northlist:
    if getNorth(north).name1 == north.name1:
        print("North-South loop: {}".format(north.name1))
    for south in southlist:
        if getNorth(north).name1 == south.name1:
            if getSouth(south).name1 != north.name1:
                print("North-South does not match: {}-{}".format(north.name1, south.name1))
            break

for south in southlist:
    if getSouth(south).name1 == south.name1:
        print("South-North loop: {}".format(south.name1))
    for north in northlist:
        if getSouth(south).name1 == north.name1:
            if getNorth(north).name1 != south.name1:
                print("South-North does not match: {}-{}".format(south.name1, north.name1))
            break

for east in eastlist:
    if getEast(east).name1 == east.name1:
        print("East-West loop: {}".format(east.name1))
    for west in westlist:
        if getEast(east).name1 == west.name1:
            if getWest(west).name1 != east.name1:
                print("East-West does not match: {}-{}".format(east.name1, west.name1))
            break

for west in westlist:
    if getWest(west).name1 == west.name1:
        print("West-East loop: {}".format(west.name1))
    for east in eastlist:
        if getWest(west).name1 == east.name1:
            if getEast(east).name1 != west.name1:
                print("West-East does not match: {}-{}".format(west.name1, east.name1))
            break

