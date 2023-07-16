import os

from characterai import PyCAI
from dotenv import load_dotenv
load_dotenv()

PYCHAI_KEY=os.environ.get("PYCHAI")
CHARECTER_KEY=os.environ.get("CHARECTER_KEY")


client = PyCAI(PYCHAI_KEY)
message=""
name=""
def send_message(user_input):
    global message, name
    message_send = user_input
    data = client.chat.send_message(CHARECTER_KEY, message_send)

    message = data['replies'][0]['text']
    name = data['src_char']['participant']['name']



def received_message():
    print(f"{name}: {message}")
    return message