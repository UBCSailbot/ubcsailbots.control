'''
Created on Jan 19, 2013

@author: joshandrews
'''

import sailbot.GlobalVar as glob
from sailbot import parser
import sailbot.GlobalVar

hog_index=0
cog_index=1
awa_index=2
gps_index=3
rud_index=4
sht_index=5

end_flag=0

# --- Round Buoy ---
# Input: TODO
# Output: TODO
def roundBuoy():
    return 0

# --- Point to Point ---
# Input: Destination GPS Coordinate
# Output: Nothing
def pointToPoint(Dest):
    while(end_flag == 0):
        currentData = glob.currentData
        GPSCoord = currentData[gps_index]
        appWindAng = currentData[awa_index]
        cog = currentData[cog_index]
        hog = currentData[hog_index]
        
        while(GPSCoord != Dest):
            
        if(GPSCoord == Dest):
            end_flag = 1
        
    
    
    return 0

# --- Station Keeping ---
# Input: TODO
# Output: TODO
def stationKeep():
    return 0