import unittest
from datetime import date
from applications.data_collector.src.main.data_collector import create_app, db, Drug, Reaction, AdverseEvent
from applications.data_analyzer.src.main.data_analyzer import get_age_distribution_for_drug, get_top_drugs, get_top_reactions_by_age

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        # Mock AdverseEvent, Drug, and Reaction data
        mock_event = AdverseEvent(
            safety_report_id="test-id-1",
            received_date=date(2025, 1, 1),
            patient_sex="Male",
            patient_age=28,
            seriousness_death=False,
        )
        mock_drug = Drug(
            event_id="test-id-1",
            drug_name="Lipitor",
        )
        mock_reaction = Reaction(
            event_id="test-id-1",
            reaction_medical_term="Headache"
        )

        db.session.add_all([mock_event, mock_drug, mock_reaction])
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    """
    Test analysis functions
    """
    def test_get_top_drugs(self):
        top_drugs = get_top_drugs()
        self.assertIn("Lipitor", top_drugs)

    def test_get_age_distribution_for_drug(self):
        age_distribution = get_age_distribution_for_drug("Lipitor")
        self.assertTrue(any(distro["age_group"] == "19-44" for distro in age_distribution))

    def test_get_top_reaction_by_age(self):
        reactions = get_top_reactions_by_age("Lipitor")
        self.assertIn("19-44", reactions)
        self.assertEqual(reactions["19-44"]['reaction'], "Headache")

if __name__ == '__main__':
    unittest.main()