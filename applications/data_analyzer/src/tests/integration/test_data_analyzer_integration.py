import unittest
from applications.frontend.src.main.app import app

class TestDataAnalyzerIntegration(unittest.TestCase):
    def test_data_analyzer_integration(self):
        self.assertIsNotNone(app)
        
    # TODO - build a more robust test set for integration

if __name__ == '__main__':
    unittest.main()