#Unit tests of standardcalc.py module

import unittest
import math
import sys
sys.path.append("..")
from control.logic import standardcalc
from control.datatype import datatypes
from control import StaticVars as sVars
from control import GlobalVars as gVars

class TestGPSDistAway(unittest.TestCase):
    def setUp(self):
        self.source = datatypes.GPSCoordinate(49.262330, -123.248148)
        self.result1 = datatypes.GPSCoordinate(49.26322919993, -123.24677409844) #100m north, 100m east
        self.result2 = datatypes.GPSCoordinate(49.26143080008, -123.24952185164) #100m south, 100m west
        self.result3 = datatypes.GPSCoordinate(49.27132080213, -123.23440919997) #1km north, 1km east
        self.result4 = datatypes.GPSCoordinate(49.25333758688, -123.26188680003) #1km south, 1km west
    def testGPSCalc1(self):
        self.test1 = standardcalc.GPSDistAway(self.source, 100, 100)
        self.test2 = standardcalc.GPSDistAway(self.source, -100, -100)
        self.assertEqual((math.fabs(self.result1.lat - self.test1.lat) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result1.long - self.test1.long) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result2.lat - self.test2.lat) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result2.long - self.test2.long) <= 0.00004),1)
    def testGPSCalc2(self):
        self.test3 = standardcalc.GPSDistAway(self.source, 1000, 1000)
        self.test4 = standardcalc.GPSDistAway(self.source, -1000, -1000)
        self.assertEqual((math.fabs(self.result3.lat - self.test3.lat) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result3.long - self.test3.long) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result4.lat - self.test4.lat) <= 0.00004),1)
        self.assertEqual((math.fabs(self.result4.long - self.test4.long) <= 0.00004),1)
    def testGPSCalc3(self):
        self.test5 = standardcalc.GPSDistAway(self.source, 0, 0)
        self.assertEqual(self.test5.lat, self.source.lat)
        self.assertEqual(self.test5.long, self.source.long)
        
class TestDistBetweenTwoCoords(unittest.TestCase):
    def setUp(self):
        self.point1 = datatypes.GPSCoordinate(0,0)
        self.point2 = datatypes.GPSCoordinate(1,1)
        
    def testDist1(self):
        distance = standardcalc.distBetweenTwoCoords(self.point1, self.point2)
        self.assertEqual(round(distance/1000,1), 157.4)
        
class TestAngleBetweenTwoCoords(unittest.TestCase):
    def setUp(self):
        self.source1 = datatypes.GPSCoordinate(100,100)
        self.dest1 = datatypes.GPSCoordinate(300,100)
        
        self.angle1 = standardcalc.angleBetweenTwoCoords(self.source1, self.dest1)
        self.angle2 = standardcalc.angleBetweenTwoCoords(self.dest1, self.source1)
        
        self.source2 = datatypes.GPSCoordinate(0,0)
        self.dest2 = datatypes.GPSCoordinate(1,1)
        
        self.angle3 = standardcalc.angleBetweenTwoCoords(self.source2, self.dest2)
        self.angle4 = standardcalc.angleBetweenTwoCoords(self.dest2, self.source2)
        
        
    def testAngleSet1(self):        
        self.assertEqual(self.angle1, 0)
        self.assertEqual(self.angle2, 180)
        
    def testAngleSet2(self):
        self.assertEqual(round(self.angle3,0), 45)
        self.assertEqual(round(self.angle4,0), -135)
        
class TestSearchAWAIndex(unittest.TestCase):
    def setUp(self):
        self.list1 = [0,1,2,3]
        self.list2 = [0,1,2,3]
        self.big_list = list()
        self.big_list = [self.list1,self.list2]
        self.value1 = 2
        self.value2 = 2.3
        self.value3 = 20
        
    def testSearch1(self):
        self.assertEqual(standardcalc.searchAWAIndex(self.value1, self.big_list)[0][0], 0)
        self.assertEqual(standardcalc.searchAWAIndex(self.value1, self.big_list)[0][1], 2)
        self.assertEqual(standardcalc.searchAWAIndex(self.value1, self.big_list)[1][0], 1)
        self.assertEqual(standardcalc.searchAWAIndex(self.value1, self.big_list)[1][1], 2)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[0][0], 0)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[0][1], 2)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[1][0], 0)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[1][1], 3)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[2][0], 1)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[2][1], 2)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[3][0], 1)
        self.assertEqual(standardcalc.searchAWAIndex(self.value2, self.big_list)[3][1], 3)
        
class TestSearchSOGIndex(unittest.TestCase):
    def setUp(self):
        self.list1 = [0,1,2,3]
        self.list2 = [0,1,2,3]
        self.big_list = list()
        self.big_list = [self.list1,self.list2]
        self.value1 = 2
        self.value2 = 2.3
        self.value3 = 20
        
    def testSearchSOG1(self):
        self.assertEqual(standardcalc.searchSOGIndex(self.value1, self.big_list)[0][0], 0)
        self.assertEqual(standardcalc.searchSOGIndex(self.value1, self.big_list)[0][1], 2)
        self.assertEqual(standardcalc.searchSOGIndex(self.value1, self.big_list)[1][0], 1)
        self.assertEqual(standardcalc.searchSOGIndex(self.value1, self.big_list)[1][1], 2)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[0][0], 0)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[0][1], 2)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[1][0], 0)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[1][1], 3)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[2][0], 1)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[2][1], 2)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[3][0], 1)
        self.assertEqual(standardcalc.searchSOGIndex(self.value2, self.big_list)[3][1], 3)

class TestGetTrueWindAngle(unittest.TestCase):
    def setUp(self):
        self.sog1 = 127
        self.awa1 = 95
        
        self.TWA1 = standardcalc.getTrueWindAngle(self.awa1, self.sog1)
        
    def testGetTrueWindAngle1(self):
        self.assertEqual(self.TWA1, 141)
        
class TestFindCosLawAngle(unittest.TestCase):
    def testFindCosLawAngle(self):
        self.assertEqual(standardcalc.findCosLawAngle(0,1,2),0)
        self.assertEqual(standardcalc.findCosLawAngle(1,-1,2),0)
        self.assertEqual((standardcalc.findCosLawAngle(2,3,4) - 104.477) <=0.001, 1)
    
class TestMeanOfList(unittest.TestCase):
    def setUp(self):
        self.list1 = []
        self.list2 = [1,2,3,4]
        self.list3 = [-0.2, 0, 0.7, 0.9]
        self.list4 = [2]
        
    def testMeanofList1(self):
        self.assertEqual(standardcalc.meanOfList(self.list1), -1)
        self.assertEqual(standardcalc.meanOfList(self.list2), 2.5)
        self.assertEqual(standardcalc.meanOfList(self.list3), 0.35)
        self.assertEqual(standardcalc.meanOfList(self.list4), 2)
        
class TestChangeSpdList(unittest.TestCase):
    def setUp(self):
        self.list1 = []
        self.list2 = [1,2,3]
        self.list3 = standardcalc.changeSpdList(self.list2)
        
    def testChangeSpdList1(self):
        self.assertEqual(standardcalc.changeSpdList(self.list1), -1)
        self.assertEqual(self.list3[0] != 1, 1)
        self.assertEqual(self.list3[2] == gVars.currentData[sVars.SOG_INDEX], 1)