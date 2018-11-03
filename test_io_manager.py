import unittest
import numpy as np
from io_manager import read_and_convert_to_signal, convert_file_to_signal
import struct

class TestIoManager(unittest.TestCase):
    def setUp(self):
        Fs = 44100
        f = 440
        sample_rate = 44100
        # generate a 10 second sine wave 
        x = np.arange(sample_rate * 10) 
        self.y = 100*np.sin(2 * np.pi * f * x / Fs)
        f = open('test.wav', 'wb')
        for i in self.y:
            f.write(struct.pack('d', i))
        f.close()


    def test_convert_file_to_signal(self):
        (rate, signal) = convert_file_to_signal("./", "test.wav")
        self.assertEqual(rate, 44100)
        self.assertEqual(signal, self.y)

    def test_read_and_convert_to_signal(self):
        (rate, signal) = read_and_convert_to_signal("./", "test.wav")
        self.assertEqual(rate, 44100)
        self.assertEqual(signal, self.y)
    

if __name__ == '__main__':
    unittest.main()