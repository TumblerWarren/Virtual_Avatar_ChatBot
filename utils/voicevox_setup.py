'''from voicevox import Client
import asyncio
import utils.translationtest
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the file in the 'utils' folder
FILE_PATH= os.path.join(script_dir, "..", "utils", "resource", "voice_out", "voicevox.wav")

async def generate_voice(text, id):
    text = utils.translationtest.translation(text, "ja")
    async with Client() as client:
        audio_query = await client.create_audio_query(text, speaker=id)
        with open(FILE_PATH, "wb") as f:
            f.write(await audio_query.synthesis(speaker=id))

def run_voicevox(message, id):
    text = utils.translationtest.translation(message, "ja")
    asyncio.to_thread(generate_voice, text, id)


#run_voicevox("Hello, My name is warren!",8)'''


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



