from applications.data_collector.src.main.data_collector import create_app, db, AdverseEvent, Drug, Reaction
from datetime import date
import logging
import random

def populate_test_db(app, n_drugs=50):
    """
    This function is for populating an in-memory temporary database used for testing and debugging.
    The database is filled with random data.
    For debugging convenience.

    :param n_drugs: number of drugs to fill temp database with
    """
    logging.basicConfig(level=logging.INFO)

    with app.app_context():
        db.drop_all()
        db.create_all()

        events = []
        drugs = []
        reactions = []

        for i in range(n_drugs):
            report_id = f"FAKE-{i}"
            events.append(AdverseEvent(
                safety_report_id=report_id,
                received_date=date.today(),
                serious=random.choice([True, False]),
                seriousness_death=random.choice([True, False]),
                patient_age=random.randint(1, 99),
                patient_sex=random.choice(["male", "female", "unknown"])
            ))

            drugs.append(Drug(
                event_id=report_id,
                drug_characterization="Testing",
                drug_name=f"Fake-Drug-{i:03}",
                drug_indication=str(random.randint(1, 2))
            ))

            reactions.append(Reaction(
                event_id=report_id,
                reaction_medical_term=random.choice(["fake reaction 1", "fake reaction 2",
                                                     "fake reaction 3", "fake reaction 4"])
            ))

        db.session.bulk_save_objects(events + drugs + reactions)
        db.session.commit()

        logging.info(f"Inserted {len(events)} events into the test database.")

if __name__ == "__main__":
    app = create_app(testing=True)
    populate_test_db(app)


