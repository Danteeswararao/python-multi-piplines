"""
Hello World Flask Web Application
"""
import logging
from flask import Flask, render_template, jsonify
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        """Main hello world page"""
        logger.info("Hello World page accessed")
        return render_template('index.html', 
                             message="Hello, World!", 
                             timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    @app.route('/api/hello')
    def api_hello():
        """API endpoint for hello world"""
        logger.info("API hello endpoint accessed")
        return jsonify({
            "message": "Hello, World!",
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        })
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({"status": "healthy", "service": "helloworld-webapp"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)