#Unit Tests of DataTypes.py Module

import unittest
import math
import control.datatype.datatypes as datatype
import control.StaticVars as sVars

class TestGPSCoordinate(unittest.TestCase):
	def setUp(self):
		self.x = datatype.GPSCoordinate()
		self.y = datatype.GPSCoordinate(42, -121)
	
	def testConstructor(self):
		self.assertEqual(self.x.lat, 0)
		self.assertEqual(self.x.long, 0)
		self.assertEqual(self.y.lat, 42)
		self.assertEqual(self.y.long, -121)
		
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
		self.assertEqual(self.y.degrees(), -10)

	def test_radianConversion(self):
		self.assertEqual(self.default.radians(), math.radians(0))
		self.assertEqual(self.x.radians(), math.radians(10))
		self.assertEqual(self.y.radians(), math.radians(-10))

	def test_wraparound(self):
		self.assertEqual(datatype.Angle(740).degrees(), 20)
		self.assertEqual(datatype.Angle(-400).degrees(), -40)

	def test_operators(self):
		self.assertEqual((self.x + 20).degrees(), 30)
		self.assertEqual((20 + self.x).degrees(), 30)
		self.assertEqual((self.x + 360).degrees(), 10)
		self.assertEqual((self.x - 360).degrees(), 10)

class TestWaypoint(unittest.TestCase):
	def setUp(self):
		self.x = datatype.Waypoint(datatype.GPSCoordinate())
		self.y = datatype.Waypoint(datatype.GPSCoordinate(42, -121), sVars.GO_TO)
	
	def testConstructor(self):
		self.assertEqual(self.x.coordinate.lat, 0)
		self.assertEqual(self.x.coordinate.long, 0)
		self.assertEqual(self.x.wtype, "")
		self.assertEqual(self.y.coordinate.lat, 42)
		self.assertEqual(self.y.coordinate.long, -121)
		self.assertEqual(self.y.wtype, sVars.GO_TO)

class TestBoundary(unittest.TestCase):
	def setUp(self):
		self.x = datatype.Boundary(datatype.GPSCoordinate())
		self.y = datatype.Boundary(datatype.GPSCoordinate(42, -121), 123.456)
	
	def testConstructor(self):
		self.assertEqual(self.x.coordinate.lat, 0)
		self.assertEqual(self.x.coordinate.long, 0)
		self.assertEqual(self.x.radius, 0)
		self.assertEqual(self.y.coordinate.lat, 42)
		self.assertEqual(self.y.coordinate.long, -121)
		self.assertEqual(self.y.radius, 123.456)

class TestInstructions(unittest.TestCase):
	def setUp(self):
		self.x = datatype.Instructions()
		self.y = datatype.Instructions(sVars.LONG_DISTANCE_CHALLENGE, [0, 1], [0, 1])
	
	def testConstructor(self):
		self.assertEqual(self.x.challenge, "")
		self.assertEqual(self.x.waypoints, [])
		self.assertEqual(self.x.boundaries, [])
		self.assertEqual(self.y.challenge, sVars.LONG_DISTANCE_CHALLENGE)
		self.assertEqual(self.y.waypoints, [0, 1])
		self.assertEqual(self.y.boundaries, [0, 1])
		
if __name__ == '__main__':
	unittest.main()