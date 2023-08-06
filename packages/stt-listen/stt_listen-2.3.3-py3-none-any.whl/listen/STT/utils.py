import os
import re
import json
import toml
import logging
import threading

from pathlib import Path
from urllib import request
from time import sleep
#from typing import List, Optional, Dict


from coqui_stt_model_manager.modelmanager import ModelCard, ModelManager

logging.basicConfig(level=logging.INFO)

I18N, L10N = (x for x in os.environ.get('LANG', "en_EN.UTF-8").split(".")[0].split("_"))

USERNAME = os.environ.get("USERNAME", 'root')
ASSISTANT_PATH = f"/home/{USERNAME}/.assistant" if USERNAME != "root" else "/usr/share/assistant"
CONFIG_PATH = f"{ASSISTANT_PATH}/stt.toml"


MODELS_URL = "https://raw.githubusercontent.com/wasertech/stt-models-locals/main/models.json"

manager = ModelManager()

# custom exception hook
def custom_hook(args):
    # report the failure
    logging.error(f'Thread failed: {args.exc_value}')

# set the exception hook
threading.excepthook = custom_hook

def get_config_or_default():
    # Check if conf exist

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as cfg:
            CONFIG = toml.loads(cfg.read())
    else:
        CONFIG = {
            'service': {
                'host': '0.0.0.0',
                'port': '5063',
                'n_proc': 2
            },
            'stt': {
                'is_allowed': False
            }
        }
        with open(CONFIG_PATH, 'w') as f:
            f.write(toml.dumps(CONFIG))
    
    return CONFIG

def is_allowed_to_listen(conf=get_config_or_default()):
    _stt_conf = conf.get('stt', False)
    if _stt_conf:
        return _stt_conf.get('is_allowed', False)
    return False

def fetch_stt_models():
    """
    Fetches model cards and local pointers for available STT models
    Checkout  https://github.com/wasertech/stt-models-locals
    """
    r = request.urlopen(MODELS_URL)
    rb = r.read()
    return json.loads(rb.decode('utf-8'))

def get_loc_model_path(language=None):
    """
    Get localised model path.
    Returns the path to the STT model of the choosen language.
    [Default] language: System language
    """
    custom_models_localized_path=f"{ASSISTANT_PATH}/models/{I18N}/STT"
    if os.path.isfile(f"{custom_models_localized_path}/output_graph.tflite") and os.path.isfile(f"{custom_models_localized_path}/kenlm.scorer"):
        logging.debug(f"Models: (Custom) {I18N} for {USERNAME} by {USERNAME}")
        return custom_models_localized_path
    elif not manager.install_dir.exists():
        manager.mkdir(parents=True, exist_ok=True)

    loc_models = fetch_stt_models()
    model_name = None
    
    if loc_models:
        model_lang = loc_models['locals'].get(
            f'{language}', # first we try with given language 
            loc_models['locals'].get(
                f'{I18N}', # or with system $LANG
                loc_models['locals'].get(
                    'en', # else failback to english
                    None
                    )
                )
            )
    
    if model_lang:
        logging.debug(f"Language: {model_lang}")
        _models_dict = loc_models.get('models')
        model_name = _models_dict[f'{model_lang}'].get('name')
    
    if model_name:
        logging.debug(f"Models: {model_name}")
        models_dict = manager.models_dict()
        model_card = models_dict.get(f'{model_name}', None)
        if model_card:
            is_model_installed = bool(model_card.get('installed', False))
        else:
            is_model_installed = False
        
        if is_model_installed:
            logging.debug("Models are installed")
            accoustic_path = model_card.get('acoustic_path', None)
        else:
            logging.debug("Models are not installed")
            logging.debug("Installing now...")
            download_task_id = manager.download_model(_models_dict[f"{model_lang}"])

            while manager.has_install_task_state(download_task_id):
                ts = manager.get_install_task_state(download_task_id).to_dict()
                logging.debug("-"*10)
                logging.debug(f"Downloading: {model_name}")
                logging.debug(f"Acoustic model: {ts.get('acoustic_progress')} %")
                logging.debug(f"Scorer: {ts.get('scorer_progress')} %")
                logging.debug(f"Total ({ts.get('step', 0)}/{ts.get('total_steps')}): {ts.get('total_progress')} %")
                logging.debug("-"*10)
                if int(ts.get('total_progress')) == 100:
                    break
                else:
                    sleep(10)
            
            models_dict = manager.models_dict()
            if models_dict:
                model_card = models_dict.get(f'{model_name}', None)
            if model_card:
                is_model_installed = bool(model_card.get('installed', False))
                accoustic_path = model_card.get('acoustic_path', None)
            else:
                is_model_installed = False
                accoustic_path = None
            
        if is_model_installed and accoustic_path:
            model_path = Path(accoustic_path).parent
            return model_path

    return None

def get_available_cpu_count():
    """Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program
    See this https://stackoverflow.com/a/1006301/13561390"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r"(?m)^Cpus_allowed:\s*(.*)$", open("/proc/self/status").read())
        if m:
            res = bin(int(m.group(1).replace(",", ""), 16)).count("1")
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing

        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # https://github.com/giampaolo/psutil
    try:
        import psutil

        return psutil.cpu_count()  # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass

    # POSIX
    try:
        res = int(os.sysconf("SC_NPROCESSORS_ONLN"))

        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ["NUMBER_OF_PROCESSORS"])

        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime

        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(["sysctl", "-n", "hw.ncpu"], stdout=subprocess.PIPE)
        scStdout = sysctl.communicate()[0]
        res = int(scStdout)

        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open("/proc/cpuinfo").read().count("processor\t:")

        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudoDevices = os.listdir("/devices/pseudo/")
        res = 0
        for pd in pseudoDevices:
            if re.match(r"^cpuid@[0-9]+$", pd):
                res += 1

        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open("/var/run/dmesg.boot").read()
        except IOError:
            dmesgProcess = subprocess.Popen(["dmesg"], stdout=subprocess.PIPE)
            dmesg = dmesgProcess.communicate()[0]

        res = 0
        while "\ncpu" + str(res) + ":" in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    raise Exception("Can not determine number of CPUs on this system")

