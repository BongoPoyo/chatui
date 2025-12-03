import spinner
from ollama import chat

question = str(input("Enter the question: "))

spinner1 = spinner.Spinner("Fetching response")
spinner1.start()

llm_output = chat(
    model='gemma3:1b',
    messages=[{'role': 'user', 'content': question}],
    stream=True,
)


spinner1.stop()
