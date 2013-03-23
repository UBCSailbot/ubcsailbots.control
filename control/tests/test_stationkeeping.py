import unittest
import sys
sys.path.append("..")
from control.challenge import stationkeeping
from control.datatype import datatypes

class TestSetBoxCoords(unittest.TestCase):
    def setUp(self):
        self.coord1 = datatypes.GPSCoordinate(2,2) #square
        self.coord2 = datatypes.GPSCoordinate(2,3)
        self.coord3 = datatypes.GPSCoordinate(1,3)
        self.coord4 = datatypes.GPSCoordinate(1,2)
        
        self.coord1 = datatypes.GPSCoordinate(1,1) #diamond
        self.coord2 = datatypes.GPSCoordinate(2,2)
        self.coord3 = datatypes.GPSCoordinate(1,3)
        self.coord4 = datatypes.GPSCoordinate(1,2)
        
        self.coord1 = datatypes.GPSCoordinate(2,2) #left tilted square (notdone)
        self.coord2 = datatypes.GPSCoordinate(2,3)
        self.coord3 = datatypes.GPSCoordinate(1,3)
        self.coord4 = datatypes.GPSCoordinate(1,2)
        
        self.coord1 = datatypes.GPSCoordinate(2,2) #right tilted square (notdone)
        self.coord2 = datatypes.GPSCoordinate(2,3)
        self.coord3 = datatypes.GPSCoordinate(1,3)
        self.coord4 = datatypes.GPSCoordinate(1,2)