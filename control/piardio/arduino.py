'''
Created on Jan 19, 2013

@author: joshandrews

Data interpreter: Returns values for current state passed from the arduino
Format of return from Arduino:
    TODO
'''
import serial
import re
import sys
sys.path.append("..")
import control.datatype.datatypes as datatype
from serial.tools import list_ports
import control.StaticVars as sVars

SERIAL_PORT = '/dev/ttyACM0'
BAUD = 57600

ARD_AUT = 0
ARD_LONG = 1
ARD_LAT = 2
ARD_COG = 3
ARD_HOG = 4
ARD_AWA = 5
#Apparent Wind Average
ARD_AWAV = 6
#Sheet Percentage
ARD_SHT = 7
#Num Satalites
ARD_SAT = 8
#GPS Accuracy
ARD_ACC = 9
ARD_SOG = 10

coms = list_ports.comports()
print coms
usbserials = []
for com in coms:
    for port in com:
        if "usbserial" in port:
            usbserials.append(port)

if (len(usbserials) > 0):
    SERIAL_PORT = usbserials[0]
    
class arduino:
    
    def __init__(self):
        self.ser = serial.Serial(SERIAL_PORT, BAUD)
        
    # returns Heading Over Ground
    def getHOG(self):
        # Example
        #     HOG = getFromArduino()[0]
        #     return datatypes.Angle(HOG)
        return datatype.Angle()
    
    # returns Course Over Ground
    def getCOG(self):
        return datatype.Angle()
    
    # returns Apparent Wind Angle
    def getAWA(self):
        return datatype.Angle()
    
    # returns GPS coordinate
    def getGPSCoordinate(self): 
        return datatype.GPSCoordinate()
    
    # returns Rudder Angle
    def getRudderAngle(self):
        return datatype.Angle()
    
    # returns Sheet Percentage
    def getSheetPercentage(self):
        return 0
        
    # calls adjust_sheets on arduino with sheet percentage
    def adjust_sheets(self, sheet_percent):                                                
        # Format
        #    "ADJUST_SHEETS,<sheet_percent>"
        wr = "ADJUST_SHEETS,{sp}\r\n".format(sp=sheet_percent)
        print wr
        self.ser.write(wr)
        
    # calls steer on arduino with method and degree
    # TODO:
    #    Change documentation so method is type 0, 1, 2 based on:
    #        enum sailByCourse {  
    #                            compassMethod,
    #                            cogMethod,
    #                            apprentWindMethod  
    #                           };  
    def steer(self, method, degree):
        # Format
        #    "STEER,<method>,<degree>"
        wr = "STEER,{m},{d}\n".format(m=method, d=degree)
        print wr
        self.ser.write(wr)
    
    # calls tack on arduino    
    def tack(self):
        # Format
        #    "TACK,"
        wr = "TACK,"
        print wr
        self.ser.write(wr)
     
    # Calls gybe on the arduino
    def gybe(self):
        # Format
        #    "GYBE,"
        wr = "GYBE,"
        self.ser.write(wr)
    
    # returns the latest array of all info from the arduino
    def getFromArduino(self):
        
        # First parameter: serial port for the APM
        #     * to get serial port for the APM, type ls /dev/tty* ont he pi
        # Second parameter: baud rate on APM
        
        # Splits comma-separated string (ex-"1, 12, 123, 1234, 12345") into array
        ardArr = []
        # Waits for a response from the Arduino
        timesTried = 0
        while (len(ardArr) == 0 and timesTried < 10 and self.ser):
            readarr = self.ser.read(600)
            print readarr
            newarr = ""
            if '\n' in readarr:
                lines = readarr.split('\n') # Guaranteed to have at least 2 entries
                newarr = lines[-2]
            print newarr
            newarr = newarr.replace(" ", "")
            if (newarr is not None):
                ardArr = re.findall("[^,\s][^\,]*[^,\s]*", newarr)
                i = 0
                while (i < len(ardArr)):
                    ardArr[i] = float(ardArr[i])
                    i +=1
                
            timesTried += 1
            
        if (len(ardArr) > 0):
            arr = self.interpretArr(ardArr)
            return arr
        else:
            return None
        
    def interpretArr(self, ardArr):
        arr = [0, 0, 0, 0, 0, 0, 0, 0]
        arr[sVars.HOG_INDEX] = ardArr[ARD_HOG]
        arr[sVars.COG_INDEX] = ardArr[ARD_COG]
        arr[sVars.SOG_INDEX] = ardArr[ARD_SOG]
        arr[sVars.AWA_INDEX] = ardArr[ARD_AWAV]
        arr[sVars.GPS_INDEX] = datatype.GPSCoordinate(ARD_LAT, ARD_LONG)
        arr[sVars.SHT_INDEX] = ardArr[ARD_SHT]
        arr[sVars.SAT_INDEX] = ardArr[ARD_SAT]
        arr[sVars.ACC_INDEX] = ardArr[ARD_ACC]
        return arr
