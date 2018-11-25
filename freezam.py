import argparse
from io_manager import setuplogger, getListOfFiles
import os
import json
from song_manager import Song
from database_manager import Database
import sounddevice as sd
import numpy as np

def add(args):
    """
    compute the song's siganature and add the song's info and 
    signature to the database. 
    ----------
    args : Namespace
        the namespace that was pasrsed from the commind line input
    """
    filename = args.filename
    if filename.startswith("http"):
        filePath = filename
    else:
        filePath = os.path.join("./Library", filename)

    libPath = './Library/'
    if args.filename == 'all':
        # adding all songs in the Library folder
        audio_paths = getListOfFiles(libPath)
        db = Database("localhost", "postgres", "postgres", "Ivan@1995")
        songs = []
        for audio_path in audio_paths:
            title = os.path.basename(audio_path)
            artist = "various"
            song = Song(title, artist, audio_path, libPath, True)
            songs.append(song)
            db = Database("localhost", "postgres", "postgres", "Ivan@1995")
            db.save_to_database([song])
            print("{} added".format(title))
    else:
        if args.title is None:
            title = os.path.basename(filePath)
        else:
            title = args.title
        song = Song(title, args.artist, filePath, libPath, True)
        db = Database("localhost", "postgres", "postgres", "Ivan@1995")
        db.save_to_database([song])

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
    if filename is None:
        # record the audio
        print("*recording")
        myrecording = sd.rec(int(30 * 8000), 8000, 2)
        # reshape the recorded signal
        sd.wait()
        print("*end")
        mono_signal = np.mean(myrecording, axis=1)
        sd.play(mono_signal, 8000)
        #myrecording = np.reshape(myrecording, (int(30 * 8000),))
        sd.play(mono_signal, 8000)
        snippet = Song("recording", "user", "from recording", "None", True, mono_signal, 8000)
    else:
        if filename.startswith("http"):
            filePath = filename
        else:
            filePath = os.path.join("./snippets", filename)
            libPath = './Library/'
            snippet = Song("recording", "user", filePath, libPath, True)
    db = Database("localhost", "postgres", "postgres", "Ivan@1995")
    matched_result = db.search(snippet)
    """
    song = Song("demo_1", "various", "./Library/demo_1.wav", libPath, False)
    snippet_keys = ["({},{}):{}".format(h[0], h[1], h[2]) for h in snippet.hash_values]
    song_keys = ["({},{}):{}".format(h[0], h[1], h[2]) for h in song.hash_values]
    # check if there are same keys
    match = []
    
    for k1 in snippet_keys:
        for k2 in song_keys:
            if k1==k2:
                match.append(k1)
    print(len(match))
    """

    logger.info("find the matched song {}".format(matched_result))


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

def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='freezam')
    parser.add_argument('--version', action="store_true",
                        help='current version of freezam')
    subparsers = parser.add_subparsers(dest='subparser_name',\
                         help='sub-command help')
   

    # create the parser for the "add" command
    parser_add = subparsers.add_parser('add', help='add a song to the library')
    parser_add.add_argument('-t', "--title", help='title of the song')
    parser_add.add_argument('-a', "--artist", help='artist of the song')
    parser_add.add_argument("filename", help='audio file name in /Data directory or \
                                              its url')
    parser_add.add_argument('-v', "--verbose", help="verbose mode", action='store_true')
    parser_add.set_defaults(func=add)
    

    # creat the parser for the "identiy" command
    parser_idfy = subparsers.add_parser('identify', help='identify a song in \
                                         the library')
    parser_idfy.add_argument("filename", nargs='?', help='file name in /Search directory or \
                                               its url')
    parser_idfy.add_argument('-v', "--verbose", help="verbose mode", action='store_true')
    parser_idfy.set_defaults(func=identify)

    # creat the parser for the "list" command
    parser_list = subparsers.add_parser('list', help='list all the songs in \
                                         the library')
    parser_list.add_argument('-v', "--verbose", help="verbose mode", action='store_true')
    
    #TODO: implement listSongs function
    parser_list.set_defaults(func=listSongs)

    
    args = parser.parse_args()
    if args.version:
        print("freezam 1.0")
    args.func(args)
    

if __name__ == '__main__':
    main()
