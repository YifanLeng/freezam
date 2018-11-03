import unittest
from database_manager import Database
from song_manager import Song
import os

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
        self.song1 = Song(44100, [1,2,3,2,1], "test1", "unknown", "test1.wav")
        self.song2 = Song(44100, [2,2,5,0,-1], "test2", "unknown", "test2.wav")
        

    def test_save_to_database(self):
        self.db.save_to_database(self.song1, "test1Obj")
        self.db.save_to_database(self.song2, "test2Obj")
        self.db_files = getListOfFiles("./Database")
        self.assertTrue("test1Obj" in self.db_files)
        self.assertTrue("test2Obj" in self.db_files)
    

    def test_remove_from_database(self):
        self.db.remove_from_database("test1Obj")
        self.db.remove_from_database("test2Obj")
        self.db_files = getListOfFiles("./Database")
        self.assertFalse("test1Obj" in self.db_files)
        self.assertFalse("test2Obj" in self.db_files)

    def test_slowSearch(self):
        self.db.save_to_database(self.song1, "test1Obj")
        self.db.save_to_database(self.song2, "test2Obj")
        self.assertEqual([], self.db.slowSearch([1,1,1,1,1], 2))
        self.assertEqual(["test1Obj"], self.db.slowSearch([1,1,1,1,1], 3))
        self.assertEqual(["test1Obj", "test2Obj"], self.db.slowSearch([1,1,1,1,1], 5))
        

    def test_match(self):
        self.assertEqual([], self.db.slowSearch([1,1,1,1,1], 2))
        self.assertEqual([("test1", "unknown", "test1.wav")], \
                           self.db.slowSearch([1,1,1,1,1], 3))
        self.assertEqual([("test1", "unknown", "test1.wav"), \
                          ("test2", "unknown", "test2.wav")], \
                           self.db.slowSearch([1,1,1,1,1], 5))
        

if __name__ == '__main__':
    unittest.main()