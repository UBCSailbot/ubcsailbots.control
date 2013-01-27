'''
Created on Jan 20, 2013

@author: joshandrews
'''
import math
from sailbot.datatype import datatypes

def distBetweenTwoCoords(coord1, coord2):
    dLongRad = math.radians(coord1.long - coord2.long)
    dLatRad = math.radians(coord1.lat - coord2.lat)
    latRad1 = math.radians(coord1.lat)
    latRad2 = math.radians(coord2.lat)
    
    a = math.pow(math.sin(dLatRad/2),2) + math.cos(latRad1)*math.cos(latRad2)*math.pow(math.sin(dLongRad/2),2)
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    return 6371.0*c #6371 is mean radius of earth in km

def angleBetweenTwoCoords(sourceCoord, destCoord):
    GPSCoord = datatypes.GPSCoordinate
    
    if(sourceCoord.lat > destCoord.lat):
        GPSCoord.lat = sourceCoord.lat
        GPSCoord.long = destCoord.long
    
    elif(sourceCoord.lat < destCoord.lat):
        GPSCoord.lat = destCoord.lat
        GPSCoord.long = sourceCoord.long
    
    elif(sourceCoord.long < destCoord.long):
        return -90
    
    elif(sourceCoord.long > destCoord.long):
        return 90
    
    else:
        return None
    
    
    distBtwnCoords = distBetweenTwoCoords(sourceCoord, destCoord)
    distSin = distBetweenTwoCoords(destCoord, GPSCoord)
    
    angle = math.asin(distSin/distBtwnCoords)
    
    if(sourceCoord.lat < destCoord.lat):
        if(sourceCoord.long < destCoord.long):
            angle = -angle
            return datatypes.Angle(angle)
        elif(sourceCoord.long > destCoord.long):
            return datatypes.Angle(angle)
        else:
            return datatypes.Angle(0)        
    else:
        if(sourceCoord.long < destCoord.long):
            angle = -90-angle
            return datatypes.Angle(angle)
        elif(sourceCoord.long > destCoord.long):
            angle = 90+angle
            return datatypes.Angle(angle)
        else:
            return datatypes.Angle(180)
            
            