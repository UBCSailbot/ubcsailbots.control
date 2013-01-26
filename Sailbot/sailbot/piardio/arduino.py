'''
Created on Jan 19, 2013

@author: joshandrews

Data interpreter: Returns values for current state passed from the arduino
Format of return from Arduino:
    TODO
'''

import serial
import re
from sailbot.datatype import datatypes

# returns Heading Over Ground
def getHOG():
    # Example
    #     HOG = getFromArduino()[0]
    #     return datatypes.Angle(HOG)
    return datatypes.Angle()

# returns Course Over Ground
def getCOG():
    return datatypes.Angle()

# returns Apparent Wind Angle
def getAWA():
    return datatypes.Angle()

# returns GPS coordinate
def getGPSCoordinate(): 
    return datatypes.GPSCoordinate()

# returns Rudder Angle
def getRudderAngle():
    return datatypes.Angle()

# returns Sheet Percentage
def getSheetPercentage():
    return 0

# calls adjust_sheets on arduino with sheet percentage
def adjust_sheets(sheet_percent):                                                
    ser = serial.Serial('/dev/ttyACM0', 57600)
    # Format
    #    "ADJUST_SHEETS:<sheet_percent>"
    wr = "ADJUST_SHEETS:{sp}".format(sp=sheet_percent)
    ser.write(wr)
    
# calls steer on arduino with method and degree
def steer(method, degree):
    ser = serial.Serial('/dev/ttyACM0', 57600)
    # Format
    #    "STEER:<method>,<degree>"
    wr = "STEER:{m},{d}".format(m=method, d=degree)
    ser.write(wr)
    
# returns the latest array of all info from the arduino
def getFromArduino():
    # First parameter: serial port for the APM
    #     * to get serial port for the APM, type ls /dev/tty* ont he pi
    # Second parameter: baud rate on APM
    ser = serial.Serial('/dev/ttyACM0', 57600)
    # Splits comma-separated string (ex-"1, 12, 123, 1234, 12345") into array
    ardArr = []
    # Waits for a response from the Arduino
    while (len(ardArr) == 0):
        ardArr = re.findall("[^,\s][^\,]*[^,\s]*", ser.readLine())
    return ardArr