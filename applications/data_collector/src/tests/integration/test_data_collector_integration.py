from applications.data_collector.src.main.data_collector import db, create_app, AdverseEvent, Drug, Reaction, DataCollector
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import unittest

class TestDataCollectorIntegration(unittest.TestCase):
    def setUp(self):
        """
        Setup a temporary app and DB.
        """
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        with self.app.app_context():
            db.create_all()

        self.collector = DataCollector(base_endpoint="", api_key=None)

    def tearDown(self):
        # Tear down temporary DB
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_fetch_process_save(self):
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

        with self.app.app_context():
            self.collector.save_data(events, drugs, reactions)

            self.assertEqual(db.session.query(AdverseEvent).count(), 1)
            self.assertEqual(db.session.query(Drug).count(), len(drugs))
            self.assertEqual(db.session.query(Reaction).count(), len(reactions))

            event = db.session.query(AdverseEvent).first()
            self.assertEqual(event.patient_age, 26)