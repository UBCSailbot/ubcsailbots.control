'''
Created on Jan 20, 2013

@author: joshandrews
'''
import math
from os import path
from control.datatype import datatypes
from control.parser import parsing
from control import StaticVars as sVars
from control import GlobalVars as gVars

EARTH_RADIUS = 6378140.0

#returns gpscoordinate distance in meters away from starting point.
#positive yDist = North, positive xDist = East
def GPSDistAway(coord, xDist, yDist):
    result = datatypes.GPSCoordinate()
    result.long = coord.long + (180.0/math.pi)*(float(xDist)/EARTH_RADIUS)/math.cos(math.radians(coord.lat))
    result.lat = coord.lat + (180.0/math.pi)*(float(yDist)/EARTH_RADIUS)
    return result

def setBoxCoords(tL, tR, bL, bR): #sets coords of box so that topleft is most west point of the two most northern points
    coordHalf1 = [tL, tR]
    coordHalf2 = [bL, bR]
    firstCoordHalf = []
    secondCoordHalf = []
    coordList = []
    finalCoordList = []
    if (coordHalf1[1].lat > coordHalf1[0].lat):
        firstCoordHalf = [coordHalf1[1], coordHalf1[0]]
    else:
        firstCoordHalf = [coordHalf1[0], coordHalf1[1]]
    if (coordHalf2[1].lat > coordHalf2[0].lat):
        secondCoordHalf = [coordHalf2[1], coordHalf2[0]]
    else:
        secondCoordHalf = [coordHalf2[0], coordHalf2[1]]
        
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


#Returns the distance in metres
def distBetweenTwoCoords(coord1, coord2):
    dLongRad = math.radians(coord1.long - coord2.long)
    dLatRad = math.radians(coord1.lat - coord2.lat)
    latRad1 = math.radians(coord1.lat)
    latRad2 = math.radians(coord2.lat)
    
    a = math.pow(math.sin(dLatRad/2),2) + math.cos(latRad1)*math.cos(latRad2)*math.pow(math.sin(dLongRad/2),2)
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    return EARTH_RADIUS*c

#Returns the angle in degrees
def angleBetweenTwoCoords(sourceCoord, destCoord):
    GPSCoord = datatypes.GPSCoordinate
    
    if(sourceCoord.lat > destCoord.lat):
        GPSCoord.lat = sourceCoord.lat
        GPSCoord.long = destCoord.long
    
    elif(sourceCoord.lat < destCoord.lat):
        GPSCoord.lat = destCoord.lat
        GPSCoord.long = sourceCoord.long
    
    elif(sourceCoord.long < destCoord.long):
        return 90
    
    elif(sourceCoord.long > destCoord.long):
        return -90
    
    else:
        return None
    
    
    distBtwnCoords = distBetweenTwoCoords(sourceCoord, destCoord)
    distSin = distBetweenTwoCoords(destCoord, GPSCoord)
    
    angle = math.asin(distSin/distBtwnCoords)*180/math.pi
    
    if(sourceCoord.lat < destCoord.lat):
        if(sourceCoord.long < destCoord.long):
            return angle
        elif(sourceCoord.long > destCoord.long):
            angle = -angle
            return angle
        else:
            return 0        
    else:
        if(sourceCoord.long < destCoord.long):
            angle = 90+angle
            return angle
        elif(sourceCoord.long > destCoord.long):
            angle = -90-angle
            return angle
        else:
            return 180

#Determines whether the waypoint can be reached with our current coordinates
#Returns 1 if waypoint can't be reached
#Returns 0 if waypoint can be reached
def isWPNoGo (AWA, hog, dest, sog, GPS):
    if(sog < sVars.SPEED_AFFECTION_THRESHOLD):
        if(hog-AWA-45 < angleBetweenTwoCoords(GPS,dest) and angleBetweenTwoCoords(GPS,dest) < hog-AWA+45):
            return 1
        else:
            return 0
    else:
        TWA = getTrueWindAngle(AWA, sog)
        if(hog-TWA-45 < angleBetweenTwoCoords(GPS,dest) and angleBetweenTwoCoords(GPS,dest) < hog-TWA+45):
            return 1
        else:
            return 0

#Determines whether the waypoint can be reached with our current coordinates using AWA
#Returns 1 if waypoint can't be reached
#Returns 0 if waypoint can be reached
def isWPNoGoAWA (AWA, hog, dest, sog, GPS):
    if(sog < sVars.SPEED_AFFECTION_THRESHOLD):
        if(hog-AWA-45 < angleBetweenTwoCoords(GPS,dest) and angleBetweenTwoCoords(GPS,dest) < hog-AWA+45):
            return 1
        else:
            return 0
    else:
        if(hog-AWA-34 < angleBetweenTwoCoords(GPS,dest) and angleBetweenTwoCoords(GPS,dest) < hog-AWA+34):
            return 1
        else:
            return 0

def getTrueWindAngle(awa, sog):
    sVars.AWA_THRESHOLD = 0.9
    while(1):
        sVars.SOG_THRESHOLD = 0.9
        while(1):
            AWAList = parsing.parse(path.join(path.dirname(__file__), 'AWA.txt'))
            SOGList = parsing.parse(path.join(path.dirname(__file__), 'SOGarray'))
            AWAentries = searchAWAIndex(awa, AWAList)
            SOGentries = searchSOGIndex(sog, SOGList)
        
            for i in range(len(AWAentries)):
                index = AWAentries[i][0]
                column = AWAentries[i][1]
                    
                for x in range(len(SOGentries)):
                    if (SOGentries[x][0] == index) and (SOGentries[x][1] == column):
                        gVars.currentColumn = column
                        if(awa < 0):
                            gVars.trueWindAngle = -index
                        else:
                            gVars.trueWindAngle = index       
                        sVars.SOG_THRESHOLD = 0.9                 
                        return index
            
            sVars.SOG_THRESHOLD += 10
            
            if(sVars.SOG_THRESHOLD >= 500):
                print ("Hit Threshold")
                break
            
        sVars.AWA_THRESHOLD += 1
        
        if(sVars.AWA_THRESHOLD >= 100):
            return None    

# takes in a list of speeds. Deletes first element and appends the current speed to the end
def changeSpdList(spdList):
    if (len(spdList) == 0):
        return -1
    del spdList[0]
    spdList.append(gVars.currentData[sVars.SOG_INDEX])
    return spdList

def meanOfList(numberList):
    if len(numberList) == 0:
        return -1
 
    floatNums = [float(x) for x in numberList]
    return sum(floatNums) / len(numberList)

#Only works with tables with 4 columns!!!!!        
def searchAWAIndex(number, list1):
    number = abs(number)
    big_list = list()
    indcol_list = list()
    
    for i in range(len(list1)):
        for j in range(len(list1[i])):
            big_list.append(list1[i][j])    
    
    for n in range(len(big_list)):
        if( math.fabs(big_list[n]-number) <= sVars.AWA_THRESHOLD ):
            index = math.floor(n/4)
            column = n%4
            small_list = [index,column]
            indcol_list.append(small_list)
            
    return indcol_list

def searchSOGIndex(numberSOG, list1SOG):
    numberSOG = abs(numberSOG)
    big_listSOG = list()
    indcol_listSOG = list()
    
    for i in range(len(list1SOG)):
        for j in range(len(list1SOG[i])):
            big_listSOG.append(list1SOG[i][j])    
    
    for n in range(len(big_listSOG)):
        if( math.fabs(big_listSOG[n]-numberSOG) <= sVars.SOG_THRESHOLD ):
            indexSOG = math.floor(n/4)
            columnSOG = n%4
            small_listSOG = [indexSOG,columnSOG]
            indcol_listSOG.append(small_listSOG)
            
    return indcol_listSOG

#Convert a vector to degrees with respect to North
def vectorToDegrees(x, y):
    if(x >= 0 and y >= 0):
        return math.tan(x/y)*180/3.14159
    elif(x < 0 and y > 0):
        return 90 - math.tan(x/y)*180/3.14159
    elif(x < 0 and y < 0):
        return 180 - math.tan(x/y)*180/3.14159
    else:
        return 90 + math.tan(x/y)*180/3.14159
    
def findCosLawAngle(a, b, c):  #cos law: c^2 = a^2 + b^2 - 2*a*b*cos(theta):
    if ((a < 1) or (b < 1) or (c < 1)):
        return 0
    return math.acos((math.pow(a, 2) + math.pow(b, 2) - math.pow(c, 2)) / (2*a*b))

# Bounds angle to -180 to 180
def boundTo180(angle):
    if (angle < -180):
        return angle+360
    elif (angle > 180):
        return angle-360
    else:
        return angle
