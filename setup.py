import sys
import os

from shutil import rmtree
from setuptools import find_packages, setup, Command

# The directory containing this file
HERE = os.path.dirname(__file__)

NAME = 'pydeepspeech'
DESCRIPTION = "Mozilla's DeepSpeech transcriber in a pip installable package."
URL = 'https://github.com/zackees/pydeepspeech'
EMAIL = 'dont@email.me'
AUTHOR = 'Zach Vorhies'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.1'

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fd:
    README = fd.read()

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        pass

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')

        sys.exit()


# This call to setup() does all the work
setup(
    name=NAME,
    python_requires=REQUIRES_PYTHON,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        'deepspeech==0.9.3',
        'webrtcvad',
        'pyqt5',
        'pathlib',
        'capturing_process',
        'requests',
    ],

    entry_points = {
        'console_scripts': [
            'pydeepspeech = pydeepspeech.run:main',
        ],              
    },
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    extras_require={},
    cmdclass={
        'upload': UploadCommand,
    },
)