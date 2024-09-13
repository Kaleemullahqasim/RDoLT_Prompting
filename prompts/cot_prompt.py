from scripts.connect_lm_studio import connect_lm_studio

def run_prompt(task):
    prompt = f"Let's think step by step and solve the problem: {task}. Answer? "
    result = connect_lm_studio(prompt)
    return result
