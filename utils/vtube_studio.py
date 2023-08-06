import asyncio,os,threading
import utils.audio
import pyvts
from dotenv import load_dotenv

VTS = pyvts.vts(
    plugin_info={
        "plugin_name": "waifu",
        "developer": "Warren",
        "authentication_token_path": "./token.txt",
    },
    vts_api_info={
        "version": "1.0",
        "name": "VTubeStudioPublicAPI",
        "port": os.environ.get("VTUBE_STUDIO_API_PORT", 8001)
    }
)

VOICE_LEVEL = 0

load_dotenv()
TTS_CHOICE = os.environ.get("TTS_CHOICE")


def set_audio_level(level):
    global VOICE_LEVEL
    VOICE_LEVEL = level

async def start():
    await VTS.connect()
    await VTS.request_authenticate_token()
    await VTS.request_authenticate()

    # Continuously update the mouth movement based on VOICE_LEVEL
    while True:
        await VTS.request(
            VTS.vts_request.requestSetParameterValue(parameter="MouthOpen", value=VOICE_LEVEL)
        )
        await asyncio.sleep(1/30)  # 30fps

def run_vtube_studio():
    asyncio.run(start())






def speak():
    if TTS_CHOICE.upper()=="LOCAL_TTS":
        memfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource", "Voice_out", "local_tts_output.wav")

        utils.audio.play_wav(memfile, set_audio_level)

    elif TTS_CHOICE.upper()=="ELEVENLABS":
        memfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource", "Voice_out", "output.mp3")
        utils.audio.play_mp3(memfile,set_audio_level)

    elif TTS_CHOICE.upper()=="VOICEVOX":
        memfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource", "Voice_out", "voicevox.wav")
        utils.audio.play_wav(memfile, set_audio_level)


def action():
    # Start the VTube Studio interaction in a separate thread
    vtube_studio_thread = threading.Thread(target=run_vtube_studio)
    vtube_studio_thread.daemon = True
    vtube_studio_thread.start()
    speak()




