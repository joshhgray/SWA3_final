import unittest
from applications.frontend.src.main.app import init_dash_app
from applications.data_collector.src.main.data_collector import create_app


class AppTest(unittest.TestCase):

    def setUp(self):
        self.flask_app = create_app(testing=True)
        self.dash_app = init_dash_app(self.flask_app)
        self.client = self.dash_app.server.test_client()

    def test_main(self):
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()
