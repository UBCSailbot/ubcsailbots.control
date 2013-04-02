'''
Created on Jan 19, 2013

@author: joshandrews
'''
import time
import math
import thread
import sys
sys.path.append("..")
from control.logic import standardcalc
from control.logic import coresailinglogic
from control.datatype import datatypes
from control import GlobalVars as gVars
from control import StaticVars as sVars

hog_index=sVars.HOG_INDEX
cog_index=sVars.COG_INDEX
sog_index=sVars.SOG_INDEX
awa_index=sVars.AWA_INDEX
gps_index=sVars.GPS_INDEX
sht_index=sVars.SHT_INDEX
aut_index=sVars.AUT_INDEX
COMPASS_METHOD = 0
COG_METHOD = 1
AWA_METHOD = 2

HORIZ_BOUNDARY_DISTANCE = 60 

# ---    Navigation Challenge    ---
#Input: Buoy GPS Coordinates (Latitude and Longitude of the Buoy), Left Inner Point (The coordinates of the left innermost gate), Right Inner Point (The coordinates of the right innermost gate)
#Output: None
def run(Waypoint1,Waypoint2,Waypoint3):
    currentData = gVars.currentData
    GPSCoord = currentData[gps_index]
    
    gVars.kill_flagNav = 0
    
    num_nav_first = 0
    num_nav_start_port = 0
    num_nav_start_stbd = 0
    
    wayList = list()
    
    wayList.append(Waypoint1)
    wayList.append(Waypoint2)
    wayList.append(Waypoint3)
    
    for waypoint in wayList:
        if(waypoint.wtype == "nav_first"):
            BuoyCoords = waypoint.coordinate
            num_nav_first = num_nav_first + 1
        elif(waypoint.wtype == "nav_start_port"):
            PortStartInnerPoint = waypoint.coordinate
            num_nav_start_port = num_nav_start_port + 1
        elif(waypoint.wtype == "nav_start_stbd"):
            StarboardStartInnerPoint = waypoint.coordinate
            num_nav_start_stbd = num_nav_start_stbd + 1
    
    if(num_nav_start_port > 1 or num_nav_start_stbd > 1 or num_nav_first > 1):
        gVars.logger.error("Repeating or too many arguments")
    
    interpolatedPoint = datatypes.GPSCoordinate((PortStartInnerPoint.latitude+StarboardStartInnerPoint.latitude)/2,(PortStartInnerPoint.longitude+StarboardStartInnerPoint.longitude)/2)
    angleOfCourse = standardcalc.angleBetweenTwoCoords(interpolatedPoint, BuoyCoords)
    boundAngle = math.atan(HORIZ_BOUNDARY_DISTANCE/30)*180/math.pi
    
    bound_dist = math.sqrt(HORIZ_BOUNDARY_DISTANCE^2+30^2)
    
    netAngleLeft = boundAngle - angleOfCourse
    netAngleRight = boundAngle + angleOfCourse
    
    leftBoundaryPoint = standardcalc.GPSDistAway(StarboardStartInnerPoint, bound_dist*math.sin(netAngleLeft), bound_dist*math.cos(netAngleLeft))
    
    rightBoundaryPoint = standardcalc.GPSDistAway(PortStartInnerPoint, bound_dist*math.sin(netAngleRight), bound_dist*math.cos(netAngleRight))
    
    
    
    buoySailPoint = setNavigationBuoyPoint(BuoyCoords, GPSCoord, 10)
    
    if(gVars.kill_flagNav == 0):
        coresailinglogic.pointToPoint(buoySailPoint)
    
    if(gVars.kill_flagNav == 0):
        coresailinglogic.roundBuoyPort(BuoyCoords,standardcalc.angleBetweenTwoCoords(BuoyCoords,GPSCoord))
    
    if(gVars.kill_flagNav == 0):
        thread.start_new_thread(coresailinglogic.pointToPoint, interpolatedPoint)
    
    while(standardcalc.distBetweenTwoCoords(GPSCoord, interpolatedPoint)>sVars.ACCEPTANCE_DISTANCE_DEFAULT and gVars.kill_flagNav == 0):
        GPSCoord = currentData[gps_index]
        appWindAng = currentData[awa_index]
        
        while(gVars.currentData[aut_index] == False):
            time.sleep(0.1)
        
        if(standardcalc.distBetweenTwoCoords(GPSCoord,leftBoundaryPoint) > bound_dist or standardcalc.distBetweenTwoCoords(GPSCoord,rightBoundaryPoint) > bound_dist):
            if(appWindAng > 0):
                tackDirection = 1
            else:
                tackDirection = 0
                
            gVars.arduino.tack(gVars.currentColumn,tackDirection)
            gVars.tacked_flag = 1
    
    return 0

def setNavigationBuoyPoint(buoyLocation, boatCoords, distFromBuoy):
    interpoAngle = 90 - standardcalc.angleBetweenTwoCoords(buoyLocation, boatCoords)
    xDelta = distFromBuoy*math.cos(interpoAngle)
    yDelta = distFromBuoy*math.sin(interpoAngle)
    
    return standardcalc.GPSDistAway(buoyLocation, xDelta, yDelta)