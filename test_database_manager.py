import unittest
from database_manager import Database
from song_manager import Song
import os
from io_manager import setuplogger

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database("./Database")
        self.logger = setuplogger(False, "./log/test_log")
        self.song1 = Song("test1", "tester", "test1.wav", "./test/test1.wav", self.logger)
        self.song2 = Song("test2", "tester", "test2.wav", "./test/test2.wav", self.logger)
        

    def test_save_to_database(self):
        self.db.save_to_database(self.song1)
        self.db.save_to_database(self.song2)
        self.db_files = getListOfFiles("./Database")
        self.assertTrue("./Database\\test1.json" in self.db_files)
        self.assertTrue("./Database\\test2.json" in self.db_files)
    

    def test_remove_from_database(self):
        self.db.remove_from_database("test1.wav", self.logger)
        self.db.remove_from_database("test2.wav", self.logger)
        self.db_files = getListOfFiles("./Database")
        self.assertFalse("./Database\\test1.json" in self.db_files)
        self.assertFalse("./Database\\test2.json" in self.db_files)
    
        
        

    def test_slowSearch(self):
        snippet = Song("snippet", "unknown", "demo_1_snippet.wav", \
                       "./snippets/demo_1_snippet.wav", self.logger)
        snippet.get_songSignature(k=10)
        threshold = 0.2
        self.assertEqual("demo_1", self.db.slowSearch(snippet.signature, threshold, self.logger))
        self.assertEqual(None, self.db.slowSearch(self.song1.signature, threshold, self.logger))
        
if __name__ == '__main__':
    unittest.main()