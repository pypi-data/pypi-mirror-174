import os
import toml, json
import websockets # not websocket!!!
import asyncio

from listen.STT import utils

HOST, PORT = "0.0.0.0", "5063"
CONFIG = utils.get_config_or_default()

if CONFIG.get('service'):
    HOST = CONFIG['service'].get('host', None)
    PORT = CONFIG['service'].get('port', None)

async def stt(audio_bin: bytes, host=HOST, port=PORT):
    async with websockets.connect(f"ws://{host}:{port}/api/v1/stt") as ws:
        try:
            await ws.send(audio_bin)
            r = json.loads(await ws.recv())
            if r.get('message'):
                return r.get('message')
            elif r.get('text'):
                return r.get('text')[0]
        except Exception as e:
            ws.close()
            raise e