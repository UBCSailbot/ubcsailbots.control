'''
Created on Jan 26, 2013

@author: joshandrews
'''
from sailbot.datatype import *

    
# Array for all current data from arduino
#    Format: TODO
currentData = []
functionQueue = []
queueParameters = []
boundaries = []
run = True
auto = False
currentProcess = None
currentParams = None

# Constant names for challenges and logic
NAVIGATION_CHALLENGE = "challenge.navigation"
STATION_KEEPING_CHALLENGE = "challenge.stationkeeping"
LONG_DISTANCE_CHALLENGE = "challenge.longdistance"
POINT_TO_POINT = "logic.coresailinglogic.pointToPoint"
STATION_KEEP = "logic.coresailinglogic.stationKeep"
ROUND_BUOY = "logic.coresailinglogic.roundBuoy"