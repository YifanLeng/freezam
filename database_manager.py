import json
import numpy as np
import os
from scipy import spatial
import sys

class Database:
    def __init__(self, path):
        self.path = path

    def save_to_database(self, song):
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
        filename = song.filename
        song_dict = {}
        song_dict["title"] = song.title
        song_dict["artist"] = song.artist
        song_dict["signature"] = song.signature
        song_dict["sample_rate"] = song.sample_rate
        songname = filename.split(".")[0]
        filePath = os.path.join(self.path, songname + '.json')
        with open(filePath, 'w') as fp:
            json.dump(song_dict, fp)
        # add the song' signatures 

    def remove_from_database(self, filename, logger):
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
        f = os.path.join(self.path, filename)
        try:
            os.remove(f)
        except:
            logger.error("Failed tp remove {} from the database".format)
        

    def slowSearch(self, signature, threshold, logger):
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
         # set the initial search space to be the whole library
        database = self.path
        # start matching from the start of a song's signature
        search_space = [f for f in os.listdir(database) if f.endswith('.json')]
        matched_result = []
        # load all the songs' signatures
        for fname in search_space:
            f = open(database + fname)
            song = json.loads(f.read())
            f.close()
            # convert to 2D numpy array
            
            song_signature = np.asarray(song['signature'], dtype=np.float32)
            logger.info("start matching with {}".format(fname))
            #if Database.match(signature, song_signature, threshold):
            #    matched_result.append(fname)
            matched_result.append(Database.match(signature, song_signature, threshold))
        song_idx = matched_result.index(min(matched_result))
        return search_space[song_idx]

    @staticmethod
    def match(snip_sig, song_sig, threshold):
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
        dissimilarity = [sys.maxsize]

        if len(snip_sig) > len(song_sig):
            m = len(snip_sig)
            n = len(song_sig)
            diff = m-n
            snip_sig = snip_sig[(n-diff):n]
        snip_start = snip_sig[0]
        for i in range(len(song_sig)):
            # find the start of the window that matched the start of the snippet
            # if np.allclose(snip_start, song_sig[i], atol = threshold):
            d = spatial.distance.cosine(snip_start, song_sig[i])
            if d < threshold:
                k = len(snip_sig)
                if i+k > len(song_sig):
                    break
                dis_snip = []
                for j in range(1, k):
                    #if spatial.distance.cosine(snip_sig[j], song_sig[i+j]) > threshold:
                    #    return False
                    dis_snip.append(spatial.distance.cosine(snip_sig[j], song_sig[i+j]))
                #return True
                dissimilarity.append(sum(dis_snip)/len(dis_snip))
        return min(dissimilarity)


        

   
            
                       
                





        
        

