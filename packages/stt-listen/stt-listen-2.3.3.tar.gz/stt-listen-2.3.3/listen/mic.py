# Code to listen to a mic and transcribe the stream.
import os, sys
import wave
import asyncio
import webrtcvad
import pyaudio
import numpy as np
import collections, queue, os

from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from scipy import signal
from prompt_toolkit.shortcuts import clear

from listen.STT import as_client


DEFAULT_SAMPLE_RATE = 16000

@contextmanager
def noalsaerr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)

class Audio(object):
    """Streams raw audio from microphone. Data is received in a separate thread, and stored in a buffer, to be read from."""

    FORMAT = pyaudio.paInt16
    # Network/VAD rate-space
    RATE_PROCESS = 16000
    CHANNELS = 1
    BLOCKS_PER_SECOND = 50

    def __init__(self, callback=None, device=None, input_rate=RATE_PROCESS, file=None):
        def proxy_callback(in_data, frame_count, time_info, status):
            #pylint: disable=unused-argument
            if self.chunk is not None:
                in_data = self.wf.readframes(self.chunk)
            callback(in_data)
            return (None, pyaudio.paContinue)
        if callback is None: callback = lambda in_data: self.buffer_queue.put(in_data)
        self.buffer_queue = queue.Queue()
        self.device = device
        self.input_rate = input_rate
        self.sample_rate = self.RATE_PROCESS
        self.block_size = int(self.RATE_PROCESS / float(self.BLOCKS_PER_SECOND))
        self.block_size_input = int(self.input_rate / float(self.BLOCKS_PER_SECOND))
        with noalsaerr():
            self.pa = pyaudio.PyAudio()

        kwargs = {
            'format': self.FORMAT,
            'channels': self.CHANNELS,
            'rate': self.input_rate,
            'input': True,
            'frames_per_buffer': self.block_size_input,
            'stream_callback': proxy_callback,
        }

        self.chunk = None
        # if not default device
        if self.device:
            kwargs['input_device_index'] = self.device
        elif file is not None:
            self.chunk = 320
            self.wf = wave.open(file, 'rb')
        try:
            with noalsaerr():
                self.stream = self.pa.open(**kwargs)
                self.stream.start_stream()
        except Exception as e:
            raise e

    def resample(self, data, input_rate):
        """
        Microphone may not support our native processing sampling rate, so
        resample from input_rate to RATE_PROCESS here for webrtcvad and
        stt

        Args:
            data (binary): Input audio stream
            input_rate (int): Input audio rate to resample from
        """
        data16 = np.frombuffer(buffer=data, dtype=np.int16)
        resample_size = int(len(data16) / self.input_rate * self.RATE_PROCESS)
        resample = signal.resample(data16, resample_size)
        resample16 = np.array(resample, dtype=np.int16)
        return resample16.tobytes()

    def read_resampled(self):
        """Return a block of audio data resampled to 16000hz, blocking if necessary."""
        try:
            return self.resample(data=self.buffer_queue.get(),
                             input_rate=self.input_rate)
        except KeyboardInterrupt:
            return

    def read(self):
        """Return a block of audio data, blocking if necessary."""
        try:
            return self.buffer_queue.get()
        except Exception as e:
            return
    
    def destroy(self):
        with noalsaerr():
            self.stream.stop_stream()
            self.stream.close()
            self.pa.terminate()

    frame_duration_ms = property(lambda self: 1000 * self.block_size // self.sample_rate)

    def write_wav(self, filename, data):
        #logging.info("write wav %s", filename)
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        # wf.setsampwidth(self.pa.get_sample_size(FORMAT))
        assert self.FORMAT == pyaudio.paInt16
        wf.setsampwidth(2)
        wf.setframerate(self.sample_rate)
        wf.writeframes(data)
        wf.close()


class VADAudio(Audio):
    """Filter & segment audio with voice activity detection."""

    def __init__(self, aggressiveness=3, device=None, input_rate=None, file=None):
        super().__init__(device=device, input_rate=input_rate, file=file)
        self.vad = webrtcvad.Vad(aggressiveness)

    def frame_generator(self):
        """Generator that yields all audio frames from microphone."""
        try:
            if self.input_rate == self.RATE_PROCESS:
                while True:
                    yield self.read()
            else:
                while True:
                    yield self.read_resampled()
        except (KeyboardInterrupt, Exception) as e:
            raise e
        

    def vad_collector(self, padding_ms=300, ratio=0.75, frames=None):
        """Generator that yields series of consecutive audio frames comprising each utterence, separated by yielding a single None.
            Determines voice activity by ratio of frames in padding_ms. Uses a buffer to include padding_ms prior to being triggered.
            Example: (frame, ..., frame, None, frame, ..., frame, None, ...)
                      |---utterence---|        |---utterence---|
        """
        if frames is None: frames = self.frame_generator()
        num_padding_frames = padding_ms // self.frame_duration_ms
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False
        try:
            for frame in frames:
                if len(frame) < 640:
                    return

                is_speech = self.vad.is_speech(frame, self.sample_rate)

                if not triggered:
                    ring_buffer.append((frame, is_speech))
                    num_voiced = len([f for f, speech in ring_buffer if speech])
                    if num_voiced > ratio * ring_buffer.maxlen:
                        triggered = True
                        for f, s in ring_buffer:
                            yield f
                        ring_buffer.clear()

                else:
                    yield frame
                    ring_buffer.append((frame, is_speech))
                    num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                    if num_unvoiced > ratio * ring_buffer.maxlen:
                        triggered = False
                        yield None
                        ring_buffer.clear()
        except TypeError:
            return
        except (KeyboardInterrupt, Exception) as e:
            raise e

class Microphone():
    aggressiveness = 1
    device = None
    input_rate = DEFAULT_SAMPLE_RATE
    save_wav = None

    transcript = [] #[str,] or str or None

    vad_audio = None
    frames = None
    buffer_data = wav_data = bytearray()

    def __init__(self, device=device, input_rate=input_rate, aggressiveness=aggressiveness, save_wav=save_wav):
        self.aggressiveness = aggressiveness
        self.device = device
        self.input_rate = input_rate
        self.save_wav = save_wav
        with noalsaerr():
            self.vad_audio = VADAudio(aggressiveness=self.aggressiveness, device=self.device, input_rate=self.input_rate)
    
    def transcribe(self, forever=False):
        self.transcript = []
        try:
            with noalsaerr():
                self.frames = self.vad_audio.vad_collector()
            self.buffer_data = self.wav_data = bytearray()
            print("You can speak now.")
            if not forever:
                return self.transcribe_until_silence()
            else:
                return self.transcribe_forever()
        # Ctrl + C to exit
        except (RuntimeError, KeyboardInterrupt, Exception) as e:
            sys.exit(1)
        finally:
            print()
            print("Stopped listening.")
    
    def transcribe_until_silence(self):
        try:
            for frame in self.frames:
                if frame is not None:
                    self.buffer_data.extend(frame)
                    #if self.save_wav: self.wav_data.extend(frame)
                else:
                    text = asyncio.run(as_client.stt(self.buffer_data))
                    if text:
                        self.transcript = text.capitalize()
                        print(text)
                        if self.save_wav:
                            f_path = os.path.join(self.save_wav, datetime.now().strftime("savewav_%Y-%m-%d_%H-%M-%S_%f.wav"))
                            self.vad_audio.write_wav(f_path, self.buffer_data)
                            #self.wav_data = bytearray()
                        return self.transcript
                    self.buffer_data = bytearray()
        # Ctrl + C to exit
        except (RuntimeError, KeyboardInterrupt, Exception) as e:
            raise e

    def transcribe_forever(self):
        try:
            for frame in self.frames:
                if frame is not None:
                    self.buffer_data.extend(frame)
                    #if self.save_wav: self.wav_data.extend(frame)
                else: # Frame is None
                    text = asyncio.run(as_client.stt(self.buffer_data))
                    if text:
                        t = text.capitalize()
                        print(t)
                        self.transcript.append(t)
                        if self.save_wav:
                            f_path = os.path.join(self.save_wav, datetime.now().strftime("savewav_%Y-%m-%d_%H-%M-%S_%f.wav"))
                            self.vad_audio.write_wav(f_path, self.buffer_data)
                            #self.wav_data = bytearray()
                    self.buffer_data = bytearray()
        # Ctrl + C to exit
        except (RuntimeError, KeyboardInterrupt, Exception) as e:
            raise e
        
        return self.transcript