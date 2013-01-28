#Unit tests of standardcalc.py module

import unittest
from sailbot.logic import standardcalc
from sailbot.datatype import datatypes

class TestDistBetweenTwoCoords(unittest.TestCase):
    def setUp(self):
        self.point1 = datatypes.GPSCoordinate(0,0)
        self.point2 = datatypes.GPSCoordinate(1,1)
        
    def distTest1(self):
        distance = standardcalc.distBetweenTwoCoords(self.point1, self.point2)
        self.assertEqual(round(distance/1000,1), 157.2)
        
'''class TestAngleBetweenTwoCoords(unittest.TestCase):
    def setUp(self):
        self.source = datatypes.GPSCoordinate(100,100)
        self.dest = datatypes.GPSCoordinate(300,100)
        
    def angleTest1(self):
        angle1 = standardcalc.angleBetweenTwoCoords(self.source, self.dest)
        angle2 = standardcalc.angleBetweenTwoCoords(self.dest, self.source)
        
        angle1value = self.angle1.degrees()
        angle2value = self.angle2.degrees()
        
        self.assertEqual(angle1value, 0)
        self.assertEqual(angle2value, 180)'''