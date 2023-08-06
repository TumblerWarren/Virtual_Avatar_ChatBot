import os
import subprocess
import Voicevox_engine
from dotenv import load_dotenv
import psutil

def is_program_running(program_path):
    program_exe = os.path.basename(program_path)
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == program_exe:
            return True
    return False
def run_program(program_name):
    try:
        subprocess.Popen(program_name)
    except Exception as e:
        print(f"Failed to run {program_name}: {e}")

def program_run_main():

    load_dotenv()
    TTS_CHOICE=os.environ.get("TTS_CHOICE")

    if TTS_CHOICE=="VOICEVOX":


        script_dir = os.path.dirname(os.path.abspath(__file__))
        Voicevox_path = os.path.join(script_dir, "..", "VOICEVOX", "VOICEVOX.exe")

        if os.path.exists(Voicevox_path) and os.path.isfile(Voicevox_path):
            if is_program_running(Voicevox_path):
                print("Voicevox is already running!")

            else:
                print("Lanching Voicevox!")
                run_program(Voicevox_path)

        else:
            print(f"ERROR: {Voicevox_path} not found or is not an executable file.")
            print("Attempting to autodownload")
            zip_file_path = "voicevox.zip"
            Voicevox_engine.download_voicevox()
            extract_to_folder = "."
            Voicevox_engine.extract_zip(zip_file_path, extract_to_folder)
            os.remove(zip_file_path)
            run_program(Voicevox_path)



