from TTS.api import TTS
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the file in the 'utils' folder
FILE_PATH= os.path.join(script_dir, "", "", "resource", "voice_out", "local_tts_output.wav")

# List available 🐸TTS models and choose the first one
'''Useable models:- ['tts_models/en/ek1/tacotron2','tts_models/en/ljspeech/tacotron2-DDC','tts_models/en/ljspeech/tacotron2-DDC_ph',
'tts_models/en/ljspeech/glow-tts','tts_models/en/jenny/jenny']
'''

def voice_generation(responded_text):

    tts = TTS(model_name='tts_models/en/ljspeech/tacotron2-DDC_ph', progress_bar=False, gpu=False)
    tts.tts_to_file(text= responded_text, emotion="happy",file_path=FILE_PATH)
    return FILE_PATH
