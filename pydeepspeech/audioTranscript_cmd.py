import sys
import logging
import argparse

from pydeepspeech.transcribe import transcribe

# Debug helpers
logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)


def main(args):
    parser = argparse.ArgumentParser(description='Transcribe long audio files using webRTC VAD or use the streaming interface')
    parser.add_argument('--aggressive', type=int, choices=range(4), required=False,
                        help='Determines how aggressive filtering out non-speech is. (Interger between 0-3)')
    parser.add_argument('--audio', required=False,
                        help='Path to the audio file to run (WAV format)')
    parser.add_argument('--model', required=True,
                        help='Path to directory that contains all model files (output_graph and scorer)')
    args = parser.parse_args(args)
    if args.audio is not None:
        logging.debug("Transcribing audio file @ %s" % args.audio)
    else:
        parser.print_help()
        parser.exit()
    transcribe(args.aggressive, args.audio, args.model)



if __name__ == '__main__':
    main(sys.argv[1:])
