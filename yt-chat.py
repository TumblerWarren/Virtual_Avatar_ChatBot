import pytchat
import random, os, json, asyncio, threading, re
import subprocess

import utils.vtube_studio
from dotenv import load_dotenv
load_dotenv()

TTS_CHOICE = os.environ.get("TTS_CHOICE")
TT_CHOICE = os.environ.get("WHISPER_CHOICE")
CHATBOT_CHOICE = os.environ.get("CHATBOT_SERVICE")
input_choice = os.environ.get("INPUT_CHOICE")
sentiment = os.environ.get("SENTIMENT_ENABLED")

video_id = os.environ.get("LIVESTREAM_ID")
message_pick_prob = int(os.environ.get("MESSAGE_PICKING_PROBABILITY"))
message_pick_prob = int(100/message_pick_prob)
stored_timestamp = 0
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def message_picking(messages):

    for message in messages:
        timestamp = message.get("timestamp", "")

        if (stored_timestamp != timestamp) and message.get("amountValue", 0.0) > 0:
            author_name = message["author"]["name"]
            message = message.get("message", "")
            viewer_message = author_name+": "+message

            return True, viewer_message

        elif (stored_timestamp != timestamp) and (random.randint(1, message_pick_prob) == 1):
            author_name = message["author"]["name"]
            message = message.get("message", "")
            viewer_message = author_name+": "+message
            return True, viewer_message

    else:
        return False, ""

def user_message_read():
    try:
        with open("utils/resource/Cache/user_cache.txt", 'r') as file:
            content = file.read()

        with open("utils/resource/Cache/user_cache.txt", 'w') as file:
            file.truncate(0)

        if len(content)>0:
            return content
        else:
            return None

    except FileNotFoundError:
        print(f"Error: File user_tmp not found.")
    except PermissionError:
        print(f"Error: File user_tmp is in use. Please close the file and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def message_arrangement():
    user_message = user_message_read()
    if user_message is None:
        return ""
    else:
        return "\nWarren: "+user_message

def extract_pure_text(text):

    # Remove text within asterisks
    text = re.sub(r'\*.*?\*', '', text)

    # Remove emojis and other special characters
    text = re.sub(r'[\U0001F600-\U0001F6FF]+', '', text)  # Remove emojis
    text = re.sub(r'[\U0001F300-\U0001F5FF]+', '', text)  # Remove other symbols

    # Remove extra spaces
    text = ' '.join(text.split())

    return text

def main():

    global message
    chat = pytchat.create(video_id=video_id)

    while chat.is_alive():
        data = (chat.get().json())
        messages = json.loads(data)

        permission,comment = message_picking(messages)


        if permission:
            comment = comment + "\n" + message_arrangement()
            print(comment)
            if CHATBOT_CHOICE == "oogabooga":
                import API.Oogabooga_Api_Support
                API.Oogabooga_Api_Support.send_via_oogabooga(comment)
                message = API.Oogabooga_Api_Support.receive_via_oogabooga()

            elif CHATBOT_CHOICE == "betacharacter":
                import utils.character_ai
                message = utils.character_ai.send_message(comment)

            elif CHATBOT_CHOICE == "local_llm" or CHATBOT_CHOICE == "collab_llm":
                import API.local_llm_inference
                API.local_llm_inference.send_via_local_llm(comment)
                message = API.local_llm_inference.receive_via_local_llm()

            else:
                print("Sorry Wrong Chatbot Choice")


            if sentiment == "True":
                import API.sentiment_analysis_local_api
                mood = API.sentiment_analysis_local_api.sub_action(message)
                print("Mood:- ", mood)
                utils.vtube_sentiment.run_trigger(mood)

                # Set audio level using VTube Studio
                utils.vtube_studio.set_audio_level(0.5)

                # Play audio using VTube Studio 1o
                utils.vtube_studio.speak()
                utils.vtube_sentiment.run_trigger(mood)

            else:
                if TTS_CHOICE == "ELEVENLABS":
                    import utils.Elevenlabs
                    utils.Elevenlabs.generate_voice(message)
                    utils.vtube_studio.set_audio_level(0.5)
                    utils.vtube_studio.speak()

                # LOCAL_TTS is out of support for now. Will be back soon.
                elif TTS_CHOICE == "LOCAL":
                    import utils.Offline_tts
                    utils.Offline_tts.voice_generation(message)
                    utils.vtube_studio.set_audio_level(0.5)
                    utils.vtube_studio.speak()

                elif TTS_CHOICE == "VOICEVOX":
                    import utils.voicevox_setup
                    id = os.environ.get("VOICE_ID")
                    utils.voicevox_setup.generate_voice(message, id)
                    utils.vtube_studio.set_audio_level(0.5)
                    utils.vtube_studio.speak()

                else:
                    print("The Choice put in .env file not correct!")





def run_program():

    vtube_studio_thread = threading.Thread(target=utils.vtube_studio.run_vtube_studio)
    vtube_studio_thread.daemon = True
    vtube_studio_thread.start()
    main()


if __name__ == "__main__":

    run_program()
