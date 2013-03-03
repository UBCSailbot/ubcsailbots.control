'''
Created on Jan 19, 2013

@author: joshandrews
'''
import sys
import thread
from piardio import arduino as ard
from piardio import mockarduino as mockard
import challenge
import logic
import GlobalVars as globvar
import logging
from os import path
import sched, time
from serial.tools import list_ports

# Main - pass challenge or logic function name as argument
def main(argv=None):
    logging.basicConfig(filename=path.join(path.dirname(__file__),'log/sailbot.log'), format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
    # Mock:
    #   - If true, mock will run from a mock arduino class which simulates boat and wind conditions (see readme)
    #   - If false, mock will run off of an actual arduino through dev/tty ports     
    mock = True
    if argv is None:
        argv = sys.argv
        print"Started: synchronous"
    else:
        print"Started: asynchronous"
        if (argv[1]):
            mock = argv[1]
    
    print("Mock Enabled: " + str(mock))
    if (mock == False):        
        arduino = ard.arduino()
    else:
        arduino = mockard.arduino()
    i = 0
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, setGlobVar, (arduino, s,))
    thread.start_new_thread(s.run, ())
    while (globvar.run):
        # When the function queue has waiting calls, and there is no currently running process,
        # switch processes to the next function in the queue (FIFO)
        i += 1
        if (len(globvar.functionQueue) > 0 and globvar.currentProcess is None):
            currentProcess = globvar.functionQueue.pop(0)
            currentParams = globvar.queueParameters.pop(0)
            thread.start_new_thread(currentProcess, currentParams)

def setGlobVar(arduino, sc):
    globvar.currentData = arduino.getFromArduino()
    printArdArray(globvar.currentData)
    sc.enter(1, 1, setGlobVar, (arduino, sc,))
    
def printArdArray(arr):
    print("Heading: " + str(arr[0]) + ", COG: " + str(arr[1]) + ", SOG: " + str(arr[2]) + ", AWA: " + str(arr[3]) + ", GPS[ lat=" + str(arr[4]) + " ], Rudder: " + str(arr[5]) + ", Sheet Percent: " + str(arr[6]))
    
if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print ("\n Exit - Keyboard Interrupt")
