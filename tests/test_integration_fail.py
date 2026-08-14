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


def test_that_always_fails(base_url):
    assert False

