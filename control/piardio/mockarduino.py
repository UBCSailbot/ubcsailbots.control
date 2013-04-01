'''
Created on Feb 2, 2013

Mock Arduino which should simulate changing wind conditions and return simulated
boat data that can be used by the control logic and gui.
-   By creating a mock arduino object, you may call functions which will return mock
    data.  All of the data will be simulated to show relative wind conditions and
    will be reactive upon functions called to the Arduino
    
@author: joshandrews
'''

from control.datatype import datatypes
import control.StaticVars as sVars
import random
import math
import thread

EARTH_RADIUS = 6378140

# Parameters which may be changed to affect how the simulation runs
ALLOW_WIND_REVERSAL = False
STRONG_CURRENT = False


class arduino:
    def __init__(self):
        
        # Sets initial vectors and magnitudes for wind and boat
        self.flipflag = False
        self.windStrength = round(random.uniform(1, 5), 0)
        self.actualWindAngle = round(random.uniform(-179, 180), 2)
        self.actualWindSpeed = round(random.uniform(3, 6), 2)*self.windStrength
        self.idealBoatSpd = round(random.uniform(.5, 1), 2)*self.windStrength
        self.previousx = None
        if (STRONG_CURRENT):
            self.currplusmin = round(random.uniform(-4, 4), 2)
        else:
            self.currplusmin = round(random.uniform(-1, 1), 2)
        
        print("Current Plus/Min: " + str(self.currplusmin))  
        # Instantiates an array of initial conditions which simulates putting a boat in the water.
        cog = round(random.uniform(-179, 180), 2)
        hog = cog - round(random.uniform(-2, 2), 2)
        self.ardArray = [hog, cog, 0,
                          round(random.uniform(-179, 180), 2), datatypes.GPSCoordinate(49.27480, -123.18960), 0, 
                          15, 80, 1, 20]
        print(self.ardArray)
        
    def getFromArduino(self):
        self._update()
        return self.ardArray
    
    def tack(self, x, y):
        hog = self.ardArray[sVars.HOG_INDEX]
        if (self.actualWindAngle < hog):
            hog = self.actualWindAngle - 45
        else:
            hog = self.actualWindAngle + 45
        
        if (hog > 180):
            hog -= 360
        elif (hog < -180):
            hog += 360
        
        self.ardArray[sVars.HOG_INDEX] = hog
    
    def gybe(self, x):
        pass
    def adjust_sheets(self, sheet_percent):                                                
        self.ardArray[sVars.SHT_INDEX] = sheet_percent
        
    def steer(self, method, degree):
        self.ardArray[sVars.HOG_INDEX] = degree
    
    def _update(self):
        if (ALLOW_WIND_REVERSAL):
            self.actualWindAngle += random.uniform(-.2, 0)
        else:
            self.actualWindAngle += random.uniform(-.1, .1)
        
        if (self.actualWindAngle < -180):
            self.actualWindAngle += 360
        if (self.actualWindAngle > 180):
            self.actualWindAngle -= 360            
                
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
        boat_bearing = self.ardArray[sVars.HOG_INDEX]
        if (boat_bearing >= 0):
            boat_bearing -= 180
        else:
            boat_bearing += 180
        boat_speed = self.ardArray[sVars.SOG_INDEX]
        
        wind_bearing = self.actualWindAngle
        if (wind_bearing >= 0):
            wind_bearing -= 180
        else:
            wind_bearing += 180
            
        wind_speed = self.actualWindSpeed
        
        boat_x = boat_speed * math.cos(boat_bearing)
        boat_y = boat_speed * math.sin(boat_bearing)
        wind_x = wind_speed * math.cos(wind_bearing)
        wind_y = wind_speed * math.sin(wind_bearing)
        
        x = boat_x + wind_x
        y = boat_y + wind_y
        
        if self.previousx is None:
            self.previousx = x
        
        awa = math.atan(y/x)

        if(math.copysign(self.previousx, x) != self.previousx or self.flipflag): 
            if (not self.flipflag):
                self.flipflag = True
            elif (math.copysign(self.previousx, x) != self.previousx):
                self.flipflag = False
                
            print(str(self.previousx) + ", " + str(x))  
            if(awa > 0):
                awa -= math.pi
            else:
                awa += math.pi
         
        awa = awa * 180/math.pi
            
        awa -= self.ardArray[sVars.HOG_INDEX]
        
        if (awa > 180):
            awa -= 360
        elif (awa < -180):
            awa += 360
        
        self.ardArray[sVars.AWA_INDEX] = awa
        self.previousx = x
        
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