'''
Created on Jan 19, 2013

@author: joshandrews
'''

import control.GlobalVars as glob
import math
from control.parser import parsing
from os import path
from control.logic import standardcalc
from control import StaticVars as sVars

hog_index=0
cog_index=1
sog_index=2
awa_index=3
gps_index=4
rud_index=5
sht_index=6

end_flag=0

# --- Round Buoy Port---
# Input: TODO
# Output: TODO
def roundBuoyPort(BuoyLoc, FinalBearing):
    currentData = glob.currentData
        
    GPSCoord = currentData[gps_index]
    appWindAng = currentData[awa_index]
    cog = currentData[cog_index] # Course  over ground    
    hog = currentData[hog_index] # Height over ground
    
    X = 16.64 # Degrees, Calculated
    Dest = 23.41 # Meters, Distance from boat to buoy
    angleToNorth = standardcalc.angleBetweenTwoCoords(GPSCoord, BuoyLoc)
    reflectLong = GPSCoord.long * -1 # Used for calculation ONLY, when longitude decreases from left to right
    
    if reflectLong > BuoyLoc.long & GPSCoord.lat > BuoyLoc.lat:
        moveLong = abs(math.sin(180 - angleToNorth + X)) * -1 # - X movement 
        moveLat = abs(math.cos(180 - angleToNorth + X)) * - 1 # - Y movement
    elif reflectLong < BuoyLoc.long & GPSCoord.lat > BuoyLoc.lat:
        moveLong = abs(math.cos(angleToNorth -90 - X)) # + X Movement
        moveLat = abs(math.sin(angleToNorth - 90 - X)) * -1 # - Y Movement
    elif reflectLong < BuoyLoc.long & GPSCoord.lat < BuoyLoc.lat:
        moveLong = abs(math.sin(angleToNorth - X)) # + X Movement
        moveLat = abs(math.cos(angleToNorth - X)) # + Y Movement
    else:
        moveLong = abs(math.sin(angleToNorth + X)) * - 1 # - X Movement
        moveLat = abs(math.cos(angleToNorth + X)) # + Y Movement 
        
    moveLong *= Dest
    moveLat *= Dest
    
    moveLong *= -1 # Convert back actual coordinates 
    return 0

# --- Round Buoy Stbd---
# Input: TODO
# Output: TODO
def roundBuoyStbd(BuoyLoc, FinalBearing):
    currentData = glob.currentData
        
    GPSCoord = currentData[gps_index]
    appWindAng = currentData[awa_index]
    cog = currentData[cog_index] # Course  over ground    
    hog = currentData[hog_index] # Height over ground
    
    X = 16.64 # Degrees, Calculated
    Dest = 23.41 # Meters, Distance from boat to buoy
    angleToNorth = standardcalc.angleBetweenTwoCoords(GPSCoord, BuoyLoc)
    reflectLong = GPSCoord.long * -1 # Used for calculation ONLY, when longitude decreases from left to right
    
    if reflectLong > BuoyLoc.long & GPSCoord.lat > BuoyLoc.lat:
        moveLong = abs(math.cos(180 - angleToNorth + X)) * -1 # - X movement 
        moveLat = abs(math.sin(180 - angleToNorth + X)) * - 1 # - Y movement
    elif reflectLong < BuoyLoc.long & GPSCoord.lat > BuoyLoc.lat:
        moveLong = abs(math.sin(angleToNorth -90 - X)) # + X Movement
        moveLat = abs(math.cos(angleToNorth - 90 - X)) * -1 # - Y Movement
    elif reflectLong < BuoyLoc.long & GPSCoord.lat < BuoyLoc.lat:
        moveLong = abs(math.cos(angleToNorth - X)) # + X Movement
        moveLat = abs(math.sin(angleToNorth - X)) # + Y Movement
    else:
        moveLong = abs(math.sin(angleToNorth - X)) * - 1 # - X Movement
        moveLat = abs(math.cos(angleToNorth - X)) # + Y Movement 
    
    moveLong *= Dest
    moveLat *= Dest
    
    moveLong *= -1 # Convert back to actual coordinates
    return 0

# --- Point to Point ---
# Input: Destination GPS Coordinate
# Output: Nothing
def pointToPoint(Dest):
    list = parsing.parse(path.join(path.dirname(__file__), 'sheetSettings'))
    while(end_flag == 0):
        currentData = glob.currentData
        
        GPSCoord = currentData[gps_index]
        appWindAng = currentData[awa_index]
        cog = currentData[cog_index]
        hog = currentData[hog_index]
        sog = currentData[sog_index]
        
        if(standardcalc.distBetweenTwoCoords(GPSCoord, Dest) > sVars.ACCEPTANCE_DISTANCE):
            #This if statement determines the sailing method we are going to use based on apparent wind angle
            if( -34 < appWindAng and appWindAng < 34):
                x = 1
            else:
                x = 1
            
        else:
            end_flag = 1
    
    
    return 0