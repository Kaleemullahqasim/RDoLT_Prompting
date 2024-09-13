from scripts.connect_lm_studio import connect_lm_studio
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def run_prompt(task):
    prompt = f"""
    You are an expert problem solver with expertise in common sense reasoning, mathematical problem-solving, and logical reasoning. Perform the following tasks in a single response. Be concise:

    1. **Decompose the following problem into three steps: Easy, Intermediate, and Final.** 
       - Problem: {task}
       - Use the format:
         Step 1 (Easy): [description]
         Step 2 (Intermediate): [description]
         Step 3 (Final): [description]

    2. **Generate three distinct and non-empty thoughts for each step.** 
       - Use the format:
         Step 1 (Easy):
         Thought 1: [thought]. Scores: Logical Validity: [score], Coherence: [score], Simplicity: [score], Adaptiveness: [score].
         Thought 2: [thought]. Scores: Logical Validity: [score], Coherence: [score], Simplicity: [score], Adaptiveness: [score].
         Thought 3: [thought]. Scores: Logical Validity: [score], Coherence: [score], Simplicity: [score], Adaptiveness: [score].
         
         Step 2 (Intermediate):
         Thought 1: [thought]. Scores: Logical Validity: [score], Coherence: [score], Simplicity: [score], Adaptiveness: [score].
         Thought 2: [thought]. Scores: Logical Validity: [score], Coherence: [score], Simplicity: [score], Adaptiveness: [score].
         Thought 3: [thought]. Scores: Logical Validity: [score], Coherence: [score], Simplicity: [score], Adaptiveness: [score].
         
         Step 3 (Final):
         Thought 1: [thought]. Scores: Logical Validity: [score], Coherence: [score], Simplicity: [score], Adaptiveness: [score].
         Thought 2: [thought]. Scores: Logical Validity: [score], Coherence: [score], Simplicity: [score], Adaptiveness: [score].
         Thought 3: [thought]. Scores: Logical Validity: [score], Coherence: [score], Simplicity: [score], Adaptiveness: [score].

    3. **Score each thought based on logical validity, coherence, simplicity, and adaptiveness.** 
       - Use a scale of 0 to 10 for each score. Scoring these thoughts is very important, selection and rejection of thoughts will be based on these scores.

    4. **Propagate knowledge from one step to the next, maintaining context. Use selected thoughts to inform subsequent steps. Include rejected thoughts for guidance.** 
       - Use the format:
         Selected Thought for Step 1: [selected thought]
         Rejected Thoughts for Step 1: [rejected thoughts]

         Selected Thought for Step 2: [selected thought]
         Rejected Thoughts for Step 2: [rejected thoughts]
         
         Selected Thought for Step 3: [selected thought]
         Rejected Thoughts for Step 3: [rejected thoughts]

    5. **Apply the selected thoughts to solve the initial task.** 
       - Use the knowledge and steps from the selected thoughts to provide the final solution to the problem.

    **Output Format:**
    Step 1 (Easy): [description]
    Thought 1: [thought]. Scores: Logical Validity: [score], Coherence: [score], Simplicity: [score], Adaptiveness: [score].
    Thought 2: [thought]. Scores: [scores].
    Thought 3: [thought]. Scores: [scores].
    Selected Thought for Step 1: [selected thought]
    Rejected Thoughts for Step 1: [rejected thoughts]

    Step 2 (Intermediate): [description]
    Thought 1: [thought]. Scores: [scores].
    Thought 2: [thought]. Scores: [scores].
    Thought 3: [thought]. Scores: [scores].
    Selected Thought for Step 2: [selected thoughts]
    Rejected Thoughts for Step 2: [rejected thoughts]

    Step 3 (Final): [description]
    Thought 1: [thought]. Scores: [scores].
    Thought 2: [thought]. Scores: [scores].
    Thought 3: [thought]. Scores: [scores].
    Selected Thought for Step 3: [selected thought]
    Rejected Thoughts for Step 3: [rejected thoughts]

    **Final Solution:**
    [final solution to the initial task based on the selected thoughts and propagated context]
   
    """
    
    response = connect_lm_studio(prompt)
    logging.debug(f"Full response: {response}")
    return response


