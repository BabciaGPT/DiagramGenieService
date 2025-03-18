import unittest
import os
import json

from dotenv import load_dotenv
from ai.client.OpenAiClient import OpenAIClient
from ai.models.PlantUmlJsonResponse import PlantUmlJsonResponse


class TestOpenAIClient(unittest.TestCase):
    def setUp(self):
        # Ensure OPENAI_API_KEY environment variable is set
        load_dotenv("../../.env")
        if not os.environ.get("OPENAI_API_KEY"):
            self.skipTest("OPENAI_API_KEY environment variable not set")

        self.client = OpenAIClient()
        self.model = "gpt-4o-mini"  # Using gpt-4o-mini model as requested

    def test_ask_basic(self):
        """Test basic functionality of ask method without formatoutput."""
        system_prompt = (
            "You are a helpful assistant. Keep your response brief and direct."
        )
        user_messages = [{"role": "user", "content": "What is 2+2?"}]

        response = self.client.ask(self.model, system_prompt, user_messages)

        # Basic verification that we got a response
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_ask_with_pydantic_model(self):
        """Test ask method with output that can be parsed to a Pydantic model."""
        system_prompt = """You are an assistant that helps with generating PlantUML diagrams. 
        Provide a description and the PlantUML code for a simple diagram."""

        user_messages = [
            {
                "role": "user",
                "content": "Generate a simple class diagram for a User class.",
            }
        ]
        formatoutput = PlantUmlJsonResponse

        response = self.client.ask(
            self.model, system_prompt, user_messages, formatoutput
        )

        # Verify response can be parsed to ResponseModel
        try:
            response_obj = PlantUmlJsonResponse(**json.loads(response))
            self.assertIsInstance(response_obj, PlantUmlJsonResponse)
            self.assertTrue(hasattr(response_obj, "description"))
            self.assertTrue(hasattr(response_obj, "plantuml_code"))
            self.assertIn("@startuml", response_obj.plantuml_code)
            self.assertIn("@enduml", response_obj.plantuml_code)
        except Exception as e:
            self.fail(f"Failed to parse response to ResponseModel: {e}")

    def test_multiple_user_messages(self):
        """Test ask method with a conversation history."""
        system_prompt = "You are a helpful assistant."
        user_messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there! How can I help?"},
            {"role": "user", "content": "What's your name?"},
        ]

        response = self.client.ask(self.model, system_prompt, user_messages)

        # Basic verification that we got a response
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)


if __name__ == "__main__":
    unittest.main()
