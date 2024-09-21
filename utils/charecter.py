import os
from dotenv import load_dotenv
from characterai import PyCAI

load_dotenv()

PYCHAI_KEY = os.environ.get("PYCHAI")
CHARECTER_KEY = os.environ.get("CHARECTER_KEY")

client = PyCAI(PYCHAI_KEY)
message = ""
name = ""

char = CHARECTER_KEY
chat = client.chat.get_chat(char)

participants = chat['participants']

if not participants[0]['is_human']:
    tgt = participants[0]['user']['username']
else:
    tgt = participants[1]['user']['username']


def send_message(user_input):

    message = user_input
    data = client.chat.send_message(
        chat['external_id'], tgt, message
    )
    name = data['src_char']['participant']['name']

    text = data['replies'][0]['text']
    print(f"{name}: {text}")
    return text
