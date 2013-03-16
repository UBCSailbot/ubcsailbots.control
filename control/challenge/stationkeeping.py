'''
Created on Jan 19, 2013

@author: joshandrews
'''
import math
import sys
sys.path.append("..")
from datetime import datetime
import control.logic.standardcalc as standardcalc
import control.GlobalVars as gVars
import control.StaticVars as sVars
from control.logic import coresailinglogic
import thread

def setWayPtCoords(boxCoords): #sets the waypoints of the challenge
    wayPtCoords = []    #order = top face, right face, bottom face, left face
    if (boxCoords[0].lat == boxCoords[1].lat):    #square
        wayPtCoords[0] = standardcalc.GPSDistAway(boxCoords[0], 20.0, 100.0)
        wayPtCoords[1] = standardcalc.GPSDistAway(boxCoords[1], 100.0, -20.0)
        wayPtCoords[2] = standardcalc.GPSDistAway(boxCoords[2], -20.0, -100.0)
        wayPtCoords[3] = standardcalc.GPSDistAway(boxCoords[3], -100.0, 20.0)
    elif (boxCoords[0].lat < boxCoords[1].lat):     #diamond or tilted left square
        cAngle = standardcalc.angleBetweenTwoCoords(boxCoords[0],boxCoords[1])
        wayPntDist1 = 100.0*math.cos(cAngle)
        wayPntDist2 = 100.0*math.sin(cAngle)
        midDist1 = 20.0*math.cos(90 - cAngle)
        midDist2 = 20.0*math.sin(90 - cAngle)
        
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
        midDist1 = 20.0*math.cos(90 - cAngle)
        midDist2 = 20.0*math.sin(90 - cAngle)
        
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

def SKTimer():
    gVars.SKMinLeft = ((datetime.now() - gVars.taskStartTime ).seconds) / 60
    gVars.SKSecLeft = ((datetime.now() - gVars.taskStartTime ).seconds) - gVars.SKMinLeft*60
    gVars.SKMilliSecLeft = ((datetime.now() - gVars.taskStartTime).microseconds) / 1000

def getBoxDist(boxCoords):
    boxDistList = []  #top, right, bottom, left
    TL2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData[sVars.GPS_INDEX], boxCoords[0]) #top left to boat
    TR2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData[sVars.GPS_INDEX], boxCoords[1]) #top right to boat
    BR2Boat = standardcalc.distBetweenTwoCoords(gVars.currentData[sVars.GPS_INDEX], boxCoords[2]) #bottom right to boat
    TL2TR = standardcalc.distBetweenTwoCoords(boxCoords[0], boxCoords[1]) #top left to top right
    TR2BR = standardcalc.distBetweenTwoCoords(boxCoords[1], boxCoords[2]) #top right to bottom right
        
    topLeftAngle = standardcalc.findCosLawAngle(TL2TR, TL2Boat, TR2Boat)
    rightTopAngle = standardcalc.findCosLawAngle(TR2BR, TR2Boat, BR2Boat)
        
    boxDistList[0] = TL2Boat * math.sin(topLeftAngle)   #top dist
    boxDistList[1] = TR2Boat * math.sin(rightTopAngle)   #right dist
    boxDistList[2] = 40 - boxDistList[0] #bottom dist
    boxDistList[3] = 40 - boxDistList[1] #left dist
    return boxDistList

def stationKeepInit(topLeftWaypnt, topRightWaypnt, botLeftWaypnt, botRightWaypnt):
    topLeftCoord = topLeftWaypnt.coordinate
    topRightCoord = topRightWaypnt.coordinate
    botLeftCoord = botLeftWaypnt.coordinate
    botRightCoord = botRightWaypnt.coordinate
    boxCoords = setBoxCoords(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord)   #boxCoords[0] = TL, boxCoords[1] = TR, boxCoords[2] = BR, boxCoords[3] = BL
    wayPtCoords = setWayPtCoords(boxCoords)  #top, right, bottom, left
    spdList = [0.75]*10
    boxDistList = getBoxDist(boxCoords)  #top, right, bottom, left
    meanSpd = 0.75
    arduino = gVars.arduino
    gVars.SKCurrentWaypnt = boxDistList.index(min(boxDistList))
    thread.start_new_thread(coresailinglogic.pointToPoint, boxCoords[gVars.SKCurrentWaypnt])
    run(boxCoords, wayPtCoords, spdList, meanSpd, arduino)
    return
    
def run(boxCoords, wayPtCoords, spdList, meanSpd, arduino):
    while ((datetime.now() - gVars.taskStartTime).seconds < 300):
        secLeft = 300 - (datetime.now() - gVars.taskStartTime).seconds
        turning = 0
        SKTimer();
        boxDistList = getBoxDist(boxCoords)
        if (standardcalc.isWPNoGo(gVars.currentData[sVars.AWA_INDEX],gVars.currentData[sVars.HOG_INDEX], gVars.SKCurrentWaypnt, gVars.currentData[sVars.SOG_INDEX], gVars.currentData[sVars.GPS_INDEX])):
            gVars.SKCurrentWaypnt = (gVars.SKCurrentWaypnt + 1) % 4
            gVars.kill_flag = 1
            thread.start_new_thread(coresailinglogic.pointToPoint, boxCoords[gVars.SKCurrentWaypnt])
            turning = 1
        if (boxDistList[gVars.SKCurrentWaypnt] < 5):
            gVars.SKCurrentWaypnt = (gVars.SKCurrentWaypnt + 2) % 4
            gVars.kill_flag = 1
            if (gVars.currentData[sVars.AWA_INDEX] < 0):
                arduino.gybe(1)
            else:
                arduino.gybe(0)
            thread.start_new_thread(coresailinglogic.pointToPoint, boxCoords[gVars.SKCurrentWaypnt])
            turning = 1
        if (turning == 0):
            spdList = standardcalc.changeSpdList(spdList)
            meanSpd = standardcalc.meanOfList(spdList)
        if (boxDistList[gVars.SKCurrentWaypnt] >= meanSpd*(secLeft+2)):  #leeway of 2 seconds
            break
        elif (boxDistList[(gVars.SKCurrentWaypnt + 2) % 4] >= meanSpd*(secLeft+2+4) ): #leeway of 2 seconds, 4 seconds for gybe
            gVars.SKCurrentWaypnt = (gVars.SKCurrentWaypnt + 2) % 4
            gVars.kill_flag = 1
            if (gVars.currentData[sVars.AWA_INDEX] < 0):
                arduino.gybe(1)
            else:
                arduino.gybe(0)
            thread.start_new_thread(coresailinglogic.pointToPoint, boxCoords[gVars.SKCurrentWaypnt])
            break

    boxDistList = getBoxDist(boxCoords)
    '''gVars.SKMinLeft = 0
    gVars.SKSecLeft = 0
    gVars.SKMilliSecLeft = 0'''
    
    gVars.SKCurrentWaypnt = None
    
    return