#Unit Tests of DataTypes.py Module

import unittest
from DataTypes import *

class TestBoundInt(unittest.TestCase):
	def setUp(self):
		self.x = BoundInt()
		self.y = BoundInt(-20,-10,10)

	def test_constructor(self):
		self.assertEqual(self.x.value(), 0)
		self.assertEqual(self.y.value(), -10)

	def test_outofboundassignment(self):
		self.y.set(20)
		self.assertEqual(self.y.value(), 10)

	def test_changebounds(self):
		self.y.setBound(0,10)
		self.y.set(-10)
		self.assertEqual(self.y.value(), 0)

		self.y.setLowerBound(5)
		self.assertEqual(self.y.value(), 5)

		self.y.setUpperBound(8)
		self.y.set(10)
		self.assertEqual(self.y.value(), 8)

if __name__ == '__main__':
	unittest.main()



			#What is the pythonic way to handle unit tests? Is there a 3rd party library ala JUnit or something we can use?
	errorCount = 0
	#INFORMAL unit tests for Bounded Value Class
	#TODO: Formalize
	print "Testing BoundInt Class:"
	
	#I think this way of handling unit tests is horrendous. -Sam
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