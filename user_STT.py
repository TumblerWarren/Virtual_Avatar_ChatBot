import keyboard
import time
import pyaudio
import wave
import os
import whisper
from colorama import *
import humanize
from dotenv import load_dotenv
import psutil

load_dotenv()
choice = os.environ.get('WHISPER_CHOICE')


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
FILENAME = "recording.wav"
RATE = 44100
KEYS = ["RIGHT_CTRL"]
Audio_Path = r'utils\Resource\voice_in'
file_path_tmp = r'utils\resource\Cache\user_cache.txt'

def audio_input():
    return all(keyboard.is_pressed(key) for key in KEYS)


def audio_input_await():
    while not audio_input():
        time.sleep(0.1)


def record():

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    while audio_input():
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    p.terminate()

    ''' 
   if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    '''
    file_path = os.path.join(Audio_Path, FILENAME)

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return file_path


def timestamp(result):
    for mem in result["segments"]:
        #return mem['start'], mem['end'], mem['text']
        return mem['text']


def translate_any_to_english(file_path):
    user_model_choice = os.environ.get('WHISPER_MODEL')
    model = whisper.load_model(user_model_choice)
    result = model.transcribe(file_path, task="translate")
    return result


def to_transcribe_original_language(file_path):
    user_model_choice = os.environ.get('WHISPER_MODEL')
    model = whisper.load_model(user_model_choice,in_memory=True)
    result = model.transcribe(file_path,language="en")
    return result


def write_contents(user_message):
    try:
        # Open the file in write mode ('w')
        with open(file_path_tmp, 'w') as file:
            if user_message!=None:
                # Write contents to the file
                file.write(user_message)


        print(f"Contents have been written to {file_path_tmp}.")
    except Exception as e:
        print(f"An error occurred in writing the user_tmp file: {e}")


def is_file_accessed():
    for proc in psutil.process_iter():
        try:
            open_files = proc.open_files()
            for file in open_files:
                if file.path == file_path_tmp:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False


def file_read_delete():
    try:
        # Read the contents of the file
        with open(file_path_tmp, 'r') as file:
            content = file.read()
            print(f"Contents of {file_path_tmp}:\n{content}")

        # Delete the contents of the file
        with open(file_path_tmp, 'w') as file:
            file.truncate(0)
            print(f"Contents of {file_path_tmp} have been deleted.")
    except FileNotFoundError:
        print(f"The file {file_path_tmp} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


while True:

    print(Style.RESET_ALL + Fore.RESET, end="")

    print("You" + Fore.GREEN + Style.BRIGHT + " (mic) " + Fore.RESET + ">", end="", flush=True)

    # Wait for audio input
    audio_input_await()

    print("\rYou" + Fore.GREEN + Style.BRIGHT + " (mic " + Fore.YELLOW + "[Recording]" + Fore.GREEN +")" + Fore.RESET + ">", end="", flush=True)

    audio_buffer = record()

    if choice == 'TRANSCRIBE':

        try:
            transcribing_log = "\rYou" + Fore.GREEN + Style.BRIGHT + " (mic " + Fore.BLUE + "[Transcribing (" + str(
                humanize.naturalsize(os.path.getsize(audio_buffer))) + ")]" + Fore.GREEN + ") " + Fore.RESET + "> "

            print(transcribing_log, end="", flush=True)
            raw_transcript = to_transcribe_original_language(audio_buffer)
            transcript = timestamp(raw_transcript)


        except Exception as e:
            print(Fore.RED + Style.BRIGHT + "Error in transcribing: " + str(e))
            continue

        print('\r' + ' ' * len(transcribing_log), end="")
        print("\rYou" + Fore.GREEN + Style.BRIGHT + " (mic) " + Fore.RESET + "> ", end="", flush=True)

        print(f"{transcript}")

        write_contents(transcript)

    if choice == 'TRANSLATE':
        try:
            translation_log = "\rYou" + Fore.GREEN + Style.BRIGHT + " (mic " + Fore.BLUE + "[Translating (" + str(humanize.naturalsize(os.path.getsize(audio_buffer))) + ")]" + Fore.GREEN +") " + Fore.RESET + "> "
            print(translation_log, end="", flush=True)
            raw_translation = translate_any_to_english(audio_buffer)
            translation = timestamp(raw_translation)

        except Exception as e:
            print(Fore.RED + Style.BRIGHT + "Error in translation: " + str(e))
            continue

        print('\r' + ' ' * len(translation_log), end="")
        print("\rYou" + Fore.GREEN + Style.BRIGHT + " (mic) " + Fore.RESET + "> ", end="", flush=True)

        print(f"{translation}")

        write_contents(translation)


