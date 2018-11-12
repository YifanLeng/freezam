import argparse
from io_manager import add
from io_manager import identify
from io_manager import listSongs

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
    parser_add.set_defaults(func=add)
    

    # creat the parser for the "identiy" command
    parser_idfy = subparsers.add_parser('identify', help='identify a song in \
                                         the library')
    parser_idfy.add_argument("filename", help='file name in /Search directory or \
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
