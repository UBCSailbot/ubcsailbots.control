#Unit Tests of DataTypes.py Module

import unittest
import math
import sailbot.datatype.datatypes as datatype

class TestBoundInt(unittest.TestCase):
	def setUp(self):
		self.x = datatype.BoundInt()
		self.y = datatype.BoundInt(-20,-10,10)

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

class testAngle(unittest.TestCase):
	def setUp(self):
		self.default = datatype.Angle()
		self.x = datatype.Angle(10)
		self.y = datatype.Angle(-10)

	def test_constructor(self):
		self.assertEqual(self.default.degrees(), 0)
		self.assertEqual(self.x.degrees(), 10)
		self.assertEqual(self.y.degrees(), 350)

	def test_radianConversion(self):
		self.assertEqual(self.default.radians(), math.radians(0))
		self.assertEqual(self.x.radians(), math.radians(10))
		self.assertEqual(self.y.radians(), math.radians(350))

	def test_wraparound(self):
		self.assertEqual(datatype.Angle(740).degrees(), 20)
		self.assertEqual(datatype.Angle(-400).degrees(), 320)

	def test_operators(self):
		self.assertEqual((self.x + 20).degrees(), 30)
		self.assertEqual((20 + self.x).degrees(), 30)
		self.assertEqual((self.x + 360).degrees(), 10)
		self.assertEqual((self.x - 360).degrees(), 10)



if __name__ == '__main__':
	unittest.main()