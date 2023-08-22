import colorama
import humanize, os, threading

import utils.Elevenlabs
import utils.charecter
import utils.audio
import utils.hotkeys
import utils.transcriber_translate
import TTS.Offline_tts
import utils.vtube_studio
import utils.voicevox_setup
import API.Oogabooga_Api_Support

from dotenv import load_dotenv
load_dotenv()

TTS_CHOICE = os.environ.get("TTS_CHOICE")
TT_CHOICE = os.environ.get("WHISPER_CHOICE")
CHATBOT_CHOICE = os.environ.get("CHATBOT_SERVICE")


def main():
    while True:
        print("You" + colorama.Fore.GREEN + colorama.Style.BRIGHT + " (mic) " + colorama.Fore.RESET + ">", end="", flush=True)
        utils.hotkeys.audio_input_await()
        print("\rYou" + colorama.Fore.GREEN + colorama.Style.BRIGHT + " (mic " + colorama.Fore.YELLOW + "[Recording]" + colorama.Fore.GREEN + ") " + colorama.Fore.RESET + ">", end="", flush=True)
        audio_buffer = utils.audio.record()

        try:
            tanscribing_log = "\rYou" + colorama.Fore.GREEN + colorama.Style.BRIGHT + " (mic " + colorama.Fore.BLUE + "[Transcribing (" + str(humanize.naturalsize(os.path.getsize(audio_buffer))) + ")]" + colorama.Fore.GREEN + ") " + colorama.Fore.RESET + "> "
            print(tanscribing_log, end="", flush=True)
            if TT_CHOICE.upper()== "TRANSLATE":
                transcript=utils.transcriber_translate.translate_any_to_english(audio_buffer)

            elif TT_CHOICE.upper()=="TRANSCRIBE":
                transcript = utils.transcriber_translate.to_transcribe_original_language(audio_buffer)

        except Exception as e:
            print(colorama.Fore.RED + colorama.Style.BRIGHT + "Error: " + str(e))
            continue

        # Clear the last line.
        print('\r' + ' ' * len(tanscribing_log), end="")
        print("\rYou" + colorama.Fore.GREEN + colorama.Style.BRIGHT + " (mic) " + colorama.Fore.RESET + "> ", end="", flush=True)

        print(f"{transcript.strip()}")

        if CHATBOT_CHOICE=="oogabooga":
            API.Oogabooga_Api_Support.send_via_oogabooga(transcript)
            message = API.Oogabooga_Api_Support.receive_via_oogabooga()

        elif CHATBOT_CHOICE == "betacharacter":
            utils.charecter.send_message(transcript)
            message = utils.charecter.received_message()

        else:
            print("Sorry Wrong Chatbot Choice")



        if TTS_CHOICE == "ELEVENLABS":
            utils.Elevenlabs.generate_voice(message)

        elif TTS_CHOICE == "LOCAL_TTS":
            TTS.Offline_tts.test_1(message)

        elif TTS_CHOICE == "VOICEVOX":
            id=os.environ.get("VOICE_ID")
            utils.voicevox_setup.generate_voice(message,id)






        else:
            print("The Choice put in .env file not correct!")



        # Set audio level using VTube Studio
        utils.vtube_studio.set_audio_level(0.5)


        # Play audio using VTube Studio
        utils.vtube_studio.speak()

        # After use, delete the recording.
        try:
            os.remove(audio_buffer)
        except:
            pass

def run_program():
    # Start the VTube Studio interaction in a separate thread
    vtube_studio_thread = threading.Thread(target=utils.vtube_studio.run_vtube_studio)
    vtube_studio_thread.daemon = True
    vtube_studio_thread.start()

    main()


if __name__ == "__main__":

    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Create the resource directory path based on the current directory
    resource_directory = os.path.join(current_directory, "utils","resource")
    os.makedirs(resource_directory, exist_ok=True)

    # Create the voice_in and voice_out directory paths
    voice_in_directory = os.path.join(resource_directory, "voice_in")
    voice_out_directory = os.path.join(resource_directory, "voice_out")

    # Create the voice_in and voice_out directories if they don't exist
    os.makedirs(voice_in_directory, exist_ok=True)
    os.makedirs(voice_out_directory, exist_ok=True)


    run_program()
