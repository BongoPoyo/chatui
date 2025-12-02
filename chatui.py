import os
import sys
import time
import threading
import itertools
from ollama import ChatResponse
from ollama import chat


class Spinner:
    def __init__(self, message="Loading"):
        self.message = message
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._spin, daemon=True).start()

    def _spin(self):
        spinner = itertools.cycle(["|", "/", "-", "\\"])
        while self.running:
            sys.stdout.write(f"\r{self.message} {next(spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)

    def stop(self):
        self.running = False
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()


config_dir = os.path.expanduser('~/.config/chatui')
config_path = os.path.join(config_dir, 'open-ai-api-key')

os.makedirs(config_dir, exist_ok=True)

open_ai_api_key = ""

print("Opening", config_path)
try:
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:
            print("Reading API key from config file:")
            open_ai_api_key = content
        else:
            print("File is empty!")
except FileNotFoundError:
    print("API key file not found.")

if not open_ai_api_key:
    open_ai_api_key = input("Enter the API key: ").strip()
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(open_ai_api_key)
    print("Saved in ~/.config/chatui/open-ai-api-key")


prompt = str(input("Enter the question: "))

spinner = Spinner("Fetching response")
spinner.start()


stream = chat(
    model='gemma3',
    messages=[{'role': 'user', 'content': prompt}],
    stream=True,
)


spinner.stop()
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
