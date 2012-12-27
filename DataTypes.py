#DataTypes.py 
#Data type module for UBC Sailbot 2013 Control Team
#Initialy Created: Sam Coulter, Nov. 3rd 2012
#Last Updated: November 29th

import math

class Coordinate:
	def __Init__(self):
		print("Do some even Cooler stuff")

class GPSCoordinate:
	def __init__(self):
		print("Do Some Cool Stuff")

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

	def __pow__(self, power):
		return self._value**power



class Angle:
	def __init__(self, target):
		self._degree = float(target)
		self._balance()

	def degree(self):
		return self._degree

	def radian(self):
		return math.radians(self._degree)

	def set(self, target):
		self._degree = float(target)
		self._balance()

	def add(self, target):
		self._degree += float(target)
		self._balance()
	
	def _balance(self):
		while (self._degree < 0):
			self._degree = self._degree + 360
		if (self._degree >= 360):
			self._degree = self._degree % 360

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

	def __pow__(self, power):
		return Angle(self._degree**float(power))


if (__name__ == "__main__"):
	print "DataTypes.py"