import os
import threading
import requests
from transformers import pipeline
from dotenv import load_dotenv
import json
import torch
with open('F:\Projects\Vtube-Plugin-Demo\O-O-Chat\expression_config.json', 'r') as file:
    data = json.load(file)
    labels = list(data.keys())
    expression_name = list(data.values())

#device = "cuda" if torch.cuda.is_available() else "cpu"

load_dotenv()
TTS_CHOICE = os.environ.get("TTS_CHOICE")
ANALYSIS_TYPE = os.environ.get("ANALYSIS_TYPE")
HUGG_API = os.environ.get('HUGGING_FACE_API_KEY')
API_KEY = "Bearer "+HUGG_API
sentiment_result = 'neutral'


def choose_tts():
    if TTS_CHOICE.upper() == 'ELEVENLABS':
        import utils.Elevenlabs
        return utils.Elevenlabs.generate_voice

    elif TTS_CHOICE.upper() == 'LOCAL':
        import utils.Offline_tts
        return utils.Offline_tts.voice_generation

    elif TTS_CHOICE.upper() == 'VOICEVOX':
        import VoiceVox_local.voice_vox_api
        return VoiceVox_local.voice_vox_api.generate_voice

    else:
        print("Wrong TTS choice!")


def huggingface_api_sentiment_analysis(message):
    global sentiment_result
    # API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    API_URL = "https://api-inference.huggingface.co/models/MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli"

    headers = {"Authorization": API_KEY}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": message,
        "parameters": {"candidate_labels": labels},
    })

    sentiment_result = (output['labels'])[0]


def local_machine_sentiment_analysis(message):
    global sentiment_result
    classifier = pipeline("zero-shot-classification",
                          model=r"F:\Projects\Resource\Models\MoritzLaurer\multilingual-MiniLMv2-L6-mnli-xnli",device="cpu",use_fast=True)
    sequence_to_classify = message
    candidate_labels = labels
    output = classifier(sequence_to_classify, candidate_labels, multi_label=False)

    sentiment_result = (output['labels'])[0]
    print(sentiment_result)

def sub_action_api(message):

    sentiment_analysis_thread = threading.Thread(target=huggingface_api_sentiment_analysis,args=(message,))
    tts_thread = threading.Thread(target=choose_tts(), args=(message,))
    sentiment_analysis_thread.start()
    tts_thread.start()
    sentiment_analysis_thread.join()
    tts_thread.join()
    sentiment_info = sentiment_result

    for k, v in data.items():
        if k == sentiment_info:
            return data.get(k)

def sub_action_local(message):

    sentiment_analysis_thread = threading.Thread(target=local_machine_sentiment_analysis,args=(message,))
    tts_thread = threading.Thread(target=choose_tts(), args=(message,))
    sentiment_analysis_thread.start()
    tts_thread.start()
    sentiment_analysis_thread.join()
    tts_thread.join()
    sentiment_info = sentiment_result

    for k, v in data.items():
        if k == sentiment_info:
            return data.get(k)

def sub_action(message):
    if ANALYSIS_TYPE == "local":
        sub_action_local(message)
    elif ANALYSIS_TYPE == "huggingface":
        sub_action_api(message)
