import unittest
import sys
sys.path.append("..")
from control.challenge import stationkeeping
from control.datatype import datatypes

class TestSetBoxCoords(unittest.TestCase):
    def setUp(self):
        self.coord1 = datatypes.GPSCoordinate(2.0,2.0) #square
        self.coord2 = datatypes.GPSCoordinate(2.0,3.0)
        self.coord3 = datatypes.GPSCoordinate(1.0,3.0)
        self.coord4 = datatypes.GPSCoordinate(1.0,2.0)
        
        self.coord5 = datatypes.GPSCoordinate(1.0, 2.0)  # diamond
        self.coord6 = datatypes.GPSCoordinate(2.0, 3.0)
        self.coord7 = datatypes.GPSCoordinate(3.0, 2.0)
        self.coord8 = datatypes.GPSCoordinate(2.0, 1.0)
        
        self.coord9 = datatypes.GPSCoordinate(2.0, 1.0)  # right tilted square
        self.coord10 = datatypes.GPSCoordinate(4.0, 2.0)
        self.coord11 = datatypes.GPSCoordinate(1.0, 3.0)
        self.coord12 = datatypes.GPSCoordinate(3.0, 4.0)
        
        self.coord13 = datatypes.GPSCoordinate(2.0, 4.0)  # left tilted square
        self.coord14 = datatypes.GPSCoordinate(1.0, 2.0)
        self.coord15 = datatypes.GPSCoordinate(3.0, 1.0)
        self.coord16 = datatypes.GPSCoordinate(4.0, 3.0)
        
        self.coordlist1 = []
        self.coordlist2 = []
        self.coordlist3 = []
        self.coordlist4 = []
        self.coordlist5 = []
        
    def testSetSquare(self):
        self.coordlist1 = stationkeeping.setBoxCoords(self.coord2, self.coord4, self.coord3, self.coord1)
        self.assertEqual((self.coordlist1[0] == self.coord1),1)
        self.assertEqual((self.coordlist1[1] == self.coord2),1)
        self.assertEqual((self.coordlist1[2] == self.coord3),1)
        self.assertEqual((self.coordlist1[3] == self.coord4),1)              
    def testSetDiamond1(self):
        self.coordlist2 = stationkeeping.setBoxCoords(self.coord7, self.coord8, self.coord6, self.coord5)
        self.assertEqual((self.coordlist2[0] == self.coord8),1)
        self.assertEqual((self.coordlist2[1] == self.coord7),1)
        self.assertEqual((self.coordlist2[2] == self.coord6),1)
        self.assertEqual((self.coordlist2[3] == self.coord5),1)
    def testSetDiamond2(self):
        self.coordlist3 = stationkeeping.setBoxCoords(self.coord5, self.coord6, self.coord8, self.coord7)
        self.assertEqual((self.coordlist3[0] == self.coord8),1)
        self.assertEqual((self.coordlist3[1] == self.coord7),1)
        self.assertEqual((self.coordlist3[2] == self.coord6),1)
        self.assertEqual((self.coordlist3[3] == self.coord5),1)
    def testSetRSquare(self):
        self.coordlist4 = stationkeeping.setBoxCoords(self.coord10, self.coord11, self.coord9, self.coord12)
        self.assertEqual((self.coordlist4[0] == self.coord10),1)
        self.assertEqual((self.coordlist4[1] == self.coord12),1)
        self.assertEqual((self.coordlist4[2] == self.coord11),1)
        self.assertEqual((self.coordlist4[3] == self.coord9),1)
    def testSetLSquare(self):
        self.coordlist5 = stationkeeping.setBoxCoords(self.coord15, self.coord13, self.coord14, self.coord16)
        self.assertEqual((self.coordlist5[0] == self.coord15),1)
        self.assertEqual((self.coordlist5[1] == self.coord16),1)
        self.assertEqual((self.coordlist5[2] == self.coord13),1)
        self.assertEqual((self.coordlist5[3] == self.coord14),1)