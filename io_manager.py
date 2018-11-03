import os
import re
from pydub import AudioSegment
import numpy as np
import urllib.request
import scipy.io.wavfile
from spectral_analysis import get_spectrograms, get_signature
from database_manager import Database
from song_manager import Song


def read_and_convert_to_signal(directory, filename):
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
    filepath = directory+filename
    rate, signal = None, None
    #TODO: read audio in other formats
    if not filename.endswith(".wav"):
        audio = AudioSegment.from_mp3(filepath)
        wav_filename = filename[:-4] + "_wav.wav"
        wav_path = directory + wav_filename
        wav = audio.export(wav_path, format="wav")
        wav_path = wav.name
        (rate, signal) = scipy.io.wavfile.read(wav_path)
    else:
        (rate, signal) = scipy.io.wavfile.read(filepath)
    return (rate, signal)

def convert_file_to_signal(directory, filename):
    """
    cheack the validity of the audio file
    download the audio file given its url
    convert audio file into the numpy arrays
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
    # TODO: handle remote file
    # check if file is a supported sound file 
    accept_formats = [".wav", ".mp3", ".ogg", ".flv", ".mp4", ".wma", ".aac"]
    formats = re.compile("|".join(accept_formats))
    isFile = formats.search(filename)
    rate, signal = None, None
    # find the path of the file
    if isFile is None:
        raise Exception("Invalid sound file type \
                         only accept wav, mp3, ogg, flv, mp4, wma and aac")
    elif not os.path.exists(directory+filename):
        raise Exception("Sound file not found in "+directory)
    else:
        try:
            # read in the sound file and convert to wav
            (rate, signal) = read_and_convert_to_signal(directory, filename)
        except Exception:
            print("Failed to convert the sound file to wav format")
    return (rate, signal)
        

def add(args):
    """
    compute the song's siganature and add the song's info and 
    signature to the database. 
    ----------
    args : Namespace
        the namespace that was pasrsed from the commind line input
    """
    # check if the user provides an audio file or url
    # http://www.music.helsinki.fi/tmt/opetus/uusmedia/esim/a2002011001-e02-128k.mp3
    filename = args.filename
    if filename.startswith("http"):
        print("=========downloading the audio file===================")
        url = filename
        name = url.split('/')[-1]
        (filepath, _) = urllib.request.urlretrieve(url, './Data/'+name)
        (rate, signal) = convert_file_to_signal("", filepath)
    else:
        (rate, signal) = convert_file_to_signal("./Data/",filename)
    mono_signal = signal[:,0]
    song = Song(rate, mono_signal.tolist())
    song.set_info(args.title, args.artist, filename)
    spectro = get_spectrograms(rate, mono_signal, 10, 2, window_type="hann")
    signature = get_signature(spectro, k=5)
    song.set_signature(signature)
    # song.set_key(...)
    # song.set_path(...)
    db = Database("./Library/")
    # print(song.get_data())
    db.save_to_database(song.get_data(), filename)

def identify(args):
    filename = args.filename
    (rate, signal) = convert_file_to_signal("./Data/",filename)
    mono_signal = signal[:,0]
    spectro = get_spectrograms(rate, mono_signal, 10, 2, window_type="hann")
    signature = get_signature(spectro, k=5)


def listSongs(args):
    pass