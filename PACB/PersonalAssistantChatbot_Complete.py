"""
PERSONAL ASSISTANT CHATBOT
Complete Implementation with Multiple Features

This chatbot handles:
- Intent recognition
- Entity extraction
- Natural language understanding
- Response generation
- Context management
- Conversation history
"""

import re
from datetime import datetime, timedelta
from collections import defaultdict
import json
import pickle

# ============================================================================
# PART 1: DATA AND DEFINITIONS
# ============================================================================

class IntentPatterns:
    """Define patterns and intents for the chatbot"""
    
    def __init__(self):
        self.intents = {
            'greeting': {
                'patterns': [
                    r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b',
                    r'\bhow are you\b',
                    r'\bwhat\'s up\b',
                ],
                'responses': [
                    "Hello! How can I help you today?",
                    "Hi there! What can I do for you?",
                    "Hey! Good to see you. What do you need?",
                    "Greetings! I'm here to assist you.",
                ]
            },
            
            'goodbye': {
                'patterns': [
                    r'\b(bye|goodbye|see you|farewell|take care|gotta go|quit|exit)\b',
                    r'\bsee you later\b',
                    r'\buntil next time\b',
                ],
                'responses': [
                    "Goodbye! Have a great day!",
                    "See you later!",
                    "Thanks for chatting. Take care!",
                    "Bye! Come back soon!",
                ]
            },
            
            'weather': {
                'patterns': [
                    r'\b(weather|temperature|forecast|rain|sunny|cloudy)\b',
                    r'\bhow\'s the weather\b',
                    r'\bwill it rain\b',
                    r'\bis it cold\b',
                ],
                'responses': [
                    "I don't have real-time weather data, but you can check weather.com or your local weather service.",
                    "For weather information, I recommend checking a weather service.",
                    "Weather forecasts change frequently. Check your local weather app for current conditions.",
                ]
            },
            
            'time': {
                'patterns': [
                    r'\b(what time|current time|what\'s the time|tell me the time)\b',
                    r'\bwhat hour is it\b',
                    r'\bis it morning|afternoon|evening\b',
                ],
                'responses': [
                    "The current time is {time}.",
                    "It's {time} right now.",
                    "The time is {time}.",
                ]
            },
            
            'date': {
                'patterns': [
                    r'\b(what date|today\'s date|current date|what\'s today)\b',
                    r'\bwhat day is it\b',
                    r'\btell me the date\b',
                ],
                'responses': [
                    "Today's date is {date}.",
                    "It's {date}.",
                    "The current date is {date}.",
                ]
            },
            
            'name': {
                'patterns': [
                    r'\bwhat\'?s? (?:your|ur) name\b',
                    r'\bwho are you\b',
                    r'\btell me your name\b',
                    r'\bwhat do they call you\b',
                ],
                'responses': [
                    "I'm your Personal Assistant Chatbot!",
                    "You can call me your Personal Assistant.",
                    "I'm an AI Personal Assistant, here to help you.",
                    "My name is Personal Assistant. Nice to meet you!",
                ]
            },
            
            'help': {
                'patterns': [
                    r'\b(help|assist|support|what can you do|capabilities)\b',
                    r'\bwhat can i ask you\b',
                    r'\bhow can you help\b',
                    r'\bwhat are your functions\b',
                ],
                'responses': [
                    "I can help you with: greetings, time/date, weather info, reminders, calculations, definitions, and general conversation. Ask me anything!",
                    "I'm here to help with scheduling, answering questions, telling the time, and having conversations!",
                    "I can assist with reminders, provide definitions, answer questions, tell time and date, and more!",
                ]
            },
            
            'reminder': {
                'patterns': [
                    r'\b(remind|set reminder|don\'t forget|remember to)\b',
                    r'\bset an? (?:alarm|reminder)\b',
                    r'\btell me to\b',
                ],
                'responses': [
                    "I'll help you set a reminder. What should I remind you about and when?",
                    "Sure! What do you want me to remind you about?",
                    "I can set that reminder for you. Just tell me what and when.",
                ]
            },
            
            'calculation': {
                'patterns': [
                    r'\b(?:what is|calculate|compute)\b',
                    r'\b(?:\d+\s*[\+\-\*/]\s*\d+)\b',
                    r'\bhow much is\b',
                    r'\bwhat\'s .*? times .*?\b',
                ],
                'responses': [
                    "Let me help you calculate that.",
                    "I can do that math for you.",
                    "Let me compute that.",
                ]
            },
            
            'definition': {
                'patterns': [
                    r'\b(define|what is|what does|meaning of)\b',
                    r'\bwhat\'?s the definition\b',
                    r'\bexplain\b',
                ],
                'responses': [
                    "Let me explain that for you.",
                    "Here's what that means:",
                    "I can help explain that.",
                ]
            },
            
            'thanks': {
                'patterns': [
                    r'\b(thanks|thank you|appreciate|grateful)\b',
                    r'\bthanks\b',
                    r'\byou\'?re helpful\b',
                ],
                'responses': [
                    "You're welcome! Happy to help.",
                    "My pleasure! Let me know if you need anything else.",
                    "Glad I could help!",
                    "Anytime! What else can I do for you?",
                ]
            },
            
            'affirmative': {
                'patterns': [
                    r'\b(yes|yeah|yep|yup|sure|okay|ok|affirmative)\b',
                    r'\bi agree\b',
                    r'\bthat\'s right\b',
                ],
                'responses': [
                    "Great! What would you like to do?",
                    "Awesome! Let's proceed.",
                    "Perfect! How can I help?",
                ]
            },
            
            'negative': {
                'patterns': [
                    r'\b(no|nope|nah|negative|don\'t|not really)\b',
                    r'\bi disagree\b',
                    r'\bthat\'s wrong\b',
                ],
                'responses': [
                    "No problem. How can I help you then?",
                    "Understood. What do you need?",
                    "Okay, let me know what you'd prefer.",
                ]
            },
            
            'general': {
                'patterns': [
                    r'.*',  # Catch-all pattern
                ],
                'responses': [
                    "That's interesting! Tell me more.",
                    "I understand. How can I assist with that?",
                    "Can you provide more details?",
                    "I'm here to help. What specifically do you need?",
                ]
            }
        }
    
    def get_intents(self):
        return self.intents


# ============================================================================
# PART 2: ENTITY EXTRACTION
# ============================================================================

class EntityExtractor:
    """Extract entities (numbers, dates, names, etc.) from user input"""
    
    def __init__(self):
        self.number_pattern = r'(?:the\s+)?(\d+(?:\.\d+)?)'
        self.time_pattern = r'(\d{1,2}):(\d{2})\s*(am|pm)?'
        self.date_pattern = r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})'
        
    def extract_numbers(self, text):
        """Extract numerical values from text"""
        numbers = re.findall(self.number_pattern, text)
        return [float(n) for n in numbers]
    
    def extract_time(self, text):
        """Extract time expressions from text"""
        matches = re.findall(self.time_pattern, text, re.IGNORECASE)
        return matches
    
    def extract_names(self, text):
        """Extract potential names (capitalized words)"""
        words = text.split()
        names = [word for word in words if word[0].isupper() and len(word) > 1]
        return names
    
    def extract_dates(self, text):
        """Extract date patterns from text"""
        matches = re.findall(self.date_pattern, text)
        return matches
    
    def extract_all(self, text):
        """Extract all entity types"""
        return {
            'numbers': self.extract_numbers(text),
            'times': self.extract_time(text),
            'names': self.extract_names(text),
            'dates': self.extract_dates(text)
        }


# ============================================================================
# PART 3: INTENT RECOGNITION
# ============================================================================

class IntentRecognizer:
    """Recognize user intent from input text"""
    
    def __init__(self, intent_patterns):
        self.intent_patterns = intent_patterns.get_intents()
        self.entity_extractor = EntityExtractor()
    
    def recognize_intent(self, user_input):
        """Identify the primary intent from user input"""
        text = user_input.lower().strip()
        
        # Check each intent's patterns
        for intent, data in self.intent_patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, text, re.IGNORECASE):
                    return {
                        'intent': intent,
                        'confidence': self._calculate_confidence(text, pattern),
                        'entities': self.entity_extractor.extract_all(user_input)
                    }
        
        # Default to general if no match
        return {
            'intent': 'general',
            'confidence': 0.5,
            'entities': self.entity_extractor.extract_all(user_input)
        }
    
    def _calculate_confidence(self, text, pattern):
        """Calculate confidence score for intent match"""
        matches = re.findall(pattern, text, re.IGNORECASE)
        confidence = min(0.95, len(matches) * 0.3 + 0.5)
        return confidence


# ============================================================================
# PART 4: RESPONSE GENERATION
# ============================================================================

class ResponseGenerator:
    """Generate responses based on intent and context"""
    
    def __init__(self, intent_patterns):
        self.intent_patterns = intent_patterns.get_intents()
        self.entity_extractor = EntityExtractor()
    
    def generate_response(self, intent_result, conversation_context=None):
        """Generate response based on recognized intent"""
        intent = intent_result['intent']
        entities = intent_result['entities']
        
        # Get responses for the intent
        responses = self.intent_patterns[intent]['responses']
        response = responses[len(responses) % 2] if responses else ""
        
        # Format response with entities/context
        response = self._format_response(response, entities, conversation_context)
        
        return response
    
    def _format_response(self, response, entities, context):
        """Format response with dynamic content"""
        # Handle time placeholders
        if '{time}' in response:
            current_time = datetime.now().strftime("%I:%M %p")
            response = response.format(time=current_time)
        
        # Handle date placeholders
        if '{date}' in response:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            response = response.format(date=current_date)
        
        return response
    
    def handle_calculation(self, text):
        """Handle mathematical calculations"""
        try:
            # Extract numbers and operators
            numbers = re.findall(r'(\d+(?:\.\d+)?)', text)
            
            # Find operators
            if '+' in text:
                result = sum(float(n) for n in numbers)
                return f"The sum is {result}"
            elif '-' in text:
                result = float(numbers[0]) - sum(float(n) for n in numbers[1:])
                return f"The result is {result}"
            elif '*' in text or 'times' in text.lower():
                result = float(numbers[0])
                for n in numbers[1:]:
                    result *= float(n)
                return f"The result is {result}"
            elif '/' in text or 'divided' in text.lower():
                result = float(numbers[0])
                for n in numbers[1:]:
                    if float(n) != 0:
                        result /= float(n)
                return f"The result is {result}"
        except:
            pass
        
        return "I couldn't calculate that. Can you rephrase?"
    
    def handle_definition(self, text, definitions_dict=None):
        """Handle word definitions"""
        if definitions_dict is None:
            definitions_dict = self._get_default_definitions()
        
        # Extract potential word to define
        words = text.lower().split()
        
        for word in words:
            if word in definitions_dict:
                return f"'{word.capitalize()}' means: {definitions_dict[word]}"
        
        return "I don't have a definition for that word. Try a different term?"
    
    def _get_default_definitions(self):
        """Provide default definitions"""
        return {
            'chatbot': 'A computer program designed to simulate conversation.',
            'ai': 'Artificial Intelligence - the simulation of human intelligence by machines.',
            'nlp': 'Natural Language Processing - the field of AI that deals with text/speech.',
            'algorithm': 'A step-by-step procedure for solving a problem.',
            'database': 'An organized collection of structured data.',
            'python': 'A popular programming language known for simplicity.',
            'machine learning': 'A field of AI where systems learn from data.',
            'neural network': 'A computing system inspired by biological neurons.',
        }


# ============================================================================
# PART 5: CONVERSATION CONTEXT MANAGEMENT
# ============================================================================

class ConversationContext:
    """Manage conversation history and context"""
    
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history
        self.user_name = None
        self.preferences = {}
        self.reminders = []
    
    def add_exchange(self, user_input, bot_response):
        """Add user input and bot response to history"""
        exchange = {
            'timestamp': datetime.now(),
            'user': user_input,
            'bot': bot_response
        }
        self.history.append(exchange)
        
        # Keep history size manageable
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_history(self):
        """Get conversation history"""
        return self.history
    
    def get_last_exchange(self):
        """Get the last exchange"""
        return self.history[-1] if self.history else None
    
    def set_user_name(self, name):
        """Set the user's name"""
        self.user_name = name
    
    def get_user_name(self):
        """Get the user's name"""
        return self.user_name
    
    def add_reminder(self, reminder_text, reminder_time=None):
        """Add a reminder"""
        reminder = {
            'text': reminder_text,
            'time': reminder_time or datetime.now() + timedelta(hours=1),
            'created': datetime.now()
        }
        self.reminders.append(reminder)
        return f"Reminder set: {reminder_text}"
    
    def get_pending_reminders(self):
        """Get reminders that should be shown"""
        current_time = datetime.now()
        pending = [r for r in self.reminders if r['time'] <= current_time]
        return pending
    
    def clear_reminder(self, index):
        """Clear a specific reminder"""
        if 0 <= index < len(self.reminders):
            self.reminders.pop(index)


# ============================================================================
# PART 6: MAIN CHATBOT CLASS
# ============================================================================

class PersonalAssistantChatbot:
    """Complete Personal Assistant Chatbot"""
    
    def __init__(self, name="Personal Assistant"):
        self.name = name
        self.intent_patterns = IntentPatterns()
        self.intent_recognizer = IntentRecognizer(self.intent_patterns)
        self.response_generator = ResponseGenerator(self.intent_patterns)
        self.context = ConversationContext()
        self.entity_extractor = EntityExtractor()
        self.is_running = False
    
    def preprocess_input(self, user_input):
        """Clean and preprocess user input"""
        # Remove extra whitespace
        text = ' '.join(user_input.split())
        # Convert to lowercase for processing
        return text
    
    def process_input(self, user_input):
        """Process user input and generate response"""
        # Preprocess
        processed_input = self.preprocess_input(user_input)
        
        # Check for exit commands
        if processed_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
            return "Goodbye! Have a great day!", True
        
        # Recognize intent
        intent_result = self.intent_recognizer.recognize_intent(processed_input)
        intent = intent_result['intent']
        
        # Generate response based on intent
        if intent == 'calculation':
            response = self.response_generator.handle_calculation(processed_input)
        elif intent == 'definition':
            response = self.response_generator.handle_definition(processed_input)
        elif intent == 'reminder':
            response = "I've noted your reminder. What should I remind you about?"
        else:
            response = self.response_generator.generate_response(intent_result, self.context)
        
        # Add to conversation history
        self.context.add_exchange(user_input, response)
        
        return response, False
    
    def start_conversation(self):
        """Start interactive conversation"""
        self.is_running = True
        print(f"\n{'='*70}")
        print(f"{self.name} Started!")
        print(f"{'='*70}")
        print("Type 'help' for available commands, 'quit' or 'exit' to end.\n")
        
        # Initial greeting
        greeting = self.response_generator.generate_response(
            self.intent_recognizer.recognize_intent("hello")
        )
        print(f"{self.name}: {greeting}\n")
        
        while self.is_running:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Process and respond
                response, should_exit = self.process_input(user_input)
                print(f"\n{self.name}: {response}\n")
                
                if should_exit:
                    self.is_running = False
                
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Goodbye! See you later!\n")
                self.is_running = False
            except Exception as e:
                print(f"\n{self.name}: Sorry, I encountered an error. {str(e)}\n")
    
    def get_conversation_history(self):
        """Get the full conversation history"""
        return self.context.get_history()
    
    def print_conversation_summary(self):
        """Print a summary of the conversation"""
        history = self.get_conversation_history()
        
        print(f"\n{'='*70}")
        print("CONVERSATION SUMMARY")
        print(f"{'='*70}\n")
        
        for i, exchange in enumerate(history, 1):
            print(f"Exchange {i}:")
            print(f"  You: {exchange['user']}")
            print(f"  {self.name}: {exchange['bot']}")
            print()
    
    def test_mode(self, test_inputs):
        """Test the chatbot with predefined inputs"""
        print(f"\n{'='*70}")
        print(f"{self.name} - TEST MODE")
        print(f"{'='*70}\n")
        
        for test_input in test_inputs:
            print(f"You: {test_input}")
            response, _ = self.process_input(test_input)
            print(f"{self.name}: {response}\n")
        
        self.print_conversation_summary()


# ============================================================================
# PART 7: EXAMPLE USAGE AND TESTING
# ============================================================================

def main():
    """Main function to run the chatbot"""
    
    # Create chatbot instance
    chatbot = PersonalAssistantChatbot(name="Assistant")
    
    # Example 1: Test mode with predefined inputs
    print("\n" + "="*70)
    print("DEMONSTRATION: Testing Personal Assistant Chatbot")
    print("="*70)
    
    test_inputs = [
        "Hello!",
        "What time is it?",
        "What's today's date?",
        "What can you do?",
        "Calculate 25 + 15",
        "What is a chatbot?",
        "Thank you!",
        "Goodbye",
    ]
    
    chatbot.test_mode(test_inputs)
    
    # Example 2: Interactive mode (uncomment to use)
    # print("\n" + "="*70)
    # print("Starting Interactive Conversation")
    # print("="*70)
    # chatbot.start_conversation()


def advanced_example():
    """Advanced example with more features"""
    
    print("\n" + "="*70)
    print("ADVANCED EXAMPLE: Testing More Features")
    print("="*70 + "\n")
    
    chatbot = PersonalAssistantChatbot(name="Assistant")
    
    # Test various input categories
    examples = {
        'Greetings': ['Hi there!', 'Hello!', 'Good morning!'],
        'Time & Date': ['What time is it?', "What's today's date?"],
        'Help': ['Can you help me?', 'What can you do?'],
        'Math': ['What is 100 times 5?', 'Calculate 50 - 25'],
        'Definitions': ['Define AI', 'What is machine learning?'],
        'Expressions': ['Thanks!', 'That\'s great!', 'No thanks'],
    }
    
    for category, inputs in examples.items():
        print(f"\n{category.upper()}")
        print("-" * 50)
        
        for user_input in inputs:
            print(f"Input: {user_input}")
            response, _ = chatbot.process_input(user_input)
            print(f"Response: {response}\n")


if __name__ == "__main__":
    # Run basic demonstration
    main()
    
    # Run advanced example
    # Uncomment the line below to see more examples
    # advanced_example()
