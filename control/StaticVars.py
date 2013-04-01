'''
Created on Jan 26, 2013

Static Variables for the control logic and GUI
-   All static variables are contained within the StaticVars module.
    If you wish to add a new challenge, you must define its name 
    inside of StaticVars.  Any new Waypoint types must also be added 
    to StaticVars.

'''

# Constant names for challenges and logic
NAVIGATION_CHALLENGE = "navigation"
STATION_KEEPING_CHALLENGE = "stationkeeping"
LONG_DISTANCE_CHALLENGE = "longdistance"
NO_CHALLENGE = "NONE"

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
NAV_START_PORT ="nav_start_port"
NAV_START_STARBOARD ="nav_start_stbd"

# Station Keeping Challenge waypoint types
SK_TOP_LEFT = "sk_top_left"
SK_TOP_RIGHT = "sk_top_right"
SK_BOTTOM_LEFT = "sk_bottom_left"
SK_BOTTOM_RIGHT = "sk_bottom_right"

# Thresholds for sailing logic functions
ACCEPTANCE_DISTANCE_DEFAULT = 3     #The acceptable distance (how close the boat has to be to the waypoint before it accepts that it has reached its destination
AWA_THRESHOLD = 0.9         #Since the table has non-realistic values for AWA, this allows the AWA lookup to be off slightly
SOG_THRESHOLD = 0.9
SPEED_AFFECTION_THRESHOLD = 55     #Speed threshold at which lower speeds are shown to note have a significant variation between AWA and TWA

# Indices for current_data
HOG_INDEX=0     # Heading over Ground
COG_INDEX=1     # Course over Ground
SOG_INDEX=2     # Speed over Ground
AWA_INDEX=3     # Apparent Wind Angle Average
GPS_INDEX=4     # GPS Coordinate
SHT_INDEX=5     # Sheet Percentage
SAT_INDEX=6     # GPS Number of Satellites
ACC_INDEX=7     # GPS Accuracy (HDOP)
AUT_INDEX=8     # Auto Mode
RUD_INDEX=9     # Rudder
