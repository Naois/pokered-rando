from hashlib import new
import os, shutil, sys
from random import Random
import random
from xmlrpc.client import Boolean
import MapHeader
import CheckConnectedness
import BasicLogic

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

filedir = os.path.dirname(os.path.realpath(__file__))

os.chdir(filedir + "/../data/maps/")

cwd = os.getcwd()

print("Maps folder located at: \"" + cwd + "\"")

shutil.rmtree("headers", True)

carl = Random()

if len(sys.argv) > 1:
    carl.seed(sys.argv[1])

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

def getPos(name: str, dir: str) -> int:
    if not os.path.exists("headers_clean/" + name + ".meta"):
        return None
    metafile = open("headers_clean/" + name + ".meta", "r")
    entries = metafile.read().split("\n")
    for entry in entries:
        if dir in entry:
            return int(entry.replace(dir, "").replace("=", ""))

def isOverworld(header: MapHeader.MapHeader) -> Boolean:
    return "OVERWORLD" == header.tileset

headerfiles = os.listdir("headers_clean")
headerlist = list()
southlist = list()
northlist = list()
eastlist = list()
westlist = list()
for file in headerfiles:
    current = open("headers_clean/" + file, "r")
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

if len(southlist) != len(northlist):
    sys.exit("north and south connections don't match")
if len(eastlist) != len(westlist):
    sys.exit("east and west connections don't match")

southlistbackup = southlist[:]
westlistbackup = westlist[:]

loopcounter = 1

while True:
    connectionlist: str = ""

    for bottom in northlist:
        top = bottom
        counter = 0
        while top == bottom and counter < 100: #Tries to avoid a map looping onto itself, but it may fail if it's the last remaining map, hence the counter
            top = southlist[carl.randint(0, len(southlist)-1)]
            counter += 1
        southlist.remove(top)
        botpos = getPos(bottom.name1, "north")
        toppos = getPos(top.name1, "south")
        topcon = getSouth(top)
        botcon = getNorth(bottom)
        topcon.name1 = bottom.name1
        topcon.name2 = bottom.name2
        topcon.offset = -int((botpos - toppos)/2)
        botcon.name1 = top.name1
        botcon.name2 = top.name2
        botcon.offset = int((botpos - toppos)/2)
        connectionlist += "Made north-south connection: {}-{}\n".format(top.name1, bottom.name1)

    for left in eastlist:
        right = left
        counter = 0
        while right == left and counter < 100:
            right = westlist[carl.randint(0, len(westlist)-1)]
            counter += 1
        westlist.remove(right)
        lefpos = getPos(left.name1, "east")
        rigpos = getPos(right.name1, "west")
        rigcon = getWest(right)
        lefcon = getEast(left)
        rigcon.name1 = left.name1
        rigcon.name2 = left.name2
        rigcon.offset = -int((lefpos - rigpos)/2)
        lefcon.name1 = right.name1
        lefcon.name2 = right.name2
        lefcon.offset = int((lefpos - rigpos)/2)
        connectionlist += "Made east-west connection: {}-{}\n".format(right.name1, left.name1)
    
    filedir = os.path.dirname(os.path.realpath(__file__)) + "/connectionlist.txt"

    open(filedir, "w").write(connectionlist)

    # if CheckConnectedness.checkConnection(CheckConnectedness.makeGraph(), "PalletTown"):
    #     break

    if BasicLogic.logic():
        break

    southlist = southlistbackup[:]
    westlist = westlistbackup[:]
    print(loopcounter)
    loopcounter += 1

print("Made completable map after {} attempts.".format(loopcounter))

os.makedirs("headers")

for header in headerlist:
    open("headers/" + header.name1 + ".asm", "w").write(header.toString())
