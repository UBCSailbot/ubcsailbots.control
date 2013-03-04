'''
Created on Jan 19, 2013

@author: joshandrews
'''
import math
from datetime import datetime
import control.logic.standardcalc as standardcalc
import control.GlobalVars as GlobalVars
import control.StaticVars as StaticVars

def setWayPtCoords(boxCoords): #sets the waypoints of the challenge
    wayPtCoords = []    #order = top face, right face, bottom face, left face
    if (boxCoords[0].lat == boxCoords[1].lat):    #square
        wayPtCoords[0] = standardcalc.GPSDistAway(boxCoords[0], 30.0, 100.0)
        wayPtCoords[1] = standardcalc.GPSDistAway(boxCoords[1], 100.0, -30.0)
        wayPtCoords[2] = standardcalc.GPSDistAway(boxCoords[2], -30.0, -100.0)
        wayPtCoords[3] = standardcalc.GPSDistAway(boxCoords[3], -100.0, 30.0)
    elif (boxCoords[0].lat < boxCoords[1].lat):     #diamond or tilted left square
        cAngle = standardcalc.angleBetweenTwoCoords(boxCoords[0],boxCoords[1])
        wayPntDist1 = 100.0*math.cos(cAngle)
        wayPntDist2 = 100.0*math.sin(cAngle)
        midDist1 = 30.0*math.cos(90 - cAngle)
        midDist2 = 30.0*math.sin(90 - cAngle)
        
        topMidpnt = standardcalc.GPSDistAway(boxCoords[0], midDist1, midDist2)
        rightMidpnt = standardcalc.GPSDistAway(boxCoords[1], midDist2, -midDist1)
        botMidpnt = standardcalc.GPSDistAway(boxCoords[2], -midDist1, -midDist2)
        leftMidpnt = standardcalc.GPSDistAway(boxCoords[3], -midDist2, midDist1)
        wayPtCoords[0] = standardcalc.GPSDistAway(topMidpnt, -wayPntDist1, wayPntDist2)
        wayPtCoords[1] = standardcalc.GPSDistAway(rightMidpnt, wayPntDist2, wayPntDist1)
        wayPtCoords[2] = standardcalc.GPSDistAway(botMidpnt, wayPntDist1, -wayPntDist2)
        wayPtCoords[3] = standardcalc.GPSDistAway(leftMidpnt, -wayPntDist2, -wayPntDist1)
    else:    #right tilted square
        cAngle = 180 - standardcalc.angleBetweenTwoCoords(boxCoords[0],boxCoords[1])
        wayPntDist1 = 100.0*math.cos(cAngle)
        wayPntDist2 = 100.0*math.sin(cAngle)
        midDist1 = 30.0*math.cos(90 - cAngle)
        midDist2 = 30.0*math.sin(90 - cAngle)
        
        topMidpnt = standardcalc.GPSDistAway(boxCoords[0], midDist1, -midDist2)
        rightMidpnt = standardcalc.GPSDistAway(boxCoords[1], -midDist2, -midDist1)
        botMidpnt = standardcalc.GPSDistAway(boxCoords[2], -midDist1, midDist2)
        leftMidpnt = standardcalc.GPSDistAway(boxCoords[3], midDist2, midDist1)
        wayPtCoords[0] = standardcalc.GPSDistAway(topMidpnt, wayPntDist1, wayPntDist2)
        wayPtCoords[1] = standardcalc.GPSDistAway(rightMidpnt, wayPntDist2, -wayPntDist1)
        wayPtCoords[2] = standardcalc.GPSDistAway(botMidpnt, -wayPntDist1, -wayPntDist2)
        wayPtCoords[3] = standardcalc.GPSDistAway(leftMidpnt, -wayPntDist2, wayPntDist1)
        
    return wayPtCoords

def setBoxCoords(tL, tR, bL, bR): #sets coords of box so that topleft is most west point of the two most northern points
    coordHalf1 = [tL, tR]
    coordHalf2 = [bL, bR]
    coordList = []
    finalCoordList = []
    if (coordHalf1[1].lat > coordHalf1[0].lat):
        firstCoordHalf = [coordHalf1[1], coordHalf1[0]]
    if (coordHalf2[1].lat > coordHalf2[0].lat):
        secondCoordHalf = [coordHalf1[1], coordHalf1[0]]
        
    if (firstCoordHalf[0].lat >= secondCoordHalf[0].lat):  #mergesort
        coordList.append(firstCoordHalf[0])
        if (firstCoordHalf[1].lat >= secondCoordHalf[0].lat):
            coordList.append(firstCoordHalf[1])
            coordList.append(secondCoordHalf[0])
            coordList.append(secondCoordHalf[1])
        else:
            coordList.append(secondCoordHalf[0])
            if(firstCoordHalf[1].lat >= secondCoordHalf[1].lat):
                coordList.append(firstCoordHalf[1])
                coordList.append(secondCoordHalf[1])
            else:
                coordList.append(secondCoordHalf[1])
                coordList.append(firstCoordHalf[1])
    else:
        coordList.append(secondCoordHalf[0])
        if (firstCoordHalf[0].lat < secondCoordHalf[1].lat):
            coordList.append(secondCoordHalf[1])
            coordList.append(firstCoordHalf[0])
            coordList.append(firstCoordHalf[1])
        else:
            coordList.append(firstCoordHalf[0])
            if(firstCoordHalf[1].lat >= secondCoordHalf[1].lat):
                coordList.append(firstCoordHalf[1])
                coordList.append(secondCoordHalf[1])
            else:
                coordList.append(secondCoordHalf[1])
                coordList.append(firstCoordHalf[1])
    
    if (coordList[0].lat == coordList[1].lat):      #square
        if (coordList[0].long < coordList[1].long):
            finalCoordList.append(coordList[0])
            finalCoordList.append(coordList[1])
        else:
            finalCoordList.append(coordList[1])
            finalCoordList.append(coordList[0])
        if (coordList[2].long < coordList[3].long):
            finalCoordList.append(coordList[3])
            finalCoordList.append(coordList[2])
        else:
            finalCoordList.append(coordList[2])
            finalCoordList.append(coordList[3])
    elif (coordList[1].long < coordList[2].long):  #tilted left square or diamond
        finalCoordList.append(coordList[1])
        finalCoordList.append(coordList[0])
        finalCoordList.append(coordList[2])
        finalCoordList.append(coordList[3])
        
    elif (coordList[1].lat == coordList[2].lat):        #diamond 
        finalCoordList.append(coordList[2])
        finalCoordList.append(coordList[0])
        finalCoordList.append(coordList[1])
        finalCoordList.append(coordList[3])
    else:                                             #tilted right square
        finalCoordList.append(coordList[0])
        finalCoordList.append(coordList[1])
        finalCoordList.append(coordList[3])
        finalCoordList.append(coordList[2])
    return finalCoordList

def stationKeepInit(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord):
    boxCoords = setBoxCoords(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord)   #boxCoords[0] = TL, boxCoords[1] = TR, boxCoords[2] = BR, boxCoords[3] = BL
    wayPtCoords = setWayPtCoords(boxCoords)
    GlobalVars.SKStartTime = datetime.now()
    run(boxCoords, wayPtCoords)
    return

def SKTimer():
    GlobalVars.SKMinLeft = ((datetime.now() - GlobalVars.SKStartTime ).seconds) / 60
    GlobalVars.SKSecLeft = ((datetime.now() - GlobalVars.SKStartTime ).seconds) - GlobalVars.SKMinLeft*60
    GlobalVars.SKMilliSecLeft = ((datetime.now() - GlobalVars.SKStartTime).microseconds) / 1000
    
def run(boxCoords, wayPtCoords):
    while ((datetime.now() - GlobalVars.SKStartTime).seconds < 300):
        SKTimer();
        TL2Boat = standardcalc.distBetweenTwoCoords(GlobalVars.currentData[StaticVars.GPS_INDEX], boxCoords[0]) #top left to boat
        TR2Boat = standardcalc.distBetweenTwoCoords(GlobalVars.currentData[StaticVars.GPS_INDEX], boxCoords[1]) #top right to boat
        BR2Boat = standardcalc.distBetweenTwoCoords(GlobalVars.currentData[StaticVars.GPS_INDEX], boxCoords[2]) #bottom right to boat
        TL2TR = standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1]) #top left to top right
        TR2BR = standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2]) #top right to bottom right
        
        topLeftAngle = standardcalc.findCosLawAngle(TL2TR, TL2Boat, TR2Boat)
        rightTopAngle = standardcalc.findCosLawAngle(TR2BR, TR2Boat, BR2Boat)
        
        topDist = TL2Boat * math.sin(topLeftAngle)
        rightDist = TR2Boat * math.sin(rightTopAngle)
        
        if ((topDist < 5) or (topDist > 95)):
            #jibe
            print "jibe"
        elif ((rightDist < 5) or (rightDist > 95)):
            #jibe
            print "jibe"
        #perhaps keep track of which side heading to.
        #need to figure time it takes to do turn
        #need to add if statements for which sides closest to
    GlobalVars.SKMinLeft = 0
    GlobalVars.SKSecLeft = 0
    GlobalVars.SKMilliSecLeft = 0
    return