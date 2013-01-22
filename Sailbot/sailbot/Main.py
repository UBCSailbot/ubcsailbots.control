'''
Created on Jan 19, 2013

@author: joshandrews
'''
import sys
import thread
from piardio import arduino
import challenge
import logic

# Array for all current data from arduino
#    Format: TODO
currentData = []
functionQueue = []
queueParameters = []
boundaries = []
run = True
currentProcess = None
currentParams = None

# Constant names for challenges and logic
NAVIGATION_CHALLENGE = "challenge.navigation"
STATION_KEEPING_CHALLENGE = "challenge.stationkeeping"
LONG_DISTANCE_CHALLENGE = "challenge.longdistance"
POINT_TO_POINT = "logic.coresailinglogic.pointToPoint"
STATION_KEEP = "logic.coresailinglogic.stationKeep"
ROUND_BUOY = "logic.coresailinglogic.roundBuoy"

# All Getters/Setters
def getBoundaries():
    return boundaries

def setBoundaries(bou):
    boundaries = bou
    
def getCurrentData():
    return currentData

def setCurrentData(curr):
    currentData = curr
    
def getFunctionQueue():
    return functionQueue

def setFunctionQueue(func):
    functionQueue = func

def getQueueParameters():
    return queueParameters

def setQueueParameters(que):
    queueParameters = que
    
def getRun():
    return run

def setRun(r):
    run = r
    
def getCurrentProcess():
    return currentProcess

def setCurrentProcess(proc):
    currentProcess = proc
    

# Main - pass challenge or logic function name as argument
def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    while (run):
        currentData = arduino.getFromArduino()
        # When the function queue has waiting calls, and there is no currently running process,
        # switch processes to the next function in the queue (FIFO)
        if (len(functionQueue) > 0 and currentProcess is None):
            currentProcess = functionQueue.pop(0)
            currentParams = queueParameters.pop(0)
            thread.start_new_thread(currentProcess, currentParams)
    

    
if __name__ == '__main__':
    sys.exit(main())
