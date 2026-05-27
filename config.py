import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the chatbot."""
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MODEL = os.getenv('MODEL', 'gpt-4')
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '2048'))
    
    # API Settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    API_PORT = int(os.getenv('API_PORT', '5000'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # System Prompt - Define the chatbot's behavior
    SYSTEM_PROMPT = """You are an intelligent AI assistant designed to help users with a wide range of tasks. 
You are:
- Knowledgeable and accurate
- Helpful and friendly
- Clear in your explanations
- Respectful and professional

Provide detailed, well-structured responses. When appropriate, break down complex topics into digestible parts."""
    
    # Conversation Settings
    MAX_HISTORY = 20  # Maximum messages to keep in history
    CONVERSATION_TIMEOUT = 3600  # 1 hour in seconds
    
    @classmethod
    def validate(cls):
        """Validate that all required settings are configured."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY not set. Please add it to your .env file."
            )
        if not cls.OPENAI_API_KEY.startswith('sk-'):
            raise ValueError(
                "Invalid OPENAI_API_KEY format. It should start with 'sk-'"
            )
