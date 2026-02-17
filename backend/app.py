"""
Main Flask Application for Fruit Classification System
"""
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import Config
from backend.routes.api import api_bp


def create_app():
    """Create and configure the Flask application"""
    app = Flask(
        __name__,
        template_folder='../frontend',
        static_folder='../frontend/static'
    )
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Ensure upload folder exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Home route
    @app.route('/')
    def index():
        """Serve the main page"""
        return render_template('index.html')
    
    # PWA manifest
    @app.route('/manifest.json')
    def manifest():
        """Serve the PWA manifest"""
        return send_from_directory('../frontend', 'manifest.json', mimetype='application/manifest+json')
    
    # Health check endpoint for Render
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Fruit Classification System is running'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return {'error': 'File too large'}, 413
    
    return app


# Create app instance for Gunicorn
app = create_app()

if __name__ == '__main__':
    print("🍎 Fruit Classification System Starting...")
    print("📍 Server running at http://localhost:5000")
    print("📊 API endpoints available at http://localhost:5000/api")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
