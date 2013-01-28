'''
Created on Jan 21, 2013

@author: joshandrews

'''

import sailbot.datatype.datatypes as datatype
import sailbot.GlobalVar
import sailbot.StaticVars

# GUI Handler Class
#    * GUI can call any of these functions and rest will be taken care of
class GuiHandler:
    
    # when the user sends new instructions
    # the control code will update its instructions object
    # When the remote control signals a switch to auto then the instructions are carried out
    def setInstructions(self, instructionsData):
        pass
    
    
    # returns the  instructions object
    def getInstructions(self):        #main.returninstructionsdataforgui
        pass
    
    # returns all the telemetry data as an object
    # ex. apparent wind, gps location, SOG, COG, heading, etc.
    def getData(self):
        pass
    
    
    #returns a string of debug messages
    def getDebugMessages(self):
        #debug messages should be appended to a string buffer
        #this buffer will be cleared every time this function is called
        #a limit could be placed on the length of this buffer (ex. 100 lines)
        pass
