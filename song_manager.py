import os
import re
from io_manager import convert_to_signal
from spectral_analysis import get_spectrogram, get_signature,\
     get_constellation_map, combinatorial_hashing

class Song:
    def __init__(self, title, artist, filePath, libPath, plot, signal=None, sample_rate=None):
        self.title = "unknown" if title is None else title
        self.artist = "various" if artist is None else artist
        self.filename = os.path.basename(filePath)
        self.plot = plot
        if signal is not None and sample_rate is not None:
            (self.sample_rate, self.signal) = (sample_rate, signal)
        else:
            (self.sample_rate, self.signal) = convert_to_signal(filePath, libPath)
        self.spectrogram = get_spectrogram(self.sample_rate, self.signal, self.sample_rate,
                                           int(self.sample_rate/2), self.filename, self.plot)
        self.constellation_map = get_constellation_map(self.spectrogram, self.filename, self.plot)
        self.hash_values = combinatorial_hashing(self.constellation_map)    
        self.path = filePath
        # self.signature = get_signature(self.spectrogram, 10)
    
    