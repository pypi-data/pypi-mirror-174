# Listen: STT Services

This program is composed of two parts:
- A server aimed to be runned as a background service to serve STT models within the bounds of a socket.
- A client to query the models to transcribe audio from files or directly from a live microphone stream.


The outputed wav file can be stored for later use.

You can then use the `data.helper` script to verify the transcription of every wav file and update the CSV training register before you start training a model.

## Requirements

If you intent to use `listen` using Python 3.10 or above, you'll need my patched version of `PyAudio` for Python 3.10.

```
pip install git+https://gitlab.com/waser-technologies/technologies/pyaudio.git
```

## Installation

Once you have a working `pyaudio` for your version of python, install `listen`.

```zsh
pip install stt-listen
# Or from source
pip install git+https://gitlab.com/waser-technologies/technologies/listen.git
```

## Usage

```zsh
❯ listen --help
usage: listen [-h] [-f FILE] [--aggressive {0,1,2,3}] [-d MIC_DEVICE]
                   [-w SAVE_WAV]

Transcribe long audio files using webRTC VAD or use the streaming interface
from a microphone

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the audio file to run (WAV format)
  --aggressive {0,1,2,3}
                        Determines how aggressive filtering out non-speech is.
                        (Integer between 0-3)
  -d MIC_DEVICE, --mic_device MIC_DEVICE
                        Device input index (Int) as listed by
                        pyaudio.PyAudio.get_device_info_by_index(). If not
                        provided, falls back to PyAudio.get_default_device().
  -w SAVE_WAV, --save_wav SAVE_WAV
                        Path to directory where to save recorded sentences
  --debug               Show debug info
```

## Start the server

To use `listen`, you need a socket with STT models at the ready.

Example to enable as service.
```zsh
cp ./listen.service.example /usr/lib/systemd/user/listen.service
systemctl --user enable --now listen.service
```

Models for STT and punctuation will be downloaded the first time your run the server.

Or manually using python

```zsh
python -m listen.STT.as_service
```

### Get authorization to listen

You need to authorize the system to listen first. Change the service configuration as follows.

```toml
# ~/.assistant/stt.toml
...
[stt]
is_allowed = true
...
```

Then [start the server](#start-the-server) and use `listen` to start [transcribing audio](#use-the-client).

## Use the client

### Transcribe a file

You can quickly transcribe a wav file.
```zsh
❯ listen -f savewav_2022-04-11_17-18-08_578756.wav
Filename                       Duration(s)         
savewav_2022-04-11_17-18-08_578756.wav 3.580               

❯ cat savewav_2022-04-11_17-18-08_578756.txt
───────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: savewav_2022-04-11_17-18-08_578756.txt
───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ Bonjour.
───────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

### Transcribe from a live microphone stream

You can also query the models in real time from a microphone.

```zsh
❯ listen
You can speak now.
Bonjour.
^C
Stopped listening.
```

## Supported languages

By default, the server uses the system's language according to the environment variable `$LANG`.

You can manually specify a supported language for the server to use.

```zsh
LANG="en_US.UTF-8" python -m listen.STT.as_service
```

Have a look at [stt-models-locals](https://github.com/wasertech/stt-models-locals#languages) to see the complete list.

If the provided `$LANG` is not supported by any STT model, english is used as a failback.
