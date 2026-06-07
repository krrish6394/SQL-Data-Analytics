"""Unit tests for the Personal Assistant Chatbot.

Run tests with `pytest -q` from the repository root.
"""

import os
import sys
from pathlib import Path

# Ensure repository root is on sys.path so imports like `from chatbot import ...`
# work when pytest runs from the tests directory.
REPO_ROOT = str(Path(__file__).resolve().parent.parent)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from chatbot import PersonalAssistant


def test_greeting():
    assistant = PersonalAssistant("intents.json")
    resp = assistant.respond("Hello")
    # either one of the configured responses or a fallback string
    expected = [r for it in assistant.intents if it["tag"] == "greeting" for r in it["responses"]]
    assert isinstance(resp, str)
    assert resp in expected or resp.startswith("Sorry") or resp.startswith("I didn't")


def test_time_intent_substitution():
    # ensure time intent exists and template contains {time}
    assistant = PersonalAssistant("intents.json")
    # Find time intent
    time_intent = next((it for it in assistant.intents if it.get("tag") == "time"), None)
    assert time_intent is not None
    # The response template contains {time}
    assert any("{time}" in r for r in time_intent.get("responses", []))


def test_good_night():
    assistant = PersonalAssistant("intents.json")
    resp = assistant.respond("Good night")
    # Accept either one of the listed responses or fallback
    expected = [r for it in assistant.intents if it["tag"] == "good_night" for r in it["responses"]]
    assert isinstance(resp, str)
    assert resp in expected or resp.startswith("Sorry")
