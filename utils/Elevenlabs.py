from elevenlabs import save
import os
from elevenlabs import Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

KEY = os.environ.get("ELEVENLAB_KEY")
client = ElevenLabs(api_key=KEY,)

USER_VOICE = os.environ.get("VOICE_MODEL").title()

current_directory = os.path.dirname(os.path.abspath(__file__))
FILENAME = "output.mp3"
OUTPUT_PATH = os.path.join(current_directory, "resource", "voice_out", FILENAME)
voices_list = client.voices.get_all()


def get_voice_id_by_name(voice_name):
    voice_name = voice_name.lower()

    # Iterate through the voices to find the matching name
    for voice in voices_list:
        for mem in voice[1]:

            if mem.name.lower()==voice_name:
                return mem.voice_id
    return None


def generate_voice(responded_text):

    voice_id = get_voice_id_by_name(USER_VOICE)
    if voice_id is None:
        print("No voice found with the name, please select another voice.")
    audio_gen = client.generate(
        text=responded_text,
        voice=Voice(
            voice_id=voice_id,
            settings=VoiceSettings(stability=0.70, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
        )
    )
    save(audio_gen, OUTPUT_PATH)
    return OUTPUT_PATH

