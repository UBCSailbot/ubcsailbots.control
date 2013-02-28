# Unit tests for the guihandler

import unittest
from control import GuiHandler
from control import GlobalVars as gVars
from control import StaticVars as sVars
from control.datatype import datatypes
from control.logic import coresailinglogic as sl
import control.challenge.navigation as nav
import control.challenge.stationkeeping as sk
import control.challenge.longdistance as ld
class TestGuiHandler(unittest.TestCase):
    def setUp(self):
        self.x = GuiHandler.GuiHandler()
    
    def resetGlobVar(self):
        gVars.boundaries = []
        gVars.currentData = []
        gVars.functionQueue = []  
        gVars.instructions = None
        gVars.queueParameters = []
          
    def testSetInstructionsWithNoChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(0, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.x.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sl.pointToPoint])
        self.assertListEqual(gVars.queueParameters, [datatypes.GPSCoordinate(1, 1)])
    
    def testSetInstructionsWithNavChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.NAVIGATION_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.x.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [nav.run])
        self.assertListEqual(gVars.queueParameters, [(datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO),)])
    
    def testSetInstructionsWithStationKeepChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.STATION_KEEPING_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.x.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sk.run])
        self.assertListEqual(gVars.queueParameters, [(datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO),)])
    
    def testSetInstructionsWithLDChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.LONG_DISTANCE_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.x.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [ld.run])
        self.assertListEqual(gVars.queueParameters, [(datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO),)])
         
    def testGetCurrentData(self):
        self.resetGlobVar()
        self.currdata = [1, 2, 3, 4, 5, 6, 7]
        gVars.currentData = self.currdata
        self.assertEquals(self.x.getData(), {"telemetry":{"Heading": self.currdata[0], "COG" : self.currdata[1], "SOG" : self.currdata[2], "AWA" : self.currdata[3], "latitude": datatypes.GPSCoordinate(self.currdata[4]).lat , "longitude" : datatypes.GPSCoordinate(self.currdata[4]).long, "Rudder" : self.currdata[5], "SheetPercent": self.currdata[6]}})
        
if __name__ == '__main__':
    unittest.main()
