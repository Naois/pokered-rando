

from distutils.dep_util import newer
import os, sys
from platform import node


nodeset = {"PalletTown", "PalletDex", "Route1", "ViridianCity-South", "ViridianCity-West", "ViridianCity-North",
            "Route2", "Route2-Cave", "Route11", "PewterCity", "Route3", "Route4-South", "Route4-East",
            "CeruleanCity-West", "CeruleanCity-North", "CeruleanCity-East", "CeruleanCity-South",
            "CeruleanCity-Bike", "Route5-North", "Route5-South", "Route6-North", "Route6-South", "Route7-East",
            "Route7-West", "Route8-East", "Route8-West", "Route9-West", "Route9-East", "Route10",
            "Route24", "Route25", "LavenderTown", "Poketower", "VermilionCity", "VermilionGym", "SSAnne",
            "Route11", "Route12-North", "Route12-West", "Route12-South", "Route13", "Route14", "Route15",
            "FuchsiaCity", "CinnabarIsland", "Route17", "Route16-East", "Route16-South", "Route16-Mid",
            "Route18-East", "Route18-North", "Route19-North", "Route19-West", "Route20-West", "Route20-East",
            "Route21-South", "Route21-North", "Route22", "CeladonCity", "CeladonGym", "SaffronCity", "SaffronGym"
            }

initialEdges = {("ViridianCity-South", "ViridianCity-West"), ("ViridianCity-West", "ViridianCity-South"),
                #Old man makes Viridian city one way
                ("ViridianCity-North", "ViridianCity-South"),
                #Diglett's cave
                ("Route2-Cave", "Route11"),
                #Route4 contains a ledge which can only be bypassed using surf
                ("Route4-South", "Route4-East"),
                #In cerulean city, it is possible to get between west and north, and between east and south,
                #but there is a ledge leading from the east into the central area, making it one-way. This can be bypassed
                #by talking to bill or getting cut (which requires talking to bill.)
                ("CeruleanCity-West", "CeruleanCity-North"), ("CeruleanCityEast", "CeruleanCity-South"),
                ("CeruleanCity-North", "CeruleanCity-West"), ("CeruleanCity-South", "CeruleanCityEast"),
                ("CeruleanCity-East", "CeruleanCity-West"),
                #Route 5 can only be passed south to north, and Route 6 south to north, until you give a drink to a guard
                ("Route5-South", "Route5-North"), ("Route6-North, Route6-South"),
                #Route 7 east to west, Route 8 west to east, as above
                ("Route7-East", "Route7-West"), ("Route8-West", "Route8-East"),
                #Saffron city underpasses
                ("Route5-North", "Route6-South"), ("Route6-South", "Route5-North"),
                ("Route7-West", "Route8-East"), ("Route8-East", "Route7-West"),
                #Bike Gates are one way until you get the bike
                ("Route16-South", "Route16-Mid"), ("Route18-North", "Route18-East")
                }
surfStrengthEdges = {   #Route4 contains a ledge which can only be bypassed using surf
                        ("Route4-East", "Route4-South"),
                        #You can surf to the vermilion gym
                        ("VermilionCity", "VermilionGym"), ("VermilionGym", "VermilionCity"),
                        #Surf allows you to go north-south on Route12
                        ("Route12-North", "Route12-South"), ("Route12-South", "Route12-North"),
                        #Surf is needed for Routes 19, 20, 21, and Strength is needed for Route 20
                        ("Route19-North", "Route19-West"), ("Route19-West", "Route19-North"),
                        ("Route20-West", "Route20-East"), ("Route20-East", "Route20-West"),
                        ("Route21-South", "Route21-North"), ("Route21-North", "Route21-South")
                    }
billEdges = {   
                #Helping Bill gets the guard to move
                ("CeruleanCity-West", "CeruleanCity-East"),
                #Bill gives you the SS. Anne ticket
                ("VermilionCity", "SSAnne"), ("SSAnne", "VermilionCity")
            }
cutEdges = {#Cut allows you to bypass the old man
            ("ViridianCity-South", "ViridianCity-North"),
            #Cut allows you to go between diglett's cave and the rest of route 2
            ("Route2", "Route2-Cave"), ("Route2-Cave", "Route2"),
            #Cut allows you to reach the south and west exits of cerulean
            ("CeruleanCity-West", "CeruleanCity-East"),
            #Cut is needed to traverse route 9
            ("Route9-East", "Route9-West"), ("Route9-West", "Route9-East"),
            #Cut allows you to access the Vermilion Gym
            ("VermilionCity", "VermilionGym"), ("VermilionGym", "VermilionCity"),
            #Cut required to get to the Celadon Gym
            ("CeladonCity", "CeladonGym"), ("CeladonGym", "CeladonCity")
            }
drinkEdges = {  #Gates can be passed through once guards have been given drinks.
                ("Route5-South", "Route5-North"), ("Route6-South", "Route6-North"),
                ("Route7-West", "Route7-East"), ("Route8-East", "Route8-West")
}
fluteEdges = {  #Pokeflute allows you to get rid of the snorlax on route 12
                ("Route12-North", "Route12-South"), ("Route12-South", "Route12-North"),
                ("Route12-North", "Route12-West"), ("Route12-West", "Route12-North"),
                #And on route 18
                ("Route16-Mid", "Route16-East"), ("Route16-East", "Route16-Mid"),
                #Need flute to beat Silph Co. to access Saffron Gym
                ("SaffronCity", "SaffronGym"), ("SaffronGym", "SaffronCity")
}
silphScopeEdges = {("LavenderTown", "Poketower"), ("Poketower", "LavenderTown")}
bikeVoucherEdges = {("CeruleanCity-West", "CeruleanCity-Bike"), ("CeruleanCity-Bike", "CeruleanCity-West")}
bikeEdges = {   #Bike lets you through bike gates
                ("Route16-Mid", "Route16-South"), ("Route18-East", "Route18-North")
            }
dexEdges = {("ViridianCity-South", "ViridianCity-North")}
#Currently there is a shortcoming in my code in that the player might be able to reach Viridian to get the parcel but not get back to Pallet.
#Death abuse is recommended in this case, if possible.
#I'm keeping this functionality for the purpose of future-proofing, in case I implement a backtracking algorithm *shudders*
parcelEdges = {("PalletTown", "PalletDex"), ("PalletDex", "PalletTown")}

essentialNodes = {
    #First requirement is to get all the gyms
    "PewterCity", "CeruleanCity-West", "SaffronGym", "VermilionGym", "CeladonGym", "FuchsiaCity", "CinnabarIsland", "ViridianCity-West",
    #Access to Route 22, strength and surf
    "Route22", "FuchsiaCity"
}

def makeGraph() -> set:
    filedir = os.path.dirname(os.path.realpath(__file__)) + "/connectionlist.txt"

    connections = open(filedir, "r").read().split("\n")
    edgeset = set()

    for connection in connections:
        if "Made north-south connection: " in connection:
            pair = connection.replace("Made north-south connection: ", "").split("-")
            if pair[0] not in nodeset and pair[0] + "-South" not in nodeset:
                sys.exit("missing {} from logic".format(pair[0] + "-South"))
            if pair[1] not in nodeset and pair[1] + "-North" not in nodeset:
                sys.exit("missing {} from logic".format(pair[1] + "-North"))
            if pair[0] not in nodeset:
                pair[0] += "-South"
            if pair[1] not in nodeset:
                pair[1] += "-North"
            edgeset.add((pair[0], pair[1]))
            edgeset.add((pair[1], pair[0]))
        if "Made east-west connection: " in connection:
            pair = connection.replace("Made east-west connection: ", "").split("-")
            if pair[0] not in nodeset and pair[0] + "-West" not in nodeset:
                sys.exit("missing {} from logic".format(pair[0] + "-West"))
            if pair[1] not in nodeset and pair[1] + "-East" not in nodeset:
                sys.exit("missing {} from logic".format(pair[1] + "-East"))
            if pair[0] not in nodeset:
                pair[0] += "-West"
            if pair[1] not in nodeset:
                pair[1] += "-East"
            edgeset.add((pair[0], pair[1]))
            edgeset.add((pair[1], pair[0]))
    return edgeset

def logic():
    randomEdges = makeGraph()
    reachable = set()
    edges = initialEdges.copy()
    edges = edges.union(randomEdges)
    newReachable = {"PalletTown"}
    while len(newReachable) > 0:
        newnewreachable = set()
        for pair in edges:
            if pair[0] in newReachable:
                newnewreachable.add(pair[1])
        reachable = reachable.union(newReachable)
        newReachable = newnewreachable.difference(reachable)
        flag = False
        if "FuchsiaCity" in newReachable:
            flag = True
            edges = edges.union(surfStrengthEdges)
        if "Route25" in newReachable:
            flag = True
            edges = edges.union(billEdges)
        if "SSAnne" in newReachable:
            flag = True
            edges = edges.union(cutEdges)
        if "CeladonCity" in newReachable:
            flag = True
            edges = edges.union(drinkEdges)
        if "Poketower" in newReachable:
            flag = True
            edges = edges.union(fluteEdges)
        if "CeladonCity" in newReachable:
            flag = True
            edges = edges.union(silphScopeEdges)
        if "VermilionCity" in newReachable:
            flag = True
            edges = edges.union(bikeVoucherEdges)
        if "CeruleanCity-Bike" in newReachable:
            flag = True
            edges = edges.union(bikeEdges)
        if "PalletDex" in newReachable:
            flag = True
            edges = edges.union(dexEdges)
        if "ViridianCity-South" in newReachable:
            flag = True
            edges = edges.union(parcelEdges)
        
        if flag:
            newReachable = reachable.union(newReachable)
            reachable = set()
    return essentialNodes.issubset(reachable)
