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

Angles
======

Angles are always between -180 and 180

                  * ^ *                       
               *    |    *                        
             *      |      *                 
            *       |       *                
           *        |        *               
           *    -   |   +    *              
           *        |        *               
            *       |       *                
             *      |      *                  
               *    |    *                    
                  * | *                       
            -180        +180                
       

Libraries
========

To run the project you must have the mock and serial libraries installed. To do this, go to the control/lib folder and install the egg folder into site-packages by unzipping the folder, navigating to the directory and running "python setup.py install".

Core Sailing Logic & Standard Calc
==================================

All sailing logic is in a module logic/coresailinglogic.  In that module you may call roundBuoyPort, roundBuoyStbd, and pointToPoint.  This logic relies on standard calculation methods which can be found inside of the module logic/standardcalc.  Any new helper methods which are not directly related toward a specific function may be put in logic/standardcalc.  All new sailing logic may be put in logic/coresailinglogic.

Challenges
==========

All challenges are in the package challenge.  You must import each challenge module individually to run it. To run a challenge, import the individual package and call {challenge}.run(params).

Naming
======

All static variables are contained within the StaticVars module.  If you wish to add a new challenge, you must define its name inside of StaticVars.  Any new waypoint types must also be added to StaticVars.

