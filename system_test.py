import unittest
import subprocess
import sys
import os

def my_command_call(command, input_string=None):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, \
                         stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.communicate(input=input_string)
    return result[0]

#YANT = './yant.py'
YANT = '/usr/local/yant/yant.py'

class SystemTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SystemTest, self).__init__(*args, **kwargs)

        pwd = my_command_call(['pwd']).strip()
        my_command_call(['mkdir', 'devo'])
        # set data dir
        os.environ['YANT_PATH'] =  os.path.join(pwd, 'devo')
        self.yant_path = os.getenv('YANT_PATH')

    def setUp(self):
        my_command_call([YANT, 'create', '-b', 'whereIs', '--desc', \
                         'A notebook for finding my personal belongings'])
        my_command_call([YANT, 'add', '-b', 'whereIs', 'item1'], 'location1\n\n')
        my_command_call([YANT, 'add', '-b', 'whereIs', 'item2'], 'location2\n\n')
        my_command_call([YANT, 'add', '-b', 'whereIs', 'item3'], 'location3\n\n')

    def test_list(self):
        ls_output1 = my_command_call([YANT, 'list'])
        self.assertIn('whereIs', ls_output1)
        self.assertIn('scratchpad', ls_output1)
        ls_output2 = my_command_call([YANT, 'list', '-b', 'whereIs'])
        self.assertIn('for finding my personal belongings', ls_output2)

    def test_find(self):
        find_output = my_command_call([YANT, 'find', '-b', 'whereIs', 'item2'])
        self.assertIn('location2', find_output)
        self.assertNotIn('location1', find_output)
        find_output = my_command_call([YANT, 'find', '-b', 'whereIs', 'location3'])
        self.assertIn('location3', find_output)
        self.assertIn('item3', find_output)
        self.assertNotIn('location1', find_output)

    def test_delete(self):
        my_command_call([YANT, 'delete', '-b', 'whereIs', 'item3'])
        find_output = my_command_call([YANT, 'find', '-b', 'whereIs', 'item3'])
        self.assertNotIn('location3', find_output[1])

    def test_review(self):
        review_output = my_command_call([YANT, 'review', '-b', 'whereIs'], '\n\n\n\n\n\n')
        self.assertEqual(review_output.count('Remember this flashcard?'), 3) 

    def test_tag(self):
        ls_output = my_command_call([YANT, 'list', '-b', 'whereIs'])
        self.assertIn('all', ls_output)
        self.assertNotIn('tag1', ls_output)
        my_command_call([YANT, 'tag', '-b', 'whereIs', 'tag1;tag2'])
        ls_output = my_command_call([YANT, 'list', '-b', 'whereIs'])
        self.assertIn('tag1', ls_output)
        self.assertIn('tag2', ls_output)

    def test_export_import(self):
        export_file = os.path.join(self.yant_path, 'whereIs.ex')
        my_command_call([YANT, 'export', '-b', 'whereIs', '--file', export_file])
        my_command_call([YANT, 'create', '-b', 'whereIs2', '--desc', \
                          'A notebook for finding my personal belongings'])
        my_command_call([YANT, 'import', '-b', 'whereIs2', '--file', export_file])
        find_output = my_command_call([YANT, 'find', '-b', 'whereIs2', 'item2'])
        self.assertIn('location2', find_output)
        self.assertNotIn('location1', find_output)

    def test_update(self):
        my_command_call([YANT, 'update', '-b', 'whereIs', 'item1'], 'r1\nlocation_1\n\n')
        find_output = my_command_call([YANT, 'find', '-b', 'whereIs', 'item1'])
        self.assertIn('location_1', find_output)
        self.assertNotIn('location1', find_output)

        my_command_call([YANT, 'update', '-b', 'whereIs', 'item2'], 'a\nlocation_2\n\n')
        find_output = my_command_call([YANT, 'find', '-b', 'whereIs', 'item2'])
        self.assertIn('location2', find_output)
        self.assertIn('location_2', find_output)

        my_command_call([YANT, 'update', '-b', 'whereIs', 'item3'], 'd1\n\n')
        find_output = my_command_call([YANT, 'find', '-b', 'whereIs', 'item3'])
        self.assertNotIn('location3', find_output)
        
    def tearDown(self):
        my_command_call([YANT, 'destroy', '-b', 'whereIs'], 'y\n')
        my_command_call([YANT, 'destroy', '-b', 'whereIs2'], 'y\n')

if __name__ == '__main__':
    unittest.main()
