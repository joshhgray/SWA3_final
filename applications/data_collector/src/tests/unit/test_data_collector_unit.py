import unittest
from unittest.mock import patch, mock_open, MagicMock
from applications.data_collector.src.main.data_collector import DataCollector

class TestDataCollector(unittest.TestCase):
    def setUp(self):
        self.api_url = "https://api.example.com/data"
        self.api_key = "test_api_key"
        self.collector = DataCollector(self.api_url, self.api_key)
        
    # TODO - implement unit test for fetch_data()
    # def test_fetch_data(self, mock_get):

        
    # TODO - implement unit test for process_data()
    # def test_process_data(self):
    #     raw_data = {"key": "value"}
    #     processed_data = self.collector.process_data(raw_data)
        
    # TODO - Imlpement test for save_data()
    #def test_save_data(self):
        
       
        
        
        
        

