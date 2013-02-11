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
        
        print(self.currplusmin)  
        # Instantiates an array of initial conditions which simulates putting a boat in the water.
        cog = round(random.uniform(-179, 180), 2)
        hog = cog - round(random.uniform(-2, 2), 2)
        self.ardArray = [hog, cog, 0,
                          round(random.uniform(-179, 180), 2), datatype.GPSCoordinate(49, -121), 0, 
                          round(random.uniform(0, 100), 2)]
        print(self.ardArray)
        
    def getFromArduino(self):
        self._update()
        return self.ardArray
    
    def adjust_rudder(self, rudder_angle):
        self.ardArray[rud_index] = rudder_angle
    
    def adjust_sheets(self, sheet_percent):                                                
        self.ardArray[sht_index] = sheet_percent
        
    def steer(self, method, degree):
        self.ardArray[hog_index] = degree
    
    def _update(self):
        if (ALLOW_WIND_REVERSAL):
            self.actualWindAngle += random.uniform(-.2, .1)
        else:
            self.actualWindAngle += random.uniform(-.1, .1)
        
        # Makes the rudder turn the boat
        rud = self.ardArray[rud_index]
        
        if (rud != 0):
            hog = self.ardArray[hog_index]
            hog -= rud/3
            if (hog > 180):
                hog -= 360
            elif (hog < -180):
                hog += 360
            self.ardArray[hog_index] = hog
            
                
        self.ardArray[hog_index] += round(random.uniform(-.1, .1), 2)

        if (math.fabs(self.ardArray[cog_index]+self.currplusmin-self.ardArray[hog_index]) < .4):
            self.ardArray[cog_index] += round(random.uniform(-.1, .1), 2)
        elif (self.ardArray[cog_index]+self.currplusmin < self.ardArray[hog_index]):
            self.ardArray[cog_index] += round(random.uniform(0, .2), 2)
        elif (self.ardArray[cog_index]+self.currplusmin > self.ardArray[hog_index]):
            self.ardArray[cog_index] += round(random.uniform(-.2, 0), 2)
        
                
        # Gets the boat up to speed and allows for a little variation
        if (math.fabs(self.ardArray[sog_index]-self.idealBoatSpd) < .2):
            self.ardArray[sog_index] += round(random.uniform(-.1, .1), 2)
        elif (self.ardArray[sog_index] < self.idealBoatSpd):
            self.ardArray[sog_index] += round(random.uniform(0, .1), 2)
        elif (self.ardArray[sog_index] >= self.idealBoatSpd):
            self.ardArray[sog_index] += round(random.uniform(-.1, 0), 2)
        
        
        # Sets the apparent wind angle using vectors/magnitudes
        if (self.ardArray[hog_index] < 0):
            boat_bearing = 360 + self.ardArray[hog_index]
        else:
            boat_bearing = self.ardArray[hog_index]
        boat_speed = self.ardArray[sog_index]
        if (self.actualWindAngle < 0):
            wind_bearing = 360 + self.actualWindAngle
        else:
            wind_bearing = self.actualWindAngle
        
        boat_bearing = boat_bearing - 180
        if (boat_bearing < 0):
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
        if (awa > 180):
            awa = awa - 360
        self.ardArray[awa_index] = awa
        
        # Calculation for change in GPS Coordinate
        heading = self.ardArray[hog_index]
        
        if (heading < 0):
            heading = 360 + heading
        
        lon0 = self.ardArray[gps_index].long
        lat0 = self.ardArray[gps_index].lat
        heading = self.ardArray[hog_index]
        speed = self.ardArray[sog_index]
        
        x = speed * math.sin(heading*math.pi/180) * 1.5
        y = speed * math.cos(heading*math.pi/180) * 1.5
        
        lat = lat0 + 180 / math.pi * y / EARTH_RADIUS;
        lon = lon0 + 180 / math.pi / math.sin(lat0*math.pi/180) * x / EARTH_RADIUS;
        
        self.ardArray[gps_index].lat = lat
        self.ardArray[gps_index].long = lon