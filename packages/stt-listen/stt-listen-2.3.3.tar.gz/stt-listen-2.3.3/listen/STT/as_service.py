import os
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import perf_counter
import toml
from sanic import Sanic, response
from sanic.log import logger

from listen.STT.engine import STT, Response, Error
from listen.STT import utils
from listen.STT.exception import NotAllowedToListenError

# Check if conf exist
CONFIG = utils.get_config_or_default()

is_allowed_to_listen = utils.is_allowed_to_listen(CONFIG)
            
if not is_allowed_to_listen:
    raise NotAllowedToListenError(utils.CONFIG_PATH)

# Load app configs and initialize STT model

models_path = utils.get_loc_model_path()

try:
    n_proc_available = CONFIG['service']['n_proc'] or utils.get_available_cpu_count()
except Exception as e:
    print(e)
    print("Using 2 instead.")
    n_proc_available = 2

engine = STT(
    models_path=Path(models_path).absolute().as_posix(),
)

# Initialze Sanic and ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=n_proc_available)
app = Sanic("stt_service")


@app.route("/", methods=["GET"])
async def healthcheck(_):
    return response.text("Welcome to listen.sock: STT as a Service!")


@app.websocket("/api/v1/stt")
async def stt(request, ws):
    logger.debug(f"Received {request.method} request at {request.path}")
    try:
        audio_bin = await ws.recv()

        inference_start = perf_counter()
        text = await app.loop.run_in_executor(executor, lambda: engine.run(audio_bin))
        inference_end = perf_counter() - inference_start

        await ws.send(json.dumps(Response(text, inference_end).__dict__))
        logger.debug(f"Completed {request.method} request at {request.path} in {inference_end} seconds")
    except Exception as e:  # pylint: disable=broad-except
        logger.debug(f"Failed to process {request.method} request at {request.path}. The exception is: {str(e)}.")
        await ws.send(json.dumps(Error("Something went wrong").__dict__))
        raise e

    await ws.close()


if __name__ == "__main__":
    app.run(
        host=CONFIG["service"]["host"],
        port=CONFIG["service"]["port"],
        access_log=True,
        debug=True,
    )