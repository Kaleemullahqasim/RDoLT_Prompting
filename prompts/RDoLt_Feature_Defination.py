import logging
from scripts.connect_lm_studio import connect_lm_studio

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def run_prompt(task):
    context = {
        "Selected Thoughts": {},
        "Rejected Thoughts": {}
    }

    # Define the steps based on gradual complexity
    steps = ['Easy', 'Intermediate', 'Final']

    for step_name in steps:
        # Build the prompt for the current step
        prompt = build_prompt(task, step_name, context)
        response = connect_lm_studio(prompt)
        logging.debug(f"LLM Response for {step_name} step:\n{response}")

        # Store the response as-is
        context['Selected Thoughts'][step_name] = response.strip()
        # Note: We can't separately store rejected thoughts without parsing

    # Generate final solution based on context
    final_solution = generate_final_solution(task, context)
    logging.debug(f"Final Solution:\n{final_solution}")
    return final_solution

def build_prompt(task, step_name, context):
    # Build the prompt for the current step, including context from previous steps
    previous_steps_info = ""
    for prev_step in ['Easy', 'Intermediate', 'Final']:
        if prev_step == step_name:
            break
        if prev_step in context['Selected Thoughts']:
            previous_steps_info += f"\n{prev_step} Step Selected Thoughts:\n{context['Selected Thoughts'][prev_step]}\n"

    # Detailed definitions of the scoring features in natural language
    scoring_definitions = """
**Scoring Criteria Definitions:**

1. **Logical Validity**: The thought should be logically sound, without any contradictions or errors in reasoning. It should not violate known logical rules or facts.

2. **Coherence**: The thought should be consistent with previous thoughts and should logically follow from them. It should align with the main task and the specific decomposition step, contributing to a unified solution.

3. **Simplicity**: The thought should be clear and concise, avoiding unnecessary complexity. It should be straightforward and uncomplicated, making it easy to understand.

4. **Adaptiveness**: The thought should effectively address the current step's requirements and align with the task instructions. It should be applicable and relevant to solving the problem at hand.

Each criterion is scored out of 10, resulting in a total score out of 40 for each thought.
"""

    prompt = f"""
You are an expert problem solver with expertise in mathematical problem-solving and logical reasoning.

Main Task: "{task}"

Your goal is to decompose the task into three steps based on complexity: Easy, Intermediate, and Final. Each step should gradually build upon the previous one.

Current Step: "{step_name}"

Please perform the following:

1. **Decompose the task** by describing what needs to be done at the "{step_name}" step, based on gradual complexity from Easy to Final.

2. **Generate three distinct thoughts** that will help solve this "{step_name}" step. Each thought should focus on solving the current step and not the entire task.

3. **Evaluate and score** each thought based on the following criteria:

{scoring_definitions}

4. **Select the thoughts** that have a total score of **30 or above**. These are considered **"Selected Thoughts"**. Thoughts scoring below 30 are **"Rejected Thoughts"**.

5. **Provide the selected and rejected thoughts** to be used in subsequent steps.

**Example**:

Main Task: "John has n apples. He gives 1/3 of them to Sarah and 1/2 of the remaining apples to Tom. If John has 10 apples left, how many apples did he start with?"

Current Step: "Easy"

1. **Decompose the task**: Represent the problem using algebraic expressions.

2. **Generate three thoughts**:
   - Thought 1: Let n represent the total number of apples.
   - Thought 2: Calculate the number of apples given to Sarah.
   - Thought 3: Understand that after giving apples to Sarah, John has 2/3 of n apples left.

3. **Evaluate and score**:
   - Thought 1:
     - Logical Validity: 10/10 (Defines the variable correctly)
     - Coherence: 9/10 (Consistent with the problem)
     - Simplicity: 10/10 (Straightforward and clear)
     - Adaptiveness: 10/10 (Directly applicable to the problem)
     - **Total Score**: 39/40
   - Thought 2:
     - Logical Validity: 8/10 (Needs more detail)
     - Coherence: 8/10 (Somewhat consistent)
     - Simplicity: 8/10 (Could be clearer)
     - Adaptiveness: 8/10 (Relevant but not fully developed)
     - **Total Score**: 32/40
   - Thought 3:
     - Logical Validity: 10/10 (Correct calculation)
     - Coherence: 9/10 (Follows from previous thought)
     - Simplicity: 9/10 (Clear and concise)
     - Adaptiveness: 9/10 (Highly relevant)
     - **Total Score**: 37/40

4. **Select the thoughts**:
   - **Selected Thoughts**: Thought 1, Thought 3
   - **Rejected Thoughts**: Thought 2

5. **Provide the selected and rejected thoughts**:
   - **Selected Thoughts**:
     - Thought 1: Let n represent the total number of apples.
     - Thought 3: Understand that after giving apples to Sarah, John has 2/3 of n apples left.
   - **Rejected Thoughts**:
     - Thought 2: Calculate the number of apples given to Sarah.

---

Keep in mind any information from previous steps:
{previous_steps_info}

Please provide your reasoning and proceed with the current step.

---

Your response:
"""
    return prompt

def generate_final_solution(task, context):
    # Build the prompt for generating the final solution
    selected_thoughts_info = ""
    rejected_thoughts_info = ""
    for step_name in ['Easy', 'Intermediate', 'Final']:
        if step_name in context['Selected Thoughts']:
            selected_thoughts_info += f"\n{step_name} Step Selected Thoughts:\n{context['Selected Thoughts'][step_name]}\n"
            # We cannot extract rejected thoughts without parsing
            rejected_thoughts_info += f"\n{step_name} Step Rejected Thoughts:\n[Cannot extract due to parsing constraints]\n"

    prompt = f"""
You are an expert problem solver.

Considering all previous reasoning and thoughts, provide a comprehensive final solution to the problem.

Main Task: "{task}"

Use the **Selected Thoughts** from each step to construct your solution.

Be aware of the **Rejected Thoughts**; ensure that your final solution avoids the mistakes or incorrect reasoning found in them.

Selected Thoughts:
{selected_thoughts_info}

Rejected Thoughts:
{rejected_thoughts_info}

Please provide the final solution clearly and concisely.

---

Final Solution:
"""
    response = connect_lm_studio(prompt)
    return response.strip()