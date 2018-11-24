import os
from urllib.parse import urlparse
from pydub import AudioSegment 
import numpy as np
import urllib.request
import scipy
import scipy.io.wavfile
import logging

def setuplogger(verbose, logFile):
    # create a logger for warnings
    logging.captureWarnings(True)
    warnings_logger = logging.getLogger('py.warnings')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(logFile)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    warnings_logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    warnings_logger.addHandler(stream_handler)
    if verbose:
        logger.addHandler(stream_handler)
    return logger

def convert_local_to_wav(localPath, libPath):
    """
    convert the local audio file to wav format
    ----------
    localPath : string
        the local file path that points to the local audio file
    libPath : string
        the path where the converted wav file is stored
    Returns 
    -------
    wavPath : 
        the path that points to the converted file
    """
    # check if the local file exists
    if not os.path.isfile(localPath):
        raise Exception('Local file: {} does not exist'.format(localPath))
    else:
        filename = os.path.basename(localPath)
        extension = filename.split('.')[-1]
        # no conversion needed for wav file
        if extension == 'wav':
            return localPath

        read_methods = {'mp3': AudioSegment.from_mp3,
                        'ogg': AudioSegment.from_ogg,
                        'flv': AudioSegment.from_flv,
                        'mp4': AudioSegment.from_file,
                        'wma': AudioSegment.from_file,
                        'aac': AudioSegment.from_file}
        if extension in ['mp3', 'ogg', 'flv']:
            audio = read_methods[extension](localPath)
        else:
            audio = read_methods[extension](localPath, extension)
        # export the audio to a wav file
        base = os.path.splitext(filename)[0]
        wav_filename = base + '.wav'
        wav_path = os.path.join(libPath, wav_filename)
        wav = audio.export(wav_path, format="wav")
        return wav.name

        
def convert_path_to_wav(filePath, libPath):
    """
    decode the filepath and convert the audio that the path
    points to into wav file and store the wav file in the libPath
    ----------
    filePath : string
        the path that points to the audio file. The filePath could
        be a local directory or an URL
    libPath : string
        the path where the converted wav file is stored
    Returns 
    -------
    wavfilePath : String
        the local directory of the converted wav file
    """
    if filePath.startswith("http"):
        # download the remote file to Library and convert to wav
        url = filePath
        parse = urlparse(url)
        filename = os.path.basename(parse.path)
        (filepath, _) = urllib.request.urlretrieve(url, os.path.join(libPath, filename))
        wavPath = convert_local_to_wav(filepath, libPath)
    elif filePath.endswith((".wav", ".mp3", ".ogg", ".flv", ".mp4", ".wma", ".aac")):
        # the filePath points to a local file, convert the file to wav
        wavPath = convert_local_to_wav(filePath, libPath)
    else:
        raise Exception("Invalid File type")
    return wavPath
        
        
def convert_to_signal(filePath, libPath):
    """
    convert the valid audio file into the numpy arrays
    ----------
    filePath : string
        a path to a local directory or url that points to an audio file
    libPath :  string
        the local directory that contains the audio files
    Returns 
    -------
    (rate, signal) : tuple
        rate is the sampling rate of the audio file.
        signal is the numpy arrays of the avergae of channels of the wav files
    """
    # convert the audio file that the filePath points to into wav file
    wavPath = convert_path_to_wav(filePath, libPath)
    (rate, signal) = scipy.io.wavfile.read(wavPath)
    # delete the converted wav files if the original file is not wav format
    # if not filePath.endswith(".wav"):
        # os.remove(wavPath)
    num_channels = signal.shape[-1]
    # turn stereo into mono signal
    if num_channels == 2:
        # take the mean of the two channels
        mono_signal = np.mean(signal, axis=1)
    else:
        mono_signal = signal
    # downsample the signal with a sample rate of 8000 Hz
    out_rate = 8000
    if rate > out_rate:
        ds_factor = int(rate/out_rate)
        mono_signal = scipy.signal.resample_poly(mono_signal, 1, ds_factor)

    return (out_rate, mono_signal)
  



