'''
Created on Jan 19, 2013

@author: joshandrews
'''
import time
import math
import sys
from os import path
from control.parser import parsing
from control.logic import standardcalc
from control import StaticVars as sVars
from control import GlobalVars as gVars
from control.datatype import datatypes
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

end_flag=0

# --- Round Buoy Port---
# Input: TODO
# Output: TODO
def roundBuoyPort(BuoyLoc, FinalBearing):
    currentData = gVars.currentData
    GPSCoord = currentData[gps_index]
    # appWindAng = currentData[awa_index]
    InitCog = currentData[cog_index] # Course  over ground    
    InitHog = currentData[hog_index] # Heading over ground
    
    X = 16.64 # Degrees, Calculated
    Dest = 23.41 # Meters, Distance from boat to buoy
    angleToNorth = standardcalc.angleBetweenTwoCoords(GPSCoord, BuoyLoc)
    reflectLong = GPSCoord.long * -1 # Used for calculation ONLY, when longitude decreases from left to right
    quadDir = None
    
    if reflectLong > BuoyLoc.long & GPSCoord.lat > BuoyLoc.lat:
        moveLong = abs(math.sin(180 - angleToNorth + X)) * -1 # - X movement 
        moveLat = abs(math.cos(180 - angleToNorth + X)) * - 1 # - Y movement
        quadDir = 3;
    elif reflectLong < BuoyLoc.long & GPSCoord.lat > BuoyLoc.lat:
        moveLong = abs(math.cos(angleToNorth -90 - X)) # + X Movement
        moveLat = abs(math.sin(angleToNorth - 90 - X)) * -1 # - Y Movement
        quadDir = 4;
    elif reflectLong < BuoyLoc.long & GPSCoord.lat < BuoyLoc.lat:
        moveLong = abs(math.sin(angleToNorth - X)) # + X Movement
        moveLat = abs(math.cos(angleToNorth - X)) # + Y Movement
        quadDir = 1;
    else:
        moveLong = abs(math.sin(angleToNorth + X)) * - 1 # - X Movement
        moveLat = abs(math.cos(angleToNorth + X)) # + Y Movement 
        quadDir = 2;
        
    moveLong *= Dest # Error!
    moveLat *= Dest # Error!
    
    moveLong *= -1 # Convert back actual coordinates
    
    destinationLong = moveLong + GPSCoord.long
    destinationLat = moveLat + GPSCoord.lat
    
    # 10 represents the degree of error around the destination point
    # Calls point to point function until it reaches location past buoy
    # Adding 10 does not increase the radius by 10 meters(ERROR!)
    while (GPSCoord.long >= standardcalc.GPSDistAway(destinationLong, 10, 0) or GPSCoord.long <= standardcalc.GPSDistAway(destinationLong, -10, 0)) and (GPSCoord.lat >= standardcalc.GPSDistAway(destinationLong, 0, 10) or GPSCoord.lat <= standardcalc.GPSDistAway(destinationLong, 0, -10)): 
        GPSCoord.long = gVars.currentData[gps_index].long
        GPSCoord.lat = gVars.currentData[gps_index].lat
        pointToPoint(datatypes.GPSCoordinate(destinationLat, destinationLong),1)
        
    # Checks if the boat needs to round the buoy or just pass it
    vect = None
    vect.lat = BuoyLoc.lat - currentData.lat
    vect.long = BuoyLoc.long - currentData.long
    
    # Checks if the boat as to round the buoy
    buoyAngle = None
    buoyAngle = standardcalc.vectorToDegrees(vect.lat, vect.long)
    buoyAngle -= 90 
    buoyAngle = standardcalc.boundTo180(buoyAngle) #git later
    
    if quadDir == 1 and FinalBearing < buoyAngle and FinalBearing > (buoyAngle - 90):
        pointToPoint(standardcalc.GPSDistAway(gVars.currentData[gps_index], -10, 0), 1)
    elif quadDir == 2 and FinalBearing < buoyAngle and FinalBearing > (buoyAngle - 90):
        pointToPoint(standardcalc.GPSDistAway(gVars.currentData[gps_index], 0, -10), 1)
    elif quadDir == 3 and FinalBearing < buoyAngle and FinalBearing > (buoyAngle - 90):
        pointToPoint(standardcalc.GPSDistAway(gVars.currentData[gps_index], 10, 0), 1)
    else: #quadDir == 4 and FinalBearing < buoyAngle and FinalBearing > (buoyAngle - 90):
        pointToPoint(standardcalc.GPSDistAway(gVars.currentData[gps_index], 0, 10), 1)
    
    return 0

# --- Round Buoy Stbd---
# Input: TODO
# Output: TODO
def roundBuoyStbd(BuoyLoc, FinalBearing):
    currentData = gVars.currentData
        
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
    
    pointToPoint(datatypes.GPSCoordinate(moveLat, moveLong),1)
    
    return 0

def killPointToPoint():
    gVars.kill_flagPTP = 1

# --- Point to Point ---
# Input: Destination GPS Coordinate, initialTack: 0 for port, 1 for starboard, nothing calculates on own, TWA = 0 for sailing using only AWA and 1 for attempting to find TWA.
# Output: Nothing
def pointToPoint(Dest, initialTack = None, ACCEPTANCE_DISTANCE = sVars.ACCEPTANCE_DISTANCE_DEFAULT, TWA = 0):
    if(TWA == 1):
        print("Running pointToPointTWA!")
        pointToPointTWA(Dest, initialTack, ACCEPTANCE_DISTANCE)
    else:
        print("Running pointToPointAWA!")
        pointToPointAWA(Dest, initialTack, ACCEPTANCE_DISTANCE)
        
    return 0

def pointToPointAWA(Dest, initialTack, ACCEPTANCE_DISTANCE):
    sheetList = parsing.parse(path.join(path.dirname(__file__), 'apparentSheetSetting'))
    gVars.kill_flagPTP = 0
    end_flag = 0
    arduino = gVars.arduino
    appWindAng = 0
    oldColumn = 0
    tackDirection = 0
    print "Started point to point"
    gVars.logger.info("Started point to point")
    
    while(end_flag == 0 and gVars.kill_flagPTP == 0):
        print('hello')
        
        while(gVars.currentData[aut_index] == True):
            time.sleep(0.1)
            
        currentData = gVars.currentData
        GPSCoord = currentData[gps_index]
        newappWindAng = currentData[awa_index]
        cog = currentData[cog_index]
        hog = currentData[hog_index]
        sog = currentData[sog_index] * 100        
        
        if(standardcalc.distBetweenTwoCoords(GPSCoord, Dest) > ACCEPTANCE_DISTANCE):
            #This if statement determines the sailing method we are going to use based on apparent wind angle
            arbitraryTWA = standardcalc.getTrueWindAngle(newappWindAng,sog)
                #print ("Hit else statement")
                #print ("TWA is: " + str(gVars.TrueWindAngle))
                                
            if(standardcalc.isWPNoGoAWA(newappWindAng,hog,Dest,sog,GPSCoord)):
                
                #Trying to determine whether 45 degrees clockwise or counter clockwise of TWA wrt North is closer to current heading
                #This means we are trying to determine whether hog-TWA-45 or hog-TWA+45 (both using TWA wrt North) is closer to our current heading.
                #Since those values give us TWA wrt to north, we need to subtract hog from them to get TWA wrt to our heading and figure out which one has a smaller value.
                #To get it wrt to current heading, we use hog-TWA-45-hog and hog-TWA+45-hog.  Both terms have hogs cancelling out.
                #We are left with -TWA-45 and -TWA+45, which makes sense since the original TWA was always with respect to the boat.
                #Since we are trying to figure out which one is closest to turn to, we use absolute values.
                if((abs(-newappWindAng-43)<abs(-newappWindAng+43) and initialTack is None) or initialTack == 1):
                    initialTack = None
                    while(abs(hog-standardcalc.angleBetweenTwoCoords(GPSCoord, Dest))<80 and gVars.kill_flagPTP ==0):
                        
                        while(gVars.currentData[aut_index] == True):
                            time.sleep(0.1)
                        
                        gVars.tacked_flag = 0
                        GPSCoord = currentData[gps_index]
                        newappWindAng = currentData[awa_index]
                        cog = currentData[cog_index]
                        hog = currentData[hog_index]
                        sog = currentData[sog_index] * 100
                                               
                        arbitraryTWA = standardcalc.getTrueWindAngle(newappWindAng, sog)                            
                        
                        if( appWindAng != newappWindAng or oldColumn != gVars.currentColumn):
                            arduino.adjust_sheets(sheetList[abs(int(arbitraryTWA))][gVars.currentColumn])
                            arduino.steer(AWA_METHOD,hog-newappWindAng-43)
                            appWindAng = newappWindAng
                            oldColumn = gVars.currentColumn
                            
                        if(newappWindAng > 0):
                            tackDirection = 1
                        else:
                            tackDirection = 0
                        
                        if( len(gVars.boundaries) > 0 ):
                            for boundary in gVars.boundaries:
                                if(standardcalc.distBetweenTwoCoords(boundary, GPSCoord) <= boundary.radius):
                                    arduino.tack(gVars.currentColumn,tackDirection)
                                    gVars.tacked_flag = 1
                                    break
                        if(gVars.tacked_flag):
                            break
                                                            
                    arduino.tack(gVars.currentColumn,tackDirection)
                    
                elif((abs(-newappWindAng-43)>=abs(-newappWindAng+43) and initialTack is None) or initialTack == 0):
                    initialTack = None
                    while(abs(hog-standardcalc.angleBetweenTwoCoords(GPSCoord, Dest))<80 and gVars.kill_flagPTP == 0):
                        while(gVars.currentData[aut_index] == True):
                            time.sleep(0.1)
                        gVars.tacked_flag = 0
                        GPSCoord = currentData[gps_index]
                        newappWindAng = currentData[awa_index]
                        cog = currentData[cog_index]
                        hog = currentData[hog_index]
                        sog = currentData[sog_index]*100
                        
                        arbitraryTWA = standardcalc.getTrueWindAngle(newappWindAng, sog)
                        #TWA = abs(int(TWA))
                        #print ("TWA is: " + str(newTWA))
                        
                        if(appWindAng != newappWindAng or oldColumn != gVars.currentColumn):
                            arduino.adjust_sheets(sheetList[abs(int(arbitraryTWA))][gVars.currentColumn])
                            arduino.steer(AWA_METHOD,hog-newappWindAng+43)
                            appWindAng = newappWindAng
                            oldColumn = gVars.currentColumn
                            
                        if(newappWindAng > 0):
                            tackDirection = 1
                        else:
                            tackDirection = 0
                            
                        if( len(gVars.boundaries) > 0 ):
                            for boundary in gVars.boundaries:
                                if(standardcalc.distBetweenTwoCoords(boundary, GPSCoord) <= boundary.radius):
                                    arduino.tack(gVars.currentColumn,tackDirection)
                                    gVars.tacked_flag = 1
                                    break
                        
                        if(gVars.tacked_flag):
                            break
                        
                    arduino.tack(gVars.currentColumn,tackDirection)
                    
            elif(abs(hog-arbitraryTWA-standardcalc.angleBetweenTwoCoords(GPSCoord, Dest))>90):
                if(appWindAng != newappWindAng or oldColumn != gVars.currentColumn):
                    arduino.adjust_sheets(sheetList[abs(int(arbitraryTWA))][gVars.currentColumn])
                    arduino.steer(COMPASS_METHOD,standardcalc.angleBetweenTwoCoords(GPSCoord,Dest))
                    appWindAng = newappWindAng
                    gVars.currentColumn
            
        else:
            end_flag = 1
            print ("Finished Point to Point")
            gVars.logger.info("Finished Point to Point")
    
    return 0
    
def pointToPointTWA(Dest, initialTack, ACCEPTANCE_DISTANCE):
    sheetList = parsing.parse(path.join(path.dirname(__file__), 'apparentSheetSetting'))
    gVars.kill_flagPTP = 0
    end_flag = 0
    arduino = gVars.arduino
    TWA = 0
    oldColumn = 0
    tackDirection = 0
    print "Started point to point"
    gVars.logger.info("Started point to point")
    
    while(end_flag == 0 and gVars.kill_flagPTP == 0):
        while(gVars.currentData[aut_index] == True):
            time.sleep(0.1)
        currentData = gVars.currentData
        GPSCoord = currentData[gps_index]
        appWindAng = currentData[awa_index]
        cog = currentData[cog_index]
        hog = currentData[hog_index]
        sog = currentData[sog_index] * 100        
        
        if(standardcalc.distBetweenTwoCoords(GPSCoord, Dest) > ACCEPTANCE_DISTANCE):
            #This if statement determines the sailing method we are going to use based on apparent wind angle
            if(sog < sVars.SPEED_AFFECTION_THRESHOLD):
                newTWA = appWindAng
                newTWA = abs(int(newTWA))
                if(appWindAng < 0):
                    gVars.TrueWindAngle = -newTWA
                else:
                    gVars.TrueWindAngle = newTWA
                gVars.currentColumn = 0
                #print ("TWA is: " + str(gVars.TrueWindAngle))
            else:
                newTWA = standardcalc.getTrueWindAngle(abs(int(appWindAng)),sog)
                newTWA = abs(int(newTWA))
                if(appWindAng < 0):
                    gVars.TrueWindAngle = -newTWA
                else:
                    gVars.TrueWindAngle = newTWA
                #print ("Hit else statement")
                #print ("TWA is: " + str(gVars.TrueWindAngle))
                                
            if(standardcalc.isWPNoGo(appWindAng,hog,Dest,sog,GPSCoord)):
                
                #Trying to determine whether 45 degrees clockwise or counter clockwise of TWA wrt North is closer to current heading
                #This means we are trying to determine whether hog-TWA-45 or hog-TWA+45 (both using TWA wrt North) is closer to our current heading.
                #Since those values give us TWA wrt to north, we need to subtract hog from them to get TWA wrt to our heading and figure out which one has a smaller value.
                #To get it wrt to current heading, we use hog-TWA-45-hog and hog-TWA+45-hog.  Both terms have hogs cancelling out.
                #We are left with -TWA-45 and -TWA+45, which makes sense since the original TWA was always with respect to the boat.
                #Since we are trying to figure out which one is closest to turn to, we use absolute values.
                if((abs(-newTWA-45)<abs(-newTWA+45) and initialTack is None) or initialTack == 1):
                    initialTack = None
                    while(abs(hog-standardcalc.angleBetweenTwoCoords(GPSCoord, Dest))<80 and gVars.kill_flagPTP ==0):
                        while(gVars.currentData[aut_index] == True):
                            time.sleep(0.1)
                        gVars.tacked_flag = 0
                        GPSCoord = currentData[gps_index]
                        appWindAng = currentData[awa_index]
                        cog = currentData[cog_index]
                        hog = currentData[hog_index]
                        sog = currentData[sog_index] * 100
                        
                        if(sog > sVars.SOG_THRESHOLD):
                            newTWA = standardcalc.getTrueWindAngle(appWindAng, sog)
                        else:
                            newTWA = appWindAng
                            newTWA = abs(int(newTWA))
                            
                        
                        if( TWA != newTWA or oldColumn != gVars.currentColumn):
                            arduino.adjust_sheets(sheetList[newTWA][gVars.currentColumn])
                            arduino.steer(AWA_METHOD,hog-newTWA-45)
                            TWA = newTWA
                            oldColumn = gVars.currentColumn
                            
                        if(appWindAng > 0):
                            tackDirection = 1
                        else:
                            tackDirection = 0
                            
                        if( len(gVars.boundaries) > 0 ):
                            for boundary in gVars.boundaries:
                                if(standardcalc.distBetweenTwoCoords(boundary, GPSCoord) <= boundary.radius):
                                    arduino.tack(gVars.currentColumn,tackDirection)
                                    gVars.tacked_flag = 1
                                    break
                                
                        if(gVars.tacked_flag):
                            break
                        
                    arduino.tack(gVars.currentColumn,tackDirection)
                    
                elif((abs(-newTWA-45)>=abs(-newTWA+45) and initialTack is None) or initialTack == 0):
                    initialTack = None
                    while(abs(hog-standardcalc.angleBetweenTwoCoords(GPSCoord, Dest))<80 and gVars.kill_flagPTP == 0):
                        while(gVars.currentData[aut_index] == True):
                            time.sleep(0.1)
                        gVars.tacked_flag = 0
                        GPSCoord = currentData[gps_index]
                        appWindAng = currentData[awa_index]
                        cog = currentData[cog_index]
                        hog = currentData[hog_index]
                        sog = currentData[sog_index]*100
                        
                        if(sog > sVars.SOG_THRESHOLD):
                            newTWA = standardcalc.getTrueWindAngle(appWindAng, sog)
                        else:
                            newTWA = appWindAng
                            newTWA = abs(int(newTWA))
                        #TWA = abs(int(TWA))
                        #print ("TWA is: " + str(newTWA))
                        
                        if(TWA != newTWA or oldColumn != gVars.currentColumn):
                            arduino.adjust_sheets(sheetList[int(newTWA)][gVars.currentColumn])
                            arduino.steer(AWA_METHOD,hog-newTWA+45)
                            TWA = newTWA
                            oldColumn = gVars.currentColumn
                            
                        if(appWindAng > 0):
                            tackDirection = 1
                        else:
                            tackDirection = 0
                            
                        if( len(gVars.boundaries) > 0 ):
                            for boundary in gVars.boundaries:
                                if(standardcalc.distBetweenTwoCoords(boundary, GPSCoord) <= boundary.radius):
                                    arduino.tack(gVars.currentColumn,tackDirection)
                                    gVars.tacked_flag = 1
                                    break
                        
                        if(gVars.tacked_flag):
                            break
                        
                    arduino.tack(gVars.currentColumn,tackDirection)
                    
            elif(abs(hog-newTWA-standardcalc.angleBetweenTwoCoords(GPSCoord, Dest))>90):
                if(TWA != newTWA or oldColumn != gVars.currentColumn):
                    arduino.adjust_sheets(sheetList[newTWA][gVars.currentColumn])
                    arduino.steer(COMPASS_METHOD,standardcalc.angleBetweenTwoCoords(GPSCoord,Dest))
                    TWA = newTWA
                    gVars.currentColumn
            
        else:
            end_flag = 1
            print ("Finished Point to Point")
            gVars.logger.info("Finished Point to Point")
    
    return 0