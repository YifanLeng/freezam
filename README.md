# Freezam
A Python command-line application to recognize a real-time recording of a song snippet. The program will match the snippet with the songs in the library and displays the closest match in spectrogram. The project has been tested on Windows and Ubuntu 18.04.1 LTS.

## Getting Started
First, git clone the project into a local git directory shazam. The shazam/Library folder contains pre-downloaded music files. To run the application, the entry point is the freezam.py file under shazam folder. The application has the following functionalities:

#### Add a song to the Library
To add a song to the library, first download the music file (preferably in mp3 or wav format) into the shazam/Library folder. Then run the following command in the terminal: 
```
$ python3 freezam.py [-t song_title] [-a artist_name] [--verbose] <filename.extension>;
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
```

Install the python packages with pip3. Make sure the versions are up-to-date. If not, update the packages with:

```
$pip3 install <lib_name> --upgrade

```


## Authors

Yifan Leng

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


