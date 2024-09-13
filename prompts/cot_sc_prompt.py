from scripts.connect_lm_studio import connect_lm_studio

def run_prompt(task):
    prompt = f"Let's break down the problem and verify each step for consistency, arrive at final answer by voting majority voting thoght is correct answer: {task}. Answer:?"
    result = connect_lm_studio(prompt)
    return result
