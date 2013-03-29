'''
Created on Jan 19, 2013

@author: joshandrews
'''
import math
import thread
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
COMPASS_METHOD = 0
COG_METHOD = 1
AWA_METHOD = 2

HORIZ_BOUNDARY_DISTANCE = 60 

# ---    Navigation Challenge    ---
#Input: Buoy GPS Coordinates (Latitude and Longitude of the Buoy), Left Inner Point (The coordinates of the left innermost gate), Right Inner Point (The coordinates of the right innermost gate)
#Output: None
def navigationChallenge(BuoyCoords,LeftInnerPoint,RightInnerPoint):
    currentData = gVars.currentData
    GPSCoord = currentData[gps_index]
    interpolatedPoint = datatypes.GPSCoordinate((LeftInnerPoint.latitude+RightInnerPoint.latitude)/2,(LeftInnerPoint.longitude+RightInnerPoint.longitude)/2)
    angleOfCourse = standardcalc.angleBetweenTwoCoords(interpolatedPoint, BuoyCoords)
    boundAngle = math.atan(HORIZ_BOUNDARY_DISTANCE/30)*180/math.pi
    
    bound_dist = math.sqrt(HORIZ_BOUNDARY_DISTANCE^2+30^2)
    
    buoySailPoint = setNavigationBuoyPoint(BuoyCoords, GPSCoord, 10)
    
    coresailinglogic.pointToPoint(buoySailPoint)
    
    coresailinglogic.roundBuoyStbd(BuoyCoords,standardcalc.angleBetweenTwoCoords(BuoyCoords,GPSCoord))
    
    return 0

def setNavigationBuoyPoint(buoyLocation, boatCoords, distFromBuoy):
    interpoAngle = 90 - standardcalc.angleBetweenTwoCoords(buoyLocation, boatCoords)
    xDelta = distFromBuoy*math.cos(interpoAngle)
    yDelta = distFromBuoy*math.sin(interpoAngle)
    
    return standardcalc.GPSDistAway(buoyLocation, xDelta, yDelta)