# unit tests for yanote
import unittest
import entry
import yant
import yant_utils

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
        with self.assertRaises(Exception):
            self.dog_entry1.merge(self.cat_entry)
        # reset merged note entry
        self.dog_entry1 = entry.Entry("dog", ["a husky dog", "age: 4"])

    def test_delete(self):
        self.dog_entry1.delete(1)
        self.assertEqual(self.dog_entry1.note, ["a husky dog"])
        self.dog_entry1.note.append("age: 4")
    
    def test_exec_cmd(self):
        self.dog_entry1.weight = 1
        self.dog_entry1.exec_cmd("y")
        self.assertEqual(self.dog_entry1.weight, 0)
        # when weight is 0, no longer decrease
        self.dog_entry1.exec_cmd("y")
        self.assertEqual(self.dog_entry1.weight, 0)
        self.dog_entry1.exec_cmd("n")
        self.assertEqual(self.dog_entry1.weight, 1)
        self.dog_entry1.weight = 4
        self.dog_entry1.exec_cmd("n")
        self.assertEqual(self.dog_entry1.weight, 5)
        self.dog_entry1.exec_cmd("d")
        self.assertEqual(self.dog_entry1.weight, 0)
        with self.assertRaises(KeyboardInterrupt):
            self.dog_entry1.exec_cmd("q")
        
    def tearDown(self):
        ''' nothing to do here, Python does GC '''
        pass

if __name__ == "__main__":
    unittest.main()
