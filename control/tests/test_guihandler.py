# Unit tests for the guihandler

import unittest
from control import GuiHandler
from control import GlobalVars as gVars
from control import StaticVars as sVars
from control.datatype import datatypes
from control.logic import coresailinglogic as sl

class TestGuiHandler(unittest.TestCase):
    def setUp(self):
        self.x = GuiHandler.GuiHandler()
        
    def testSetInstructionsWithNoChallenge(self):
        self.instructions = datatypes.Instructions(0, [datatypes.Waypoint(datatypes.GPSCoordinate(1, 1), sVars.GO_TO)], [datatypes.Boundary(datatypes.GPSCoordinate(1, 1), 1)])
        self.x.setInstructions(self.instructions)
        self.assertTrue(gVars.instructions, self.instructions)
        self.assertListEqual(gVars.functionQueue, [sl.pointToPoint])
        self.assertListEqual(gVars.queueParameters, [datatypes.GPSCoordinate(1, 1)])
        
if __name__ == '__main__':
    unittest.main()
