from scripts.connect_lm_studio import connect_lm_studio

def run_prompt(task):
    prompt = f"Solve the problem from the simplest component to the most complex component: {task}.Answer:?"
    result = connect_lm_studio(prompt)
    return result
