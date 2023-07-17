from elevenlabs import generate, play, set_api_key ,save, voices
import os


from dotenv import load_dotenv
load_dotenv()

KEY = os.environ.get("ELEVENLAB_KEY")
ELEVENLABS_API=set_api_key(KEY)

USER_VOICE=os.environ.get("VOICE_MODEL").title()

current_directory = os.path.dirname(os.path.abspath(__file__))
FILENAME = "output.mp3"
OUTPUT_PATH = os.path.join(current_directory, "resource", "voice_out", FILENAME)
voices = voices()

def generate_voice(responded_text):
    audio_gen = generate(text=responded_text,voice=USER_VOICE)
    save(audio_gen, OUTPUT_PATH)
    return OUTPUT_PATH
    


