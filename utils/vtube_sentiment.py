import asyncio
import time

import pyvts
import os

VTS = pyvts.vts(
    plugin_info={
        "plugin_name": "waifu",
        "developer": "Warren",
        #"authentication_token_path": "token.txt",
        "authentication_token_path": r"./token.txt",

    },
    vts_api_info={
        "version": "1.0",
        "name": "VTubeStudioPublicAPI",
        "port": os.environ.get("VTUBE_STUDIO_API_PORT", 8001)
    }
)


async def trigger(sentiment):
    await VTS.connect()
    await VTS.request_authenticate_token()
    await VTS.request_authenticate()
    await VTS.request(VTS.vts_request.requestTriggerHotKey(sentiment))
    await VTS.close()


def run_trigger(senti):
    asyncio.run(trigger(senti))

run_trigger("Angry Sign")
time.sleep(10)
run_trigger("Angry Sign")