import unittest
import numpy as np
from random import gauss, seed
from scipy import signal
from spectral_analysis import sliding_window
from spectral_analysis import get_windowed_signals
from spectral_analysis import get_spectrograms
from spectral_analysis import get_signature



class TestSpectralAnalysis(unittest.TestCase):
    def setUp(self):
        self.line = np.array([1,2,3,4,5])
        # sampling frequency
        self.fs = 44100
        # a two second sine wav
        self.sine = np.sin(np.arange(self.fs * 2))
        # a two second white noise
        seed(1)
        self.wn = np.array([gauss(0,1) for i in range(2 * self.fs)])
        # small sine wave to test periodogram
        self.sine_small = np.sin(np.arange(1, 101))
        
    def test_sliding_window(self):
        sli_windows_w1s1 = sliding_window(self.line, 1, stepsize=1)
        self.assertTrue((np.array([[1],[2], [3], [4],[5]]) == \
                         sli_windows_w1s1).all())
        sli_windows_w3s1 = sliding_window(self.line, 3, stepsize=1)
        self.assertTrue((np.array([[1,2,3], [2,3,4], [3,4,5]]) == \
                         sli_windows_w3s1).all())
        sli_windows_w1s3 = sliding_window(self.line, 1, stepsize=3)
        self.assertTrue((np.array([[1], [4]]) == \
                         sli_windows_w1s3).all())
        sli_windows_w3s3 = sliding_window(self.line, 3, stepsize=3)
        self.assertTrue((np.array([[1,2,3]]) == \
                         sli_windows_w3s3).all())

    def test_get_windowed_signals(self):
        size = int(round(1 * self.fs))
        stepsize = int(round(0.1 * self.fs))
        signals = sliding_window(self.sine, size, stepsize)
        window = signal.get_window("hann", signals.shape[-1])
        windowed_signals = np.multiply(signals, window)
        self.assertTrue(np.allclose(windowed_signals, \
                  get_windowed_signals(self.sine, self.fs, "hann", 1, 0.1)))

        size = int(round(1 * self.fs))
        stepsize = int(round(0.1 * self.fs))
        signals = sliding_window(self.wn, size, stepsize)
        window = signal.get_window("hann", signals.shape[-1])
        windowed_signals = np.multiply(signals, window)
        self.assertTrue(np.allclose(windowed_signals, \
                  get_windowed_signals(self.wn, self.fs, "hann", 1, 0.1)))

    def test_get_spectrograms(self):
        sptrogm = get_spectrograms(self.fs, self.sine_small, 100/self.fs, 0.1)
        # use the first windowed signal as test
        f_test = np.array(sptrogm[0][0])
        Pxx_test = np.array(sptrogm[0][1])
        # the freqencies on which to estimate spectrogram are k/100 * 1
        # where 0 <= k <= 50
        # So the frequencies are [0, 0.01, 0.02 ... 0.05]
        print(np.max(Pxx_test))
        freq = np.arange(0, 0.51, 0.01)
        self.assertTrue(np.allclose(freq, np.round(f_test, 2)))
        # According to the formula in the handout, the maximum spectrogram is
        # calculated to be 22.69697
        self.assertTrue(np.allclose(22.69697, np.max(np.round(Pxx_test, 5))))

    def test_get_signature(self):
        # the 5 frequencies that match the largest 5 
        #  magnitudes in spectral density are [0.12, 0.13, ... 0.16]
        signature = np.arange(0.12, 0.17, 0.01)
        sptrogm = get_spectrograms(self.fs, self.sine_small, 100/self.fs, 0.1)
        self.assertTrue(np.allclose(signature, get_signature(sptrogm, 5)))
        

if __name__ == '__main__':
    unittest.main()