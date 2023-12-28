import requests
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the file in the 'utils' folder
path= os.path.join(script_dir, "..", "utils", "resource", "voice_out", "voicevox.wav")

# Set the base URL of the API server
BASE_URL = "http://127.0.0.1:8000"

def generate_voice(text, speaker_id):
    url = f"{BASE_URL}/generate_voice/"
    params = {"text": text, "speaker_id": speaker_id, "path": path}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        file_path = response_data.get("file_path")
        if file_path:
            #print(file_path)
            return file_path
        else:
            print("Error: Voice file path not found in the response.")
            return None
    else:
        print(f"Error: Failed to generate voice. Status code: {response.status_code}")
        return None



