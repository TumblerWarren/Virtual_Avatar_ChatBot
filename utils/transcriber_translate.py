import os

import whisper
import torch
from dotenv import load_dotenv
load_dotenv()

device = "cuda" if torch.cuda.is_available() else "cpu"

USER_MODEL=os.environ.get("WHISPER_MODEL")

def translate_any_to_english(voice):

    nresult = ""
    model = whisper.load_model(USER_MODEL)
    result = model.transcribe(voice, task="translate")
    for mem in result["segments"]:
        nresult += mem['text'] + " "

    return nresult

def to_transcribe_original_language(voice):

    nresult=""
    model = whisper.load_model(USER_MODEL)
    result = model.transcribe(voice,language="en")
    for mem in result["segments"]:
        nresult+=mem['text']+" "

    return nresult


