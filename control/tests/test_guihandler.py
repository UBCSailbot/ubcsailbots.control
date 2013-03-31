# Unit tests for the guihandler

import unittest
from control import GuiHandler
from control import GlobalVars as gVars
from control import StaticVars as sVars
from control.datatype import datatypes
from datetime import datetime
class TestGuiHandler(unittest.TestCase):
    def setUp(self):
        self.x = GuiHandler.GuiHandler()
        gVars.taskStartTime = datetime.now()
    
    def resetGlobVar(self):
        gVars.boundaries = []
        gVars.currentData = []
        gVars.functionQueue = []  
        gVars.instructions = None
        gVars.queueParameters = []
          
    def testSetInstructionsWithNoChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.NO_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.x.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sVars.GO_TO])
        self.assertEqual(gVars.queueParameters, [(datatypes.GPSCoordinate(1, 1), )])
    
    def testSetInstructionsWithNavChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.NAVIGATION_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.x.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sVars.NAVIGATION_CHALLENGE])
        self.assertEqual(gVars.queueParameters[0][0].coordinate.lat, 1)
    
    def testSetInstructionsWithStationKeepChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.STATION_KEEPING_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.x.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sVars.STATION_KEEPING_CHALLENGE])
        self.assertEqual(gVars.queueParameters[0][0].coordinate.lat, 1)
    
    def testSetInstructionsWithLDChallenge(self):
        self.resetGlobVar()
        self.instructions = datatypes.Instructions(sVars.LONG_DISTANCE_CHALLENGE, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.x.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sVars.LONG_DISTANCE_CHALLENGE])
        self.assertEqual(gVars.queueParameters[0][0].coordinate.lat, 1)
         
    def testGetCurrentData(self):
        self.resetGlobVar()
        self.currdata = [0, 1, 2, 3, datatypes.GPSCoordinate(4, 4) , 5, 6, 7, 8, 0, 20]
        gVars.currentData = self.currdata
        self.x.getData()
        if (not gVars.taskStartTime):
            seconds = None
        else:
            seconds = (datetime.now() - gVars.taskStartTime).total_seconds()
            seconds = round(seconds)
        self.assertEquals(self.x.getData(), {"telemetry":{"Heading": self.currdata[sVars.HOG_INDEX], "COG" : self.currdata[sVars.COG_INDEX], "SOG" : self.currdata[sVars.SOG_INDEX], "AWA" : self.currdata[sVars.AWA_INDEX], "latitude": self.currdata[sVars.GPS_INDEX].lat , "longitude" : self.currdata[sVars.GPS_INDEX].long, "SheetPercent": self.currdata[sVars.SHT_INDEX], "Rudder":self.currdata[sVars.RUD_INDEX]},
                  "connectionStatus":{"gpsSat":self.currdata[sVars.SAT_INDEX],"HDOP":self.currdata[sVars.ACC_INDEX], "automode":self.currdata[sVars.AUT_INDEX]},
                  "currentProcess":{"name":gVars.currentProcess,"Starttime":seconds}})
        
if __name__ == '__main__':
    unittest.main()
