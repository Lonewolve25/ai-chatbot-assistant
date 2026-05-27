#!/usr/bin/env python3
"""CLI interface for the AI Chatbot Assistant."""

import sys
from colorama import Fore, Style
from chatbot import ChatbotAssistant
from config import Config

def print_welcome():
    """Print welcome message."""
    print(f"{Fore.CYAN}")
    print("="*60)
    print("  🤖 AI Chatbot Assistant")
    print("="*60)
    print(f"{Style.RESET_ALL}")
    print("Commands:")
    print("  /quit  - Exit the chatbot")
    print("  /clear - Clear conversation history")
    print("  /help  - Show this help message")
    print()

def print_prompt():
    """Print user prompt."""
    print(f"{Fore.GREEN}You: {Style.RESET_ALL}", end="")

def handle_command(command: str, bot: ChatbotAssistant) -> bool:
    """Handle special commands.
    
    Returns:
        False if should exit, True to continue
    """
    if command == "/quit":
        print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
        return False
    elif command == "/clear":
        bot.clear_history()
        print(f"{Fore.YELLOW}Conversation history cleared.{Style.RESET_ALL}")
    elif command == "/help":
        print_welcome()
    else:
        print(f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}")
    return True

def main():
    """Main CLI loop."""
    try:
        # Initialize chatbot
        bot = ChatbotAssistant()
        
        print_welcome()
        
        while True:
            try:
                print_prompt()
                user_input = input().strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith("/"):
                    if not handle_command(user_input, bot):
                        break
                    continue
                
                # Get response from chatbot
                print(f"{Fore.BLUE}Bot: {Style.RESET_ALL}", end="")
                response = bot.chat(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    
    except ValueError as e:
        print(f"{Fore.RED}Configuration Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
