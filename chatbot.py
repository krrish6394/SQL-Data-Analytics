"""
Personal Assistant Chatbot
Simple rule-based assistant that matches input text against intent patterns
and returns an appropriate response. This file contains the core implementation
and is fully commented as required by the assignment.
"""

import json
import random
import re
from typing import Dict, List, Optional


class PersonalAssistant:
    """A small rule-based personal assistant.

    It loads intents from a JSON file (see `intents.json`) which contains a list
    of intents. Each intent should have:
      - "tag" (str): identifier
      - "patterns" (list[str]): regex or substring patterns to match user input
      - "responses" (list[str]): candidate responses to pick from

    The assistant tries to find the first matching pattern and returns a
    randomly chosen response for that intent. If nothing matches a fallback
    message is returned.
    """

    def __init__(self, intents_path: str = "intents.json"):
        """Initialize and load intents from disk.

        Args:
            intents_path: Path to a JSON file with intents data.
        """
        self.intents_path = intents_path
        self.intents = self._load_intents(intents_path)

    def _load_intents(self, path: str) -> List[Dict]:
        """Load intents JSON from a file.

        The function returns a list of intent dictionaries. If the file can't
        be read or parsed, it raises a descriptive exception.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Expecting top-level key "intents" with a list
            intents = data.get("intents") if isinstance(data, dict) else data
            if not isinstance(intents, list):
                raise ValueError("Intents file must contain a list under 'intents'")
            return intents
        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to load intents from {path}: {e}")

    def _match_intent(self, text: str) -> Optional[Dict]:
        """Return the first intent dict that matches the input text.

        The matching strategy is:
        - Normalize whitespace
        - Try each pattern from each intent in order
        - Patterns are treated as case-insensitive regular expressions; if the
          pattern contains no regex special characters, it works like a simple
          word/substring search.

        Returns:
            The matching intent dict or None if no match.
        """
        txt = text.strip()
        for intent in self.intents:
            patterns = intent.get("patterns", [])
            for pat in patterns:
                try:
                    # Use case-insensitive matching
                    if re.search(pat, txt, flags=re.IGNORECASE):
                        return intent
                except re.error:
                    # If pat is not a valid regex, fallback to substring check
                    if pat.lower() in txt.lower():
                        return intent
        return None

    def respond(self, text: str) -> str:
        """Generate a response for the provided user text.

        If a matching intent is found, a random response from that intent is
        returned. Otherwise a fallback message is used.
        """
        if not text or not text.strip():
            return "I didn't catch that. Could you rephrase?"

        intent = self._match_intent(text)
        if intent:
            responses = intent.get("responses", [])
            if responses:
                return random.choice(responses)
        # default fallback
        return "Sorry, I don't know how to help with that yet."


if __name__ == "__main__":
    # Simple manual demo when run as a script.
    assistant = PersonalAssistant()
    print("Personal Assistant ready. Type 'quit' or 'exit' to stop.")
    while True:
        try:
            user = input("You: ")
        except EOFError:
            break
        if user.lower().strip() in {"quit", "exit", "q"}:
            print("Assistant: Goodbye!")
            break
        print("Assistant:", assistant.respond(user))
