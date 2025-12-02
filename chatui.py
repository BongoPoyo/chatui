import spinner
from ollama import chat


prompt = str(input("Enter the question: "))

spinner1 = spinner.Spinner("Fetching response")
spinner1.start()

stream = chat(
    model='gemma3:1b',
    messages=[{'role': 'user', 'content': prompt}],
    stream=True,
)

spinner1.stop()
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
