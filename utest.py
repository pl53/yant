# unit tests for yanote
import unittest
import flashcard
import yant
import yant_utils

class FlashcardTestCase(unittest.TestCase):
    def setUp(self):
        self.dog_flashcard1 = flashcard.Flashcard("dog", ["a husky dog", "age: 4"])
        self.dog_flashcard2 = flashcard.Flashcard("dog", ["born in Seattle"])
        self.cat_flashcard = flashcard.Flashcard("cat", ["a tabby cat"])

    def test_merge(self):
        self.dog_flashcard1.merge(self.dog_flashcard2)
        merged_flashcard = ["a husky dog", "age: 4", "born in Seattle"]
        self.assertEqual(self.dog_flashcard1.key, "dog")
        self.assertEqual(self.dog_flashcard1.note, merged_flashcard)
        with self.assertRaises(Exception):
            self.dog_flashcard1.merge(self.cat_flashcard)
        # reset merged flashcard flashcard
        self.dog_flashcard1 = flashcard.Flashcard("dog", ["a husky dog", "age: 4"])

    def test_delete(self):
        self.dog_flashcard1.delete(1)
        self.assertEqual(self.dog_flashcard1.note, ["a husky dog"])
        self.dog_flashcard1.note.append("age: 4")
    
    def test_exec_cmd(self):
        self.dog_flashcard1.weight = 1
        self.dog_flashcard1.exec_cmd("y")
        self.assertEqual(self.dog_flashcard1.weight, 0)
        # when weight is 0, no longer decrease
        self.dog_flashcard1.exec_cmd("y")
        self.assertEqual(self.dog_flashcard1.weight, 0)
        self.dog_flashcard1.exec_cmd("n")
        self.assertEqual(self.dog_flashcard1.weight, 1)
        self.dog_flashcard1.weight = 4
        self.dog_flashcard1.exec_cmd("n")
        self.assertEqual(self.dog_flashcard1.weight, 5)
        self.dog_flashcard1.exec_cmd("d")
        self.assertEqual(self.dog_flashcard1.weight, 0)
        with self.assertRaises(KeyboardInterrupt):
            self.dog_flashcard1.exec_cmd("q")
        
    def tearDown(self):
        ''' nothing to do here, Python does GC '''
        pass

if __name__ == "__main__":
    unittest.main()
