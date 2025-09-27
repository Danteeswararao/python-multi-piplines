"""
Integration tests for the Hello World application
"""
import pytest
import requests
import time
import subprocess
import signal
import os
from multiprocessing import Process
from helloworld.app import create_app

class TestIntegration:
    """Integration test cases"""
    
    @pytest.fixture(scope="class")
    def running_app(self):
        """Start the application for integration testing"""
        def run_app():
            app = create_app()
            app.run(host='127.0.0.1', port=5001, debug=False)
        
        # Start app in separate process
        process = Process(target=run_app)
        process.start()
        
        # Wait for app to start
        time.sleep(2)
        
        # Check if app is running
        try:
            response = requests.get('http://127.0.0.1:5001/health', timeout=5)
            if response.status_code != 200:
                process.terminate()
                pytest.skip("Could not start application for integration tests")
        except requests.exceptions.RequestException:
            process.terminate()
            pytest.skip("Could not connect to application for integration tests")
        
        yield 'http://127.0.0.1:5001'
        
        # Cleanup
        process.terminate()
        process.join()
    
    def test_full_application_flow(self, running_app):
        """Test complete application workflow"""
        base_url = running_app
        
        # Test health endpoint
        health_response = requests.get(f'{base_url}/health')
        assert health_response.status_code == 200
        health_data = health_response.json()
        assert health_data['status'] == 'healthy'
        
        # Test main page
        main_response = requests.get(base_url)
        assert main_response.status_code == 200
        assert 'Hello, World!' in main_response.text
        
        # Test API endpoint
        api_response = requests.get(f'{base_url}/api/hello')
        assert api_response.status_code == 200
        api_data = api_response.json()
        assert api_data['message'] == 'Hello, World!'
        assert api_data['status'] == 'success'
    
    def test_api_response_format(self, running_app):
        """Test API response format and content"""
        base_url = running_app
        
        response = requests.get(f'{base_url}/api/hello')
        assert response.status_code == 200
        assert response.headers['content-type'] == 'application/json'
        
        data = response.json()
        required_fields = ['message', 'timestamp', 'status']
        for field in required_fields:
            assert field in data
        
        assert isinstance(data['timestamp'], str)
        assert data['status'] == 'success'