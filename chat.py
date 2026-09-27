"""Optional live Chat example; lab requirements are on the course assignment page.

The default endpoint uses mock_chat.Chat. For the project integration, import
that project's Chat class as described on the course page. Live reply wording
is not deterministic, even at temperature zero, so it is not a doctest fixture.
"""
import os
from dotenv import load_dotenv
from groq import Groq


class Chat:
    MODEL = 'openai/gpt-oss-20b'

    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
        self.messages = [{'role': 'system', 'content': 'Reply in one or two sentences.'}]

    def send_message(self, message, temperature=0.8):
        self.messages.append({'role': 'user', 'content': message})
        response = self.client.chat.completions.create(
            model=self.MODEL, messages=self.messages, temperature=temperature,
        )
        reply = response.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': reply})
        return reply


def repl():
    chat = Chat()
    try:
        while True:
            print(chat.send_message(input('chat> ')))
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == '__main__':
    repl()
