import requests
from dotenv import load_dotenv
import os
load_dotenv()
CHATBOT_SERVICE = os.environ.get("CHATBOT_SERVICE")
message = ""

def send_via_local_llm(user_input):
    global message
    if CHATBOT_SERVICE == 'local_llm':
        url = 'http://localhost:5000/generate_response'
    elif CHATBOT_SERVICE == 'collab_llm':
        url = os.environ.get("ngrok_url")+"/generate_response"
    data = {'user_send_input': user_input}
    response = requests.post(url, json=data)
    try:
        if response.status_code == 200:
            response_json = response.json()
            if 'response' in response_json:
                message = response_json['response']

            else:
                print("Response JSON doesn't contain 'response' key:", response_json)
        else:
            print("Error Response")
    except Exception as e:
        print("Exception during response handling:", e)

def receive_via_local_llm():
    print("AI: ",message)
    return message