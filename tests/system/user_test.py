from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                # data is not json but request.data type
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})
                                            # Content-Type header says which kind of data we are sending

                self.assertIn('access_token', json.loads(auth_response.data).keys() )

    def test_register_duplicate_user(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                # We should get an error, get code 400

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'},
                                        json.loads(response.data))
