#Unit tests of standardcalc.py module

import unittest
from sailbot.logic import standardcalc
from sailbot.datatype import datatypes

class TestDistBetweenTwoCoords(unittest.TestCase):
    def setUp(self):
        self.point1 = datatypes.GPSCoordinate(0,0)
        self.point2 = datatypes.GPSCoordinate(1,1)
        
    def testDist1(self):
        distance = standardcalc.distBetweenTwoCoords(self.point1, self.point2)
        self.assertEqual(round(distance/1000,1), 157.2)
        
class TestAngleBetweenTwoCoords(unittest.TestCase):
    def setUp(self):
        self.source1 = datatypes.GPSCoordinate(100,100)
        self.dest1 = datatypes.GPSCoordinate(300,100)
        
        self.angle1 = standardcalc.angleBetweenTwoCoords(self.source1, self.dest1)
        self.angle2 = standardcalc.angleBetweenTwoCoords(self.dest1, self.source1)
        
        self.angle1value = self.angle1.degrees()
        self.angle2value = self.angle2.degrees()
        
    def testAngle1(self):        
        self.assertEqual(self.angle1value, 0)
        self.assertEqual(self.angle2value, 180)