#DataTypes.py 
#Data type module for UBC Sailbot 2013 Control Team
#Initialy Created: Sam Coulter, Nov. 3rd 2012
#Last Updated: Above

#TODO Nov 3:
#		Need to implement overloaded operators for Angle and BountInt
#		Details at: http://docs.python.org/2/reference/datamodel.html
import math

class BoundInt:
	def __init__(self, target = 0, low=0, high=1):
		if(type(target) != BoundInt):
			self.lowerLimit = low
			self.upperLimit = high
			self._value = target
			self._balance()
		elif(type(target) == BoundInt &&):
			self.lowerLimit = target.lowerLimit
			self.upperLimit = target.upperLimit
			self._value = target._value
			self._balance()
	
	def _balance(self):
		if (self._value > self.upperLimit):
			self._value = self.upperLimit
		elif (self._value < self.lowerLimit):
			self._value = self.lowerLimit
		self._value = int(round(self._value))

	def value(self):
		self._balance()
		return self._value

	def set(self, target):
		self._value = target
		self._balance()

	def __str__(self):
		return str(self._value)

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
		self._degree = target
		self._balance()

	def degree(self):
		return self._degree

	def radian(self):
		return math.radians(self._degree)

	def set(self, target):
		self._degree = target
		self._balance()

	def add(self, target):
		self._degree += target
		self._balance()
	
	def _balance(self):
		while (self._degree < 0):
			self._degree = self._degree + 360
		if (self._degree >= 360):
			self._degree = self._degree % 360

	def __str__(self):
		return str(self._degree)


if (__name__ == "__main__"):
	errorCount = 0
	#INFORMAL unit tests for Bounded Value Class
	#TODO: Formalize
	print "Testing BoundInt Class:"
	
	x = BoundInt()
	print "x = " + str(x) + " == 0"
	if (x.value() == 0):
		print "Default Construction test Passed"
	else:
		errorCount += 1
		print "Default Construction test Failed"

	x.set(2)
	print x
	x = BoundInt(0,-10,10)
	x.set(-20)
	print x
	x.set(20)
	print x

	#INFORMAL unit tests for Angle Class
	#TODO: Formalize
	print "Testing Angle Class"
	x = Angle(0)
	print x
	x.set(370)
	print x
	x.add(10)
	print x
	x.set(-10)
	print x
	x.set(0)
	x.add(-10)
	print x
	x.set(-370)
	print x
	x.set(0)
	print str(x.radian())
	x.set(180)
	print str(x.radian())
	x.set(360)
	print str(x.radian())
	print x