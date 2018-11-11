class Song:
    def __init__(self, rate, signal):
        self.data = {}
        self.data["sample_rate"] = rate
        self.data["signal"] = Song.ndarray_to_list(signal)
    
    @staticmethod
    def ndarray_to_list(arr):
        if isinstance(arr, list):
            return arr
        else:
            return arr.tolist()
    
    def set_info(self, title, artist, filename):
        self.data["title"] = title
        self.data["artist"] = artist
        self.data["filename"] = filename

    def set_signature(self, signature):
        self.data['signature'] = Song.ndarray_to_list(signature)
    
    def set_key(self, key):
        """
        set the key of a song in the remote database
        where the song's signature at each window is stored
        Parameters
        ----------
        key : string
        The key of the song.
        Returns
        -------
        None
        """
        self.data["key"] = key

    def set_path(self, path):
        """
        set the path of a song
        Parameters
        ----------
        path : string
        The filepath of the song or the url
        Returns
        -------
        None
        """
        self.data["path"] = path

    def get_data(self):
        return self.data

  
    
    
   
