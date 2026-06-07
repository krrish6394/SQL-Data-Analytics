"""
PERSONAL ASSISTANT CHATBOT - PRACTICAL EXAMPLES
Complete Working Examples and Use Cases
"""

# ============================================================================
# EXAMPLE 1: BASIC USAGE
# ============================================================================

def example_1_basic_usage():
    """Basic chatbot usage example"""
    from PersonalAssistantChatbot_Complete import PersonalAssistantChatbot
    
    print("\n" + "="*70)
    print("EXAMPLE 1: BASIC USAGE")
    print("="*70 + "\n")
    
    # Create chatbot
    chatbot = PersonalAssistantChatbot(name="Assistant")
    
    # Simple test inputs
    test_inputs = [
        "Hello!",
        "What time is it?",
        "What's today's date?",
        "Thank you!",
    ]
    
    # Process each input
    for user_input in test_inputs:
        response, should_exit = chatbot.process_input(user_input)
        print(f"You: {user_input}")
        print(f"Assistant: {response}\n")


# ============================================================================
# EXAMPLE 2: INTENT RECOGNITION
# ============================================================================

def example_2_intent_recognition():
    """Demonstrate intent recognition"""
    from PersonalAssistantChatbot_Complete import (
        IntentRecognizer, 
        IntentPatterns
    )
    
    print("\n" + "="*70)
    print("EXAMPLE 2: INTENT RECOGNITION")
    print("="*70 + "\n")
    
    recognizer = IntentRecognizer(IntentPatterns())
    
    # Test various inputs
    test_inputs = [
        "Hello there!",
        "What's 25 + 15?",
        "Define machine learning",
        "Can you help me?",
        "Set a reminder",
        "Goodbye!",
        "What's the weather like?",
        "Thanks for your help!",
    ]
    
    print(f"{'Input':<30} {'Intent':<15} {'Confidence':<12}")
    print("-" * 60)
    
    for user_input in test_inputs:
        result = recognizer.recognize_intent(user_input)
        intent = result['intent']
        confidence = result['confidence']
        
        print(f"{user_input:<30} {intent:<15} {confidence:>10.2f}")
    
    print()


# ============================================================================
# EXAMPLE 3: ENTITY EXTRACTION
# ============================================================================

def example_3_entity_extraction():
    """Demonstrate entity extraction"""
    from PersonalAssistantChatbot_Complete import EntityExtractor
    
    print("\n" + "="*70)
    print("EXAMPLE 3: ENTITY EXTRACTION")
    print("="*70 + "\n")
    
    extractor = EntityExtractor()
    
    # Test sentences with different entities
    test_sentences = [
        "I have 5 apples and 3 oranges",
        "Call me John at 3:45 pm",
        "The meeting is on 12/25/2024",
        "My name is Sarah and I have 100 dollars",
        "See you at 2:30 pm on 01/15/2025",
    ]
    
    for sentence in test_sentences:
        entities = extractor.extract_all(sentence)
        
        print(f"Text: {sentence}")
        print(f"  Numbers: {entities['numbers']}")
        print(f"  Times: {entities['times']}")
        print(f"  Dates: {entities['dates']}")
        print(f"  Names: {entities['names']}")
        print()


# ============================================================================
# EXAMPLE 4: CALCULATIONS
# ============================================================================

def example_4_calculations():
    """Demonstrate calculation handling"""
    from PersonalAssistantChatbot_Complete import (
        ResponseGenerator,
        IntentPatterns
    )
    
    print("\n" + "="*70)
    print("EXAMPLE 4: CALCULATIONS")
    print("="*70 + "\n")
    
    generator = ResponseGenerator(IntentPatterns())
    
    # Test mathematical expressions
    calculations = [
        "What is 25 + 15?",
        "Calculate 100 * 2",
        "What's 50 / 2?",
        "50 - 30",
        "15 times 4",
        "100 divided by 5",
    ]
    
    print(f"{'Expression':<30} {'Result':<20}")
    print("-" * 50)
    
    for calc in calculations:
        result = generator.handle_calculation(calc)
        print(f"{calc:<30} {result:<20}")
    
    print()


# ============================================================================
# EXAMPLE 5: DEFINITIONS
# ============================================================================

def example_5_definitions():
    """Demonstrate definition handling"""
    from PersonalAssistantChatbot_Complete import (
        ResponseGenerator,
        IntentPatterns
    )
    
    print("\n" + "="*70)
    print("EXAMPLE 5: DEFINITIONS")
    print("="*70 + "\n")
    
    generator = ResponseGenerator(IntentPatterns())
    
    # Test definition queries
    queries = [
        "What is a chatbot?",
        "Define AI",
        "What does NLP mean?",
        "Explain machine learning",
        "What is Python?",
        "Define neural network",
    ]
    
    for query in queries:
        result = generator.handle_definition(query)
        print(f"Q: {query}")
        print(f"A: {result}\n")


# ============================================================================
# EXAMPLE 6: CONVERSATION CONTEXT
# ============================================================================

def example_6_conversation_context():
    """Demonstrate conversation context management"""
    from PersonalAssistantChatbot_Complete import ConversationContext
    from datetime import datetime, timedelta
    
    print("\n" + "="*70)
    print("EXAMPLE 6: CONVERSATION CONTEXT")
    print("="*70 + "\n")
    
    context = ConversationContext(max_history=5)
    
    # Add some exchanges
    exchanges = [
        ("Hello", "Hi! How can I help?"),
        ("What time is it?", "It's 3:45 PM"),
        ("Thank you", "You're welcome!"),
    ]
    
    for user_msg, bot_msg in exchanges:
        context.add_exchange(user_msg, bot_msg)
    
    # Display history
    print("Conversation History:")
    print("-" * 60)
    
    history = context.get_history()
    for i, exchange in enumerate(history, 1):
        print(f"Exchange {i}:")
        print(f"  Time: {exchange['timestamp'].strftime('%I:%M %p')}")
        print(f"  User: {exchange['user']}")
        print(f"  Bot: {exchange['bot']}")
        print()
    
    # Test user name
    print("User Information:")
    print("-" * 60)
    context.set_user_name("Alice")
    print(f"User Name: {context.get_user_name()}\n")
    
    # Test reminders
    print("Reminders:")
    print("-" * 60)
    context.add_reminder("Call mom", datetime.now() + timedelta(hours=2))
    context.add_reminder("Buy groceries", datetime.now() + timedelta(days=1))
    
    for i, reminder in enumerate(context.reminders, 1):
        print(f"Reminder {i}: {reminder['text']}")
        print(f"  Scheduled: {reminder['time'].strftime('%I:%M %p on %B %d, %Y')}\n")


# ============================================================================
# EXAMPLE 7: TEST MODE
# ============================================================================

def example_7_test_mode():
    """Run chatbot in test mode"""
    from PersonalAssistantChatbot_Complete import PersonalAssistantChatbot
    
    print("\n" + "="*70)
    print("EXAMPLE 7: TEST MODE")
    print("="*70 + "\n")
    
    chatbot = PersonalAssistantChatbot(name="TestBot")
    
    # Comprehensive test cases
    test_inputs = [
        # Greetings
        "Hello!",
        "Hi there, how are you?",
        
        # Time and Date
        "What time is it?",
        "What's today's date?",
        
        # Help
        "What can you help me with?",
        
        # Calculations
        "Calculate 50 + 25",
        "What is 100 times 2?",
        
        # Definitions
        "Define AI",
        "What is a chatbot?",
        
        # Expressions
        "That's great!",
        "Thank you so much!",
        
        # Goodbye
        "Goodbye!",
    ]
    
    # Run in test mode
    chatbot.test_mode(test_inputs)


# ============================================================================
# EXAMPLE 8: MULTIPLE CONVERSATIONS
# ============================================================================

def example_8_multiple_conversations():
    """Run multiple separate conversations"""
    from PersonalAssistantChatbot_Complete import PersonalAssistantChatbot
    
    print("\n" + "="*70)
    print("EXAMPLE 8: MULTIPLE CONVERSATIONS")
    print("="*70 + "\n")
    
    # Conversation 1: Morning routine
    print("CONVERSATION 1: Morning Routine")
    print("-" * 60)
    
    chatbot1 = PersonalAssistantChatbot(name="Morning Bot")
    conversation1 = [
        "Good morning!",
        "What time is it?",
        "What's the date?",
        "Thanks!",
    ]
    
    for user_input in conversation1:
        response, _ = chatbot1.process_input(user_input)
        print(f"User: {user_input}")
        print(f"Bot: {response}\n")
    
    # Conversation 2: Help and calculations
    print("\nCONVERSATION 2: Help and Math")
    print("-" * 60)
    
    chatbot2 = PersonalAssistantChatbot(name="Math Bot")
    conversation2 = [
        "Hi!",
        "Can you help me with math?",
        "What is 75 + 25?",
        "Multiply 12 times 5",
    ]
    
    for user_input in conversation2:
        response, _ = chatbot2.process_input(user_input)
        print(f"User: {user_input}")
        print(f"Bot: {response}\n")


# ============================================================================
# EXAMPLE 9: ERROR HANDLING
# ============================================================================

def example_9_error_handling():
    """Demonstrate error handling"""
    from PersonalAssistantChatbot_Complete import PersonalAssistantChatbot
    
    print("\n" + "="*70)
    print("EXAMPLE 9: ERROR HANDLING")
    print("="*70 + "\n")
    
    chatbot = PersonalAssistantChatbot(name="Robust Bot")
    
    # Test cases that might cause issues
    test_cases = [
        "",  # Empty input
        "   ",  # Whitespace only
        "!!!!!",  # Special characters
        "xyzabc qwerty",  # Unknown words
        "123 456 789",  # Only numbers
        "a" * 100,  # Very long input
    ]
    
    print(f"{'Input':<30} {'Status':<15} {'Response':<30}")
    print("-" * 75)
    
    for test_input in test_cases:
        try:
            if test_input.strip():  # Skip empty
                response, _ = chatbot.process_input(test_input)
                status = "✓ OK"
                display_input = test_input[:25] + "..." if len(test_input) > 25 else test_input
                print(f"{display_input:<30} {status:<15} {response[:28]:<30}")
        except Exception as e:
            print(f"{test_input[:25]:<30} {'✗ ERROR':<15} {str(e)[:28]:<30}")


# ============================================================================
# EXAMPLE 10: ADVANCED - CUSTOM INTENTS
# ============================================================================

def example_10_custom_intents():
    """Demonstrate adding custom intents"""
    from PersonalAssistantChatbot_Complete import (
        PersonalAssistantChatbot,
        IntentPatterns
    )
    
    print("\n" + "="*70)
    print("EXAMPLE 10: CUSTOM INTENTS")
    print("="*70 + "\n")
    
    # Create custom patterns with additional intents
    class CustomPatterns(IntentPatterns):
        def __init__(self):
            super().__init__()
            
            # Add custom intents
            self.intents['joke'] = {
                'patterns': [
                    r'\b(joke|funny|laugh|tell me a joke)\b',
                    r'\bmake me laugh\b',
                ],
                'responses': [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "I'm not funny, but I'm programmed to try!",
                    "Did you hear about the Python programmer? He was very Pythonic!",
                ]
            }
            
            self.intents['programming'] = {
                'patterns': [
                    r'\b(code|programming|python|javascript|java)\b',
                    r'\bhow do i code\b',
                    r'\bprogramming language\b',
                ],
                'responses': [
                    "Programming is the art of telling another human what you want the computer to do!",
                    "I love talking about code! What would you like to know?",
                    "Programming is fun and challenging. What language interests you?",
                ]
            }
    
    # Create chatbot with custom patterns
    chatbot = PersonalAssistantChatbot(name="Advanced Bot")
    chatbot.intent_patterns = CustomPatterns()
    chatbot.intent_recognizer.intent_patterns = chatbot.intent_patterns.get_intents()
    chatbot.response_generator.intent_patterns = chatbot.intent_patterns.get_intents()
    
    # Test custom intents
    test_inputs = [
        "Tell me a joke!",
        "Can you make me laugh?",
        "I want to learn Python",
        "How do I start programming?",
    ]
    
    print("Testing Custom Intents:")
    print("-" * 60)
    
    for user_input in test_inputs:
        response, _ = chatbot.process_input(user_input)
        print(f"User: {user_input}")
        print(f"Bot: {response}\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_all_examples():
    """Run all examples"""
    
    examples = [
        ("Basic Usage", example_1_basic_usage),
        ("Intent Recognition", example_2_intent_recognition),
        ("Entity Extraction", example_3_entity_extraction),
        ("Calculations", example_4_calculations),
        ("Definitions", example_5_definitions),
        ("Conversation Context", example_6_conversation_context),
        ("Test Mode", example_7_test_mode),
        ("Multiple Conversations", example_8_multiple_conversations),
        ("Error Handling", example_9_error_handling),
        ("Custom Intents", example_10_custom_intents),
    ]
    
    print("\n" + "="*70)
    print("PERSONAL ASSISTANT CHATBOT - COMPLETE EXAMPLES")
    print("="*70)
    
    for i, (name, example_func) in enumerate(examples, 1):
        try:
            print(f"\nRunning Example {i}: {name}...\n")
            example_func()
            print(f"✓ Example {i} completed successfully")
        except Exception as e:
            print(f"✗ Example {i} failed: {str(e)}")
    
    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED!")
    print("="*70 + "\n")


def run_single_example(example_num):
    """Run a single example"""
    examples = {
        1: ("Basic Usage", example_1_basic_usage),
        2: ("Intent Recognition", example_2_intent_recognition),
        3: ("Entity Extraction", example_3_entity_extraction),
        4: ("Calculations", example_4_calculations),
        5: ("Definitions", example_5_definitions),
        6: ("Conversation Context", example_6_conversation_context),
        7: ("Test Mode", example_7_test_mode),
        8: ("Multiple Conversations", example_8_multiple_conversations),
        9: ("Error Handling", example_9_error_handling),
        10: ("Custom Intents", example_10_custom_intents),
    }
    
    if example_num in examples:
        name, func = examples[example_num]
        print(f"\nRunning Example {example_num}: {name}\n")
        func()
    else:
        print(f"Example {example_num} not found. Available: 1-10")


if __name__ == "__main__":
    # Run all examples
    run_all_examples()
    
    # Or run a single example (uncomment to use):
    # run_single_example(1)
    # run_single_example(7)
