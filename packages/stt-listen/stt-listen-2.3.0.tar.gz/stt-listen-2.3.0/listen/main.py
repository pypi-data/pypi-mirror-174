import sys
import os
#import threading
import asyncio
import logging
import argparse
import subprocess
import shlex
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='Transcribe long audio files using webRTC VAD or use the streaming interface from a microphone')
    parser.add_argument('-v', '--version', action='store_true', help="shows the current version of listen")
    parser.add_argument('-f', '--file', required=False,
                        help='Path to the audio file to run (WAV format)')
    
    parser.add_argument('--aggressive', type=int, choices=range(4), required=False,
                        help='Determines how aggressive filtering out non-speech is. (Integer between 0-3)', default=2)
    
    #parser.add_argument('--model', required=True,
    #                    help='Path to directory that contains all models files (output_graph and scorer)')
    parser.add_argument('-d', '--mic_device', required=False, type=int, help="Device input index (Int) as listed by pyaudio.PyAudio.get_device_info_by_index(). If not provided, falls back to PyAudio.get_default_device().")
    parser.add_argument('-w', '--save_wav', required=False, default=None, type=str, help="Path to directory where to save recorded sentences")
    parser.add_argument("--debug", action='store_true', help="Show debug info")
    args = parser.parse_args()

    # Debug helpers
    loglevel = logging.DEBUG if args.debug is True else logging.ERROR
    logging.basicConfig(
        stream=sys.stderr,
        level=loglevel,
        format='%(asctime)s %(name)s %(levelname)-8s  %(message)s',
        datefmt='(%H:%M:%S)')
    # disable all loggers from different files
    logging.getLogger('asyncio').setLevel(logging.ERROR)
    logging.getLogger('asyncio.coroutines').setLevel(logging.ERROR)
    logging.getLogger('websockets.server').setLevel(logging.ERROR)
    logging.getLogger('websockets.protocol').setLevel(logging.ERROR)
    logging.getLogger('websockets.client').setLevel(logging.ERROR)

    if args.version:
        import datetime
        from listen import __version__ as ver
        from stt import version as stt_ver

        LICENCE_NAME = "GNU GPL v3"
        CURRENT_YEAR = str(datetime.date.today().year)

        print("Listen")
        print(f"Version: {ver}")
        print(f"Using STT version: {stt_ver()}")
        print(f"Licenced under: {LICENCE_NAME}")
        print(f"Copyright © {CURRENT_YEAR} - Danny Waser (Waser Technologies)")
        exit(0)

    if args.file is not None:
        from listen.STT import engine, audio, as_client
        logging.debug("Transcribing audio file @ %s" % args.file)

    if args.save_wav:
        logging.debug("Saving sentences audio to %s" % args.save_wav)
        os.makedirs(args.save_wav, exist_ok=True)

    if args.file:
        title_names = ['Filename', 'Duration(s)']
        print("\n%-30s %-20s" % (title_names[0], title_names[1]))

        #inference_time = 0.0

        # Run VAD on the input file
        waveFile = args.file
        segments, sample_rate, audio_length = audio.vad_segment_generator(waveFile, args.aggressive)
        f = open(waveFile.rstrip(".wav") + ".txt", 'w')
        logging.debug("Saving Transcript @: %s" % waveFile.rstrip(".wav") + ".txt")

        for i, segment in enumerate(segments):
            # Run stt on the chunk that just completed VAD
            logging.debug("Processing chunk %002d" % (i,))
            output = asyncio.run(as_client.stt(segment))
            #inference_time += output[1]
            if output:
                logging.debug("Transcript: %s" % output.capitalize())
                f.write(output + "\n")
            
            if args.save_wav and output:
                audio.write_wave(f"{args.save_wav}{waveFile.rstrip('.wav')}_{str(i)}.wav", audio_bin, sample_rate)

        # Summary of the files processed
        f.close()

        # Extract filename from the full file path
        filename, ext = os.path.split(os.path.basename(waveFile))
        logging.debug("************************************************************************************************************")
        logging.debug("%-30s %-20s" % (title_names[0], title_names[1]))
        logging.debug("%-30s %-20.3f" % (filename + ext, audio_length))
        logging.debug("************************************************************************************************************")
        print("%-30s %-20.3f" % (filename + ext, audio_length))
    else:
        from listen import mic
        source = mic.Microphone(aggressiveness=args.aggressive, device=args.mic_device, save_wav=args.save_wav)
        source.transcribe(forever=True)
        
               
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(1)
