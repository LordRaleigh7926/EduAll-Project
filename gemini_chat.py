import google.generativeai as genai
import json


# Loading the JSON configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


API_KEY = config['API_Key']
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_chat_response(prompt):
    chat_session = model.start_chat()
    response = chat_session.send_message(f"{prompt}. Please not write 'Assistant:' or something like that before your messages.")
    return response.candidates[0].content.parts[0].text
