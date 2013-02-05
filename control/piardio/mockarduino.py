'''
Created on Feb 2, 2013

@author: joshandrews
'''

import control.datatype.datatypes as datatype
import random

hog_index=0
cog_index=1
sog_index=2
awa_index=3
gps_index=4
rud_index=5
sht_index=6


class arduino:
    def __init__(self):
        self.ardArray = [round(random.uniform(-179, 180), 2), round(random.uniform(-179, 180), 2), round(random.uniform(0, 3.5), 2),
                          round(random.uniform(-179, 180), 2), datatype.GPSCoordinate(49, -121), round(random.uniform(-89, 90), 2), 
                          round(random.uniform(0, 100), 2)]
    def getFromArduino(self):
        return self.ardArray
    def adjust_sheets(self, sheet_percent):                                                
        return
    def steer(self, method, degree):
        return