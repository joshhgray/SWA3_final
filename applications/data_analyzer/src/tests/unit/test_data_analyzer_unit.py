import unittest
from applications.frontend.src.main.app import init_dash_app
from applications.data_collector.src.main.data_collector import create_app, db

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        self.flask_app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        # mock 
    


if __name__ == '__main__':
    unittest.main()