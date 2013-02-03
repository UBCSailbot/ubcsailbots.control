'''
Created on Jan 26, 2013

Static Variables for the control logic and GUI
-   All static variables are contained within the StaticVars module.
    If you wish to add a new challenge, you must define its name 
    inside of StaticVars.  Any new Waypoint types must also be added 
    to StaticVars.

'''

# Constant names for challenges and logic
NAVIGATION_CHALLENGE = "challenge.navigation"
STATION_KEEPING_CHALLENGE = "challenge.stationkeeping"
LONG_DISTANCE_CHALLENGE = "challenge.longdistance"

# -- Logic Waypoint Types --
# Point to Point waypoint types
GO_TO = "pointToPoint"

# Round Buoy waypoint types
GO_AROUND_PORT = "roundBuoyPort"
GO_AROUND_STBD = "roundBuoyStbd"

# -- Challenge Waypoint types --
# Long Distance Challenge waypoint types
LD_START_FINISH = "ld_start_finish"
LD_FIRST = "ld_first"
LD_SECOND = "ld_second"

# Navigation Challenge waypoint types
NAV_FIRST = "nav_first"
NAV_FINISH ="nav_finish"
# Station Keeping Challenge waypoint types
SK_TOP_LEFT = "sk_top_left"
SK_TOP_RIGHT = "sk_top_right"
SK_BOTTOM_LEFT = "sk_bottom_left"
SK_BOTTOM_RIGHT = "sk_bottom_right"

ACCEPTANCE_DISTANCE = 3
AWA_THRESHOLD = 1