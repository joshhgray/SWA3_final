import pandas as pd
import requests
import logging
import json

class DataCollector:
    def __init__(self, api_url, api_key=None):
        """
        Initialize Data Collector.
        :param api_url: The URL of the external API.
        :param api_key: The API key for authentication.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None
        }
        logging.info(f"DataCollector initialized with API URL: {self.api_url}")
        
    def fetch_data(self):
        """
        Fetch data from external API.
        :return: response data in JSON format.
        """
        try:
            logging.info("Fetching data from the API. . .")
            res = requests.get(self.api_url, headers=self.headers)
            res.raise_for_status()
            data = res.json()
            logging.info("Data successfuly fetched.")
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return None
        
    def process_data(self, data):
        """
        Pre-process raw data fetched from the API.
        :param data: Raw data from the API.
        :return: Processed data.
        """
        logging.info("Processing data. . .")
        # TODO - preprocess data
        return data
    
    def save_data(self, data, output_file="output.json"):
        """
        Saves data to file.
        :param data: The data to be saved.
        :param output_file: The file to store the data.
        """
        try:
            logging.info(f"Saving data to {output_file}. . .")
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
            logging.info(f"Successfully saved data to {output_file}")
        except Exception as e:
            logging.error(f"Error saving data: {e}")
            
    # TODO - Add method for passing data to data analyzer
    # TODO - Add scheduler to API pull
    
    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO)
        #api_url = TODO -
        #api_key = TODO -
        
        collector = None # TODO - DataCollector(api_url, api_key)
        raw_data = None  # TODO - collector.fetch_data()
        if raw_data:
            processed_data = collector.process_data(raw_data)
            collector.save_data(processed_data)