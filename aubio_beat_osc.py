import pyaudio
import numpy as np
import aubio
import signal
import os
import time

import argparse

from pythonosc.udp_client import SimpleUDPClient

from typing import List, NamedTuple, Tuple


class ClientInfo(NamedTuple):
    ip: str
    port: int
    address: str


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--client", help="OSC Client address (multiple can be provided)", nargs=3, action="append",
                    metavar=("IP", "PORT", "ADDRESS"), required=True)
parser.add_argument("-b", "--bufsize", help="Size of audio buffer for beat detection (default: 128)", default=128,
                    type=int)
parser.add_argument("-v", "--verbose", help="Print BPM on beat", action="store_true")
args = parser.parse_args()

# Pack data from arguments into ClientInfo objects
client_infos: List[ClientInfo] = [ClientInfo(x[0], int(x[1]), x[2]) for x in args.client]


class BeatPrinter:
    def __init__(self):
        self.state: int = 0
        self.spinner = "▚▞"

    def print_bpm(self, bpm: float) -> None:
        print(f"{self.spinner[self.state]}\t{bpm:.1f} BPM")
        self.state = (self.state + 1) % len(self.spinner)


class BeatDetector:
    def __init__(self, buf_size: int, client_infos: List[ClientInfo]):
        self.buf_size: int = buf_size
        self.client_infos: List[ClientInfo] = client_infos

        # Set up pyaudio and aubio beat detector
        self.p: pyaudio.PyAudio = pyaudio.PyAudio()
        samplerate: int = 44100
        self.stream: pyaudio.Stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=samplerate,
            input=True,
            frames_per_buffer=self.buf_size,
            stream_callback=self._pyaudio_callback
        )

        fft_size: int = self.buf_size * 2
        self.tempo: aubio.tempo = aubio.tempo("default", fft_size, self.buf_size, samplerate)

        # Set up OSC clients to send beat data to
        self.osc_clients: List[Tuple[SimpleUDPClient, str]] = [(SimpleUDPClient(x.ip, x.port), x.address) for x in
                                                               self.client_infos]

        self.spinner: BeatPrinter = BeatPrinter()

    def _pyaudio_callback(self, in_data, frame_count, time_info, status):
        signal = np.frombuffer(in_data, dtype=np.float32)
        beat = self.tempo(signal)
        if beat[0]:
            if args.verbose:
                self.spinner.print_bpm(self.tempo.get_bpm())
            for client in self.osc_clients:
                client[0].send_message(client[1], self.tempo.get_bpm())

        return None, pyaudio.paContinue  # Tell pyAudio to continue

    def __del__(self):
        self.stream.close()
        self.p.terminate()


def main():
    bd = BeatDetector(args.bufsize, client_infos)
    
    # Audio processing happens in separate thread, so put this thread to sleep
    if os.name == 'nt': # Windows is not able to pause the main thread :(
        while True:
            time.sleep(1)
    else:
        signal.pause()


if __name__ == "__main__":
    main()
