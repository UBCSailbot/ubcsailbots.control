'''
Created on Mar 9, 2013

@author: joshandrews
'''

import logging
from os import path

class logger:
    def __init__(self):
        logging.basicConfig(filename=path.join(path.dirname(__file__),'log/sailbot.log'), format='%(levelname)s:%(message)s', level=logging.DEBUG)
        self.logger = logging.getLogger("sailbot.log")
        self.buffer = ""
    
    def warn(self, msg):
        self.logger.warn(msg)
        self.buffer += ("[WARN]:" + msg + "\n")
        
    def warning(self, msg):
        self.logger.warning(msg)
        self.buffer += ("[WARNING]:" + msg + "\n")    
        
    def critical(self, msg):
        self.logger.critical(msg)
        self.buffer += ("[CRITICAL]:" + msg + "\n")
    
    def debug(self, msg):
        self.logger.debug(msg)
        self.buffer += ("[DEBUG]:" + msg + "\n")
    
    def error(self, msg):
        self.logger.error(msg)
        self.buffer += ("[ERROR]:" + msg + "\n")  
          
    def info(self, msg):
        self.logger.info(msg)
        self.buffer += ("[INFO]:" + msg + "\n")  
        
    def clearBuffer(self):
        self.buffer = ""
