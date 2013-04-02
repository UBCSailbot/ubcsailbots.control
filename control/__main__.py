'''
Created on Jan 19, 2013

@author: joshandrews
'''
import sys
import thread
import logging
import sched
import time
from datetime import datetime
from os import path
from challenge import longdistance
from challenge import navigation
from challenge import stationkeeping
from logic import coresailinglogic
from control import sailbotlogger
from datatype import datatypes
import control.GlobalVars as gVars
import control.StaticVars as sVars
import piardio.arduino
import piardio.mockarduino

# Mock:
    #   - If true, mock will run from a mock arduino class which simulates boat and wind conditions (see readme)
    #   - If false, mock will run off of an actual arduino through dev/tty ports     
mock = True

# Main - pass challenge or logic function name as argument
def main(argv=None):
    #with open(path.join(path.dirname(__file__),'log/sailbot.log'), 'w'):
    #    pass
    #logging.basicConfig(filename=path.join(path.dirname(__file__),'log/sailbot.log'), format='%(levelname)s:%(message)s', level=logging.DEBUG)
    #logger = logging.getLogger("sailbot.log")
    gVars.logger = sailbotlogger.logger()
    gVars.logger.info("Start")
    
    print("Mock Enabled: " + str(mock))
    if (mock == False):        
        arduino = piardio.arduino.arduino()
    else:
        arduino = piardio.mockarduino.arduino()
    gVars.arduino = arduino
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, setGlobVar, (arduino, s,))
    thread.start_new_thread(s.run, ())
    i = 0
    while (gVars.run):
        # When the function queue has waiting calls, and there is no currently running process,
        # switch processes to the next function in the queue (FIFO)
        i +=1
        if i == 5:
            coresailinglogic.roundBuoyPort(datatypes.GPSCoordinate(49.276037,-123.195105), 179)
        if (len(gVars.functionQueue) > 0 and gVars.currentProcess is None):
            gVars.currentProcess = gVars.functionQueue.pop(0)
            gVars.currentParams = gVars.queueParameters.pop(0)
            if (gVars.currentProcess == sVars.GO_AROUND_PORT or gVars.currentProcess == sVars.GO_AROUND_STBD or gVars.currentProcess == sVars.GO_TO):
                gVars.taskStartTime = datetime.now()
                thread.start_new_thread(getattr(coresailinglogic, gVars.currentProcess), gVars.currentParams)
            elif (gVars.currentProcess == sVars.NAVIGATION_CHALLENGE):
                gVars.taskStartTime = datetime.now()
                thread.start_new_thread(navigation.run, gVars.currentParams)
            elif (gVars.currentProcess == sVars.STATION_KEEPING_CHALLENGE):
                gVars.taskStartTime = datetime.now()
                thread.start_new_thread(stationkeeping.run, gVars.currentParams)
            elif (gVars.currentProcess == sVars.LONG_DISTANCE_CHALLENGE):
                gVars.taskStartTime = datetime.now()
                thread.start_new_thread(longdistance.run, gVars.currentParams)
            else:
                gVars.logger.warning("No instruction task named " + str(gVars.currentProcess))
                gVars.currentProcess = None
                gVars.currentParams = None
        time.sleep(1)
        

def setGlobVar(arduino, sc):
    gVars.currentData = gVars.arduino.getFromArduino()
    printArdArray(gVars.currentData)
    if (mock):
        sc.enter(1, 1, setGlobVar, (gVars.arduino, sc,))
    else:
        sc.enter(.3, 1, setGlobVar, (gVars.arduino, sc,))
    
def printArdArray(arr):
    print("Heading: " + str(arr[sVars.HOG_INDEX]) + ", COG: " + str(arr[sVars.COG_INDEX]) + ", SOG: " + str(arr[sVars.SOG_INDEX]) + ", AWA: " + str(arr[sVars.AWA_INDEX]) + ", GPS[" + str(arr[sVars.GPS_INDEX]) + "]" + ", Sheet Percent: " + str(arr[sVars.SHT_INDEX]) + ", Num of Satellites: " + str(arr[sVars.SAT_INDEX]) + ", Accuracy: " + str(arr[sVars.ACC_INDEX]) + ", Rudder: " + str(arr[sVars.RUD_INDEX]))
    
if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print ("\n Exit - Keyboard Interrupt")
