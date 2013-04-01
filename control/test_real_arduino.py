import unittest
import serial as ser
from piardio import arduino
import StaticVars as sVars
import time
from nose.tools import nottest

class testGetFromArduino(unittest.TestCase):
    def setUp(self):
        self.ard = arduino.arduino()
    
    @nottest 
    def testReturn(self):
        arr = self.ard.getFromArduino()
        print("Heading: " + str(arr[sVars.HOG_INDEX]) + ", COG: " + str(arr[sVars.COG_INDEX]) + ", SOG: " + 
              str(arr[sVars.SOG_INDEX]) + ", AWA: " + str(arr[sVars.AWA_INDEX]) + ", GPS[" + str(arr[sVars.GPS_INDEX]) 
              + "]" + ", Sheet Percent: " + str(arr[sVars.SHT_INDEX]) + ", Num of Satellites: " + str(arr[sVars.SAT_INDEX]))
        #self.ard.ser.close()
    
    @nottest 
    def testSend(self):
        time.sleep(1)
        self.ard.adjust_sheets(50)
        time.sleep(1)
        self.testReturn()
        self.ard.ser.close() 

if __name__ == '__main__':
    unittest.main()