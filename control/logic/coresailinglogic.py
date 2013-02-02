'''
Created on Jan 19, 2013

@author: joshandrews
'''

import control.GlobalVars as glob
from control.parser import parsing
from os import path

hog_index=0
cog_index=1
sog_index=2
awa_index=3
gps_index=4
rud_index=5
sht_index=6

end_flag=0

# --- Round Buoy Port---
# Input: TODO
# Output: TODO
def roundBuoyPort():
    return 0

# --- Round Buoy Stbd---
# Input: TODO
# Output: TODO
def roundBuoyStbd():
    return 0

# --- Point to Point ---
# Input: Destination GPS Coordinate
# Output: Nothing
def pointToPoint(Dest):
    list = parsing.parse(path.join(path.dirname(__file__), 'sheetSettings'))
    while(end_flag == 0):
        currentData = glob.currentData
        
        GPSCoord = currentData[gps_index]
        appWindAng = currentData[awa_index]
        cog = currentData[cog_index]
        
        hog = currentData[hog_index]
        sog = currentData[sog_index]
        
        if(GPSCoord.lat != Dest.lat or GPSCoord.long != Dest.long):
            #This if statement determines the sailing method we are going to use based on apparent wind angle
            if( -34 < appWindAng and appWindAng < 34):
                x = 1
            else:
                x = 1
            
        else:
            end_flag = 1
    
    
    return 0

# --- Station Keeping ---
# Input: TODO
# Output: TODO
def stationKeep():
    return 0