from applications.data_collector.src.main.data_collector import DataCollector
from unittest.mock import patch, mock_open, MagicMock
import unittest

class TestDataCollector(unittest.TestCase):
    def setUp(self):
        self.collector = DataCollector(
            base_endpoint="https://api.fda.gov/drug/event.json",
            api_key=None
        )

    @patch("applications.data_collector.src.main.data_collector.requests.get")
    def test_fetch_data(self, mock_get):
        # mock res
        mock_res = MagicMock()
        mock_res.json.return_value = {
            "results": [
                {"safetyreportid": "5801206-7"},
                {"safetyreportid": "4318221-5"}
            ]
        }
        mock_get.return_value = mock_res

        data = self.collector.fetch_data(search="", count=2, num_calls=1, delay=0)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertEqual(data[1]["safetyreportid"], "4318221-5")

    def test_process_data(self):
        # Sample JSON result from openFDA API
        sample_input = [{
            "safetyreportid": "5801206-7",
            "receivedate": "20080707",
            "serious": "1",
            "seriousnessdeath": "1",
            "patient": {
                "patientonsetage": "26",
                "patientsex": "1",
                "drug": [{
                    "drugcharacterization": "1",
                    "medicinalproduct": "DURAGESIC-100",
                    "drugindication": "DRUG ABUSE"
                }],
                "reaction": [
                    {"reactionmeddrapt": "DRUG ADMINISTRATION ERROR"},
                    {"reactionmeddrapt": "OVERDOSE"}
                ]
            }
        }]

        events, drugs, reactions = self.collector.process_data(sample_input)

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].safety_report_id, "5801206-7")
        self.assertEqual(len(drugs), 1)
        self.assertEqual(drugs[0].drug_name, "DURAGESIC-100")
        self.assertEqual(len(reactions), 2)
        self.assertEqual(reactions[0].reaction_medical_term, "DRUG ADMINISTRATION ERROR")
        

        
       
        
        
        
        

