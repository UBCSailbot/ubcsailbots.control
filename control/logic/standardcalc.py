'''
Created on Jan 20, 2013

@author: joshandrews
'''
import math
import control.datatype.datatypes as datatype
from control.parser import parsing
from os import path
from control.logic import coresailinglogic

EARTH_RADIUS = 6378140

#returns gpscoordinate distance in meters away from starting point.
#positive yDist = North, positive xDist = East
def GPSDistAway(coord, yDist, xDist):
    result = datatype.GPSCoordinate()
    result.long = coord.long + (180.0/math.pi)*(float(xDist)/EARTH_RADIUS)/math.cos(math.radians(coord.lat))
    result.lat = coord.lat + (180.0/math.pi)*(float(yDist)/EARTH_RADIUS)
    return result


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
    GPSCoord = datatype.GPSCoordinate
    
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
            return datatype.Angle(angle)
        elif(sourceCoord.long > destCoord.long):
            angle = -angle
            return datatype.Angle(angle)
        else:
            return datatype.Angle(0)        
    else:
        if(sourceCoord.long < destCoord.long):
            angle = 90+angle
            return datatype.Angle(angle)
        elif(sourceCoord.long > destCoord.long):
            angle = -90-angle
            return datatype.Angle(angle)
        else:
            return datatype.Angle(180)

def isWPNoGo (AWA, hog, dest, sog, GPS):
    AWAList = parsing.parse(path.join(path.dirname(__file__), 'AWA'))
    if(sog<119):
        if(hog-AWA-45 < 90 - angleBetweenTwoCoords(GPS,dest).degrees() and 90 - angleBetweenTwoCoords(GPS,dest).degrees() < hog-AWA+45):
            return 1
        else:
            return 0
    else:
        AWAindex = searchIndex(AWA, AWAList)
        return 0
        
def searchIndex(number, list1):
    big_list = list1[0]+list1[1]+list1[2]+list1[3]
    indcol_list = list()
    
    for n in big_list:
        if( math.fabs(big_list[n]-number) <= coresailinglogic.AWA_THRESHOLD ):
            index = n%181
            column = n%4
            small_list = [index,column]
            indcol_list.append(small_list)
            
    return indcol_list
    
        
        
    
                    