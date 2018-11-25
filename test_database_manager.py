import unittest
from database_manager import Database
from song_manager import Song
import os
from io_manager import setuplogger

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database("localhost", "postgres", "postgres", "Ivan@1995")
        self.logger = setuplogger(False, "./log/test_log")
        self.song1 = Song("sinetest", "unknown", "./test_audio/sinetest.wav", "./test_audio/", False)
        self.song2 = Song("sine", "unknown", "./test_audio/sine.mp3", "./test_audio/", False)
        

    def test_save_to_database(self):
        self.db.save_to_database([self.song1])
        self.db.save_to_database([self.song2])    
        print("test save to db") 
        self.assertTrue(self.db.is_in_database(self.song1))
        self.assertTrue(self.db.is_in_database(self.song2))
    

    def test_remove_from_database(self):
        self.db.remove_from_database([self.song1])
        self.db.remove_from_database([self.song2])
        print("test remove from db") 
        self.assertFalse(self.db.is_in_database(self.song1))
        self.assertFalse(self.db.is_in_database(self.song2))
    

    def test_search(self):
        # a cut snippet (with high sound quality)
        snippet = Song("dvorak_mini_snippet", "dvorak", \
                         "./snippets/dvorak_mini_snippet.wav",
                         "./snippets/", False)
                       
        # a real-worlf recording (with low sound quality)
        recording = Song("who_knew_noise", "pink", "./snippets/who_knew_noise.wav", \
                       "./snippets/", False)
        self.assertEqual("dvorak_miniatures_opus_74a_3.mp3", self.db.search(snippet))
        self.assertEqual("who_knew.mp3", self.db.search(recording))
       
if __name__ == '__main__':
    unittest.main()