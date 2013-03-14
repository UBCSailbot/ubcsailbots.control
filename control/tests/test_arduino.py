'''
Created on Jan 20, 2013

@author: joshandrews
'''

import unittest
import serial
from control.piardio import arduino
from mock import MagicMock

class testGetFromArduino(unittest.TestCase):
    def setUp(self):
        self.returnstr = "\n1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 \n1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 \n1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 "
        self.returnarr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.returnstrnospace = "\n1,2,3,4,5,6,7,8,9,10,11,12 \n1,2,3,4,5,6,7,8,9,10,11,12 \n1,2,3,4,5,6,7,8,9,10,11,12"
        self.ser = serial.Serial()
        serial.Serial = MagicMock(return_value=self.ser)
        self.ser.Serial = MagicMock(return_value=None)
        self.ser.flushInput = MagicMock(return_value=None)
        self.ard = arduino.arduino()
        
    def testNoReturn(self):
        self.ser = serial.Serial()
        serial.Serial = MagicMock(return_value=self.ser)
        self.ser.read = MagicMock(return_value=None)
        self.assertEqual(self.ard.getFromArduino(), None)
        
    def testWithReturn(self):
        self.ser = serial.Serial()
        serial.Serial = MagicMock(return_value=self.ser)
        self.ser.read = MagicMock(return_value=self.returnstr)
        self.assertEqual(self.ard.getFromArduino()[0], self.returnarr[4])
                
    def testWithReturnNoSpace(self):
        self.ser = serial.Serial()
        serial.Serial = MagicMock(return_value=self.ser)
        self.ser.read = MagicMock(return_value=self.returnstrnospace)
        self.assertEqual(self.ard.getFromArduino()[0], self.returnarr[4])
        
if __name__ == '__main__':
    unittest.main()