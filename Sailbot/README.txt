===========
UBC Sailbot
===========

UBC Sailbot runs the UBC Sailbot control system.  Running __main__ starts a loop which will continue to run until told otherwise by the GUI.

Architecture of __main__
========================

  GlobalVars                 Main Thread
      |                           |          
      |                     ------| if (function in queue)
      |                     |     |--------
      |          while(run) |     |       |
      |                     |     |       | run (function) on Background Thread
      |                     |     |       | 
      |             get()   |     |       |
      ----------------------|     |       |
                            |     |       |
                            -------       |
                                          |
                                  |       |
                                          |
                                  |       |
                                          |
                                  |       |
                                  --------- join() when complete

GUIHandler
==========

The GUI must import the Datatypes.py class containing the necessary objects to send over to control.  

The important types to be used are:

* Instructions
* Waypoint
* Boundary
* GPS Coordinate

The GUI sends instructions to the GUIHandler which will parse the data and add function queues