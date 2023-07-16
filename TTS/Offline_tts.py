from TTS.api import TTS
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the file in the 'utils' folder
FILE_PATH= os.path.join(script_dir, "..", "utils", "resource","voice_out","local_tts_output.wav")

# List available 🐸TTS models and choose the first one


'''print(model_name)
print(model_name.index("tts_models/en/jenny/jenny"))'''

def voice_generation(responded_text):
    model_name = TTS.list_models()[24]
    tts = TTS(model_name, progress_bar=True, gpu=False)
    tts.tts_to_file(text= responded_text, emotion="happy",file_path=FILE_PATH)
    return FILE_PATH

def test_1(responded_text):
    model_name = TTS.list_models()[0]

    tts = TTS(model_name)

    wav = tts.tts(responded_text, speaker=tts.speakers[0], language=tts.languages[0])
    # Text to speech to a file
    tts.tts_to_file(text=responded_text, speaker=tts.speakers[0], language=tts.languages[0], file_path=FILE_PATH)
    return FILE_PATH

