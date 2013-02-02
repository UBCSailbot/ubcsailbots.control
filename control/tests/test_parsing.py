#Unit Tests of parsing.py Module

import unittest
from control.parser import parsing
from os import path

class TestParsing(unittest.TestCase):
	def setUp(self):
		self.fname = "test_file"
	def test_noFile(self):
		self.assertEqual(parsing.parse(""), None)
		self.assertEqual(parsing.parse("fakeFile"), None)
	def test_yesFile(self):
		self.assertEqual(parsing.parse(path.join(path.dirname(__file__), self.fname))[1][1], 7)

if __name__ == '__main__':
	unittest.main()