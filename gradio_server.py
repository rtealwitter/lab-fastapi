#!/usr/bin/env python
'''
A bare-bones web interface for conversations with LLMs served from openai-compatible endpoints.
'''

import argparse
import gradio as gr
from openai import OpenAI

parser = argparse.ArgumentParser()
parser.add_argument("--url")
parser.add_argument("--apikey", default="local-placeholder")
parser.add_argument("--model", default='openai/gpt-oss-20b')
parser.add_argument("--port", type=int, default=7860)
args = parser.parse_args()

client = OpenAI(base_url=args.url, api_key=args.apikey)

def chat(message, history):
    messages = []
    for msg in history:
        content = msg["content"]
        # Gradio 6 represents text as content blocks; the API accepts plain text.
        if isinstance(content, list):
            content = "".join(block.get("text", "") for block in content
                              if block.get("type") == "text")
        messages.append({"role": msg["role"], "content": content})
    messages.append({"role": "user", "content": message})
    completion = client.chat.completions.create(
        model=args.model,
        messages=messages
    )
    return completion.choices[0].message.content

gr.ChatInterface(chat).launch(server_port=args.port)
