# import logging
# from scripts.connect_lm_studio import connect_lm_studio

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# def decompose_task(task):
#     prompt = f"""
# You are an expert problem solver with expertise in mathematical problem-solving and logical reasoning.

# **Task**: Decompose the following problem into three steps based on complexity: Easy, Intermediate, and Final.

# **Problem**: "{task}"

# Provide each step clearly labeled.

# **Examples**:

# **Example 1**:

# **Problem**: "If a train travels at 60 miles per hour for 2 hours, and then at 80 miles per hour for another 3 hours, what is the total distance traveled by the train?"

# **Easy**: Calculate the distance traveled during the first segment at 60 miles per hour for 2 hours.

# **Intermediate**: Calculate the distance traveled during the second segment at 80 miles per hour for 3 hours.

# **Final**: Add both distances to find the total distance traveled by the train.

# #####################################################

# **Example 2**:

# **Problem**: "Sarah has twice as many apples as Tom. If Tom has 4 apples, how many apples do they have together?"

# **Easy**: Determine the number of apples Tom has.

# **Intermediate**: Calculate the number of apples Sarah has, knowing she has twice as many as Tom.

# **Final**: Add the number of apples Sarah and Tom have to find the total.

# Now, please decompose the problem.

# Easy:"""
#     response = connect_lm_studio(prompt)
#     print(f"LLM Response in decompose_task:\n{response}")  
#     steps = extract_steps(response)
#     return steps

# def extract_steps(response):
#     steps = {}
#     current_step = None
#     lines = response.strip().split('\n')
#     for line in lines:
#         line = line.strip()
#         if line.startswith('Easy:'):
#             current_step = 'Easy'
#             steps[current_step] = line[len('Easy:'):].strip()
#         elif line.startswith('Intermediate:'):
#             current_step = 'Intermediate'
#             steps[current_step] = line[len('Intermediate:'):].strip()
#         elif line.startswith('Final:'):
#             current_step = 'Final'
#             steps[current_step] = line[len('Final:'):].strip()
#         elif current_step and line:
#             steps[current_step] += ' ' + line
#     logging.debug(f"Extracted steps: {steps}")
#     return steps

# def generate_thoughts(task, step_name, step_description, context):
#     # Build the prompt with robust examples
#     prompt = f"""
# You are an expert problem solver focusing on solving the main task: "{task}".

# Generate three distinct and non-empty thoughts for the following step to help solve the main problem.

# **Step**: "{step_name}"
# **Description**: "{step_description}"

# **Context**:
# Selected Thoughts: {context.get('Selected Thoughts', {})}
# Rejected Thoughts: {context.get('Rejected Thoughts', {})}

# **Examples**:

# **Example 1**:

# **Problem**: "If a train travels at 60 miles per hour for 2 hours, and then at 80 miles per hour for another 3 hours, what is the total distance traveled by the train?"

# **Step**: "Easy: Calculate the distance traveled during the first segment at 60 miles per hour for 2 hours."

# 1. Recall that distance equals speed multiplied by time.
# 2. Calculate 60 mph × 2 hours = 120 miles.
# 3. Note the distance for the first segment is 120 miles.

# **Example 2**:

# **Problem**: "John has n apples. He gives 1/3 of them to Sarah and 1/2 of the remaining apples to Tom. If John has 10 apples left, how many apples did he start with?"

# **Step**: "Intermediate: Set up an equation based on the information given."

# 1. Let n be the total number of apples.
# 2. After giving 1/3 to Sarah, John has (2/3)n apples left.
# 3. After giving 1/2 of the remaining to Tom, John has (1/3)n apples left.

# Now, based on the step description and context, generate three new thoughts:

# 1."""
#     response = connect_lm_studio(prompt)
#     logging.debug(f"LLM Response in generate_thoughts for {step_name}: {response}")
#     thoughts = extract_thoughts(response)
#     return thoughts

# def extract_thoughts(response):
#     thoughts = []
#     lines = response.strip().split('\n')
#     for line in lines:
#         line = line.strip()
#         if line.startswith('1.'):
#             thoughts.append(line[2:].strip())
#         elif line.startswith('2.'):
#             thoughts.append(line[2:].strip())
#         elif line.startswith('3.'):
#             thoughts.append(line[2:].strip())
#     return thoughts[:3]  # Ensure only three thoughts are returned

# def score_thought(task, thought, step_name, step_description):
#     # Build the prompt with updated definitions
#     prompt = f"""
# You are an expert evaluator.

# Evaluate the following thought for solving the main problem: "{task}".

# **Current Step**: "{step_name}"
# **Description**: "{step_description}"

# **Thought**: "{thought}"

# Score the thought based on the following criteria, each out of 10:

# 1. **Logical Validity**: Does the thought use correct logical reasoning without errors?
# 2. **Coherence**: Is the thought consistent with the main task and the specific decomposition step? Does it logically connect with previous thoughts and contribute to a unified solution?
# 3. **Relevance**: Is the thought directly related to the problem and helpful in progressing towards the solution at this specific step?
# 4. **Specificity**: Is the thought detailed and precise, avoiding vagueness and generalities?

# Calculate the **total score out of 40** by summing the scores for each criterion.

# Provide **only** the total score as a number.

# **Example**:

# Thought: "Calculate 60 mph × 2 hours = 120 miles to find the distance of the first segment."

# Total Score: 38

# Now, evaluate the provided thought and give the total score only.

# Total Score:"""
#     response = connect_lm_studio(prompt)
#     try:
#         score_line = response.strip().split('\n')[0]
#         score = int(score_line.strip().split()[0])
#         return score
#     except (ValueError, IndexError):
#         logging.error(f"Invalid score received: {response}")
#         return 0

# def run_prompt(task):
#     context = {
#         "Selected Thoughts": {},
#         "Rejected Thoughts": {}
#     }

#     # Step 1: Decompose the task
#     steps = decompose_task(task)
#     logging.debug(f"Steps: {steps}")

#     if not steps:
#         logging.error("Failed to decompose the task.")
#         return None

#     for step_name in ['Easy', 'Intermediate', 'Final']:
#         step_description = steps.get(step_name)
#         if not step_description:
#             logging.error(f"No description found for step: {step_name}")
#             continue

#         # Generate thoughts for the current step
#         thoughts = generate_thoughts(task, step_name, step_description, context)
#         logging.debug(f"Thoughts for {step_name}: {thoughts}")

#         if not thoughts:
#             logging.error(f"Failed to generate thoughts for step: {step_name}")
#             continue

#         selected_thoughts = []
#         rejected_thoughts = []

#         for thought in thoughts:
#             score = score_thought(task, thought, step_name, step_description)
#             logging.debug(f"Thought: {thought}, Score: {score}")

#             thought_entry = {"Thought": thought, "Total Score": score}

#             if score >= 30:
#                 selected_thoughts.append(thought_entry)
#             else:
#                 rejected_thoughts.append(thought_entry)

#         # Update context for knowledge propagation
#         context['Selected Thoughts'][step_name] = [t['Thought'] for t in selected_thoughts]
#         context['Rejected Thoughts'][step_name] = [t['Thought'] for t in rejected_thoughts]

#     # Generate final solution based on selected thoughts and context
#     final_solution = generate_final_solution(task, context)
#     logging.debug(f"Final Solution: {final_solution}")
#     return final_solution

# def generate_final_solution(task, context):
#     # Build the prompt with few-shot examples
#     prompt = f"""
# You are an expert problem solver.

# Based on the selected thoughts and knowledge from previous steps and rejected thoughts, provide a comprehensive final solution to the problem.

# **Problem**: "{task}"

# **Context**:
# Selected Thoughts: {context['Selected Thoughts']}
# Rejected Thoughts: {context['Rejected Thoughts']}

# **Example**:

# Problem: "How can we reduce traffic congestion in urban areas?"

# Selected Thoughts:
# - "Improve public transportation options."
# - "Encourage carpooling through incentives."

# Final Solution:
# To reduce traffic congestion, enhancing public transportation by increasing routes and frequency can make it a more viable option for commuters. Additionally, offering incentives for carpooling can decrease the number of vehicles on the road.

# Now, based on the problem and the selected thoughts, provide the final solution.

# Final Solution:"""
#     response = connect_lm_studio(prompt)
#     return response.strip()




# import logging
# from scripts.connect_lm_studio import connect_lm_studio

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# def run_prompt(task):
#     context = {
#         "Selected Thoughts": {},
#         "Rejected Thoughts": {}
#     }

#     # Define the steps
#     steps = ['Easy', 'Intermediate', 'Final']

#     for step_index, step_name in enumerate(steps):
#         # Build the prompt for the current step
#         prompt = build_prompt(task, step_name, context)
#         response = connect_lm_studio(prompt)
#         logging.debug(f"LLM Response for {step_name} step:\n{response}")

#         # Since we cannot parse the response, we'll assume the LLM has internally handled
#         # decomposition, thought generation, scoring, and knowledge propagation.

#         # We'll store the entire response as the output for this step
#         context['Selected Thoughts'][step_name] = response.strip()

#     # Generate final solution based on context
#     final_solution = generate_final_solution(task, context)
#     logging.debug(f"Final Solution:\n{final_solution}")
#     return final_solution

# def build_prompt(task, step_name, context):
#     # Build the prompt for the current step, including context from previous steps
#     previous_steps_info = ""
#     for prev_step in ['Easy', 'Intermediate', 'Final']:
#         if prev_step == step_name:
#             break
#         if prev_step in context['Selected Thoughts']:
#             previous_steps_info += f"\n{prev_step} Step Thoughts:\n{context['Selected Thoughts'][prev_step]}\n"

#     prompt = f"""
# You are an expert problem solver with expertise in mathematical problem-solving and logical reasoning.

# Main Task: "{task}"

# Current Step: "{step_name}"

# Please perform the following:

# 1. **Decompose the task** for the current step "{step_name}" and describe what needs to be done at this step.
# 2. **Generate three distinct thoughts** that will help solve this step. Think carefully and consider different approaches.
# 3. **Evaluate and score** each thought based on:
#    - Logical Validity
#    - Coherence with the task and step
#    - Relevance to the current step
#    - Specificity and detail
#    Provide a score out of 40 for each thought.
# 4. **Select the best thought(s)** based on the scores.
# 5. **Provide the selected thought(s)** to be used in subsequent steps.

# Keep in mind any information from previous steps:
# {previous_steps_info}

# Please provide your reasoning and proceed with the current step.

# ---

# Your response:
# """
#     return prompt

# def generate_final_solution(task, context):
#     # Build the prompt for generating the final solution
#     previous_steps_info = ""
#     for step_name in ['Easy', 'Intermediate', 'Final']:
#         if step_name in context['Selected Thoughts']:
#             previous_steps_info += f"\n{step_name} Step Thoughts:\n{context['Selected Thoughts'][step_name]}\n"

#     prompt = f"""
# You are an expert problem solver.

# Considering all previous reasoning and selected thoughts, provide a comprehensive final solution to the problem.

# Main Task: "{task}"

# Previous Steps and Thoughts:
# {previous_steps_info}

# Please provide the final solution clearly and concisely.

# ---

# Final Solution:
# """
#     response = connect_lm_studio(prompt)
#     return response.strip()




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

        # Since we cannot parse the response, we'll store it as-is
        # However, we'll inform the LLM to internally handle selection and rejection of thoughts
        context['Selected Thoughts'][step_name] = response.strip()
        # Note: We won't store rejected thoughts separately since we can't parse the response

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

    prompt = f"""
You are an expert problem solver with expertise in mathematical problem-solving and logical reasoning.

Main Task: "{task}"

Your goal is to decompose the task into three steps based on complexity: Easy, Intermediate, and Final. Each step should gradually build upon the previous one.

Current Step: "{step_name}"

Please perform the following:

1. **Decompose the task** by describing what needs to be done at the "{step_name}" step, based on the gradual complexity from Easy to Final.

2. **Generate three distinct thoughts** that will help solve this "{step_name}" step. Each thought should focus on solving the current step and not the entire task.

3. **Evaluate and score** each thought based on the following criteria (each out of 10):
   - **Logical Validity**: Correctness of reasoning.
   - **Coherence**: Consistency with the task and current step.
   - **Relevance**: Applicability to the current step.
   - **Specificity**: Level of detail and precision.

   Provide a **total score out of 40** for each thought.

4. **Select the thoughts** that have a total score of **30 or above**. These are considered **"Selected Thoughts"**. Thoughts scoring below 30 are **"Rejected Thoughts"**.

5. **Provide the selected and rejected thoughts** to be used in subsequent steps.

**Example**:

Main Task: "Calculate the value of 2 + 2."

Current Step: "Easy"

1. **Decompose the task**: Identify the numbers involved (2 and 2).

2. **Generate three thoughts**:
   - Thought 1: Recognize that both numbers are integers.
   - Thought 2: Recall that addition is the operation required.
   - Thought 3: Understand that adding two equal numbers doubles the value.

3. **Evaluate and score**:
   - Thought 1: Score 32/40
   - Thought 2: Score 38/40
   - Thought 3: Score 28/40

4. **Select the thoughts**:
   - **Selected Thoughts**: Thought 1, Thought 2
   - **Rejected Thoughts**: Thought 3

5. **Provide the selected and rejected thoughts**:
   - **Selected Thoughts**:
     - Thought 1: Recognize that both numbers are integers.
     - Thought 2: Recall that addition is the operation required.
   - **Rejected Thoughts**:
     - Thought 3: Understand that adding two equal numbers doubles the value.

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
        # Since we cannot parse the response, we assume rejected thoughts are included in the response
        # We include the entire response for both selected and rejected thoughts
        # This is a limitation due to not parsing the LLM's output

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