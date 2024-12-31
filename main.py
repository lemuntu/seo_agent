import openai 
import os
from dotenv import load_dotenv
from actions import get_seo_page_report
from prompts import react_system_prompt 
from json_helpers import extract_json 

#load environment variables
load_dotenv()

#create an instance of the OpenAI class
openai.api_key = os.getenv ("OPENAI_API_KEY")

def generate_text_with_conversation(messages, model = "gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
        model=model, 
        messages = messages
        )
        return response.choices[0].message.content
    except Exception as e: 
        print (f"An error occured: {e}")
        return None
    
#Available actions are: 
available_actions = {
    "get_seo_page_report": get_seo_page_report 
}
user_prompt = "What is the response time of google.com?"

messages = [
    {"role": "system", "content": react_system_prompt}, 
   {"role": "system", "content": user_prompt},  
]

turn_count = 1
max_turns = 5

while turn_count < max_turns: 
    print (f"loop: {turn_count}")
    print ("------------------------------")
    turn_count += 1
    
    response = generate_text_with_conversation(messages, model = "gpt-3.5-turbo")
    print(response)

    json_function = extract_json(response) 
    if json_function: 
        function_name = json_function[0]['function_name']
        function_parms = json_function[0]['function_parms']
        if function_name not in available_actions: 
            raise Exception(f"Unknown action: {function_name}: {function_parms}")
        print(f" -- running {function_name} {function_parms}")
        action_function = available_actions[function_name]
        #call the function
        result = action_function(**function_parms)
        function_result_message = f"Action_Response: {result}"