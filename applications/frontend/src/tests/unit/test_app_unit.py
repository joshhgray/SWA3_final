import unittest
from applications.frontend.src.main.app import app

class AppTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_main(self):
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)
        
    def test_echo_input(self):
        res = self.app.post('/echo_user_input',
                            data=dict(user_input="test string"))
        self.assertIn(b'You entered: test string', res.data)

if __name__ == '__main__':
    unittest.main()
        