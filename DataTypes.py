#DataTypes module for UBC Sailbot 2013 Control Team
import math

class BoundInt:
	def __init__(self, low=0, high=1):
		#stuff
		self.x = 100


class Angle:
	def __init__(self, target):
		self._degree = target
		self.balance()

	def degree(self):
		return self._degree

	def radian(self):
		return math.radians(self._degree)

	def set(self, target):
		self._degree = target
		self.balance()

	def add(self, target):
		self._degree += target
		self.balance()
	
	def balance(self):
		while (self._degree < 0):
			self._degree = self._degree + 360
		if (self._degree >= 360):
			self._degree = self._degree % 360

	def __str__(self):
		return str(self._degree)


if (__name__ == "__main__"):
	#INFORMAL unit tests for Angle Class
	#Todo: Formalize
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