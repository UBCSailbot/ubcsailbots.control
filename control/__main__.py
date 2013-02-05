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

# Main - pass challenge or logic function name as argument
def main(argv=None):
    logging.basicConfig(filename=path.join(path.dirname(__file__),'log/sailbot.log'), format='%(levelname)s:%(message)s', level=logging.DEBUG)
    mock = True
    if argv is None:
        argv = sys.argv
    else:
        if (argv[1]):
            mock = argv[1]
    
    if (mock == False):        
        arduino = ard.arduino()
    else:
        arduino = mockard.arduino()
    i = 0
    while (globvar.run):
        if (i % 5000000 == 0):
            print globvar.currentData
            globvar.currentData = arduino.getFromArduino()
        # When the function queue has waiting calls, and there is no currently running process,
        # switch processes to the next function in the queue (FIFO)
        i += 1
        if (len(globvar.functionQueue) > 0 and globvar.currentProcess is None and globvar.auto):
            currentProcess = globvar.functionQueue.pop(0)
            currentParams = globvar.queueParameters.pop(0)
            thread.start_new_thread(currentProcess, currentParams)
    

    
if __name__ == '__main__':
    sys.exit(main())
