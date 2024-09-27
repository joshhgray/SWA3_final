import unittest
from applications.frontend.src.main.app import app

class TestDataAnalyzer(unittest.TestCase):
    # TODO - add unit tests for methods in data analyzer
    def test_temp(self):
        # temp
        x = 5
        self.assertEqual(x, 5)
    
        

if __name__ == '__main__':
    unittest.main()