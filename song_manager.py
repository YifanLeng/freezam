import os
import re
from pydub import AudioSegment
import numpy as np
import urllib.request
import scipy.io.wavfile
from spectral_analysis import get_spectrograms, get_signature
import matplotlib.pyplot as plt


class Song:
    def __init__(self, title, artist, filename, path, logger):
        self.title = title
        self.artist = artist
        self.filename = filename
        self.logger = logger
        self.signal = []
        self.spectrogram = [] 
        self.sample_rate = 44100
        self.path = path
        self.signature = []
    
    @staticmethod
    def read_and_convert_to_signal(filepath):
        """
        convert the valid audio file into the numpy arrays
        ----------
        directory : string
            the directory of the audio files
        filename :  file, str, or pathlib.Path
            filename of the audio
        Returns 
        -------
        (rate, signal) : tuple
            rate is the sampling rate of the audio file.
            signal include the numpy arrays of each channel of the wav files
        """
        rate, signal = None, None
        filename = os.path.basename(filepath)
        #TODO: read audio in other formats
        if not filename.endswith(".wav"):
            audio = AudioSegment.from_mp3(filepath)
            wav_path = filepath[:-4] + ".wav"
            wav = audio.export(wav_path, format="wav")
            wav_path = wav.name
            (rate, signal) = scipy.io.wavfile.read(wav_path)
        else:
            (rate, signal) = scipy.io.wavfile.read(filepath)
        return (rate, signal)
    
    @staticmethod
    def convert_file_to_signal(filePath, logger):
        """
        check the validity of the audio file
        and convert the valid audio file into numpy array
        ----------
        filePath :  file, str, or pathlib.Path
            filePath of the audio
        Returns 
        -------
        (rate, signal) : tuple
            rate is the sampling rate of the audio file.
            signal include the numpy arrays of each channel of the wav files
        """
        # TODO: handle remote file
        # check if file is a supported sound file 
        accept_formats = [".wav", ".mp3", ".ogg", ".flv", ".mp4", ".wma", ".aac"]
        formats = re.compile("|".join(accept_formats))
        isFile = formats.search(filePath)
        rate, signal = None, None
        # find the path of the file
        if isFile is None:
            logger.error("Invalid sound file format")
            raise Exception("Invalid sound file format \
                            only accept wav, mp3, ogg, flv, mp4, wma and aac")
        elif not os.path.exists(filePath):
            logger.error("Sound file not found in {}".format(filePath))
            raise Exception("Sound file not found in "+filePath)
        else:
            try:
                # read in the sound file and convert to wav
                (rate, signal) = Song.read_and_convert_to_signal(filePath)
            except Exception:
                logger.error("Failed to convert the sound file {} to wav format".format(filePath))
        return (rate, signal)

    def get_signal(self):
        """
        check the path of the audio file, download the file if
        the path is url, and convert the valid audio file into numpy array
        (transformed to mono channel if the audio file is stereo)
        ----------
        None
        Returns 
        -------
        (rate, signal) : tuple
            rate is the sampling rate of the audio file.
            signal include the numpy arrays of each channel of the wav files
        """
        logger = self.logger
        filename = self.filename
        if filename.startswith("http"):
            print("=========downloading the audio file===================")
            url = filename
            name = url.split('/')[-1]
            (filepath, _) = urllib.request.urlretrieve(url, os.path.join(self.path, name))
            (rate, signal) = Song.convert_file_to_signal(filepath, logger)
        else:
            (rate, signal) = Song.convert_file_to_signal(self.path, logger)
       
        num_channels = signal.shape[-1]
        # turn stereo into mono signal
        if num_channels == 2:
            # take the mean of the two channels
            mono_signal = np.mean(signal, axis=1)
        else:
            mono_signal = signal
        # update Song attributes
        self.sample_rate = rate
        self.signal = mono_signal
        return (rate, mono_signal)

    def get_spectrogram(self, plot):
        """
        compute and plot (optional) the spectrogram of the
        audio file with a frequency resolution of 10.7Hz
        ----------
        plot :  bool
            control the generation of the spectrogram plot
        Returns 
        -------
        spectrogram : list of (f, p) tuples
            a list of the frequency, power tuples for each window.
        """
        sample_rate = self.sample_rate
        signal = self.signal
        if len(signal) == 0:
            (sample_rate, signal) = self.get_signal()
        # fix the frequency resolution to be 10.7Hz 
        # calculate the window width = sample_rate/resolution
        resolution = 10.7
        width = int(sample_rate/resolution)
        shift = int(width/2)
        spectrogram = get_spectrograms(sample_rate, signal, width, shift, window_type="hann")
        self.spectrogram = spectrogram
        if plot:
            plot_name = "./spectrograms/"+self.filename[:-4]+".png"
            plt.specgram(signal,Fs=sample_rate)
            plt.savefig(plot_name)
        return spectrogram

    def get_songSignature(self, k):
        """
        compute the signature of the audio file with 
        the signature method in spectral_analysis.py
        ----------
        k : int
            the dimenstion of the signature in a window
        Returns 
        -------
        signature : list of k-length lists
            a list of the signatures computed for each window.
        """
        spectro = self.spectrogram
        if len(spectro) == 0:
            spectro = self.get_spectrogram(False)
        signature = get_signature(spectro, k)
        self.signature = signature
        return signature
        

