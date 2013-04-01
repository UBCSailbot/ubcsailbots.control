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
import thread
import control.sailbotlogger as SBLogger
from control.logic import coresailinglogic

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
    boxCoords = standardcalc.setBoxCoords(topLeftCoord, topRightCoord, botLeftCoord, botRightCoord)   #boxCoords[0] = TL, boxCoords[1] = TR, boxCoords[2] = BR, boxCoords[3] = BL
    wayPtCoords = setWayPtCoords(boxCoords)  #top, right, bottom, left
    spdList = [0.75]*10
    boxDistList = getBoxDist(boxCoords)  #top, right, bottom, left
    meanSpd = 0.75   #from old arduino code
    arduino = gVars.arduino
    gVars.SKCurrentWaypnt = boxDistList.index(min(boxDistList))
    logger = SBLogger.logger()
    thread.start_new_thread(coresailinglogic.pointToPoint, boxCoords[gVars.SKCurrentWaypnt])
    logger.info("The current waypoint is " + gVars.SKCurrentWaypnt + ". 0 means top, 1 means right, 2 means bottom, 3 means left")
    logger.info("Station Keeping Initialization finished. Now running Station Keeping Challenge")
    run(boxCoords, wayPtCoords, spdList, meanSpd, arduino, logger)
    return
    
def run(boxCoords, wayPtCoords, spdList, meanSpd, arduino, logger):
    exiting = 0
    while (((datetime.now() - gVars.taskStartTime).seconds < 300) and (gVars.kill_flagSK == 0)):
        secLeft = 300 - (datetime.now() - gVars.taskStartTime).seconds
        turning = 0
        SKTimer()
        boxDistList = getBoxDist(boxCoords)
        if (exiting == 0):
            if (standardcalc.isWPNoGo(gVars.currentData[sVars.AWA_INDEX],gVars.currentData[sVars.HOG_INDEX], gVars.SKCurrentWaypnt, gVars.currentData[sVars.SOG_INDEX], gVars.currentData[sVars.GPS_INDEX])):
                logger.info("The boat is sailing upwind. Changing current waypoint.")
                gVars.SKCurrentWaypnt = (gVars.SKCurrentWaypnt + 1) % 4
                logger.info("The current waypoint is " + gVars.SKCurrentWaypnt + ". 0 means top, 1 means right, 2 means bottom, 3 means left")
                gVars.kill_flagPTP = 1
                thread.start_new_thread(coresailinglogic.pointToPoint, boxCoords[gVars.SKCurrentWaypnt])
                turning = 1
            if (boxDistList[gVars.SKCurrentWaypnt] < 5):
                logger.info("The boat is too close to an edge. Changing current waypoint.")
                gVars.SKCurrentWaypnt = (gVars.SKCurrentWaypnt + 2) % 4
                logger.info("The current waypoint is " + gVars.SKCurrentWaypnt + ". 0 means top, 1 means right, 2 means bottom, 3 means left")
                gVars.kill_flagPTP = 1
                logger.info("Commencing gybe.")
                if (gVars.currentData[sVars.AWA_INDEX] < 0):
                    arduino.gybe(1)
                else:
                    arduino.gybe(0)
                thread.start_new_thread(coresailinglogic.pointToPoint, boxCoords[gVars.SKCurrentWaypnt])
                turning = 1
            if (turning == 0):
                spdList = standardcalc.changeSpdList(spdList)
                meanSpd = standardcalc.meanOfList(spdList)
                logger.info("The mean speed of the boat is " + meanSpd + " metres per second.")
            if (boxDistList[gVars.SKCurrentWaypnt] >= meanSpd*(secLeft+2)):  #leeway of 2 seconds
                exiting = 1
                logger.info("Station Keeping event is about to end. Exiting to current waypoint.")
            elif (boxDistList[(gVars.SKCurrentWaypnt + 2) % 4] >= meanSpd*(secLeft+2+4) ): #leeway of 2 seconds, 4 seconds for gybe
                gVars.SKCurrentWaypnt = (gVars.SKCurrentWaypnt + 2) % 4
                gVars.kill_flagPTP = 1
                logger.info("Station Keeping event is about to end. Gybing and exiting to waypoint " + gVars.SKCurrentWaypnt)
                if (gVars.currentData[sVars.AWA_INDEX] < 0):
                    arduino.gybe(1)
                else:
                    arduino.gybe(0)
                thread.start_new_thread(coresailinglogic.pointToPoint, boxCoords[gVars.SKCurrentWaypnt])
                exiting = 1
    if (gVars.kill_flagSK == 1):
        logger.info("Station Keeping Kill Flag initialized. Station Keeping Challenge has been stopped.")
    else:
        logger.info("Station Keeping Challenge timer has ended.")
    boxDistList = getBoxDist(boxCoords)
    gVars.SKMinLeft = 0
    gVars.SKSecLeft = 0
    gVars.SKMilliSecLeft = 0
    gVars.kill_flagSK = 0
    gVars.SKCurrentWaypnt = None
    
    return