#!/usr/bin/env python
import os
from setuptools import setup, find_packages
import listen

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()


setup(
    name='stt-listen',
    author='Danny Waser',
    version=listen.__version__,
    license='LICENSE',
    url='https://gitlab.com/waser-technologies/technologies/dmt',
    description='Transcribe long audio files with STT or use the streaming interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('.'),
    python_requires='>=3.8,<3.11',
    install_requires = [
        'coqui_stt_model_manager>=0.0.21',
        'numpy>=1.15.1',
        'pyaudio~=0.2.12',
        'webrtcvad~=2.0.10',
        'scipy>=1.1.0',
        'prompt_toolkit>=2.0.0,<3.1.0',
        'toml~=0.10.2',
        'sanic~=22.6.0',
        'ffmpeg-python~=0.2.0',
        'websockets~=10.3',
        'deepmultilingualpunctuation',
    ],
    entry_points={
        'console_scripts': [
            'listen = listen.main:main',
        ]
    },
)
