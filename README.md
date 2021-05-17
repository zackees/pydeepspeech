
[![Actions Status](https://github.com/zackees/pydeepspeech/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/pydeepspeech/actions/workflows/push_macos.yml)
[![Actions Status](https://github.com/zackees/pydeepspeech/workflows/Win_Tests/badge.svg)](https://github.com/zackees/pydeepspeech/actions/workflows/push_win.yml)
[![Actions Status](https://github.com/zackees/pydeepspeech/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/pydeepspeech/actions/workflows/push_ubuntu.yml)


# pydeepspeech
  * The simpliest way to use AI to generate transcriptions from a wav file.
  * This project uses the Mozilla DeepSpeech engine built from the included demo:
    * https://github.com/mozilla/DeepSpeech-examples/tree/r0.9/vad_transcriber


# Quick start

## Optional: Create a virtual python package
  * Works for Ubuntu/MacOS bash or win32 git-bash
  * `mkdir pydeepspeech`
  * `cd pydeepspeech`
  * Download and install virtual env:
    * `curl -X GET https://raw.githubusercontent.com/zackees/make_venv/main/make_venv.py -o make_env.py`
    * `python make_env.py`
  * Enter the environment:
    * `source activate.sh`
  * Continue on in the next step...

The environment is now active and the next step will only install to the local python. If the terminal
is closed then to get back into the environment `cd pydeepspeech` and execute `source activate.sh`

## Required: Install to current python environment
  * `pip install pydeepspeech`
    * The command `pydeepspeech` will magically become available.
  * `pydeepspeech --wav_file <MY_WAVE>`
  