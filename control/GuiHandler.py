'''
Created on Jan 21, 2013

GUI Handler for the control logic
-   The GUI sends instructions to the GUIHandler which 
    will parse the data and add function queues.

@author: joshandrews
'''

import control.GlobalVars as gVars
import control.StaticVars as sVars
import control.challenge as challenge
import control.logic.coresailinglogic as sl
import control.datatype.datatypes as dt

# GUI Handler Class
#    * GUI can call any of these functions and rest will be taken care of
class GuiHandler:
    
    # when the user sends new instructions
    # the control code will update its instructions object
    # When the remote control signals a switch to auto then the instructions are carried out
    def setInstructions(self, instructionsData):
        # Stores current boundaries
        gVars.currentProcess = None
        gVars.boundaries = instructionsData.boundaries
        gVars.instructions = instructionsData
        # Stores function queue and parameter queue
        if (instructionsData.challenge == 0):
            for waypoint in instructionsData.waypoints:
                gVars.functionQueue.append(waypoint.wtype)
                gVars.queueParameters.append(tuple(waypoint.coordinate, ))
                
        elif (instructionsData.challenge == sVars.NAVIGATION_CHALLENGE):
            gVars.functionQueue.append(getattr(challenge.navigation, "run"))
            gVars.queueParameters.append(tuple(instructionsData.waypoints))
        elif (instructionsData.challenge == sVars.STATION_KEEPING_CHALLENGE):
            gVars.functionQueue.append(getattr(challenge.stationkeeping, "run"))
            gVars.queueParameters.append(tuple(instructionsData.waypoints))
        elif (instructionsData.challenge == sVars.LONG_DISTANCE_CHALLENGE):
            gVars.functionQueue.append(getattr(challenge.longdistance, "run"))
            gVars.queueParameters.append(tuple(instructionsData.waypoints))
            
    # returns the  instructions object
    def getInstructions(self):        #main.returninstructionsdataforgui
        return gVars.instructions
    
    # returns all the telemetry data as an object
    # ex. apparent wind, gps location, SOG, COG, heading, etc.
    def getData(self):
        arr = gVars.currentData
        output = {"telemetry":{"Heading": arr[sVars.HOG_INDEX], "COG" : arr[sVars.COG_INDEX], "SOG" : arr[sVars.SOG_INDEX], "AWA" : arr[sVars.AWA_INDEX], "latitude": arr[sVars.GPS_INDEX].lat , "longitude" : arr[sVars.GPS_INDEX].long, "SheetPercent": arr[sVars.SHT_INDEX]},
                  "connectionStatus":{"gpsSat":arr[sVars.SAT_INDEX],"HDOP":arr[sVars.ACC_INDEX]}, "automode":arr[sVars.AUT_INDEX]}
        return output
    
    #returns a string of debug messages
    def getDebugMessages(self):
        #debug messages should be appended to a string buffer
        #this buffer will be cleared every time this function is called
        #a limit could be placed on the length of this buffer (ex. 100 lines)
        pass
