from models.item import ItemModel
from models.user import UserModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):

    def setUp(self):
        # Create and store access token once for all tests in setUp method
        super(ItemTest, self).setUp()

        with self.app() as client:
            with self.app_context():
                UserModel('test', 1234).save_to_db()
                auth_request = client.post('/auth', data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})

                auth_token = json.loads(auth_request.data)['access_token']
                self.accessToken = f'JWT {auth_token}'


    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                # Authorization header is not included
                    # The jwt_required runs BEFORE the method
                    # If the auth header is not valir or present, it returns 404
                resp = client.get('item/test')

                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Code done by setUp, but I leave it here for example
                UserModel('test', 1234).save_to_db()
                auth_request = client.post('/auth', data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})

                auth_token = json.loads(auth_request.data)['access_token']
                header = {'Authorization': f'JWT {auth_token}'}

                resp = client.get('/item/test', headers=header)
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 20, 1).save_to_db()

                resp = client.get('/item/test', headers={'Authorization': self.accessToken})
                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 20, 1).save_to_db()

                resp = client.delete('/item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', data={'price': 20, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 20}, json.loads(resp.data))

    def test_create_item_duplicate(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 20, 1).save_to_db()
                resp = client.post('/item/test', data={'price': 20, 'store_id': 1})

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': 'An item with name \'test\' already exists.'}, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', data={'price': 20, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 20)
                self.assertDictEqual({'name': 'test', 'price': 20}, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 123, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 123)

                resp = client.put('/item/test', data={'price': 20, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 20)
                self.assertDictEqual({'name': 'test', 'price': 20}, json.loads(resp.data))

    def test_list_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 20, 1).save_to_db()

                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 20}]},
                                    json.loads(resp.data))