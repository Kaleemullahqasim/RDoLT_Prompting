from scripts.connect_lm_studio import connect_lm_studio

def run_prompt(task):
    prompt = f"Answer the following question: {task}. Answer:?"
    result = connect_lm_studio(prompt)
    return result
