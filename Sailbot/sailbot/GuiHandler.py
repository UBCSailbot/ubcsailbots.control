'''
Created on Jan 21, 2013

@author: joshandrews
'''

from sailbot.datatype import datatypes
import GlobalVar

# Main GUI Handler Function
#    * GUI can call any of these functions and rest will be taken care of

# Run Navigation challenge
# arg must be a tuple in format:
#    TODO
def navigationChallenge(arg):
    GlobalVar.functionQueue.append(GlobalVar.NAVIGATION_CHALLENGE)

# Run Station Keeping challenge
# arg must be a tuple in format:
#    TODO
def stationKeepingChallenge(arg):
    GlobalVar.functionQueue.append(GlobalVar.STATION_KEEPING_CHALLENGE)

# Run Long Distance challenge
# arg must be a tuple in format:
#    TODO
def longDistanceChallenge(arg):
    GlobalVar.functionQueue.append(GlobalVar.LONG_DISTANCE_CHALLENGE)

# Run Point to Point logic
# arg must be a tuple in format:
#    TODO
def pointToPoint(arg):
    GlobalVar.functionQueue.append(GlobalVar.POINT_TO_POINT)

# Run Station Keep logic
# arg must be a tuple in format:
#    TODO
def stationKeep(arg):
    GlobalVar.functionQueue.append(GlobalVar.STATION_KEEP)

# Run Round Buoy logic
# arg must be a tuple in format:
#    TODO
def roundBuoy(arg):
    GlobalVar.functionQueue.append(GlobalVar.ROUND_BUOY)

def setBoundary(coordinate, radius):
    #Boundary format: [<GPSCoordinate>, <radius(float)>]
    GlobalVar.boundaries.append([coordinate, radius])