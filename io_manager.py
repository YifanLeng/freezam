import os
from database_manager import Database
from song_manager import Song
import logging
import json

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

def add(args):
    """
    compute the song's siganature and add the song's info and 
    signature to the database. 
    ----------
    args : Namespace
        the namespace that was pasrsed from the commind line input
    """
    logger = setuplogger(args.verbose, "./log/add_log")
    filename = args.filename
    if filename.startswith("http"):
        path = "./Library"
    else:
        path = os.path.join("./Library", filename)
 
    song = Song(args.title, args.artist, filename, path, logger)
    song.get_signal()
    song.get_spectrogram(plot=True)
    song.get_songSignature(k=10)
    db = Database("./Database/")
    # print(song.get_data())
    db.save_to_database(song)
    logger.info('Adding the song info and signature: {} to database'.format(filename))

def identify(args):
    """
    compute the snippet's siganature and compare it with the 
    signatures of songs in the database. Return the closest match.
    ----------
    args : Namespace
        the namespace that was pasrsed from the commind line input
    """
    logger = setuplogger(args.verbose, "./log/identify_log")
    filename = args.filename
    if filename.startswith("http"):
        path = filename
    else:
        path = os.path.join("./snippets", filename)
    
    snippet = Song("recording", "user", filename, path, logger)
    snippet.get_songSignature(k=10)
    db = Database("./Database/")
    # threshold = 1-cosine similarity
    # It measures how disimilar two windows are. 
    # We want threshold to be small
    threshold = 0.2
    logger.info("start identifying")
    matched_result = db.slowSearch(snippet.signature, threshold, logger)
    print(matched_result)
    logger.info("find the matched song {}".format(matched_result))
    return matched_result


def listSongs(args):
    """
    List a useful summary of the library contents
    ----------
    args : Namespace
        the namespace that was pasrsed from the commind line input
    """
    logger = setuplogger(args.verbose, "./log/list_log")
    logger.info("list a summary of the songs in the library")
    database = "./Database"
    search_space = [f for f in os.listdir(database) if f.endswith('.json')]
    # load all the songs' information
    for fname in search_space:
        f = open(os.path.join(database, fname))
        song = json.loads(f.read())
        f.close()
        info = "The song has title {}, aritst {}, sampling rate {}".format(song['title'], \
                song['artist'], song['sample_rate'])
        logger.info(info)
    
