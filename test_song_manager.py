import unittest
import numpy as np
from song_manager import Song
from io_manager import setuplogger
import wave, struct


class TestIoManager(unittest.TestCase):
    def setUp(self):
        self.sine_signal = []
        waveFile = wave.open('./test_audio/sine.wav', 'r')
        length = waveFile.getnframes()
        for i in range(0,length):
            waveData = waveFile.readframes(1)
            data = struct.unpack("<h", waveData)
            self.sine_signal.append((int(data[0])))

    # test the read signal function of song class
    # other core functions such as computing spectrograms
    # and signatures are already tested in test_spectral_analysis.py 
    def test_convert_file_to_signal(self):
        logger = setuplogger(False, "./log/test_log")
        song = Song("test", "unknown", "sine.wav", "./test_audio/sine.wav", logger)
        song.get_signal()
        self.assertEqual(song.sample_rate, 44100)
        self.assertTrue(song.signal.tolist() == self.sine_signal)

    # test reading in mp3 format audio file
    def test_convert_mp3_to_signal(self):
        logger = setuplogger(False, "./log/test_log")
        song = Song("test", "unknown", "sine.mp3", "./test_audio/sine.mp3", logger)
        song.get_signal()
        self.assertEqual(song.sample_rate, 44100)
        self.assertTrue(song.signal.tolist() == self.sine_signal)

    # test reading in remote file
    def test_convert_remote_to_signal(self):
        logger = setuplogger(False, "./log/test_log")
        url = "https://ia600209.us.archive.org/12/items/SineWaveStudiosSineWaveTestFile/sinetest.mp3"
        song = Song("test", "unknown", url, "./test_audio", logger)
        song.get_signal()
        self.assertEqual(song.sample_rate, 44100)
        self.assertTrue(song.signal.tolist() == self.sine_signal)



    

if __name__ == '__main__':
    unittest.main()