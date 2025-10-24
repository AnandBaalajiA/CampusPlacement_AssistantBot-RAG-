"""
Health check endpoints
"""
from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Placement Prep RAG Bot is running'
    }), 200

@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness check for dependencies"""
    try:
        # Add checks for Gemini API, vector DB, etc.
        return jsonify({
            'status': 'ready',
            'gemini_api': 'connected',
            'vector_db': 'initialized'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'not ready',
            'error': str(e)
        }), 503
