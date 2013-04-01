===================
UBC Sailbot Control
===================

UBC Sailbot runs the UBC Sailbot control system.  Running __main__ starts a loop which will continue to run until told otherwise by the GUI.

Steps to get project running:
1) Navigate to top level directory
2) Run 'python setup.py install_lib' (May need sudo before or run as admin)
3) Run 'python setup.py test' (May need sudo before or run as admin)
4) Navigate to control directory
5) Start code, run 'python __main__.py'

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

From console in top level run: 'python setup.py install_lib'

To run the project you must have all libraries installed

Tests
=====

From console in top level run: 'python setup.py test'

If a class is written which can be unit tested, it should be unit tested.  All tests must be added to control/tests package and named test_{file_being_tested}.py.  To run simulation tests, you may run the Mock Arudino as documented elsewhere in this document.

Core Sailing Logic & Standard Calc
==================================

All sailing logic is in a module logic/coresailinglogic.  In that module you may call roundBuoyPort, roundBuoyStbd, and pointToPoint.  This logic relies on standard calculation methods which can be found inside of the module logic/standardcalc.  Any new helper methods which are not directly related toward a specific function may be put in logic/standardcalc.  All new sailing logic may be put in logic/coresailinglogic.

Challenges
==========

All challenges are in the package challenge.  You must import each challenge module individually to run it. To run a challenge, import the individual package and call {challenge}.run(params).

Naming
======

All static variables are contained within the StaticVars module.  If you wish to add a new challenge, you must define its name inside of StaticVars.  Any new waypoint types must also be added to StaticVars.


Mock Arduino
============

To activate set mock bool in main.

Mocks an arduino class which should feed back information as if the boat was in the water.  Use this class to test code in a simulation mode.  There are parameters which can be explicitly set in the class to test implementation code in different ways.

Logging
=======

There is support for logging throughout the entire project which logs to a file in log/sailbot.log.  To access the logger call functions on 'logger' in GlobalVar.
Example Calls:
	globvar.logger.warning("Warning Message")
    	globvar.logger.debug("Debug Message")
    	globvar.logger.critical("Critical Message")

Test change
