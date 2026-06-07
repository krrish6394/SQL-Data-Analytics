"""Small CLI runner for the Personal Assistant Chatbot.

Run with: python run_chatbot.py
"""

from datetime import datetime
from chatbot import PersonalAssistant


class Runner:
    """Wraps the assistant to provide small dynamic substitutions."""

    def __init__(self):
        self.assistant = PersonalAssistant("intents.json")

    def format_response(self, resp_template: str) -> str:
        """Fill small placeholders in response templates.

        Currently supports:
          - {time}: local time formatted as HH:MM
        """
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        return resp_template.replace("{time}", time_str)

    def run(self):
        print("Personal Assistant CLI (type 'exit' or 'quit' to stop)")
        while True:
            try:
                user = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nAssistant: Goodbye!")
                break
            if not user:
                continue
            if user.lower() in {"exit", "quit", "q"}:
                print("Assistant: Goodbye!")
                break
            resp = self.assistant.respond(user)
            resp = self.format_response(resp)
            print("Assistant:", resp)


if __name__ == "__main__":
    Runner().run()
