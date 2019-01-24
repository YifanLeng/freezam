# Freezam
A Python command-line application to recognize a real-time recording of a song snippet. The program will match the snippet with the songs in the library and displays the closest match in spectrogram. The project has been tested on Windows and Ubuntu 18.04.1 LTS.

## Getting Started
First, git clone the project into a local git directory shazam. The shazam/Library folder contains pre-downloaded music files. To run the application, the entry point is the freezam.py file under shazam folder. The application has the following functionalities:

#### Add a song to the Library
To add a song to the library, first download the music file (preferably in mp3 or wav format) into the shazam/Library folder. Then run the following command in the terminal: 
```
$python3 freezam.py [-t song_title] [-a artist_name] [--verbose] <filename.extension>;
```

### Identify a recording
Provide a filename in shazam/snippets or an url. If no filename is provided, the program will start recording a snippet to match with songs in the Library.
```
$python3 freezam.py identify [--verbose] <filename.extension or url> 
```

### List the infromation of songs in the PostgreSQL Database
```
$python3 freezam.py [--verbose] list
```

### Prerequisite
#### software:

ffmpeg

libportaudio2 

PostgreSQL 

#### Python packages

NumPy-1.16.0

SciPy-1.2.0

psycopg2

pydub

sounddevice

matplotlib

### Installing

Install the softwares by running on Linux

```
$sudo apt-get install libportaudio2
$sudo apt-get install libasound-dev
$sudo apt install ffmpeg
$sudo apt-get install postgresql-10 
```

Change the line in /etc/postgresql/10/main/pg_hba.conf from
```
local   all             postgres                                peer
```
to
```
local   all             postgres                                trust
```

Install the python packages with pip3. Make sure the versions are up-to-date. If not, update the packages with:
```
$pip3 install <lib_name> --upgrade

```


## Authors

Yifan Leng

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


