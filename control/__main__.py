'''
Created on Jan 19, 2013

@author: joshandrews
'''
import sys
import thread
import logging
import sched
import time
import datetime
from os import path
from challenge import longdistance
from challenge import navigation
from challenge import stationkeeping
from logic import coresailinglogic
import control.GlobalVars as gVars
import control.StaticVars as sVars
import piardio.arduino
import piardio.mockarduino


# Main - pass challenge or logic function name as argument
def main(argv=None):
    #with open(path.join(path.dirname(__file__),'log/sailbot.log'), 'w'):
    #    pass
    logging.basicConfig(filename=path.join(path.dirname(__file__),'log/sailbot.log'), format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger("sailbot.log")
    gVars.logger = logger
    logger.info(datetime.datetime.now())
    # Mock:
    #   - If true, mock will run from a mock arduino class which simulates boat and wind conditions (see readme)
    #   - If false, mock will run off of an actual arduino through dev/tty ports     
    mock = False
    if argv is None:
        argv = sys.argv
        print"Started: synchronous"
    else:
        print"Started: asynchronous"
        if (argv[1]):
            mock = argv[1]
    
    print("Mock Enabled: " + str(mock))
    if (mock == False):        
        arduino = piardio.arduino.arduino()
    else:
        arduino = piardio.mockarduino.arduino()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, setGlobVar, (arduino, s,))
    thread.start_new_thread(s.run, ())
    while (gVars.run):
        # When the function queue has waiting calls, and there is no currently running process,
        # switch processes to the next function in the queue (FIFO)
        if (len(gVars.functionQueue) > 0 and gVars.currentProcess is None):
            currentProcess = gVars.functionQueue.pop(0)
            currentParams = gVars.queueParameters.pop(0)
            if (currentProcess == sVars.GO_AROUND_PORT or currentProcess == sVars.GO_AROUND_STBD or currentProcess == sVars.GO_TO):
                thread.start_new_thread(getattr(coresailinglogic, currentProcess), currentParams)
                getattr()
            elif (currentProcess == sVars.NAVIGATION_CHALLENGE):
                thread.start_new_thread(navigation.run, currentParams)
            elif (currentProcess == sVars.STATION_KEEPING_CHALLENGE):
                thread.start_new_thread(stationkeeping.run, currentParams)
            elif (currentProcess == sVars.LONG_DISTANCE_CHALLENGE):
                thread.start_new_thread(longdistance.run, currentParams)
            else:
                gVars.logger.warning("No instruction task named " + str(currentProcess))
                currentProcess = None
                currentParams = None

def setGlobVar(arduino, sc):
    gVars.currentData = arduino.getFromArduino()
    printArdArray(gVars.currentData)
    sc.enter(1, 1, setGlobVar, (arduino, sc,))
    
def printArdArray(arr):
    print("Heading: " + str(arr[sVars.HOG_INDEX]) + ", COG: " + str(arr[sVars.COG_INDEX]) + ", SOG: " + str(arr[sVars.SOG_INDEX]) + ", AWA: " + str(arr[sVars.AWA_INDEX]) + ", GPS[" + str(arr[sVars.GPS_INDEX]) + "]" + ", Sheet Percent: " + str(arr[sVars.SHT_INDEX]) + ", Num of Satellites: " + str(arr[sVars.SAT_INDEX]))
    
if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print ("\n Exit - Keyboard Interrupt")
