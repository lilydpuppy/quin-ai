import requests
import json


class LLMBot:
    def __init__(self, model="llama3.1"):
        self.model = model
        self.messages = []

    def add_message(self, role, content):
        """
        Adds a new message to the conversation history.
        """
        self.messages.append({"role": role, "content": content})

    def get_history(self):
        """
        Returns the full conversation history.
        """
        return self.messages

    def clear_history(self):
        """
        Clears the conversation history.
        """
        self.messages = []

    def chat(self, stream=False, temperature=0):
        """
        Sends the conversation history to the model and returns the response.
        """
        url = "http://127.0.0.1:11434/api/chat"  # URL of the API
        headers = {"Content-Type": "application/json"}

        payload = {
            "model": self.model,
            "messages": self.messages,
            "stream": stream,
            "options": {"temperature": temperature}
        }

        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                message = response.json()
                print("Final Response:", message['message']['content'])
                return message['message']['content']
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
