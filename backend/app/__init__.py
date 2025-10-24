"""
Flask application factory
"""
from flask import Flask
from flask_cors import CORS
from app.config.settings import Config
from app.utils.logger import setup_logger
import os

def create_app(config_class=Config):
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Setup logging
    setup_logger(app)
    
    # Register blueprints
    from app.api.health_routes import health_bp
    from app.api.pdf_routes import pdf_bp
    from app.api.query_routes import query_bp
    
    app.register_blueprint(health_bp, url_prefix='/api/health')
    app.register_blueprint(pdf_bp, url_prefix='/api/pdf')
    app.register_blueprint(query_bp, url_prefix='/api/query')
    
    # Create necessary directories
    _create_directories(app)
    
    return app

def _create_directories(app):
    """Create required directories if they don't exist"""
    directories = [
        app.config['UPLOAD_FOLDER'],
        app.config['VECTOR_DB_PATH'],
        app.config['METADATA_PATH'],
        'data/processed',
        'data/temp',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
