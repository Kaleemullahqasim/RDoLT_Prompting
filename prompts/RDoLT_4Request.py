from scripts.connect_lm_studio import connect_lm_studio
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def decompose_task(task):
    prompt = f"""
You are an expert problem solver with expertise in common sense reasoning, mathematical problem-solving, and logical reasoning.

**Task**: Decompose the following problem into three steps based on complexity: Easy, Intermediate, and Final.

**Problem**: "{task}"

Provide each step clearly labeled.

**Example**:
Easy: Identify the main sources of plastic waste.
Intermediate: Explore methods to reduce plastic usage.
Final: Develop strategies to recycle existing plastic waste.

Now, please decompose the problem.

Easy:"""
    response = connect_lm_studio(prompt)
    steps = extract_steps(response)
    return steps

def extract_steps(response):
    steps = {}
    current_step = None
    lines = response.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('Easy:'):
            current_step = 'Easy'
            steps[current_step] = line[len('Easy:'):].strip()
        elif line.startswith('Intermediate:'):
            current_step = 'Intermediate'
            steps[current_step] = line[len('Intermediate:'):].strip()
        elif line.startswith('Final:'):
            current_step = 'Final'
            steps[current_step] = line[len('Final:'):].strip()
        elif current_step and line:
            steps[current_step] += ' ' + line
    return steps

def generate_thoughts(step_name, step_description, context):
    # Build the prompt with few-shot examples
    prompt = f"""
You are an expert problem solver focusing on solving the main task: "{task}".

Generate three distinct and non-empty thoughts for the following step to help solve the main problem.

**Step**: "{step_name}"
**Description**: "{step_description}"

**Context**:
Selected Thoughts: {context.get('Selected Thoughts', {})}
Rejected Thoughts: {context.get('Rejected Thoughts', {})}

**Example**:
1. Thought about reducing plastic bag usage.
2. Idea on promoting reusable containers.
3. Suggestion to implement plastic taxes.

Now, based on the step description and context, generate three new thoughts:

1."""
    response = connect_lm_studio(prompt)
    thoughts = extract_thoughts(response)
    return thoughts

def extract_thoughts(response):
    thoughts = []
    lines = response.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('1.'):
            thoughts.append(line[2:].strip())
        elif line.startswith('2.'):
            thoughts.append(line[2:].strip())
        elif line.startswith('3.'):
            thoughts.append(line[2:].strip())
    return thoughts[:3]  # Ensure only three thoughts are returned

def score_thought(thought):
    # Build the prompt with few-shot examples
    prompt = f"""
You are an expert evaluator.

Evaluate the following thought for solving the main problem: "{task}".

**Thought**: "{thought}"

Consider the following criteria, each scored out of 10:
- Logical Validity
- Coherence
- Simplicity
- Adaptiveness

Calculate the **total score out of 40** by summing the scores for each criterion.

Provide **only** the total score as a number.

**Example**:

Thought: "Encourage recycling programs in schools."
Total Score: 32

Now, evaluate the provided thought and give the total score only.

Total Score:"""
    response = connect_lm_studio(prompt)
    try:
        score = int(response.strip().split()[0])
        return score
    except (ValueError, IndexError):
        logging.error(f"Invalid score received: {response}")
        return 0

def run_multistep_reasoning(task):
    context = {
        "Selected Thoughts": {},
        "Rejected Thoughts": {}
    }

    # Step 1: Decompose the task
    steps = decompose_task(task)
    logging.debug(f"Steps: {steps}")

    if not steps:
        logging.error("Failed to decompose the task.")
        return None

    for step_name in ['Easy', 'Intermediate', 'Final']:
        step_description = steps.get(step_name)
        if not step_description:
            logging.error(f"No description found for step: {step_name}")
            continue

        # Generate thoughts for the current step
        thoughts = generate_thoughts(step_name, step_description, context)
        logging.debug(f"Thoughts for {step_name}: {thoughts}")

        if not thoughts:
            logging.error(f"Failed to generate thoughts for step: {step_name}")
            continue

        selected_thoughts = []
        rejected_thoughts = []

        for thought in thoughts:
            score = score_thought(thought)
            logging.debug(f"Thought: {thought}, Score: {score}")

            thought_entry = {"Thought": thought, "Total Score": score}

            if score >= 30:
                selected_thoughts.append(thought_entry)
            else:
                rejected_thoughts.append(thought_entry)

        # Update context for knowledge propagation
        context['Selected Thoughts'][step_name] = selected_thoughts
        context['Rejected Thoughts'][step_name] = rejected_thoughts

    # Generate final solution based on selected thoughts and context
    final_solution = generate_final_solution(task, context)
    logging.debug(f"Final Solution: {final_solution}")
    return final_solution

def generate_final_solution(task, context):
    # Build the prompt with few-shot examples
    prompt = f"""
You are an expert problem solver.

Based on the selected thoughts and knowledge from previous steps, provide a comprehensive final solution to the problem.

**Problem**: "{task}"

**Context**:
Selected Thoughts: {context['Selected Thoughts']}

**Example**:

Problem: "How can we reduce traffic congestion in urban areas?"

Selected Thoughts:
- "Improve public transportation options."
- "Encourage carpooling through incentives."

Final Solution:
To reduce traffic congestion, enhancing public transportation by increasing routes and frequency can make it a more viable option for commuters. Additionally, offering incentives for carpooling can decrease the number of vehicles on the road.

Now, based on the problem and the selected thoughts, provide the final solution.

Final Solution:"""
    response = connect_lm_studio(prompt)
    return response.strip()

# Example usage
if __name__ == "__main__":
    task = "How can we reduce the environmental impact of plastic waste?"
    final_solution = run_multistep_reasoning(task)
    print("Final Solution:")
    print(final_solution)