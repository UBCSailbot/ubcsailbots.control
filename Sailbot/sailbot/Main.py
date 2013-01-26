'''
Created on Jan 19, 2013

@author: joshandrews
'''
import sys
import thread
from piardio import arduino
import challenge
import logic
import GlobalVar


# Main - pass challenge or logic function name as argument
def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    while (GlobalVar.run):
        GlobalVar.currentData = arduino.getFromArduino()
        # When the function queue has waiting calls, and there is no currently running process,
        # switch processes to the next function in the queue (FIFO)
        if (len(GlobalVar.functionQueue) > 0 and GlobalVar.currentProcess is None and GlobalVar.auto):
            currentProcess = GlobalVar.functionQueue.pop(0)
            currentParams = GlobalVar.queueParameters.pop(0)
            thread.start_new_thread(currentProcess, currentParams)
    

    
if __name__ == '__main__':
    sys.exit(main())
