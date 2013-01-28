'''
Created on Jan 20, 2013

@author: joshandrews
'''
import math
import sailbot.datatype.datatypes as datatype

#Returns the distance in metres
def distBetweenTwoCoords(coord1, coord2):
    dLongRad = math.radians(coord1.long - coord2.long)
    dLatRad = math.radians(coord1.lat - coord2.lat)
    latRad1 = math.radians(coord1.lat)
    latRad2 = math.radians(coord2.lat)
    
    a = math.pow(math.sin(dLatRad/2),2) + math.cos(latRad1)*math.cos(latRad2)*math.pow(math.sin(dLongRad/2),2)
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    return 6371.0*c*1000 #6371 is mean radius of earth in km

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
            
            