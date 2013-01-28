#Unit Tests of parsing.py Module

import unittest
from sailbot.parser import parsing
import os

class TestParsing(unittest.TestCase):
	def setUp(self):
		self.fname = "test_file"
	def test_noFile(self):
		self.assertEqual(parsing.parse(""), None)
		self.assertEqual(parsing.parse("fakeFile"), None)
	def test_yesFile(self):
		self.assertEqual(parsing.parse(os.path.join(os.path.dirname(__file__), 'test_file'))[1][1], 7)

if __name__ == '__main__':
	unittest.main()