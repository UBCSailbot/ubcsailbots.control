#Unit tests of standardcalc.py module

import unittest
from sailbot.logic import standardcalc
from sailbot.datatype import datatypes

class TestDistBetweenTwoCoords(unittest.TestCase):
    def setUp(self):
        self.point1 = datatypes.GPSCoordinate(0,0)
        self.point2 = datatypes.GPSCoordinate(1,1)
        
    def test1(self):
        self.assertEqual(round(standardcalc.distBetweenTwoCoords(self.point1, self.point2),1), 157.2)
