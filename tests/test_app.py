# tests/test_app.py

import unittest
from app import app
from app.routes import items

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        items.clear()

    def test_hello_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, Flask!")

    def test_add_item_route(self):
        response = self.app.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'message': 'Item added successfully'})

    def test_get_item_route(self):
        self.app.post('/items', json={"name": "item1"})

        response = self.app.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'name': 'item1'}})

    def test_filter_items_by_name(self):
        self.app.post('/items', json={"name": "filterable item"})

        response = self.app.get('/items?search=filterable')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'items': [{'name': 'filterable item'}]})

    def test_filter_items_with_no_matches(self):
        response = self.app.get('/items?search=not-present')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'items': []})

    def test_get_nonexistent_item_route(self):
        response = self.app.get('/items/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

if __name__ == '__main__':
    unittest.main()
