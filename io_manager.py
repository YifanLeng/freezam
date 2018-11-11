import os
import re
# from pydub import AudioSegment
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
        (filepath, _) = urllib.request.urlretrieve(url, './Library/'+name)
        (rate, signal) = convert_file_to_signal("", filepath)
    else:
        (rate, signal) = convert_file_to_signal("./Library/",filename)
    num_channels = signal.shape[-1]
    # turn stereo into mono signal
    if num_channels == 2:
        # take the mean of the two channels
        mono_signal = np.mean(signal, axis=1)
        print(mono_signal.shape)
        print(mono_signal.shape[-1])
    else:
        mono_signal = signal

    song = Song(rate, mono_signal.tolist())
    song.set_info(args.title, args.artist, filename)
    # fix the frequency resolution to be 10.7Hz 
    # calculate the window width = sample_rate/resolution
    resolution = 10.7
    width = int(rate/resolution)
    shift = int(width/2)
    spectro = get_spectrograms(rate, mono_signal, width, shift, window_type="hann")
    signature = get_signature(spectro, k=10)
    song.set_signature(signature)
    # song.set_key(...)
    # song.set_path(...)
    db = Database("./Database/")
    # print(song.get_data())
    db.save_to_database(song.get_data(), filename)

def identify(args):
    filename = args.filename
    (rate, signal) = convert_file_to_signal("./snippets/",filename)
    num_channels = signal.shape[-1]
    # the song has 2 channels
    if num_channels == 2:
        # take the mean of the two channels
        mono_signal = np.mean(signal, axis=1)
    else:
        mono_signal = signal
    resolution = 10.7
    width = int(rate/resolution)
    shift = int(width/2)
    spectro = get_spectrograms(rate, mono_signal, width, shift, window_type="hann")
    signature = get_signature(spectro, k=10)
    db = Database("./Database/")
    # threshold = 1-cosine similarity
    # It measures how disimilar two windows are. 
    # We want threshold to be small
    threshold = 0.2
    print("start identifying")
    matched_result = db.slowSearch(signature, threshold)
    print(matched_result)
    return matched_result


def listSongs(args):
    pass
