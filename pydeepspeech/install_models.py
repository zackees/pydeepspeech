# type: ignore

import os
import shutil
import threading
from pathlib import Path
from typing import Optional

import requests

from pydeepspeech.util import get_appdatadir

# AI model used for the application
_VERSION = "v0.9.3"

URL_PBMM = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm"

URL_SCORER = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer"

MODEL_DIR = os.path.join(get_appdatadir(), "model", _VERSION)
# Marks the model created.
IS_FINISHED_STAMP = os.path.join(MODEL_DIR, "is_finished")


def download_file(url, outfile) -> None:
    if os.path.isfile(url):
        # Actually it's a file, so we can just copy it.
        shutil.copyfile(url, outfile)
        return
    # NOTE the stream=True parameter below
    try:
        tmp = f"{outfile}.tmp"
        if os.path.exists(tmp):
            os.remove(tmp)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
        os.rename(tmp, outfile)
    except KeyboardInterrupt:
        print(f"Aborted download of {url}")
        return


def url_to_local_name(url: str) -> str:
    return os.path.join(MODEL_DIR, url.split("/")[-1])


def is_models_installed() -> bool:
    return os.path.exists(IS_FINISHED_STAMP)


def clean_dir(path: str) -> None:
    """
    Removes all files in the directory.
    """
    if not os.path.exists(path):
        return
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.path.isfile(f):
            os.remove(f)


def install_deepspeechmodules(
    url_pbmm: Optional[str] = None,
    url_scorer: Optional[str] = None,
) -> None:
    url_pbmm = url_pbmm or URL_PBMM
    url_scorer = url_scorer or URL_SCORER
    os.makedirs(MODEL_DIR, exist_ok=True)
    clean_dir(MODEL_DIR)
    threads = {}
    url_pbmm = url_pbmm or URL_PBMM
    url_scorer = url_scorer or URL_SCORER
    print(
        "Downloading and installing the models for the first time. This may take a while."
    )
    for url in [url_pbmm, url_scorer]:
        local_filename = url_to_local_name(url)
        t = threading.Thread(target=download_file, args=(url, local_filename))
        print(f"Downloading {url} -> {local_filename}")
        threads[url] = t
        t.daemon = True
        t.start()
    for url, t in threads.items():
        while t.is_alive():  # allows keyboard interrupt.
            t.join(0.2)
        print(f"Finished downloading {url}")
    Path(IS_FINISHED_STAMP).touch()


def install_dependencies_if_necessary() -> str:  # pylint: disable=invalid-name
    print(f"Model directory is: {MODEL_DIR}")
    if not is_models_installed():
        install_deepspeechmodules(url_pbmm=URL_PBMM, url_scorer=URL_SCORER)
    return MODEL_DIR


if __name__ == "__main__":
    install_dependencies_if_necessary()
