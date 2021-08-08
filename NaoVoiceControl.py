import struct
import sys
from threading import Thread

import pyaudio
from picovoice import Picovoice

from Nao import Nao


class NaoVoiceControl(Thread):

    def __init__(self, keyword_path, context_path):
        super(NaoVoiceControl, self).__init__()
        self.robot = Nao()

        self.pv = Picovoice(
            keyword_path=keyword_path,
            wake_word_callback=self.wake_word_callback,
            context_path=context_path,
            inference_callback=self.inference_callback)

    def wake_word_callback(self):
        print("Received Voice activation")

    def inference_callback(self, inference):
        self.robot.handle_callback(inference)

    def run(self):
        py_audio = None
        audio_stream = None
        print('Starting to listen to commands ...')
        try:
            py_audio = pyaudio.PyAudio()
            audio_stream = py_audio.open(
                rate=self.pv.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.pv.frame_length)
            while True:
                pcm = audio_stream.read(self.pv.frame_length)
                pcm = struct.unpack_from("h" * self.pv.frame_length, pcm)
                self.pv.process(pcm)
        except KeyboardInterrupt:
            sys.stdout.write('\b' * 2)
            print('Stopping ...')
        finally:
            if audio_stream is not None:
                audio_stream.close()

            if py_audio is not None:
                py_audio.terminate()
            self.pv.delete()
