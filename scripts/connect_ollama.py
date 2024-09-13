# scripts/connect_ollama.py

import ollama
from prompts.RDoLT_Single import run_prompt

def connect_ollama(task):
    prompt = run_prompt(task)
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']

if __name__ == "__main__":
    task = "Why is the sky blue?"
    response = connect_ollama(task)
    print(response)
