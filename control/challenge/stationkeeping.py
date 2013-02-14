'''
Created on Jan 19, 2013

@author: joshandrews
'''
import math
import control.logic.standardcalc as standardcalc
import control.datatype.datatypes as datatypes

def setBoxCoords(tL, tR, bL, bR): #sets coords of box so that topleft is most west point of the two most northern points
    top1 = 0.0
    top2 = 0.0
    topindex1 = 0
    topindex2 = 0
    index = 0
    coordList = [tL, tR, bL, bR]
    for coord in coordList:
        if (coord.lat > top1):
            top1 = coord.lat
            topindex1 = index
        else:
            if (coord.lat > top2):
                top2 = coord.lat
                topindex2 = index
            elif (coord.lat == top2): #edge case: if box forms diamond with respect to true north, choose left side as top face
                if (coord.long < top2):
                    top2 = coord.lat
                    topindex2 = index
        index += 1
    return

def lineintersect():            
    
    return

def stationKeepInit(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord):
    boxCoords = setBoxCoords(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord)
    
    northAngle = standardcalc.angleBetweenTwoCoords(topLeftCoord, topRightCoord)  # angle of top face to true north
    eastAngle = standardcalc.angleBetweenTwoCoords(topRightCoord, botRightCoord) - 90  # angle of right face to true east
    
    distBtwnCrnr = standardcalc.distBetweenTwoCoords(topLeftCoord, topRightCoord)/2.0

    if (northAngle < 90):
        #90 - northAngle
        northTriangleAngle = 90 - northAngle
        x=1
    elif (northAngle > 90):
        #northAngle - 90
        x=1
    else:
        northWayPnt = standardcalc.GPSDistAway(topLeftCoord, distBtwnCrnr, 100) #north face faces true north, want way point 100m away and square is 60m per side
        eastWayPnt = standardcalc.GPSDistAway(topRightCoord, 100, -distBtwnCrner)
def run():
    return 0
