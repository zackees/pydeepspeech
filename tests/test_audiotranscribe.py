import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from io import StringIO

import requests

from pydeepspeech.install_models import MODEL_DIR  # pylint: disable=import-error

_URL_WAV_DATA = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/audio-0.9.3.tar.gz"


def download_tar_gz(url, out_dir) -> None:
    # NOTE the stream=True parameter below
    tmp = None
    try:
        os.makedirs(out_dir, exist_ok=True)
        tmp = os.path.join(out_dir, "tmp.tar.gz")
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
        prev_cwd = os.getcwd()
        os.chdir(out_dir)
        with tarfile.open(tmp) as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar)
        os.chdir(prev_cwd)
    except KeyboardInterrupt:
        print(f"Aborted download of {url}")
        return
    finally:
        if tmp:
            os.remove(tmp)


class PyDeepSpeechTester(unittest.TestCase):
    def test_download_and_run_audio_files(self):
        print(f"MODEL_DIR: {MODEL_DIR}")
        out_dir = os.path.join(MODEL_DIR, "test_audiotranscribe")
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        download_tar_gz(_URL_WAV_DATA, out_dir)
        wav_files = []
        for root, _, files in os.walk(out_dir, topdown=False):
            for name in files:
                if ".wav" in name and "." != name[0]:
                    wav_files.append(os.path.join(root, name))
        for wav in wav_files:
            print(wav)
            cmd = f"pydeepspeech --wav_file {wav}"
            subprocess.check_output(cmd, shell=True)
            self.assertTrue(os.path.exists(wav[:-4] + ".txt"))
            os.remove(wav[:-4] + ".txt")

    def test_pydeepspeech_installmodels(self):
        self.assertEqual(0, os.system("pydeepspeech_installmodels --help"))


if __name__ == "__main__":
    unittest.main()
