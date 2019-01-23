# Freezam
a Python command-line application to recognize a real-time recording of a song snippet. The program will match the snippet with the songs in the library and displays the closest match in spectrogram. The project has been tested on Windows and Ubuntu 18.04.1 LTS.

## Getting Started
First, git clone the project into a local git directory shazam. The shazam/Library folder contains pre-downloaded music files. To run the application, the entry point is the freezam.py file under shazam folder. The application has the following functionalities:

#### Add a song to the Library
To add a song to the library, first download the music file (preferably in mp3 or wav format) into the shazam/Library folder. Then run the following command in the terminal: 
```sh
$ python3 freezam.py [-t song_title] [-a artist_name] [--verbose] $(<filename.extension>);
```

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

