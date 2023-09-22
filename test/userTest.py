import unittest
from ..user.login_user import app
from ..user.user import app

class TestLogin(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
    def tearDown(self):
        pass
    def test_login_user(self):
     response = self.app.get('drink-up/login')
     self.assertEquals(response.status_code,200)
     self.assertEquals(response.data,b'This is working')
    def test_create_user(self):
        response = self.app.post('drink-up/signup')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response)###
    def test_get_all_users(self):
        response = self.app.get('drink-up/users')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response)###
    def test_get_one_user(self):
        response = self.app.get('drink-up/user/<userId>')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response)###
    def test_update_user(self):
        response = self.app.post('drink-up/update-user/<userId>')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data,b'The user has been successfully updated')
    def test_delete_user(self):
        response = self.app.delete('drink-up/delete-user/<userId>')
        self.assertEqual(response.status_code,204)
        self.assertEqual(response.data,b'The user has been succesfully deleted')
    