"""
Unit tests for the Hello World application
"""
import pytest
import json
from helloworld.app import create_app

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

class TestHelloWorldApp:
    """Test cases for Hello World application"""
    
    def test_hello_world_page(self, client):
        """Test main hello world page"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Hello, World!' in response.data
        assert b'Welcome to our simple Flask web application!' in response.data
    
    def test_api_hello_endpoint(self, client):
        """Test API hello endpoint"""
        response = client.get('/api/hello')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['message'] == 'Hello, World!'
        assert data['status'] == 'success'
        assert 'timestamp' in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'helloworld-webapp'
    
    def test_404_page(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent')
        assert response.status_code == 404