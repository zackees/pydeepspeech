

import os
import sys
import threading
from typing import Any
from pathlib import Path

import subprocess
import requests
import shutil

from pydeepspeech.util import get_appdatadir

_VERSION = 'v0.9.3'
_URLS = [
    'https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm',
    'https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer',
]

MODEL_DIR = get_appdatadir() / 'model' / _VERSION
# Marks the model created.
IS_FINISHED_STAMP = os.path.join(MODEL_DIR, 'is_finished')

def download_file(url, outfile) -> None:
    # NOTE the stream=True parameter below
    try:
        tmp = f'{outfile}.tmp'
        if os.path.exists(tmp):
            os.remove(tmp)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(tmp, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)
        shutil.move(tmp, outfile)
    except KeyboardInterrupt:
        print(f'Aborted download of {url}')
        return

def url_to_local_name(url: str) -> str:
    return os.path.join(MODEL_DIR, url.split('/')[-1])

def installModels() -> None:
    os.makedirs(MODEL_DIR, exist_ok=True)
    threads = {}
    if os.path.exists(IS_FINISHED_STAMP):
        return
    print('Downloading and installing the models for the first time. This may take a while.')
    for url in _URLS:
        local_filename = url_to_local_name(url)
        t = threading.Thread(
            target=download_file, args=(url, local_filename))
        print(f'Downloading {url} -> {local_filename}')
        threads[url] = t
        t.daemon = True
        t.start()
    for url, t in threads.items():
        while t.is_alive():  # allows keyboard interrupt.
            t.join(.2)
        print(f'Finished downloading {url}')    
    Path(IS_FINISHED_STAMP).touch()

def installModelsIfNecessary() -> str:
    print(f'Model directory is: {MODEL_DIR}')
    installModels()
    return MODEL_DIR

if __name__ == '__main__':
    installModelsIfNecessary()
