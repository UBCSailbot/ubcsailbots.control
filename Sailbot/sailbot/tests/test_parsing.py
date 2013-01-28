#Unit Tests of parsing.py Module

import unittest
from sailbot.parser import parsing

class TestParsing(unittest.TestCase):
	def setUp(self):
		self.fname = "test_file"
	def test_noFile(self):
		self.assertEqual(parse(""), None)
		self.assertEqual(parse("fakeFile"), None)
	def test_yesFile(self):
		self.assertEqual(parse("test_file")[1][1], 7)
if __name__ == '__main__':
    unittest.main()