from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                response = client.post('/store/store_test')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('store_test'))
                self.assertDictEqual({'name': 'store_test', 'items': []},
                                     json.loads(response.data))

    def create_duplicate_store(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                response = client.post('/store/store_test')
                response = client.post('/store/store_test')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A store with name store_test already exists'},
                                    json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                response = client.post('/store/store_test')
                response = client.delete('/store/store_test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                response = client.post('/store/store_test')
                response = client.get('/store/store_test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'store_test', 'items': []},
                                    json.loads(response.data))
                
    def test_store_found_with_items(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                response = client.post('/store/store_test')
                item = ItemModel('item_test', 20, 1).save_to_db() 

                response = client.get('/store/store_test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'store_test', 'items': [{'name': 'item_test', 'price': 20}]},
                                    json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                response = client.get('/store/store_test')

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'},
                                    json.loads(response.data))

    def test_store_list(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                response = client.post('/store/store_test')
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'store_test', 'items': []}]},
                                    json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client: # this pretend to be a client of our API
            with self.app_context(): # we can use the context to register info in DB
                response = client.post('/store/store_test')
                item = ItemModel('item_test', 20, 1).save_to_db() 
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'store_test', 'items': [{'name': 'item_test', 'price': 20}]}]},
                                    json.loads(response.data))
