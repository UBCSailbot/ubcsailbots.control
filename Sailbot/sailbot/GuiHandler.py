'''
Created on Jan 21, 2013

@author: joshandrews
'''

from sailbot.datatype import datatypes
from sailbot import Main

# Main GUI Handler Function
#    * GUI can call any of these functions and rest will be taken care of

# Run Navigation challenge
# arg must be a tuple in format:
#    TODO
def navigationChallenge(arg):
    Main.setFunctionQueue(Main.getFunctionQueue().append(Main.NAVIGATION_CHALLENGE))

# Run Station Keeping challenge
# arg must be a tuple in format:
#    TODO
def stationKeepingChallenge(arg):
    Main.setFunctionQueue(Main.getFunctionQueue().append(Main.STATION_KEEPING_CHALLENGE))

# Run Long Distance challenge
# arg must be a tuple in format:
#    TODO
def longDistanceChallenge(arg):
    Main.setFunctionQueue(Main.getFunctionQueue().append(Main.LONG_DISTANCE_CHALLENGE))

# Run Point to Point logic
# arg must be a tuple in format:
#    TODO
def pointToPoint(arg):
    Main.setFunctionQueue(Main.getFunctionQueue().append(Main.POINT_TO_POINT))

# Run Station Keep logic
# arg must be a tuple in format:
#    TODO
def stationKeep(arg):
    Main.setFunctionQueue(Main.getFunctionQueue().append(Main.STATION_KEEP))

# Run Round Buoy logic
# arg must be a tuple in format:
#    TODO
def roundBuoy(arg):
    Main.setFunctionQueue(Main.getFunctionQueue().append(Main.ROUND_BUOY))

def setBoundary(coordinate, radius):
    #Boundary format: [<GPSCoordinate>, <radius(float)>]
    Main.setBoundaries(Main.getBoundaries().append([coordinate, radius]))