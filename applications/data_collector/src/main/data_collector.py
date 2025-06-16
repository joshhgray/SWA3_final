from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask
import requests
import logging
import time
import os

load_dotenv()
api_key = os.getenv("OPEN_FDA_KEY")

app = Flask(__name__)

# Manually fix URL - Heroku using deprecated postgres:// update to postgresql://
raw_url = os.getenv("DATABASE_URL", "")
if raw_url and raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = raw_url

db = SQLAlchemy(app)
class AdverseEvent(db.Model):
    safety_report_id = db.Column(db.String, primary_key=True)
    received_date = db.Column(db.Date)
    patient_sex = db.Column(db.String(10))
    patient_age = db.Column(db.Float)
    serious = db.Column(db.Boolean)
    seriousness_death = db.Column(db.Boolean)

    drugs = db.relationship("Drug", backref="event", cascade="all, delete-orphan")
    reactions = db.relationship("Reaction", backref="event", cascade="all, delete-orphan")

class Drug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String, db.ForeignKey('adverse_event.safety_report_id'))
    drug_name = db.Column(db.String(100))
    drug_indication = db.Column(db.String(200))
    drug_characterization = db.Column(db.String(10))

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String, db.ForeignKey('adverse_event.safety_report_id'))
    reaction_medical_term = db.Column(db.String(200))


class DataCollector:
    def __init__(self, base_endpoint, api_key):
        """
        Initialize Data Collector.
        # """
        self.base_endpoint = base_endpoint
        self.api_key = api_key
        logging.info(f"DataCollector initialized.")
        
    def fetch_data(self, search, count, num_calls, limit):
        """
        Fetch data from openFDA Drug Adverse Events API. 

        :param count: Number of records to return per API call (Max: 1000, default: 1).
        :param num_calls: Number of requests (Max: 240/min, 120,000/day with API key).
        :param limit: Delay between requests (Min: 0.25 to satisfy Max num_calls).
        :return: response data in JSON format.
        """
        logging.info("Fetching data from the API. . .")
        combined_res = []

        for i in range(num_calls):
            skip = i * count
            query_params = {
                "search": search,
                "limt": limit,
                "skip": skip,
                "api_key": self.api_key,
            }

            try:
                res = requests.get(self.base_endpoint, params=query_params)
                batch = res.json().get("results", [])
                combined_res.extend(batch)
                time.sleep(limit)
                
            except:
                logging.error(f'Error fetching data from API.')
                break

        logging.info(f"Fetched {len(combined_res)} results")
        return combined_res

        
    def process_data(self, raw_data):
        """
        Pre-process raw data from JSON to Python Objects.
        :param raw_data: Raw data from the API.
        :return: Processed data.
        """
        logging.info("Processing data. . .")
        adverse_events = []
        drugs = []
        reactions = []

        for entry in raw_data:
            try:
                report_id = entry["safetyreportid"] # PK
                event = AdverseEvent(
                    safety_report_id = report_id,
                    received_date = datetime.strptime(entry["receivedate"], "%Y%m%d").date(),
                    serious = entry.get("serious") == "1", # 1 if true 0 otherwise (false, null, etc)
                    seriousness_death = entry.get("seriousnessdeath") == 1,
                    patient_age = float(entry["patient"].get("patientonsetage")),
                    patient_sex = {"1": "male", "2": "female"}.get(entry["patient"].get("patientsex")),
                )
                adverse_events.append(event)

                for drug in entry["patient"].get("drug", []):
                    drugs.append(Drug(
                        event_id=report_id, #FK
                        drug_characterization=drug.get("drugcharacterization"),
                        drug_name = drug["medicinalproduct"],
                        drug_indication=drug.get("drugindication"),
                    ))
                
                for reaction in entry["patient"].get("reaction", []):
                    reactions.append(Reaction(
                        event_id=report_id, # FK
                        reaction_medical_term=reaction["reactionmeddrapt"]
                    ))

            except Exception as e:
                logging.error(f"Error parsing adverse Event: {e}")
                continue

        return adverse_events, drugs, reactions
    
    def save_data(self, events, drugs, reactions):
        """
        Saves data to file.
        :param events: Adverse Events table
        :param drugs: Drugs table
        :param reactions: Reactions table
        """
        try:
            logging.info(f"Saving data to Database. . .")
            db.session.bulk_save_objects(events)
            db.session.bulk_save_objects(drugs)
            db.session.bulk_save_objects(reactions)
            db.session.commit()
            logging.info(f"Saved {len(events)} events to Database. ")
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving data: {e} \n Rolling back.")
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    base_endpoint = "https://api.fda.gov/drug/event.json"
    search = "" # TODO
    count = 1000
    num_calls = 5
    limit = 1

    collector = DataCollector(base_endpoint=base_endpoint, api_key=api_key)
    raw_data = collector.fetch_data(search=search, count=count, num_calls=num_calls, limit=limit)

    # preprocess raw data if it exsists
    if raw_data:
        events, drugs, reactions = collector.process_data(raw_data)
        collector.save_data(events, drugs, reactions)