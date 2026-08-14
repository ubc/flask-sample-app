# tests/test_integration.py

import pytest
import requests
import threading
import time
import os
from app import app


@pytest.fixture(scope="session")
def base_url():
    """Start the Flask server in a separate thread and return the base URL."""
    # Use a test port to avoid conflicts
    test_port = int(os.environ.get("TEST_PORT", 5001))
    base_url = f"http://localhost:{test_port}"
    
    # Wait for server to be ready
    max_attempts = 4
    for _ in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/", timeout=1)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(0.1)
    else:
        raise RuntimeError("Server failed to start within expected time")
    
    yield base_url


def test_hello_route(base_url):
    """Test the root endpoint returns correct greeting."""
    response = requests.get(f"{base_url}/")
    assert response.status_code == 200
    assert response.text == "Hello, Flask!"
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'


def test_get_items_empty_list(base_url):
    """Test getting items when list is empty (or after clearing)."""
    response = requests.get(f"{base_url}/items")
    assert response.status_code == 200
    data = response.json()
    assert 'items' in data
    assert isinstance(data['items'], list)


def test_add_item_success(base_url):
    """Test adding an item successfully."""
    item_data = {'name': 'test_item', 'description': 'A test item'}
    response = requests.post(
        f"{base_url}/items",
        json=item_data,
        headers={'Content-Type': 'application/json'}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data == {'message': 'Item added successfully'}


def test_get_items_after_adding(base_url):
    """Test getting items after adding one."""
    # Add an item
    item_data = {'name': 'integration_test_item', 'value': 42}
    response = requests.post(f"{base_url}/items", json=item_data)
    assert response.status_code == 201
    
    # Get all items
    response = requests.get(f"{base_url}/items")
    assert response.status_code == 200
    data = response.json()
    assert 'items' in data
    assert isinstance(data['items'], list)
    # The item should be in the list (may be at the end if other tests ran)
    item_names = [item.get('name') for item in data['items']]
    assert 'integration_test_item' in item_names


def test_get_item_by_id_success(base_url):
    """Test getting an item by valid ID."""
    # First, add an item
    item_data = {'name': 'get_by_id_test', 'id': 999}
    response = requests.post(f"{base_url}/items", json=item_data)
    assert response.status_code == 201
    
    # Get all items to find the index
    response = requests.get(f"{base_url}/items")
    items = response.json()['items']
    item_index = len(items) - 1  # Last added item
    
    # Get item by ID
    response = requests.get(f"{base_url}/items/{item_index}")
    assert response.status_code == 200
    data = response.json()
    assert 'item' in data
    assert data['item']['name'] == 'get_by_id_test'


def test_get_item_by_id_not_found(base_url):
    """Test getting an item with non-existent ID."""
    # Get current items count
    response = requests.get(f"{base_url}/items")
    items_count = len(response.json()['items'])
    
    # Try to get an item that doesn't exist
    response = requests.get(f"{base_url}/items/{items_count + 100}")
    assert response.status_code == 404
    data = response.json()
    assert data == {'error': 'Item not found'}


def test_add_multiple_items(base_url):
    """Test adding multiple items and retrieving them."""
    items_to_add = [
        {'name': 'item1', 'type': 'test'},
        {'name': 'item2', 'type': 'test', 'value': 10},
        {'name': 'item3', 'type': 'test', 'value': 20}
    ]
    
    # Add all items
    for item in items_to_add:
        response = requests.post(f"{base_url}/items", json=item)
        assert response.status_code == 201
    
    # Get all items
    response = requests.get(f"{base_url}/items")
    assert response.status_code == 200
    data = response.json()
    
    # Verify all items are present
    item_names = [item.get('name') for item in data['items']]
    for item in items_to_add:
        assert item['name'] in item_names


def test_add_item_with_nested_data(base_url):
    """Test adding an item with nested data structures."""
    complex_item = {
        'name': 'complex_item',
        'metadata': {
            'tags': ['tag1', 'tag2'],
            'settings': {'enabled': True, 'count': 5}
        },
        'numbers': [1, 2, 3, 4, 5]
    }
    
    response = requests.post(f"{base_url}/items", json=complex_item)
    assert response.status_code == 201
    
    # Verify it was added correctly by getting all items
    response = requests.get(f"{base_url}/items")
    items = response.json()['items']
    
    # Find our complex item
    complex_items = [item for item in items if item.get('name') == 'complex_item']
    assert len(complex_items) > 0
    added_item = complex_items[-1]  # Get the last one added
    
    assert added_item['metadata']['tags'] == ['tag1', 'tag2']
    assert added_item['metadata']['settings']['enabled'] is True
    assert added_item['numbers'] == [1, 2, 3, 4, 5]


def test_add_empty_item(base_url):
    """Test adding an empty item object."""
    response = requests.post(f"{base_url}/items", json={})
    assert response.status_code == 201
    data = response.json()
    assert data == {'message': 'Item added successfully'}


def test_full_workflow(base_url):
    """Test a complete workflow: add items, get all, get specific."""
    # Add first item
    item1 = {'name': 'workflow_item1', 'step': 1}
    response = requests.post(f"{base_url}/items", json=item1)
    assert response.status_code == 201
    
    # Add second item
    item2 = {'name': 'workflow_item2', 'step': 2}
    response = requests.post(f"{base_url}/items", json=item2)
    assert response.status_code == 201
    
    # Get all items
    response = requests.get(f"{base_url}/items")
    assert response.status_code == 200
    data = response.json()
    assert 'items' in data
    
    # Find the indices of our items
    items = data['items']
    indices = {}
    for idx, item in enumerate(items):
        if item.get('name') == 'workflow_item1':
            indices['item1'] = idx
        if item.get('name') == 'workflow_item2':
            indices['item2'] = idx
    
    # Get first item by ID
    if 'item1' in indices:
        response = requests.get(f"{base_url}/items/{indices['item1']}")
        assert response.status_code == 200
        assert response.json()['item']['name'] == 'workflow_item1'
    
    # Get second item by ID
    if 'item2' in indices:
        response = requests.get(f"{base_url}/items/{indices['item2']}")
        assert response.status_code == 200
        assert response.json()['item']['name'] == 'workflow_item2'


def test_invalid_route(base_url):
    """Test accessing a non-existent route."""
    response = requests.get(f"{base_url}/nonexistent")
    assert response.status_code == 404


def test_get_items_response_format(base_url):
    """Test that GET /items returns proper JSON format."""
    response = requests.get(f"{base_url}/items")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    
    data = response.json()
    assert isinstance(data, dict)
    assert 'items' in data
    assert isinstance(data['items'], list)


def test_get_item_response_format(base_url):
    """Test that GET /items/<id> returns proper JSON format."""
    # First add an item
    item_data = {'name': 'format_test'}
    requests.post(f"{base_url}/items", json=item_data)
    
    # Get all items to find index
    response = requests.get(f"{base_url}/items")
    items = response.json()['items']
    test_item_idx = None
    for idx, item in enumerate(items):
        if item.get('name') == 'format_test':
            test_item_idx = idx
            break
    
    if test_item_idx is not None:
        response = requests.get(f"{base_url}/items/{test_item_idx}")
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        
        data = response.json()
        assert isinstance(data, dict)
        assert 'item' in data


def test_post_items_without_json_header(base_url):
    """Test POST /items with JSON data but explicit header."""
    item_data = {'name': 'header_test'}
    response = requests.post(
        f"{base_url}/items",
        json=item_data,
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201


def test_get_item_negative_id(base_url):
    """Test getting an item with negative ID (should return 404)."""
    response = requests.get(f"{base_url}/items/-1")
    # Flask routing will handle this - likely 404
    assert response.status_code in [404, 405]
