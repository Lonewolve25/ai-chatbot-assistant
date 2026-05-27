import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
import openai
from config import Config

# Configure logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

class ChatbotAssistant:
    """Intelligent AI chatbot powered by OpenAI."""
    
    def __init__(self, system_prompt: Optional[str] = None):
        """Initialize the chatbot with OpenAI configuration."""
        Config.validate()
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.MODEL
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKENS
        self.system_prompt = system_prompt or Config.SYSTEM_PROMPT
        self.conversation_history: List[Dict[str, str]] = []
        self.session_id = None
        logger.info(f"Chatbot initialized with model: {self.model}")
    
    def _add_to_history(self, role: str, content: str) -> None:
        """Add a message to conversation history."""
        # Keep history within max limit
        if len(self.conversation_history) >= Config.MAX_HISTORY * 2:
            self.conversation_history = self.conversation_history[-Config.MAX_HISTORY:]
        
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def _prepare_messages(self, user_message: str) -> List[Dict[str, str]]:
        """Prepare messages for the API call."""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": user_message})
        return messages
    
    def chat(self, user_message: str) -> str:
        """Send a message to the chatbot and get a response.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The chatbot's response
        """
        try:
            if not user_message or not user_message.strip():
                return "Please provide a message."
            
            logger.info(f"User message: {user_message[:100]}...")
            
            # Prepare messages
            messages = self._prepare_messages(user_message)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            # Extract response
            assistant_message = response.choices[0].message.content
            
            # Add to history
            self._add_to_history("user", user_message)
            self._add_to_history("assistant", assistant_message)
            
            logger.info(f"Response generated successfully")
            return assistant_message
            
        except openai.error.AuthenticationError:
            error_msg = "Authentication failed. Check your OpenAI API key."
            logger.error(error_msg)
            return error_msg
        except openai.error.RateLimitError:
            error_msg = "Rate limit exceeded. Please try again later."
            logger.error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get current conversation history."""
        return self.conversation_history.copy()
    
    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt."""
        self.system_prompt = prompt
        logger.info("System prompt updated")
