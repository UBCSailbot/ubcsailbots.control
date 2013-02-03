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
        self.ardArray = [None, None, None, None, None, None, None]
    def getFromArduino(self):
        return [self.calcRandHOG(self.ardArray)]
    def adjust_sheets(self, sheet_percent):                                                
        return
    def steer(self, method, degree):
        return
    def calcRandHOG(self, prev):
        if (prev == None):
            self.ardArray[0] = round(random.uniform(-179, 180), 2)
            return self.ardArray[0]
        else:
            self.ardArray[0] = self.ardArray[0] + random.uniform(0, .4)