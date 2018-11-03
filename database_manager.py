import json
class Database:
    def __init__(self, path):
        self.path = path

    def save_to_database(self, song, filename):
        """
        store a song's data into a json file the database
        ----------
        song : dictionary
            a dictionary storing a song's data
        filename :  file, str, or pathlib.Path
            File or filename to which the data is saved. 
        Returns 
        -------
        None
        """
        songname = filename.split(".")[0]
        filePath = self.path + songname + '.json'
        with open(filePath, 'w') as fp:
            json.dump(song, fp)

    def remove_from_database(self, filename):
        """
        remove a song object into the database
        ----------
        filename :  file, str, or pathlib.Path
            File or filename to which the data is saved. 
        Returns 
        -------
        result : int
            0 if the removal fails and 1 if it succedds
        """
        pass

    
    def slowSearch(self, signature, threshold):
        """
        match the signature of a song with the signatures
        stored in the data base
        ----------
        signature : numpy array
            the signature we compute for a snippet
        threshold : float
            the error we allowed for the match
        Returns 
        -------
        result : list
            a list of song objects
            or an empty list if no match is found
        """
        pass


    def match(self, signature, threshold):
        """
        match the signature of a song with the signatures
        stored in the data base
        ----------
        signature : numpy array
            the signature we compute for a snippet
        threshold : float
            the error we allowed for the match
        Returns 
        -------
        result : list
            a list of tuples with (title, artist, song's name)
            or an empty list if no match is found
        """
        pass

