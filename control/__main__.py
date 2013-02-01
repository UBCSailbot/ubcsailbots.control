'''
Created on Jan 19, 2013

@author: joshandrews
'''
import sys
import thread
from piardio import arduino as ard
import challenge
import logic
import GlobalVars as globvar


# Main - pass challenge or logic function name as argument
def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    arduino = ard()
    while (globvar.run):
        globvar.currentData = arduino.getFromArduino()
        # When the function queue has waiting calls, and there is no currently running process,
        # switch processes to the next function in the queue (FIFO)
        if (len(globvar.functionQueue) > 0 and globvar.currentProcess is None and globvar.auto):
            currentProcess = globvar.functionQueue.pop(0)
            currentParams = globvar.queueParameters.pop(0)
            thread.start_new_thread(currentProcess, currentParams)
    

    
if __name__ == '__main__':
    sys.exit(main())
