from elevenlabs import set_api_key ,save, voices,Voice, VoiceSettings, generate
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


def get_voice_id_by_name(name):
    voices_dict = {voice.name.lower(): voice.voice_id for voice in voices}
    return voices_dict.get(name.lower())


def generate_voice(responded_text):
    # audio_gen = generate(text=responded_text, voice=USER_VOICE)
    voice_id = get_voice_id_by_name(USER_VOICE)
    audio_gen = generate(
        text=responded_text,
        model="eleven_multilingual_v2",
        voice=Voice(
            voice_id=voice_id,

            settings=VoiceSettings(stability=0.70, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
        )
    )
    save(audio_gen, OUTPUT_PATH)
    return OUTPUT_PATH




