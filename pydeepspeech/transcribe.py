import logging
import os
import shlex
import subprocess

import numpy as np  # pylint: disable=import-error

import pydeepspeech.wav_transcriber as wav_transcriber


def transcribe(aggressive, audio, model):
    # Point to a path containing the pre-trained models & resolve ~ if used
    dir_name = os.path.expanduser(model)

    # Resolve all the paths of model files
    output_graph, scorer = wav_transcriber.resolve_models(dir_name)

    # Load output_graph, alpahbet and scorer
    model_retval = wav_transcriber.load_model(output_graph, scorer)

    if audio is not None:
        title_names = [
            "Filename",
            "Duration(s)",
            "Inference Time(s)",
            "Model Load Time(s)",
            "Scorer Load Time(s)",
        ]
        print(
            "\n%-30s %-20s %-20s %-20s %s"
            % (
                title_names[0],
                title_names[1],
                title_names[2],
                title_names[3],
                title_names[4],
            )
        )

        inference_time = 0.0

        # Run VAD on the input file
        wave_file = audio
        (
            segments,
            sample_rate,
            audio_length,
        ) = wav_transcriber.vad_segment_generator(wave_file, aggressive)
        f = open(wave_file.rstrip(".wav") + ".txt", "w")
        logging.debug("Saving Transcript @: %s" % wave_file.rstrip(".wav") + ".txt")

        for i, segment in enumerate(segments):
            # Run deepspeech on the chunk that just completed VAD
            logging.debug("Processing chunk %002d" % (i,))
            audio = np.frombuffer(segment, dtype=np.int16)
            output = wav_transcriber.stt(model_retval[0], audio, sample_rate)
            inference_time += output[1]
            logging.debug("Transcript: %s" % output[0])

            f.write(output[0] + " ")

        # Summary of the files processed
        f.close()

        # Extract filename from the full file path
        filename, ext = os.path.split(os.path.basename(wave_file))
        logging.debug(
            "************************************************************************************************************"
        )
        logging.debug(
            "%-30s %-20s %-20s %-20s %s"
            % (
                title_names[0],
                title_names[1],
                title_names[2],
                title_names[3],
                title_names[4],
            )
        )
        logging.debug(
            "%-30s %-20.3f %-20.3f %-20.3f %-0.3f"
            % (
                filename + ext,
                audio_length,
                inference_time,
                model_retval[1],
                model_retval[2],
            )
        )
        logging.debug(
            "************************************************************************************************************"
        )
        print(
            "%-30s %-20.3f %-20.3f %-20.3f %-0.3f"
            % (
                filename + ext,
                audio_length,
                inference_time,
                model_retval[1],
                model_retval[2],
            )
        )
    else:
        sctx = model_retval[0].createStream()
        subproc = subprocess.Popen(
            shlex.split("rec -q -V0 -e signed -L -c 1 -b 16 -r 16k -t raw - gain -2"),
            stdout=subprocess.PIPE,
            bufsize=0,
        )
        print("You can start speaking now. Press Control-C to stop recording.")

        try:
            while True:
                data = subproc.stdout.read(512)
                sctx.feedAudioContent(np.frombuffer(data, np.int16))
        except KeyboardInterrupt:
            print("Transcription: ", sctx.finishStream())
            subproc.terminate()
            subproc.wait()
