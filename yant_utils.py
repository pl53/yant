import os
import re
import configparser
import hashlib

class YantException(Exception):
    def __init__(self, s):
        self.value = s
    def __str__(self):
        return str(self.value)

def get_config_parser():
    main_base = os.path.dirname(__file__)
    config_file = os.path.join(main_base, 'yant.cfg')
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def get_data_path():
    note_path = os.getenv("YANT_PATH")
    #note_path = "./devo_data"
    if note_path == None:
        note_path = os.path.join(os.getenv("HOME"), ".yanote")
    if not os.path.exists(note_path):
        os.makedirs(note_path)
    return note_path

def list_all_books():
    # retrive current notebooks
    note_path = get_data_path()
    all_files = os.listdir(note_path)
    db_files = [f for f in all_files if f.endswith(".db")]
    current_books = [name[:-3] for name in db_files]
    return current_books

def validate_name(pattern, name, exception_msg=""):
    if not re.match(pattern, name):
        if exception_msg == "":
            exception_msg = "'" + name + "' doesn't match required pattern " + pattern
        raise Exception(exception_msg) 

def hashkey(s):
    '''
        Generate a 28 bits (7 hex digits) hashcode
        Birthday attach prob.: (0.01, 2322), (0.001, 732), (0.0001, 231)
        In case of collision, we can still use raw key for the dict
    '''
    md5 = hashlib.md5(bytearray(s, 'utf-8'))
    hexdigest = md5.hexdigest()
    return hexdigest[:7]

def quote_multi_words(s):
    ''' add single-quote to string if it contains whitespace'''
    if len(s.split()) > 1:
        # s contains whitespace
        return "'" + s + "'"
    else:
        return s
