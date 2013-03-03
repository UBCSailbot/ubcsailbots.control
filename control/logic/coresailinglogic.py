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
from control.piardio import arduino

hog_index=sVars.HOG_INDEX
cog_index=sVars.COG_INDEX
sog_index=sVars.SOG_INDEX
awa_index=sVars.AWA_INDEX
gps_index=sVars.GPS_INDEX
rud_index=sVars.RUD_INDEX
sht_index=sVars.SHT_INDEX
tac_index=sVars.TAC_INDEX

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
# Input: Destination GPS Coordinate, initialTack: 0 for port, 1 for starboard, nothing calculates on own.
# Output: Nothing
def pointToPoint(Dest, initialTack=None):
    sheetList = parsing.parse(path.join(path.dirname(__file__), 'sheetSettings'))
    end_flag = 0
    while(end_flag == 0):
        currentData = glob.currentData
        
        GPSCoord = currentData[gps_index]
        appWindAng = currentData[awa_index]
        cog = currentData[cog_index]
        hog = currentData[hog_index]
        sog = currentData[sog_index]
        
        aobject = arduino.arduino()
        
        if(standardcalc.distBetweenTwoCoords(GPSCoord, Dest) > sVars.ACCEPTANCE_DISTANCE):
            #This if statement determines the sailing method we are going to use based on apparent wind angle
            if(sog < sVars.SPEED_AFFECTION_THRESHOLD):
                    TWA = appWindAng
            else:
                    TWA = standardcalc.getTrueWindAngle(appWindAng,sog)
                    
            if(standardcalc.isWPNoGo(appWindAng,hog,Dest,sog,GPSCoord)):
                
                #Trying to determine whether 45 degrees clockwise or counter clockwise of TWA wrt North is closer to current heading
                #This means we are trying to determine whether hog-TWA-45 or hog-TWA+45 (both using TWA wrt North) is closer to our current heading.
                #Since those values give us TWA wrt to north, we need to subtract hog from them to get TWA wrt to our heading and figure out which one has a smaller value.
                #To get it wrt to current heading, we use hog-TWA-45-hog and hog-TWA+45-hog.  Both terms have hogs cancelling out.
                #We are left with -TWA-45 and -TWA+45, which makes sense since the original TWA was always with respect to the boat.
                #Since we are trying to figure out which one is closest to turn to, we use absolute values.
                if(abs(-TWA-45)<abs(-TWA+45) and initialTack is None):
                    while(abs(hog-standardcalc.angleBetweenTwoCoords(GPSCoord, Dest))<80):
                        GPSCoord = currentData[gps_index]
                        appWindAng = currentData[awa_index]
                        cog = currentData[cog_index]
                        hog = currentData[hog_index]
                        sog = currentData[sog_index]
                        aobject.adjust_sheets(sheetList[TWA][glob.currentColumn])
                        aobject.steer(aobject,'AWA',hog-TWA-45)
                        
                    aobject.tack()
                elif(abs(-TWA-45)>=abs(-TWA+45) and initialTack is None):
                    while(abs(hog-standardcalc.angleBetweenTwoCoords(GPSCoord, Dest))<80):
                        GPSCoord = currentData[gps_index]
                        appWindAng = currentData[awa_index]
                        cog = currentData[cog_index]
                        hog = currentData[hog_index]
                        sog = currentData[sog_index]
                        
                        #Just calling this to update currentColumn
                        TWA = standardcalc.getTrueWindAngle(appWindAng, sog)
                        
                        aobject.adjust_sheets(sheetList[TWA][glob.currentColumn])
                        aobject.steer(aobject,'AWA',hog-TWA+45)
                    
                    aobject.tack()
                    
            elif(abs(hog-TWA-standardcalc.angleBetweenTwoCoords(GPSCoord, Dest))>90):
                aobject.adjust_sheets(sheetList[TWA][glob.currentColumn])
                aobject.steer(aobject,'compass',standardcalc.angleBetweenTwoCoords(GPSCoord,Dest))
            
        else:
            end_flag = 1
    
    
    return 0