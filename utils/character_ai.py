import asyncio
import os

from dotenv import load_dotenv, dotenv_values, set_key
from PyCharacterAI import Client


load_dotenv()
token = os.environ.get("PYCHAI")
character_id = os.environ.get("CHARECTER_KEY")
chat_id = os.environ.get("chat_id")

def update_env_file(key, value, env_path='.env'):
    set_key(env_path, key, value)

async def main(message):
    global chat_id

    client = Client()
    try:
        await client.authenticate(token)

        if chat_id == '':
            print("Hello:-",chat_id)
            chat, greeting_message = await client.chat.create_chat(character_id)
            update_env_file('chat_id', chat.chat_id)
            chat_id = chat.chat_id
            answer = await client.chat.send_message(character_id, chat.chat_id, message)

        else:
            answer = await client.chat.send_message(character_id, chat_id, message)

        print(f"{answer.author_name}: {answer.get_primary_candidate().text}")
        return answer.get_primary_candidate().text
    except Exception as e:
        print(f"Error in Character.AI interaction: {e}")
        return f"Sorry, there was an error: {e}"
    finally:
        try:
            await client.close_session()
        except Exception:
            pass

def send_message(message):

    return asyncio.run(main(message))

