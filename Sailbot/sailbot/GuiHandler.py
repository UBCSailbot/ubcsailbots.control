'''
Created on Jan 21, 2013

@author: joshandrews

'''

import sailbot.GlobalVars as gVars
import sailbot.StaticVars as sVars
import sailbot.challenge as challenge
import sailbot.logic.coresailinglogic as sl

# GUI Handler Class
#    * GUI can call any of these functions and rest will be taken care of
class GuiHandler:
    
    # when the user sends new instructions
    # the control code will update its instructions object
    # When the remote control signals a switch to auto then the instructions are carried out
    def setInstructions(self, instructionsData):
        # Stores current boundaries
        gVars.boundaries = instructionsData.boundaries
        gVars.instructions = instructionsData
        # Stores function queue and parameter queue
        if (instructionsData.challenge == 0):
            for waypoint in instructionsData.waypoints:
                gVars.functionQueue.append(getattr(sl, waypoint.wtype))
                gVars.queueParameters.append(waypoint.coordinate)
                
        elif (instructionsData.challenge == sVars.NAVIGATION_CHALLENGE):
            gVars.functionQueue.append(getattr(challenge.navigation, "run"))
            gVars.queueParameters.append(tuple(instructionsData.waypoints))
        elif (instructionsData.challenge == sVars.STATION_KEEPING_CHALLENGE):
            gVars.functionQueue.append(getattr(challenge.stationkeeping, "run"))
            gVars.functionQueue.append(getattr(challenge.stationkeeping, "run"))
        elif (instructionsData.challenge == sVars.LONG_DISTANCE_CHALLENGE):
            gVars.functionQueue.append(getattr(challenge.longdistance, "run"))
            gVars.functionQueue.append(getattr(challenge.stationkeeping, "run"))
            
    # returns the  instructions object
    def getInstructions(self):        #main.returninstructionsdataforgui
        return gVars.instructions
    
    # returns all the telemetry data as an object
    # ex. apparent wind, gps location, SOG, COG, heading, etc.
    def getData(self):
        return gVars.currentData
    
    
    #returns a string of debug messages
    def getDebugMessages(self):
        #debug messages should be appended to a string buffer
        #this buffer will be cleared every time this function is called
        #a limit could be placed on the length of this buffer (ex. 100 lines)
        pass
