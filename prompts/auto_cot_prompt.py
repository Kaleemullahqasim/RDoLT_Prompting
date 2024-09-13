from scripts.connect_lm_studio import connect_lm_studio

def run_prompt(task):
    prompt = f"Think step by step and one by one to answer the: {task}. Answer:?"
    result = connect_lm_studio(prompt)
    return result
