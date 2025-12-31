from elevenlabs import save
import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

KEY = os.environ.get("ELEVENLAB_KEY")
client = ElevenLabs(api_key=KEY)

USER_VOICE = os.environ.get("VOICE_MODEL")
if USER_VOICE:
    USER_VOICE = USER_VOICE.title()

current_directory = os.path.dirname(os.path.abspath(__file__))
FILENAME = "output.mp3"
OUTPUT_PATH = os.path.join(current_directory, "resource", "voice_out", FILENAME)


def get_voice_id_by_name(voice_name):
    if not voice_name:
        return None
    voice_name = voice_name.lower()

    # Get all voices
    response = client.voices.get_all()
    
    # Check structure (response might be object with .voices or list)
    voices = getattr(response, 'voices', response)

    for voice in voices:
        if voice.name.lower() == voice_name:
            return voice.voice_id
    return None


def generate_voice(responded_text):
    voice_id = get_voice_id_by_name(USER_VOICE)
    if voice_id is None:
        print(f"No voice found with the name '{USER_VOICE}', please select another voice.")
        return None

    # Use the new convert method as requested
    audio = client.text_to_speech.convert(
        text=responded_text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    # Save the audio
    save(audio, OUTPUT_PATH)
    return OUTPUT_PATH

