'''
Created on Jan 19, 2013

@author: joshandrews
'''
import math
import sailbot.logic.standardcalc as standardcalc
import sailbot.datatype.datatypes as datatypes

def lineintersect(coord):
    return

def stationKeepInit(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord):  # assume topleft is most west point of the two most northern points
    northAngle = standardcalc.angleBetweenTwoCoords(topLeftCoord, topRightCoord)  # angle of top face to true north
    eastAngle = standardcalc.angleBetweenTwoCoords(topRightCoord, botRightCoord) - 90  # angle of right face to true east

    if (northAngle < 90):
        #90 - northAngle
        break
    elif (northAngle > 90):
        #northAngle - 90
        break
    else:
        #northWayPnt = datatypes.GPSCoordinate(topLeftCoord.long+, t)
        break
def run():
    return 0
