
[![Actions Status](https://github.com/zackees/pydeepspeech/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/pydeepspeech/actions/workflows/push_macos.yml)
[![Actions Status](https://github.com/zackees/pydeepspeech/workflows/Win_Tests/badge.svg)](https://github.com/zackees/pydeepspeech/actions/workflows/push_win.yml)
[![Actions Status](https://github.com/zackees/pydeepspeech/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/pydeepspeech/actions/workflows/push_ubuntu.yml)


# pydeepspeech

  * The simpliest way to use AI to generate transcriptions from a wav file.
  * This project uses the Mozilla DeepSpeech engine built from the included demo:
    * https://github.com/mozilla/DeepSpeech-examples/tree/r0.9/vad_transcriber

## Why you need this

Mozilla's deep speech can't process long voice samples. `pydeepspeech` fixes this by "chunking" the input sound into seperate wav files that are then individualy processed. Wav files are cut along periods of detected silence, controlled by the `aggressive` parameter.

Besides this, `pydeepspeech` is probably better to use anyway because it's *much* simpler to install than Mozilla's Deepspeech because the required data models needed for `pydeepspeech` are automatically downloaded and installed on first use.


# Quick start

Console api:
```
$ pip install pydeepspeech
$ pydeepspeech --wav_file <WAVE_FILE> --aggressive 1 --out_file <TEXT_FILE>
```

-or-

```
$ pip install pydeepspeech
$ pydeepspeech --wav_file <WAVE_FILE> --out_file <TEXT_FILE> --model_dir <MY_PBMM_AND_SCORER_FILES>
```

-or-

```
$ pip install pydeepspeech
$ pydeepspeech_installmodels --pbmm <PBMM_FILE_OR_URL> --scorer <SCORER_FILE_OR_URL>
$ pydeepspeech --wav_file <WAVE_FILE> --out_file <TEXT_FILE>
```

Or in python
```
from pydeepspeech.transcribe import transcribe
transcribe(...)
```


## Optional: Create a virtual python package

Download and install virtual env:

```
# Download
curl -X GET https://raw.githubusercontent.com/zackees/make_venv/main/make_venv.py -o make_env.py
python make_env.py  # Make the environment
source activate.sh  # Enter environment
$ pip install pydeepspeech
```
  
To get back into the environment execute `source activate.sh` (if windows, you must be using git-bash)


# Testing

Testing and linting is very simple. Just run `tox` ([link](https://tox.wiki/en/latest/install.html)).
```
$ pip install tox
$ tox
```
