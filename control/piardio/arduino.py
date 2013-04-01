'''
Created on Jan 19, 2013

@author: joshandrews

Data interpreter: Returns values for current state passed from the arduino
Format of return from Arduino is defined by index in StaticVars
'''

import serial
import re
import sys
sys.path.append("..")
from control.datatype import datatypes
from serial.tools import list_ports
import control.StaticVars as sVars
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUD = 57600
PC = True

ARD_AUT = 0     # Auto Mode
ARD_LONG = 1    # GPS Longitude
ARD_LAT = 2     # GPS Latitude
ARD_COG = 3     # Course over Ground
ARD_HOG = 4     # Heading over Ground
ARD_AWA = 5     # Apparent Wind Angle
ARD_AWAV = 6    # Apparent Wind Angle Average
ARD_SHT = 7     # Sheet Percentage
ARD_SAT = 8     # Number of Satellites
ARD_ACC = 9     # GPS Accuracy
ARD_SOG = 10    # Speed over Ground
ARD_RUD = 11    # Rudder Angle

coms = list_ports.comports()
print coms
usbserials = []
for com in coms:
    for port in com:
        if "usbserial" in port:
            usbserials.append(port)

if (len(usbserials) > 0):
    SERIAL_PORT = usbserials[0]

if (PC):
    SERIAL_PORT = 'COM3' 
    
class arduino:
    
    def __init__(self):
        self.ser = serial.Serial(SERIAL_PORT, BAUD)
        
    # Calls adjust_sheets on arduino with sheet percentage
    def adjust_sheets(self, sheet_percent):                                                
        # Format
        #    "ADJUST_SHEETS,<sheet_percent>"
        wr = "ADJUST_SHEETS,{sp}\r\n".format(sp=sheet_percent)
        print wr
        self.ser.write(wr)
        time.sleep(.1)
        
    # Calls steer on arduino with method and degree
    # COMPASS_METHOD = 0
    # COG_METHOD = 1
    # AWA_METHOD = 2 
    def steer(self, method, degree):
        # Format
        #    "STEER,<method>,<degree>"
        wr = "STEER,{m},{d}\n".format(m=method, d=degree)
        print wr
        self.ser.write(wr)
        time.sleep(.1)
    
    # Calls tack on arduino    
    def tack(self, weather, tack):
        # Format
        #     Tack: Port=0 Stbd=1
        #    "TACK,<Weather>, <WindwardSideOfBoat>"
        wr = "TACK,{w},{t}".format(w=weather, t=tack)
        print wr
        self.ser.write(wr)
        time.sleep(.1)
     
    # Calls gybe on the arduino
    def gybe(self, tack):
        # Format
        #    Gybe: Port=0 Stbd=1
        #    "GYBE,<WindwardSideOfBoat>"
        wr = "GYBE,{t}".format(t=tack)
        self.ser.write(wr)
        time.sleep(.1)
    
    # Returns the latest array of all info from the arduino
    def getFromArduino(self):

        self.ser.flushInput()
        ardArr = []
        ardBuffer = ''
        for i in range(0,1):
            buff = self.ser.read(600)
            if (buff):
                ardBuffer = ardBuffer + buff
            if '\n' in ardBuffer:
                lines = ardBuffer.split('\n') # Guaranteed to have at least 2 entries
                ardArr = lines[-2]
                #If the Arduino sends lots of empty lines, you'll lose the
                #last filled line, so you could make the above statement conditional
                #like so: if lines[-2]: last_received = lines[-2]
                ardBuffer = lines[-1]                
        print ardArr
        if (len(ardBuffer) > 0):
            ardArr = ardArr.replace(" ", "")
        if (len(ardArr) > 0):
            ardArr = re.findall("[^,\s][^\,]*[^,\s]*", ardArr)
            i = 0
            while (i < len(ardArr)):
                ardArr[i] = float(ardArr[i])
                i+=1     
        if (len(ardArr) > 0):
            arr = self.interpretArr(ardArr)
            return arr
        else:
            return None
    
    # Takes an array from the arduino and maps it to the appropriate objects in the python array
    def interpretArr(self, ardArr):
        arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        arr[sVars.HOG_INDEX] = ardArr[ARD_HOG]
        arr[sVars.COG_INDEX] = ardArr[ARD_COG]
        arr[sVars.SOG_INDEX] = ardArr[ARD_SOG]
        arr[sVars.AWA_INDEX] = ardArr[ARD_AWAV]
        arr[sVars.GPS_INDEX] = datatypes.GPSCoordinate(ardArr[ARD_LAT]/10000000, ardArr[ARD_LONG]/10000000)
        arr[sVars.SHT_INDEX] = ardArr[ARD_SHT]
        arr[sVars.SAT_INDEX] = ardArr[ARD_SAT]
        arr[sVars.ACC_INDEX] = ardArr[ARD_ACC]
        arr[sVars.AUT_INDEX] = ardArr[ARD_AUT]
        arr[sVars.RUD_INDEX] = ardArr[ARD_RUD]
        return arr
