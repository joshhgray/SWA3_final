import unittest
from applications.frontend.src.main.app import app as dash_app


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = dash_app.server.test_client()
        self.app.testing = True

    def test_main(self):
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()
