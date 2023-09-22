import unittest
from ..drink.drink import app

class drinkTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
    def tearDown(self):
        pass
    def test_get_all_drinks(self):
        response = self.app.get('drink-up/drinks') 
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data,b'')###
    def test_get_one_drink(self):
        response = self.app.get('drink-up/drink/<drinkId>')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data,b'The drink was successfully found')
    def test_update_drink(self):
        response = self.app.post('drink-up/update/<drinkId>')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data,b'The drink has been successfully modified')
    def test_create_drink(self):
        response = self.app.post('drink-up/create-drink')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data,b'The drink has been successfully created')
    def test_delete_user(self):
        response = self.app.delete('drink-up/delete-drink/<deleteId>')
        self.assertEqual(response.status_code,204)
        self.assertEqual(response.data,b'The drink has been successfully deleted')
        