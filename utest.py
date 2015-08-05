# unit tests for yanote
import unittest
import entry
import yanote
import utils

class NoteEntryTestCase(unittest.TestCase):
    def setUp(self):
        self.dog_entry1 = entry.Entry("dog", ["a husky dog", "age: 4"])
        self.dog_entry2 = entry.Entry("dog", ["born in Seattle"])
        self.cat_entry = entry.Entry("cat", ["a tabby cat"])

    def test_merge(self):
        self.dog_entry1.merge(self.dog_entry2)
        merged_note = ["a husky dog", "age: 4", "born in Seattle"]
        self.assertEqual(self.dog_entry1.key, "dog")
        self.assertEqual(self.dog_entry1.note, merged_note)
        with self.assertRaises(utils.YantException):
            self.dog_entry1.merge(self.cat_entry)
        # reset merged note entry
        self.dog_entry1 = entry.Entry("dog", ["a husky dog", "age: 4"])
    
   def test_exec_cmd(self):
       pass
        
    ''' nothing to do here, Python does GC
    '''
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
