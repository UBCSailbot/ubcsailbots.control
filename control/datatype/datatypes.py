#datatypes.py 
#Data type module for UBC Sailbot 2013 Control Team
#Initialy Created: Sam Coulter, Nov. 3rd 2012
#Last Updated: January 19th - SC

import math

class Coordinate:
	#This class will be python representation of a coordinate
	#ie: degree.minute.second
	#the values of each should wrap around, and incrememnt eachother
	#properly
	def __init__(self):
		print("Do some even Cooler stuff")

class GPSCoordinate:
	#This class will be a python representation of GPS coordinates
	#ie with a latitude/longitude made up of "Coordinates"
	#the class should support coordinate operations similar to vector
	#operations, ie GPSCoord1 - GPSCoord2 = A direction and magnitude
	#from one coordinate to the other.
	def __init__(self, latitude=0, longitude=0):
		self.lat = latitude
		self.long = longitude
		
	def __repr__(self):
		return str("{lat}, {long}".format(lat=self.lat, long=self.long))
	
	def __str__(self):
		return str("{lat}, {long}".format(lat=self.lat, long=self.long))
	
	def __eq__(self, other):
		return (self.lat == other.lat and self.long == other.long)

# Binds an int to a specific upper and lower bound
class BoundInt():
	def __init__(self, target = 0, low=0, high=1):
		self._value, self.lowerLimit, self.upperLimit = int(target), int(low), int(high)
	
	def _balance(self):
		if (self._value > self.upperLimit):
			self._value = self.upperLimit
		elif (self._value < self.lowerLimit):
			self._value = self.lowerLimit
		self._value = int(round(self._value))

	def value(self):
		self._balance()
		return int(self._value)

	def set(self, target):
		self._value = int(target)
		self._balance()

	def setBound(self, low, high):
		self.upperLimit = int(high)
		self.lowerLimit = int(low)

	def setLowerBound(self, low):
		self.lowerLimit = int(low)

	def setUpperBound(self, high):
		self.upperLimit = int(high)

	def __str__(self):
		return str(self._value)

	def __int__(self):
		self._balance()
		return int(self._value)

	def __add__(self, other):
		return self._value + other

	def __sub__(self, other):
		return self._value - other

	def __mul__(self, other):
		return self._value * other

	def __div__(self, other):
		return self._value / other

	def __radd__(self, other):
		return self._value + other

	def __rsub__(self, other):
		return self._value - other

	def __rmul__(self, other):
		return self._value * other

	def __rdiv__(self, other):
		return self._value / other

	def __pow__(self, power):
		return self._value**power

# Instantiates angle between -180 and 180 degrees
class Angle:
	def __init__(self, target=0):
		self._degree = float(target)
		self._balance()

	def degrees(self):
		return self._degree

	def radians(self):
		return math.radians(self._degree)

	def set(self, target):
		self._degree = float(target)
		self._balance()

	def add(self, target):
		self._degree += float(target)
		self._balance()
	
	def _balance(self):
		while (self._degree <= -180):
			self._degree = self._degree + 360
		while (self._degree > 180):
			self._degree = self._degree - 360

	def __str__(self):
		return str(self._degree)

	def __int__(self):
		self._balance()
		return int(round(self._degree))

	def __float__(self):
		self._balance()
		return float(self._degree)

	def __add__(self, other):
		return Angle(self._degree + float(other))

	def __sub__(self, other):
		return Angle(self._degree - float(other))

	def __mul__(self, other):
		return Angle(self._degree * float(other))

	def __div__(self, other):
		return Angle(self._degree / float(other))

	def __radd__(self, other):
		return Angle(self._degree + float(other))

	def __rsub__(self, other):
		return Angle(self._degree - float(other))

	def __rmul__(self, other):
		return Angle(self._degree * float(other))

	def __rdiv__(self, other):
		return Angle(self._degree / float(other))

	def __pow__(self, power):
		return Angle(self._degree**float(power))

# Instantiates a waypoint for interpretation by the control logic
class Waypoint:
	def __init__(self, coordinate, wtype=""):
		self.coordinate = coordinate
		self.wtype = wtype
	
	def __eq__(self, other):
		return (self.coordinate == other.coordinate and self.wtype == other.wtype)


# Instantiates a circular boundary set by a GPS Coordinate and a radius
class Boundary:
	def __init__(self, coordinate, radius=0):
		self.coordinate = coordinate
		self.radius = radius

# Instructions which contain all instructions passed from a GUI to the control logic
class Instructions:
	def __init__(self, challenge="", waypoints=[], boundaries=[]):
		self.challenge = challenge
		self.waypoints = waypoints
		self.boundaries = boundaries

if (__name__ == "__main__"):
	print "DataTypes.py"