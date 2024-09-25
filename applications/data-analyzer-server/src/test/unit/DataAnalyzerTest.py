import unittest
from applications.frontend.src.main.app import app

class TestDataAnalyzer(unittest.TestCase):
    def test_data_analyzer(self):
        self.assertIsNotNone(app)

if __name__ == '__main__':
    unittest.main()