'''
Created on Jan 20, 2013

@author: joshandrews
'''

import unittest
import serial as ser
from control.piardio import arduino
from mock import MagicMock

class testGetFromArduino(unittest.TestCase):
    def setUp(self):
        self.returnstr = "1, 2, 3, 4, 5, 6, 7, 8, 9"
        self.returnarr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.returnstrnospace = "1,2,3,4,5,6,7,8,9"
        self.ard = arduino.arduino()
        
    def testNoReturn(self):
        self.ser = ser.Serial()
        ser.Serial = MagicMock(return_value=self.ser)
        self.ser.readLine = MagicMock(return_value=None)
        self.assertEqual(self.ard.getFromArduino(), None)
        
    def testWithReturn(self):
        self.ser = ser.Serial()
        ser.Serial = MagicMock(return_value=self.ser)
        self.ser.readLine = MagicMock(return_value=self.returnstr)
        self.assertEqual(self.ard.getFromArduino(), self.returnarr)
        
    def testWithReturnNoSpace(self):
        self.ser = ser.Serial()
        ser.Serial = MagicMock(return_value=self.ser)
        self.ser.readLine = MagicMock(return_value=self.returnstrnospace)
        self.assertEqual(self.ard.getFromArduino(), self.returnarr)
        
if __name__ == '__main__':
    unittest.main()