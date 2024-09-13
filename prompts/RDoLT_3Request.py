from scripts.connect_lm_studio import connect_lm_studio
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def generate_initial_thoughts(problem):
    prompt = f"""
    Decompose the following problem into three steps: Easy, Intermediate, and Final. Generate three thoughts for each step.
    Problem: {problem}
    
    Format:
    Easy Step: [description]
    Thought 1: [thought]
    Thought 2: [thought]
    Thought 3: [thought]

    Intermediate Step: [description]
    Thought 1: [thought]
    Thought 2: [thought]
    Thought 3: [thought]

    Final Step: [description]
    Thought 1: [thought]
    Thought 2: [thought]
    Thought 3: [thought]
    """
    logging.debug(f"Initial thoughts prompt: {prompt}")
    response = connect_lm_studio(prompt)
    logging.debug(f"Initial thoughts response: {response}")
    return response

def evaluate_and_select_thoughts(initial_thoughts):
    prompt = f"""
    Evaluate the following thoughts on the following four features and select the best thought for each step. Provide the selected thought for each step.
    
    Definitions:
    - Logical Validity: Correctness of the thought.
    - Coherence: How well the thought fits with the problem and other thoughts.
    - Simplicity: Clarity and simplicity of the thought.
    - Adaptiveness: Applicability and flexibility of the thought.

    Thoughts:
    {initial_thoughts}

    Format:
    Easy Step: [selected thought]
    Intermediate Step: [selected thought]
    Final Step: [selected thought]
    """
    logging.debug(f"Evaluate and select thoughts prompt: {prompt}")
    response = connect_lm_studio(prompt)
    logging.debug(f"Evaluate and select thoughts response: {response}")
    return response

def generate_final_solution(problem, selected_thoughts):
    prompt = f"""
    Integrate the following selected thoughts into a coherent final solution to the problem. Ensure the final solution is logical and coherent and answer the problem.
    Problem = {problem}

    Selected Thoughts:
    {selected_thoughts}

    Final Solution:
    """
    logging.debug(f"Generate final solution prompt: {prompt}")
    response = connect_lm_studio(prompt)
    logging.debug(f"Generate final solution response: {response}")
    return response

def run_prompt(task):
    initial_thoughts = generate_initial_thoughts(task)
    logging.debug(f"Initial thoughts: {initial_thoughts}")
    selected_thoughts = evaluate_and_select_thoughts(initial_thoughts)
    logging.debug(f"Selected thoughts: {selected_thoughts}")
    final_solution = generate_final_solution(task, selected_thoughts)
    logging.debug(f"Final solution: {final_solution}")
    return final_solution
