'''
Created on Feb 2, 2013

Mock Arduino which should simulate changing wind conditions and return simulated
boat data that can be used by the control logic and gui.
-   By creating a mock arduino object, you may call functions which will return mock
    data.  All of the data will be simulated to show relative wind conditions and
    will be reactive upon functions called to the Arduino
    
@author: joshandrews
'''

import control.datatype.datatypes as datatype
import control.StaticVars as sVars
import random
import math

EARTH_RADIUS = 6378140

# Parameters which may be changed to affect how the simulation runs
ALLOW_WIND_REVERSAL = True
STRONG_CURRENT = False


class arduino:
    def __init__(self):
        
        # Sets initial vectors and magnitudes for wind and boat
        self.windStrength = round(random.uniform(1, 5), 0)
        self.actualWindAngle = round(random.uniform(-179, 180), 2)
        self.actualWindSpeed = round(random.uniform(3, 6), 2)*self.windStrength
        self.idealBoatSpd = round(random.uniform(.5, 1), 2)*self.windStrength
        if (STRONG_CURRENT):
            self.currplusmin = round(random.uniform(-4, 4), 2)
        else:
            self.currplusmin = round(random.uniform(-1, 1), 2)
        
        print("Current Plus/Min: " + str(self.currplusmin))  
        # Instantiates an array of initial conditions which simulates putting a boat in the water.
        cog = round(random.uniform(-179, 180), 2)
        hog = cog - round(random.uniform(-2, 2), 2)
        self.ardArray = [hog, cog, 0,
                          round(random.uniform(-179, 180), 2), datatype.GPSCoordinate(49.27480, -123.18960), 0, 
                          round(random.uniform(0, 100), 2)]
        print(self.ardArray)
        
    def getFromArduino(self):
        self._update()
        return self.ardArray
    
    def adjust_rudder(self, rudder_angle):
        self.ardArray[sVars.RUD_INDEX] = rudder_angle
    
    def adjust_sheets(self, sheet_percent):                                                
        self.ardArray[sVars.SHT_INDEX] = sheet_percent
        
    def steer(self, method, degree):
        self.ardArray[sVars.HOG_INDEX] = degree
    
    def _update(self):
        if (ALLOW_WIND_REVERSAL):
            self.actualWindAngle += random.uniform(-.2, .1)
        else:
            self.actualWindAngle += random.uniform(-.1, .1)
        
        # Makes the rudder turn the boat
        rud = self.ardArray[sVars.RUD_INDEX]
        
        if (rud != 0):
            hog = self.ardArray[sVars.HOG_INDEX]
            hog -= rud/6
            if (hog > 180):
                hog -= 360
            elif (hog < -180):
                hog += 360
            self.ardArray[sVars.HOG_INDEX] = hog
            
                
        self.ardArray[sVars.HOG_INDEX] += round(random.uniform(-.1, .1), 2)

        if (math.fabs(self.ardArray[sVars.COG_INDEX]+self.currplusmin-self.ardArray[sVars.HOG_INDEX]) < .4):
            self.ardArray[sVars.COG_INDEX] += round(random.uniform(-.1, .1), 2)
        elif (self.ardArray[sVars.COG_INDEX]+self.currplusmin < self.ardArray[sVars.HOG_INDEX]):
            self.ardArray[sVars.COG_INDEX] += round(random.uniform(0, 5), 2)
        elif (self.ardArray[sVars.COG_INDEX]+self.currplusmin > self.ardArray[sVars.HOG_INDEX]):
            self.ardArray[sVars.COG_INDEX] += round(random.uniform(-5, 0), 2)
        
                
        # Gets the boat up to speed and allows for a little variation
        if (math.fabs(self.ardArray[sVars.SOG_INDEX]-self.idealBoatSpd) < .2):
            self.ardArray[sVars.SOG_INDEX] += round(random.uniform(-.1, .1), 2)
        elif (self.ardArray[sVars.SOG_INDEX] < self.idealBoatSpd):
            self.ardArray[sVars.SOG_INDEX] += round(random.uniform(0, .2), 2)
        elif (self.ardArray[sVars.SOG_INDEX] >= self.idealBoatSpd):
            self.ardArray[sVars.SOG_INDEX] += round(random.uniform(-.2, 0), 2)
        
        
        # Sets the apparent wind angle
        if (self.ardArray[sVars.HOG_INDEX] < -180):
            boat_bearing = 360 + self.ardArray[sVars.HOG_INDEX]
        else:
            boat_bearing = self.ardArray[sVars.HOG_INDEX]
        boat_speed = self.ardArray[sVars.SOG_INDEX]
        if (self.actualWindAngle < -180):
            wind_bearing = 360 + self.actualWindAngle
        else:
            wind_bearing = self.actualWindAngle
        
        boat_bearing = boat_bearing - 180
        if (boat_bearing < -180):
            boat_bearing = 360 + boat_bearing
             
        wind_speed = self.actualWindSpeed
        
        boat_x = boat_speed * math.cos(boat_bearing)
        boat_y = boat_speed * math.sin(boat_bearing)
        wind_x = wind_speed * math.cos(wind_bearing)
        wind_y = wind_speed * math.sin(wind_bearing)
        
        x = boat_x + wind_x
        y = boat_y + wind_y
        
        awa = math.atan(x/y)
        awa = awa * 180/math.pi
        self.ardArray[sVars.AWA_INDEX] = awa
        
        # Calculation for change in GPS Coordinate
        heading = self.ardArray[sVars.HOG_INDEX]
        
        if (heading < 0):
            heading = 360 + heading
        
        lon0 = self.ardArray[sVars.GPS_INDEX].long
        lat0 = self.ardArray[sVars.GPS_INDEX].lat
        heading = self.ardArray[sVars.HOG_INDEX]
        speed = self.ardArray[sVars.SOG_INDEX]
        
        x = speed * math.sin(heading*math.pi/180)
        y = speed * math.cos(heading*math.pi/180)
        
        lat = lat0 + 180 / math.pi * y / EARTH_RADIUS;
        lon = lon0 + 180 / math.pi / math.sin(lat0*math.pi/180) * x / EARTH_RADIUS;
        
        self.ardArray[sVars.GPS_INDEX].lat = lat
        self.ardArray[sVars.GPS_INDEX].long = lon