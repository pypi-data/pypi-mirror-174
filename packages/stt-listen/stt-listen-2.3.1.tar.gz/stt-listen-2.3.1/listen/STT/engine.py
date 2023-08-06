import os
import glob
import logging

import numpy as np
from stt import Model
from timeit import default_timer as timer
from deepmultilingualpunctuation import PunctuationModel

from listen.STT import audio, utils

'''
Load the pre-trained model into the memory
@param models: TFLite file
@param scorer: Scorer file
@Retval
Returns a list [STT Model, Model Load Time, Scorer Load Time]
'''
def load_model(models, scorer):
    model_load_start = timer()
    stt = Model(models)
    model_load_end = timer() - model_load_start
    logging.debug("Loaded model in %0.3fs." % (model_load_end))

    scorer_load_start = timer()
    stt.enableExternalScorer(scorer)
    scorer_load_end = timer() - scorer_load_start
    logging.debug('Loaded external scorer in %0.3fs.' % (scorer_load_end))

    return [stt, model_load_end, scorer_load_end]


'''
Resolve directory path for the models and fetch each of them.
@param dirName: Path to the directory containing pre-trained models
@Retval:
Returns a tuple containing each of the model files (tf, scorer)
'''
def resolve_models(dirName):
    try:
        tf = glob.glob(dirName + "/*.tflite")[0]
        logging.debug("Found Model: %s" % tf)
    except IndexError:
        tf = None
        logging.debug(f"Not found any output graph")

    try:
        scorer = glob.glob(dirName + "/*.scorer")[0]
        logging.debug("Found scorer: %s" % scorer)
    except IndexError:
        scorer = None
        logging.debug(f"Not found any scorer")
    
    return tf, scorer


class STT:

    def __init__(self, models_path):
        abs_models_path = os.path.expanduser(models_path)
        self.output_graph, self.scorer = resolve_models(abs_models_path)
        self.model, _, _  = load_model(self.output_graph, self.scorer)
        self.punct_model = PunctuationModel(model="oliverguhr/fullstop-punctuation-multilingual-sonar-base")
    
    def punctuate(self, sentence: str):
        return self.punct_model.restore_punctuation(sentence).capitalize()

    '''
    Run Inference on input audio
    @param models: STT Model object
    @param audio: Input audio for running inference on
    @param fs: Sample rate of the input audio file
    @Retval:
    Returns a list [Inference, Inference Time]
    '''
    def stt(self, audio_bin, fs):
        inference_time = 0.0
        audio_length = len(audio_bin) * (1 / fs)

        # Run STT
        logging.debug('Running inference...')
        inference_start = timer()
        output = self.model.stt(audio_bin)
        inference_end = timer() - inference_start
        inference_time += inference_end
        logging.debug('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))
        if output:
            logging.debug('Punctuating sentence...')
            inference_start = timer()
            output = self.punctuate(output)
            inference_end = timer() - inference_start
            inference_time += inference_end
            logging.debug('Punctuation took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))
        logging.debug(f'Inference: {output}')
        
        return [output, inference_time]

    def run(self, audio_bin):
        #pcm, sample_rate, duration = audio.read_wave(audio_bin)
        audio_bin = np.frombuffer(audio_bin, np.int16)
        return self.stt(audio_bin, 16_000)

class Response:
    def __init__(self, text, time):
        self.text = text
        self.time = time


class Error:
    def __init__(self, message):
        self.message = message