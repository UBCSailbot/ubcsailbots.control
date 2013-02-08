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
import random
import math

hog_index=0
cog_index=1
sog_index=2
awa_index=3
gps_index=4
rud_index=5
sht_index=6
EARTH_RADIUS = 6378140

# Parameters which may be changed to affect how the simulation runs
ALLOW_WIND_REVERSAL = False



class arduino:
    def __init__(self):
        
        # Sets initial vectors and magnitudes for wind and boat
        self.windStrength = round(random.uniform(1, 5), 0)
        self.actualWindAngle = round(random.uniform(-179, 180), 2)
        self.actualWindSpeed = round(random.uniform(3, 6), 2)*self.windStrength
        self.idealBoatSpd = round(random.uniform(.5, 1), 2)*self.windStrength
        
        # Instantiates an array of initial conditions which simulates putting a boat in the water.
        cog = round(random.uniform(-179, 180), 2)
        hog = cog - round(random.uniform(-2, 2), 2)
        self.ardArray = [hog, cog, 0,
                          round(random.uniform(-179, 180), 2), datatype.GPSCoordinate(49, -121), round(random.uniform(-89, 90), 2), 
                          round(random.uniform(0, 100), 2)]
        print(self.ardArray)
        
    def getFromArduino(self):
        self._update()
        return self.ardArray
    
    def adjust_sheets(self, sheet_percent):                                                
        self.ardArray[sht_index] = sheet_percent
        
    def steer(self, method, degree):
        return
    
    def _update(self):
        if (ALLOW_WIND_REVERSAL):
            self.actualWindAngle += round(random.uniform(-.2, .1))
        else:
            self.actualWindAngle += round(random.uniform(-.1, .1), 2)
            
        self.actualWindSpeed += round(random.uniform(-.1, .1), 2)
        self.ardArray[hog_index] += random.uniform(-.5, .5)
        self.ardArray[cog_index] += round(random.uniform(-.5, .5), 2)
        
        # Gets the boat up to speed and allows for a little variation
        if (math.fabs(self.ardArray[sog_index]-self.idealBoatSpd) < .2):
            self.ardArray[sog_index] += round(random.uniform(-.1, .1), 2)
        elif (self.ardArray[sog_index] < self.idealBoatSpd):
            self.ardArray[sog_index] += round(random.uniform(0, .1), 2)
        elif (self.ardArray[sog_index] >= self.idealBoatSpd):
            self.ardArray[sog_index] += round(random.uniform(-.1, 0), 2)
            
        self.ardArray[awa_index] += round(random.uniform(-.5, .5), 2)
        # Calculation for change in GPS Coordinate
        lon = self.ardArray[gps_index].long
        lat = self.ardArray[gps_index].lat
        vx = self.ardArray[sog_index] * math.cos(self.ardArray[hog_index])
        vy = self.ardArray[sog_index] * math.sin(self.ardArray[hog_index])
        vz = 0
        x = EARTH_RADIUS * math.cos(lat) * math.cos(lon)
        y = EARTH_RADIUS * math.cos(lat) * math.sin(lon)
        z = EARTH_RADIUS * math.sin(lat)
        vlon = (-1*vx* math.sin(lon) + vy* math.cos(lon))/50000
        vlat = (vx *math.cos(lon)* math.cos(lat) + vy* math.sin(lon) * math.cos(lat) - vz * math.sin(lat))/50000
        
        self.ardArray[gps_index].lat += vlat
        self.ardArray[gps_index].long += vlon