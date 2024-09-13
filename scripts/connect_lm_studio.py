# import requests
# import logging

# # Configure logging
# logging.basicConfig(level=logging.ERROR)

# def connect_lm_studio(system_prompt, user_prompt):
#     api_url = "http://localhost:1234/v1/completions"
    
#     prompt = f"{system_prompt}\n\n{user_prompt}"
    
#     payload = {
#         "model": "model-identifier",  # Replace with your model identifier
#         "prompt": prompt,
#         "max_tokens": 8000,  # Ensure this is high enough to handle long responses
#         "temperature": 0.7
#     }
    
#     headers = {
#         "Authorization": "Bearer lm-studio",  # Replace with your actual API key if required
#         "Content-Type": "application/json"
#     }
    
#     try:
#         response = requests.post(api_url, json=payload, headers=headers)
#         response.raise_for_status()
#         result = response.json()
#         if 'choices' in result and result['choices']:
#             return result['choices'][0]['text'].strip()
#         else:
#             logging.error("No choices found in the response.")
#             return "Error: No response generated."
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Request failed: {e}")
#         return "Error: Request failed."



import requests
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

def connect_lm_studio(user_prompt, system_prompt=None):
    api_url = "http://localhost:1234/v1/completions"
    
    # Default system prompt
    default_system_prompt = "You are an advanced language model that provides detailed and accurate responses."

    # Use the provided system_prompt or the default one
    if system_prompt is None:
        system_prompt = default_system_prompt

    # Combine the prompts
    prompt = f"{system_prompt}\n\n{user_prompt}"
    
    payload = {
        "model": "model-identifier",  # Replace with your model identifier
        "prompt": prompt,
        "max_tokens": 8000,  # Ensure this is high enough to handle long responses
        "temperature": 0.7
    }
    
    headers = {
        "Authorization": "Bearer lm-studio",  # Replace with your actual API key if required
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        if 'choices' in result and result['choices']:
            return result['choices'][0]['text'].strip()
        else:
            logging.error("No choices found in the response.")
            return "Error: No response generated."
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return "Error: Request failed."

