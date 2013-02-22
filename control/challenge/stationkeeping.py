'''
Created on Jan 19, 2013

@author: joshandrews
'''
import math
import control.logic.standardcalc as standardcalc
import control.GlobalVars as GlobalVars
import control.StaticVars as StaticVars

def findCosLawAngle(a, b, c):  #cos law: c^2 = a^2 + b^2 - 2*a*b*cos(theta):
    return math.acos((math.pow(a, 2) + math.pow(b, 2) - math.pow(c, 2)) / (2*a*b))

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
    else:                                             #tilted right square
        return coordList
    return finalCoordList

def stationKeepInit(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord):
    boxCoords = setBoxCoords(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord)
    if (GlobalVars.timerSet == True):
        run(boxCoords)
    return

def run(boxCoords):
    while (timer != 0):
        TL2Boat = standardcalc.distBetweenTwoCoords(GlobalVars.currentData[StaticVars.GPS_INDEX], boxCoords[0]) #top left to boat
        TR2Boat = standardcalc.distBetweenTwoCoords(GlobalVars.currentData[StaticVars.GPS_INDEX], boxCoords[1]) #top right to boat
        BR2Boat = standardcalc.distBetweenTwoCoords(GlobalVars.currentData[StaticVars.GPS_INDEX], boxCoords[2]) #bottom right to boat
        TL2TR = standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1]) #top left to top right
        TR2BR = standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2]) #top right to bottom right
        
        topLeftAngle = findCosLawAngle(TL2TR, TL2Boat, TR2Boat)
        rightTopAngle = findCosLawAngle(TR2BR, TR2Boat, BR2Boat)
        
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
    return