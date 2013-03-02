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

SERIAL_PORT = '/dev/ttyACM0'
BAUD = 57600

class arduino:
    
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
    
    # calls adjust_rudder on arduino with rudder percentage
    def adjust_rudder(self, rudder_percent):                                                
        ser = serial.Serial(SERIAL_PORT, BAUD)
        # Format
        #    "ADJUST_RUDDER,<rudder_percent>"
        wr = "ADJUST_RUDDER,{rp}".format(rp=rudder_percent)
        ser.write(wr)
        
    # calls adjust_sheets on arduino with sheet percentage
    def adjust_sheets(self, sheet_percent):                                                
        ser = serial.Serial(SERIAL_PORT, BAUD)
        # Format
        #    "ADJUST_SHEETS,<sheet_percent>"
        wr = "ADJUST_SHEETS,{sp}".format(sp=sheet_percent)
        ser.write(wr)
        
    # calls steer on arduino with method and degree
    def steer(self, method, degree):
        ser = serial.Serial(SERIAL_PORT, BAUD)
        # Format
        #    "STEER,<method>,<degree>"
        wr = "STEER,{m},{d}".format(m=method, d=degree)
        ser.write(wr)
    
    # calls tack on arduino    
    def tack(self):
        ser = serial.Serial(SERIAL_PORT, BAUD)
        # Format
        #    "TACK,"
        wr = "TACK,"
        ser.write(wr)
     
    # Calls gybe on the arduino
    def gybe(self):
        ser = serial.Serial(SERIAL_PORT, BAUD)
        # Format
        #    "GYBE,"
        wr = "GYBE,"
        ser.write(wr)
    
    # returns the latest array of all info from the arduino
    def getFromArduino(self):
        # First parameter: serial port for the APM
        #     * to get serial port for the APM, type ls /dev/tty* ont he pi
        # Second parameter: baud rate on APM
        ser = serial.Serial(SERIAL_PORT, BAUD)
        # Splits comma-separated string (ex-"1, 12, 123, 1234, 12345") into array
        ardArr = []
        # Waits for a response from the Arduino
        timesTried = 0
        while (len(ardArr) == 0 and timesTried < 10 and ser):
            readarr = ser.readLine()
            if (readarr is not None):
                ardArr = re.findall("[^,\s][^\,]*[^,\s]*", readarr)
                i = 0
                while (i < len(ardArr)):
                    ardArr[i] = float(ardArr[i])
                    i +=1
                
            timesTried += 1
            
        if (len(ardArr) > 0):
            return ardArr
        else:
            return None
