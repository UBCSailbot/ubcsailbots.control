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

Libraries
========

To run the project you must have the mock and serial libraries installed. To do this, go to the control/lib folder and install the egg folder into site-packages by unzipping the folder, navigating to the directory and running "python setup.py install".

Core Sailing Logic & Standard Calc
==================================

All sailing logic is in a module logic/coresailinglogic.  In that module you may call roundBuoyPort, roundBuoyStbd, and pointToPoint.  This logic relies on standard calculation methods which can be found inside of the module logic/standardcalc

Challenges
==========

All challenges are in the package challenge.  You must import each challenge module individually to run it. To run a challenge, import the individual package and call {challenge}.run(params).

