from openai import OpenAI


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI()

    def ask(self, model, system_prompt, user_messages, formatoutput=None):
        system_message = {
            "role": "system",
            "content": system_prompt,
        }

        if formatoutput is not None:
            system_message["content"] += f"\n Json object:\n{formatoutput}"

        request_params = {
            "model": model,
            "messages": [system_message] + user_messages,
        }

        if formatoutput is not None:
            request_params["response_format"] = formatoutput

        return (
            self.client.beta.chat.completions.parse(**request_params)
            .choices[0]
            .message.content
        )
