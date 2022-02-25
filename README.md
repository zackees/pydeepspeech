
[![Actions Status](https://github.com/zackees/pydeepspeech/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/pydeepspeech/actions/workflows/push_macos.yml)
[![Actions Status](https://github.com/zackees/pydeepspeech/workflows/Win_Tests/badge.svg)](https://github.com/zackees/pydeepspeech/actions/workflows/push_win.yml)
[![Actions Status](https://github.com/zackees/pydeepspeech/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/pydeepspeech/actions/workflows/push_ubuntu.yml)


# pydeepspeech
  * The simpliest way to use AI to generate transcriptions from a wav file.
  * This project uses the Mozilla DeepSpeech engine built from the included demo:
    * https://github.com/mozilla/DeepSpeech-examples/tree/r0.9/vad_transcriber


# Quick start


Install to current python environment

Console api:
```
$ pip install pydeepspeech
$ pydeepspeech --wav_file <WAVE_FILE> --aggressive 1 --out_file <TEXT_FILE>
```

-or-

```
$ pydeepspeech --wav_file <WAVE_FILE> --out_file <TEXT_FILE> --model_dir <MY_PBMM_AND_SCORER_FILES>
```

-or-

```
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
python make_env.p  # Make the environment
source activate.sh  # Enter environment
pip install -e .
```
  
To get back into the environment execute `source activate.sh` (if windows, you must be using git-bash)


# Testing

Testing and linting is very simple. Just run `tox`
```
$ tox
```
