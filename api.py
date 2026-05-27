#!/usr/bin/env python3
"""REST API interface for the AI Chatbot Assistant."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
from chatbot import ChatbotAssistant
from config import Config

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Initialize chatbot
try:
    bot = ChatbotAssistant()
except ValueError as e:
    logger.error(f"Failed to initialize chatbot: {e}")
    bot = None

# Store sessions
sessions = {}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'model': Config.MODEL
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint to send messages to the chatbot."""
    try:
        if bot is None:
            return jsonify({'error': 'Chatbot not initialized'}), 500
        
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Missing message field'}), 400
        
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get or create session
        if session_id not in sessions:
            sessions[session_id] = ChatbotAssistant()
        
        session_bot = sessions[session_id]
        
        # Get response
        response = session_bot.chat(user_message)
        
        return jsonify({
            'response': response,
            'session_id': session_id,
            'timestamp': datetime.utcnow().isoformat(),
            'model': Config.MODEL
        })
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/sessions/<session_id>/history', methods=['GET'])
def get_history(session_id):
    """Get conversation history for a session."""
    try:
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 404
        
        history = sessions[session_id].get_history()
        
        return jsonify({
            'session_id': session_id,
            'history': history,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/sessions/<session_id>/clear', methods=['POST'])
def clear_session(session_id):
    """Clear conversation history for a session."""
    try:
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 404
        
        sessions[session_id].clear_history()
        
        return jsonify({
            'message': 'History cleared',
            'session_id': session_id,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error clearing session: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info(f"Starting AI Chatbot API on port {Config.API_PORT}")
    app.run(
        host='0.0.0.0',
        port=Config.API_PORT,
        debug=Config.FLASK_DEBUG
    )
